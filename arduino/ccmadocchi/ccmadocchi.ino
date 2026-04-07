#include <Servo.h>

Servo servo;
const int SERVO_PIN = 9;
const int REST_ANGLE = 45;

void setup() {
    servo.attach(SERVO_PIN);
    servo.write(REST_ANGLE);
    Serial.begin(9600);
}

void wave() {
    int count = random(2, 5);
    for (int i = 0; i < count; i++) {
        int angle = random(20, 40);
        int speed = random(100, 300);
        servo.write(REST_ANGLE + angle);
        delay(speed);
        servo.write(REST_ANGLE);
        delay(speed);
    }
    servo.write(REST_ANGLE);
}

void loop() {
    if (Serial.available() > 0) {
        char c = Serial.read();
        if (c == 'w') {
            wave();
            Serial.write('k');
        }
    }
}
