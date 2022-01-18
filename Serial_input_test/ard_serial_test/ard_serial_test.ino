char ser;

void setup() 
{
  pinMode(12,OUTPUT);
  pinMode(13,OUTPUT);
  pinMode(7, OUTPUT);
  digitalWrite(7,LOW);
  digitalWrite(12, LOW);
  digitalWrite(13,LOW);  
  Serial.begin(9600);
  while(Serial.available() == 0) {
    } // wait for input
  ser = Serial.read();
  Serial.print(F("recieved "));
  Serial.print(ser);
}

void green_q(){
    digitalWrite(7,HIGH);
    delay(1000);
    digitalWrite(7,LOW);
    delay(1000);
}

void green_j(){
    digitalWrite(7,HIGH);
    delay(500);
    digitalWrite(7,LOW);
    delay(500);
}
void loop() 
{

    if(ser == 'q') // red
    {
      digitalWrite(13,HIGH);
      digitalWrite(12,LOW);
      green_q();
    }
    
    else if (ser == 'j'){ // yellow
      
      digitalWrite(12,HIGH);
      digitalWrite(13,LOW);
      green_j();
      
    }
    Serial.print(ser);

}
