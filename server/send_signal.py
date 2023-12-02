import time
import paho.mqtt.publish as publish

# MQTT 서버 주소 및 포트 설정
MQTT_SERVER = "127.0.0.1"
MQTT_PORT = 1883

# 특정 장비에 대한 명령 전송
target_mac = "68:C6:3A:DD:75:05"
command = "1"  # LED 1을 깜빡이라는 명령

publish.single(target_mac, command, hostname=MQTT_SERVER, port=MQTT_PORT, auth={'username':"jyyang", 'password':"didwhdduf"})

time.sleep(5)
command = "2"  # LED 1을 깜빡이라는 명령
publish.single(target_mac, command, hostname=MQTT_SERVER, port=MQTT_PORT, auth={'username':"jyyang", 'password':"didwhdduf"})
