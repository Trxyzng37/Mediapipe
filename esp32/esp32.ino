#include <WiFi.h>       //include wifi library       
#include <PubSubClient.h>  //include mqtt library


const char* ssid = "TTT";                //wifi name
const char* password = "10032001";        //wifi password

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
    if (client.connect("ESP32_hoacchitrung_nguyengiahung", NULL, NULL, "esp32_status", 2, true, "Esp32 disconnected", false)) {  //clientID, user, pass, willtopic, willqos, willretain, willmessage, clean session
      Serial.println("Connected to mqtt broker");                                                   //last will message is "Esp32 disconnected"
      client.publish("esp32_status", "Esp32 connected", "true");
      client.subscribe("rasp4_to_esp32", 1);
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

const int btn1 = 15;
const int btn2 = 13;
const int btn3 = 12;
const int btn4 = 14;
const int btn5 = 16;
const int btn6 = 32;
const int btn7 = 33;
const int btn8 = 27;
const int btn9 = 26;

int buttonState1;
int buttonState2;
int buttonState3;
int buttonState4;
int buttonState5;
int buttonState6;
int buttonState7;
int buttonState8;
int buttonState9;

int lastButtonState1 = HIGH;
int lastButtonState2 = HIGH;
int lastButtonState3 = HIGH;
int lastButtonState4 = HIGH;
int lastButtonState5 = HIGH;
int lastButtonState6 = HIGH;
int lastButtonState7 = HIGH;
int lastButtonState8 = HIGH;
int lastButtonState9 = HIGH;

unsigned long lastDebounceTime1 = 0;
unsigned long lastDebounceTime2 = 0;
unsigned long lastDebounceTime3 = 0;
unsigned long lastDebounceTime4 = 0;
unsigned long lastDebounceTime5 = 0;
unsigned long lastDebounceTime6 = 0;
unsigned long lastDebounceTime7 = 0;
unsigned long lastDebounceTime8 = 0;
unsigned long lastDebounceTime9 = 0;

unsigned long debounceDelay = 50;

const int led1 = 17;
const int led2 = 25;
const int led3 = 5;
const int led4 = 18;
const int led5 = 19;
const int led6 = 21;
const int led7 = 22;
const int led8 = 23;

int LedState1 = LOW;
int LedState2 = LOW;
int LedState3 = LOW;
int LedState4 = LOW;
int LedState5 = LOW;
int LedState6 = LOW;
int LedState7 = LOW;
int LedState8 = LOW;

void callback(char* topic, byte* payload, unsigned int length) {
  String msg;
  for (int i = 0; i < length; i++) {
    msg += (char)payload[i];
  };
  Serial.print("\nReceive: \n");
  Serial.print(msg);
  if ((char)payload[0] == '1') {
    LedState1 = HIGH;
    digitalWrite(led1, LedState1);
  }
  else {
    LedState1 = LOW;
    digitalWrite(led1, LedState1);
  }
  
  if ((char)payload[1] == '1') {
    LedState2 = HIGH;
    digitalWrite(led2, LedState2);
  }
  else {
    LedState2 = LOW;
    digitalWrite(led2, LedState2);
    
  }
  
  if ((char)payload[2] == '1') {
    LedState3 = HIGH;
    digitalWrite(led3, LedState3);
  }
  else {
    LedState3 = LOW;
    digitalWrite(led3, LedState3);
  }
  
  if ((char)payload[3] == '1') {
    LedState4 = HIGH;
    digitalWrite(led4, LedState4);
  }
  else {
    LedState4 = LOW;
    digitalWrite(led4, LedState4);
  }
  
  if ((char)payload[4] == '1') {
    LedState5 = HIGH;
    digitalWrite(led5, LedState5);
  }
  else {
    LedState5 = LOW;
    digitalWrite(led5, LedState5);
  }
  
  if ((char)payload[5] == '1') {
    LedState6 = HIGH;
    digitalWrite(led6, LedState6);
  }
  else {
    LedState6 = LOW;
    digitalWrite(led6, LedState6);
  }

  if ((char)payload[6] == '1') {
    LedState7 = HIGH;
    digitalWrite(led7, LedState7);
  }
  else {
    LedState7 = LOW;
    digitalWrite(led7, LedState7);
  }

  if ((char)payload[7] == '1') {
    LedState8 = HIGH;
    digitalWrite(led8, LedState8);
  }
  else {
    LedState8 = LOW;
    digitalWrite(led8, LedState8);
  }
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
        String all_state = String(LedState1)+String(LedState2)+String(LedState3)+String(LedState4)+String(LedState5)+String(LedState6)+String(LedState7)+String(LedState8);
        client.publish("esp32_to_rasp4", all_state.c_str());
        Serial.print("\nPublish 1: \n");
        Serial.print(all_state.c_str());
        digitalWrite(led1, LedState1);
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
        String all_state = String(LedState1)+String(LedState2)+String(LedState3)+String(LedState4)+String(LedState5)+String(LedState6)+String(LedState7)+String(LedState8);
        client.publish("esp32_to_rasp4", all_state.c_str());
        Serial.print("\nPublish 2: \n");
        Serial.print(all_state.c_str());
        digitalWrite(led2, LedState2);
        //code here
      }
    }
  }
  lastButtonState2 = reading;
}

