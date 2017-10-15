/* Pill Popper
 * Authors: Emma, Binit and Max
 * 
 * This program will read in values from the Force Sensitive Resistor
 * and output the value to an LCD.
 */

 
#include <Arduino.h>
#include <Wire.h>
#include <SPI.h>
#include <ESP8266WiFi.h>



String receiveCommandString2();


WiFiClient client;

void setup() {
  Serial.begin(115200);
  Serial.println("test");

  

  WiFi.begin("MaxiPhone", "23smjt5j43rts");

  Serial.print("Connecting");
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }
  Serial.println();

  Serial.print("Connected, IP address: ");
  Serial.println(WiFi.localIP());
}

void loop() {
 
}

void sendCommand2(String str)
{
  Serial.print(str);
}


String receiveCommandString2()
{
  if (!Serial.available())
  {
  }
  String tempString = Serial.readString();
  return tempString;
}
