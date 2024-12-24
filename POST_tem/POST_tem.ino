#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <DHT.h>

#define DHTPIN 0  // Digital pin connected to the DHT sensor
#define DHTTYPE DHT11  // DHT 11

// Initialize DHT sensor
DHT dht(DHTPIN, DHTTYPE);

const char* ssid = "MengMeng";  // le nom de WiFi
const char* password = "mengmengzuikeai";  // le mot de passe de WiFi
const char* serverUrl = "http://172.20.10.10:1880/mesures";  // l'adresse Serveur Python

WiFiServer server(80);  // l'objet de WiFiSever
 
void setup() {
  Serial.begin(115200);
  dht.begin();

  WiFi.begin(ssid, password);
  while(WiFi.status() != WL_CONNECTED){  // vérifier la connection
    delay(1000);
    Serial.println("En train de connecter. Veuillez patienter!");
  }
  Serial.println("Connexion réussie!"); 
}

void loop() {
  // Wait a few seconds between measurements.
  delay(2000);

  // Read temperature as Celsius (the default)
  float t = dht.readTemperature();

  // Check if any reads failed and exit early (to try again)
  if (isnan(t)) {
    Serial.println(F("Failed to read from DHT sensor!"));
    return;
  }
  
  Serial.print(F("Temperature: "));
  Serial.print(t);
  Serial.print(F("°C "));

  // Send temperature data to the server
  if (WiFi.status() == WL_CONNECTED) {
    WiFiClient client;  // l'objet WiFiClient
    HTTPClient http;  // l'objet HTTPClient
    http.begin(client, serverUrl);  // spécifier l'url
    http.addHeader("Content-Type", "application/json");  // spécifier le type du contexte json

    String jsonData = "{\"Valeur\": " + String(t) + ", \"id_cap\": 1}";
    int httpResponseCode = http.POST(jsonData);  // envoyer la requête POST
    Serial.println(jsonData);
    if (httpResponseCode > 0) {  //requête réussie
      Serial.println("POST successful!");
      String response = http.getString();
      Serial.println(httpResponseCode);  // print le code du réponse 
      Serial.println(response);  // print le contexte du réponse

      // Parse the server's response for LED control
      if (response.indexOf("\"led_status\":\"ON\"") != -1) {
        digitalWrite(LED_BUILTIN, LOW); // Turn LED on
      } else {
        digitalWrite(LED_BUILTIN, HIGH);  // Turn LED off
      }
    } 
    else {
      Serial.print("Erreur!");
      Serial.println(httpResponseCode);
    }
    http.end();  // finir la requête HTTP
  }
}
