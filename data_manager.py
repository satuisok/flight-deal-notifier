import requests
import os
from dotenv import load_dotenv
from pprint import pprint

load_dotenv()


class DataManager:
    def __init__(self):
        self.url = "https://api.sheety.co/f9159d5548706cc52f9f2cc1418403a9/flightDeals/prices"
        self.header = {"Authorization": f"Bearer {os.getenv("SHEETY_TOKEN")}"}
        self.data = []
        self.connect()

    def connect(self):
        sheety_connect = requests.get(url=self.url, headers=self.header)
        sheety_connect.raise_for_status()
        sheety_data = sheety_connect.json()
        self.data = sheety_data["prices"]
        return self.data

    def update(self, whats_new, object_id):
        connection = requests.put(url=f"{self.url}/{object_id}", json=whats_new, headers=self.header)
        print(connection.text)
