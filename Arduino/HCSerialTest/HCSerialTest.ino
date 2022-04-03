#include <Wire.h> 
#include <EEPROM.h>
#include <LiquidCrystal_I2C.h>
#include <Adafruit_MLX90614.h>
Adafruit_MLX90614 mlx1 = Adafruit_MLX90614(0x5A);
Adafruit_MLX90614 mlx2 = Adafruit_MLX90614(0x5B);
Adafruit_MLX90614 mlx3 = Adafruit_MLX90614(0x5C);
#include <OneWire.h>
#include <DallasTemperature.h>


//Declare LCD i2c addresses
LiquidCrystal_I2C lcd1(0x27, 16, 2);
LiquidCrystal_I2C lcd2(0x26, 16, 2);

//Declare Pin Usage
int startButton = 11; int previousButton = 12; int nextButton = 13;    // Assign button pins
int startReadOld = 1; int previousReadOld = 1; int nextReadOld = 1; // Button Initializations
//Equipment Relay Pins
int fermentor1Pin = 9;
int fermentor2Pin = 8;
int fermentor3Pin = 7;
int heaterPin = 10;
int chillerPin = 6;
int buzzerPin = 5;
int parserPin = 2;

//One wire usage:
#define ONE_WIRE_BUS 4                                // Data wire is plugged into port 4 on the Arduino
OneWire oneWire(ONE_WIRE_BUS);                        // Setup a oneWire instance to communicate with any OneWire devices (not just Maxim/Dallas temperature ICs)
DallasTemperature sensors(&oneWire);                  // Pass our oneWire reference to Dallas Temperature.


//Declare global variables 

  int startRead;
  int previousRead;
  int nextRead;
  bool stageState = false;
  int stageNumber = 1;
  int f1Temp;
  int f2Temp;
  int f3Temp;
                                            
  unsigned long lastDebounceTime = 0;               // This is reset to millis() each time a switch is pressed
  unsigned long debounceDelay = 150;                // Debounce delay, 150ms seems like a good balance
  unsigned long BuzzerLength = 1000;

//Parser Declarations
  int addr;
  bool parserMode = false;                  // holds the state of the serial mode
  int ser;                                  // holds incoming serial value
  
//initialize retrieval addresses
  int step_addr = 3;
  int time_addr = 4;
  int timeu_addr = 5;
  int temp_addr = 6;
  int stage_addr = 7;

  byte num_steps;
  int step_flag = 0; // indicates if next message is step info
  int step_count = 1; // counts number of steps added (used as back up because of step flag bug)
  int start_flag = 0; // indicates the start of instruction info


//Stage Info Default Declarations
  
  int totalStages = 1;
  int stageName = 0;
  int stageTemp = 0;
  int stageTime = 0;
  int stageDevice = 0;  //1 for kettle, 2 for chiller, 3 for fermenter 1, 4 for fermenter 2, 5 for fermenter 3

  int fermentorState[3] = {0,0,0}; //EG Fermentor 1 running, 2 and 3 off. 1 should be set to 0 once that fermentor is finished running based on timer
  int f1Target = 27;               //EG Fermentor 1 starting target temp is 27C
  int f2Target = 27;               //EG Fermentor 2 starting target temp is 27C
  int f3Target = 27;               //EG Fermentor 3 starting target temp is 27C


  String stageNames[] = {"NONE","PREHEAT","HEATING","MASHING","SPARGING","CHILLING","FERMENTER1","FERMENTER2","FERMENTER3"};             //Stage "name" to be displayed on LCD


 //Timer initializations
  const unsigned long kettleTimeIncr = 1000;        // Kettle timer count down every second
  const unsigned long fermentorTimeIncr = 60000;    // Fermentor timers count down every minute
  unsigned long previousTime_1 = 0;
  unsigned long previousTime_2 = 0;

  int kettleMinutes = 0;
  int kettleSeconds = 0;
  unsigned long kettleTime;

// Data struct to hold one step of a recipe instruction
  struct recipeInstructs {
  byte step; // stored in addr = step*5 - 2
  byte time; // stored in addr = step*5 - 1
  char time_unit; //stored in addr = step*5
  byte temp; // stored in addr = step*5 + 1
  byte stage; // stored in addr = step*5 + 2
};
const char *stages[] = {"none","preheat", "heating", "mashing", "sparging",  "chilling", "fermenter1", "fermenter2", "fermenter3"};
    
//------------VOID SETUP----------------------------------------------------------------------

