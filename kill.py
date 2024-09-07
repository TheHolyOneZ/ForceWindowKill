import pygetwindow as gw
import pyautogui
from pynput import keyboard
import threading

# Variable to store the close key
close_key = None
stop_flag = False  # Flag to stop the script

# Function to get the close key from the user
def set_close_key():
    global close_key
    print("Press the key you want to use to close the window:")

    # Listener for keyboard input
    def on_press(key):
        global close_key
        try:
            close_key = key.char  # Store the pressed key
        except AttributeError:
            close_key = key.name  # For special keys like 'shift', 'ctrl', etc.
        print(f"Close key set to: {close_key}")
        return False  # Stop the listener after getting input

    # Start the keyboard listener
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

# Function to get the window under the cursor
def get_window_under_cursor():
    x, y = pyautogui.position()
    for window in gw.getAllWindows():
        if window.left <= x <= window.right and window.top <= y <= window.bottom:
            return window
    return None

# Function to monitor the key input
def monitor_key():
    def on_press(key):
        global stop_flag
        if key == keyboard.Key.esc:  # Stop the program
            stop_flag = True
            print("Program terminated.")
            return False  # Stop the listener

        if hasattr(key, 'char') and key.char == close_key:
            window = get_window_under_cursor()  # Get the current window
            if window:
                print(f"Closing window: {window.title}")
                window.close()  # Close the window

    # Start the keyboard listener for the set close key
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

def main():
    set_close_key()  # Ask for the close key first
    print("Press the assigned key to close windows. (Press ESC to exit)")

    # Start the key monitoring in a separate thread
    while not stop_flag:
        key_thread = threading.Thread(target=monitor_key)
        key_thread.start()
        key_thread.join()  # Wait for the thread to finish

if __name__ == "__main__":
    main()
