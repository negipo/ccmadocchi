#include <Servo.h>

Servo servo;
const int SERVO_PIN = 9;
const int BUZZER_PIN = 8;
const int REST_ANGLE = 180;

void setup() {
    Serial.begin(9600);
}

void initServo() {
    noInterrupts();
    servo.attach(SERVO_PIN);
    servo.write(REST_ANGLE);
    interrupts();
    delay(200);
}

void executeSteps(String command) {
    int start = 0;
    while (start < command.length()) {
        int semicolon = command.indexOf(';', start);
        if (semicolon == -1) semicolon = command.length();
        String step = command.substring(start, semicolon);

        int comma = step.indexOf(',');
        int angle = step.substring(0, comma).toInt();
        int hold = step.substring(comma + 1).toInt();

        servo.write(angle);
        delay(hold);

        start = semicolon + 1;
    }
    servo.write(REST_ANGLE);
    delay(400);
    servo.detach();
}

void loop() {
    if (Serial.available() > 0) {
        String command = Serial.readStringUntil('\n');
        command.trim();
        if (command.length() > 0) {
            if (!servo.attached()) {
                initServo();
            }
            if (command.startsWith("D:")) {
                tone(BUZZER_PIN, 2000, 100);
                delay(150);
                noTone(BUZZER_PIN);
                command = command.substring(2);
            }
            executeSteps(command);
            Serial.write('k');
        }
    }
}
