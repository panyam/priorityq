
class Handle(object):
    """
    Base class of all reference/handles to actual values contained
    in the internal nodes of a PQ.  Specific implementations of priority
    queues/heaps would inherit from this and return these handle values
    which can also be passed back to a queue.
    """
    def __init__(self, value):
        self._value = value

    @property
    def value(self): return self._value

class Storage(object):
    def __iter__(self):
        return []

    def heapify(self, values):
        """
        Adds a bunch of values to the heap.
        """
        pass

    def set_comparator(self, cmpfunc):
        """
        Set's the comparator function and re-heapifies the elements
        currently stored.  Note that this does not invalidate any 
        handles that are maintained for the elements in this storage.
        """
        pass

    def push(self, value):
        """
        Pushes a new value onto this heap storage and returns a Handle
        to the node in question.
        """
        return None

    @property
    def top(self):
        """
        Returns a handle to the top value.
        """
        return None

    def pop(self):
        """
        Pops the top value and returns the value held by the last top value.
        """
        return None

    def find(self, value):
        """
        Returns a handle to the node that contains the particular key.
        If the from parameter is provided, then the seach is performed relative
        to that handle (in case of duplicate keys).
        """
        return None

    def remove(self, handle):
        """
        Removes the node referenced by the handle from the heap.
        """
        pass

    @property
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


