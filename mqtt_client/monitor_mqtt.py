import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

# 버튼 상태를 저장할 딕셔너리
button_states = {}

MQTT_SERVER = "127.0.0.1"

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("buttonTopic")

def on_message(client, userdata, msg):
    message = msg.payload.decode()
    print(msg.topic + " " + message)

    # 메시지에서 MAC 주소와 버튼 상태 추출
    mac_address, button_status = message.split(' ', 1)
    
    # 특정 조건에 따른 LED 제어 메시지 전송
    if button_status == "Button 1 Pressed":
        publish.single(mac_address, "1", hostname=MQTT_SERVER, auth={'username':"jyyang", 'password':"didwhdduf"})
        print(f"publish {mac_address} 1")
    elif button_status == "Button 2 Pressed":
        publish.single(mac_address, "2", hostname=MQTT_SERVER, auth={'username':"jyyang", 'password':"didwhdduf"})
        print(f"publish {mac_address} 2")

    # 버튼 상태 업데이트
    button_states[mac_address] = button_status
    print(f"Current state of {mac_address}: {button_status}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# 사용자 이름과 비밀번호 설정
client.username_pw_set("jyyang", "didwhdduf")

client.connect("127.0.0.1", 1883, 60)
client.loop_forever()
