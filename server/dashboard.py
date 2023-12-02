import streamlit as st
import json
import time

def read_from_file():
    with open('button_data.json', 'r') as file:
        return json.load(file)

def display_dashboard(data, placeholders):
    for device_id, button_pressed in data.items():
        placeholders[device_id].markdown(f"Device ID: {device_id}, Last Button Pressed: {button_pressed}")

def main():
    st.title('Button Press Dashboard')
    data = read_from_file()
    
    # Create placeholders for each device
    placeholders = {device_id: st.empty() for device_id in data}

    # Update dashboard in a loop
    while True:
        data = read_from_file()
        display_dashboard(data, placeholders)
        time.sleep(1)  # Refresh every 1 second

if __name__ == "__main__":
    main()