void btn_3() {
  int reading = digitalRead(btn3);

  if (reading != lastButtonState3) {
    lastDebounceTime3 = millis();
  }
  if ((millis() - lastDebounceTime3) > debounceDelay) {
    if (reading != buttonState3) {
      buttonState3 = reading;
      if (buttonState3 == HIGH) {
        LedState3 = !LedState3;
        String all_state = String(LedState1)+String(LedState2)+String(LedState3)+String(LedState4)+String(LedState5)+String(LedState6)+String(LedState7)+String(LedState8);
        client.publish("esp32_to_rasp4", all_state.c_str());
        Serial.print("\nPublish 3: \n");
        Serial.print(all_state.c_str());
        digitalWrite(led3, LedState3);
        //code here
      }
    }
  }
  lastButtonState3 = reading;
}

void btn_4() {
  int reading = digitalRead(btn4);

  if (reading != lastButtonState4) {
    lastDebounceTime4 = millis();
  }
  if ((millis() - lastDebounceTime4) > debounceDelay) {
    if (reading != buttonState4) {
      buttonState4 = reading;
      if (buttonState4 == HIGH) {
        LedState4 = !LedState4;
        String all_state = String(LedState1)+String(LedState2)+String(LedState3)+String(LedState4)+String(LedState5)+String(LedState6)+String(LedState7)+String(LedState8);
        client.publish("esp32_to_rasp4", all_state.c_str());
        Serial.print("\nPublish 4: \n");
        Serial.print(all_state.c_str());
        digitalWrite(led4, LedState4);
        //code here
      }
    }
  }
  lastButtonState4 = reading;
}

void btn_5() {
  int reading = digitalRead(btn5);

  if (reading != lastButtonState5) {
    lastDebounceTime5 = millis();
  }
  if ((millis() - lastDebounceTime5) > debounceDelay) {
    if (reading != buttonState5) {
      buttonState5 = reading;
      if (buttonState5 == HIGH) {
        LedState5 = !LedState5;
        String all_state = String(LedState1)+String(LedState2)+String(LedState3)+String(LedState4)+String(LedState5)+String(LedState6)+String(LedState7)+String(LedState8);
        client.publish("esp32_to_rasp4", all_state.c_str());
        Serial.print("\nPublish 5: \n");
        Serial.print(all_state.c_str());
        digitalWrite(led5, LedState5);
        //code here
      }
    }
  }
  lastButtonState5 = reading;
}

void btn_6() {
  int reading = digitalRead(btn6);

  if (reading != lastButtonState6) {
    lastDebounceTime6 = millis();
  }
  if ((millis() - lastDebounceTime6) > debounceDelay) {
    if (reading != buttonState6) {
      buttonState6 = reading;
      if (buttonState6 == HIGH) {
        LedState6 = !LedState6;
        String all_state = String(LedState1)+String(LedState2)+String(LedState3)+String(LedState4)+String(LedState5)+String(LedState6)+String(LedState7)+String(LedState8);
        client.publish("esp32_to_rasp4", all_state.c_str());
        Serial.print("\nPublish 6: \n");
        Serial.print(all_state.c_str());
        digitalWrite(led6, LedState6);
        //code here
      }
    }
  }
  lastButtonState6 = reading;
}

