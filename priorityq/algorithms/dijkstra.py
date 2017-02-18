
import sys
from priorityq import PQ
import priorityq.storage
from collections import defaultdict
INFINITY = sys.maxint

def shortest_path(source, target, neighbour_func, storage_class = None):
    """Return the shortest path from the source to target.

    **Parameters**
        source          -   The source node from which the path is to be calculated
        target          -   The target node to which the path is to be calculated
        neighbour_func  -   A function that when given a node, returns an iterator of tuples where each tuple is an edge to another node along with the weight of the edge.

    **Keyword Arguments**
        storage_class   -   The Storage class that is to be used for the priority queue 
                            which stores the nodes prioritized by their distance from the 
                            source.   Default: prioirityq.storage.binheap.Storage

    **Returns**
        A tuple that contains a map of distances for each node from the source along with a map of each node to its parent.
    """
    storage_class = storage_class or "prioirityq.storage.binheap.Storage"

    # Keep track of the distance of each node to the source node
    distances = {source: 0, target: INFINITY}

    # Keeps track of the parent node for a node in the path between source and target.
    parents = defaultdict(lambda: None)

    # The nodes that are known to have the shortest path in each iteration
    known_nodes = set([source])

    # A heap of nodes is used where they nodes are sorted by their distance to the source node
    nodeheap = PQ([source, target], 
                  store = storage_class(),
                  comparator = lambda x,y: distances[x] - distances[y])

    # Add start's neighbours to heap
    for neighbour,neigh_dist in neighbour_func(source):
        distances[neighbour] = neigh_dist
        nodeheap.push(neighbour)

    last = None
    while last != target and nodeheap:
        # get the node that is closest to the source at this point
        currnode = nodeheap.pop()

        # If the node is already known then skip its children
        if currnode in known_nodes: continue

        # Go through each of the curr node's neighbours
        # and update it's distances.   It's "new" distance can either
        # be "via" its parent (currnode) or directly from the
        # source node if such an edge exists.
        for child,child_dist in neighbour_func(currnode):
            curr_dist = distances[currnode] + child_dist
            if child not in distances or curr_dist < distances[child]:
                distances[child] = curr_dist
                parents[child] = currnode

            # Ensure the heap update's the child priority
            childptr = nodeheap.find(child)
            if childptr:
                nodeheap.adjust(childptr)
            else:
                nodeheap.push(child)

        last = currnode
        known_nodes.add(currnode)

    # Return the list of all parent nodes that can be walked up
    # backwards to extract the path to the source (in reverse)
    return distances, parents

