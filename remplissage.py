import sqlite3, random
from datetime import datetime

# Connect to the SQLite database (creates logement.db if it doesn't exist)
conn = sqlite3.connect('logement.db')
conn.row_factory = sqlite3.Row
c = conn.cursor()

# Read and execute the SQL script to initialize the database structure
with open('logement.sql', 'r') as file:
    sql_script = file.read()

# Execute the script to create tables and initial data
c.executescript(sql_script)

# Function to insert random Mesures with correct association between capteur_id and sensor type
def insert_random_mesures(num_mesures):
    # Retrieve sensor details: id and id_type to match correct range for each sensor
    c.execute("SELECT id, id_type FROM Capteur")
    capteur_info = [(row['id'], row['id_type']) for row in c.fetchall()]

    # Define ranges for each sensor type (id_type)
    sensor_ranges = {
        1: (0.0, 50.0),    # Temperature (Celsius)
        2: (0.0, 100.0),   # Humidity (Percent)
        3: (0.0, 1000.0),  # Light (Lux)
        4: (90000, 110000) # Pressure (Pascal)
    }

    for _ in range(num_mesures):
        capteur_id, id_type = random.choice(capteur_info)
        min_val, max_val = sensor_ranges.get(id_type, (10.0, 100.0))  # Use default range if type is unknown
        valeur = round(random.uniform(min_val, max_val), 2)
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # Insert only if sensor type matches expected range
        c.execute("INSERT INTO Mesure (Valeur, id_cap, Date) VALUES (?, ?, ?)", (valeur, capteur_id, date))

# Function to insert random Factures with a relation between Consom and Montant
def insert_random_factures(num_factures):
    # Retrieve logement IDs
    c.execute("SELECT id FROM Logement")
    logement_ids = [row['id'] for row in c.fetchall()]

    # Define multipliers for each facture type
    facture_types = {
        "Electricity": 0.35,  # Cost per unit for electricity
        "Water": 0.20,        # Cost per unit for water
        "Gas": 0.30,          # Cost per unit for gas
        "Internet": 0.10      # Cost per unit for internet
    }

    for _ in range(num_factures):
        logement_id = random.choice(logement_ids)
        type_fac = random.choice(list(facture_types.keys()))
        consom_range = (50.0, 500.0) if type_fac != "Internet" else (10.0, 100.0)  # Lower range for Internet
        consom = round(random.uniform(*consom_range), 2)
        montant = round(consom * facture_types[type_fac], 2)
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        c.execute("INSERT INTO Facture (Type_fac, Montant, Consom, id_log, Date) VALUES (?, ?, ?, ?, ?)",(type_fac, montant, consom, logement_id, date))

# Insert additional random data into Mesure and Facture tables
insert_random_mesures(10)  # Insert 10 random measurements
insert_random_factures(4)  # Insert 4 random invoices with Consom-Montant relationship

# Commit changes and close the connection
conn.commit() # Saves all changes to the database
conn.close()

print("Database initialized and populated with additional data successfully.")
