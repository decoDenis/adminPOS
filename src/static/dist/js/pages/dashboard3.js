
$(function () {
  "use strict";

  var ticksStyle = {
    fontColor: "#495057",
    fontStyle: "bold",
  };

  var mode = "index";
  var intersect = true;

  var salesChart = new Chart($salesChart, {
    type: "bar",
    data: {
      labels: _labels,
      datasets: [
        {
          backgroundColor: "#007bff",
          borderColor: "#007bff",
          data: _data,
        },
        {
          backgroundColor: "#ced4da",
          borderColor: "#ced4da",
          data: _data,
        },
      ],
    },
    options: {
      maintainAspectRatio: false,
      tooltips: {
        mode: mode,
        intersect: intersect,
      },
      hover: {
        mode: mode,
        intersect: intersect,
      },
      legend: {
        display: false,
      },
      scales: {
        yAxes: [
          {
            display: false,
            gridLines: {
              display: true,
              lineWidth: "4px",
              color: "rgba(0, 0, 0, .2)",
              zeroLineColor: "transparent",
            },
            // ticks: $.extend(
            //   {
            //     beginAtZero: true,

            //     // Include a dollar sign in the ticks
            //     callback: function (value, index, values) {
            //       if (value >= 1000) {
            //         value /= 1000;
            //         value += "k";
            //       }
            //       return "$" + value;
            //     },
            //   },
            //   ticksStyle
            // ),
          },
        ],
        xAxes: [
          {
            display: true,
            gridLines: {
              display: false,
            },
            ticks: ticksStyle,
          },
        ],
      },
    },
  });

  // var $visitorsChart = $("#visitors-chart");
  // var visitorsChart = new Chart($visitorsChart, {
  //   data: {
  //     labels: [1,2,3,4],
  //     datasets: [
  //       {
  //         type: "line",
  //         data: [100, 120, 170, 167, 180, 177, 160],
  //         backgroundColor: "transparent",
  //         borderColor: "#007bff",
  //         pointBorderColor: "#007bff",
  //         pointBackgroundColor: "#007bff",
  //         fill: false,
  //         pointHoverBackgroundColor: '#007bff',
  //         pointHoverBorderColor    : '#007bff'
  //       },
  //     ],
  //   },
  //   options: {
  //     maintainAspectRatio: false,
  //     tooltips: {
  //       mode: mode,
  //       intersect: intersect,
  //     },
  //     hover: {
  //       mode: mode,
  //       intersect: intersect,
  //     },
  //     legend: {
  //       display: false,
  //     },
  //     scales: {
  //       yAxes: [
  //         {
  //           // display: false,
  //           gridLines: {
  //             display: true,
  //             lineWidth: "4px",
  //             color: "rgba(0, 0, 0, .2)",
  //             zeroLineColor: "transparent",
  //           },
  //           ticks: $.extend(
  //             {
  //               beginAtZero: true,
  //               suggestedMax: 200,
  //             },
  //             ticksStyle
  //           ),
  //         },
  //       ],
  //       xAxes: [
  //         {
  //           display: true,
  //           gridLines: {
  //             display: false,
  //           },
  //           ticks: ticksStyle,
  //         },
  //       ],
  //     },
  //   },
  // });
});
