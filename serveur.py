from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from jinja2 import Template, Environment, FileSystemLoader
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import sqlite3
import requests
from typing import List, Optional
from datetime import datetime
from sqlalchemy import create_engine

# Initialize the FastAPI app
app = FastAPI()

# Database connection helper
def get_db_connection():
    conn = sqlite3.connect('logement.db')
    conn.row_factory = sqlite3.Row  # Allows accessing columns by name
    return conn

# entity Logement
class Logement(BaseModel):
    Numero_de_telephone: int
    Adress_IP: int
    id_Ad: int
    Date: Optional[str] = None

# entity Piece
class Piece(BaseModel):
    Nom: str
    id_Loca: int
    id_loge: int

# GET endpoint to retrieve all logements
@app.get("/logements", response_model=List[Logement])
def get_logements():
    conn = get_db_connection()
    logements = conn.execute("SELECT * FROM Logement").fetchall()
    conn.close()
    return [dict(row) for row in logements]

# POST endpoint to create a new logement
@app.post("/logements", response_model=Logement)
def create_logement(logement: Logement):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if a logement with the same `Numero_de_telephone` and `Adress_IP` already exists
    existing_logement = cursor.execute(
        """
        SELECT * FROM Logement
        WHERE Numero_de_telephone = ? AND Adress_IP = ?
        """,
        (logement.Numero_de_telephone, logement.Adress_IP)
    ).fetchone()

    if existing_logement:
        conn.close()
        raise HTTPException(
            status_code=400,
            detail="Logement with the same Numero_de_telephone and Adress_IP already exists."
        )

    # If not, insert the new logement
    cursor.execute(
        """
        INSERT INTO Logement (Numero_de_telephone, Adress_IP, id_Ad, Date)
        VALUES (?, ?, ?, CURRENT_TIMESTAMP)
        """,
        (logement.Numero_de_telephone, logement.Adress_IP, logement.id_Ad)
    )
    conn.commit()
    logement_id = cursor.lastrowid
    conn.close()
    return {**logement.model_dump(), "id": logement_id}

# GET endpoint to retrieve all pieces for a given logement
@app.get("/pieces/{logement_id}", response_model=List[Piece])
def get_pieces(logement_id: int):
    conn = get_db_connection()
    pieces = conn.execute(
        "SELECT * FROM Piece WHERE id_loge = ?", (logement_id,)
    ).fetchall()
    conn.close()
    return [dict(row) for row in pieces]

# POST endpoint to create a new piece
@app.post("/pieces", response_model=Piece)
def create_piece(piece: Piece):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if a piece with the same `Nom` and `id_loge` already exists
    existing_piece = cursor.execute(
        """
        SELECT * FROM Piece
        WHERE Nom = ? AND id_loge = ?
        """,
        (piece.Nom, piece.id_loge)
    ).fetchone()

    if existing_piece:
        conn.close()
        raise HTTPException(
            status_code=400,
            detail="Piece with the same Nom already exists in the specified logement."
        )

    # If not, insert the new piece
    cursor.execute(
        "INSERT INTO Piece (Nom, id_Loca, id_loge) VALUES (?, ?, ?)",
        (piece.Nom, piece.id_Loca, piece.id_loge)
    )
    conn.commit()
    piece_id = cursor.lastrowid
    conn.close()
    return {**piece.model_dump(), "id": piece_id}

# entity Ville
class Ville(BaseModel):
    Code: int
    Nom: str

@app.get("/villes", response_model=List[Ville])
def get_villes():
    conn = get_db_connection()
    villes = conn.execute("SELECT * FROM Ville").fetchall()
    conn.close()
    return [dict(row) for row in villes]

@app.post("/villes", response_model=Ville)
def create_ville(ville: Ville):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if a ville with the same Code or Nom already exists
    existing_ville = cursor.execute(
        """
        SELECT * FROM Ville
        WHERE Code = ? OR Nom = ?
        """,
        (ville.Code, ville.Nom)
    ).fetchone()

    if existing_ville:
        conn.close()
        raise HTTPException(
            status_code=400,
            detail="Ville with the same Code or Nom already exists."
        )

    # If not, insert the new ville
    query = "INSERT INTO Ville (Code, Nom) VALUES (?, ?)"
    cursor.execute(query, (ville.Code, ville.Nom))
    conn.commit()
    conn.close()
    return ville

# entity Adresse
class Adresse(BaseModel):
    Numero: int
    Voie: str
    Nom_voie: str
    Code: int

