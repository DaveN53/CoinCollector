$.get('/graph', updateCallback)

update_time = 5 * 1000

function poll(){
 $.get('/update', updateCallback);
}

graph_data = { 'labels' : [], 'data': []}

function updateCallback(data, textStatus){
  $('#time_div').html(data); // just replace a chunk of text with the new text
  $('#eth_price').html(data['value']);
  graph_data = data['graph_data']
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
        name: 'Value',
        data: graph_data['data'],
        color: 'rgba(244,208,111,1.0)'
    }],
  });
}