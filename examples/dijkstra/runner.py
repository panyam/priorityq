
import cProfile, importlib
import sys, gzip
import time, random
from priorityq import PQ
import priorityq.storage
from collections import defaultdict
INFINITY = sys.maxint


def dijkstra(nodes, edges, source, target, heapmodule):
    """
    Return the shortest path from the source to target.
    """
    # Keeps track of the parent node for a node in the path
    # between source and target.
    distances = {source: 0, target: INFINITY}
    parents = defaultdict(lambda: None)
    known_nodes = set([source])
    nodeheap = PQ([source, target], 
                  store = heapmodule.Storage(),
                  comparator = lambda x,y: distances[x] - distances[y])

    def neighbours_of(node):
        return edges[node].keys()

    # Add start's neighbours to heap
    for neighbour in neighbours_of(source):
        distances[neighbour] = edges[source][neighbour]
        nodeheap.push(neighbour)

    numfinds = 0
    numadjusts = 0
    numpushes = 0
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
        for child in neighbours_of(currnode):
            numfinds += 1
            childptr = nodeheap.find(child)
            curr_dist = distances[currnode] + edges[currnode][child]
            if child not in distances or curr_dist < distances[child]:
                distances[child] = curr_dist
                parents[child] = currnode
            if childptr:
                numadjusts += 1
                nodeheap.adjust(childptr)
            else:
                numpushes += 1
                nodeheap.push(child)
        last = currnode
        known_nodes.add(currnode)

    # Return the list of all parent nodes that can be walked up
    # backwards to extract the path to the source (in reverse)
    return distances[target], parents, numfinds, numadjusts, numpushes

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

def read_graph(graph_path):
    nodes = set()
    edges = {}

    numnodes = None
    numedges = None
    edgecount = 0
    for l in lines_from(graph_path):
        if l[0] == 'p':
            numnodes,numedges = int(l[2]),int(l[3])
        elif l[0] == 'a':
            edgecount += 1
            nodes.add(l[1])
            src,dest,dist = int(l[1]),int(l[2]),int(l[3])
            if src not in edges:
                edges[src] = {}
            edges[src][dest] = dist
    if numnodes is None:
        numnodes = len(nodes)
        numedges = edgecount
    assert numnodes == len(nodes)
    assert numedges == edgecount
    return nodes, edges, numnodes, numedges

def random_nodes(numnodes):
    source = int(random.random() * numnodes)
    dest = int(random.random() * numnodes)
    while dest == source:
        dest = int(random.random() * numnodes)
    return source, dest

def profile_shortest_path(nodes, edges, source, dest, heapmodule):
    starttime = time.time()
    dist, parents, numfinds, numadjusts, numpushes = dijkstra(nodes, edges, source, dest, heapmodule)
    endtime = time.time()
    timetaken = endtime - starttime
    print "HeapModule: %s, SP (%d -> %d), Distance = %d, Nodes Processed: %d, Time Taken: %f seconds, %f nodes/seconds" % (heapmodule.__name__, source, dest, dist, numfinds, timetaken, numfinds / float(timetaken))
    return numfinds, timetaken

def shortest_path(nodes, edges, numnodes, numedges, heapmodules, test_nodes):
    # The graph file contains entry of the following format:
    # c <comment>
    # a source target dist
    # p sp numnodes numedges

    totaltimes = [0] * len(heapmodules)
    totalnodes = [0] * len(heapmodules)
    for source,dest in test_nodes:
        for hindex, heapmodule in enumerate(heapmodules):
            nodes_processed, timetaken = profile_shortest_path(nodes, edges, source, dest, heapmodule)
            totalnodes[hindex] += nodes_processed
            totaltimes[hindex] += timetaken
    for hindex, heapmodule in enumerate(heapmodules):
        print "Heapmodule: %s, Total Nodes: %d, Total Time: %f seconds, Nodes per second: %f seconds" % (heapmodule.__name__, totalnodes[hindex], totaltimes[hindex], totalnodes[hindex] / float(totaltimes[hindex]))

def run_tests(graph_path, numtries, heapmodule = None):
    if heapmodule:
        heapmodules = [heapmodule]
    else:
        from priorityq.storage import binheap
        from priorityq.storage import listheap
        heapmodules = [
            binheap,
            listheap
        ]
    nodes, edges, numnodes, numedges = read_graph(graph_path)
    test_nodes = [random_nodes(numnodes) for i in range(numtries)]
    shortest_path(nodes, edges, numnodes, numedges, heapmodules, test_nodes)

if __name__ == "__main__":
    graph_path = sys.argv[1]
    numtries = int(sys.argv[2])
    heapmodule = None
    if len(sys.argv) > 3:
        heapmodule = importlib.import_module("priorityq.storage." + sys.argv[3])
    run_tests(graph_path, numtries, heapmodule)
