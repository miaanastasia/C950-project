# simulated_annealing.py

import math
import random


class SimulatedAnnealing:
    def __init__(self, distance_matrix, init_temp, alpha, address_to_index):
        self.distance_matrix = distance_matrix
        self.init_temp = init_temp
        self.alpha = alpha  # cooling rate
        self.address_to_index = address_to_index

    # find distance of a given route
    def calculate_route_distance(self, route):
        total_distance = 0
        for i in range(len(route) - 1):
            # get the addresses of the current and next package
            current_address = self.address_to_index[route[i].address]
            next_address = self.address_to_index[route[i + 1].address]

            # add the distance between the two points to the total distance
            total_distance += self.distance_matrix[current_address][next_address]

        # add distance from last package back to first package
        current_address = self.address_to_index[route[-1].address]
        next_address = self.address_to_index[route[0].address]
        total_distance += self.distance_matrix[current_address][next_address]
        print(f"Total distance for route: {total_distance}")

        return total_distance

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

    # define a small probability of acceptance for non-optimal solutions
    def acceptance_probability(self, old_cost, new_cost, temp):
        if new_cost < old_cost:
            return 1.0
        return math.exp((old_cost - new_cost) / temp)

    # reduce scope of search for next point by slightly lowering the temperature
    def cooling_schedule(self, temp, iteration):
        return temp * (self.alpha ** iteration)

    # optimize given route with simulated annealing algorithm
    def optimize_route(self, trucks, stop_temp=1):
        curr_solution = trucks
        curr_cost = self.calculate_route_distance(trucks)
        temp = self.init_temp
        iteration = 0

        while temp > stop_temp:
            # call the neighbor solution and set to new solution for comparison
            new_solution = self.swap_two_packages(curr_solution)
            # find the cost (distance) of the new solution
            new_cost = self.calculate_route_distance(new_solution)

            if self.acceptance_probability(curr_cost, new_cost, temp) > random.random():
                curr_cost = new_cost
                curr_solution = new_solution

            # reduce the temperature
            temp = self.cooling_schedule(temp, iteration)
            iteration += 1

        return curr_solution
