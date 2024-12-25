let temperatureChart = null;
let windSpeedChart = null;

// Function to create a chart
function createChart(canvasId, data, label, borderColor, title) {
    const ctx = document.getElementById(canvasId).getContext("2d");

    return new Chart(ctx, {
        type: "line",
        data: {
            labels: data.map(item => item.datetime),
            datasets: [
                {
                    label: label,
                    data: data.map(item => item.value),
                    borderColor: borderColor,
                    borderWidth: 2,
                    fill: false,
                },
            ],
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: title,
                },
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: "Date & Time",
                    },
                },
                y: {
                    title: {
                        display: true,
                        text: label,
                    },
                },
            },
        },
    });
}

// Function to fetch and display the weather forecast
async function fetchWeatherForecast(city) {
    const chartsContainer = document.getElementById("charts-container");

    try {
        // Fetch weather data from the server
        const response = await fetch(`http://127.0.0.1:8000/weather/${city}`);

        if (response.ok) {
            const data = await response.json();

            // Clear old charts
            if (temperatureChart) {
                temperatureChart.destroy();
            }
            if (windSpeedChart) {
                windSpeedChart.destroy();
            }

            // Update city name
            const cityTitle = document.querySelector("h1");
            cityTitle.textContent = `5-Day Weather Forecast for ${data.city}, ${data.country}`;

            // Create temperature chart
            temperatureChart = createChart(
                "temperature-chart",
                data.forecast.map(item => ({
                    datetime: item.datetime,
                    value: item.temperature,
                })),
                "Temperature (°C)",
                "rgba(255, 99, 132, 1)",
                "Temperature Over Time"
            );

            // Create wind speed chart
            windSpeedChart = createChart(
                "wind-speed-chart",
                data.forecast.map(item => ({
                    datetime: item.datetime,
                    value: item.wind_speed,
                })),
                "Wind Speed (m/s)",
                "rgba(54, 162, 235, 1)",
                "Wind Speed Over Time"
            );
        } else {
            chartsContainer.innerHTML = `
                <div class="alert alert-danger">
                    Failed to fetch weather data. Please try again later.
                </div>
            `;
        }
    } catch (error) {
        console.error("Error fetching weather forecast:", error);
        chartsContainer.innerHTML = `
            <div class="alert alert-danger">
                An error occurred while fetching the weather data.
            </div>
        `;
    }
}

// Event listener for form submission
document.getElementById("weather-form").addEventListener("submit", async (event) => {
    event.preventDefault();
    const city = document.getElementById("city").value.trim();
    fetchWeatherForecast(city);
});
