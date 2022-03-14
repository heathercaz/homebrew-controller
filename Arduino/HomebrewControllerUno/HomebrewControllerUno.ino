#include <Wire.h> 
#include <LiquidCrystal_I2C.h>
#include <Adafruit_MLX90614.h>
Adafruit_MLX90614 mlx = Adafruit_MLX90614();
#include <OneWire.h>
#include <DallasTemperature.h>


//Declare LCD i2c addresses
LiquidCrystal_I2C lcd1(0x27, 16, 2);
LiquidCrystal_I2C lcd2(0x26, 16, 2);

//Declare Pin Usage
int startButton = 0; int previousButton = 1; int nextButton = 2;    // Assign button pins
int startReadOld = 1; int previousReadOld = 1; int nextReadOld = 1; // Button Initializations

//One wire usage:
#define ONE_WIRE_BUS 4                                // Data wire is plugged into port 4 on the Arduino
OneWire oneWire(ONE_WIRE_BUS);                        // Setup a oneWire instance to communicate with any OneWire devices (not just Maxim/Dallas temperature ICs)
DallasTemperature sensors(&oneWire);                  // Pass our oneWire reference to Dallas Temperature.


int fermentor1Pin = 7;
int heaterPin = 10;

//Declare global variables 

  int startRead;
  int previousRead;
  int nextRead;
  bool stageState = false;
  int stageNumber = 1;
                                            
  
  unsigned long lastDebounceTime = 0;               // This is reset to millis() each time a switch is pressed
  unsigned long debounceDelay = 150;                // Debounce delay, 200ms seems like a good balance

 //Stage Info Default Declarations
  bool parserGate = false;
  int totalStages = 5;
  int stageName[] = {0,1,2,1,2};  //Stage "name" codes to be displayed on LCD from stageNames
  //int *stageTemp = (int *) malloc(totalStages * sizeof(int));
  int stageTemp[] = {25,30,40,50,30};                                          //Stage target temp in C
  //int *stageTime = (int *) malloc(totalStages * sizeof(int));
  int stageTime[] = {3,3,4,6,2};
  int stageDevice[] = {1,1,2,1,2}; //1 for kettle, 2 for chiller, 3 for fermenter 1, etc...

//  int stageName[50];
  String stageNames[] = {"PREHEAT","HEATING","CHILLING"};             //Stage "name" to be displayed on LCD
//  int stageTemp[50];                                                  //Stage target temp in C
//  int stageTime[50];                                                  //Stage time in minutes

 //Timer initializations
  const unsigned long kettleTimeIncr = 1000;        // Kettle timer count down every second
  const unsigned long fermentorTimeIncr = 60000;    // Fermentor timers count down every minute
  unsigned long previousTime_1 = 0;
  unsigned long previousTime_2 = 0;

  int kettleMinutes = 0;
  int kettleSeconds = 0;
  unsigned long kettleTime;
    
//------------VOID SETUP----------------------------------------------------------------------

void setup() {
  // put your setup code here, to run once:

  Serial.begin(9600);
  // initialize the LCD
  lcd1.begin(); lcd2.begin(); lcd1.backlight(); lcd2.backlight();
  // initialize buttons
  pinMode(startButton, INPUT); pinMode(previousButton, INPUT); pinMode(nextButton, INPUT);  //setting pinmodes for buttons
  // contactless sensor
  mlx.begin();
  // contact sensor
  sensors.begin();
  
  // equipment pins
  pinMode(fermentor1Pin, OUTPUT);

}

