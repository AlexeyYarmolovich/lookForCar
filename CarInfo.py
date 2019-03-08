import geopy.distance


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

    def is_close_to_any(self, other_cars) -> bool:
        if len(other_cars) == 0:
            return False

        my_location = (self.car['Lon'], self.car['Lat'])
        closest_found_distance = 99999999
        for other in other_cars:
            other_location = (other.car['Lon'], other.car['Lat'])
            distance = geopy.distance.distance(my_location, other_location).m
            if distance <= 30:
                return True
            else:
                closest_found_distance = min(distance, closest_found_distance)
                continue
        if len(other_cars) == 1:
            oth_car = list(other_cars)[0]
            print(self.distance, my_location, oth_car.distance, (oth_car.car['Lat'], oth_car.car['Lon']))
        else:
            print(closest_found_distance)
        return False
