function posneg() {

    var chart = new CanvasJS.Chart("posneg", {
        animationEnabled: true,
        theme: "light2", // "light1", "light2", "dark1", "dark2"
        title: {
            text: "Positive and Negative count"
        },
        axisY: {
            title: "Sentence counts"
        },
        data: [{
            type: "column",
            showInLegend: true,
            legendMarkerColor: "grey",
            legendText: "Sentiment",
            dataPoints: [
                { y: 23456, label: "Positive" },
                { y: 23985, label: "Negative" }
            ]
        }]
    });
    chart.render();
}
// dataPoints may vary, these are just for demonstration purpose