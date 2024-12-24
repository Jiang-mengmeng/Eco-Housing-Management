// Get the logement ID from localStorage
const logementId = localStorage.getItem("logementId");

// Display logement ID on the page
document.getElementById("logement-id-display").textContent = logementId;

// Function to ensure Google Charts is loaded
function loadGoogleCharts() {
    return new Promise((resolve, reject) => {
        if (window.google && google.charts) {
            resolve(); // Already loaded
        } else {
            const script = document.createElement("script");
            script.src = "https://www.gstatic.com/charts/loader.js";
            script.onload = () => {
                if (window.google && google.charts) {
                    resolve();
                } else {
                    reject(new Error("Failed to load Google Charts"));
                }
            };
            script.onerror = () => reject(new Error("Failed to load Google Charts"));
            document.head.appendChild(script);
        }
    });
}

// Function to fetch and display the pie chart
async function loadPieChart() {
    const chartContainer = document.getElementById("chart-container");

    try {
        // Ensure Google Charts library is loaded
        await loadGoogleCharts();

        // Fetch the pie chart HTML from the server
        const response = await fetch(`http://127.0.0.1:8000/facture-piechart/${logementId}`);

        if (response.ok) {
            // Get the HTML content
            const chartHtml = await response.text();

            // Inject the HTML content into the chart container
            chartContainer.innerHTML = chartHtml;

            // Execute any <script> tags inside the injected HTML
            const scripts = chartContainer.querySelectorAll("script");
            scripts.forEach(script => {
                const newScript = document.createElement("script");
                if (script.src) {
                    newScript.src = script.src;
                } else {
                    newScript.textContent = script.textContent;
                }
                document.body.appendChild(newScript);
            });
        } else if (response.status === 404) {
            chartContainer.innerHTML = `
                <div class="alert alert-warning">
                    No consumption data available for the specified logement ID.
                </div>
            `;
        } else {
            chartContainer.innerHTML = `
                <div class="alert alert-danger">
                    An error occurred while loading the chart. Please try again later.
                </div>
            `;
        }
    } catch (error) {
        console.error("Error fetching pie chart:", error);
        chartContainer.innerHTML = `
            <div class="alert alert-danger">
                Unable to fetch the chart. Please check your connection and try again.
            </div>
        `;
    }
}

// Load the chart on page load
loadPieChart();
