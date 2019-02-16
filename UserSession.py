import geopy.distance


class UserSession:
    def __init__(self, map_info, chat_id, user_location):
        self.map_info = map_info
        self.chat_id = chat_id
        self.last_location = (user_location['longitude'], user_location['latitude'])


    def start(self, callback):
        cars = self.map_info.get_cars_info()
        self.callback = callback
        self.find_cars_in_range(self.last_location, 5, cars)


    def find_cars_in_range(self, user_location, search_range, cars):
        cars_in_range = []
        for car in cars:
            car_position = (car['Lon'], car['Lat'])
            distance = geopy.distance.vincenty(user_location, car_position).km
            if distance < search_range:
                cars_in_range.append({'car': car, 'distance': distance})
        if len(cars_in_range) > 0:
            readable_info = list(map(self.readable_info_for_car, cars_in_range))
            self.callback(self.chat_id, readable_info)
            print(readable_info)

    def readable_info_for_car(self, car_info):
        distance = car_info['distance']
        car = car_info['car']
        return '{} {} is in {}km'.format(car['Brand'], car['Model'], round(distance, 2))
