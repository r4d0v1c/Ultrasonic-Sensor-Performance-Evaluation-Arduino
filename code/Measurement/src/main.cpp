#include <Arduino.h>

#define TRIG_PIN 9
#define ECHO_PIN 10
#define TEMP 23
#define SOUND_SPEED (331.3 + 0.606 * TEMP) / 10000 // Speed of sound in cm/us
#define DELAY_BETWEEN_MEASUREMENTS 1000 // Delay in milliseconds

long duration;

void initializePins() {
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  duration = 0;
}

void triggerUltrasonicPulse() {
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);
}

long measureDistance() {
  duration = pulseIn(ECHO_PIN, HIGH);
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
  Serial.print(distance);
  Serial.print(',');
  Serial.println(duration);
  delay(DELAY_BETWEEN_MEASUREMENTS);
}
