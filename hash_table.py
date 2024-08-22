# hash_table.py
# references WGU Let's Go Hashing Webinar code

class HashTable:

    # constructor with initial capacity parameter
    # assigns all buckets with an empty list
    def __init__(self, initial_capacity=40):
        # initialize hash table with empty bucket list entries
        self.table = []
        for i in range(initial_capacity):
            self.table.append([])

    def insert(self, key, item):
        # find the bucket where the item will be inserted
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        # check if key exists and update item if it does
        for kv in bucket_list:
            if kv[0] == key:
                kv[1] = item
                return True

        # if key doesn't exist, add a new item
        bucket_list.append([key, item])
        return True

    def lookup(self, key):
        # find the bucket where the key would be
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        for kv in bucket_list:
            if kv[0] == key:
                return kv[1]
            return None

    def remove(self, key):
        # find the bucket where the item will be removed
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        for kv in bucket_list:
            if kv[0] == key:
                bucket_list.remove(kv)
                return True
        return False

    # retrieve all packages stored in the hash table
    # will be used when calling the greedy algorithm
    def get_all_packages(self):
        all_packages = []
        for bucket in self.table:
            if bucket:
                for key, package in bucket:
                    all_packages.append(package)
        return all_packages
