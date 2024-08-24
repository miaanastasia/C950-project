# hash_table.py
# references WGU Let's Go Hashing Webinar code

class HashTable:

    # constructor with initial capacity parameter
    # assigns all buckets with an empty list
    def __init__(self, initial_capacity=80):
        # initialize hash table with empty bucket list entries
        self.list = []
        for i in range(initial_capacity):
            self.list.append([])

    # define hash function for package placement
    # used for testing purposes only
    def _hash_function(self, key):
        return int(key) % len(self.list)

    def insert(self, key, item):
        # find the bucket where the item will be inserted
        bucket = hash(key) % len(self.list)
        bucket_list = self.list[bucket]

        # check if key exists and update item if it does
        for kv in bucket_list:
            if kv[0] == key:
                kv[1] = item
                return True

        # if key doesn't exist, add a new item
        key_value = (key, item)
        bucket_list.append(key_value)
        return True

    def lookup(self, key):
        # find the bucket where the key would be
        bucket_index = hash(key) % len(self.list)
        bucket_list = self.list[bucket_index]

        # print(f"Looking up key {key} in bucket {bucket_index} (bucket contains {len(bucket_list)} items)")

        for pair in bucket_list:
            # print(f"Checking key {pair} against {key}")
            if key == pair[0]:
                # print(f"Found package {key} in bucket {bucket_index}")
                return pair[1]

        # print(f"Package {key} not found in bucket {bucket_index}")
        return None  # if key not found

    def remove(self, key):
        # find the bucket where the item will be removed
        bucket = hash(key) % len(self.list)
        bucket_list = self.list[bucket]

        for kv in bucket_list:
            if kv[0] == key:
                bucket_list.remove(kv)
                return True
        return False

    # retrieve all packages stored in the hash table
    # will be used when calling the greedy algorithm
    def get_all_packages(self):
        all_packages = []
        for bucket in self.list:
            if bucket:
                for key, package in bucket:
                    all_packages.append(package)
        return all_packages
