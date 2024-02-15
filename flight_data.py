import requests
import os
from data_manager import DataManager
from datetime import datetime, timedelta
from notification_manager import NotificationManager


class FlightData:
    def __init__(self, dest_data: DataManager):
        self.time = datetime.now().today()
        self.manager = dest_data
        self.destinations = dest_data.data
        self.notifier = NotificationManager()
        self.location_url = "https://api.tequila.kiwi.com/locations/query?"
        self.search_url = "https://api.tequila.kiwi.com/v2/search"
        self.header = {
            "apikey": os.getenv("KIWI_KEY")
        }

    def update_destinations(self):
        self.manager.connect()
        self.destinations = self.manager.data

    def update_iatas(self):
        for dest in self.destinations:
            if dest["iataCode"] == "":
                kiwi_get_params = {
                    "term": dest["city"],
                    "limit": 1
                }
                connection = requests.get(url=self.location_url, params=kiwi_get_params, headers=self.header)
                flight_data = connection.json()
                new_data = {
                    "price": {
                        "iataCode": flight_data["locations"][0]["code"]
                    }
                }
                object_id = dest["id"]
                self.manager.update(new_data, object_id)
                self.update_destinations()

    def flight_search(self, dest, dest_price):
        try:
            kiwi_search_params = {"fly_from": "HEL", "fly_to": dest["iataCode"],
                                  "date_from": self.time.strftime("%d/%m/%Y"),
                                  "date_to": (self.time + timedelta(days=180)).strftime("%d/%m/%Y"),
                                  "nights_in_dst_from": 7, "nights_in_dst_to": 28, "curr": "EUR", "one_for_city": 1,
                                  "max-stepovers": 0, "limit": 2}
            connection = requests.get(url=self.search_url, params=kiwi_search_params, headers=self.header)
            print(connection.status_code)
            flight_data = connection.json()["data"][0]
        except ConnectionError:
            print("Connection Error")
        except IndexError:
            print("No flights to destinations.")
        else:
            if dest_price >= flight_data["price"]:
                departure_date = flight_data["route"][0]["local_departure"].split("T")[0]
                departure_time = flight_data["route"][0]["local_departure"].split("T")[1].split(".")[0]
                trip = self.notifier.send_notification(price=flight_data["price"],
                                                       city_from=flight_data["cityFrom"],
                                                       where=flight_data["cityTo"],
                                                       when=f"{departure_date} at {departure_time}",
                                                       how_long=flight_data["nightsInDest"])
                return trip

    def notify_next_trip(self):
        for dest in self.destinations:
            self.flight_search(dest, dest["lowestPrice"])
