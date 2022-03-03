# class HashTable holds the info for all packages.
class HashTable:
    # initial function called when HashTable is created. it sets the table as a list containing 10 empty lists.
    def __init__(self, default_range=10):
        self.table = []
        for i in range(default_range):
            self.table.append([])

    # function insert receives the package ID and the package object.
    def insert(self, ID, values):
        # first finds the right bucket using a hash algorithm.
        bucket = hash(ID) % len(self.table)
        bucket_list = self.table[bucket]

        # update value if key is found.
        for kv in bucket_list:
            if kv[0] == ID:
                kv[1] = values
                return True
        # add package to proper bucket.
        key_value = [ID, values]
        bucket_list.append(key_value)
        return True

    # function search receives the package ID.
    def search(self, ID):
        # It first finds the proper bucket using a hash algorithm.
        bucket = hash(ID) % len(self.table)
        bucket_list = self.table[bucket]
        # returns the package object if found. Returns none if not found.
        for kv in bucket_list:
            if kv[0] == ID:
                return kv[1]
        return None

    # function remove receives the package ID.
    def remove(self, ID):
        # It first finds the proper bucket using a hash algorithm.
        bucket = hash(ID) % len(self.table)
        bucket_list = self.table[bucket]
        # then removes the package ID and its package object if found.
        for kv in bucket_list:
            if kv[0] == ID:
                bucket_list.remove([kv[0], kv[1]])
