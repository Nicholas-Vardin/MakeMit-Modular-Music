#include <WiFi.h>
#include <WebServer.h>
#define pianoModulePin 25
#define guitarModulePin 23
#define drumModulePin 27

const char* ssid = "Nicholas’s iPhone";
const char* password = "Trash Pig";

WebServer server(80);
String instruments = "";
bool pianoOn = false;
bool guitarOn = false;
bool drumOn = false;

void handleRoot() {
  server.send(200, "text/plain", "ESP32 Server Running");
}

void handleNumber() {
  server.send(200, "text/plain", String("42"));
}

void handleInstruments() {
  server.send(200, "text/plain", String(instruments));
}

void connectToWiFi() {
  Serial.println("----- WiFi Connection Start -----");
  Serial.print("SSID: ");
  Serial.println(ssid);

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  int attempts = 0;

  while (WiFi.status() != WL_CONNECTED && attempts < 30) {
    Serial.print("Attempt ");
    Serial.print(attempts + 1);
    Serial.print(" | Status: ");
    Serial.println(WiFi.status());
    delay(1000);
    attempts++;
  }

  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("WiFi CONNECTED");
    Serial.print("IP Address: ");
    Serial.println(WiFi.localIP());
    Serial.print("Gateway: ");
    Serial.println(WiFi.gatewayIP());
    Serial.print("Signal RSSI: ");
    Serial.println(WiFi.RSSI());
  } else {
    Serial.println("WiFi FAILED TO CONNECT");
  }

  Serial.println("----- WiFi Connection End -----");
}

void setup() {
  Serial.begin(115200);
  delay(1500);

  pinMode(pianoModulePin, INPUT_PULLUP);
  pinMode(guitarModulePin, INPUT_PULLUP);
  pinMode(drumModulePin, INPUT_PULLUP);

  connectToWiFi();

  if (WiFi.status() == WL_CONNECTED) {
    server.on("/", handleRoot);
    server.on("/number", HTTP_GET, handleNumber);
    server.on("/instruments", HTTP_GET, handleInstruments);
    server.begin();
    Serial.println("HTTP server started");
  } else {
    Serial.println("Server not started due to WiFi failure");
  }
}

void getNewInstruments()
{
  String oldInstruments = instruments;
  if (digitalRead(pianoModulePin) == LOW && !pianoOn) {
    if (instruments.length() > 0) instruments += ", ";
    pianoOn = true;
    instruments += "piano";
  }

  if (digitalRead(guitarModulePin) == LOW && !guitarOn) {
    if (instruments.length() > 0) instruments += ", ";
    guitarOn = true;
    instruments += "guitar";
  }

  if (digitalRead(drumModulePin) == LOW && !drumOn) {
    if (instruments.length() > 0) instruments += ", ";
    drumOn = true;
    instruments += "drums";
  }

  if (oldInstruments != instruments) {
    Serial.print("Instruments Updated: ");
    Serial.println(instruments);
  }
}

void loop() {
  server.handleClient();

  getNewInstruments();
}