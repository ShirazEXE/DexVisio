#include <Servo.h>

const int numServos = 5;
const int servoPins[numServos] = {9, 10, 11, 12, 13};  // Pins for thumb, index, middle, ring, pinky
Servo servos[numServos];

const int straight_angle = 0;  // Angle for straight finger

void setup() {
  Serial.begin(9600);
  for (int i = 0; i < numServos; i++) {
    servos[i].attach(servoPins[i]);
    servos[i].write(straight_angle);  // Set initial position to straight
  }
}

void loop() {
  if (Serial.available() > 0) {
    String input = Serial.readStringUntil('\n');
    int angles[numServos];
    int index = 0;
    int start = 0;
    for (int i = 0; i < input.length(); i++) {
      if (input[i] == ',') {
        angles[index++] = input.substring(start, i).toInt();
        start = i + 1;
      }
    }
    angles[numServos - 1] = input.substring(start).toInt();

    for (int i = 0; i < numServos; i++) {
      servos[i].write(angles[i]);
    }
  }
}