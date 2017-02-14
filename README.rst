PriorityQ
---------

PriorityQ is a library for managing a priority queue (PQ) with a cleaner API to enable custom comparators, 
finding references to values efficiently (in constant time) and deleting values from the PQ.   This was 
developed because the current heapq module (in python's standard library) does not provide an efficient
find operation (it is O(n)) and has no easy way to deleting an element and ensuring the heap invariant
afterwards.

Features
````````

* O(1) finding of elements
* Deletion of elements possible (in O(log n)).
* Adjusting of the priority of an element without requiring a deletion followed by an insertion.
* Opaque handles to elements that can be used to reference to the same item again.
* Duplicate elements allowed.
* Custom comparator function can be passed to the PQ itself instead of needing to implement __cmp__.

It is simple to use
```````````````````

To create a PQ simply do:

.. code:: python

    # A simple object with a comparator
    class Item(object):
        def __init__(self, value):
            self.value = value
        def __cmp__(self, another):
            return cmp(self.value, another.value)

    from priorityq import PQ
    pq = PQ()
    pq.heapify([Item(r) for r in [1, 10, 2, 20, 4, 7, 9, 3, 5, 6]])

    print list(pq)

    # Should print:
    # 1 2 3 4 5 6 7 9 10 20

    handle_10 = pq.find(25)   #   Happens in O(1)

    handle_10.value = 12      #   Modify its value - O(log n)
    pq.adjust(handle_10)      #   Indicate to the heap to reprioritise/adjust it

    print list(pq)

    # Should print:
    # 1 2 3 4 5 6 7 9 20 25

    handle_10.value = 10      #   Modify its value using the same opaque pointer as before
    pq.adjust(handle_10)      #   Indicate to the heap to reprioritise/adjust it

    print list(pq)

    # Should print:
    # 1 2 3 4 5 6 7 9 10 20

Links
`````
* `Documentation Wiki <https://github.com/panyam/priorityq/wiki>`_
* `Website <https://github.com/panyam/priorityq>`_
