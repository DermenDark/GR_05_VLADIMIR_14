const points = JSON.parse(
    document.getElementById("ln-series-data").textContent
);

const xValues = [];
const seriesValues = [];
const mathValues = [];
const differenceValues = [];
let chart;

function generateData(n) {
    xValues.length = 0;
    seriesValues.length = 0;
    mathValues.length = 0;
    differenceValues.length = 0;

    points.forEach(point => {
        const x = Number(point.x);
        let sum = 0;

        // ln(1 - x) = -x - x²/2 - ... - xⁿ/n
        for (let k = 1; k <= n; k++) {
            sum -= Math.pow(x, k) / k;
        }

        xValues.push(x.toFixed(1));
        seriesValues.push(sum);

        const mathFx = Number(point.math_fx);
        mathValues.push(mathFx);

        differenceValues.push(Math.abs(mathFx - sum));
    });
}

function drawChart() {
    const n = Number(document.getElementById("ln-terms").value);

    if (!Number.isInteger(n) || n < 1 || n > 1000) {
        alert("Введите n от 1 до 1000");
        return;
    }

    generateData(n);

    document.getElementById("ln-series-table-body").innerHTML =
        xValues.map((x, i) => `
        <tr>
            <td>${x}</td>
            <td>${seriesValues[i].toFixed(8)}</td>
            <td>${n}</td>
            <td>${mathValues[i].toFixed(8)}</td>
            <td>${differenceValues[i].toFixed(8)}</td>
        </tr>
    `).join("");

    if (chart) chart.destroy();

    chart = new Chart("ln-series-chart", {
        type: "line",

        data: {
            labels: xValues,
            datasets: [
                {
                    label: "Разложение в ряд",
                    data: seriesValues,
                    fill: false,
                    pointRadius: 3,
                    borderColor: "blue"
                },
                {
                    label: "Math F(x)",
                    data: mathValues,
                    fill: false,
                    pointRadius: 3,
                    borderColor: "orange"
                }
            ]
        },

        options: {
            responsive: true,
            maintainAspectRatio: false,

            animation: {
                duration: 5000,
                easing: "easeOutElastic"
            },

            animations: {
                y: {
                    from: 0,
                    duration: 5000,
                    easing: "easeOutElastic"
                }
            },

            plugins: {
                legend: {
                    display: true,
                    position: "top",
                    labels: {
                        color: "#000000",
                        padding: 15,
                        font: {
                            size: 18,
                            weight: "bold"
                        }
                    }
                },
                title: {
                    display: true,
                    text: "Графики ln(1 - x)"
                },

                annotation: {
                    annotations: {
                        zeroLine: {
                            type: "line",
                            xMin: "0.0",
                            xMax: "0.0",
                            borderColor: "red",
                            borderWidth: 3,
                            label: {
                                display: true,
                                content: "x = 0; ln(1) = 0"
                            }
                        }
                    }
                }
            },

            scales: {
                x: {
                    ticks: {
                        color: "#ffffff"
                    },
                    title: {
                        display: true,
                        text: "x — аргумент",
                        color: "#ffffff"
                    },
                    grid: {
                        color: "rgba(255,255,255,0.2)"
                    }
                },

                y: {
                    ticks: {
                        color: "#ffffff"
                    },
                    title: {
                        display: true,
                        text: "F(x) — значение функции",
                        color: "#ffffff"
                    },
                    grid: {
                        color: "rgba(255,255,255,0.2)"
                    }
                }
            }
        }
    });
}

document.getElementById("ln-rebuild")
    .addEventListener("click", drawChart);

document.getElementById("ln-save")
    .addEventListener("click", () => {
        if (!chart) return;

        const link = document.createElement("a");
        link.href = chart.toBase64Image();
        link.download = "ln-chart.png";
        link.click();
    });

drawChart();