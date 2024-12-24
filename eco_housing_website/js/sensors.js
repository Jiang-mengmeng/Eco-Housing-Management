const logementId = localStorage.getItem("logementId");
document.getElementById("logement-id-display").textContent = logementId;

// Fetch and display sensors for the current logement ID
async function fetchSensors() {
    try {
        const response = await fetch(`http://127.0.0.1:8000/logement/${logementId}/capteurs`);

        if (response.ok) {
            const sensors = await response.json();
            console.log("Fetched sensors:", sensors); // Log the entire response
            const tableBody = document.getElementById("sensors-table-body");
            tableBody.innerHTML = ""; // Clear any previous rows

            sensors.forEach(sensor => {
                const row = document.createElement("tr");
                row.innerHTML = `
                    <td>${sensor.sensor_id}</td>
                    <td>${sensor.type_unit} / ${sensor.type_range}</td>
                    <td>Belongs to ${sensor.piece_name}</td>
                    <td>${sensor.ref_com}</td>
                    <td>${sensor.Port}</td>
                    <td>
                        <button class="btn btn-danger btn-sm" onclick="deleteSensor(${sensor.sensor_id})">
                            Delete
                        </button>
                    </td>
                `;
                tableBody.appendChild(row);
            });
        } else {
            console.error("Failed to fetch sensors:", response.statusText);
            showAlert("Failed to fetch sensors", "danger");
        }
    } catch (error) {
        console.error("Error fetching sensors:", error);
        showAlert("An error occurred while fetching sensors.", "danger");
    }
}

// Add a new sensor
document.getElementById("add-sensor-form").addEventListener("submit", async (e) => {
    e.preventDefault();

    const sensorType = document.getElementById("sensor-type").value;
    const sensorPiece = document.getElementById("sensor-piece").value;
    const sensorRef = document.getElementById("sensor-ref").value;
    const sensorPort = document.getElementById("sensor-port").value;

    try {
        const response = await fetch("http://127.0.0.1:8000/capteurs", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                id_type: parseInt(sensorType),
                id_piece: parseInt(sensorPiece),
                ref_com: sensorRef,
                Port: parseInt(sensorPort),
            }),
        });

        if (response.ok) {
            showAlert("Sensor added successfully!", "success");
            fetchSensors(); // Refresh sensor list
            document.getElementById("add-sensor-form").reset();
        } else {
            const error = await response.json();
            showAlert(error.detail || "Failed to add sensor", "danger");
        }
    } catch (error) {
        console.error("Error adding sensor:", error);
        showAlert("An error occurred while adding the sensor.", "danger");
    }
});

// Delete a sensor
async function deleteSensor(sensorId) {
    if (!confirm("Are you sure you want to delete this sensor?")) return;

    try {
        const response = await fetch(`http://127.0.0.1:8000/capteurs/${sensorId}`, {
            method: "DELETE",
        });

        if (response.ok) {
            showAlert("Sensor deleted successfully!", "success");
            fetchSensors(); // Refresh sensor list
        } else {
            showAlert("Failed to delete sensor", "danger");
        }
    } catch (error) {
        console.error("Error deleting sensor:", error);
        showAlert("An error occurred while deleting the sensor.", "danger");
    }
}

// Show alert messages
function showAlert(message, type) {
    const alertDiv = document.getElementById("alert-message");
    alertDiv.textContent = message;
    alertDiv.className = `alert alert-${type}`;
    alertDiv.classList.remove("d-none");

    setTimeout(() => {
        alertDiv.classList.add("d-none");
    }, 5000);
}

// Fetch sensors on page load
fetchSensors();
