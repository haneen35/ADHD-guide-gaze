#include <SoftwareSerial.h>

#define LED_PIN 13

const int RX_PIN=0;
const int TX_PIN=1;
SoftwareSerial serial(RX_PIN,TX_PIN);
String receivedData;

void setup() {
  pinMode(LED_PIN, OUTPUT);
  Serial.begin(9600);
}

void loop() {
    if (Serial.available() > 0) {
        receivedData = Serial.readStringUntil('\r');
        Serial.print("Received: ");
        Serial.println(receivedData);
        if (receivedData == "on") {
            digitalWrite(LED_PIN, HIGH);
        }
         if (receivedData == "off") {
            digitalWrite(LED_PIN, LOW);
        }
    }
}
