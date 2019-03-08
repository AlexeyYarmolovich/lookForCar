import requests
import datetime


class MapTracker:
    def __init__(self):
        self._cars_info = None
        self._last_load_date = None

        self.load_cars_info()


    def load_cars_info(self):
        #print("started loading cars info", datetime.datetime.now())
        self._cars_info = requests.get('http://service.drivetime.by/api/cars').json()['cars']
        vesuha_cars = requests.get('https://service.vezuha.club/api/cars').json()['cars']
        self._cars_info.extend(vesuha_cars)
        self._last_load_date = datetime.datetime.now()
        #print("finished loading cars info", datetime.datetime.now())


    def get_cars_info(self):
        #print("cars info requested", datetime.datetime.now())
        passed_interval = datetime.datetime.now() - self._last_load_date
        if passed_interval.seconds > 30:
            self.load_cars_info()
        #print("cars info will be returned", datetime.datetime.now())
        return self._cars_info