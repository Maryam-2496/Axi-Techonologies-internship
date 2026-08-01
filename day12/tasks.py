import time
import random

def send_welcome_email(email, name):
    print(f"Starting background task: sending welcome email to {email}...")
    time.sleep(1)

    if random.random() < 0.2:
        print(f"Simulated failure sending email to {email}!")
        raise Exception("Simulated SMTP failure")

    print(f"Welcome email sent to {name} ({email})!")
    return f"Email sent to {email}"