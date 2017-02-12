from heapq import heapq

class PQ(object):
    def __init__(self, storage):
        self.storage = storage

    def top(self):
        return self.storage.top().value

    def topref(self):
        return self.storage.top()

    def pop(self):
        return self.storage.pop()

    def push(self, value):
        return self.storage.push(value)

    def find(self, value):
        return self.storage.push(value)

