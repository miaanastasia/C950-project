# ID: 010347381
# main.py
import package
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

        # load each column of data into the table, identifiable by unique package ID
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
        # convert to list for easy access and iteration
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


# ensure we are using two addresses to determine the distance between packages instead of two indices
# extract address only from each row in address list
def find_address_index(address, address_list):
    index = 0
    # for row in distance_matrix:
    for row in address_list:
        # using address at index 2, NOT location name at index 1
        # i.e. '0', '4001 South 700 East'
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
    if distance is None:
        distance = distance_matrix[point_2][point_1]

    # convert distance to float and validate
    return float(distance) if distance is not None else None


# def display_truck_status(truck_loader):
#     for truck_id, truck in truck_loader.trucks.items():
#         print(f"Truck ID: {truck_id}")
#         for package in truck.packages:
#             print(f"Package: {package.package_id}, Address: {package.address}, Status: {package.status}")
#


# quicksort package list after loading packages but before deliveries are made
# citing StackOverflow as reference https://stackoverflow.com/questions/18262306/quicksort-with-python
def sort_packages(packages, start_address, address_list):
    # validation if there is only one element in the array
    if len(packages) <= 1:
        return packages

    pivot = packages[0]  # set pivot to first element in array for comparison
    # find distance in miles between start location (hub) and pivot location
    pivot_distance = find_distance_between(start_address, pivot.address, address_list)

    # find distance in miles between hub and next package address, compare to pivot distance
    less = \
        [pkg for pkg in packages if find_distance_between(start_address, pkg.address, address_list) < pivot_distance]
    equal = \
        [pkg for pkg in packages if find_distance_between(start_address, pkg.address, address_list) == pivot_distance]
    greater = \
        [pkg for pkg in packages if find_distance_between(start_address, pkg.address, address_list) > pivot_distance]

    # join sorted lists
    return (sort_packages(less, start_address, address_list) + equal +
            sort_packages(greater, start_address, address_list))


# deliver packages after sorting and optimization
def process_deliveries(tl, address_list):
    # loop over all available trucks and deliver packages
    for truck in tl.trucks.values():
        # current_location = "HUB"
        current_location = "4001 South 700 East"
        current_time = truck.departure_time
        truck.total_mileage = 0  # initialize total mileage for each truck
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
            # update distance traveled for each truck
            truck.total_mileage += min_distance
            print(
                f"Package {min_package.package_id} delivered at {min_package.delivery_time} on Truck {truck.truck_id}")
            current_location = package.address

        print(f"Total mileage for Truck {truck.truck_id}: {truck.total_mileage}")

        truck.current_package_index += 1


distance_matrix = read_distance_file()


# address_list = read_address_file()
# address_to_index = create_address_to_index(address_list)


def main():
    load_hash_table()
    address_list = read_address_file()
    address_to_index = create_address_to_index(address_list)

    # print(distance_matrix)

    # create TruckLoader instance and load trucks
    truck_loader = TruckLoader(hash_table, distance_matrix, address_list)

    # initialize simulated annealing with address_to_index for distance calculation
    optimizer = SimulatedAnnealing(distance_matrix, init_temp=100, alpha=0.995, address_to_index=address_to_index)

    truck_loader.load_truck_2_packages(truck_loader)
    truck_loader.load_together_packages(truck_loader)
    truck_loader.load_initial_trucks(truck_loader)
    truck_loader.load_delayed_packages(truck_loader)

    # sort packages on each truck before processing deliveries
    for truck in truck_loader.trucks.values():
        start_address = "4001 South 700 East"  # hub address
        sorted_packages = sort_packages(truck.packages, start_address, address_list)
        print(f"Sorted packages: {sorted_packages}")
        truck.packages = sorted_packages

    # optimize routes now that packages have been sorted on each truck
    # truck_loader.optimize_truck_routes(optimizer)

    # process all deliveries along optimized routes
    process_deliveries(truck_loader, address_list)

    #
    print(f"Truck 1 packages: {[p.package_id for p in truck_loader.trucks[1].packages]}")
    print(f"Truck 2 packages: {[p.package_id for p in truck_loader.trucks[2].packages]}")
    print(f"Truck 3 packages: {[p.package_id for p in truck_loader.trucks[3].packages]}")

    #
    # display_truck_status(truck_loader)


if __name__ == "__main__":
    main()
