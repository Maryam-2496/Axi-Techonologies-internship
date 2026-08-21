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


def slow_operation(label="task"):
    """Simulates a heavy operation like PDF generation or image processing."""
    time.sleep(3)
    return f"{label} completed"

_processed_orders = set()

def generate_invoice(order_id, customer_email):
    if order_id in _processed_orders:
        print(f"Invoice for order {order_id} already generated — skipping duplicate")
        return f"Invoice for order {order_id} already exists (skipped)"
    import time
    time.sleep(2)
    _processed_orders.add(order_id)
    print(f"Invoice generated for order {order_id}, sent to {customer_email}")
    return f"Invoice for order {order_id} generated"

def flaky_invoice(order_id):
    """Always fails — used to test DLQ routing."""
    raise Exception("Simulated invoice generation failure")