#include <Servo.h>

#define delay_time 750
#define ptr_delay 500

Servo arm; //pin 9
Servo rot; //pin 10
Servo ptr; //pin 5

String sr_buf = "";

void setup() {
  
  Serial.begin(9600);
  //Serial.print("Ready!");

  arm.attach(9);
  rot.attach(10);
  ptr.attach(5);

  arm.write(90);
  ptr.write(0);
  rot.write(90);
  //Serial.print("entcmd");
  
  Serial.print('e');
}

String cmd = "";
unsigned int timecount = 0

void loop() {
  
  if(Serial.available() > 0){
    sr_buf = sr_buf + Serial.readString();  
    timecount = 0;
  }

  timecount++;

  //Enter some random number
  if (timecount > 5000000){
    Serial.print("e");
    timecount = 0;
  }

  if(sr_buf.length() >= 3){
    cmd = sr_buf.substring(0,3);
    sr_buf = sr_buf.substring(3);

    int pos = (int)((cmd[1] - '0')*16 + cmd[2] - '0');
    
    switch(cmd[0]){
    case 'a':
      arm.write(pos%181);
      //Serial.println("wt");
      Serial.print("a");
      break;
    case 'b':
      rot.write(pos%181);
      //Serial.println("Writing " + String(pos) + " to rotor"); 
      Serial.print("b");
      break;
    case 'c':
      ptr.write(pos%181);
      //Serial.println("Writing " + String(pos) + " to pointer"); 
      Serial.print("c");
      break;
    case 'd':
      delay(pos*10);
      Serial.print("d");
      //Serial.println("Delaying " + String(pos*10) + "ms");
      break;
  }
  }
  
}
/*
void getcmd(){

  byte i = 0;

  Serial.print("Buffer:" + sr_buf);
  
  while(sr_buf.length() <= 3){

      if(i == 0){
        Serial.print('e');  
      }
      
      if(Serial.available() > 0){
        sr_buf += Serial.readString();  
      }
      
      i = (i +1)%63;
  }
}
*/
void docmd(){
  
  if(sr_buf.length() <= 3){
    getcmd();
  }
  
  String cmd = sr_buf.substring(0,3);

  //Serial.println("Command: " + cmd);

  sr_buf = sr_buf.substring(3);
  
  int pos = 0;
  
  for(int k = 1; k < cmd.length(); k++){
    pos = pos*16 + (cmd[k] - '0');
  }
  
  switch(cmd[0]){
    case 'a':
      arm.write(pos%181);
      //Serial.println("wt");
      Serial.print("a");
      break;
    case 'b':
      rot.write(pos%181);
      //Serial.println("Writing " + String(pos) + " to rotor"); 
      Serial.print("b");
      break;
    case 'c':
      ptr.write(pos%181);
      //Serial.println("Writing " + String(pos) + " to pointer"); 
      Serial.print("c");
      break;
    case 'd':
      delay(pos*10);
      Serial.print("d");
      //Serial.println("Delaying " + String(pos*10) + "ms");
      break;
  }

//  delay(delay_time);

//  if(pos == 0 && cmd[0] == 'c'){
//    delay(ptr_delay);
//  }
  
}
