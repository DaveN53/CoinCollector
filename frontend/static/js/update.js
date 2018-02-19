update_time = 2000
setTimeout(poll, update_time); // every 10 seconds

function poll(){
 $.get('/update', updateCallback);
}

function updateCallback(data, textStatus){
  $('#time_div').html(data); // just replace a chunk of text with the new text
  $('#eth_price').html(data['value']);
  setTimeout(poll, update_time);
}

var ctx = document.getElementById('linechart').getContext('2d');
var myChart = new Chart(ctx, {
  type: 'line',
  data: {
    labels: ['M', 'T', 'W', 'T', 'F', 'S', 'S'],
    datasets: [{
      label: 'apples',
      data: [12, 19, 3, 17, 6, 3, 7],
      backgroundColor: "rgba(153,255,51,0.4)"
    }, {
      label: 'oranges',
      data: [2, 29, 5, 5, 2, 3, 10],
      backgroundColor: "rgba(255,153,0,0.4)"
    }]
  }
});