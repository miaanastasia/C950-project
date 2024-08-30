# truck_loader.py

from truck import Truck
from datetime import timedelta


class TruckLoader:
    def __init__(self, hash_table, distance_matrix, address_list, sorted_packages):
        self.hash_table = hash_table
        self.distance_matrix = distance_matrix
        self.address_list = address_list
        self.sorted_packages = sorted_packages

        # all packages that must be loaded together will go out on Truck 1 at 8:00am
        # all delayed packages except for 9 will go out on Truck 2 at 9:05am based on sorting of packages by deadline
        # all remaining packages will be sorted by distance and loaded accordingly across the three trucks
        self.trucks = {1: Truck(1, timedelta(hours=8)),
                       2: Truck(2, timedelta(hours=9, minutes=5)),
                       3: Truck(3, timedelta(hours=10, minutes=20))}

        # initialize sets to hold constrained packages
        # all together-packages loaded on Truck 1.  truck leaves from hub at 8:00am
        self.together_packages = [13, 14, 15, 16, 19, 20]
        # all delayed packages loaded on Truck 2.  truck leaves from hub at 09:05am
        self.delayed_packages = [6, 25, 28, 32, 3, 18, 36, 38]
        self.remaining_packages = [35, 5, 37, 12, 8, 9, 30, 39]

    def load_truck_1_packages(self, tl):
        # load all packages that must be delivered together
        # together_packages = [13, 14, 15, 16, 19, 20]
        together_packages = [22, 26, 24, 14, 15, 16, 34, 20, 21, 19, 2, 33, 11, 4, 40, 13]
        for package_id in together_packages:
            package = tl.hash_table.lookup(package_id)
            if package:
                # choosing Truck 1 based on initial sort and time constraints
                tl.trucks[1].load_package(package)
                # add package ID to together-packages list
                tl.together_packages.append(package_id)
                # print(f"Together-packages loaded on truck 1")

    def load_truck_2_packages(self, tl):
        # load packages delayed until 9:05am or 10:20am
        # delayed_packages = [6, 9, 25, 28, 32]
        delayed_packages = [25, 28, 1, 7, 29, 23, 10, 31, 32, 17, 18, 6, 36, 27, 38, 3]
        for package_id in delayed_packages:
            package = tl.hash_table.lookup(package_id)
            if package:
                tl.trucks[2].load_package(package)
                # add package ID to delayed-package list
                tl.delayed_packages.append(package_id)

    def load_remaining_packages(self, tl):

        remaining_packages = [35, 5, 37, 12, 8, 9, 30, 39]

        for package_id in remaining_packages:
            package = tl.hash_table.lookup(package_id)
            if package:
                tl.trucks[3].load_package(package)
                tl.remaining_packages.append(package_id)
