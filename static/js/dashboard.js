document.addEventListener("DOMContentLoaded", function () {

    const demandCanvas = document.getElementById("demandChart");

    if (demandCanvas) {

        new Chart(demandCanvas, {
            type: "bar",

            data: {
                labels: ["Current Stock", "Predicted Demand"],

                datasets: [{
                    label: "Units",
                    data: [
                        Number(demandCanvas.dataset.stock),
                        Number(demandCanvas.dataset.demand)
                    ]
                }]
            },

            options: {
                responsive: true,
                plugins: {
                    legend: {
                        display: false
                    }
                }
            }
        });

    }

    const historyCanvas = document.getElementById("historyChart");

    if (historyCanvas) {

        const dates = JSON.parse(historyCanvas.dataset.dates);
        const sales = JSON.parse(historyCanvas.dataset.sales);

        new Chart(historyCanvas, {
            type: "line",

            data: {
                labels: dates,

                datasets: [{
                    label: "Units Sold",
                    data: sales,
                    tension: 0.3
                }]
            },

            options: {
                responsive: true,
                plugins: {
                    legend: {
                        display: true
                    }
                }
            }
        });

    }

});
