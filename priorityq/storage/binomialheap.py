
from base import Handle as BaseHandle
from base import Storage as BaseStorage

class Node(BaseHandle):
    def __init__(self, value, degree = 0):
        super(Node, self).__init__(value)
        self.degree = degree
        self.parent = None
        self.next = None
        self.child_head = None

    @property
    def children(self):
        """Return an iterator over the children of a given node."""
        curr = self.child_head
        while curr:
            yield curr
            curr = curr.next

class Storage(BaseStorage):
    """
    A heap implemented as an array of elements where a node at index 
    i has children at indexes 2*i+1 and 2*i+2
    """
    def __init__(self, cmpfunc = cmp):
        super(Storage, self).__init__(cmpfunc)
        self.clear()

    def __nonzero__(self):
        return self._count > 0

    def __len__(self):
        """
        Returns the number of elements in the heap.
        """
        return self._count

    def clear(self):
        """Removes all elements from the heap."""
        self._count = 0
        self._roots = None

    def all_handles(self):
        """Returns an iterator over all the values in the heap."""
        out = []
        for root in self._roots:
            stack = [root]
            while stack:
                next = stack.pop()
                out.append(next)
                for child in next.children:
                    stack.append(child)
        out.sort(cmp = lambda x,y: self._cmpfunc(x.value, y.value))
        return out

    def push(self, value):
        """Pushes a new value onto the heap."""
        newnode = Node(value)
        self._push_node(newnode)
        return newnode

    def _push_node(self, node):
        if not self._roots:
            self._root = [node]
        else:

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

    def _merge(self, node1, node):
        diff = self._cmpfunc(node1.value, node2.value)
        if node1.degree == node2.degree:
            if diff <= 0:
                self._add_child(node1, node2)
            else:
                self._add_child(node2, node1)
        elif node1.degree < node2.degree:
            pass
        else:

    def _add_child(self, parent, child):
        # if we already have a child with the same degree, 
        # then merge with that one!

