#include <EEPROM.h>
int addr;
volatile int button;
char saved_val;
volatile int saved_button;

int ser;
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
  addr = 0;

  attachInterrupt(digitalPinToInterrupt(2), button_handler, RISING);

}

void green_q() {
  digitalWrite(7, HIGH);
  delay(1000);
  digitalWrite(7, LOW);
  delay(1000);
}

void green_j() {
  digitalWrite(7, HIGH);
  delay(500);
  digitalWrite(7, LOW);
  delay(500);
}

void button_handler() {
  static unsigned long last_interrupt_time = 0;
  unsigned long interrupt_time = millis();
  // If interrupts come faster than 200ms, assume it's a bounce and ignore
  if (interrupt_time - last_interrupt_time > 200)
  {
    button = !button;
    EEPROM.update(1, button);
    Serial.print("HELLO ");
    Serial.print(button);
  }
  last_interrupt_time = interrupt_time;


}
void loop()
{
  Serial.print("saved val: ");
  Serial.print(saved_val);
  Serial.print("\n");


  digitalWrite(7, saved_button);
    saved_button = EEPROM.read(1);\

    // Waits until in "serial mode" to write values
    if (Serial.available() >0 && saved_button == 1){
    ser = Serial.read();
    EEPROM.update(0, ser);
    }
    
    saved_val = EEPROM.read(0);
  if (saved_val == 'q') // red
  {
    digitalWrite(13, HIGH);
    digitalWrite(12, LOW);
  }

  else if (saved_val == 'j') { // yellow

    digitalWrite(12, HIGH);
    digitalWrite(13, LOW);

  }
  else {
    digitalWrite(12, LOW);
    digitalWrite(13, LOW);
  }


}