$.get('/graph', updateCallback)

update_time = 60 * 1000

Highcharts.setOptions({
        global: {
            useUTC: false
        }
    });

function poll(){
 $.get('/update', updateCallback);
}

graph_data = { 'label' : [], 'graph_data': []}

function updateCallback(data, textStatus){
  $('#time_div').html(data); // just replace a chunk of text with the new text
  $('#eth_price').html(data['value']);
  graph_data = data
  renderGraph()
  setTimeout(poll, update_time);
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
}