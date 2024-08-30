# truck.py

class Truck:
    def __init__(self, truck_id, departure_time):
        self.truck_id = truck_id
        # self.driver = None
        self.package_list = []
        self.route = []  # list of points in the distance matrix
        self.status = "At Hub"
        self.departure_time = departure_time

    def load_package(self, package):
        if len(self.package_list) < 16:
            self.package_list.append(package)
            self.status = 'En Route'
            return True
        return False

