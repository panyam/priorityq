
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
        A tuple of distance to the target node along with a dictionary that contains the parent
        node for each node in the traversal from the source.
    """
    # Keeps track of the parent node for a node in the path
    # between source and target.
    storage_class = storage_class or "prioirityq.storage.binheap.Storage"
    distances = {source: 0, target: INFINITY}
    parents = defaultdict(lambda: None)
    known_nodes = set([source])
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
        if currnode in known_nodes:
            continue
        # Go through each of the curr node's neighbours
        # and update it's distances.   It's "new" distance can either
        # be "via" its parent (currnode) or directly from the
        # source node if such an edge exists.
        for child,child_dist in neighbour_func(currnode):
            childptr = nodeheap.find(child)
            curr_dist = distances[currnode] + child_dist
            if child not in distances or curr_dist < distances[child]:
                distances[child] = curr_dist
                parents[child] = currnode
            if childptr:
                nodeheap.adjust(childptr)
            else:
                nodeheap.push(child)
        last = currnode
        known_nodes.add(currnode)

    # Return the list of all parent nodes that can be walked up
    # backwards to extract the path to the source (in reverse)
    return distances[target], parents

def lines_from(path):
    if path.lower().endswith(".gz"):
        infile = gzip.GzipFile(path)
    else:
        infile = open(path)

    lines = infile.read().split("\n")
    for line in lines:
        l = [l.strip() for l in line.split(" ") if l.strip()]
        if not l or l[0] not in ["a", "p"]:
            continue
        yield l
    infile.close()

