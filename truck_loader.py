# truck_loader.py
# load trucks based on given constraints before implementing delivery algorithms

from truck import Truck


class TruckLoader:
    def __init__(self, hash_table, distance_matrix, address_list):
        self.hash_table = hash_table
        self.distance_matrix = distance_matrix
        self.address_list = address_list
        self.trucks = {1: Truck(1, 16), 2: Truck(2, 16), 3: Truck(3, 16)}

    def load_truck_2_constraints(self):
        # load packages 3, 18, 36, and 38 onto truck 2 as required
        for package_id in [3, 18, 36, 38]:
            package = self.hash_table.lookup(package_id)
            if package:
                self.trucks[2].load_package(package)
                # print(f"Packages 3, 18, 36, 38 loaded on truck 2")

    def load_delayed_packages(self):
        # load all delayed packages together
        delayed_packages = [6, 9, 25, 28, 32]
        for package_id in delayed_packages:
            package = self.hash_table.lookup(package_id)
            if package:
                # arbitrarily choose a truck, may change later
                self.trucks[3].load_package(package)
                # print(f"Delayed packages loaded on truck 3")

    def load_packages_together(self):
        # load all packages that must be delivered together
        together_packages = [13, 14, 15, 16, 19, 20]
        for package_id in together_packages:
            package = self.hash_table.lookup(package_id)
            if package:
                # arbitrarily choose a truck, may change later
                self.trucks[1].load_package(package)
                # print(f"Together-packages loaded on truck 1")

    def load_remaining_packages(self):
        # load all packages that do not have constraints
        for package_id in range(1, 41):
            package = self.hash_table.lookup(package_id)
            if package and not any(package in truck.packages for truck in self.trucks.values()):
                # choose the truck with the least amount of packages
                least_loaded_truck = min(self.trucks.values(), key=lambda t: len(t.packages))
                least_loaded_truck.load_package(package)

    def load_all_trucks(self):
        self.load_truck_2_constraints()
        self.load_delayed_packages()
        self.load_packages_together()
        self.load_remaining_packages()
        # self.execute_greedy_algorithm()


