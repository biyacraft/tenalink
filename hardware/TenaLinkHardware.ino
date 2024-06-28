#include <SoftwareSerial.h>
#include <OneWire.h>
#include <DallasTemperature.h>
SoftwareSerial ESP8266(2, 3); // Rx,  Tx

long writingTimer = 17; 
long startTime = 0;
long waitTime = 0;

#define ONE_WIRE_BUS 5

OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);
const int sensor= 5; // Assigning analog pin A1 to variable 'sensor'
float tempc;  //variable to store temperature in degree Celsius
float vout;  //temporary variable to hold sensor reading
unsigned char check_connection=0;
unsigned char times_check=0;
boolean error;

String myAPIkey = "4164JEX10KFZ4RGS";  //Your Write API Key from Thingsspeak

void setup()
{
  Serial.begin(9600);
  sensors.begin(); 
  ESP8266.begin(9600); 
  pinMode(10, INPUT); // Setup for leads off detection LO +
  pinMode(11, INPUT); // Setup for leads off detection LO -
  startTime = millis(); 
  delay(4000);
  Serial.println("Connecting to Wifi");
   while(check_connection==0)
  {
  Serial.print(".");
  ESP8266.print("AT+CWJAP=\"Abi\",\"4141711609\"\r\n");
  ESP8266.setTimeout(5000);
 if(ESP8266.find("WIFI CONNECTED\r\n")==1)
 {
 Serial.println("WIFI CONNECTED");
 break;
 }
 times_check++;
 if(times_check>3) 
 {
  times_check=0;
   Serial.println("Trying to Reconnect..");
  }
  }
}

void loop()
{
  float temperatureC;
  waitTime = millis()-startTime;   
  if((digitalRead(10) == 1)||(digitalRead(11) == 1)){
  Serial.print("ECG Value: ");
  Serial.println(analogRead(A0));
  }
  else{
    // send the value of analog input 0:
  Serial.println(analogRead(A0));
  }
  //Wait for a bit to keep serial data from saturating
  delay(4000);
  if (waitTime > (writingTimer*1000))
  {
    sensors.requestTemperatures();
    float temperatureC = sensors.getTempCByIndex(0);
    //vout=analogRead(sensor);
    //vout=(vout*500)/1023;
    //tempc=vout; // Storing value in Degree Celsius
    startTime = millis();   
    Serial.print("Temperature: ");
    Serial.print(temperatureC);
    Serial.println(" degrees Celsius");
     
  ESP8266.flush();
  String cmd = "AT+CIPSTART=\"TCP\",\"";
  cmd += "184.106.153.149"; // api.thingspeak.com IP address
  cmd += "\",80";
  ESP8266.println(cmd);
  Serial.print("Start Commands: ");
  Serial.println(cmd);

  if(ESP8266.find("Error"))
  {
    Serial.println("AT+CIPSTART error");
    return;
  }
  // preparacao da string GET
  
  String getStr = "GET /update?api_key=";
  getStr += myAPIkey;
  getStr +="&field1=";
  getStr += String(temperatureC);
  getStr +="&field2=";
  getStr += String(analogRead(A0));
  getStr += "\r\n\r\n";
  GetThingspeakcmd(getStr); 
  }
  
}


void startThingSpeakCmd(void)
{
  
}

String GetThingspeakcmd(String getStr)
{
  String cmd = "AT+CIPSEND=";
  cmd += String(getStr.length());
  ESP8266.println(cmd);
  Serial.println(cmd);

  if(ESP8266.find(">"))
  {
    ESP8266.print(getStr);
    Serial.println(getStr);
    delay(500);
    String messageBody = "";
    while (ESP8266.available()) 
    {
      String line = ESP8266.readStringUntil('\n');
      if (line.length() == 1) 
      { 
        messageBody = ESP8266.readStringUntil('\n');
      }
    }
    Serial.print("MessageBody received: ");
    Serial.println(messageBody);
    return messageBody;
  }
  else
  {
    ESP8266.println("AT+CIPCLOSE");     
    Serial.println("AT+CIPCLOSE"); 
  } 
}
