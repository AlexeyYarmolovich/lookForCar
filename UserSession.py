import geopy.distance
import asyncio


class UserSession:
    def __init__(self, map_info, chat_id, callback):
        self.map_info = map_info
        self.chat_id = chat_id
        self.send_message_callback = callback
        self.last_location = None
        self.started = False

    async def set_last_location(self, location):
        self.last_location = location

        if not self.started:
            self.started = True
            await self.start()

    async def start(self):
        if self.last_location is None:
            await self.send_message_callback(self.chat_id, 'send me your location please')
        else:
            self.started = True
            await self.start_check_cycle()

    def stop(self):
        self.started = False

    async def start_check_cycle(self):
        print('start_check_cycle begin')
        interval = 15
        distance = 1.5
        known_cars = set()
        while self.started:
            cars = self.map_info.get_cars_info()
            found_cars = self.find_cars_in_range(self.last_location, distance, cars)
            print('found cars in range: ', found_cars)
            # look for cars that weren't found before
            new_cars = found_cars.difference(known_cars)
            print('new cars: ', new_cars)

            # look for cars that were found but are not visible now
            dismissed_cars = known_cars.difference(found_cars)
            print('dismissed cars: ', len(dismissed_cars))
            known_cars.update(new_cars)
            known_cars.difference_update(dismissed_cars)

            if len(new_cars) > 0:
                new_cars_info = self.get_readable_info_for_cars(new_cars)
                await self.send_message_callback(self.chat_id, new_cars_info)

            await asyncio.sleep(interval)

    def get_readable_info_for_cars(self, cars):
        readable_info = list(map(self.readable_info_for_car, cars))
        return '\n'.join(readable_info)

    def find_cars_in_range(self, user_location, search_range, cars) -> set:
        cars_in_range = []
        for car in cars:
            car_position = (car['Lon'], car['Lat'])
            distance = geopy.distance.vincenty(user_location, car_position).km
            if distance < search_range:
                cars_in_range.append(CarInfo(car, distance))

        return set(cars_in_range)

    def readable_info_for_car(self, car_info):
        distance = car_info.distance
        car = car_info.car
        return '{} {} is in {}km'.format(car['Brand'], car['Model'], round(distance, 2))


class CarInfo:
    # TODO: handle somehow insignificant location changes. Now car that was insignificantly moved is treated as new car
    def __init__(self, car, distance):
        self.car = car
        self.distance = distance

    @property
    def custom_id(self):
        return str(self.car['Lat']) + str(self.car['Lon'])

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return str(self.car['Lat'])[-2:] + str(self.car['Lon'])[-2:]

    def __hash__(self):
        return hash(self.custom_id)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.custom_id == other.custom_id
        else:
            return False
