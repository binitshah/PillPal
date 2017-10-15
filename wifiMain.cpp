/* Pill Popper
 * Authors: Emma, Binit and Max
 * 
 * This program will read in values from the Force Sensitive Resistor
 * and output the value to an LCD.
 */

 
#include <Arduino.h>
#include <Wire.h>

String receiveCommandString2();

void setup()
{
  Serial.begin(9600);
}

void loop()
{
    
      String incomingString = receiveCommandString2();
    
      delay(10);
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
