
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
    """Base class of all storage strategies that can back a priority queue.

        **Implementations**

        ``priorityq.storage.binheap.Storage``
        ``priorityq.storage.binaryheap.Storage``
    """
    def __init__(self, cmpfunc = cmp):
        self._cmpfunc = cmpfunc

    def clear(self):
        """Removes all elements from the heap."""
        pass

    def all_handles(self):
        """Returns a list of all the values in the heap."""
        return []

    def adjust(self, handle):
        """ Called to move a particular value to the correct position in the heap after it has been modified."""

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

    def heapify(self, values):
        """Heapifies a collection of values onto this heap.

        **Parameters**

        values  -   The iteratable of values that are to be added.

        **Returns**

        A list of handles for the values that were actually added onto the heap.
        """
        return map(self.push, values)

    def __len__(self):
        """Returns the number of elements in the heap."""
        return 0

    def __iter__(self):
        for h in self.all_handles(): yield h

    @property
    def comparator(self):
        """Returns the comparator currently used to prioritize the elements in this heap."""
        return self._cmpfunc

    @comparator.setter
    def comparator(self, cmpfunc):
        """Setter for the comparator."""
        self._cmpfunc = cmpfunc
        self._comparator_changed()

    def _comparator_changed(self):
        """Method invoked when the comparator has been modified and values in the heap need to be reprioritized.  Default behaviour is to simply make a copy of all the values, clear the heap and re-insert them"""
        handles = self.all_handles()
        self.clear()
        for h in handles:
            self.push(h.value)
