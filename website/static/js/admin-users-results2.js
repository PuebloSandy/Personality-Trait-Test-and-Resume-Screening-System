var quality = document.getElementById("qua").value;
var operation = document.getElementById("ope").value;
var supply = document.getElementById("supp").value;
var project = document.getElementById("pro").value;
var datas = document.getElementById("data").value;
var care = document.getElementById("care").value;


var xValues = ["Quality", "Operations", "Supplychain", "Project", "data", "healthcare"];
var yValues = [quality, operation, supply, project, datas, care];
var barColors = ["red", "green","blue","orange","brown","yellow"];

new Chart("pieChart", {
    type: "pie",
    data: {
      labels: xValues,
      datasets: [{
        backgroundColor: barColors,
        data: yValues
      }]
    },
    options: {
      title: {
        display: true,
        text: "Resume Score"
      }
    }
  });