# package.py

class Package:
    def __init__(self, package_id, address, deadline, city, zipcode, weight, status):
        self.package_id = package_id
        self.address = address
        self.deadline = deadline
        self.city = city
        self.zipcode = zipcode
        self.weight = weight
        self.status = status
        self.departure_time = None
        self.delivery_time = None
        self.truck_id = None

    def update_status(self, new_status, time, truck_id=None):
        self.status = new_status
        if new_status == "En Route":
            self.departure_time = time
            self.truck_id = truck_id
        elif new_status == "Delivered":
            self.delivery_time = time

    # return string value instead of memory address for readability
    def __str__(self):
        return (f"Package ID: {self.package_id}, Address: {self.address}, Status: {self.status}, "
                f"Delivery Time: {self.delivery_time}, Truck ID: {self.truck_id}")

    def __repr__(self):
        return self.__str__()

