#include <Servo.h>

Servo servo;
const int SERVO_PIN = 9;
const int REST_ANGLE = 45;

void setup() {
    randomSeed(analogRead(A0));
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

void love() {
    int angle = random(80, 100);
    int hold = random(800, 1200);
    servo.write(REST_ANGLE + angle);
    delay(hold);
    servo.write(REST_ANGLE);
}

void sad() {
    int angle = random(15, 25);
    int hold = random(1500, 2500);
    servo.write(REST_ANGLE + angle);
    delay(hold);
    servo.write(REST_ANGLE);
}

void loop() {
    if (Serial.available() > 0) {
        char c = Serial.read();
        if (c == 'w') {
            wave();
            Serial.write('k');
        } else if (c == 'l') {
            love();
            Serial.write('k');
        } else if (c == 's') {
            sad();
            Serial.write('k');
        }
    }
}
