# ID: 010347381
# main.py

import datetime
import random
import math
from hash_table import HashTable
import csv
from package import Package
from truck_loader import TruckLoader

# create hash table instance
hash_table = HashTable()


# read in package file and load into hash table
def load_hash_table():
    # opens and closes the file after block of code is executed
    with open('CSV/package.csv', mode='r') as csv_file_1:
        package_data = csv.reader(csv_file_1)

        for pk in package_data:
            package_id = pk[0]
            address = pk[1]
            deadline = pk[2]
            city = pk[3]
            zipcode = pk[4]
            weight = pk[5]
            status = "At Hub"

            # create package object and insert into hash table
            package = Package(package_id, address, deadline, city, zipcode, weight, status)
            hash_table.insert(package.package_id, package)


# read in address file
def read_address_file():
    with open('CSV/address.csv', mode='r') as csv_file_2:
        address_data = csv.reader(csv_file_2)
        # convert to list for easy access and readability
        address_list = list(address_data)
    return address_list


# read in distance file and create matrix
def read_distance_file():
    with open('CSV/distance.csv', mode='r') as csv_file_3:
        distance_data = csv.reader(csv_file_3)

        # create 2-dimensional list
        distance_matrix = []
        for row in distance_data:
            float_row = []
            # convert each value to float and add to the row
            for value in row:
                # handle ValueError exception
                try:
                    float_row = [float(value) for value in row]
                    distance_matrix.append(float_row)
                except ValueError:
                    # print(f"Skipping row due to conversion error: {row}")
                    continue

    return distance_matrix


# get distance between two addresses from the matrix
def find_distance_between(point_1, point_2, distance_matrix):
    distance = distance_matrix[point_1][point_2]

    # if distance one way is empty, get distance from opposite way
    if distance is None:
        distance = distance_matrix[point_2][point_1]

    # convert distance to float and validate
    return float(distance) if distance is not None else None


'''
# TESTING
load_hash_table()

addresses = read_address_file()
print(addresses)

dist_matrix = read_distance_file()
print(dist_matrix)
'''


# function to find the nearest package
def find_nearest_package(curr_location, packages, distance_matrix, address_list):
    min_distance = float('inf')
    nearest_package = None

    for package in packages:
        # get index of current location and package delivery address
        curr_index = address_list.index(curr_location)
        package_index = address_list.index(package.address)

        # get distance between current location and package address
        distance = distance_matrix[curr_index][package_index]

        # find package with minimum distance
        if distance < min_distance:
            min_distance = distance
            nearest_package = package

    return nearest_package, min_distance


# initial greedy algorithm to deliver packages
def greedy_initial_algorithm(packages, distance_matrix, address_list, start_location, truck_speed=18):
    curr_location = start_location
    total_time = datetime.timedelta(hours=0)
    delivered_packages = []

    # sort packages based on priority or other criteria if needed
    # starting by prioritizing the earliest deadline
    packages.sort(key=lambda p: p.deadline)

    while packages:
        # find nearest package to deliver next
        nearest_package, distance = find_nearest_package(curr_location, packages, distance_matrix, address_list)

        if nearest_package:
            time_taken = datetime.timedelta(hours=distance / truck_speed)

            # update current time and location
            total_time += time_taken
            curr_location = nearest_package.address

            # mark as delivered and remove from list of packages
            nearest_package.status = "Delivered"
            delivered_packages.append(nearest_package)
            packages.remove(nearest_package)

            # TESTING
            print(f"Delivered {nearest_package.package_id} to {nearest_package.address}")

        else:
            break

        return delivered_packages


def calculate_total_distance(trucks, dist_matrix):
    total_distance = 0

    for truck in trucks.values():
        for i in range(len(truck.packages) - 1):
            from_address = truck.packages[i].address
            to_address = truck.packages[i + 1].address

            from_index = truck.packages[i].address_list.index(from_address)
            to_index = truck.packages[i + 1].address_list.index(to_address)

            total_distance += dist_matrix[from_index][to_index]

    return total_distance


# simulated annealing approach for optimization begins here
# neighbor solution slightly modifies existing greedy solution
def generate_neighbor_solution(trucks):
    # choose two random trucks
    truck_ids = list(trucks.keys())
    truck1, truck2 = random.sample(truck_ids, 2)

    if trucks[truck1].packages and trucks[truck2].packages:
        # choose a random package between two trucks
        package1 = random.choice(trucks[truck1].packages)
        package2 = random.choice(trucks[truck2].packages)

        # swap the packages between the two trucks
        trucks[truck1].packages.remove(package1)
        trucks[truck2].packages.remove(package2)
        trucks[truck1].packages.append(package2)
        trucks[truck2].packages.append(package1)

    # return the modified trucks as the new neighbor solution
    return trucks


# define small probability of acceptance for non-optimal solutions
def acceptance_probability(old_cost, new_cost, temp):
    if new_cost < old_cost:
        return 1.0
    return math.exp((new_cost - old_cost) / temp)


# reduce scope of search for next point by slightly lowering temperature
def cooling_schedule(init_temp, alpha, iteration):
    return init_temp * (alpha ** iteration)


def simulated_annealing(trucks, dist_matrix, address_list, init_temp=10000, alpha=0.995, stop_temp=1):
    curr_solution = trucks
    curr_cost = calculate_total_distance(trucks, dist_matrix)
    temp = init_temp
    iteration = 0

    while temp > stop_temp:
        new_solution = generate_neighbor_solution(trucks)
        new_cost = calculate_total_distance(trucks, dist_matrix)

        if acceptance_probability(curr_cost, new_cost, temp) > random.random():
            curr_cost = new_cost
            curr_solution = new_solution
        temp = cooling_schedule(temp, alpha, iteration)
        iteration += 1

    return curr_solution


load_hash_table()
addresses = read_address_file()
distance_matrix = read_distance_file()

# create TruckLoader instance
truck_loader = TruckLoader(hash_table, distance_matrix, addresses)
truck_loader.load_all_trucks()

initial_trucks = truck_loader.trucks
all_packages = hash_table.get_all_packages()
delivered_packages = greedy_initial_algorithm(all_packages, distance_matrix, addresses,
                                              "Western Governors University")

optimized_trucks = simulated_annealing(initial_trucks, distance_matrix, addresses)


def display_truck_status(trucks):
    for truck_id, truck in trucks.items():
        print(f"Truck ID: {truck_id}")
        for package in truck.packages:
            print(f"Package: {package.package_id}, Address: {package.address}, Status: {package.status}")


def main():
    while True:
        print("Options:")
        print("1. View Truck Status")
        print("2. Exit")

        choice = input("Enter your choice: ")
        if choice == "1":
            display_truck_status(optimized_trucks)
        elif choice == "2":
            break
        else:
            print("Invalid choice")