void setup() {
  // put your setup code here, to run once:

  Serial.begin(9600);
  Serial.flush();
  // initialize the LCD
  lcd1.begin(); lcd2.begin(); lcd1.backlight(); lcd2.backlight();
  // initialize buttons
  pinMode(startButton, INPUT); pinMode(previousButton, INPUT); pinMode(nextButton, INPUT);  //setting pinmodes for buttons
  // contactless sensors
  mlx1.begin();
  mlx2.begin();
  mlx3.begin();
  // contact sensor
  sensors.begin();
  
  // equipment pins
  pinMode(fermentor1Pin, OUTPUT);
  addr = 3;
}

//------------VOID LOOP----------------------------------------------------------------------
void loop() {
  // put your main code here, to run repeatedly:

//FERMENTOR CONTROL

  if (fermentorState[0] == 1){                  //FERMENTER 1
    f1Temp = fermentor1(f1Target);    
  } 
  else{
    digitalWrite(fermentor1Pin,LOW);  
  }

  if (fermentorState[1] == 1){                  //FERMENTER 2
    f2Temp = fermentor2(f2Target);    
  } 
  else{
    digitalWrite(fermentor2Pin,LOW);  
  }
    
  if (fermentorState[2] == 1){                  //FERMENTER 3
    f3Temp = fermentor3(f3Target);    
  } 
  else{
    digitalWrite(fermentor3Pin,LOW);  
  }

  
//FERMENTOR STATE CONTROL;
  if (stageDevice == 3){                                        //stageDevice 3 is FERMENTER 1
    if ((stageState == true) && (fermentorState[0] == 0)){
      fermentorState[0] = 1;
      f1Target = stageTemp;
      lcd2.setCursor(12,0);
      lcd2.print("  ON");
      stageState = false;
    }
    if ((stageState == true) && (fermentorState[0] == 1)){
      fermentorState[0] = 0;
      lcd2.setCursor(12,0);
      lcd2.print(" OFF"); 
      stageState = false;
    }
  }

  if (stageDevice == 4){                                        //stageDevice 4 is FERMENTER 2
    if ((stageState == true) && (fermentorState[1] == 0)){
      fermentorState[1] = 1;
      f2Target = stageTemp;
      lcd2.setCursor(12,0);
      lcd2.print("  ON");
      stageState = false;
    }
    if ((stageState == true) && (fermentorState[1] == 1)){
      fermentorState[1] = 0;
      lcd2.setCursor(12,0);
      lcd2.print(" OFF"); 
      stageState = false;
    }
  }  

  if (stageDevice == 5){                                        //stageDevice 5 is FERMENTER 3
    if ((stageState == true) && (fermentorState[2] == 0)){
      fermentorState[2] = 1;
      f3Target = stageTemp;
      lcd2.setCursor(12,0);
      lcd2.print("  ON");
      stageState = false;
    }
    if ((stageState == true) && (fermentorState[2] == 1)){
      fermentorState[2] = 0;
      lcd2.setCursor(12,0);
      lcd2.print(" OFF"); 
      stageState = false;
    }
  }

 
           
//STAGE & BUTTON CONTROL OPERATION
  
  if ((millis() - lastDebounceTime) > debounceDelay){   //check if more time has passed than debounce Delay
    lastDebounceTime = millis();                        //reset debounce timer
    startRead = digitalRead(startButton);
    nextRead = digitalRead(nextButton);
    previousRead = digitalRead(previousButton);

    
    if (startRead==1){                                            // START/STOP button operation
      stageState = !stageState;
      
    }
//PARSER BUTTON AND OPERATION

  if (nextRead==1 && previousRead==1 && stageState==false){                   // Parser gate control (NEXT & PREVIOUS button pressed at same time)
    parserMode=!parserMode;
    EEPROM.update(0,parserMode);      
  }

  parserMode = EEPROM.read(0);
  int avail = Serial.available();
  if (parserMode==true && avail>0){
    ser = Serial.read();
    // check if start byte has been read and end byte hasn't
    // update EEPROM with new value
    if (start_flag == 1 && ser != '&') {
      EEPROM.update(addr, ser);
      addr++;
    }
    
    if (ser == '!') {                           // ! means incoming byte is total number of steps    
      step_flag = 1;                            //  EEPROM.update(2, ser);
    }
   
    if (ser == '#') { // start char             // check for start byte and set start flag
      start_flag = 1;
    }
    
    else if (ser == '&') { // stop char         //check for stop byte and reset start flag
      step_count++;
      start_flag = 0;
      EEPROM.update(2, step_count);
    }
    stageTime = EEPROM.read((stageNumber*5)-1);
    kettleTime = (stageTime)*60000;   
  }
  else{
    Serial.flush();
  }
  char start = EEPROM.read(1);
  
  //get_message();
    if (parserMode == true){
      digitalWrite(parserPin,HIGH);
    }
    if (parserMode == false){
      digitalWrite(parserPin,LOW);
    }
    Serial.print(parserMode);  

    if (parserMode==true && startRead==1){                // EEPROM clear functionality, when parserMode is on, hold START button for a second.
      for (int i = 1 ; i < EEPROM.length() ; i++) {
        EEPROM.write(i, 0);
        
      }
      Serial.flush();
      addr = 3;           
    }

//NAVIGATION BUTTONS   
    if (nextRead==1 && stageState==false){                  // NEXT button operation
      lcd1.clear();
      if (stageNumber <= totalStages){
        stageNumber = stageNumber + 1;
      }
      if (stageNumber == (totalStages+1)){
        stageNumber = 1;
      }
      stageTime = EEPROM.read((stageNumber*5)-1); 
      kettleTime = (stageTime)*60000;      
    }
    if (previousRead==1 && stageState==false){              // PREVIOUS button operation
      lcd1.clear();
      if (stageNumber > 0){
        stageNumber = stageNumber - 1;
      }
      if (stageNumber == 0){
        stageNumber = totalStages;
      }
      stageTime = EEPROM.read((stageNumber*5)-1);
      kettleTime = (stageTime)*60000; 
    }    
  }   // END BUTTON AND STAGE CONTROL

  totalStages = (EEPROM.read(2))-1;
  //stageNumber = EEPROM.read((stageNumber*5)-2);     //Not necessary as stageNumber does same thing
  stageTime = EEPROM.read((stageNumber*5)-1);       //read current stage time from EEPROM
  //timeu_addr = EEPROM.read((stageNumber*5));      //read time unit, not used yet
  stageTemp = EEPROM.read((stageNumber*5)+1);       //read current stage temp
  stageName = EEPROM.read((stageNumber*5)+2);       //read stage name
  //Set stage device
  if (stageName==1 || stageName==2 || stageName==3 || stageName==4){    //If stage is "PREHEAT","HEATING","MASHING","SPARGING"
    stageDevice = 1;                                                    //Set stage device to KETTLE
  }
  if (stageName==5){                                                    //If stage is "CHILLING"
    stageDevice = 2;                                                    //Set stage device to chiller
  }
  if (stageName==6){                                                    //If stage is "FERMENTOR1"
    stageDevice = 3;                                                    //Set stage device to fermentor1
  }
  if (stageName==7){                                                    //Fermentor 2...
    stageDevice = 4;
  }
  if (stageName==8){                                                    //Femrnetor 3...
    stageDevice = 5;
  }
// HEATER AND CHILLER TIME CONTROL
  unsigned long currentTime = millis();

  if (stageState==true){                                                 //if stage is ON
    //unsigned long kettleTime = (stageTime[(stageNumber-1)])*60000;
    if(currentTime-previousTime_1>=kettleTimeIncr){
      lcd1.setCursor(0,1);
      lcd1.print("     ");
      lcd1.setCursor(0,0);
      previousTime_1 = currentTime;
      kettleTime = kettleTime - 1000;  
    } 
    if (kettleTime == 0){
      stageState = false;    
    }
  }
  kettleMinutes = kettleTime/60000;
  kettleSeconds = (kettleTime%60000)/1000;

// BUZZER CONTROL

  if ((kettleMinutes == 0) && (kettleSeconds == 1)){
    digitalWrite(buzzerPin,HIGH);   
  }
  else {
    digitalWrite(buzzerPin,LOW);
  }

// HEATER CONTROL
  int heaterTarget = stageTemp;
  int kettleTempRead = sensors.getTempCByIndex(0);
  //Serial.println(sensors.getTempCByIndex(0));
  
  if ((stageState==true) && (stageDevice==1) ){
    
  int kettleTemp = heater(heaterTarget, kettleTempRead);
  }

  else{
    digitalWrite(heaterPin,LOW);  
  }

// CHILLER CONTROL
  
  if (stageState==true && stageDevice==2 ){
    
  int kettleTemp = chiller(heaterTarget, kettleTempRead);
  }
  else{
    digitalWrite(chillerPin,LOW);  
  }

    
// STAGE INFORMATION DISPLAY / LCD CODE
  //lcd1.clear();
  lcd1.setCursor(0,0);
  lcd1.print("S" + String(stageNumber) + " :" + stageNames[stageName]);    //LCD1 Stage number, name, state
  lcd1.setCursor(13,0);
  if ((stageState == true) && (stageDevice != 3)){
    lcd1.print("ON ");
    lcd1.setCursor(0,0);     
  }
  if (stageState == false  && (stageDevice != 3)) {
    lcd1.print("OFF");
    lcd1.setCursor(0,0);
  }
 
  
  lcd1.setCursor(0,1);
  lcd1.print(String(kettleMinutes) + ":" + String(kettleSeconds));             //LCD1 Time Remaining
  lcd1.setCursor(6,1);
  lcd1.print(String(stageTemp)+"C");
  lcd1.setCursor(11,1);
  lcd1.print(String(kettleTempRead)+"C");
  lcd1.setCursor(0,0);

  //Fermentor LCD:
  lcd2.setCursor(0,0);  
  lcd2.print("F1:" + String(f1Temp) + "C " + "F2:" + String(f2Temp) + "C " + "F3:" + String(f3Temp) + "C ");
  lcd2.setCursor(0,1);
  lcd2.print(String(f1Temp) + "C");
  lcd2.setCursor(0,0);

  //Serial.println("S" + String(stageNumber) + " :" + String(stageNames[stageName])+ " " + String(kettleMinutes) + ":" + String(kettleSeconds) +" " + String(stageTemp)+"C"); 
  
  
  

 get_message();   
}     //END VOID LOOP


