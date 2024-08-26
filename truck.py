# truck.py

from datetime import datetime, timedelta


class Truck:
    def __init__(self, truck_id, departure_time):
        self.truck_id = truck_id
        self.driver = None
        self.packages = []
        self.route = []  # list of points in the distance matrix
        self.status = "At Hub"
        self.departure_time = departure_time
        self.current_package_index = 0  # incrementing index

    def assign_driver(self, driver):
        self.driver = driver

    def load_package(self, package):
        if len(self.packages) < 16:
            self.packages.append(package)
            return True
        return False

    def get_route(self):
        return self.route

    def depart(self, current_time):
        self.departure_time = current_time
        self.status = "En Route"

    def is_active(self):
        return self.status == "En Route"

    def return_to_hub(self, return_time):
        self.return_time = return_time
        self.status = "At Hub"

    def __str__(self):
        return f"Truck {self.truck_id}: {self.status}, Packages: {[pkg.package_id for pkg in self.packages]}"

