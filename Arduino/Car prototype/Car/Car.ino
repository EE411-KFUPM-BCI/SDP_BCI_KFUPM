#include <Wire.h>                                             //This library allows you to communicate with I2C addresses
#include <Adafruit_MotorShield.h>                             //Include Adafruit MotorShield libraries
#include <SoftwareSerial.h>

SoftwareSerial Bluetooth(2, 3);

Adafruit_MotorShield AFMS = Adafruit_MotorShield();
Adafruit_DCMotor *myMotor1 = AFMS.getMotor(1);
Adafruit_DCMotor *myMotor2 = AFMS.getMotor(2);
Adafruit_DCMotor *myMotor3 = AFMS.getMotor(3);
Adafruit_DCMotor *myMotor4 = AFMS.getMotor(4);

int incomingByte; // variable to read serial data into

void setup() {

  Bluetooth.begin(9600);
  AFMS.begin();
  myMotor1->setSpeed(100);
  myMotor2->setSpeed(100);
  myMotor3->setSpeed(100);
  myMotor4->setSpeed(100);
}

void loop() {

  // check if there's incoming data
  if (Bluetooth.available() > 0) {

    // read the oldest byte in the buffer:
    incomingByte = Bluetooth.read();

    if (incomingByte == 'F') {
        myMotor1->run(FORWARD);
        myMotor2->run(FORWARD);
        myMotor3->run(FORWARD);
        myMotor4->run(FORWARD);
    }

    if (incomingByte == 'R') {
        myMotor1->run(FORWARD);
        myMotor2->run(FORWARD);
        myMotor3->run(BACKWARD);
        myMotor4->run(BACKWARD);
    }

    if (incomingByte == 'L') {
        myMotor1->run(BACKWARD);
        myMotor2->run(BACKWARD);
        myMotor3->run(FORWARD);
        myMotor4->run(FORWARD);
    }


    if (incomingByte == 'S') {
        myMotor1->run(RELEASE);
        myMotor2->run(RELEASE); 
        myMotor3->run(RELEASE);
        myMotor4->run(RELEASE);

    }
  }
}