//----------- FUNCTIONS----------------------------------------------------------------------------

int fermentor1(int f1Target){                       //FERMENTOR 1 OPERATION FUNCTION, RETURNS FERMENTER 1 TEMP
    float f1TempData = mlx1.readObjectTempC();
    int f1Temp = f1TempData;
    if (f1Temp > f1Target){
      digitalWrite(fermentor1Pin,HIGH);
    }
    else{
      digitalWrite(fermentor1Pin,LOW);
    }

    return(f1Temp);
}

int fermentor2(int f2Target){                       //FERMENTOR 2 OPERATION FUNCTION, RETURNS FERMENTER 2 TEMP
    float f2TempData = mlx2.readObjectTempC();
    int f2Temp = f2TempData;
    if (f2Temp > f2Target){
      digitalWrite(fermentor2Pin,HIGH);
    }
    else{
      digitalWrite(fermentor2Pin,LOW);
    }

    return(f2Temp);
}

int fermentor3(int f3Target){                       //FERMENTOR 3 OPERATION FUNCTION, RETURNS FERMENTER 3 TEMP
    float f3TempData = mlx3.readObjectTempC();
    int f3Temp = f3TempData;
    if (f3Temp > f3Target){
      digitalWrite(fermentor3Pin,HIGH);
    }
    else{
      digitalWrite(fermentor3Pin,LOW);
    }

    return(f3Temp);
}

