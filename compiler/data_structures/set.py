class Set:
    """
    A set implementation for Vasuki.
    Uses a hash table for O(1) average case operations.
    """
    def __init__(self, capacity=16):
        self.capacity = capacity
        self.size = 0
        self.buckets = [[] for _ in range(capacity)]
        self.load_factor_threshold = 0.75
    
    def _hash(self, key):
        """
        Hash function for the set.
        
        Args:
            key: The key to hash.
            
        Returns:
            The hash value.
        """
        # Simple hash function
        if isinstance(key, int):
            return abs(key) % self.capacity
        elif isinstance(key, float):
            return abs(int(key)) % self.capacity
        elif isinstance(key, str):
            # String hashing using polynomial rolling hash
            h = 0
            for c in key:
                h = (h * 31 + ord(c)) % self.capacity
            return h
        elif isinstance(key, bool):
            return int(key) % self.capacity
        else:
            # For other types, use id as hash
            return id(key) % self.capacity
    
    def _find_entry(self, key):
        """
        Find the entry with the given key in the appropriate bucket.
        
        Args:
            key: The key to find.
            
        Returns:
            A tuple (bucket_index, entry_index) if found, or (bucket_index, -1) if not found.
        """
        bucket_index = self._hash(key)
        bucket = self.buckets[bucket_index]
        
        for i, k in enumerate(bucket):
            if k == key:
                return bucket_index, i
        
        return bucket_index, -1
    
    def _resize(self, new_capacity):
        """
        Resize the hash table when load factor exceeds threshold.
        
        Args:
            new_capacity: The new capacity for the hash table.
        """
        old_buckets = self.buckets
        self.capacity = new_capacity
        self.buckets = [[] for _ in range(new_capacity)]
        self.size = 0
        
        # Rehash all entries
        for bucket in old_buckets:
            for key in bucket:
                self.add(key)
    
    def add(self, key):
        """
        Add a key to the set.
        
        Args:
            key: The key to add.
            
        Returns:
            True if the key was added, False if it was already in the set.
        """
        bucket_index, entry_index = self._find_entry(key)
        
        if entry_index >= 0:
            # Key already exists
            return False
        else:
            # Insert new entry
            self.buckets[bucket_index].append(key)
            self.size += 1
            
            # Check if resize is needed
            if self.size / self.capacity > self.load_factor_threshold:
                self._resize(self.capacity * 2)
            
            return True
    
    def remove(self, key):
        """
        Remove a key from the set.
        
        Args:
            key: The key to remove.
            
        Returns:
            True if the key was removed, False if it was not in the set.
        """
        bucket_index, entry_index = self._find_entry(key)
        
        if entry_index >= 0:
            # Remove the entry
            del self.buckets[bucket_index][entry_index]
            self.size -= 1
            return True
        else:
            return False
    
    def contains(self, key):
        """
        Check if the set contains a key.
        
        Args:
            key: The key to check.
            
        Returns:
            True if the key is in the set, False otherwise.
        """
        _, entry_index = self._find_entry(key)
        return entry_index >= 0
    
    def clear(self):
        """
        Remove all keys from the set.
        """
        self.buckets = [[] for _ in range(self.capacity)]
        self.size = 0
    
    def union(self, other_set):
        """
        Return a new set that is the union of this set and other_set.
        
        Args:
            other_set: Another Set object.
            
        Returns:
            A new Set object containing all elements from both sets.
        """
        result = Set()
        
        # Add all elements from this set
        for bucket in self.buckets:
            for key in bucket:
                result.add(key)
        
        # Add all elements from other set
        for bucket in other_set.buckets:
            for key in bucket:
                result.add(key)
        
        return result
    
    def intersection(self, other_set):
        """
        Return a new set that is the intersection of this set and other_set.
        
        Args:
            other_set: Another Set object.
            
        Returns:
            A new Set object containing elements that are in both sets.
        """
        result = Set()
        
        # Add elements that are in both sets
        for bucket in self.buckets:
            for key in bucket:
                if other_set.contains(key):
                    result.add(key)
        
        return result
    
    def difference(self, other_set):
        """
        Return a new set that is the difference of this set and other_set.
        
        Args:
            other_set: Another Set object.
            
        Returns:
            A new Set object containing elements that are in this set but not in other_set.
        """
        result = Set()
        
        # Add elements that are in this set but not in other_set
        for bucket in self.buckets:
            for key in bucket:
                if not other_set.contains(key):
                    result.add(key)
        
        return result
    
    def is_subset(self, other_set):
        """
        Check if this set is a subset of other_set.
        
        Args:
            other_set: Another Set object.
            
        Returns:
            True if this set is a subset of other_set, False otherwise.
        """
        # Check if all elements in this set are also in other_set
        for bucket in self.buckets:
            for key in bucket:
                if not other_set.contains(key):
                    return False
        
        return True
    
    def is_superset(self, other_set):
        """
        Check if this set is a superset of other_set.
        
        Args:
            other_set: Another Set object.
            
        Returns:
            True if this set is a superset of other_set, False otherwise.
        """
        return other_set.is_subset(self)
    
    def to_list(self):
        """
        Convert the set to a list.
        
        Returns:
            A list containing all elements in the set.
        """
        result = []
        for bucket in self.buckets:
            for key in bucket:
                result.append(key)
        return result
    
    def __len__(self):
        """
        Return the number of elements in the set.
        
        Returns:
            The number of elements in the set.
        """
        return self.size
    
    def __str__(self):
        """
        Return a string representation of the set.
        
        Returns:
            A string representation of the set.
        """
        elements = []
        for bucket in self.buckets:
            for key in bucket:
                elements.append(repr(key))
        return "{" + ", ".join(elements) + "}"
