
import sys
import os

print("Starting test script...")

# Add current directory to path so we can import backend
sys.path.append(os.getcwd())

from backend.main import send_email

def test_email_logic():
    print("Testing Low Risk (< 40%)...")
    # Sending to self to verify
    send_email("cardiacattackpredictor@gmail.com", 0.20)
    print("Email sent to cardiacattackpredictor@gmail.com")
    print("-" * 20)

    # print("Testing Medium Risk (40% - 70%)...")
    # send_email("test_med@example.com", 0.55)
    # print("-" * 20)

    # print("Testing High Risk (> 70%)...")
    # send_email("test_high@example.com", 0.85)
    # print("-" * 20)

if __name__ == "__main__":
    test_email_logic()
