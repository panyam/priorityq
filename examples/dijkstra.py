
import sys, gzip
import time, random
from priorityq import PQ
from priorityq.storage import binheap
from collections import defaultdict
INFINITY = sys.maxint

def dijkstra(nodes, edges, source, target):
    """
    Return the shortest path from the source to target.
    """
    # Keeps track of the parent node for a node in the path
    # between source and target.
    distances = {source: 0, target: INFINITY}
    parents = defaultdict(lambda: None)
    known_nodes = {source}
    nodeheap = PQ([source, target], 
                  comparator = lambda x,y: distances[x] - distances[y])

    def neighbours_of(node):
        return edges[node].keys()

    # Add start's neighbours to heap
    for neighbour in neighbours_of(source):
        distances[neighbour] = edges[source][neighbour]
        nodeheap.push(neighbour)

    last = None
    while last != target and nodeheap:
        # get the node that is closest to the source at this point
        import ipdb ; ipdb.set_trace()
        currnode = nodeheap.pop()
        if currnode in known_nodes:
            continue
        # Go through each of the curr node's neighbours
        # and update it's distances.   It's "new" distance can either
        # be "via" its parent (currnode) or directly from the
        # source node if such an edge exists.
        for child in neighbours_of(currnode):
            childptr = nodeheap.find(child)
            curr_dist = distances[currnode] + edges[currnode][child]
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
    with (gzip.GzipFile(graph_path) if graph_path.lower().endswith(".gz") else open(graph_path)) as infile:
        lines = infile.read().split("\n")
        for line in lines:
            l = [l.strip() for l in line.split(" ") if l.strip()]
            if not l or l[0] not in ["a", "p"]:
                continue
            yield l

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

def shortest_path(graph_path, numtries = 10):
    # The graph file contains entry of the following format:
    # c <comment>
    # a source target dist
    # p sp numnodes numedges

    nodes, edges, numnodes, numedges = read_graph(graph_path)

    totaltime = 0
    for i in xrange(numtries):
        source = int(random.random() * numnodes)
        dest = int(random.random() * numnodes)
        while dest == source:
            dest = int(random.random() * numnodes)
        starttime = time.time()
        dist, parents = dijkstra(nodes, edges, source, dest)
        endtime = time.time()
        print "Distance from %d -> %d = %d" % (source, dest, dist)
        totaltime += (endtime - starttime)

    print "Num Tries: %f, Total Time: %f seconds, Average: %f seconds" % (numtries, totaltime, totaltime / float(numtries))


if __name__ == "__main__":
    graph_path = sys.argv[1]
    numtries = int(sys.argv[2])
    shortest_path(graph_path, numtries)
