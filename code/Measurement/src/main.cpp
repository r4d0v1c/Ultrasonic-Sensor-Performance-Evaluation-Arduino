#include <Arduino.h>

#define TRIG_PIN 9
#define ECHO_PIN 10
#define SOUND_SPEED 0.0343 // Speed of sound in cm/us
#define DELAY_BETWEEN_MEASUREMENTS 1000 // Delay in milliseconds

void initializePins() {
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
}

void triggerUltrasonicPulse() {
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);
}

long measureDistance() {
  long duration = pulseIn(ECHO_PIN, HIGH);
  return (duration / 2) * SOUND_SPEED;
}

void setup() {
  Serial.begin(9600);
  Serial.println("Ultrasonic Sensor Initialized");
  initializePins();
}

void loop() {
  triggerUltrasonicPulse();
  long distance = measureDistance();

  Serial.print("Distance: ");
  Serial.print(distance);
  Serial.println(" cm");

  delay(DELAY_BETWEEN_MEASUREMENTS);
}