@app.get("/adresses", response_model=List[Adresse])
def get_adresses():
    conn = get_db_connection()
    adresses = conn.execute("SELECT * FROM Adresse").fetchall()
    conn.close()
    return [dict(row) for row in adresses]

@app.post("/adresses", response_model=Adresse)
def create_adresse(adresse: Adresse):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if an adresse with the same `Numero`, `Voie`, and `Nom_voie` already exists
    existing_adresse = cursor.execute(
        """
        SELECT * FROM Adresse
        WHERE Numero = ? AND Voie = ? AND Nom_voie = ?
        """,
        (adresse.Numero, adresse.Voie, adresse.Nom_voie)
    ).fetchone()

    if existing_adresse:
        conn.close()
        raise HTTPException(
            status_code=400,
            detail="Adresse with the same Numero, Voie, and Nom_voie already exists."
        )

    # If not, insert the new adresse
    cursor.execute(
        "INSERT INTO Adresse (Numero, Voie, Nom_voie, Code) VALUES (?, ?, ?, ?)",
        (adresse.Numero, adresse.Voie, adresse.Nom_voie, adresse.Code)
    )
    conn.commit()
    adresse_id = cursor.lastrowid
    conn.close()
    return {**adresse.model_dump(), "id": adresse_id}

# entity Location
class Location(BaseModel):
    dim_x: float
    dim_y: float
    dim_z: float

@app.get("/locations", response_model=List[Location])
def get_adresses():
    conn = get_db_connection()
    locations = conn.execute("SELECT * FROM Location").fetchall()
    conn.close()
    return [dict(row) for row in locations]

@app.post("/locations", response_model=Location)
def create_location(location: Location):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if a location with the same dimensions already exists
    existing_location = cursor.execute(
        """
        SELECT * FROM Location
        WHERE dim_x = ? AND dim_y = ? AND dim_z = ?
        """,
        (location.dim_x, location.dim_y, location.dim_z)
    ).fetchone()

    if existing_location:
        conn.close()
        raise HTTPException(
            status_code=400,
            detail="Location with the same dimensions already exists."
        )

    # If not, insert the new location
    cursor.execute(
        "INSERT INTO Location (dim_x, dim_y, dim_z) VALUES (?, ?, ?)",
        (location.dim_x, location.dim_y, location.dim_z)
    )
    conn.commit()
    location_id = cursor.lastrowid
    conn.close()
    return {**location.model_dump(), "id": location_id}

# entity Type_Capteur
class TypeCapteur(BaseModel):
    Unite: str
    Plage: float

@app.get("/type_capteurs", response_model=List[TypeCapteur])
def get_type_capteurs():
    conn = get_db_connection()
    type_capteurs = conn.execute("SELECT * FROM Type_Capteur").fetchall()
    conn.close()
    return [dict(row) for row in type_capteurs]

@app.post("/type_capteurs", response_model=TypeCapteur)
def create_type_capteur(type_capteur: TypeCapteur):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if the entry already exists
    existing = cursor.execute(
        "SELECT * FROM Type_Capteur WHERE Unite = ? AND Plage = ?",
        (type_capteur.Unite, type_capteur.Plage)
    ).fetchone()

    if existing:
        conn.close()
        raise HTTPException(
            status_code=400, detail="Type_Capteur with the same Unite and Plage already exists"
        )

    # Insert the new entry
    cursor.execute(
        "INSERT INTO Type_Capteur (Unite, Plage) VALUES (?, ?)",
        (type_capteur.Unite, type_capteur.Plage)
    )
    conn.commit()
    type_capteur_id = cursor.lastrowid
    conn.close()
    return {**type_capteur.model_dump(), "id": type_capteur_id}

# entity Capteur
class Capteur(BaseModel):
    id_type: int
    id_piece: int
    ref_com: str
    Port: int

@app.get("/capteurs", response_model=List[Capteur])
def get_capteurs():
    conn = get_db_connection()
    capteurs = conn.execute("SELECT * FROM Capteur").fetchall()
    conn.close()
    return [dict(row) for row in capteurs]

@app.post("/capteurs", response_model=Capteur)
def create_capteur(capteur: Capteur):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if the entry already exists
    existing = cursor.execute(
        "SELECT * FROM Capteur WHERE ref_com = ? AND Port = ?",
        (capteur.ref_com, capteur.Port)
    ).fetchone()

    if existing:
        conn.close()
        raise HTTPException(
            status_code=400, detail="Capteur with the same ref_com and Port already exists"
        )

    # Insert the new entry
    cursor.execute(
        """
        INSERT INTO Capteur (id_type, id_piece, ref_com, Port, Date)
        VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
        """,
        (capteur.id_type, capteur.id_piece, capteur.ref_com, capteur.Port)
    )
    conn.commit()
    capteur_id = cursor.lastrowid
    conn.close()
    return {**capteur.model_dump(), "id": capteur_id}

