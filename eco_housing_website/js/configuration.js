document.getElementById("login-form").addEventListener("submit", async (event) => {
    event.preventDefault(); // Prevent form submission from refreshing the page

    // Get form input values as strings
    const userId = document.getElementById("user-id").value.trim();
    const securityCode = document.getElementById("security-code").value.trim();

    console.log("Sending login data:", { numero_de_telephone: userId, adresse_ip: securityCode });

    try {
        const response = await fetch("http://127.0.0.1:8000/authenticate", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ numero_de_telephone: userId, adresse_ip: securityCode }),
        });

        console.log("Response status:", response.status);

        if (response.ok) {
            const data = await response.json();
            console.log("Response data:", data);

            // Show logement id and proceed to confirmation section
            document.getElementById("logement-id").textContent = data.id_log;
            document.getElementById("login-section").style.display = "none";
            document.getElementById("confirm-section").style.display = "block";
        } else {
            console.error("Invalid credentials response:", await response.text());
            alert("Invalid credentials. Please try again.");
        }
    } catch (error) {
        console.error("Error during login:", error);
        alert("An error occurred while trying to log in. Please try again later.");
    }
});

document.getElementById("confirm-btn").addEventListener("click", async () => {
    const logementId = document.getElementById("logement-id").textContent;

    // Validate logementId
    if (!logementId) {
        alert("Invalid logement ID. Please try again.");
        return;
    }

    // Save logementId in localStorage
    try {
        localStorage.setItem("logementId", logementId);
    } catch (error) {
        console.error("Failed to save logementId to localStorage:", error);
        alert("Unable to save logement details. Please try again.");
        return;
    }

    console.log("Attempting to fetch logement details for ID:", logementId);

    // Fetch logement details
    try {
        const response = await fetch(`http://127.0.0.1:8000/logement/${logementId}`);
        console.log("Fetch response status:", response.status);

        if (response.ok) {
            const data = await response.json();
            console.log("Received logement details:", data);

            // Update DOM with logement details
            document.getElementById("info-logement-id").textContent = data.id_log;
            document.getElementById("info-adresse").textContent = data.adresse;
            document.getElementById("info-ville").textContent = `${data.ville.nom} (Code: ${data.ville.code})`;

            // Show user info section and hide confirmation section
            document.getElementById("confirm-section").style.display = "none";
            document.getElementById("user-info-section").style.display = "block";
        } else {
            const errorMsg = await response.text();
            console.error("Failed to fetch logement details:", errorMsg);
            alert(`Failed to fetch logement details. Server responded with status: ${response.status}`);
        }
    } catch (error) {
        console.error("Error fetching logement details:", error);
        alert("A network error occurred while trying to fetch logement details. Please check your connection.");
    }
});

