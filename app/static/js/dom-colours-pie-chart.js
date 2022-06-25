// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';

function updateDomColoursPlot() {
  var url = window.location.pathname
  var splitURL = url.toString().split("/");

  var view = splitURL.at(-2)
  var name = splitURL.at(-1)

  var fetch_url = `/get_dom_colour_data?${view}=` + name;
  fetch(fetch_url)
      .then(function(response) { return response.json(); })
      .then((data) => {
        pieChart = updateDomColoursChart(data, pieChart);
  });
}


function createNewDomColoursChart(data) { 
  var ctx = document.getElementById("myPieChart");
  var domColoursChart = new Chart(ctx, {
    type: 'doughnut',
    data: {
      // labels: Array(data.colours.length).fill("")
      datasets: [{
        data: data.perc,
        backgroundColor: data.colours,
        hoverBackgroundColor: data.colours,
        hoverBorderColor: "rgba(234, 236, 244, 1)",
      }],
    },
    options: {
      maintainAspectRatio: false,
      tooltips: {
        callbacks: {
          label: function(tooltipItem, data) {
            var dataset = data.datasets[tooltipItem.datasetIndex];
            var currentValue = (dataset.data[tooltipItem.index] * 100).toFixed(1);       
            return currentValue + "%";
          }
        },
        backgroundColor: "rgb(255,255,255)",
        bodyFontColor: "#858796",
        borderColor: '#dddfeb',
        borderWidth: 1,
        xPadding: 15,
        yPadding: 15,
        displayColors: false,
        caretPadding: 10,
      },
      legend: {
        display: false
      },
      cutoutPercentage: 0,
    },
})
return domColoursChart
}


function updateDomColoursChart(data, pieChart) {
  if (!pieChart) {
    pieChart = createNewDomColoursChart(data)
  } else {
    pieChart.data = {
      labels: Array(data.colours.length).fill("Percentage"),
      datasets: [{
        data: data.percentages,
        backgroundColor: data.colours,
        hoverBackgroundColor: data.colours,
        hoverBorderColor: "rgba(234, 236, 244, 1)",
      }],
    }
    pieChart.update()
  }
}

