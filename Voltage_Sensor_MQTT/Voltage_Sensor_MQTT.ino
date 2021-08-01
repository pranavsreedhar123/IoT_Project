#include <ESP8266WiFi.h>
#include <PubSubClient.h>

// Update these with values suitable for your network.

const char* ssid = "Livebox-F7A6";
const char* password = "6D5CF624D45C4DEAD5514FA436";
const char* mqtt_server = "192.168.1.10";
int BAT= A0;              //Analog channel A0 as used to measure battery voltage
float RatioFactor=2.93;  //Resistors Ratio Factor

WiFiClient espClient;
PubSubClient client(espClient);
unsigned long lastMsg = 0;
#define MSG_BUFFER_SIZE  (50)
char msg[MSG_BUFFER_SIZE];
int value = 0;

void setup_wifi() {

  delay(10);
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  randomSeed(micros());

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }
  Serial.println();

  // Switch on the LED if an 1 was received as first character
  if ((char)payload[0] == '1') {
    digitalWrite(BUILTIN_LED, LOW);   // Turn the LED on (Note that LOW is the voltage level
    // but actually the LED is on; this is because
    // it is active low on the ESP-01)
  } else {
    digitalWrite(BUILTIN_LED, HIGH);  // Turn the LED off by making the voltage HIGH
  }

}

void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Create a random client ID
    String clientId = "ESP8266Client-";
    clientId += String(random(0xffff), HEX);
    // Attempt to connect
    if (client.connect(clientId.c_str())) {
      Serial.println("connected");
      // Once connected, publish an announcement...

      int value = LOW;
  float Tvoltage=0.0;
  float Vvalue=0.0,Rvalue=0.0;

   /////////////////////////////////////Battery Voltage//////////////////////////////////  
  for(unsigned int i=0;i<10;i++){
  Vvalue=Vvalue+analogRead(BAT);         //Read analog Voltage
  delay(5);                              //ADC stable
  }
  Vvalue=(float)Vvalue/10.0;            //Find average of 10 values
  Rvalue=(float)(Vvalue/1024.0)*5;      //Convert Voltage in 5v factor
  Tvoltage=Rvalue*RatioFactor;          //Find original voltage by multiplying with factor
    /////////////////////////////////////Battery Voltage//////////////////////////////////
    value = HIGH;
  Serial.println("Battery Voltage = ");
  Serial.println(Tvoltage);
  if(value == HIGH) {
    Serial.println("Updated");
    
  } else {
    Serial.print("Not Updated");
  }
  //String  VoltageString = "";
  //client.publish("Voltagedata", String(Tvoltage,2));
  if(Tvoltage<=1){
    Serial.println("UPS Drained");
    client.publish("Voltagedata","UPS is Full");
    }
  else if(Tvoltage>2 && Tvoltage<=8){
    Serial.println("UPS needs to be recharged");
    client.publish("Voltagedata","UPS is Full");
    }
  else{
      Serial.println("UPS is Full");
      client.publish("Voltagedata","UPS is Full");
      }
      // ... and resubscribe
      client.subscribe("inTopic");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

void setup() {
  pinMode(BUILTIN_LED, OUTPUT);     // Initialize the BUILTIN_LED pin as an output
  Serial.begin(115200);
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
}

void loop() {

  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  unsigned long now = millis();
  if (now - lastMsg > 2000) {
    lastMsg = now;
    ++value;
      int value = LOW;
  float Tvoltage=0.0;
  float Vvalue=0.0,Rvalue=0.0;

   /////////////////////////////////////Battery Voltage//////////////////////////////////  
  for(unsigned int i=0;i<10;i++){
  Vvalue=Vvalue+analogRead(BAT);         //Read analog Voltage
  delay(5);                              //ADC stable
  }
  Vvalue=(float)Vvalue/10.0;            //Find average of 10 values
  Rvalue=(float)(Vvalue/1024.0)*5;      //Convert Voltage in 5v factor
  Tvoltage=Rvalue*RatioFactor;          //Find original voltage by multiplying with factor
    /////////////////////////////////////Battery Voltage//////////////////////////////////
    value = HIGH;
  Serial.println("Battery Voltage = ");
  Serial.println(Tvoltage);
  if(value == HIGH) {
    Serial.println("Updated");
    
  } else {
    Serial.print("Not Updated");
  }
   if(Tvoltage<=1){
    Serial.println("UPS Drained");
    client.publish("Voltagedata","UPS is Full");
    }
  else if(Tvoltage>2 && Tvoltage<=8){
    Serial.println("UPS needs to be recharged");
    client.publish("Voltagedata","UPS is Full");
    }
  else{
      Serial.println("UPS is Full");
      client.publish("Voltagedata","UPS is Full");
      }
  }
}
