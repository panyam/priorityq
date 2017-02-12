
class Pointer(object):
    """
    Base class of all reference/pointers to actual values contained
    in the internal nodes of a PQ.  Specific implementations of priority
    queues/heaps would inherit from this and return these pointer values
    which can also be passed back to a queue.
    """
    def __init__(self, value):
        self._value = value

    @property
    def value(self): return self._value

class HeapStorage(object):
    def heapify(self, values):
        """
        Adds a bunch of values to the heap.
        """
        pass

    def push(self, value):
        """
        Pushes a new value onto this heap storage and returns a Pointer
        to the node in question.
        """
        return None

    def top(self):
        """
        Returns a pointer to the top value.
        """
        return None

    def pop(self):
        """
        Pops the top value and returns the value held by the last top value.
        """
        return None

    def find(self, value, from = None):
        """
        Returns a pointer to the node that contains the particular key.
        If the from parameter is provided, then the seach is performed relative
        to that pointer (in case of duplicate keys).
        """
        return None

    def remove(self, pointer):
        """
        Removes the node referenced by the pointer from the heap.
        """
        pass

    def is_empty(self):
        """
        Tells if the heap is empty.
        """
        return False

    def __len__(self):
        """
        Returns the number of elements in the heap.
        """
        return 0


