import geopy.distance
import asyncio
from CarInfo import CarInfo


def find_cars_in_range(user_location, search_range, cars) -> set:
    cars_in_range = []
    for car in cars:
        car_position = (car['Lon'], car['Lat'])
        distance = geopy.distance.distance(user_location, car_position).km
        if distance < search_range:
            cars_in_range.append(CarInfo(car, distance))

    return set(cars_in_range)


def readable_info_for_car(car_info):
    distance = car_info.distance
    car = car_info.car
    return '{} {} is in {}km'.format(car['Brand'], car['Model'], round(distance, 2))


def get_readable_info_for_cars(cars):
    sorted_cars = sorted(cars, key=lambda car: car.distance)
    readable_info = list(map(readable_info_for_car, sorted_cars))
    return '\n'.join(readable_info)


class UserSession:
    def __init__(self, map_info, chat_id, callback):
        self.map_info = map_info
        self.chat_id = chat_id
        self.send_message_callback = callback
        self.last_location = None
        self.started = False
        self.search_range = None

    async def set_last_location(self, location):
        self.last_location = location

        if not self.started:
            self.started = True
            await self.start(self.search_range)

    async def start(self, search_range=None):
        search_range = search_range if search_range is not None else 1.5
        self.search_range = search_range
        if self.last_location is None:
            await self.send_message_callback(self.chat_id, 'send me your location please')
        else:
            self.started = True
            await self.send_message_callback(self.chat_id, 'starting with search range {}km'.format(search_range))
            await self.start_check_cycle(self.search_range)

    def stop(self):
        self.started = False

    async def start_check_cycle(self, search_range):
        print('start_check_cycle begin')
        interval = 15
        distance = search_range
        is_first_iteration = True
        known_cars = set()
        while self.started:
            cars = self.map_info.get_cars_info()
            found_cars = find_cars_in_range(self.last_location, distance, cars)
            # look for cars that weren't found before
            new_cars = found_cars.difference(known_cars)
            # look for cars that were found but are not visible now
            dismissed_cars = known_cars.difference(found_cars)

            precised_new_cars = list(filter(lambda new_car: not new_car.is_close_to_any(dismissed_cars), new_cars))
            precised_dismissed_cars = list(filter(lambda dismissed_car:
                                                  not dismissed_car.is_close_to_any(new_cars), dismissed_cars))
            if not (len(dismissed_cars) - len(precised_dismissed_cars)) == (len(new_cars) - len(precised_new_cars)):
                print('!!!!!!!!!!!!!!!!! thats instead of exception')
            else:
                print('precision is ', len(dismissed_cars) - len(precised_dismissed_cars))

            known_cars.update(precised_new_cars)
            known_cars.difference_update(precised_dismissed_cars)

            if len(precised_new_cars) > 0:
                new_cars_info = get_readable_info_for_cars(precised_new_cars)
                await self.send_message_callback(self.chat_id, new_cars_info)
            elif is_first_iteration:
                await self.send_message_callback(self.chat_id, ' currently I don\'t see cars around you, but I\'ll let you know when smth appears')

            print('found {} cars in range, {} new cars, {} dismissed,  {} new cars after precision'
                  .format(len(found_cars), len(new_cars), len(dismissed_cars), len(precised_new_cars)))
            is_first_iteration = False
            await asyncio.sleep(interval)
