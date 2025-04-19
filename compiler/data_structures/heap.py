class MinHeap:
    """
    A min-heap implementation for Vasuki's priority queue.
    """
    def __init__(self):
        self.heap = []
        self.size = 0
    
    def parent(self, i):
        """Return the index of the parent of the node at index i."""
        return (i - 1) // 2
    
    def left_child(self, i):
        """Return the index of the left child of the node at index i."""
        return 2 * i + 1
    
    def right_child(self, i):
        """Return the index of the right child of the node at index i."""
        return 2 * i + 2
    
    def has_parent(self, i):
        """Return True if the node at index i has a parent."""
        return self.parent(i) >= 0
    
    def has_left_child(self, i):
        """Return True if the node at index i has a left child."""
        return self.left_child(i) < self.size
    
    def has_right_child(self, i):
        """Return True if the node at index i has a right child."""
        return self.right_child(i) < self.size
    
    def get_parent(self, i):
        """Return the value of the parent of the node at index i."""
        return self.heap[self.parent(i)]
    
    def get_left_child(self, i):
        """Return the value of the left child of the node at index i."""
        return self.heap[self.left_child(i)]
    
    def get_right_child(self, i):
        """Return the value of the right child of the node at index i."""
        return self.heap[self.right_child(i)]
    
    def swap(self, i, j):
        """Swap the values at indices i and j."""
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]
    
    def peek(self):
        """Return the minimum value in the heap without removing it."""
        if self.size == 0:
            return None
        return self.heap[0]
    
    def poll(self):
        """Remove and return the minimum value in the heap."""
        if self.size == 0:
            return None
        
        item = self.heap[0]
        self.heap[0] = self.heap[self.size - 1]
        self.size -= 1
        self.heap.pop()
        self.heapify_down()
        return item
    
    def add(self, item):
        """Add an item to the heap."""
        self.heap.append(item)
        self.size += 1
        self.heapify_up()
    
    def heapify_up(self):
        """Restore the heap property by moving a value up the tree."""
        index = self.size - 1
        while (self.has_parent(index) and 
               self.get_parent(index) > self.heap[index]):
            parent_index = self.parent(index)
            self.swap(parent_index, index)
            index = parent_index
    
    def heapify_down(self):
        """Restore the heap property by moving a value down the tree."""
        index = 0
        while self.has_left_child(index):
            smaller_child_index = self.left_child(index)
            if (self.has_right_child(index) and 
                self.get_right_child(index) < self.get_left_child(index)):
                smaller_child_index = self.right_child(index)
            
            if self.heap[index] < self.heap[smaller_child_index]:
                break
            else:
                self.swap(index, smaller_child_index)
            
            index = smaller_child_index
    
    def is_empty(self):
        """Return True if the heap is empty."""
        return self.size == 0
    
    def __len__(self):
        """Return the number of items in the heap."""
        return self.size
    
    def __str__(self):
        """Return a string representation of the heap."""
        return str(self.heap[:self.size])


class MaxHeap:
    """
    A max-heap implementation for Vasuki's priority queue.
    """
    def __init__(self):
        self.heap = []
        self.size = 0
    
    def parent(self, i):
        """Return the index of the parent of the node at index i."""
        return (i - 1) // 2
    
    def left_child(self, i):
        """Return the index of the left child of the node at index i."""
        return 2 * i + 1
    
    def right_child(self, i):
        """Return the index of the right child of the node at index i."""
        return 2 * i + 2
    
    def has_parent(self, i):
        """Return True if the node at index i has a parent."""
        return self.parent(i) >= 0
    
    def has_left_child(self, i):
        """Return True if the node at index i has a left child."""
        return self.left_child(i) < self.size
    
    def has_right_child(self, i):
        """Return True if the node at index i has a right child."""
        return self.right_child(i) < self.size
    
    def get_parent(self, i):
        """Return the value of the parent of the node at index i."""
        return self.heap[self.parent(i)]
    
    def get_left_child(self, i):
        """Return the value of the left child of the node at index i."""
        return self.heap[self.left_child(i)]
    
    def get_right_child(self, i):
        """Return the value of the right child of the node at index i."""
        return self.heap[self.right_child(i)]
    
    def swap(self, i, j):
        """Swap the values at indices i and j."""
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]
    
    def peek(self):
        """Return the maximum value in the heap without removing it."""
        if self.size == 0:
            return None
        return self.heap[0]
    
    def poll(self):
        """Remove and return the maximum value in the heap."""
        if self.size == 0:
            return None
        
        item = self.heap[0]
        self.heap[0] = self.heap[self.size - 1]
        self.size -= 1
        self.heap.pop()
        self.heapify_down()
        return item
    
    def add(self, item):
        """Add an item to the heap."""
        self.heap.append(item)
        self.size += 1
        self.heapify_up()
    
    def heapify_up(self):
        """Restore the heap property by moving a value up the tree."""
        index = self.size - 1
        while (self.has_parent(index) and 
               self.get_parent(index) < self.heap[index]):
            parent_index = self.parent(index)
            self.swap(parent_index, index)
            index = parent_index
    
    def heapify_down(self):
        """Restore the heap property by moving a value down the tree."""
        index = 0
        while self.has_left_child(index):
            larger_child_index = self.left_child(index)
            if (self.has_right_child(index) and 
                self.get_right_child(index) > self.get_left_child(index)):
                larger_child_index = self.right_child(index)
            
            if self.heap[index] > self.heap[larger_child_index]:
                break
            else:
                self.swap(index, larger_child_index)
            
            index = larger_child_index
    
    def is_empty(self):
        """Return True if the heap is empty."""
        return self.size == 0
    
    def __len__(self):
        """Return the number of items in the heap."""
        return self.size
    
    def __str__(self):
        """Return a string representation of the heap."""
        return str(self.heap[:self.size])


class PriorityQueue:
    """
    A priority queue implementation using a min-heap.
    """
    def __init__(self, is_min=True):
        """
        Initialize a priority queue.
        
        Args:
            is_min: If True, create a min-priority queue. If False, create a max-priority queue.
        """
        if is_min:
            self.heap = MinHeap()
        else:
            self.heap = MaxHeap()
    
    def enqueue(self, item):
        """Add an item to the priority queue."""
        self.heap.add(item)
    
    def dequeue(self):
        """Remove and return the highest-priority item from the queue."""
        return self.heap.poll()
    
    def peek(self):
        """Return the highest-priority item without removing it."""
        return self.heap.peek()
    
    def is_empty(self):
        """Return True if the queue is empty."""
        return self.heap.is_empty()
    
    def size(self):
        """Return the number of items in the queue."""
        return len(self.heap)
    
    def __str__(self):
        """Return a string representation of the queue."""
        return str(self.heap)
