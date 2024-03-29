#include <ESP8266WiFi.h>
#include <PubSubClient.h>

// WiFi 설정
const char* ssid = "AndroidHotspot7896";
const char* password = "22222222";

// MQTT 서버 설정
const char* mqtt_server = "52.79.239.104";

WiFiClient espClient;
PubSubClient client(espClient);

// 버튼 핀 설정
const int buttonPin1 = 5;
const int buttonPin2 = 4;

// LED 핀 설정
const int ledPin1 = 13;
const int ledPin2 = 15;

// 디바운싱에 필요한 변수들
unsigned long lastDebounceTime1 = 0;  
unsigned long lastDebounceTime2 = 0;  
unsigned long debounceDelay = 50;    
bool lastButtonState1 = LOW; 
bool lastButtonState2 = LOW;
bool stableButtonState1 = LOW;
bool stableButtonState2 = LOW;

String clientId;

// Function to strip characters from a string
String rstrip(String str) {
  if (str.length() == 0) return str;

  int i = str.length() - 1;
  while (i >= 0 && (str[i] == ' ' || str[i] == '\t' || str[i] == '\n' || str[i] == '\r')) {
    i--;
  }
  return str.substring(0, i + 1);
}

void setup_wifi() {
  delay(10);
  Serial.println("Connecting to WiFi...");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

  clientId = WiFi.macAddress();
  clientId = rstrip(clientId); // Strip the clientId
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Use the clientId in the connect call
    if (client.connect(clientId.c_str(), "jyyang", "didwhdduf")) {
      Serial.println("connected");

      // MQTT 연결 성공 시 수행할 작업
      String connectMessage = clientId + " Connected";
      client.publish("buttonTopic", connectMessage.c_str());

      client.subscribe(clientId.c_str());
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}
void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }
  Serial.println();

  // 클라이언트의 고유 토픽 확인
  if (String(topic) == clientId) {
    if ((char)payload[0] == '1') {
      blinkLed(ledPin1, 3);
    } else if ((char)payload[0] == '2') {
      blinkLed(ledPin2, 3);
    }
  }
}

void blinkLed(int ledPin, int times) {
  for (int i = 0; i < times; i++) {
    digitalWrite(ledPin, HIGH);
    delay(250);
    digitalWrite(ledPin, LOW);
    delay(250);
  }
}

void setup() {
  Serial.begin(9600);
  pinMode(buttonPin1, INPUT_PULLUP);
  pinMode(buttonPin2, INPUT_PULLUP);
  pinMode(ledPin1, OUTPUT);
  pinMode(ledPin2, OUTPUT);
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);

  // Initialize the button states based on the current readings
  stableButtonState1 = digitalRead(buttonPin1);
  stableButtonState2 = digitalRead(buttonPin2);
  lastButtonState1 = stableButtonState1;
  lastButtonState2 = stableButtonState2;
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  bool reading1 = digitalRead(buttonPin1);
  bool reading2 = digitalRead(buttonPin2);

  // LED 제어
  digitalWrite(ledPin1, !reading1); // 버튼 1 상태에 따라 LED 1 제어
  digitalWrite(ledPin2, !reading2); // 버튼 2 상태에 따라 LED 2 제어

  if (reading1 != lastButtonState1) {
    lastDebounceTime1 = millis();
  }

  if (reading2 != lastButtonState2) {
    lastDebounceTime2 = millis();
  }

  if ((millis() - lastDebounceTime1) > debounceDelay) {
    if (reading1 != stableButtonState1) {
      stableButtonState1 = reading1;
      if (stableButtonState1 == HIGH) {
        Serial.println("Button 1 Pressed");
        String message = clientId + " Button 1 Pressed";
        client.publish("buttonTopic", message.c_str());
      }
    }
  }

  if ((millis() - lastDebounceTime2) > debounceDelay) {
    if (reading2 != stableButtonState2) {
      stableButtonState2 = reading2;
      if (stableButtonState2 == HIGH) {
        Serial.println("Button 2 Pressed");
        String message = clientId + " Button 2 Pressed";
        client.publish("buttonTopic", message.c_str());
      }
    }
  }

  lastButtonState1 = reading1;
  lastButtonState2 = reading2;
}

