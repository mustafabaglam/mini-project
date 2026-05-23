#include <Servo.h>

const int servoPin = 6;
const int trigPin = 9;
const int echoPin = 10;

Servo myservo;

int measureDistance() {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  long duration = pulseIn(echoPin, HIGH, 30000);
  if (duration == 0) return -1;
  return duration * 0.034 / 2;
}

void setup() {
  Serial.begin(9600);
  myservo.attach(servoPin);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
}

void loop() {
  for (int angle = 0; angle <= 90; angle += 15) {
    myservo.write(angle);
    delay(400);
    int d = measureDistance();
    Serial.print("{\"d\":");
    Serial.print(d);
    Serial.print(",\"r\":");
    Serial.print(angle);
    Serial.println("}");
  }

  for (int angle = 90; angle >= 0; angle -= 15) {
    myservo.write(angle);
    delay(400);
    int d = measureDistance();
    Serial.print("{\"d\":");
    Serial.print(d);
    Serial.print(",\"r\":");
    Serial.print(angle);
    Serial.println("}");
  }
}
