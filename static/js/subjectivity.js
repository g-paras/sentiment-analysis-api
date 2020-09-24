function subject() {
    var chart = new CanvasJS.Chart("subjectivity", {
        animationEnabled: true,
        theme: "light2",
        title: {
            text: "Subjectivity Curve"
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
