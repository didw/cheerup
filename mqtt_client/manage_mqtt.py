import paho.mqtt.client as mqtt
import time

# MQTT 클라이언트 인스턴스 생성
client = mqtt.Client()

# MQTT 브로커에 연결
client.connect("127.0.0.1", 1883, 60)

def publish(topic, payload):
    client.publish(topic, payload)

if __name__ == "__main__":
    while True:
        # 조건에 따라 메시지를 전송하거나 사용자 입력을 받아 메시지를 전송
        message = input("Enter message to publish: ")
        print(f"Publishing message: {message}")
        publish("buttonStatus", message)
        time.sleep(1)  # 루프 사이에 간단한 딜레이를 주어 메시지 입력 가능
