-- sqlite3 logement.db
-- .read logement.sql

-- commandes de destruction des tables
DROP TABLE IF EXISTS Logement;
DROP TABLE IF EXISTS Piece;
DROP TABLE IF EXISTS Capteur;
DROP TABLE IF EXISTS Type_Capteur;
DROP TABLE IF EXISTS Mesure;
DROP TABLE IF EXISTS Facture;
DROP TABLE IF EXISTS Adresse;
DROP TABLE IF EXISTS Ville;
DROP TABLE IF EXISTS Location;

-- commandes de creation des tables
CREATE TABLE Logement (id INTEGER PRIMARY KEY AUTOINCREMENT, Numero_de_telephone INTEGER NOT NULL, Adress_IP INTEGER NOT NULL, id_Ad INTEGER NOT NULL, Date TIMESTAMP DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY (id_Ad) REFERENCES Adresse(id));
CREATE TABLE Piece (id  INTEGER PRIMARY KEY AUTOINCREMENT, Nom TEXT NOT NULL, id_Loca INTEGER NOT NULL, id_loge INTEGER NOT NULL, FOREIGN KEY (id_Loca) REFERENCES Location(id), FOREIGN KEY (id_loge) REFERENCES Logement(id));
CREATE TABLE Capteur (id  INTEGER PRIMARY KEY AUTOINCREMENT, id_type INTEGER NOT NULL, id_piece INTEGER NOT NULL, ref_com TEXT NOT NULL, Port INTEGER NOT NULL, Date TIMESTAMP DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY (id_type) REFERENCES Type_Capteur(id), FOREIGN KEY (id_piece) REFERENCES Piece(id));
CREATE TABLE Type_Capteur (id  INTEGER PRIMARY KEY AUTOINCREMENT, Unite TEXT NOT NULL, Plage DOUBLE NOT NULL);
CREATE TABLE Mesure (id  INTEGER PRIMARY KEY AUTOINCREMENT, Valeur DOUBLE NOT NULL, id_cap INTEGER NOT NULL, Date TIMESTAMP DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY (id_cap) REFERENCES Capteur(id));
CREATE TABLE Adresse (id  INTEGER PRIMARY KEY AUTOINCREMENT, Numero INTEGER NOT NULL, Voie TEXT NOT NULL, Nom_voie TEXT NOT NULL, Code INTEGER NOT NULL, FOREIGN KEY (Code) REFERENCES Ville(Code));
CREATE TABLE Ville (Code INTEGER PRIMARY KEY, Nom TEXT NOT NULL);
CREATE TABLE Facture (id  INTEGER PRIMARY KEY AUTOINCREMENT, Type_fac TEXT NOT NULL, Montant DOUBLE NOT NULL, Consom DOUBLE NOT NULL, id_log INTEGER NOT NULL, Date TIMESTAMP DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY (id_log) REFERENCES Logement(id));
CREATE TABLE Location (id  INTEGER PRIMARY KEY AUTOINCREMENT, dim_x DOUBLE NOT NULL, dim_y DOUBLE NOT NULL, dim_z DOUBLE NOT NULL);

-- insertion de données
INSERT INTO Piece (Nom, id_Loca, id_loge) VALUES
       ('Salon', 1,1),
       ('Chambre', 2,1),
       ('Cuisine', 3,1),
       ('Salle de bain', 4,1);

INSERT INTO Location (dim_x, dim_y, dim_z) VALUES
       (0.5, 1.1, 2.3),
       (0.9, 1.8, 2.1),
       (0.8, 1.6, 2.9),
       (0.7, 1.4, 2.5);

INSERT INTO Adresse (Numero, Voie, Nom_voie, Code) VALUES
       (4, 'allée', 'des groseilliers', 92140),
       (14, 'rue', 'Berthelot', 94200),
       (18, 'rue', 'd Estree', 75007),
       (56, 'rue', 'Arthur Rimbaud', 93300);

INSERT INTO Ville (Code, Nom) VALUES
       (92140, 'Clamart'),
       (94200, 'Ivry sur Seine'),
       (75007, 'Paris'),
       (93300, 'Aubervilliers');

INSERT INTO Logement (Numero_de_telephone, Adress_IP, id_Ad) VALUES (0123456789, 200212110125, 3);

INSERT INTO Type_Capteur (Unite, Plage) VALUES
       ('Celsius', 100.0),     -- Temperature sensor
       ('Percent', 100.0),     -- Humidity sensor
       ('Lux', 1000.0),        -- Light sensor
       ('Pascal', 100000.0),   -- Pressure sensor
       ('kWh', 10000.0),       -- Electricity consumption sensor, up to 10,000 kWh
       ('Liters', 1000.0),     -- Water flow sensor, measures up to 1000 liters per hour
       ('Cubic meters', 500.0),   -- Gas flow sensor, up to 500 m³ for residential gas usage
       ('ppm', 5000.0),        -- CO2 sensor, 0 to 5000 ppm for indoor air quality
       ('Cubic meters', 100.0),     -- General volume sensor, up to 100 m³ (e.g., for gas or water in larger systems)
       ('Watts', 10000.0);          -- Power sensor, up to 10,000 watts for larger appliances or HVAC.

INSERT INTO Capteur (id_type, id_piece, ref_com, Port) VALUES
       (1, 2, 'ABC001', 77),  -- Sensor of type Temperature
       (2, 1, 'XYZ007', 99),   -- Sensor of type Humidity
       (5, 3, 'ELEC001', 12),     -- Electricity sensor in the kitchen (kWh)
       (6, 2, 'WATER002', 45),    -- Water sensor in the bathroom (liters)
       (7, 1, 'GAS003', 88);      -- Gas sensor in the living room (cubic meters)

INSERT INTO Mesure (Valeur, id_cap) VALUES
       (23.5, 1),  -- Measurement for sensor with id 1 (Temperature sensor)
       (24.0, 1),
       (45.2, 2),
       -- Measurement for sensor with id 2 (Humidity sensor)
       (46.0, 2);

INSERT INTO Facture (Type_fac, Montant, Consom, id_log) VALUES
       ('Electricity', 122.5, 350.0, 1),
       ('Water', 16.0, 80.0, 1),
       ('Gas', 60.0, 200.0, 1),
       ('Internet', 10.0, 100.0, 1);