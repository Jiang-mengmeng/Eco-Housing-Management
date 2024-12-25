# **Eco-Responsible Housing Management System**

## **Overview**
This project aims to create an interactive, responsive internet application for managing an eco-responsible home. It integrates data from sensors and external APIs and visualizes consumption data. The project is structured into three main components: **Database**, **Server**, and **Website**.

---

### **1. Database**

#### **1.1 Structure**
The database, defined in `logement.sql`, follows a relational model with the following tables:
- **Logement**: Stores housing information.
- **Piece**: Represents rooms in a logement.
- **Capteur**: Details sensors/actuators in each room.
- **Type_Capteur**: Defines types of sensors/actuators (e.g., temperature, electricity).
- **Mesure**: Logs measurements from sensors.
- **Facture**: Tracks bills (electricity, water, waste) for each logement.
- **Adresse**, **Ville**, **Location**: Specify address-related information.

#### **1.2 Initialization and Data Filling**
- **Script**: `remplissage.py` initializes the database structure and populates it with sample data.
- **Generated Data**: Includes random `Mesures` and `Factures` for testing and demonstration.

---

### **2. Server**

#### **2.1 REST API**
The server, implemented in `serveur.py`, provides RESTful endpoints to interact with the database:
- **GET Requests**: Retrieve information (e.g., logements, capteurs, mesures, factures).
- **POST Requests**: Add new data (e.g., capteurs, mesures, factures).

#### **2.2 Dynamic HTML Generation**
- **Functionality**: Creates on-the-fly HTML pages for visualizing data.
- **Example**: `index.jinja` generates a pie chart displaying invoice values using Google Charts.

#### **2.3 Weather Integration**
- **Feature**: Fetches 5-day weather forecasts using the OpenWeatherMap API.
- **HTML Integration**: `weather_forecast.html` visualizes the weather data.

#### **2.4 Sensor Integration**
- **Hardware Support**: Integrates DHT11 sensors and ESPs.
- **Example Script**: `POST_tem.ino` feeds temperature data into the database and automates actions (e.g., turning on LEDs).

---

### **3. Website**

#### **3.1 Structure**
The website resides in the `eco_housing_website` directory, with subdirectories for:
- **`css/`**: Stylesheets for consistent and responsive design.
- **`html/`**: HTML files for individual pages.
- **`images/`**: Images used across the site.
- **`js/`**: JavaScript files for dynamic functionalities.

#### **3.2 Pages**
- **Home Page**: An attractive landing page showcasing features.
- **Consumption Page**: Visualizes consumption data with dynamic time scales (daily, weekly, monthly).
- **Sensors Page**: Displays sensor statuses and allows users to add or delete sensors.
- **Savings Page**: Provides comparative graphs of bills over time.
- **Configuration Page**: Manages user login and configuration settings.

#### **3.3 Key Features**
- **Dynamic Charts**: Line and pie charts for data visualization.
- **Responsive Design**: Ensures usability across devices with Bootstrap.
- **Interactive Elements**: JavaScript-powered buttons and forms for user interaction.

---

## **Installation and Usage**

### **Prerequisites**
- **Python 3.x**
- **SQLite3**
- **A local HTTP server** (e.g., Node.js, Python's `http.server`).

### **Steps**

1. **Database Initialization**:
    ```bash
    sqlite3 logement.db < logement.sql
    python remplissage.py
    ```

2. **Start the Server**:
    ```bash
    uvicorn serveur:app --reload
    ```

3. **Access the Website**:
    - Serve `eco_housing_website` using a local HTTP server, or
    - Directly open `html/index.html` in your browser.

---

## **Project Logic and Flow**

### **Workflow**
1. **Database**: Stores structured data for all housing-related entities.
2. **Server**: Acts as a middleware to handle requests, fetch data, and interact with APIs.
3. **Website**: Provides an intuitive and interactive interface for users to manage their eco-responsible home.

### **Features**
- Centralized management of housing data.
- Advanced visualization of consumption and cost trends.
- Configurable sensor management.

---

## **Future Enhancements**
- Integrate weather-based decision-making tools.
- Include predictive analytics for consumption trends.
- Expand sensor support to cover more types.

---

## **Contact**
For any inquiries or questions, please reach out to:
- **Email**: [jiangmengmeng1211@gmail.com](mailto:jiangmengmeng1211@gmail.com)
- **Project Link**: [GitHub Repository](https://github.com/jiangmengmeng/Eco-Housing-Management)

## **Acknowledgments**
This project was made possible with the help of the following resources:
- **ChatGPT**: Assistance with various coding and project management tasks.
- **W3Schools**: Web development tutorials and references.
- **OpenWeatherMap API**: For providing weather forecast data.