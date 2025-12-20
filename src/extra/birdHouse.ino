#include <WiFiManager.h>
#include <ESP8266HTTPClient.h>
#include <ArduinoJson.h>


int sensor = D5;
int led = D4;
int light = D7;
int sensorValue = 0;
bool active = false;
char apiPath[50];
char auxApiPath[50];
char apiPing[50];
char apiSighting[50];
char apiLightValue[50];
bool res;
bool lightActive = false;


void blink() {
  for (int i = 0; i <= 5; i++) {
    digitalWrite(led, LOW);
    delay(500);
    digitalWrite(led, HIGH);
    delay(500);
  }
}

void checkLight() {
  WiFiClient client;
  HTTPClient http;
  http.begin(client, apiLightValue);
  int httpCode = http.GET();
  String payload = http.getString();
  if (payload == "true" && !lightActive){
    lightActive = true;
    Serial.println("Switching on light");
    digitalWrite(light, HIGH);
  } else if (payload == "false" && lightActive) {
    lightActive = false;
    Serial.println("Switching off light");
    digitalWrite(light, LOW);
  }
}

void sighting() {
    Serial.println("Active");

    // Set the API get
    WiFiClient client;
    HTTPClient http;
    http.begin(client, apiSighting);
    int httpCode = http.GET();
    String payload = http.getString();
    if (httpCode == 200) {
        Serial.print("Sighting received: ");
        Serial.println(payload);
    }
    else {
        Serial.print("Sighting problem, code: ");
        Serial.println(httpCode);
        Serial.print("Payload: ");
        Serial.println(payload);
    }
    active = true;
}

void setup() {

  // Active LED until configuration is ok
  pinMode(sensor, INPUT);
  pinMode(led, OUTPUT);
  pinMode(light, OUTPUT);
  blink();

  // Light start high
  pinMode(light, OUTPUT);
  digitalWrite(light, LOW);

  // Setup wifi manager
  WiFi.mode(WIFI_STA);
  Serial.begin(9600);
  WiFiManager wm;
  wm.setDebugOutput(false);
  wm.resetSettings();  // Comment this in production

  // Set the parameters
  WiFiManagerParameter apiPathTextBox("ip_text", "Set the API url", "http://192.168.1.1:8000", 50);
  wm.addParameter(&apiPathTextBox);

  if(!wm.autoConnect("BirdHouseConnect","password")) {
    Serial.println("Failed to connect");
    ESP.restart();
    delay(1000);
  }
  else {
    Serial.println("WiFi connected");
    Serial.print("Ip address: ");
    Serial.println(WiFi.localIP());

    strncpy(apiPath, apiPathTextBox.getValue(), sizeof(apiPath));

    Serial.print("Ping API server address: ");
    Serial.println(apiPath);

    // Check for ping
    WiFiClient client;
    HTTPClient http;
    strcpy(auxApiPath, apiPath);
    strcpy(apiPing, strncat(auxApiPath, "/ping", 106));
    strcpy(auxApiPath, apiPath);
    strcpy(apiSighting, strncat(auxApiPath, "/sighting", 110));
    strcpy(auxApiPath, apiPath);
    strcpy(apiLightValue, strncat(auxApiPath, "/light_value", 110));

    Serial.println(apiPing);
    Serial.println(apiSighting);
    Serial.println(apiLightValue);

    http.begin(client, apiPing);
    Serial.println(http.headers());

    int httpCode = http.GET();
    if (httpCode == 200) {
        String payload = http.getString();
        Serial.println(httpCode);
        Serial.println(payload);

        // Blink led to show that the configuration was ok
        blink();
    }
    else {
      Serial.println(httpCode);
      Serial.println(http.getString());
      Serial.println("Error on HTTP request");
      ESP.restart();
    }
  }
}

void loop() {

  // Check for light
  checkLight();

  sensorValue = digitalRead(sensor);
  if (sensorValue && !active)
  {
    sighting();
  }
  else if (!sensorValue && active)
  {
    Serial.println("Inactive");
    active = false;
  }
}
