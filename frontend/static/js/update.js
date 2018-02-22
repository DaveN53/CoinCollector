$.get('/graph', updateCallback)

update_time = 60 * 1000
setTimeout(poll, update_time);

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
    var ctx = document.getElementById('linechart').getContext('2d');
    var myChart = new Chart(ctx, {
      type: 'line',
      data: {
        labels: graph_data['labels'],
        datasets: [{
          label: graph_data['label'],
          data: graph_data['data'],
          backgroundColor: "rgba(153,255,51,0.4)"
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
                yAxes: [{
                    ticks: {
                        autoSkip: true,
                        maxTicksLimit: 10,
                        min: graph_data['min'],
                        max: graph_data['max']
                    }
                }],
                xAxes: [{
                    ticks: {
                        maxTicksLimit: graph_data['num_labels'],
                    }
                }]
            }
      }
    });
}