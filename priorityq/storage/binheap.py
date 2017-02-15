
from base import Handle as BaseHandle
from base import Storage as BaseStorage

class Storage(BaseStorage):
    """
    A heap implemented as an array of elements where a node at index 
    i has children at indexes 2*i+1 and 2*i+2
    """
    def __init__(self, cmpfunc = cmp):
        self._values = []
        self._cmpfunc = cmpfunc
        self.comparator = cmpfunc

    @property
    def comparator(self):
        return self._cmpfunc

    @comparator.setter
    def comparator(self, cmpfunc):
        self._cmpfunc = cmpfunc
        self._count = 0
        old_values = self._values
        self._values = []
        for v in old_values:
            if v:
                self.push_handle(v)

    def heapify(self, values):
        """
        Adds a bunch of values to the heap.
        Returns the handles to all the values inserted
        """
        return map(self.push, values)

    @property
    def top(self):
        """
        Returns a handle to the top value.
        """
        return self._values[0]

    @property
    def is_empty(self):
        """
        Tells if the heap is empty.
        """
        return self._count == 0

    def __iter__(self):
        """
        Iterates through the values yielding them in order of priority.
        """
        out = self._values[:]
        out.sort(cmp = self._cmpfunc)
        for handle in out: yield handle.value

    def __len__(self):
        """
        Returns the number of elements in the heap.
        """
        return self._count

    def push(self, value):
        """
        Pushes a new value onto this heap storage and returns a Handle
        to the node in question.
        """
        currptr = Storage.Handle(value, 0)
        self._push_handle(currptr)
        return currptr

    def _push_handle(self, handle):
        """
        Pushes a handle that does not exist onto the heap.
        This method is called from the push (or set_comparator)
        methods.
        """
        curr = len(self._values)
        if self._count >= curr:
            handle.index = curr
            # we are saturated so add to end and upheap
            self._values.append(handle)
        else:
            # find the first spot and upheap from there
            for i,n in enumerate(self._values):
                if n is None:
                    handle.index = i
                    self._values[i] = handle
                    break
        self._count += 1
        
        # So handle is at a given point, so upheap from there
        self._values[self._upheap(handle.index)]

    def pop(self):
        """
        Pops the top value and returns the value held by the last top value.
        """
        return self.remove(self._values[0])

    def reheap(self, handle):
        """
        Called when the value pointed by the handle has been updated so a 
        possible reheaping is required.
        """
        # Try moving it up heap if required
        curr = handle.index
        if self._upheap(curr) == curr:
            # nothing happened, then try down heaping it
            size = len(self._values)
            curr = handle.index
            while curr < size:
                left = 2 * curr + 1
                right = 2 * curr + 2
                leftPtr = None if left >= size else self._values[left]
                rightPtr = None if right >= size else self._values[right]
                if not leftPtr and not rightPtr: 
                    # we are in the right spot
                    return

                smaller = -1
                if not leftPtr and rightPtr:
                    smaller = right
                elif not rightPtr and leftPtr:
                    smaller = left 
                elif self._cmpfunc(leftPtr.value, rightPtr.value) < 0:
                    smaller = left
                else:
                    smaller = right

                # See we are smaller than the "smaller" child, if not, swap with it
                if self._cmpfunc(handle.value, self._values[smaller].value) < 0:
                    # We are smaller than the smaller child so we are in right spot
                    return

                # otherwise swap
                self._values[curr] = self._values[smaller]
                self._values[curr].index = curr
                self._values[smaller] = handle
                self._values[smaller].index = smaller
                curr = smaller
            return handle
        
    def remove(self, handle):
        """
        Removes the node referenced by the handle from the heap.
        """
        size = len(self._values)
        curr = handle.index
        while curr < size:
            left = 2 * curr + 1
            right = 2 * curr + 2
            leftPtr = None if left >= size else self._values[left]
            rightPtr = None if right >= size else self._values[right]
            # self._values[curr] = None
            which = -1
            if not leftPtr and rightPtr:
                which = right
            elif not rightPtr and leftPtr:
                which = left 
            elif not leftPtr and not rightPtr:
                break
            else:
                if self._cmpfunc(leftPtr.value, rightPtr.value) < 0:
                    which = left
                else:
                    which = right
            self._values[curr] = self._values[which]
            self._values[curr].index = curr
            self._values[which] = handle
            self._values[which].index = which
            curr = which
        self._count -= 1
        self._values[handle.index] = None
        return handle

    def _upheap(self, curr):
        while curr > 0:
            parent = (curr - 1) / 2
            if self._cmpfunc(self._values[parent].value,self._values[curr].value) <= 0:
                break
            # swap the entries
            self._values[parent].index = curr
            self._values[curr].index = parent
            self._values[parent],self._values[curr] = self._values[curr],self._values[parent]
            curr = parent
        return curr

    class Handle(BaseHandle):
        def __init__(self, value, index):
            super(Storage.Handle, self).__init__(value)
            self.index = index

        def __repr__(self): return str(self)
        def __str__(self):
            return "<Ptr (0x%x), Index: %d, Value: %s>" % (id(self), self.index, str(self.value))

        def __cmp__(self, another):
            return cmp(self.value, another.value)
