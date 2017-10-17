/* Pill Popper
 * Authors: Emma, Binit and Max
 * 
 * This program will read in values from the Force Sensitive Resistor
 * and output the value to an LCD.
 */

#include <Arduino.h>
#include <Wire.h>
#include <rgb_lcd.h>
#include <Servo.h>
#include <Time.h>

#define BUZZER 9
#define SERVO 12
#define ledPin 13
int incomingByte;

// LCD variables
rgb_lcd lcd;

// Servo variables
Servo mServo;

// Wifi variables

void playFreq(float, float);
void dispString(String);
void sendCommand(String);
String receiveCommandString();
void interpretString(String);

void setup()
{
  Serial.begin(9600);
  mServo.attach(SERVO);
  lcd.begin(16, 2);
  lcd.setRGB(100, 255, 255);
  lcd.print("Pressure:");
  pinMode(13, OUTPUT);
  pinMode(BUZZER, OUTPUT);
}

void loop()
{

  String incomingString = receiveCommandString();

  if (incomingString.length() > 1)
  {
    interpretString(incomingString);
  }
  delay(10);
}

void interpretString(String in)
{

  switch (in)
  {
  case "green":
    lcd.setRGB(0, 255, 0);
    break;
  case "red":
    lcd.setRGB(255, 0, 0);
    break;
  case "blue":
    lcd.setRGB(0, 0, 255);
    break;
  case "purple":
    lcd.setRGB(255, 0, 255);
    break;
  case "white":
    lcd.setRGB(255, 255, 255);
    break;
  case "rotate":
    break;
  }
}

void playFreq(float freq, float dur)
{
  tone(BUZZER, freq, dur);
}

void dispString(String str)
{
  lcd.setCursor(0, 1);
  lcd.print("          ");
  lcd.setCursor(0, 1);
  lcd.print(str);
}

void sendCommand(String str)
{
  Serial.print(str);
}

char receiveCommandChar()
{
  while (!Serial.available())
  {
  }
  char tempChar = Serial.read();
  return tempChar;
}
String receiveCommandString()
{
  if (!Serial.available())
  {
  }
  String tempString = Serial.readString();
  return tempString;
}

void clockwise()
{
  mServo.writeMicroseconds(1300);
}

void countclockwise()
{
  mServo.writeMicroseconds(1700);
}

bool timeIsSame() {
  getHours();
}

