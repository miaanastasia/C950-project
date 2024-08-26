# ID: 010347381
# main.py

from hash_table import HashTable
import csv
from package import Package
from simulated_annealing import SimulatedAnnealing
from datetime import timedelta
from truck_loader import TruckLoader


# create hash table instance
hash_table = HashTable()


# read in package file and load into hash table
def load_hash_table():
    # opens and closes the file after block of code is executed
    with open('CSV/package.csv', mode='r') as csv_file_1:
        package_data = csv.reader(csv_file_1)

        for pk in package_data:
            package_id = int(pk[0])
            address = pk[1]
            deadline = pk[2]
            city = pk[3]
            zipcode = pk[4]
            weight = pk[5]
            status = "At Hub"

            # create package object and insert into hash table
            package = Package(package_id, address, deadline, city, zipcode, weight, status)
            hash_table.insert(package.package_id, package)
            # print(f"Loaded package {package.package_id}")


# read in address file
def read_address_file():
    with open('CSV/address.csv', mode='r') as csv_file_2:
        address_data = csv.reader(csv_file_2)
        # convert to list for easy access and readability
        address_list = list(address_data)
    return address_list


# function for quick lookup of address indices
def create_address_to_index(address_list):
    return {row[2]: int(row[0]) for row in address_list}


# read in distance file and create matrix
def read_distance_file():
    with open('CSV/distance.csv', mode='r') as csv_file_3:
        distance_data = csv.reader(csv_file_3)

        # create 2-dimensional list
        dist_matrix = []
        for row in distance_data:
            float_row = []
            # convert each value to float and add to the row
            for value in row:
                # handle ValueError exception
                try:
                    float_row = [float(value) for value in row]
                    dist_matrix.append(float_row)
                except ValueError:
                    # print(f"Skipping row due to conversion error: {row}")
                    continue

    return dist_matrix


# this method will ensure we are using two addresses to determine the distance instead of two indices
def find_address_index(address, address_list):
    index = 0
    # for row in distance_matrix:
    for row in address_list:
        if row[2] == address:
            return index
        index += 1
    return -1


# get distance between two addresses from the matrix
def find_distance_between(start_address, end_address, address_list):
    point_1 = find_address_index(start_address, address_list)
    point_2 = find_address_index(end_address, address_list)
    distance = distance_matrix[point_1][point_2]

    # if distance one way is empty, get distance from opposite way
    if distance is None:
        distance = distance_matrix[point_2][point_1]

    # convert distance to float and validate
    return float(distance) if distance is not None else None


def display_truck_status(truck_loader):
    for truck_id, truck in truck_loader.trucks.items():
        print(f"Truck ID: {truck_id}")
        for package in truck.packages:
            print(f"Package: {package.package_id}, Address: {package.address}, Status: {package.status}")


def display_mileage(trucks, distance_matrix):
    total_mileage = sum(truck.calculate_total_distance(distance_matrix) for truck in trucks.values())
    print(f"Total mileage of all trucks: {total_mileage:.2f} miles")


# starting day here
# simulating the day starting at 8:00am, time will pass in increments of 15 minutes
# def simulate_day(truck_loader):
#     start_time = timedelta(hours=8)
#     end_of_day = timedelta(hours=17)
#
#     current_time = start_time
#
#     while current_time <= end_of_day:
#         if current_time == timedelta(hours=8):
#             truck_loader.load_initial_trucks(truck_loader)
#             truck_loader.load_together_packages(truck_loader)
#         elif current_time == timedelta(hours=9, minutes=5):
#             truck_loader.load_truck_2_packages(truck_loader)
#         elif current_time == timedelta(hours=10, minutes=20):
#             truck_loader.load_delayed_packages(truck_loader)
#
#     process_deliveries(truck_loader.trucks)


def process_deliveries(tl, address_list):
    # loop over all available trucks and deliver packages
    for truck in tl.trucks.values():
        # current_location = "HUB"
        current_location = "4001 South 700 East"
        current_time = truck.departure_time
        min_distance = 999
        min_package = None
        # process each package in the truck
        for package in truck.packages:
            print(f"Processing delivery for Package {package.package_id} on Truck {truck.truck_id}")

            # greedy nearest neighbor
            # calculate minimum distance
            distance = find_distance_between(current_location, package.address, address_list)
            # if distance < min_distance:
            min_distance = distance
            min_package = package
            # else:
            #     print("Error: distance greater than minimum distance")

            # update truck's current time and package's delivery time
            current_time += timedelta(hours=min_distance / 18)
            min_package.delivery_time = current_time
            min_package.update_status('Delivered', current_time)
            print(f"Package {min_package.package_id} delivered at {min_package.delivery_time} on Truck {truck.truck_id}")
            current_location = package.address

        truck.current_package_index += 1

        # truck returns to hub after completing deliveries
        # truck.return_to_hub(current_time)
        # print(f"Truck {truck.truck_id} returned to hub at {truck.return_time}")


distance_matrix = read_distance_file()
# address_list = read_address_file()
# address_to_index = create_address_to_index(address_list)


def main():
    load_hash_table()
    address_list = read_address_file()
    address_to_index = create_address_to_index(address_list)

    print(distance_matrix)

    # create TruckLoader instance and load trucks
    truck_loader = TruckLoader(hash_table, distance_matrix, address_list)
    # trucks = truck.get_route(truck_loader)

    # simulate_day(truck_loader)

    # initialize simulated annealing with address_to_index for distance calculation
    optimizer = SimulatedAnnealing(distance_matrix, init_temp=100, alpha=0.995, address_to_index=address_to_index)

    # truck_loader.load_trucks()
    truck_loader.load_truck_2_packages(truck_loader)
    truck_loader.load_together_packages(truck_loader)
    truck_loader.load_initial_trucks(truck_loader)
    truck_loader.load_delayed_packages(truck_loader)
    # truck_loader.load_trucks()
    #
    truck_loader.optimize_truck_routes(optimizer)
    #

    #
    print(f"Truck 1 packages: {[p.package_id for p in truck_loader.trucks[1].packages]}")
    print(f"Truck 2 packages: {[p.package_id for p in truck_loader.trucks[2].packages]}")
    print(f"Truck 3 packages: {[p.package_id for p in truck_loader.trucks[3].packages]}")

    #
    # display_truck_status(truck_loader)
    process_deliveries(truck_loader, address_list)


if __name__ == "__main__":
    main()
