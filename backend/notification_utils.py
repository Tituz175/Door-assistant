import os
from twilio.rest import Client
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

account_sid = os.getenv("account_sid")
auth_token = os.getenv("auth_token")

client = Client(account_sid, auth_token)


def send_notification():
    now = datetime.now()
    formatted_now = now.strftime("%d/%m/%y %H:%M:%S")
    message = client.messages.create(
        from_='whatsapp:+14155238886',
        body=f"Person motion detected @{formatted_now}",
        to='whatsapp:+2348182789715'
    )

    print(message.sid)


if __name__ == "__main__":
    pass
