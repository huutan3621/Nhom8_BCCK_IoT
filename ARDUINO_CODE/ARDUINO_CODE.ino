
#include <FirebaseESP8266.h>
#include <ESP8266WiFi.h>
#include <time.h>
#include <ArduinoJson.h>//ArduinoJson 5
#include <ESP8266HTTPClient.h>

// Set these to run example.
const int LED_1 = D3;
const int LED_2 = D4;
const int LED_3 = D5;
const int LED_4 = D6;
const int ledPin = D7;
const int high = 255;
const int low = 0;
WiFiServer server(80);
int timezone = 7 * 3600;
int dst = 0;
#define FIREBASE_HOST "https://test-1f0cf-default-rtdb.asia-southeast1.firebasedatabase.app/"
#define FIREBASE_AUTH "m2Za0hknbF68FZBbdwdcDiTJubBt6QhI167A8c3s"

#define WIFI_SSID "nth22"
#define WIFI_PASSWORD "22102210"
//Define the Firebase Data object
FirebaseData fbdo, fbdo_1, fbdo_2, fbdo_3, fbdo_4 ;
StaticJsonBuffer<300> JSONbuffer;   //Declaring static JSON buffer
HTTPClient http;    //Declare object of class HTTPClient
WiFiClient client;

void setup() {
  Serial.begin(9600);
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, LOW);
 
  // Connect to WiFi network
  Serial.println();
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(WIFI_SSID);
 
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("connecting");
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(500);
  }
  Serial.println();
  Serial.print("connected: ");
  Serial.println(WiFi.localIP());
 
  // Start the server
  server.begin();
  Serial.println("Server started");
 
  // Print the IP address
  Serial.print("Use this URL : ");
  Serial.print("http://");
  Serial.print(WiFi.localIP());
  Serial.println("/");
 
  Firebase.begin(FIREBASE_HOST, FIREBASE_AUTH);
  configTime(timezone, dst, "pool.ntp.org","time.nist.gov");
}
void loop() {

    if (Firebase.getString(fbdo,"/WEMOSD1/BULB/DEN1/DEN1")) {
      Serial.println("DEN1: " + fbdo.stringData());
      if(fbdo.stringData()=="1"){
        analogWrite(LED_1, high);
        digitalWrite(ledPin, HIGH);
        }
      else if(fbdo.stringData()=="0"){
        analogWrite(LED_1, low);
        digitalWrite(ledPin, LOW);
        }
      else if(fbdo.stringData()=="2"){
        if (Firebase.getFloat(fbdo,"/Brightness1")) {
          Serial.println(fbdo.floatData());
          analogWrite(LED_1,fbdo.floatData()*2.55);
        }
       }
    }    
    if (Firebase.getString(fbdo_1,"/WEMOSD1/BULB/DEN2/DEN2")) {
      if(fbdo_1.stringData()=="1"){
        analogWrite(LED_2, high);
        }
      else if(fbdo_1.stringData()=="0"){
        analogWrite(LED_2, low);
        }
      else if(fbdo_1.stringData()=="2"){
        if (Firebase.getFloat(fbdo_1,"/Brightness2")) {
          Serial.println(fbdo_1.floatData());
          analogWrite(LED_2,fbdo_1.floatData()*2.55);
        }
       }
    }
    if (Firebase.getString(fbdo_2,"/WEMOSD1/BULB/DEN3/DEN3")) {
      if(fbdo_2.stringData()=="1"){
        analogWrite(LED_3, high);
        }
      else if(fbdo_2.stringData()=="0"){
        analogWrite(LED_3, low);
        }
      else if(fbdo_2.stringData()=="2"){
        if (Firebase.getFloat(fbdo_2,"/Brightness3")) {
          Serial.println(fbdo_2.floatData());
          analogWrite(LED_3,fbdo_2.floatData()*2.55);
        }
       }
    }
    if (Firebase.getString(fbdo_3,"/WEMOSD1/BULB/DEN4/DEN4")) {
      if(fbdo_3.stringData()=="1"){
        analogWrite(LED_4, high);
        digitalWrite(LED_4, HIGH);
        Serial.print("DEN4: ");
        Serial.println(fbdo_3.stringData());
        }
      else if(fbdo_3.stringData()=="0"){
        analogWrite(LED_4, low);
        digitalWrite(LED_4, LOW);
        Serial.print("DEN4: ");
        Serial.println(fbdo_3.stringData());
        }
      else if(fbdo_3.stringData()=="2"){
        if (Firebase.getFloat(fbdo_3,"/Brightness4")) {
          Serial.println(fbdo_3.floatData());
          analogWrite(LED_4,fbdo_3.floatData()*2.55);
        }
       }
    }
    time_t now = time(nullptr);
    struct tm* p_tm = localtime(&now);
    String YYYY = (String)(1900 + p_tm->tm_year); // timeinfo.tm_year gives years since 1900
    String MM = (String)(1 + p_tm->tm_mon); // timeinfo.tm_mon gives months since january ie 0 - 11;
    String DD = (String)p_tm->tm_mday;
    String ESP_hour=(String)p_tm->tm_hour;
    String ESP_min=(String)p_tm->tm_min;
    String ESP_sec=(String)p_tm->tm_sec;
    if((int)p_tm->tm_mon + 1 <10){
      MM="0" + MM;
      }
    if((int)p_tm->tm_mday <10){
      DD="0" + DD;
      }
    if((int)p_tm->tm_min <10){
      ESP_min="0" + ESP_min;
      }
    if((int)p_tm->tm_hour <10){
      ESP_hour="0" + ESP_hour;
      }
    if((int)p_tm->tm_sec <10){
      ESP_sec="0" + ESP_sec;
      }
    String ESP_time = ESP_hour + ":" + ESP_min;
    String ESP_datetime = YYYY + "-" + MM + "-" + DD + " " + ESP_hour + ":" + ESP_min + ":" + ESP_sec;
    Serial.println("Time ESP: " + ESP_time);
    
  // TURN LED ON
  if (Firebase.getString(fbdo,"/Sche_On_1")) {
      if(fbdo.stringData() != "0"){
        Serial.println("Time Schedule Led 1 On: " + fbdo.stringData());
        if(fbdo.stringData()== ESP_time){
          digitalWrite(LED_1, HIGH);
          digitalWrite(ledPin, HIGH);
          Firebase.setString(fbdo,"/WEMOSD1/BULB/DEN1/DEN1", "1");
          Firebase.setFloat(fbdo,"/Brightness1", 100);
          Firebase.setString(fbdo,"/Sche_On_1", "0");
        }
    }} 
   if (Firebase.getString(fbdo_1,"/Sche_On_2")) {
      if(fbdo_1.stringData() != "0"){
        Serial.println("Time Schedule Led 2 On: " + fbdo_1.stringData());
       if(fbdo_1.stringData()==ESP_time){
          digitalWrite(LED_2, HIGH);
          Firebase.setString(fbdo_1,"/WEMOSD1/BULB/DEN2/DEN2", "1");
          Firebase.setFloat(fbdo_1,"/Brightness2", 100);
          Firebase.setString(fbdo_1,"/Sche_On_2", "0");
        }
    }}   
  if (Firebase.getString(fbdo_2,"/Sche_On_3")) {
      if(fbdo_2.stringData() != "0"){
        Serial.println("Time Schedule Led 3 On: " + fbdo_2.stringData());
       if(fbdo_2.stringData()==ESP_time){
          digitalWrite(LED_3, HIGH);
          Firebase.setString(fbdo_2,"/WEMOSD1/BULB/DEN3/DEN3", "1");
          Firebase.setFloat(fbdo_2,"/Brightness3", 100);
          Firebase.setString(fbdo_2,"/Sche_On_3", "0");
        }
    }}
   if (Firebase.getString(fbdo_3,"/Sche_On_4")) {
      if(fbdo_3.stringData() != "0"){
        Serial.println("Time Schedule Led 4 On: " + fbdo_3.stringData());
       if(fbdo_3.stringData()==ESP_time){
          digitalWrite(LED_4, HIGH);
          Firebase.setString(fbdo_3,"/WEMOSD1/BULB/DEN4/DEN4", "1");
          Firebase.setFloat(fbdo_3,"/Brightness4", 100);
          Firebase.setString(fbdo_3,"/Sche_On_4", "0");
        }
    }}


  // TURN LED OFF
  if (Firebase.getString(fbdo,"/Sche_Off_1")) {
      if(fbdo.stringData() != "0"){
        Serial.println("Time Schedule Led 1 Off: " + fbdo.stringData());
        if(fbdo.stringData()==ESP_time){
          digitalWrite(LED_1, LOW);
          digitalWrite(ledPin, LOW);
          Firebase.setString(fbdo,"/WEMOSD1/BULB/DEN1/DEN1", "0");
          Firebase.setFloat(fbdo,"/Brightness1", 0);
          Firebase.setString(fbdo,"/Sche_Off_1", "0");
        }
    }} 
   if (Firebase.getString(fbdo_1,"/Sche_Off_2")) {
      if(fbdo_1.stringData() != "0"){
        Serial.println("Time Schedule Led 2 Off: " + fbdo_1.stringData());
        if(fbdo_1.stringData()==ESP_time){
          digitalWrite(LED_2, LOW);
          Firebase.setString(fbdo_1,"/WEMOSD1/BULB/DEN2/DEN2", "0");
          Firebase.setFloat(fbdo_1,"/Brightness2", 0);
          Firebase.setString(fbdo_1,"/Sche_Off_2", "0");
        }
    }}   
  if (Firebase.getString(fbdo_2,"/Sche_Off_3")) {
      if(fbdo_2.stringData() != "0"){
        Serial.println("Time Schedule Led 3 Off: " + fbdo_2.stringData());
        if(fbdo_2.stringData()==ESP_time){
          digitalWrite(LED_3, LOW);
          Firebase.setString(fbdo_2,"/WEMOSD1/BULB/DEN3/DEN3", "0");
          Firebase.setFloat(fbdo_2,"/Brightness3", 0);
          Firebase.setString(fbdo_2,"/Sche_Off_3", "0");
        }
    }}
  if (Firebase.getString(fbdo_3,"/Sche_Off_4")) {
      if(fbdo_3.stringData() != "0"){
        Serial.println("Time Schedule Led 4 Off: " + fbdo_3.stringData());
        if(fbdo_3.stringData()==ESP_time){
          digitalWrite(LED_4, LOW);
          Firebase.setString(fbdo_3,"/WEMOSD1/BULB/DEN4/DEN4", "0");
          Firebase.setFloat(fbdo_3,"/Brightness4", 0);
          Firebase.setString(fbdo_3,"/Sche_Off_4", "0");
        }
    }}
  JsonObject& JSONencoder = JSONbuffer.createObject(); 
  JSONencoder["message"] = "this is a message of API";
  JSONencoder["data"] = ESP_datetime;
  Serial.println("Date Time ESP: " + ESP_datetime);
  char JSONmessageBuffer[300] = "";
  JSONencoder.prettyPrintTo(JSONmessageBuffer, sizeof(JSONmessageBuffer));
  Serial.println(JSONmessageBuffer);
  http.begin(client, "http://192.168.235.94:5000/postwemosd1");      //Specify request destination
  http.addHeader("Content-Type", "application/json");  //Specify content-type header
  int httpCode = http.POST(JSONmessageBuffer);   //Send the request
  Serial.println(httpCode);
  JSONencoder["message"] = "";
  JSONencoder["data"] = "";
  JSONbuffer.clear();
  delay(500);
  
}
