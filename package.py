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

    def update_status(self, convert_time):
        if self.delivery_time < convert_time:
            self.status = "Delivered"
        elif self.departure_time < convert_time:
            self.status = "En Route"
        else:
            self.status = "At Hub"

    def update_address(self, new_address):
        self.address = new_address


