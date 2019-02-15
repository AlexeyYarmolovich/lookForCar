import geopy.distance


class UserSession:
    def __init__(self, map_info, user_id, user_location):
        self.map_info = map_info
        self.user_id = user_id
        self.last_location = (user_location['longitude'], user_location['latitude'])


    def start(self, callback):
        cars = self.map_info.get_cars_info()
        self.callback = callback
        self.find_cars_in_range(self.last_location, 1000, cars)


    def find_cars_in_range(self, user_location, search_range, cars):
        cars_in_range = []
        for car in cars:
            car_position = ( car['Lon'], car['Lat'])
            a = geopy.distance.vincenty(user_location, car_position).km
            if a < search_range:
                cars_in_range.append(car)
        if len(cars_in_range) > 0:
            self.callback(cars_in_range)
            print('did it sent message?')


