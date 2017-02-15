
from base import Handle as BaseHandle
from base import Storage as BaseStorage

class Storage(BaseStorage):
    """
    A heap implemented as an array of elements where a node at index 
    i has children at indexes 2*i+1 and 2*i+2
    """
    def __init__(self, cmpfunc = cmp):
        self.values = []
        self.set_comparator(cmpfunc)

    def set_comparator(self, cmpfunc):
        self.cmpfunc = cmpfunc
        old_values = self.values
        self.count = 0
        self.values = []
        for v in old_values:
            if v:
                self.push_handle(v)

    def heapify(self, values):
        """
        Adds a bunch of values to the heap.
        """
        for v in values: self.push(v)

    @property
    def top(self):
        """
        Returns a handle to the top value.
        """
        return self.values[0]

    @property
    def is_empty(self):
        """
        Tells if the heap is empty.
        """
        return self.count == 0

    def __iter__(self):
        """
        Iterates through the values yielding them in order of priority.
        """
        out = self.values[:]
        out.sort(cmp = self.cmpfunc)
        for handle in out: yield handle.value

    def __len__(self):
        """
        Returns the number of elements in the heap.
        """
        return self.count

    def push(self, value):
        """
        Pushes a new value onto this heap storage and returns a Handle
        to the node in question.
        """
        # Disallow duplicate values for now
        currptr = Storage.Handle(value, 0)
        self._push_handle(currptr)

    def _push_handle(self, handle):
        """
        Pushes a handle that does not exist onto the heap.
        This method is called from the push (or set_comparator)
        methods.
        """
        curr = len(self.values)
        if self.count >= curr:
            handle.index = curr
            # we are saturated so add to end and upheap
            self.values.append(handle)
        else:
            # find the first spot and upheap from there
            for i,n in enumerate(self.values):
                if n is None:
                    handle.index = i
                    self.values[i] = handle
                    break
        self.count += 1
        
        # So handle is at a given point, so upheap from there
        self.values[self._upheap(handle.index)]

    def pop(self):
        """
        Pops the top value and returns the value held by the last top value.
        """
        return self.remove(self.values[0])

    def reheap(self, handle):
        """
        Called when the value pointed by the handle has been updated so a 
        possible reheaping is required.
        """
        # Try moving it up heap if required
        curr = handle.index
        if self._upheap(curr) == curr:
            # nothing happened, then try down heaping it
            size = len(self.values)
            curr = handle.index
            while curr < size:
                left = 2 * curr + 1
                right = 2 * curr + 2
                leftPtr = None if left >= size else self.values[left]
                rightPtr = None if right >= size else self.values[right]
                if not leftPtr and not rightPtr: 
                    # we are in the right spot
                    return

                smaller = -1
                if not leftPtr and rightPtr:
                    smaller = right
                elif not rightPtr and leftPtr:
                    smaller = left 
                elif self.cmpfunc(leftPtr.value, rightPtr.value) < 0:
                    smaller = left
                else:
                    smaller = right

                # See we are smaller than the "smaller" child, if not, swap with it
                if self.cmpfunc(handle.value, self.values[smaller].value) < 0:
                    # We are smaller than the smaller child so we are in right spot
                    return

                # otherwise swap
                self.values[curr] = self.values[smaller]
                self.values[curr].index = curr
                self.values[smaller] = handle
                self.values[smaller].index = smaller
                curr = smaller
            return handle
        
    def remove(self, handle):
        """
        Removes the node referenced by the handle from the heap.
        """
        size = len(self.values)
        handle = self.values[curr]
        curr = handle.index
        while curr < size:
            left = 2 * curr + 1
            right = 2 * curr + 2
            leftPtr = None if left >= size else self.values[left]
            rightPtr = None if right >= size else self.values[right]
            # self.values[curr] = None
            which = -1
            if not leftPtr and rightPtr:
                which = right
            elif not rightPtr and leftPtr:
                which = left 
            elif not leftPtr and not rightPtr:
                break
            else:
                if self.cmpfunc(leftPtr.value, rightPtr.value) < 0:
                    which = left
                else:
                    which = right
            self.values[curr] = self.values[which]
            self.values[curr].index = curr
            self.values[which] = handle
            self.values[which].index = which
            curr = which
        self.count -= 1
        self.values[handle.index] = None
        return handle

    def _upheap(self, curr):
        while curr > 0:
            parent = (curr - 1) / 2
            if self.cmpfunc(self.values[parent].value,self.values[curr].value) <= 0:
                break
            # swap the entries
            self.values[parent].index = curr
            self.values[curr].index = parent
            self.values[parent],self.values[curr] = self.values[curr],self.values[parent]
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
