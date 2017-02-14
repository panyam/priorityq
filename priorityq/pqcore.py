
class PQ(object):
    def __init__(self, storage):
        self.storage = storage
        self.pointsByValue = {}

    def top(self):
        return self.storage.top()

    def pop(self):
        return self.storage.pop()

    def push(self, value):
        ptr = self.storage.push(value)
        if value not in self.handlesByValue:
            self.handlesByValue[value] = []
        self.handlesByValue[value].append(ptr)
        return ptr

    def remove(self, value):
        if self.handlesByValue[value]:
            ptr = self.handlesByValue[value][0]
            self.storage.remove(ptr)
        self.handlesByValue[handle.value].remove(handle)

    def find(self, value):
        """
        Returns a handle to the node that contains the particular key.
        If the from parameter is provided, then the seach is performed relative
        to that handle (in case of duplicate keys).
        """
        v = self.handlesByValue.get(value, [])
        if v: v = v[0]
        return v

