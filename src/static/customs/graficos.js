var mychart = document.getElementById("chart").getContext("2d");
      steps = 10
      max = {{max}}
      
      new Chart(mychart, {
        
         type: 'bar',
         data: {
            labels: [{% for item in labels %}
                   "{{ item }}",
                  {% endfor %}],
            datasets: [{
               data: [{% for item in values %}
                       "{{ item }}",
                      {% endfor %}],
               backgroundColor: 'rgba(0, 140, 255, 1)',
               borderColor: 'rgba(151,187,205,1)',
               pointBackgroundColor: 'rgba(151,187,205,1)'
              //  fillColor: "rgba(0, 140, 255, 1)",
              //    //  strokeColor: "rgba(151,187,205,1)",
              //     pointColor: "rgba(151,187,205,1)",
            }]
         },
         options: {
            scales: {
               yAxes: [{
                  ticks: {
                    scaleSteps: steps,
                    scaleStepWidth: Math.ceil(max / steps),
                    barShowStroke : true,
                    scaleShowLabels: true,
                    scaleShowGridLines : true,
                    beginAtZero: true,
                    stepSize: 10
                  }
               }]
            }
         }
      });