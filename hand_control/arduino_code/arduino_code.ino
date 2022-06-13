
const int ledPin_1 = 10;     //pwm输出引脚
const int ledPin_2 = 9; 
const int ledPin_3 = 11; 
String start;
int pwm_1 = 50;
int pwm_2 = 50;
int pwm_3 = 50;
void setup()  
{  
  Serial.begin(115200);//设置波特率为9600，这里要跟软件设置相一致。当接入特定设备（如：蓝牙）时，
  //analogReference(INTERNAL);
  //pinMode(A0,INPUT_PULLUP);
}  
  
void loop()  
{  
 while (1)
{
 start = Serial.readStringUntil('s');
 if(start == "01")
 {
  pwm_1 = pwm_1+30;
  pwm_2 = pwm_2;
  pwm_3 = pwm_3;
  
analogWrite(ledPin_1,pwm_1);
analogWrite(ledPin_2,pwm_2);
analogWrite(ledPin_3,pwm_3);
 }

 if(start == "02")
 {
  pwm_1 = pwm_1;
  pwm_2 = pwm_2+30;
  pwm_3 = pwm_3;
analogWrite(ledPin_1,pwm_1);
analogWrite(ledPin_2,pwm_2);
analogWrite(ledPin_3,pwm_3);
 }

 if(start == "03")
 {
  pwm_1 = pwm_1;
  pwm_2 = pwm_2;
  pwm_3 = pwm_3+30;
analogWrite(ledPin_1,pwm_1);
analogWrite(ledPin_2,pwm_2);
analogWrite(ledPin_3,pwm_3);
 }
 
  if(start == "04")
 {
  pwm_1 = pwm_1-30;
  pwm_2 = pwm_2;
  pwm_3 = pwm_3;
  if (pwm_1<0) 
  {pwm_1=0;}
analogWrite(ledPin_1,pwm_1);
analogWrite(ledPin_2,pwm_2);
analogWrite(ledPin_3,pwm_3);
 }

   if(start == "05")
 {
  pwm_1 = pwm_1;
  pwm_2 = pwm_2-30;
  pwm_3 = pwm_3;
    if (pwm_2<0) 
  {pwm_2=0;}
analogWrite(ledPin_1,pwm_1);
analogWrite(ledPin_2,pwm_2);
analogWrite(ledPin_3,pwm_3);
 }

    if(start == "06")
 {
  pwm_1 = pwm_1;
  pwm_2 = pwm_2;
  pwm_3 = pwm_3-30;
      if (pwm_3<0) 
  {pwm_3=0;}
analogWrite(ledPin_1,pwm_1);
analogWrite(ledPin_2,pwm_2);
analogWrite(ledPin_3,pwm_3);
 }

     if(start == "07")
 {
  pwm_1 = pwm_1+3;
  pwm_2 = pwm_2;
  pwm_3 = pwm_3;

analogWrite(ledPin_1,pwm_1);
analogWrite(ledPin_2,pwm_2);
analogWrite(ledPin_3,pwm_3);
 }

      if(start == "08")
 {
  pwm_1 = pwm_1;
  pwm_2 = pwm_2+3;
  pwm_3 = pwm_3;

analogWrite(ledPin_1,pwm_1);
analogWrite(ledPin_2,pwm_2);
analogWrite(ledPin_3,pwm_3);
 }

       if(start == "09")
 {
  pwm_1 = pwm_1;
  pwm_2 = pwm_2;
  pwm_3 = pwm_3+3;
analogWrite(ledPin_1,pwm_1);
analogWrite(ledPin_2,pwm_2);
analogWrite(ledPin_3,pwm_3);
 }
        if(start == "10")
 {
  pwm_1 = pwm_1-3;
  pwm_2 = pwm_2;
  pwm_3 = pwm_3;
  if (pwm_1<0) 
  {pwm_1=0;}
analogWrite(ledPin_1,pwm_1);
analogWrite(ledPin_2,pwm_2);
analogWrite(ledPin_3,pwm_3);
 }

         if(start == "11")
 {
  pwm_1 = pwm_1;
  pwm_2 = pwm_2-3;
  pwm_3 = pwm_3;
  if (pwm_2<0) 
  {pwm_2=0;}
analogWrite(ledPin_1,pwm_1);
analogWrite(ledPin_2,pwm_2);
analogWrite(ledPin_3,pwm_3);
 }

         if(start == "12")
 {
  pwm_1 = pwm_1;
  pwm_2 = pwm_2;
  pwm_3 = pwm_3-3;
  if (pwm_3<0) 
  {pwm_3=0;}
analogWrite(ledPin_1,pwm_1);
analogWrite(ledPin_2,pwm_2);
analogWrite(ledPin_3,pwm_3);
 }

         if(start == "13")
 {
  pwm_1 = pwm_1;
  pwm_2 = pwm_2;
  pwm_3 = pwm_3;

analogWrite(ledPin_1,pwm_1);
analogWrite(ledPin_2,pwm_2);
analogWrite(ledPin_3,pwm_3);
 }

          if(start == "14")
 {
  pwm_1 = 50;
  pwm_2 = 50;
  pwm_3 = 50;

analogWrite(ledPin_1,pwm_1);
analogWrite(ledPin_2,pwm_2);
analogWrite(ledPin_3,pwm_3);
 }
}
} 
