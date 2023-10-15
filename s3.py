import os
import serial
from kivy.core.audio import SoundLoader
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.relativelayout import RelativeLayout
from kivy.utils import get_color_from_hex
import time
import threading

# Initialize the Kivy application
ser = serial.Serial('COM6', 9600)  # Replace 'COM6' with the correct serial port

# Variable to control the sound thread
sound_thread_running = False

def sound(choice):
    global sound_thread_running

    if choice == 1:
        # Start the sound thread
        sound_thread_running = True
        sound_thread = threading.Thread(target=sound_thread_function)
        sound_thread.start()
    else:
        # Stop the sound thread
        sound_thread_running = False

def sound_thread_function():
    while sound_thread_running:
        data = ser.readline().decode().strip()
        if ":" in data:
            prefix, value = data.split(":", 1)  # Split the data into prefix and value
            if prefix == "D":
                try:
                    distance = int(value)  # Extract the distance value
                    print(f"Distance: {distance} cm")

                    # Play a sound based on the distance
                    if distance < 10:
                        play_sound(r"C:\Users\HP\Downloads\veryclose.mp3")
                    elif 10 <= distance < 30:
                        play_sound(r"C:\Users\HP\Downloads\close.mp3")
                    elif 30 <= distance < 50:
                        play_sound(r"C:\Users\HP\Downloads\moderate.mp3")
                    #elif distance >= 50:
                        #play_sound("far.mp3")
                except ValueError:
                    print("Invalid distance value received.")
            elif prefix == "Obstacle Detected":
                print("Obstacle detected!")
                play_sound(r"C:\Users\HP\Downloads\obstacle.mp3")
            else:
                print(f"{prefix}")
        else:
            print("obstacle not found")

def play_sound(sound_file):
    sound_file_path = os.path.join("sounds", sound_file)
    sound = SoundLoader.load(sound_file_path)
    if sound:
        sound.play()
        time.sleep(5)
    else:
        print(f"Failed to load sound file: {sound_file_path}")

class MyApp(App):
    def build(self):
        # Create a RelativeLayout
        layout = RelativeLayout()

        # Play the instructions audio message
        play_sound(r"C:\Users\HP\Downloads\instruct.mp3")
        # Create a "Start" button with a pink background color
        start_button = Button(text='Start', size_hint=(1, 0.5), pos_hint={'top': 1})
        start_button.bind(on_press=self.start_action)
        start_button.background_color = get_color_from_hex('#FF69B4')  # Pink color

        # Create a "Stop" button with a blue background color
        stop_button = Button(text='Stop', size_hint=(1, 0.5), pos_hint={'bottom': 0})
        stop_button.bind(on_press=self.stop_action)
        stop_button.background_color = get_color_from_hex('#0000FF')  # Blue color

        # Add buttons to the layout
        layout.add_widget(start_button)
        layout.add_widget(stop_button)

        return layout

    def start_action(self, instance):
        # Define the action when the "Start" button is pressed
        print('Start button pressed')
        sound(1)

    def stop_action(self, instance):
        # Define the action when the "Stop" button is pressed
        print('Stop button pressed')
        sound(0)

if __name__ == '__main__':
    # MyApp is initialized and its run() method called
    MyApp().run()