# entity Mesure
class Mesure(BaseModel):
    Valeur: float
    id_cap: int

@app.get("/mesures", response_model=List[Mesure])
def get_mesures():
    conn = get_db_connection()
    mesures = conn.execute("SELECT * FROM Mesure").fetchall()
    conn.close()
    return [dict(row) for row in mesures]

@app.post("/mesures", response_model=dict)
def create_mesure(mesure: Mesure):
    conn = get_db_connection()
    cursor = conn.cursor()
    # Insert the new entry
    cursor.execute(
        """
        INSERT INTO Mesure (valeur, id_cap, Date)
        VALUES (?, ?, CURRENT_TIMESTAMP)
        """,
        (mesure.Valeur, mesure.id_cap)
    )
    conn.commit()
    mesure_id = cursor.lastrowid
    conn.close()
    # LED logic: Turn on if the temperature exceeds a threshold (e.g., 25°C)
    led_status = "ON" if mesure.Valeur > 25 else "OFF"
    #return {**mesure.model_dump(), "id": mesure_id}
    # Return the inserted measure and LED status
    return {
        "id": mesure_id,
        "valeur": mesure.Valeur,
        "id_cap": mesure.id_cap,
        "led_status": led_status,
    }

# entity Facture
class Facture(BaseModel):
    Type_fac: str
    Montant: float
    Consom: float
    id_log: int

@app.get("/factures", response_model=List[Facture])
def get_factures():
    conn = get_db_connection()
    factures = conn.execute("SELECT * FROM Facture").fetchall()
    conn.close()
    return [dict(row) for row in factures]

@app.post("/factures", response_model=Facture)
def create_facture(facture: Facture):
    conn = get_db_connection()
    cursor = conn.cursor()
    # Insert the new facture into the table
    cursor.execute(
        """
        INSERT INTO Facture (Type_fac, Montant, Consom, id_log, Date)
        VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
        """,
        (facture.Type_fac, facture.Montant, facture.Consom, facture.id_log)
    )
    conn.commit()
    facture_id = cursor.lastrowid
    conn.close()
    return {**facture.model_dump(), "id": facture_id}

# Initialize Jinja2 Templates
templates = Jinja2Templates(directory="templates")

@app.get("/facture-piechart/{logement_id}", response_class=HTMLResponse)
def generate_pie_chart(logement_id: int, request: Request):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch and group data for the specified logement_id
    query = """
        SELECT 
            Type_fac, 
            SUM(Montant) AS Montant, 
            SUM(Consom) AS Consom, 
            GROUP_CONCAT(DISTINCT Date) AS Dates
        FROM Facture
        WHERE id_log = ?
        GROUP BY Type_fac
    """
    data = cursor.execute(query, (logement_id,)).fetchall()
    conn.close()

    if not data:
        raise HTTPException(status_code=404, detail="No factures found for the specified logement ID")

    # load templates folder to environment (security measure)
    env = Environment(loader=FileSystemLoader('templates'))

    # load the `index.jinja` template
    index_template = env.get_template('index.jinja')
    output_from_parsed_template = index_template.render(data=data, logement_id=logement_id)

    return output_from_parsed_template

# OpenWeatherMap API key
WEATHER_API_KEY = "581434597969fcf79e980ebbffda4b8e"

@app.get("/weather/{city}")
def get_weather_forecast(city: str):
    """
    Fetches the 5-day weather forecast for the given city.
    """
    # OpenWeatherMap API endpoint
    url = f"https://api.openweathermap.org/data/2.5/forecast"
    params = {
        "q": city,
        "appid": WEATHER_API_KEY,
        "units": "metric"  # Use metric units (Celsius)
    }

    # Make the API request
    response = requests.get(url, params=params)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch weather data")

    data = response.json()

    # Extract relevant forecast data
    forecast = []
    for item in data["list"]:
        forecast.append({
            "datetime": item["dt_txt"],
            "temperature": item["main"]["temp"],
            "weather": item["weather"][0]["description"],
            "wind_speed": item["wind"]["speed"]
        })

    return {
        "city": data["city"]["name"],
        "country": data["city"]["country"],
        "forecast": forecast
    }

# Handle authentication and fetch id_log
# Define a Pydantic model for input validation
class LoginRequest(BaseModel):
    numero_de_telephone: str
    adresse_ip: str

