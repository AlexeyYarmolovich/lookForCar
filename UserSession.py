import geopy.distance
import asyncio
import datetime


class UserSession:
    def __init__(self, map_info, chat_id, callback):
        self.map_info = map_info
        self.chat_id = chat_id
        self.callback = callback
        self.last_location = None
        self.started = False

    async def set_last_location(self, location):
        self.last_location = location

        if not self.started:
            self.started = True
            await self.start()

    async def start(self):
        if self.last_location is None:
            await self.callback(self.chat_id, 'send me your location please')
        else:
            self.started = True
            await self.start_check_cycle()

    async def start_check_cycle(self):
        print('start_check_cycle begin')
        interval = 30
        distance = 3
        while True:
            cars = self.map_info.get_cars_info()
            await self.find_cars_in_range(self.last_location, distance, cars)
            await asyncio.sleep(interval)

    async def find_cars_in_range(self, user_location, search_range, cars):
        cars_in_range = []
        for car in cars:
            car_position = (car['Lon'], car['Lat'])
            distance = geopy.distance.vincenty(user_location, car_position).km
            if distance < search_range:
                cars_in_range.append({'car': car, 'distance': distance})
        if len(cars_in_range) > 0:
            readable_info = list(map(self.readable_info_for_car, cars_in_range))
            await self.callback(self.chat_id, readable_info)
            print(readable_info)

    def readable_info_for_car(self, car_info):
        distance = car_info['distance']
        car = car_info['car']
        return '{} {} is in {}km'.format(car['Brand'], car['Model'], round(distance, 2))
