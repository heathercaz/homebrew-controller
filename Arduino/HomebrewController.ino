#include <Wire.h> 
#include <LiquidCrystal_I2C.h>

//Declare LCD i2c addresses
LiquidCrystal_I2C lcd1(0x27, 16, 2);
LiquidCrystal_I2C lcd2(0x26, 16, 2);

//Declare Pin Usage
int startButton = 48; int previousButton = 49; int nextButton = 50;    // Assign pins to peripherals
int startReadOld = 1; int previousReadOld = 1; int nextReadOld = 1;


//Declare global variables 

  int startRead;
  int previousRead;
  int nextRead;
  int stageState = 0;
  int stageNumber = 1;
  int totalStages = 5;                                          // THIS NEEDS TO BE PULLED FROM PARSER LATER
  
  unsigned long lastDebounceTime = 0;               // This is reset to millis() each time a switch is pressed
  unsigned long debounceDelay = 200;                // Debounce delay, 200ms seems like a good balance
 
  const unsigned long kettleTimeIncr = 1000;        // Kettle timer count down every second
  const unsigned long fermentorTimeIncr = 60000;    // Fermentor timers count down every minute
  unsigned long previousTime_1 = 0;
  unsigned long previousTime_2 = 0;
  unsigned long kettleTime = 60;
    

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  // initialize the LCD
  lcd1.begin(); lcd2.begin(); lcd1.backlight(); lcd2.backlight();
  // initialize buttons
  pinMode(startButton, INPUT); pinMode(previousButton, INPUT); pinMode(nextButton, INPUT);

}

void loop() {
  // put your main code here, to run repeatedly:

//STAGE BUTTON CONTROL OPERATION
  
  if ((millis() - lastDebounceTime) > debounceDelay){   //check if more time has passed than debounce Delay
    lastDebounceTime = millis();                        //reset debounce timer
    startRead = digitalRead(startButton);
    nextRead = digitalRead(nextButton);
    previousRead = digitalRead(previousButton);
    if (startRead==0){
      if (stageState==0){
        stageState=1;
        lcd1.print("             ON ");
        lcd1.setCursor(0,0);
      
      }
      else {
        stageState=0;
        lcd1.print("             OFF");
        lcd1.setCursor(0,0);
      
      }
    }
    if (nextRead==0 && stageState==0){
      if (stageNumber <= totalStages){
        stageNumber = stageNumber + 1;
      }
      if (stageNumber == (totalStages+1)){
        stageNumber = 1;
      }      
    }
    if (previousRead==0 && stageState==0){
      if (stageNumber > 0){
        stageNumber = stageNumber - 1;
      }
      if (stageNumber == 0){
        stageNumber = totalStages;
      }
    }    
  }

// STAGE INFORMATION DISPLAY
  lcd1.print("S" + String(stageNumber) + ":");
  lcd1.setCursor(0,0);
  
  Serial.println(stageNumber);  

  unsigned long currentTime = millis();

  if(currentTime-previousTime_1>=kettleTimeIncr){
    previousTime_1 = currentTime;
    kettleTime = kettleTime - 1;
    if (kettleTime == 0){
      kettleTime = 60;
    }
    lcd2.print(kettleTime);
    lcd2.setCursor(0,0);
    
  }
  

  
}
