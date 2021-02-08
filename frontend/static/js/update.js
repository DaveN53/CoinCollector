$.get('/graph', updateCallback);

// TODO remove update call
//$.get('/update', updateCallback);

var ONE_MINUTE = 60 * 1000;

function repeatEvery(func, interval) {
    // Check current time and calculate the delay until next interval
    var now = new Date(),
        delay = interval - now % interval;

    function start() {
        // Execute function now...
        func();
        // ... and every interval
        setInterval(func, interval);
    }

    // Delay execution until it's an even interval
    setTimeout(start, delay);
}

function poll(){
    $.get('/update', updateCallback);
}

repeatEvery(poll, ONE_MINUTE);

Highcharts.setOptions({
        global: {
            useUTC: false
        }
    });

graph_data = { 'label' : [], 'graph_data': []}

function updateCallback(data, textStatus){
  $('#time_div').html(data['time']); // just replace a chunk of text with the new text
  $('#eth_price').html(data['value']);
  graph_data = data
  renderGraph()
}

function renderGraph(){
  Highcharts.chart('linehighchart', {

    title: {
        text: graph_data['label']
    },

    subtitle: {
        text: 'Exchange rate over time'
    },
    xAxis: {
                type: 'datetime'
            },
    yAxis: {
        title: {
            text: 'Value: ' + graph_data['label']
        }
    },
    legend: {
        enable: false
    },
    scrollbar: {
        enabled: false
    },

    plotOptions: {
        area: {
            marker: {
                radius: 2
            },
            lineWidth: 2,
            states: {
                hover: {
                    lineWidth: 2
                }
            },
            threshold: null
        },
        series: {
            fillColor: 'rgba(246,216,137,0.4)'
        }
    },

    series: [{
        type: 'area',
        name: 'Price',
        data: graph_data['graph_data']['data'],
        color: 'rgba(244,208,111,1.0)'
        },
        {
        name: 'EMA5',
        data: graph_data['ema5'],
        color: 'rgba(0,153,51,1.0)'
        },
        {
        name: 'EMA12',
        data: graph_data['ema12'],
        color: 'rgba(218,63,16,1.0)'
        },
        {
        name: 'EMA26',
        data: graph_data['ema26'],
        color: 'rgba(16,140,218,1.0)'
        },
        {
        name: 'EMA50',
        data: graph_data['ema50'],
        color: 'rgba(77,0,77,1.0)'
        }
      ]
  });

  // MACD
  Highcharts.chart('macdhighchart', {

    title: {
        text: 'MACD Indicator'
    },
    xAxis: {
                type: 'datetime'
            },
    yAxis: {
        title: {
            text: 'Value'
        },

        plotLines: [{
            color: '#05757a',
            width: 2,
            value: 0 // Need to set this probably as a var.
        }]
    },
    legend: {
        enable: false
    },
    scrollbar: {
        enabled: false
    },

    plotOptions: {
        area: {
            marker: {
                radius: 2
            },
            lineWidth: 2,
            states: {
                hover: {
                    lineWidth: 2
                }
            },
            threshold: null
        },
        series: {
            fillColor: 'rgba(246,216,137,0.4)'
        }
    },

    series: [{
        name: 'macd',
        data: graph_data['macd'],
        color: 'rgba(0,153,51,1.0)'
        },
        {
        name: 'macd_EMA9',
        data: graph_data['ema9'],
        color: 'rgba(218,63,16,1.0)'
        }],
    });
}