function polar() {
    var chart = new CanvasJS.Chart("polarity", {
        animationEnabled: true,
        theme: "light2",
        title: {
            text: "Polarity Curve"
        },
        data: [{
            type: "line",
            indexLabelFontSize: 16,
            dataPoints: [
                { y: 23 },
                { y: 67 },
                { y: 56 },
                { y: 43 },
                { y: 89 },
                { y: 94 },
                { y: 34 }
            ]
        }]
    });
    chart.render();
}

// these dataPoints may vary, the values used here are just for demonstration purposes