// Open a serial connection and flash LED when input is received

void setup(){
  // Open serial connection.
  Serial.begin(9600);
  
}

void loop(){ 
  Serial.println(analogRead(A0) * 5);
} 

