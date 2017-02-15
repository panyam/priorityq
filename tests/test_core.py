
# import unittest
import pytest
from priorityq import PQ

def test_basic():
    values = [5,1,10,4,2,6,7]
    pq = PQ(values)
    assert sorted(values) == list(pq)

