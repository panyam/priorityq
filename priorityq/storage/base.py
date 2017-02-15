
class Handle(object):
    """
    Base class of all opaque reference/handles to actual values contained
    in the internal nodes of a PQ.  Specific implementations of priority
    queues/heaps would inherit from this and return these handle values
    which can also be passed back to a queue.
    """
    def __init__(self, value):
        self._value = value

    @property
    def value(self): 
        """Returns the value pointed by the handle."""
        return self._value

class Storage(object):
    """Base class of all storage strategies that can back a priority queue."""
    def __iter__(self):
        return []

    def heapify(self, values):
        """Heapifies a collection of values onto this heap.

        **Parameters**

        values  -   The iteratable of values that are to be added.

        **Returns**

        A list of handles for the values that were actually added onto the heap.

        **Implementations**

        ``priorityqueue.storage.binheap.Storage``
        """
        pass

    def push(self, value):
        """Pushes a new value onto the storage.

        Returns an implementation specific opaque handle to the value within the heap.
        """
        return None

    @property
    def top(self):
        """Returns a handle to the top value on the heap."""
        return None

    def pop(self):
        """Pops the top value from the stack and returns a handle to it."""
        return None

    def find(self, value):
        """Returns a handle to the given value in the heap. """
        return None

    def remove(self, handle):
        """Remove a value that is referenced by a particular handle from the heap."""
        pass

    @property
    def is_empty(self):
        """Return True if the heap is empty, false otherwise."""
        return False

    def __len__(self):
        """Returns the number of elements in the heap."""
        return 0


