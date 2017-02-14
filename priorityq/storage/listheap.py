
import base

class ListHeapStorage(base.Pointer):
    """
    A heap implemented as an array of elements where a node at index 
    i has children at indexes 2*i+1 and 2*i+2
    """
    def __init__(self, cmpfunc = cmp):
        self.cmpfunc = cmpfunc
        self.values = []
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

    @property
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
        curr = len(self.values)
        currptr = ListHeapStorage.Pointer(value, 0)
        if self.count >= curr:
            currptr.index = curr
            # we are saturated so add to end and upheap
            self.values.append(currptr)
        else:
            # find the first spot and upheap from there
            for i,n in enumerate(self.values):
                if n is None:
                    currptr.index = i
                    self.values[i] = currptr
                    break
        self.count += 1
        
        # So currptr is at a given point, so upheap from there
        self.values[self._upheap(currptr.index)]

    def pop(self):
        """
        Pops the top value and returns the value held by the last top value.
        """
        return self.remove(self.values[0])

    def reheap(self, pointer):
        """
        Called when the value pointed by the pointer has been updated so a 
        possible reheaping is required.
        """
        # Try moving it up heap if required
        curr = pointer.index
        if self._upheap(curr) == curr:
            # nothing happened, then try down heaping it
            size = len(self.values)
            curr = pointer.index
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
                if self.cmpfunc(pointer.value, self.values[smaller].value) < 0:
                    # We are smaller than the smaller child so we are in right spot
                    return

                # otherwise swap
                self.values[curr] = self.values[smaller]
                self.values[curr].index = curr
                self.values[smaller] = pointer
                self.values[smaller].index = smaller
                curr = smaller
            return pointer
        
    def remove(self, pointer):
        """
        Removes the node referenced by the pointer from the heap.
        """
        size = len(self.values)
        pointer = self.values[curr]
        curr = pointer.index
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
            self.values[which] = pointer
            self.values[which].index = which
            curr = which
        self.count -= 1
        self.values[pointer.index] = None
        return pointer

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

    class Pointer(base.Pointer):
        def __init__(self, value, index):
            super(ListHeapStorage.Pointer, self).__init__(value)
            self.index = index

        def __repr__(self): return str(self)
        def __str__(self):
            return "<Ptr (0x%x), Index: %d, Value: %s>" % (id(self), self.index, str(self.value))

        def __cmp__(self, another):
            return cmp(self.value, another.value)
