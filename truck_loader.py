# truck_loader.py

from truck import Truck
from simulated_annealing import SimulatedAnnealing
from datetime import timedelta, datetime


def create_address_to_index(address_list):
    # create a mapping from address to its index in the distance matrix
    address_to_index = {row[2]: int(row[0]) for row in address_list}
    print(f"Address to Index mapping: {address_to_index}")
    return address_to_index


class TruckLoader:
    def __init__(self, hash_table, distance_matrix, address_list):
        self.hash_table = hash_table
        self.distance_matrix = distance_matrix
        self.address_list = address_list
        self.trucks = {1: Truck(1, timedelta(hours=8)),
                       2: Truck(2, timedelta(hours=9, minutes=5)),
                       3: Truck(3, timedelta(hours=10, minutes=20))}

        # initialize address_to_index mapping
        self.address_to_index = create_address_to_index(address_list)

        # initialize sets to hold constrained packages
        self.truck_2_packages = [3, 18, 36, 18]
        self.delayed_packages = [6, 25, 28, 32]
        self.together_packages = [13, 14, 15, 16, 19, 20]

        self.optimizer = SimulatedAnnealing(distance_matrix, init_temp=100, alpha=0.995,
                                            address_to_index=self.address_to_index)

    # def schedule_truck_departures(self, current_time):
    #     for t in self.trucks.values():
    #         if t.status == "At Hub" and t.departure_time <= current_time:
    #             t.depart(current_time)
    #             for package in t.packages:
    #                 package.update_status("En Route", current_time, t.truck_id)

    def load_initial_trucks(self, tl):
        # Load packages that aren't delayed or constrained to leave at 8:00am
        initial_packages = [pkg_id for pkg_id in range(1, 41)
                            if pkg_id not in tl.truck_2_packages and
                            pkg_id not in tl.delayed_packages and
                            pkg_id not in tl.together_packages and
                            pkg_id != 9]  # Exclude package #9

        for package_id in initial_packages:
            package = tl.hash_table.lookup(package_id)
            package.status = "En Route"
            if package:
                # Load onto Truck 1 or 3 based on balance, keeping in mind capacity of 16
                least_loaded_truck = min([tl.trucks[1], tl.trucks[2], tl.trucks[3]],
                                         key=lambda t: len(t.packages))
                if len(least_loaded_truck.packages) < 16:
                    least_loaded_truck.load_package(package)

        print("Initial trucks loaded for 8:00am departure")

    def load_truck_2_packages(self, tl):
        # load packages 3, 18, 36, and 38 onto truck 2 as required
        truck_2_packages = [3, 18, 36, 38]

        for package_id in truck_2_packages:
            package = tl.hash_table.lookup(package_id)
            if package:
                tl.trucks[2].load_package(package)
                tl.truck_2_packages.append(package_id)

        # return truck_2_packages

    def load_together_packages(self, tl):
        # load all packages that must be delivered together
        together_packages = [13, 14, 15, 16, 19, 20]
        for package_id in together_packages:
            package = tl.hash_table.lookup(package_id)
            if package:
                # arbitrarily choose a truck, may change later
                tl.trucks[1].load_package(package)
                # add package to together-packages list
                tl.together_packages.append(package_id)
                # print(f"Together-packages loaded on truck 1")

    def load_delayed_packages(self, tl):
        # load packages delayed until 9:05am
        delayed_packages = [6, 9, 25, 28, 32]
        for package_id in delayed_packages:
            package = tl.hash_table.lookup(package_id)
            if package:
                # arbitrarily choose a truck, may change later
                tl.trucks[3].load_package(package)
                # add package to delayed-package list
                tl.delayed_packages.append(package_id)

    def optimize_truck_routes(self, tl):
        print("Starting route optimization...")
        optimizer = SimulatedAnnealing(self.distance_matrix, init_temp=1000, alpha=0.995,
                                       address_to_index=self.address_to_index)

        for tl in self.trucks.values():
            if tl.packages:
                packages = [pkg_id for pkg_id in tl.packages]
                optimized_route = optimizer.optimize_route(packages)

            # print(f"Optimizing truck {truck.id} with packages: {[pkg.package_id for pkg in truck.packages]}")
            if tl.packages:
                # apply simulated annealing to optimize the route
                # packages = [pkg_id for pkg_id in truck.packages]  # extract package IDs
                optimized_route = self.optimizer.optimize_route(tl.packages)
                # optimized_route = self.optimizer.optimize_route(packages)
                print(f"Optimized route for Truck: {tl.truck_id}: {optimized_route}")

        print("Routes optimized")

