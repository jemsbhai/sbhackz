int motorPin = 3;
int lightpin = 4;
 
void setup() 
{ 
  pinMode(lightpin, OUTPUT);
  pinMode(motorPin, OUTPUT);
  Serial.begin(115200);
  while (! Serial);
  Serial.println("Speed 0 to 255");
} 
 
 
void loop() 
{ 
  if (Serial.available())
  {
    int speed = Serial.parseInt();
    if (speed >= 0 && speed <= 255)
    {
      analogWrite(motorPin, speed);
    }
    int light = Serial.parseInt();
    if (light > 0 && light <= 255)
    {
      digitalWrite(lightpin, HIGH);
    }
    else
    {
      digitalWrite(lightpin, LOW);
    }
  }
} 
