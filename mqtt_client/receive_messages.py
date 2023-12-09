import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import pymysql

MQTT_SERVER = "127.0.0.1"
DB_HOST = '127.0.0.1'
DB_USER = 'jyyang'
DB_PASSWORD = 'didwhdduf'
DB_DATABASE = 'QuizSystemDB'

def get_current_question_id():
    # 현재 진행중인 퀴즈 문제의 ID를 가져오는 함수
    connection = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_DATABASE)
    try:
        with connection.cursor() as cursor:
            sql = "SELECT QuestionID FROM QuizQuestions WHERE IsActive = 1"
            cursor.execute(sql)
            result = cursor.fetchone()
            return result[0] if result else None
    finally:
        connection.close()

def create_db_connection():
    return pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_DATABASE)

def update_device_status(mac_address, device_status):
    with create_db_connection() as connection:
        with connection.cursor() as cursor:
            sql = "INSERT INTO Devices (DeviceID, Status) VALUES (%s, %s) ON DUPLICATE KEY UPDATE Status=%s"
            cursor.execute(sql, (mac_address, device_status, device_status))
            connection.commit()

def store_quiz_response(mac_address, device_status):
    current_question_id = get_current_question_id()
    if current_question_id:
        with create_db_connection() as connection:
            with connection.cursor() as cursor:
                sql = "INSERT INTO QuizResponses (DeviceID, QuestionID, SelectedAnswer) VALUES (%s, %s, %s)"
                selected_answer = 'O' if device_status == "Button 1 Pressed" else 'X'
                cursor.execute(sql, (mac_address, current_question_id, selected_answer))
                connection.commit()

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("buttonTopic")

def on_message(client, userdata, msg):
    message = msg.payload.decode()
    print(msg.topic + " " + message)

    mac_address, device_status = message.split(' ', 1)
    mac_address = mac_address.strip()

    try:
        if device_status == "Connected":
            print(f"Device {mac_address} connected.")
            update_device_status(mac_address, device_status)
        elif device_status in ["Button 1 Pressed", "Button 2 Pressed"]:
            store_quiz_response(mac_address, device_status)
            update_device_status(mac_address, device_status)
    except Exception as e:
        print(f"Error: {e}")

    print(f"Device {mac_address} status updated to {device_status}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# 사용자 이름과 비밀번호 설정
client.username_pw_set("jyyang", "didwhdduf")

client.connect("127.0.0.1", 1883, 60)
client.loop_forever()
