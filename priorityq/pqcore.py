
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
        if value not in self.pointersByValue:
            self.pointersByValue[value] = []
        self.pointersByValue[value].append(ptr)
        return ptr

    def remove(self, value):
        if self.pointersByValue[value]:
            ptr = self.pointersByValue[value][0]
            self.storage.remove(ptr)
        self.pointersByValue[pointer.value].remove(pointer)

    def find(self, value):
        """
        Returns a pointer to the node that contains the particular key.
        If the from parameter is provided, then the seach is performed relative
        to that pointer (in case of duplicate keys).
        """
        v = self.pointersByValue.get(value, [])
        if v: v = v[0]
        return v

