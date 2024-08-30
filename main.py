# Mia Mitchell
# ID: 010347381
import truck
# main.py

from hash_table import HashTable
import csv
from package import Package
from simulated_annealing import SimulatedAnnealing
from datetime import timedelta
from truck_loader import TruckLoader

# create hash table instance
hash_table = HashTable()


# **********************************************************************************************************************
#                                PROCESS DATA FOR PACKAGES, ADDRESSES, AND DISTANCES

# Read in data from the package, address, and distance files.  The package data will be loaded into a hash table for
# easy access and organization.  The address data will be loaded into a simple list, and the distance data will be
# loaded into a matrix for 1:1 address mapping.

# **********************************************************************************************************************

# read in package file and load into hash table
def load_hash_table():
    # opens and closes the file after block of code is executed
    with open('CSV/package.csv', mode='r') as csv_file_1:
        package_data = csv.reader(csv_file_1)

        # load each column of data into the table, identifiable by unique package ID
        for pk in package_data:
            package_id = int(pk[0])
            address = pk[1]
            city = pk[2]
            state = pk[3]
            zipcode = pk[4]
            deadline = pk[5]
            weight = pk[6]
            note = pk[7]

            # create package object and insert into hash table
            package = Package(package_id, address, city, state, zipcode, deadline, weight, note)
            hash_table.insert(package.package_id, package)
            # print(f"Loaded package {package.package_id}")


# read in address file
def read_address_file():
    with open('CSV/address.csv', mode='r') as csv_file_2:
        address_data = csv.reader(csv_file_2)
        # convert to list for easy access and iteration
        address_list = list(address_data)
    return address_list


# read in distance file and create matrix
def read_distance_file():
    with open('CSV/distance.csv', mode='r') as csv_file_3:
        distance_data = csv.reader(csv_file_3)
        # create 2-dimensional list
        dist_matrix = []
        for row in distance_data:
            dist_matrix.append(row)

    return dist_matrix


# ensure we are using two addresses to determine the distance between packages instead of two indices
# extract address only from each row in address list
def find_address_index(address, address_list):
    index = 0
    for row in address_list:
        # row already identified, now aligning index with address at index 2, NOT location name at index 1
        # e.g. '4001 South 700 East', '0'
        if row[2] == address:
            return index
        index += 1
    return -1


# get distance between two points in the address list
def find_distance_between(start_address, end_address, address_list):
    # map each address to its index to find stored distance
    point_1 = find_address_index(start_address, address_list)
    point_2 = find_address_index(end_address, address_list)
    distance = distance_matrix[point_1][point_2]

    # if distance one way is empty, get distance from opposite way
    if distance == '':
        distance = distance_matrix[point_2][point_1]

    # convert distance to float and validate
    return float(distance) if distance is not None else None


# **********************************************************************************************************************
# **********************************************************************************************************************


# initial sort of packages by earliest deadline
def sort_by_deadline(packages):
    # sort through packages in hash table using deadline as the key
    return sorted(packages, key=lambda p: p.deadline)


# **********************************************************************************************************************
#                                       LOADING AND DELIVERING PACKAGES

# Each package will be processed on one of the three trucks, accounting for proximity from hub, delivery deadline, and
# any special note(s) the package may have.  The process_truck() function will loop through all packages using the
# greedy nearest neighbor algorithm and deliver packages accordingly, while updating delivery time and mileage for each
# individual truck.  The process_deliveries() function calls process_truck() and returns the mileage for all three
# trucks, or total mileage of the route.

# **********************************************************************************************************************

# deliver packages after sorting
def process_deliveries(tl, address_list):
    # loop over all available trucks and deliver packages
    route_mileage = 0  # placeholder for total mileage of all three trucks
    for t in tl.trucks.values():
        process_truck(t, address_list)
        route_mileage += t.truck_mileage

    # print("\nAll packages have been delivered.")
    # print(f"Total mileage for route: {route_mileage}\n")
    return route_mileage


def process_truck(t, address_list):
    current_location = "4001 South 700 East"
    current_time = t.departure_time
    t.truck_mileage = 0  # initialize total mileage for each truck

    # Ensure package 25 is delivered first on Truck 2 because of late delivery time
    # original delivery time was 11:22 am, now delivering at 09:13 am within deadline constraint
    package_25 = next((pkg for pkg in t.package_list if pkg.package_id == 25), None)
    if package_25:
        distance = find_distance_between(current_location, package_25.address, address_list)
        current_time += timedelta(hours=distance / 18)
        package_25.delivery_time = current_time
        package_25.departure_time = t.departure_time
        package_25.update_delivery_status('Delivered', current_time)
        t.truck_mileage += distance
        current_location = package_25.address
        package_25.truck_id = t.truck_id
        t.package_list.remove(package_25)

    while len(t.package_list) > 0:
        min_distance = 999
        min_package = None
        # process each package in the truck
        # the function should be processing the optimized routes here, NOT the initial routes
        for package in t.package_list:
            # print(f"\nProcessing delivery for Package {package.package_id} on Truck {t.truck_id}")

            # greedy nearest neighbor
            # calculate minimum distance to find next package to deliver
            distance = find_distance_between(current_location, package.address, address_list)

            if distance < min_distance:
                min_distance = distance
                min_package = package

        # update truck's current time and package's delivery time
        current_time += timedelta(hours=min_distance / 18)
        min_package.delivery_time = current_time
        min_package.departure_time = t.departure_time
        min_package.update_delivery_status('Delivered', current_time)
        # update distance traveled for each truck
        t.truck_mileage += min_distance
        # print(
        #     f"Package {min_package.package_id} delivered at {min_package.delivery_time} on Truck {t.truck_id}")

        # identify which truck each package is on
        min_package.truck_id = t.truck_id

        # mark current location at address where current package was delivered
        current_location = min_package.address

        # remove the delivered package from the truck's list of remaining packages
        t.package_list.remove(min_package)

    # return mileage for each individual truck
    return t.truck_mileage


