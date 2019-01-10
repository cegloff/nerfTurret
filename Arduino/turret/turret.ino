#include <Servo.h> 

Servo fireServo;
Servo aimServo;
int incomingByte = 0;
int pwrPin = 10;
int fireServoPin = 9;
int aimServoPin = 11;
char command[5] = {0,0,0,0,0};
int position = 0;
int currentByte = 9999;
String tempAngle = "000";
int homeAngle = 70;
int motorInitialized = 0;

void setup()   {
    Serial.begin(57600);
    pinMode(pwrPin, OUTPUT);
    fireServo.attach(fireServoPin);   
    fireServo.write(homeAngle);   // Rotate servo to ready to fire
    delay(500);
    aimServo.attach(aimServoPin);  // Servo is connected to digital pin 9 
    aimServo.write(72);   // Rotate servo counter clockwise
    delay(500);
    // motorOn();
    // delay(3000);
    // aim(30);
    // delay(1000);
    // fire();
    // burst();
    // burst();
    // burst();
    // motorOff();

}

void loop() {
    // send data only when you receive data:
    if (Serial.available() > 0) {
        // read the incoming byte:
        incomingByte = Serial.read();
        // say what you got:
        Serial.write(incomingByte);
        currentByte = incomingByte;    
    }
    
    if (currentByte != 9999 && currentByte != '\r' && position < 5){
        command[position]=char(incomingByte);
        position++;
        currentByte= 9999;
    }
    else {
        if (currentByte == '\r'){
            position = 0;
            Serial.print("I received: ");
            Serial.println(command);
            runCommand();
            resetCommand();
            
        }
    }
}

void runCommand() {
    // Serial.println(command[0]);
    if (command[0] == '0'){
        motorOff();
//        Serial.println('Motor Off');
    }
    if (command[0] == '1'){
        motorOn();
//        Serial.println('Motor On');
    }
    if (int(command[1]) > 0 || int(command[2]) > 0|| int(command[3]) > 0) {
        tempAngle[0] = command[1];
        tempAngle[1] = command[2];
        tempAngle[2] = command[3];
        int angle = tempAngle.toInt(); 
        if (angle == 0){ 
            angle = homeAngle;
        }
        aimServo.write(angle);
        // delay(1000);
    }
    if (command[4] == '1'){
        if (command[0] == '1'){
            fire();
        }
    }
    if (command[4] == '2'){
        if (command[0] == '1'){
            burst();
        }
    }
}

void resetCommand() {
    currentByte = 9999;
    // command[0] = '9';
    // command[1] = '9';
    // command[2] = '9';
    // command[3] = '9';
    // command[0] = '0';
    Serial.end();
    Serial.begin(57600);

}

void motorOn() {
    digitalWrite(pwrPin, HIGH);
    if (motorInitialized == 0){
        delay(3000);
        motorInitialized = 1;
    }
}

void motorOff() {
    digitalWrite(pwrPin, LOW);
    motorInitialized = 0;
}

void fire() {
    fireServo.write(10);
    // delay(500);
    fireServo.write(70);
    // delay(500);
}

void burst() {
    fire();
    fire();
    fire();
}

void aim(int dir){
    aimServo.write(dir);
}
