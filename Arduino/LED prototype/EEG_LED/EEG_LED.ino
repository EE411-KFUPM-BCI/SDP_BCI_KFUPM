#include <Wire.h>                                             //This library allows you to communicate with I2C addresses
#include <Adafruit_MotorShield.h>                             //Include Adafruit MotorShield libraries
#include <SoftwareSerial.h>

SoftwareSerial Bluetooth(2, 3);

Adafruit_MotorShield AFMS = Adafruit_MotorShield();
Adafruit_DCMotor *myMotor1 = AFMS.getMotor(1);
Adafruit_DCMotor *myMotor2 = AFMS.getMotor(2);


int greenPin = 4;


int incomingByte; // variable to read serial data into

void setup() {

  Bluetooth.begin(9600);
  AFMS.begin();
  myMotor1->setSpeed(150);
  myMotor2->setSpeed(150);


  // set LED pins as outputs
  pinMode(greenPin, OUTPUT);
}

void loop() {

  // check if there's incoming data
  if (Bluetooth.available() > 0) {

    // read the oldest byte in the buffer:
    incomingByte = Bluetooth.read();
   if (incomingByte == 'G') {
      digitalWrite(greenPin, HIGH);  // green BLINK detectod!!!
    }
    if (incomingByte == 'F') {
        myMotor1->run(FORWARD);
        myMotor2->run(FORWARD);
    }

    if (incomingByte == 'R') {
        myMotor1->run(FORWARD);
        myMotor2->run(BACKWARD);
    }

    if (incomingByte == 'L') {
        myMotor1->run(BACKWARD);
        myMotor2->run(FORWARD);
    }

    if (incomingByte == '0') {
        myMotor1->run(RELEASE);
        myMotor2->run(RELEASE);     
    }
  }<strong><br></strong>
