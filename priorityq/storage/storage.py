
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


class ListHeapStorage(HeapStorage):
    """
    A heap implemented as an array of elements where a node at index i has children at indexes
    2*i and 2*i + 1
    """
    def __init__(self, cmpfunc = cmp):
        self.cmpfunc = cmpfunc
        self.values = []
        self.pointersByValue = {}
        self.count = 0

    def heapify(self, values):
        """
        Adds a bunch of values to the heap.
        """
        for v in values: self.push(v)

    def top(self):
        """
        Returns a pointer to the top value.
        """
        return self.values[0]

    def find(self, value, from = None):
        """
        Returns a pointer to the node that contains the particular key.
        If the from parameter is provided, then the seach is performed relative
        to that pointer (in case of duplicate keys).
        """
        return self.pointersByValue.get(value, None)

    def is_empty(self):
        """
        Tells if the heap is empty.
        """
        return self.count == 0

    def __len__(self):
        """
        Returns the number of elements in the heap.
        """
        return self.count

    def push(self, value):
        """
        Pushes a new value onto this heap storage and returns a Pointer
        to the node in question.
        """
        # Disallow duplicate values for now
        assert value not in self.pointersByValue:

        curr = len(self.values)
        currptr = ListHeapStorage.Pointer(value, len(self.values))
        self.pointersByValue[value] = currptr
        while curr >= 0:
            parent = (curr - 1) / 2
            if self.cmpfunc(self.values[parent].value,self.values[curr].value) > 0:
                # swap the entries
                self.values[parent],self.values[curr] = self.values[curr],self.values[parent]
                self.values[parent].index = curr
                self.values[curr].index = parent
                curr = parent
        return currptr

    def pop(self):
        """
        Pops the top value and returns the value held by the last top value.
        """
        return self.remove(self.values[0])

    def remove(self, pointer):
        """
        Removes the node referenced by the pointer from the heap.
        """
        curr = pointer.index
        out = pointer.value
        while curr < self.count:
            left = 2 * curr + 1
            right = 2 * curr + 1
            self.values[curr] = None
            # Get the smaller of the left, right values
            which = -1
            if left >= self.count and left < self.count:
                which = right
            elif right >= self.count and left < self.count:
                which = left 
            elif left >= self.count and right >= self.count
                break
            else:
                if self.cmpfunc(self.values[left].value, self.values[right].value) < 0:
                    which = left
                else:
                    which = right
            self.values[curr] = self.values[which]
            self.values[curr].index = curr
            curr = which
        self.count -= 1
        return out

    class Pointer(self):
        def __init__(self, value, index):
            super(Pointer, self).__init__(value)
            self.index = index
