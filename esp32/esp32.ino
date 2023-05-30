#include <WiFi.h>       //include wifi library       
#include <PubSubClient.h>  //include mqtt library


const char* ssid = "VIETTEL";                //wifi name
const char* password = "13012001";        //wifi password

WiFiClient espClient;
PubSubClient client(espClient);

const char* mqtt_server = "broker.hivemq.com";        //mqtt server address
#define msg_size  20        //max size of payload 
char msg[msg_size];         //payload

void setup_wifi() {
  WiFi.begin(ssid, password);
  Serial.println("Try to connect to wifi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void setup_mqtt() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Attempt to connect
    if (client.connect("ESP32_hoacchitrung_nguyengiahung", NULL, NULL, "last_will_topic", 2, true, "Esp32 disconnected", false)) {  //clientID, user, pass, willtopic, willqos, willretain, willmessage, clean session
      Serial.println("Connected to mqtt broker");                                                   //last will message is "Esp32 disconnected"
      client.publish("hoacchitrung_nguyengiahung", "Esp32 connected", "true");
      client.subscribe("rasp4_to_esp32", 1)
      Serial.println("Publish message: Esp32 connected");
      //client.setKeepAlive(1.5);
    } 
    else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 0.5 seconds");
      delay(500);
    }
  }
}

const int btn1 = 9;
const int btn2 = 8;
const int btn3 = 7;
const int btn4 = 6;
const int btn5 = 9;
const int btn6 = 8;
const int btn7 = 7;
const int btn8 = 6;

int buttonState1;
int buttonState2;
int buttonState3;
int buttonState4;
int buttonState5;
int buttonState6;
int buttonState7;
int buttonState8;

int lastButtonState1 = LOW;
int lastButtonState2 = LOW;
int lastButtonState3 = LOW;
int lastButtonState4 = LOW;
int lastButtonState5 = LOW;
int lastButtonState6 = LOW;
int lastButtonState7 = LOW;
int lastButtonState8 = LOW;

unsigned long lastDebounceTime1 = 0;
unsigned long lastDebounceTime2 = 0;
unsigned long lastDebounceTime3 = 0;
unsigned long lastDebounceTime4 = 0;
unsigned long lastDebounceTime5 = 0;
unsigned long lastDebounceTime6 = 0;
unsigned long lastDebounceTime7 = 0;
unsigned long lastDebounceTime8 = 0;
unsigned long debounceDelay = 50;

const int led1 = 9;
const int led2 = 8;
const int led3 = 7;
const int led4 = 6;
const int led5 = 9;
const int led6 = 8;
const int led7 = 7;
const int led8 = 6;

int LedState1 = LOW;
int LedState2 = LOW;
int LedState3 = LOW;
int LedState4 = LOW;
int LedState5 = LOW;
int LedState6 = LOW;
int LedState7 = LOW;
int LedState8 = LOW;

void callback(char* topic, byte* message, unsigned int length) {
  String msg = message;
  LedState1 = int(msg[0])
  LedState2 = int(msg[1])
  LedState3 = int(msg[2])
  LedState4 = int(msg[3])
  LedState5 = int(msg[4])
  LedState6 = int(msg[5])
  LedState7 = int(msg[6])
  LedState8 = int(msg[7])
}

void btn_1() {
  int reading = digitalRead(btn1);

  if (reading != lastButtonState1) {
    lastDebounceTime1 = millis();
  }
  if ((millis() - lastDebounceTime1) > debounceDelay) {
    if (reading != buttonState1) {
      buttonState1 = reading;
      if (buttonState1 == HIGH) {
        LedState1 = !LedState1;
        //code here
      }
    }
  }
  lastButtonState1 = reading;
}

void btn_2() {
  int reading = digitalRead(btn2);

  if (reading != lastButtonState2) {
    lastDebounceTime2 = millis();
  }
  if ((millis() - lastDebounceTime2) > debounceDelay) {
    if (reading != buttonState2) {
      buttonState2 = reading;
      if (buttonState2 == HIGH) {
        LedState2 = !LedState2;
        //code here
      }
    }
  }
  lastButtonState2 = reading;
}

void setup() {
  Serial.begin(115200);
  WiFi.mode(WIFI_STA);
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  setup_wifi()
  
  pinMode(btn1, INPUT_PULLUP);
  pinMode(btn2, INPUT_PULLUP);
  pinMode(btn3, INPUT_PULLUP);
  pinMode(btn4, INPUT_PULLUP);
  pinMode(btn5, INPUT_PULLUP);
  pinMode(btn6, INPUT_PULLUP);
  pinMode(btn7, INPUT_PULLUP);
  pinMode(btn8, INPUT_PULLUP);

  pinMode(led1, OUTPUT);
  pinMode(led2, OUTPUT);
  pinMode(led3, OUTPUT);
  pinMode(led4, OUTPUT);
  pinMode(led5, OUTPUT);
  pinMode(led6, OUTPUT);
  pinMode(led7, OUTPUT);
  pinMode(led8, OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:

}
