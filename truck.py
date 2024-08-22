# truck.py

class Truck:
    def __init__(self, truck_id, capacity):
        self.truck_id = truck_id
        self.capacity = capacity
        self.packages = []
        self.current_location = "Hub"
        self.status = "At Hub"

    def load_package(self, package):
        if len(self.packages) < self.capacity:
            self.packages.append(package)
            # print(f"Package {package} is loaded")
        else:
            print(f"Truck {self.truck_id} is full")



    """
        def __init__(self, capacity, speed, load, packages, mileage, address, departure_time):
            self.capacity = capacity
            self.speed = speed
            self.load = load
            self.packages = packages
            self.mileage = mileage
            self.address = address
            self.departure_time = departure_time
    """


