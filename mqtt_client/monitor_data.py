from flask import Flask, request
import json
import os

app = Flask(__name__)

def save_to_file(device_id, button_pressed):
    filename = 'button_data.json'
    if not os.path.isfile(filename):
        with open(filename, 'w') as file:
            json.dump({}, file)

    with open(filename, 'r+') as file:
        file_data = json.load(file)
        file_data[device_id] = button_pressed
        file.seek(0)
        json.dump(file_data, file, indent=4)

@app.route('/process', methods=['GET'])
def process():
    device_id = request.args.get('device_id')
    button_pressed = request.args.get('button_pressed')

    save_to_file(device_id, button_pressed)
    
    return "Data Received"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8787)
