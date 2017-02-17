
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
        self._empty_indexes = []
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
        out = [h for h in self._handles if h]
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
        handle = Handle(value, self._count)
        self._count += 1
        if self._empty_indexes:
            i = self._empty_indexes.pop()
            handle.index = i
            self._handles[i] = handle
        else:
            # we are saturated so add to end and upheap
            self._handles.append(handle)

            # And extend with more empty space at the end so we can ammortize push speeds
            newlen = self._count
            newcapacity = ((newlen * 3) / 2)
            spare = max(8, newcapacity - newlen)
            nones = [None] * spare
            self._handles.extend(nones)
            self._empty_indexes.extend(range(newlen + spare - 1, newlen - 1, -1))
        
        # So handle is at a given point, so upheap from there
        self._upheap(handle.index)
        return handle

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
        self._release_index(handle.index)
        return handle

    def _release_index(self, index):
        A = self._empty_indexes
        lo = 0
        hi = len(A) - 1
        while lo <= hi:
            mid = (lo + hi) / 2
            assert A[mid] != index      # Value should not have been here to begin with
            if index < A[mid]:          # go to right half
                lo = mid + 1
            else:                       # go to left half
                hi = mid - 1
        A.insert(lo, index)

    def _upheap(self, curr):
        start = curr
        parent_is_empty = False
        while curr > 0:
            parent = (curr - 1) / 2
            parent_handle = self._handles[parent]
            parent_is_empty = parent_handle is None
            if parent_handle:
                if self._cmpfunc(parent_handle.value,self._handles[curr].value) <= 0:
                    break
                parent_handle.index = curr

            # swap the entries
            self._handles[curr].index = parent
            self._handles[parent],self._handles[curr] = self._handles[curr],self._handles[parent]
            curr = parent

        # If the 
        if parent_is_empty: self._release_index(start)

        return curr
