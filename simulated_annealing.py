# simulated_annealing.py

import math
import random


class SimulatedAnnealing:
    # def __init__(self, distance_matrix, init_temp, alpha, address_to_index):
    #     # values defined in def main()
    #     self.distance_matrix = distance_matrix
    #     self.init_temp = init_temp
    #     self.alpha = alpha  # cooling rate
    #     self.address_to_index = address_to_index

    def __init__(self, find_distance_between, distance_matrix, address_list, init_temp, alpha):
        # values defined in def main()
        self.find_distance_between = find_distance_between
        self.distance_matrix = distance_matrix
        self.address_list = address_list
        self.init_temp = init_temp
        self.alpha = alpha  # cooling rate

    # find the distance of a complete route
    def calculate_route_distance(self, route):
        total_distance = 0
        total_mileage = 0

        # loop through all packages in the route, find distance between each index to the next
        for i in range(len(route) - 1):
            current_address = route[i].address
            next_address = route[i + 1].address

            distance = self.find_distance_between(current_address, next_address, self.address_list)
            total_distance += distance

        # distance from last package back to first
        # next_address = route[-1].address
        # current_address = route[0].address
        # distance = self.find_distance_between(next_address, current_address, self.address_list)
        # total_distance += distance

        # adjust total distance based on truck speed (18 mph)
        total_mileage = total_distance / 18.0
        return total_mileage

    # find distance of a given route for each truck
    # def calculate_route_distance(self, route):
    #     total_distance = 0
    #     for i in range(len(route) - 1):
    #         # get the addresses of the current and next package
    #         current_address = self.address_to_index[route[i].address]
    #         next_address = self.address_to_index[route[i + 1].address]
    #         print(f"Distance from {route[i].address} to {route[i + 1].address}: {total_distance}")
    #
    #         # add the distance between the two points to the total distance
    #         total_distance += self.distance_matrix[current_address][next_address]
    #
    #     # *************************************************************************
    #     #   CHECK IF NECESSARY TO GET DISTANCE OF LAST PACKAGE BACK TO HUB
    #     # *************************************************************************
    #     # add distance from last package back to first package
    #     current_address = self.address_to_index[route[-1].address]
    #     next_address = self.address_to_index[route[0].address]
    #     total_distance += self.distance_matrix[current_address][next_address]
    #
    #     # print(f"Total distance for route: {total_distance}")
    #     total_mileage = total_distance / 18.0
    #     # print(f"\nTotal mileage for route: {total_mileage}\n")
    #
    #     return total_mileage

    # neighbor solution: swaps the delivery order of two packages
    def swap_two_packages(self, route):
        new_route = route[:]  # create copy of current route
        # ensure the sample will have at least two routes
        if len(route) < 2:
            return route
        pkg_1, pkg_2 = random.sample(range(len(route)), 2)  # randomly choose two packages
        # swap delivery order of two packages
        new_route[pkg_1], new_route[pkg_2] = new_route[pkg_2], new_route[pkg_1]

        return new_route

    # neighbor solution: remove a package from current position and set at a new position (different from swapping)
    # def insert_package(self, route):
    #     new_route = route[:]  # create copy of current route
    #     if len(route > 3):
    #         return route
    #
    #     pkg_1, pkg_2 = random.sample(range(len(route)), 2)
    #     package.new_route.pop(pkg_1)

    # neighbor solution: swap two packages between trucks
    # def swap_between_trucks(self, current_solution):
    #     # make a copy of the current solution
    #     new_solution = current_solution[:]
    #
    #     # randomly select two different trucks
    #     truck1, truck2 = random.sample(new_solution.trucks.values(), 2)
    #
    #     # randomly select one package from each truck
    #     if truck1.package_list and truck2.package_list:
    #         package1 = random.choice(truck1.package_list)
    #         package2 = random.choice(truck2.package_list)
    #
    #         # swap the packages between the two trucks
    #         truck1.package_list.remove(package1)
    #         truck2.package_list.remove(package2)
    #
    #         truck1.package_list.append(package2)
    #         truck2.package_list.append(package1)
    #
    #         # recalculate the total mileage for each truck after the swap
    #         truck1.total_mileage = self.calculate_route_distance(truck1.total_mileage)

    # define a small probability of acceptance for non-optimal solutions
    def acceptance_probability(self, old_cost, new_cost, temp):
        if new_cost < old_cost:
            return 1.0
        # find probability of accepting the new solution based on the cost
        return math.exp((old_cost - new_cost) / temp)

    # reduce scope of search for next point by slightly lowering the temperature
    def cooling_schedule(self, temp, iteration):
        # cools off each time a better solution is found
        return temp * (self.alpha ** iteration)

    # optimize given route with simulated annealing algorithm
    def simulated_annealing(self, truck_routes, stop_temp=1):
        optimized_routes = {}  # initialize list of routes that will be used when processing deliveries

        # iterate through initial route by truck ID
        for truck_id, route in truck_routes.items():
            curr_solution = route[:]  # make a copy of the current route for comparison
            # find the "cost" in distance/time of the current solution
            curr_cost = self.calculate_route_distance(curr_solution)
            temp = self.init_temp
            iteration = 0

            # curr_solution = trucks
            # curr_cost = self.calculate_route_distance(trucks)
            # temp = self.init_temp
            # iteration = 0

            while temp > stop_temp:
                # call the neighbor solution and set to new solution for comparison
                new_solution = self.swap_two_packages(curr_solution)
                # find the "cost" in distance/time of the new solution
                new_cost = self.calculate_route_distance(new_solution)

                # define acceptance probabilities for each possible solution based on the cost
                # the new solution will always be accepted, just with a lower probability
                if self.acceptance_probability(curr_cost, new_cost, temp) > random.random():
                    curr_cost = new_cost
                    curr_solution = new_solution

                # reduce the temperature
                temp = self.cooling_schedule(temp, iteration)
                iteration += 1

            # return these routes to be processed and delivered now that they have been optimized
            optimized_routes[truck_id] = curr_solution

            print(f"Optimized route for Truck: {truck_id}: {curr_solution}")

        return optimized_routes
