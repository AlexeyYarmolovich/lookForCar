import requests
import datetime


class MapTracker:
    def __init__(self):
        self._cars_info = None
        self._last_load_date = None

        self.load_cars_info()


    def load_cars_info(self):
        print("started loading cars info")
        self._cars_info = requests.get('http://service.drivetime.by/api/cars').json()['cars']
        self._last_load_date = datetime.datetime.now()
        print("finished loading cars info")


    def get_cars_info(self):
        passed_interval = datetime.datetime.now() - self._last_load_date
        if passed_interval.seconds  > 60:
            self.load_cars_info()
        return self._cars_info