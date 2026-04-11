#include <Servo.h>

Servo servo;
const int SERVO_PIN = 9;
const int REST_ANGLE = 45;

void setup() {
    servo.attach(SERVO_PIN);
    servo.write(REST_ANGLE);
    Serial.begin(9600);
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
}

void loop() {
    if (Serial.available() > 0) {
        String command = Serial.readStringUntil('\n');
        command.trim();
        if (command.length() > 0) {
            executeSteps(command);
            Serial.write('k');
        }
    }
}
