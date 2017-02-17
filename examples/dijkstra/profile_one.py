import dijkstra, cProfile
nodes, edges, numnodes, numedges = dijkstra.read_graph("data/USA-road-d.BAY.gr.gz")
source, dest = dijkstra.random_nodes(numnodes)
print "source, dest = %d,%d" % (source, dest)
from priorityq.storage import listheap as heapmodule
cProfile.run("dijkstra.profile_shortest_path(nodes, edges, source, dest, heapmodule)")
from priorityq.storage import binheap as heapmodule
cProfile.run("dijkstra.profile_shortest_path(nodes, edges, source, dest, heapmodule)")
