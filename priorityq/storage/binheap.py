
from base import Handle as BaseHandle
from base import Storage as BaseStorage

class Handle(BaseHandle):
    def __init__(self, value, index):
        super(Handle, self).__init__(value)
        self.index = index

    def __repr__(self): return str(self)
    def __str__(self):
        return "<Ptr (0x%x), Index: %d, Value: %s>" % (id(self), self.index, str(self.value))

class Storage(BaseStorage):
    """
    A heap implemented as an array of elements where a node at index 
    i has children at indexes 2*i+1 and 2*i+2
    """
    def __init__(self, cmpfunc = cmp):
        super(Storage, self).__init__(cmpfunc)
        self._handles = []
        self._count = 0

    def top(self):
        """
        Returns a handle to the top value.
        """
        return self._handles[0]

    def clear(self):
        """Removes all elements from the heap."""
        self._count = 0
        self._handles = []

    def all_handles(self):
        out = self._handles[:]
        out.sort(cmp = lambda x,y: self._cmpfunc(x.value, y.value))
        return out

    def __nonzero__(self):
        return self._count > 0

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
        currptr = Handle(value, 0)
        self._push_handle(currptr)
        return currptr

    def _push_handle(self, handle):
        """
        Pushes a handle that does not exist onto the heap.
        This method is called from the push (or set_comparator)
        methods.
        """
        curr = len(self._handles)
        if self._count >= curr:
            handle.index = curr
            # we are saturated so add to end and upheap
            self._handles.append(handle)
        else:
            # find the first spot and upheap from there
            for i,n in enumerate(self._handles):
                if n is None:
                    handle.index = i
                    self._handles[i] = handle
                    break
        self._count += 1
        
        # So handle is at a given point, so upheap from there
        self._handles[self._upheap(handle.index)]

    def pop(self):
        """
        Pops the top value and returns the value held by the last top value.
        """
        return self.remove(self._handles[0])

    def adjust(self, handle):
        """
        Called when the value pointed by the handle has been updated so a 
        possible reheaping is required.
        """
        # Try moving it up heap if required
        curr = handle.index
        if self._upheap(curr) == curr:
            # nothing happened, then try down heaping it
            size = len(self._handles)
            curr = handle.index
            while curr < size:
                left = 2 * curr + 1
                right = 2 * curr + 2
                leftPtr = None if left >= size else self._handles[left]
                rightPtr = None if right >= size else self._handles[right]
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
                if self._cmpfunc(handle.value, self._handles[smaller].value) < 0:
                    # We are smaller than the smaller child so we are in right spot
                    return

                # otherwise swap
                self._handles[curr] = self._handles[smaller]
                self._handles[curr].index = curr
                self._handles[smaller] = handle
                self._handles[smaller].index = smaller
                curr = smaller
            return handle
        
    def remove(self, handle):
        """
        Removes the node referenced by the handle from the heap.
        """
        size = len(self._handles)
        curr = handle.index
        while curr < size:
            left = 2 * curr + 1
            right = 2 * curr + 2
            leftPtr = None if left >= size else self._handles[left]
            rightPtr = None if right >= size else self._handles[right]
            # self._handles[curr] = None
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
            self._handles[curr] = self._handles[which]
            self._handles[curr].index = curr
            self._handles[which] = handle
            self._handles[which].index = which
            curr = which
        self._count -= 1
        self._handles[handle.index] = None
        return handle

    def _upheap(self, curr):
        while curr > 0:
            parent = (curr - 1) / 2
            if self._cmpfunc(self._handles[parent].value,self._handles[curr].value) <= 0:
                break
            # swap the entries
            self._handles[parent].index = curr
            self._handles[curr].index = parent
            self._handles[parent],self._handles[curr] = self._handles[curr],self._handles[parent]
            curr = parent
        return curr
