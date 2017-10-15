/* Pill Popper
 * Authors: Emma, Binit and Max
 * 
 * This program will read in values from the Force Sensitive Resistor
 * and output the value to an LCD.
 */

#include <Wire.h>
     #include <rgb_lcd.h>
     #include <microsmooth.h>
     #include <autotune.h>
     #include <Servo.h>

     // FSR variables
     #define fsrAnalogPin A0
     int fsrReading;
     uint16_t *history;

     // LCD variables
     rgb_lcd lcd;

     // Servo variables
     Servo mServo;

     // Wifi variables

     void setup() {
               Serial.begin(9600);
                 history = ms_init(KZA);
                   if (history == NULL) {
                           Serial.println("No Memory");
                             }

                     mServo.attach(13);
                       mServo.writeMicroseconds(1470);
                         
                         lcd.begin(16, 2);
                           lcd.setRGB(255, 255, 255);
                             lcd.print("Pressure:");
                               delay(1000);
                               }

     void loop() {
               fsrReading = analogRead(fsrAnalogPin);
                 int processedValue = kza_filter(fsrReading, history);
                   Serial.println(processedValue);
                     
                     lcd.setCursor(0, 1);
                       lcd.print(processedValue);
                       }
