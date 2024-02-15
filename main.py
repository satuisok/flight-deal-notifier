# This file will need to use the DataManager,FlightSearch, FlightData,
# NotificationManager classes to achieve the program requirements.

from dotenv import load_dotenv
load_dotenv()
from data_manager import DataManager
from flight_data import FlightData

sheet_data = DataManager()
flights = FlightData(sheet_data)
flights.notify_next_trip()
