import os
from twilio.rest import Client


class NotificationManager:
    # This class is responsible for sending notifications with the deal flight details.
    def __init__(self):
        self.sid = os.getenv("TWILIO_SID")
        self.token = os.getenv("TWILIO_TOKEN")

    def send_notification(self, price, city_from, where, when, how_long):
        client = Client(self.sid, self.token)

        sms = (f"Got {price} on your pocket? Let's head of to {where}! "
               f"Fly from {city_from} to {where} on {when} for {how_long} days 😎")

        message = client.messages.create(
            body=sms,
            from_="+12765944137",
            to="+358505317345"
        )

        print(message.sid)
        # print("Hit the target!!")
        # print(sms)




