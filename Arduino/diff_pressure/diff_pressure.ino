/***************************************************************

 cs pin= Arduino 8
 sdo/rdy/miso pin = Arduino 12
 sck= Arduino 13
*****************************************************************/
#include <SPI.h>


unsigned char sspin=8; //cs pin

union{
    int32_t value;
    uint8_t aa[4];
  } c ;
  

void setup(void){
pinMode(12,INPUT);  //to check ready pin
pinMode(sspin,OUTPUT);
digitalWrite(sspin,HIGH);//for single conversion
SPI.begin();
SPI.setBitOrder(MSBFIRST);
SPI.setDataMode(SPI_MODE3);
SPI.setClockDivider(SPI_CLOCK_DIV16);//max. speed of chip is 5 Mhz
Serial.begin(9600);  

}

void loop(void){
 
digitalWrite(sspin,LOW);

while(digitalRead(12)){
  
  digitalWrite(sspin,LOW);
                    
                    }
c.aa[2]=SPI.transfer(0x00);
c.aa[1]=SPI.transfer(0x00);
c.aa[0]=SPI.transfer(0x00);
c.aa[3]=0x00;
digitalWrite(sspin,HIGH);
//check if overflow has occured
if((c.aa[2]&(1<<6))|(c.aa[2]&(1<<7))){
  c.aa[2]&=~(1<<6);
  Serial.println(c.value*(5.0 / 4194304.0));;
  
}
//check if sign bit is affected. if so, since it is two's compliment,
// substract it from 2^N
else if(c.aa[2]&(1<<5)){
c.value=0x400000-c.value;
Serial.println(c.value*(5.0 / 4194304.0));;

}

else{
Serial.println(c.value*(5.0 / 4194304.0));;

}
  delay(10);

}
