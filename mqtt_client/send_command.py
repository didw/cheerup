# mqtt_client/send_command.py
import paho.mqtt.publish as publish

MQTT_SERVER = "127.0.0.1"
MQTT_PORT = 1883

def send_command_to_device(mac_address, command):
    publish.single(mac_address, command, hostname=MQTT_SERVER, port=MQTT_PORT, auth={'username':"jyyang", 'password':"didwhdduf"})
    print(f"Command {command} sent to {mac_address}")


def test_send_command_to_device():
    send_command_to_device("68:C6:3A:DD:75:05", "1")


if __name__ == "__main__":
    test_send_command_to_device()
