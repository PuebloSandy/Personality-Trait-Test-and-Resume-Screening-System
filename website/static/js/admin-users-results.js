    var agree = document.getElementById("agree").value;
    var cons = document.getElementById("cons").value;
    var extr = document.getElementById("extr").value;
    var neur = document.getElementById("neur").value;
    var opn = document.getElementById("opn").value;
 
    window.onload = function()
    {
        var randomScalingFactor = function() {
            return Math.round(Math.random() * 100);
        };
        var config = {
            type: 'bar',
            data: {
                borderColor : "#fffff",
                datasets: [{
                    data: [
                        agree,
                        cons,
                        extr,
                        neur,
                        opn
                    ],
                    borderColor : "#fff",
                    borderWidth : "3",
                    hoverBorderColor : "#000",
 
                    label: 'Personality Trait Results',
 
                    backgroundColor: [
                        "#0190ff",
                        "#56d798",
                        "#ff8397",
                        "#6970d5",
                        "#f312cb",
                        "#ff0060",
                        "#ffe400"
 
                    ],
                    hoverBackgroundColor: [
                        "#0190ff",
                        "#56d798",
                        "#ff8397",
                        "#6970d5",
                        "#f312cb"
                    ]
                }],
 
                labels: [
                    'Agreeableness',
                    'Conscientiousness',
                    'Extroversion',
                    'Neuroticism',
                    'Openness'
                ]
            },
 
            options: {
                scales: {
                    yAxes: [{
                        ticks: {
                            beginAtZero: true,
                                steps: 10,
                                stepValue: 5,
                                max: 70
                            }
                        }]
                    }
                }
        };
        var ctx = document.getElementById('myChart').getContext('2d');
        window.myPie = new Chart(ctx, config);
    };