//------------VOID LOOP----------------------------------------------------------------------
void loop() {
  // put your main code here, to run repeatedly:

//STAGE PARAMETER POPULATION (FROM PARSER)


//FERMENTOR CONTROL
  int fermentorState[3] = {1,0,0}; //EG Fermentor 1 running, 2 and 3 off. 1 should be set to 0 once that fermentor is finished running based on timer
  int f1Target = 24;               //EG Fermentor 1 target temp is 24C

  if (fermentorState[0] == 1){
  int f1Temp = fermentor1(f1Target);
  }
  
 
//STAGE & BUTTON CONTROL OPERATION
  
  if ((millis() - lastDebounceTime) > debounceDelay){   //check if more time has passed than debounce Delay
    lastDebounceTime = millis();                        //reset debounce timer
    startRead = digitalRead(startButton);
    nextRead = digitalRead(nextButton);
    previousRead = digitalRead(previousButton);
    if (startRead==0){                                            // START/STOP button operation
      stageState = !stageState;
      
    }
    if (nextRead==0 && previousRead==0 && stageState==false){                   // Parser gate control (NEXT & PREVIOUS button pressed at same time)
      parserGate=!parserGate;
      lcd1.clear();
      if (parserGate == true){
        kettleTime = (stageTime[(stageNumber-1)])*60000;         
      }
      
    }
    if (nextRead==0 && stageState==false){                  // NEXT button operation
      lcd1.clear();
      if (stageNumber <= totalStages){
        stageNumber = stageNumber + 1;
      }
      if (stageNumber == (totalStages+1)){
        stageNumber = 1;
      } 
      kettleTime = (stageTime[(stageNumber-1)])*60000;      
    }
    if (previousRead==0 && stageState==false){              // PREVIOUS button operation
      lcd1.clear();
      if (stageNumber > 0){
        stageNumber = stageNumber - 1;
      }
      if (stageNumber == 0){
        stageNumber = totalStages;
      }
      kettleTime = (stageTime[(stageNumber-1)])*60000; 
    }    
  }   // END BUTTON AND STAGE CONTROL

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

// HEATER CONTROL
  int heaterTarget = stageTemp[stageNumber-1];
  int kettleTempRead = sensors.getTempCByIndex(0);
  Serial.println(sensors.getTempCByIndex(0));
  
  if (stageState==true && stageDevice[stageNumber-1]==1 ){
    
  int kettleTemp = heater(heaterTarget, kettleTempRead);
  }

  
// STAGE INFORMATION DISPLAY
  //lcd1.clear();
  lcd1.setCursor(0,0);
  lcd1.print("S" + String(stageNumber) + " :" + stageNames[stageName[stageNumber-1]]);    //LCD1 Stage number, name, state
  lcd1.setCursor(13,0);
  if (stageState == true){
    lcd1.print("ON ");
    lcd1.setCursor(0,0);     
  }
  if (stageState == false) {
    lcd1.print("OFF");
    lcd1.setCursor(0,0);
  }
  
  lcd1.setCursor(0,1);
  lcd1.print(String(kettleMinutes) + ":" + String(kettleSeconds));             //LCD1 Time Remaining
  lcd1.setCursor(6,1);
  lcd1.print(String(stageTemp[stageNumber-1])+"C");
  lcd1.setCursor(11,1);
  lcd1.print(String(kettleTempRead)+"C");
  lcd1.setCursor(0,0);

  //Serial.println("S" + String(stageNumber) + " :" + String(stageNames[stageName[stageNumber-1]])+ " " + String(kettleMinutes) + ":" + String(kettleSeconds) +" " + String(stageTemp[stageNumber-1])+"C"); 
  
  

    
}     //END VOID LOOP


//----------- FUNCTIONS----------------------------------------------------------------------------

float fermentor1(int f1Target){                       //FERMENTOR 1 OPERATION FUNCTION, RETURNS FERMENTER 1 TEMP
    float f1TempData = mlx.readObjectTempC();
    int f1Temp = f1TempData;
    if (f1Temp > f1Target){
      digitalWrite(fermentor1Pin,HIGH);
    }
    else{
      digitalWrite(fermentor1Pin,LOW);
    }
    lcd2.print("F1:"+ String(f1Temp));
    lcd2.setCursor(5,0);
    lcd2.print("C");
    lcd2.setCursor(0,0);
    return(f1TempData);
}

float heater(int heaterTarget, int kettleTempRead)             // HEATER OPERATION FUCNTION
{
//  method 1 - slower
  
  if (kettleTempRead < heaterTarget){
    digitalWrite(heaterPin,HIGH);
  }
  else{
    digitalWrite(heaterPin,LOW);
  }
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
