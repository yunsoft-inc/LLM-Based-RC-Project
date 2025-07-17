const int voltageOutputPin = A6;
const int voltageBatteryPin = A7;
const float inputVoltageMax = 25.0;
const int adcResolution = 1023;

const int motorA_IN1 = 13;
const int motorA_IN2 = 12;
const int motorB_IN1 = 10;
const int motorB_IN2 = 11;

unsigned long lastPrintTime = 0;
const unsigned long printInterval = 1000;

String inputBuffer = "";

void setup() {
  Serial.begin(115200);

  pinMode(motorA_IN1, OUTPUT);
  pinMode(motorA_IN2, OUTPUT);
  pinMode(motorB_IN1, OUTPUT);
  pinMode(motorB_IN2, OUTPUT);

  stopMotors();
}

void loop() {
  if (millis() - lastPrintTime >= printInterval) {
    float outputV = analogRead(voltageOutputPin) * inputVoltageMax / adcResolution;
    float batteryV = analogRead(voltageBatteryPin) * inputVoltageMax / adcResolution;

    Serial.print("OUT: ");
    Serial.print(outputV, 2);
    Serial.print(" V\tBAT: ");
    Serial.print(batteryV, 2);
    Serial.println(" V");

    lastPrintTime = millis();
  }

  while (Serial.available()) {
    char c = Serial.read();
    if (c == '\n') {
      handleParsedCommand(inputBuffer);
      inputBuffer = "";
    } else {
      inputBuffer += c;
    }
  }
}

void handleParsedCommand(String cmd) {
  cmd.trim();
  if (cmd.length() == 0) return;

  int comma = cmd.indexOf(',');

  if (comma != -1 && cmd.length() > comma + 1) {
    char dir = toupper(cmd.substring(0, comma)[0]);
    int angle = cmd.substring(comma + 1).toInt();
    if ((dir == 'R' || dir == 'L') && angle > 0) {
      int mspeed = 200;
      int duration = angle * 10;

      if (dir == 'R') turnRight(mspeed);
      else if (dir == 'L') turnLeft(mspeed);

      delay(duration);
      stopMotors();
      Serial.println("E");
      return;
    }
  }

  int firstComma = cmd.indexOf(',');
  int secondComma = cmd.indexOf(',', firstComma + 1);
  if (firstComma == -1 || secondComma == -1) {
    Serial.println("Invalid command");
    return;
  }

  char move = toupper(cmd.substring(0, firstComma)[0]);
  char speedChar = toupper(cmd.substring(firstComma + 1, secondComma)[0]);
  char timeChar = cmd.substring(secondComma + 1)[0];

  int mspeed = 0;
  if (speedChar == 'L') mspeed = 150;
  else if (speedChar == 'M') mspeed = 200;
  else if (speedChar == 'H') mspeed = 255;
  else {
    Serial.println("Invalid speed");
    return;
  }

  int duration = 0;
  if (timeChar == '1') duration = 300;
  else if (timeChar == '2') duration = 800;
  else if (timeChar == '3') duration = 1500;
  else {
    Serial.println("Invalid duration");
    return;
  }

  switch (move) {
    case 'F':
      forward(mspeed); break;
    case 'B':
      backward(mspeed); break;
    case 'L':
      turnLeft(mspeed); break;
    case 'R':
      turnRight(mspeed); break;
    default:
      Serial.println("Invalid direction");
      return;
  }

  delay(duration);
  stopMotors();
  Serial.println("E");
}

void forward(int spd) {
  analogWrite(motorA_IN1, spd);
  analogWrite(motorA_IN2, 0);
  analogWrite(motorB_IN1, spd);
  analogWrite(motorB_IN2, 0);
}

void backward(int spd) {
  analogWrite(motorA_IN1, 0);
  analogWrite(motorA_IN2, spd);
  analogWrite(motorB_IN1, 0);
  analogWrite(motorB_IN2, spd);
}

void turnLeft(int spd) {
  analogWrite(motorA_IN1, 0);
  analogWrite(motorA_IN2, spd);
  analogWrite(motorB_IN1, spd);
  analogWrite(motorB_IN2, 0);
}

void turnRight(int spd) {
  analogWrite(motorA_IN1, spd);
  analogWrite(motorA_IN2, 0);
  analogWrite(motorB_IN1, 0);
  analogWrite(motorB_IN2, spd);
}

void stopMotors() {
  analogWrite(motorA_IN1, 0);
  analogWrite(motorA_IN2, 0);
  analogWrite(motorB_IN1, 0);
  analogWrite(motorB_IN2, 0);
}
