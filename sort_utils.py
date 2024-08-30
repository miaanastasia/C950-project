# sort_utils.py

from main import find_distance_between


# These functions were used only for testing.  Initial simple sort by deadline showed which packages had priority,
#   then two quick sorts before loading and after loading showed which packages were closest.

# ********************************************************************************************
#                       SORT FUNCTIONS FOR TESTING PURPOSES ONLY
# ********************************************************************************************


# # simple sort packages by earliest deadline
# def sort_by_deadline(packages):
#     # sort through packages in hash table using deadline as the key
#     return sorted(packages, key=lambda p: p.deadline)


# quicksort package list before loading packages
# citing StackOverflow as reference https://stackoverflow.com/questions/18262306/quicksort-with-python
def sort_before_loading(packages, start_address, address_list):
    # keeps return value in bounds if there is only one element in the array
    if len(packages) <= 1:
        return packages

    pivot = packages[0]
    pivot_distance = find_distance_between(start_address, pivot.address, address_list)

    # find distance in miles between hub and next package address, compare to pivot distance
    less = \
        [pkg for pkg in packages if find_distance_between(start_address, pkg.address, address_list) < pivot_distance]
    equal = \
        [pkg for pkg in packages if find_distance_between(start_address, pkg.address, address_list) == pivot_distance]
    greater = \
        [pkg for pkg in packages if find_distance_between(start_address, pkg.address, address_list) > pivot_distance]

    return (sort_before_loading(less, start_address, address_list) + equal +
            sort_before_loading(greater, start_address, address_list))


# quicksort package list after loading packages but before deliveries are made
# citing StackOverflow as reference https://stackoverflow.com/questions/18262306/quicksort-with-python
def sort_after_loading(packages, start_address, address_list):
    # keeps return value in bounds if there is only one element in the array
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
    return (sort_after_loading(less, start_address, address_list) + equal +
            sort_after_loading(greater, start_address, address_list))
