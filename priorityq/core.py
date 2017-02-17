# -*- coding: utf-8 -*-

class PQ(object):
    """A flexible PriorityQueue wrapper to allow deletions, fast findings and updates of element priorities."""
    def __init__(self, values = None, comparator = cmp,
                 duplicates = False, store = None):
        """Returns a new PriorityQueue instance.

        Parameters:
        -----------
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

        self.handlesByValue = {}
        if values:
            values = set(values) or []
            handles = self.storage.heapify(values)
            if self.duplicates:
                for h in handles: self.handlesByValue[h.value] = [h]
            else:
                for h in handles: self.handlesByValue[h.value] = h

    @property
    def top(self):
        """Returns a handle to the minimum (top) value."""
        return self.storage.top()

    def pop(self):
        """Removes the top value from the PQ and returns its value."""
        handle = self.storage.pop()
        if self.duplicates:
            self.handlesByValue[handle.value].remove(handle)
        else:
            del self.handlesByValue[handle.value]
        return handle.value

    def push(self, value):
        """Pushes a new value onto the PQ.

        If the value already exists, then the value is only added again to the storage if the duplicates flag is set to False.

        Returns a handle to the value within the PQ.
        """
        if self.duplicates:
            ptr = self.storage.push(value)
            if value not in self.handlesByValue:
                self.handlesByValue[value] = []
            self.handlesByValue[value].append(ptr)
        elif value not in self.handlesByValue:
            ptr = self.storage.push(value)
            self.handlesByValue[value] = ptr
        else:
            ptr = self.handlesByValue[value]
        return ptr

    def adjust(self, value_or_handle):
        """ Called to reevaluate the position of an entry within the heap.

        This is usually called after an entry has been modified such that its position in the heap would have changed (due to a change in its priority).
        """
        handle = None
        value = value_or_handle
        if value_or_handle in self.handlesByValue:
            # A value was passed so adjust it by its handle
            handle = self.handlesByValue[value_or_handle]
        elif hasattr(value_or_handle, "value"):
            value = value_or_handle.value
            if value_or_handle.value in self.handlesByValue:
                handle = self.handlesByValue[value_or_handle.value]
        if handle:
            self.storage.adjust(handle)
        else:
            handle = self.storage.push(value)
        return handle

    def remove(self, value_or_handle):
        """Removes a given value from the PQ.

        If a handle is passed instead of a value then only the value referred by the handle is
        removed (regardless of other duplicates).
        To remove all instances of a value from the PQ, pass the value instead.
        """
        handle = None
        value = value_or_handle
        if value_or_handle in self.handlesByValue:
            # A value was passed so adjust it by its handle
            handle = self.handlesByValue[value_or_handle]
        elif hasattr(value_or_handle, "value"):
            value = value_or_handle.value
            if value_or_handle.value in self.handlesByValue:
                handle = self.handlesByValue[value_or_handle.value]
        if handle:
            self.storage.remove(handle)
        if self.duplicates:
            self.handlesByValue[handle.value].remove(handle)
        else:
            del self.handlesByValue[handle.value]

    def find(self, value):
        """Returns a handle to the first instance of a particular value.
        """
        if self.duplicates:
            v = self.handlesByValue.get(value, [])
            if v: v = v[0]
        else:
            v = self.handlesByValue.get(value, None)
        return v

    def __iter__(self):
        return iter(self.storage)

    def __len__(self):
        return self.storage.__len__()

    def __nonzero__(self):
        return self.storage.__nonzero__()
