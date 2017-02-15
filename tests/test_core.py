
# import unittest
import pytest
from priorityq import PQ

def test_basic():
    values = [5,1,10,4,2,6,7]
    pq = PQ(values)
    assert sorted(values) == list(pq)
    for v in sorted(values):
        assert v == pq.pop().value

def test_reverse():
    values = [5,1,10,4,2,6,7]
    pq = PQ(values,
            comparator = lambda x,y: cmp(y,x))
    revlist = list(reversed(sorted(values)))
    assert revlist == list(pq)
    for v in revlist:
        assert v == pq.pop().value