# user interface for interactive console application
def user_interface():
    print(f"WGUPS Package Delivery System\tC950\tMia Mitchell\t010347381\n")
    print("Welcome to the Western Governors University Parcel Service.")

    route_mileage = process_deliveries(truck_loader, address_list)
    print(f"Total mileage for the route: {route_mileage}")

    while True:
        print("\nMenu:")
        print("1. All Package Details")
        print("2. Individual Package Status at a Specific Time")
        print("3. Status of All Packages at a Specific Time")
        print("4. Exit")
        choice = input("Please choose an option (1, 2, 3, or 4): ")

        if choice == '1':
            # print all packages and relevant data after all have been delivered
            for i in range(1, 41):
                print(hash_table.lookup(i))

        elif choice == '2':
            # identify individual package and retrieve from hash table
            pkg = input("Choose a package (1-40): ")
            package = hash_table.lookup(int(pkg))

            # identify a time to check status
            time = input("Please enter a time in this format: (HH:MM) ")
            # parse input into hours, minutes by ':'
            (hours, minutes) = time.split(':')
            convert_time = timedelta(hours=int(hours), minutes=int(minutes))
            # prints package object as a formatted string
            print(package.print_status(convert_time))

        elif choice == '3':
            # identify a time
            time = input("Please enter a time in this format: (HH:MM) ")
            # parse input into hours, minutes by ':'
            (hours, minutes) = time.split(':')
            convert_time = timedelta(hours=int(hours), minutes=int(minutes))
            for i in range(1, 41):
                package = hash_table.lookup(i)
                # prints all package objects with status at specific time as formatted string
                print(package.print_status(convert_time))

        elif choice == '4':
            print("Exiting program.")
            break

        else:
            print("Invalid choice. Please try again.")


# **********************************************************************************************************************
#                                        LOAD HASH TABLE AND NECESSARY FILES
# **********************************************************************************************************************
load_hash_table()
address_list = read_address_file()
distance_matrix = read_distance_file()

# retrieve a list of package objects to sort
all_packages = hash_table.get_all_packages()

# sort by delivery deadline to get initial routes for each truck
sorted_by_deadline = sort_by_deadline(all_packages)
# print(f"Sort by deadline {sorted_by_deadline}\n")

# **********************************************************************************************************************
#   CREATE TRUCK LOADER INSTANCE
#   FIND INITIAL ROUTES (lists of sorted packages for each truck)
#   USE GREEDY ALGORITHM TO FIND AN OPTIMAL ROUTE IN ACCORDANCE WITH CONSTRAINTS
# **********************************************************************************************************************

truck_loader = TruckLoader(hash_table, distance_matrix, address_list, sorted_by_deadline)

truck_loader.load_truck_1_packages(truck_loader)
truck_loader.load_truck_2_packages(truck_loader)
# adjust_route_for_deadline(package, address_list)
truck_loader.load_remaining_packages(truck_loader)

user_interface()

# **********************************************************************************************************************
#                                    ROUTE OPTIMIZATION WITH SIMULATED ANNEALING
# **********************************************************************************************************************

# # initialize simulated annealing with address_to_index for distance calculation
# simulated_annealing = SimulatedAnnealing(find_distance_between, distance_matrix, address_list, init_temp=10000,
#                                          alpha=0.995)
# #
# # # map each truck route as a dictionary with key 'truck_id' : value 'package_list'
# # # we will pass this to the optimization algorithm
# truck_routes = {t.truck_id: t.package_list for t in truck_loader.trucks.values()}
#
# optimized_route = simulated_annealing.simulated_annealing(truck_routes)
# #
# # # optimize the routes for each truck now that they have been initially sorted
# for t in truck_loader.trucks.values():
#     # retrieve key:value from dictionary
#     t.package_list = optimized_route.get(t.truck_id, t.package_list)
#
# # sort packages on each truck before processing deliveries
# for truck in truck_loader.trucks.values():
#     start_address = "4001 South 700 East"  # hub address
#     sorted_packages = sort_after_loading(truck.package_list, start_address, address_list)
#     print(f"Sorted packages: {sorted_packages}")
#     truck.package_list = sorted_packages
#
# # optimize routes now that packages have been sorted on each truck
# truck_loader.optimize_truck_routes()

# **********************************************************************************************************************
# **********************************************************************************************************************
