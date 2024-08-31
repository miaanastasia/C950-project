# package.py

from datetime import timedelta
import datetime


class Package:
    def __init__(self, package_id, address, city, state, zipcode, deadline, weight, note):
        self.package_id = package_id
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.deadline = deadline
        self.weight = weight
        self.note = note

        self.status = 'At Hub'  # default package status
        self.distance_from_hub = None
        self.departure_time = None
        self.delivery_time = None
        self.truck_id = None

    # update package status when delivered and account for delivery time
    def update_delivery_status(self, new_status, time, truck_id=None):
        self.status = new_status
        if new_status == "En Route":
            self.departure_time = time
            self.truck_id = truck_id
        elif new_status == "Delivered":
            self.delivery_time = time

    # return full package object details as a formatted string
    # used to display all package objects at the end of the day (all packages have been delivered)
    def __str__(self):
        return (
            f"Package ID: {self.package_id:<5}  "
            f"Deadline: {self.deadline:<15}  "
            f"Status: {self.status:<15}  "  
            f"Delivery Time: {str(self.delivery_time):<10}  "
            f"Truck ID: {self.truck_id:<5}  "
            f"Address: {self.address:<40}  "
            f"City: {self.city:<25}  "
            f"State: {self.state:<10}  "
            f"Zipcode: {self.zipcode:<10}  "
            f"Weight: {self.weight:<10}  "
            f"Note: {self.note:<10}"
        )

    # used to display the status of all packages at any point in the day
    def print_status(self, user_time):
        temp_status = 'At Hub'
        temp_delivery_time = ''
        if user_time < self.departure_time:
            temp_status = 'At Hub'
        elif user_time > self.delivery_time:
            temp_status = 'Delivered'
            temp_delivery_time = self.delivery_time
        else:
            temp_status = 'En Route'
        return (
            # f"Package ID: {self.package_id:<5}  "
            # f"Address: {self.address:<40}  "
            # f"City: {self.city:<25}  "
            # f"State: {self.state:<10}  "
            # f"Zipcode: {self.zipcode:<10}  "
            # f"Deadline: {self.deadline:<20}  "
            # f"Status: {temp_status:<20}  "
            # f"Weight: {self.weight:<10}  "
            # f"Delivery Time: {str(temp_delivery_time):<10}  "
            # f"Truck ID: {self.truck_id:<10}  "
            # f"Note: {self.note:<10}"
            f"Package ID: {self.package_id:<5}  "
            f"Deadline: {self.deadline:<15}  "
            f"Status: {temp_status:<15}  "
            f"Delivery Time: {str(temp_delivery_time):<10}  "
            f"Truck ID: {self.truck_id:<5}  "
            f"Address: {self.address:<40}  "
            f"City: {self.city:<25}  "
            f"State: {self.state:<10}  "
            f"Zipcode: {self.zipcode:<10}  "
            f"Weight: {self.weight:<10}  "
            f"Note: {self.note:<10}"
        )

    def __repr__(self):
        return self.__str__()
