
from base import Handle as BaseHandle
from base import Storage as BaseStorage

class Handle(BaseHandle):
    def __init__(self, value, index):
        super(Handle, self).__init__(value)
        self.index = index

class Storage(BaseStorage):
    """
    A simple list based heap.
    """
    def __init__(self, cmpfunc = cmp):
        super(Storage, self).__init__(cmpfunc)
        self._handles = []
        self._count = 0

    def top(self):
        """
        Returns a handle to the top value.
        """
        return min(self._handles, key = lambda x: x.value)

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
        currptr = Handle(value, len(self._handles))
        self._handles.append(currptr)
        return currptr

    def pop(self):
        """
        Pops the top value and returns the value held by the last top value.
        """
        index,handle = min(enumerate(self._handles), key = lambda x: x[1].value)
        for i in xrange(index + 1, len(self._handles)):
            self._handles[i].index = i - 1
        del self._handles[index]
        return handle

    def remove(self, handle):
        """
        Removes the node referenced by the handle from the heap.
        """
        index = handle.index
        del self._handles[index]
        for i in xrange(index, len(self._handles)):
            self._handles[i].index = i
        return handle

