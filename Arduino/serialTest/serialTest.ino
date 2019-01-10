/* Use a variable called byteRead to temporarily store
   the data coming from the computer */
byte byteRead;
char command[5] = {0,0,0,0,0};
int incomingByte = 0;
int pwrPin = 10;
int fireServoPin = 9;
int aimServoPin = 11;
int position = 0;
int currentByte = 9999;
String tempAngle = "000";
int homeAngle = 70;
int motorInitialized = 0;


void setup() {                
// Turn the Serial Protocol ON
  Serial.begin(9600);
  pinMode(pwrPin, OUTPUT);
  // Serial.write('a');
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
            // runCommand();
            // resetCommand();
        }
    }
}