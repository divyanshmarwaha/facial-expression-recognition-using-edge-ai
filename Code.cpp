#include <Servo.h>

#define LED_PIN 3
#define SERVO_PIN 6

Servo myServo;

String emotion = "";

void setup() {
  Serial.begin(9600);
  pinMode(LED_PIN, OUTPUT);
  myServo.attach(SERVO_PIN);
}

void loop() {
  if (Serial.available()) {
    emotion = Serial.readStringUntil('\n');

    Serial.print("Received: ");
    Serial.println(emotion);

    // ---- Actions ----

    if (emotion == "HAPPY") {
      digitalWrite(LED_PIN, HIGH);
      myServo.write(90);
    }

    else if (emotion == "SAD") {
      digitalWrite(LED_PIN, LOW);
      myServo.write(0);
    }

    else if (emotion == "ANGRY") {
      for (int i = 0; i < 3; i++) {
        digitalWrite(LED_PIN, HIGH);
        delay(100);
        digitalWrite(LED_PIN, LOW);
        delay(100);
      }
      myServo.write(180);
    }

    else if (emotion == "SURPRISE") {
      myServo.write(120);
    }

    else if (emotion == "FEAR") {
      myServo.write(60);
    }

    else if (emotion == "DISGUST") {
      myServo.write(30);
      }
    else if (emotion == "CONTEMPT") {
      myServo.write(150);
      }  

    else {
      myServo.write(90);
      digitalWrite(LED_PIN, LOW);
    }
  }
}
