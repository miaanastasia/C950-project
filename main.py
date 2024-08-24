# ID: 010347381
# main.py
import truck
from hash_table import HashTable
import csv
from package import Package
from simulated_annealing import SimulatedAnnealing
from datetime import datetime, timedelta
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


def display_truck_status(truck_loader):
    for truck_id, truck in truck_loader.trucks.items():
        print(f"Truck ID: {truck_id}")
        for package in truck.packages:
            print(f"Package: {package.package_id}, Address: {package.address}, Status: {package.status}")


def display_mileage(trucks, distance_matrix):
    total_mileage = sum(truck.calculate_total_distance(distance_matrix) for truck in trucks.values())
    print(f"Total mileage of all trucks: {total_mileage:.2f} miles")


#
#
# def test_hash_function(self):
#     test_keys = list(range(1, 41))
#     for key in test_keys:
#         bucket_index = hash_table._hash_function(str(key))
#         print(f"Package ID: {key}, Hash Index: {bucket_index}")


# starting day here
# simulating the day starting at 8:00am, time will pass in increments of 15 minutes
def simulate_day(truck_loader):
    start_time = datetime.strptime("08:00", "%H:%M")
    end_of_day = datetime.strptime("17:00", "%H:%M")

    current_time = start_time

    while current_time <= end_of_day:
        # print(f"Current time: {current_time.strftime('%H:%M')}")
        truck_loader.schedule_truck_departures(current_time)
        process_deliveries(truck_loader, current_time)
        current_time += timedelta(minutes=15)


def process_deliveries(tl, current_time):
    # check for truck departures
    for truck in tl.trucks.values():
        if truck.is_active():
            for package in truck.packages:
                if package.delivery_time and package.delivery_time <= current_time:
                    package.update_status('Delivered', current_time)
                    print(f"Package {package.package_id} delivered at {package.delivery_time}")

            # check if truck should return to hub
            if truck.return_time and truck.return_time <= current_time:
                truck.return_to_hub(current_time)
                print(f"Truck {truck.truck_id} returned at {truck.return_time}")


def main():
    load_hash_table()

    # pkg1 = Package(1, "123 Elm", "10:20am", "Salt Lake City", "07458", "2lb", "At Hub")
    # pkg2 = Package(2, "456 Oak", "10:30am", "Salt Lake City", "07458", "2lb", "At Hub")
    #
    # hash_table.insert(pkg1.package_id, pkg1)
    # hash_table.insert(pkg2.package_id, pkg2)
    #
    # print(hash_table.lookup(1))
    # print(hash_table.lookup(2))
    # print(hash_table.lookup(3))

    # # Print out the packages in the hash table
    # for package_id in range(1, 41):
    #     package = hash_table.lookup(str(package_id))
    #     if package:
    #         print(f"Package {package.package_id} in hash table: {package}")
    #     else:
    #         print(f"Package {package_id} not in hash table")

    distance_matrix = read_distance_file()
    address_list = read_address_file()
    address_to_index = create_address_to_index(address_list)

    init_temp = 10000
    alpha = 0.9
    # optimizer = SimulatedAnnealing(distance_matrix, init_temp=init_temp, alpha=alpha, address_to_index=address_to_index)

    # create TruckLoader instance and load trucks
    truck_loader = TruckLoader(hash_table, distance_matrix, address_list)

    # initialize simulated annealing with address_to_index for distance calculation
    optimizer = SimulatedAnnealing(distance_matrix, init_temp=1000, alpha=0.895, address_to_index=address_to_index)

    # truck_loader.load_trucks()
    truck_loader.load_together_packages(truck_loader)
    truck_loader.load_initial_trucks(truck_loader)
    # truck_loader.load_delayed_packages(truck_loader)
    # truck_loader.load_trucks()
    #
    truck_loader.optimize_truck_routes(optimizer)
    #
    # simulate_day(truck_loader)
    #
    print(f"Truck 1 packages: {[p.package_id for p in truck_loader.trucks[1].packages]}")
    print(f"Truck 2 packages: {[p.package_id for p in truck_loader.trucks[2].packages]}")
    print(f"Truck 3 packages: {[p.package_id for p in truck_loader.trucks[3].packages]}")
    #
    # display_truck_status(truck_loader)
    # display_mileage(truck_loader, distance_matrix)


if __name__ == "__main__":
    main()
