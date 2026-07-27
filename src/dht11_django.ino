#include <DHT.h>
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>

#define DHTPIN 0        // DHT11 
#define DHTTYPE DHT11    // DHT11 

const char* ssid = "your-ssid";
const char* password = "your-password";
const char* serverUrl = "https://your-domain.belajarhub.id/django/api/sensor/";  
const char* api_key = "abc123";
const char* device_id = "device01";

DHT dht(DHTPIN, DHTTYPE);
WiFiClientSecure client;

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  dht.begin();

  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi connected");
  client.setInsecure();
}

void loop() {
  float humidity = dht.readHumidity();
  float temperature = dht.readTemperature(); 

  if (isnan(humidity) || isnan(temperature)) {
    Serial.println("Failed to read from DHT sensor!");
    return;
  }

  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(client,serverUrl);
    http.addHeader("Content-Type", "application/json");
    String json = "{\"apikey\":\"" + String(api_key) + "\",";
    json += "\"device_id\":\"" + String(device_id) + "\",";
    json += "\"temperature\":" + String(temperature, 1) + ",";
    json += "\"humidity\":" + String(humidity, 1) + "}";  
   
    int httpResponseCode = http.POST(json);

    Serial.print("POST Data: ");
    Serial.println(json);
    Serial.print("Response code: ");
    Serial.println(httpResponseCode);

    http.end();
  } else {
    Serial.println("WiFi Disconnected");
  }

  delay(10000); // 10초마다 전송
}
