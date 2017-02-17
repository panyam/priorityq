
# import unittest
import pytest
from priorityq import PQ
from priorityq.storage import binheap
from priorityq.storage import listheap

storage_classes = [
    listheap.Storage,
    binheap.Storage
]

class Value(object):
    """ A simple object for testing in a PQ. """
    def __init__(self, value):
        self.value = value

    def __repr__(self): return str(self)
    def __str__(self):
        return "<Value (0x%x): %d>" % (id(self), self.value)

@pytest.mark.parametrize("StorageClass", storage_classes)
def test_basic(StorageClass):
    values = [5,1,10,4,2,6,7]
    pq = PQ(values, store = StorageClass())
    pqvalues = [h.value for h in list(pq)]
    assert sorted(values) == pqvalues
    for v in sorted(values):
        assert v == pq.pop()

@pytest.mark.parametrize("StorageClass", storage_classes)
def test_reverse(StorageClass):
    values = [5,1,10,4,2,6,7]
    pq = PQ(values,
            store = StorageClass(),
            comparator = lambda x,y: cmp(y,x))
    revlist = list(reversed(sorted(values)))
    pqvalues = [h.value for h in list(pq)]
    assert revlist == pqvalues
    for v in revlist:
        assert v == pq.pop()

@pytest.mark.parametrize("StorageClass", storage_classes)
def test_push(StorageClass):
    # Add a bunch of values, and find the entries
    pq = PQ(store = StorageClass())
    assert not pq
    ptr = pq.push(5)
    assert len(pq) == 1
    assert pq.find(5) == ptr

@pytest.mark.parametrize("StorageClass", storage_classes)
def test_find(StorageClass):
    # Add a bunch of values, and find the entries
    values = map(Value, [5,1,10,4,2,6,7])
    pq = PQ(values = values, store = StorageClass(),
            comparator = lambda x,y: cmp(x.value, y.value))
    assert pq.top.value == values[1]
    ptr = pq.find(values[0])
    assert ptr.value == values[0]

@pytest.mark.parametrize("StorageClass", storage_classes)
def test_remove(StorageClass):
    # Add a bunch of values
    values = map(Value, [5,1,10,4,2,6,7])
    pq = PQ(values = values, store = StorageClass(),
            comparator = lambda x,y: cmp(x.value, y.value))
    assert pq.top.value.value == 1
    # Pop and see the min change
    pq.pop()
    assert pq.find(values[1]) == None
    assert pq.top.value.value == 2

    # Remove and see what happens
    pq.remove(values[0])
    assert pq.top.value.value == 2
    assert pq.find(5) == None
    assert len(pq) == 5

@pytest.mark.parametrize("StorageClass", storage_classes)
def test_adjust(StorageClass):
    # Add a bunch of values, and find the entries
    values = map(Value, [5,2,10])
    pq = PQ(values = values, store = StorageClass(),
            comparator = lambda x,y: cmp(x.value, y.value))
    assert pq.top.value == values[1]

    ptr = pq.find(values[0])
    ptr.value.value = 1
    pq.adjust(ptr)
    assert pq.top.value == values[0]
