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
        # all delayed packages except 9 loaded on Truck 2.  truck leaves from hub at 09:05am
        self.delayed_packages = [6, 25, 28, 32, 3, 18, 36, 38]
        # self.remaining_packages = [35, 5, 37, 12, 8, 9, 30, 39]

        self.wrong_address = [9]

    def load_truck_1_packages(self, tl):
        # load all packages that must be delivered together
        # together_packages = [13, 14, 15, 16, 19, 20]
        # together_packages = [22, 26, 24, 14, 15, 16, 34, 20, 21, 19, 2, 33, 11, 4, 40, 13]

        truck_1_packages = [13, 14, 15, 16, 19, 20, 1, 29, 30, 31, 34, 37, 40]
        # all packages that either must be delivered together or have a 10:30 delivery deadline
        for package_id in truck_1_packages:
            package = tl.hash_table.lookup(package_id)
            if package:
                # choosing Truck 1 based on initial sort and time constraints
                tl.trucks[1].load_package(package)
                # add package ID to together-packages list
                tl.together_packages.append(package_id)
                # print(f"Together-packages loaded on truck 1")

    def load_truck_2_packages(self, tl):

        delayed_packages = [3, 6, 18, 25, 28, 32, 36, 38]
        # handling #25 separately in main bc of late delivery

        for package_id in delayed_packages:
            package = tl.hash_table.lookup(package_id)
            if package:
                tl.trucks[2].load_package(package)
                # add package ID to delayed-package list
                tl.delayed_packages.append(package_id)


    def load_remaining_packages(self, tl):
        wrong_address = [9]

        # load only package 9 onto truck 3 based on 10:20 a.m. delay with wrong address
        for package_id in wrong_address:
            package = tl.hash_table.lookup(package_id)
            if package:
                tl.trucks[3].load_package(package)
                tl.wrong_address.append(package_id)

        # load any packages not in the pre-defined sets on either truck 2 or 3 depending on capacity
        remaining_packages = [pkg_id for pkg_id in range(1, 41)
                              if pkg_id not in tl.together_packages and
                              pkg_id not in tl.delayed_packages and
                              pkg_id not in tl.wrong_address]

        for package_id in remaining_packages:
            package = tl.hash_table.lookup(package_id)
            if package:
                # load onto either truck 2 or 3 based on balance
                least_loaded_truck = min([tl.trucks[2], tl.trucks[3]], key=lambda truck: len(truck.package_list))
                least_loaded_truck.load_package(package)


