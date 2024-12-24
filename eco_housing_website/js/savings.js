// Get the logement ID from localStorage
const logementId = localStorage.getItem("logementId");

// Display logement ID on the page
document.getElementById("logement-id-display").textContent = logementId;

// Function to fetch and display the line chart
async function loadLineChart(timeScale = "weekly") {
    const container = document.getElementById("chart-container");

    try {
        // Fetch data from the server
        const response = await fetch(`http://127.0.0.1:8000/facture-linechart/${logementId}/${timeScale}`);

        if (response.ok) {
            const data = await response.json();

            // Clear previous content
            container.innerHTML = ""; // Clear any existing chart

            // Create a new canvas element
            const canvas = document.createElement("canvas");
            container.appendChild(canvas);

            // Render the line chart
            renderLineChart(canvas, data.data, timeScale);
        } else {
            container.innerHTML = `
                <div class="alert alert-warning">
                    Unable to fetch data. Please try again later.
                </div>
            `;
        }
    } catch (error) {
        console.error("Error fetching line chart data:", error);
        container.innerHTML = `
            <div class="alert alert-danger">
                An error occurred while loading the chart. Please check your connection.
            </div>
        `;
    }
}

// Function to render the line chart using Chart.js
function renderLineChart(canvas, data, timeScale) {
    const ctx = canvas.getContext("2d");

    const labels = new Set();
    const datasets = [];

    // Process data for Chart.js
    data.forEach((item) => {
        const points = item.points.map((point) => {
            labels.add(point.Date);
            return point.Montant;
        });

        datasets.push({
            label: item.Type_fac,
            data: points,
            borderColor: getRandomColor(),
            borderWidth: 2,
            fill: false,
        });
    });

    // Create the line chart
    new Chart(ctx, {
        type: "line",
        data: {
            labels: Array.from(labels).sort(), // Sorted time labels
            datasets: datasets,
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: `Consumption Trends (${timeScale})`,
                },
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: "Time",
                    },
                },
                y: {
                    title: {
                        display: true,
                        text: "Montant (€)",
                    },
                    beginAtZero: true,
                },
            },
        },
    });
}

// Helper function to generate random colors for lines
function getRandomColor() {
    const letters = "0123456789ABCDEF";
    let color = "#";
    for (let i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
}

// Update line chart when time scale is changed
document.getElementById("time-scale-selector").addEventListener("change", (event) => {
    const timeScale = event.target.value; // Get the selected time scale
    loadLineChart(timeScale); // Load the chart with the selected time scale
});

// Load the default line chart (weekly) on page load
loadLineChart();