void btn_7() {
  int reading = digitalRead(btn7);

  if (reading != lastButtonState7) {
    lastDebounceTime7 = millis();
  }
  if ((millis() - lastDebounceTime7) > debounceDelay) {
    if (reading != buttonState7) {
      buttonState7 = reading;
      if (buttonState7 == HIGH) {
        LedState7 = !LedState7;
        String all_state = String(LedState1)+String(LedState2)+String(LedState3)+String(LedState4)+String(LedState5)+String(LedState6)+String(LedState7)+String(LedState8);
        client.publish("esp32_to_rasp4", all_state.c_str());
        Serial.print("\nPublish 7: \n");
        Serial.print(all_state.c_str());
        digitalWrite(led7, LedState7);
        //code here
      }
    }
  }
  lastButtonState7 = reading;
}

void btn_8() {
  int reading = digitalRead(btn8);

  if (reading != lastButtonState8) {
    lastDebounceTime8 = millis();
  }
  if ((millis() - lastDebounceTime8) > debounceDelay) {
    if (reading != buttonState8) {
      buttonState8 = reading;
      if (buttonState8 == HIGH) {
        LedState8 = !LedState8;
        String all_state = String(LedState1)+String(LedState2)+String(LedState3)+String(LedState4)+String(LedState5)+String(LedState6)+String(LedState7)+String(LedState8);
        client.publish("esp32_to_rasp4", all_state.c_str());
        Serial.print("\nPublish 8: \n");
        Serial.print(all_state.c_str());
        digitalWrite(led8, LedState8);
        //code here
      }
    }
  }
  lastButtonState8 = reading;
}

void btn_9() {
  int reading = digitalRead(btn9);

  if (reading != lastButtonState9) {
    lastDebounceTime9 = millis();
  }
  if ((millis() - lastDebounceTime9) > debounceDelay) {
    if (reading != buttonState9) {
      buttonState9 = reading;
      if (buttonState9 == HIGH) {
        client.publish("esp32_to_rasp4", "0");
        Serial.print("\nTurn off hand gesture mode\n");
        //code here
      }
    }
  }
  lastButtonState9 = reading;
}

long lastReconnectAttempt = 0;

//reconnect
boolean reconnect() {
  if (client.connect("esp32_rasp4")) {
    // Once connected, publish an announcement...
    client.publish("esp32_status","esp32 connected");
    // ... and resubscribe
    client.subscribe("rasp4_to_esp32", 1);
  }
  return client.connected();
}

int count = 0;
void setup() {
  count = 0;
  Serial.begin(115200);
  WiFi.mode(WIFI_STA);
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  setup_mqtt();
  client.subscribe("rasp4_to_esp32",1);
  client.setCallback(callback);
  lastReconnectAttempt = 0;
  pinMode(btn1, INPUT_PULLUP);
  pinMode(btn2, INPUT_PULLUP);
  pinMode(btn3, INPUT_PULLUP);
  pinMode(btn4, INPUT_PULLUP);
  pinMode(btn5, INPUT_PULLUP);
  pinMode(btn6, INPUT_PULLUP);
  pinMode(btn7, INPUT_PULLUP);
  pinMode(btn8, INPUT_PULLUP);
  pinMode(btn9, INPUT_PULLUP);
  
  pinMode(led1, OUTPUT);
  pinMode(led2, OUTPUT);
  pinMode(led3, OUTPUT);
  pinMode(led4, OUTPUT);
  pinMode(led5, OUTPUT);
  pinMode(led6, OUTPUT);
  pinMode(led7, OUTPUT);
  pinMode(led8, OUTPUT);

  digitalWrite(led1, LOW);
  digitalWrite(led2, LOW);
  digitalWrite(led3, LOW);
  digitalWrite(led4, LOW);
  digitalWrite(led5, LOW);
  digitalWrite(led6, LOW);
  digitalWrite(led7, LOW);
  digitalWrite(led8, LOW);
}

void loop() 
{
  if (!client.connected()) {
    long now = millis();
    if (now - lastReconnectAttempt > 1000) {
      lastReconnectAttempt = now;
      // Attempt to reconnect
      if (reconnect()) {
        lastReconnectAttempt = 0;
      }
    }
  } else {
    btn_1();
    btn_2();
    btn_3();
    btn_4();
    btn_5();
    btn_6();
    btn_7();
    btn_8();
    btn_9();
    client.loop();
  }
}
