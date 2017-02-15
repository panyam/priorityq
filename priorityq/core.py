# -*- coding: utf-8 -*-
"""
Hello World
"""

class PQ(object):
    """A flexible PriorityQueue wrapper to allow deletions, fast findings and updates of element priorities."""
    def __init__(self, values = None, comparator = cmp,
                 duplicates = False, store = None):
        """Returns a new PriorityQueue instance.

        Keyword Arguments:
            values      --  The values to be initially added to the heap.
            comparator  --  The comparator function to be used to organise the values by.  
                            If one is not provided then the standard comparator (cmp) is used.
            duplicates  --  This boolean flag (default = False) specifies whether duplicate 
                            values are stored seperately or not.  If False, then only one instance
                            of a value can be in the PQ at a time.
            store       --  By default the PriorityQueue uses a binary heap to organise the values.
                            This can be overridden by any other instances that inherits the Storage
                            class.  See Storage for more details.
        """
        if not store:
            from storage import binheap
            store = binheap.Storage()
        self.duplicates = duplicates
        self.storage = store
        self.storage.comparator = comparator

        values = values or []
        self.handlesByValue = {}
        handles = self.storage.heapify(values)
        for h in handles: self.handlesByValue[h.value] = h

    def top(self):
        """Returns a handle to the minimum (top) value."""
        return self.storage.top()

    def pop(self):
        """Removes the top value from the PQ and returns its value."""
        return self.storage.pop().value

    def push(self, value_or_handle):
        """Pushes a new value onto the PQ.

        If the value already exists then the duplicate flag (passed in the initializer) determines
        the behaviour:
            duplicate = True    =>  If the value is a handle then the entry is replaced.  Otherwise
                                    the value is added (as a duplicate)
            duplicate = False   =>  The value is replaced.

        Returns a handle to the value within the PQ.
        """
        ptr = self.storage.push(value)
        if value not in self.handlesByValue:
            self.handlesByValue[value] = []
        self.handlesByValue[value].append(ptr)
        return ptr

    def remove(self, value_or_handle):
        """Removes a given value from the PQ.

        If a handle is passed instead of a value then only the value referred by the handle is
        removed (regardless of other duplicates).
        To remove all instances of a value from the PQ, pass the value instead.
        """
        if self.handlesByValue[value]:
            ptr = self.handlesByValue[value][0]
            self.storage.remove(ptr)
        self.handlesByValue[handle.value].remove(handle)

    def find(self, value):
        """Returns a handle to the first instance of a particular value.
        """
        v = self.handlesByValue.get(value, [])
        if v: v = v[0]
        return v

    def __iter__(self):
        return iter(self.storage)