@app.post("/authenticate")
def authenticate(request: LoginRequest):
    conn = get_db_connection()
    cursor = conn.cursor()

    logement = cursor.execute(
        "SELECT id FROM Logement WHERE Numero_de_telephone = ? AND Adress_IP = ?",
        (request.numero_de_telephone, request.adresse_ip)
    ).fetchone()

    conn.close()

    if not logement:
        raise HTTPException(
            status_code=401, detail="Invalid credentials. Please try again."
        )

    return {"id_log": logement["id"]}

@app.get("/logement/{id_log}")
def get_user_info(id_log: int):
    """
    Fetches user information for a given logement ID:
    - Adresse details
    - Ville details
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # Query to join Logement, Adresse, and Ville
    user_info = cursor.execute(
        """
        SELECT 
            Logement.id AS id_log,
            Adresse.Numero AS numero_adresse,
            Adresse.Voie AS voie_adresse,
            Adresse.Nom_voie AS nom_voie_adresse,
            Adresse.Code AS ville_code,
            Ville.Nom AS ville_nom
        FROM Logement
        JOIN Adresse ON Logement.id_Ad = Adresse.id
        JOIN Ville ON Adresse.Code = Ville.Code
        WHERE Logement.id = ?
        """,
        (id_log,)
    ).fetchone()

    if not user_info:
        conn.close()
        raise HTTPException(
            status_code=404, detail="Logement not found."
        )

    result = {
        "id_log": user_info["id_log"],
        "adresse": f"{user_info['numero_adresse']} {user_info['voie_adresse']} {user_info['nom_voie_adresse']}",
        "ville": {"code": user_info["ville_code"], "nom": user_info["ville_nom"]},
    }

    conn.close()
    return result

@app.get("/logement/{id_log}/capteurs", response_model=List[dict])
def get_capteurs_by_logement(id_log: int):
    conn = get_db_connection()
    capteurs = conn.execute("""
        SELECT 
            c.id AS sensor_id,
            t.Unite AS type_unit,
            t.Plage AS type_range,
            p.Nom AS piece_name,
            c.ref_com,
            c.Port
        FROM Capteur c
        JOIN Piece p ON c.id_piece = p.id
        JOIN Type_Capteur t ON c.id_type = t.id
        WHERE p.id_loge = ?
    """, (id_log,)).fetchall()
    conn.close()
    return [dict(row) for row in capteurs]

# Handle sensor deletion
@app.delete("/capteurs/{sensor_id}")
def delete_sensor(sensor_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Capteur WHERE id = ?", (sensor_id,))
    conn.commit()
    deleted_count = cursor.rowcount
    conn.close()

    if deleted_count == 0:
        raise HTTPException(status_code=404, detail="Sensor not found")
    return {"message": "Sensor deleted successfully"}

@app.get("/facture-linechart/{logement_id}/{time_scale}", response_class=JSONResponse)
def get_facture_linechart(logement_id: int, time_scale: str):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Determine the grouping method based on the time_scale
    if time_scale == "daily":
        time_format = "%Y-%m-%d"
    elif time_scale == "weekly":
        time_format = "%Y-%W"  # ISO week format
    elif time_scale == "monthly":
        time_format = "%Y-%m"
    else:
        raise HTTPException(status_code=400, detail="Invalid time_scale. Use 'daily', 'weekly', or 'monthly'.")

    # Query to group by Type_fac and the selected time scale
    query = f"""
        SELECT 
            Type_fac,
            strftime('{time_format}', Date) AS TimePeriod,
            SUM(Montant) AS TotalMontant
        FROM Facture
        WHERE id_log = ?
        GROUP BY Type_fac, TimePeriod
        ORDER BY TimePeriod
    """
    data = cursor.execute(query, (logement_id,)).fetchall()
    conn.close()

    if not data:
        return JSONResponse(content={"error": "No data found for the specified logement ID"}, status_code=404)

    # Reformat data for the line chart
    formatted_data = []
    for row in data:
        facture_type, time_period, montant = row
        existing_type = next((item for item in formatted_data if item["Type_fac"] == facture_type), None)
        if existing_type:
            existing_type["points"].append({"Date": time_period, "Montant": montant})
        else:
            formatted_data.append({"Type_fac": facture_type, "points": [{"Date": time_period, "Montant": montant}]})

    return JSONResponse(content={"data": formatted_data})

# Add CORS middleware to the app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development. Change to specific domains in production.
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Run the app with Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
# uvicorn.run("serveur:app", host="0.0.0.0", port=8000, reload=True)

# python -m uvicorn serveur:app --host 0.0.0.0 --port 8000 --reload
