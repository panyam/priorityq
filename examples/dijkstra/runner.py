
import cProfile, importlib
import sys, gzip
import time, random
from priorityq import PQ
import priorityq.storage
from priorityq.algorithms.dijkstra import shortest_path
from collections import defaultdict
INFINITY = sys.maxint

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
    def neighbour_func(node):
        return edges[node].iteritems()

    starttime = time.time()
    dist, parents = shortest_path(source, dest, neighbour_func, heapmodule.Storage)
    endtime = time.time()
    numfinds = len(parents)
    timetaken = endtime - starttime
    print "HeapModule: %s, SP (%d -> %d), Distance = %d, Nodes Processed: %d, Time Taken: %f seconds, %f nodes/seconds" % (heapmodule.__name__, source, dest, dist, numfinds, timetaken, numfinds / float(timetaken))
    return numfinds, timetaken

def profile_all_shortest_paths(nodes, edges, numnodes, numedges, heapmodules, test_nodes):
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
    profile_all_shortest_paths(nodes, edges, numnodes, numedges, heapmodules, test_nodes)

if __name__ == "__main__":
    graph_path = sys.argv[1]
    numtries = int(sys.argv[2])
    heapmodule = None
    if len(sys.argv) > 3:
        heapmodule = importlib.import_module("priorityq.storage." + sys.argv[3])
    run_tests(graph_path, numtries, heapmodule)
