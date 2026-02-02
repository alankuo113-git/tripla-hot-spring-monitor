from playwright.sync_api import sync_playwright
import smtplib
from email.message import EmailMessage
import requests
import os

# =========================
# CONFIG
# =========================

BOOKING_URL = (
    "https://bw.tripla.ai/booking/result"
    "?code=2e3b7560ba862e0c2aee8924912b97ae"
    "&checkin=2026/02/13"
    "&checkout=2026/02/14"
    "&type=room"
    "&is_day_use=false"
    "&order=price_high_to_low"
    "&is_including_occupied=false"
    "&adults=2"
    "&kids_tiers=%5B%5D"
    "&room_count=1"
    "&mcp_currency=TWD"
)

KEYWORDS = [
    "with hot spring"
]

# =========================
# EMAIL ALERT
# =========================
def send_email():
    msg = EmailMessage()
    msg["Subject"] = "🔥 HOT SPRING ROOM AVAILABLE ACT NOW"
    msg["From"] = os.environ["EMAIL_FROM"]
    msg["To"] = os.environ["EMAIL_TO"]
    msg.set_content("HOT SPRING ROOM AVAILABLE ACT NOW")

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(
            os.environ["EMAIL_FROM"],
            os.environ["EMAIL_PASSWORD"]
        )
        server.send_message(msg)

# =========================
# LINE ALERT
# =========================
def send_line():
    requests.post(
        "https://notify-api.line.me/api/notify",
        headers={
            "Authorization": f"Bearer {os.environ['LINE_NOTIFY_TOKEN']}"
        },
        data={"message": "🔥 HOT SPRING ROOM AVAILABLE ACT NOW"}
    )

# =========================
# MAIN AGENT
# =========================
def run_agent():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(BOOKING_URL, timeout=60000)

        # Give Tripla time to fully render results
        page.wait_for_timeout(10000)

        text = page.inner_text("body").lower()

        if any(keyword in text for keyword in KEYWORDS):
            send_email()
            
        browser.close()

# =========================
# RUN
# =========================
if __name__ == "__main__":
    run_agent()
