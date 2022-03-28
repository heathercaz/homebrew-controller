#include <EEPROM.h>
int addr;
volatile int button; // used in button handler for button state
int saved_val; // used for debugging
volatile int saved_button; // holds the state of the serial mode button

int ser; // holds incoming serial value

// initialize retrieval addresses
int step_addr = 3;
int time_addr = 4;
int timeu_addr = 5;
int temp_addr = 6;
int stage_addr = 7;

byte num_steps;
int step_flag = 0; // indicates if next message is step info
int step_count = 0; // counts number of steps added (used as back up because of step flag bug)
int start_flag = 0; // indicates the start of instruction info

// Data struct to hold one step of a recipe instruction
struct recipeInstructs {
  byte step; // stored in addr = step+ 2
  byte time; // stored in addr = step + 3
  byte time_unit; //stored in addr = step + 4
  byte temp; // stored in addr = step + 5
  byte stage; // stored in addr = step + 5
};

void setup()
{
  pinMode(12, OUTPUT);
  pinMode(13, OUTPUT);
  pinMode(7, OUTPUT);
  pinMode(2, INPUT_PULLUP);
  digitalWrite(7, LOW);
  digitalWrite(12, LOW);
  digitalWrite(13, LOW);

  Serial.begin(9600);
  button = 0;
  saved_button = 0;
  addr = 3;
  Serial.flush();

  attachInterrupt(digitalPinToInterrupt(2), button_handler, RISING);

}

void loop()
{

  //TODO add state in which EEPROM is cleared before writing to it for new recipes

  saved_button = EEPROM.read(0); // serial mode saved in address 0
  digitalWrite(7, saved_button);
  // Waits until in "serial mode" to write values
  if (Serial.available() > 0 && saved_button == 1) {
    ser = Serial.read();

    // check if start byte has been read and end byte hasn't
    // update EEPROM with new value
    if (start_flag == 1 && ser != '&') {
      EEPROM.update(addr, ser);
      addr++;
    }

//    if (step_flag == 1) {
//      EEPROM.update(2, ser); // save number of steps in address 2
//      step_flag == 0;
//    }

    // ! means incoming byte is total number of steps
    if (ser == '!') {
      digitalWrite(12, HIGH);
      digitalWrite(13, HIGH);
      delay(200);
      digitalWrite(12, LOW);
      digitalWrite(13, LOW);
//      EEPROM.update(2, ser);
      step_flag = 1;
    }

    // check for start byte and set start flag
    if (ser == '#') { // start char
      digitalWrite(12, LOW);
      digitalWrite(13, HIGH);
      delay(200);
      digitalWrite(13, LOW);
      start_flag = 1;
    }
    //check for stop byte and reset start flag
    else if (ser == '&') { // stop char
      step_count++;
      digitalWrite(13, LOW);
      digitalWrite(12, HIGH);
      delay(200);
      digitalWrite(12, LOW);
      start_flag = 0;\
      EEPROM.update(2, step_count);
    }
    
  }
  char start = EEPROM.read(1);
  get_message();

}
// ------------------------------ Functions ----------------------------------------

void get_message() {
  Serial.print('\n');
  num_steps = EEPROM.read(2);
  Serial.print(num_steps);
  Serial.print('\n');
  for (int i = 0; i < num_steps; i++) {

    recipeInstructs RI = {EEPROM.read(step_addr), EEPROM.read(time_addr), EEPROM.read(timeu_addr), EEPROM.read(temp_addr), EEPROM.read(stage_addr)};
    step_addr = step_addr + 5;
    time_addr = time_addr + 5;
    timeu_addr = timeu_addr + 5;
    temp_addr = temp_addr + 5;
    stage_addr = stage_addr + 5;

    Serial.print(RI.step);
    Serial.print('/');
    Serial.print(RI.time);
    Serial.print('/');
    Serial.print(RI.time_unit);
    Serial.print('/');
    Serial.print(RI.temp);
    Serial.print('/');
    Serial.print(RI.stage);
    Serial.print('\n');
  }

    step_addr = 3;
    time_addr = 4;
    timeu_addr = 5;
    temp_addr = 6;
    stage_addr = 7;
}
//---------------------------Interupt Handler----------------------------------------
void button_handler() {
  static unsigned long last_interrupt_time = 0;
  unsigned long interrupt_time = millis();
  // If interrupts come faster than 200ms, assume it's a bounce and ignore
  if (interrupt_time - last_interrupt_time > 200)
  {
    if (button == 0) {
      for (int i = 1 ; i < EEPROM.length() ; i++) {
        EEPROM.write(i, 0);
      }
    }
    button = EEPROM.read(0);
    button = !button;


    EEPROM.update(0, button);
    Serial.print("HELLO ");
    Serial.print(button);
  }
  last_interrupt_time = interrupt_time;
}