int heater(int heaterTarget, int kettleTempRead)             // HEATER OPERATION FUNCTION
{
//  method 1 - slower
  
  if ((kettleTempRead < heaterTarget) && (stageState == 1)){
    digitalWrite(heaterPin,HIGH);
  }
  else{
    digitalWrite(heaterPin,LOW);
  }
} 

int chiller(int heaterTarget, int kettleTempRead)             // CHILLER OPERATION FUNCTION
{
  
  if (kettleTempRead > heaterTarget){
    digitalWrite(chillerPin,HIGH);
  }
  else{
    digitalWrite(chillerPin,LOW);
  }
} 

void get_message() {
  Serial.print('\n');
  num_steps = EEPROM.read(2);
  Serial.print("number of steps: ");
  Serial.print(num_steps);
  Serial.print('\n');
  for (int i = 0; i < num_steps; i++) {
    // Put into data structure for easy reading later
    // It is possible to save a datastucture in EEPROM, IDK how to do that yet, if I learn in time I may implement that when data is being read.
    recipeInstructs RI = {EEPROM.read(step_addr), EEPROM.read(time_addr), (char) EEPROM.read(timeu_addr), EEPROM.read(temp_addr), EEPROM.read(stage_addr)};
    step_addr = step_addr + 5;
    time_addr = time_addr + 5;
    timeu_addr = timeu_addr + 5;
    temp_addr = temp_addr + 5;
    stage_addr = stage_addr + 5;
    
    // Example of using the information
    Serial.print(RI.step);
    Serial.print('/');
    Serial.print(RI.time);
    Serial.print('/');
    Serial.print(RI.time_unit);
    Serial.print('/');
    Serial.print(RI.temp);
    Serial.print('/');
    Serial.print(stages[RI.stage]);
    Serial.print('\n');
  }

    step_addr = 3;
    time_addr = 4;
    timeu_addr = 5;
    temp_addr = 6;
    stage_addr = 7;
}
//Serial.print(" Temp F: ");
//Serial.print(sensors.getTempF(deviceAddress)); // Makes a second call to getTempC and then converts to Fahrenheit

//   method 2 - faster
//  float tempC = sensors.getTempC(deviceAddress);
//  if(tempC == DEVICE_DISCONNECTED_C) 
//  {
//    Serial.println("Error: Could not read temperature data");
//    return;
//  }
//  Serial.print("Temp C: ");
//  Serial.print(tempC);
//  Serial.print(" Temp F: ");
//  Serial.println(DallasTemperature::toFahrenheit(tempC)); // Converts tempC to Fahrenheit
//}
