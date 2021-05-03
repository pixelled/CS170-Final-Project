

import networkx as nx
import graph_tool as gt
import graph_tool.search as gt_search
import graph_tool.topology as gt_topo

class VisitorConnected(gt_search.DFSVisitor):
    def __init__(self):
        self.c = 0

    def discover_vertex(self, u):
        self.c += 1

def is_connected(G):
    visitor = VisitorConnected()
    gt_search.dfs_search(G, G.vertex(0), visitor);
    return visitor.c == G.num_vertices()

def is_valid_solution(G, c, k):
    """
    Checks whether D is a valid mapping of G, by checking every room adheres to the stress budget.
    Args:
        G: networkx.Graph
        c: List of cities to remove
        k: List of edges to remove (List of tuples)
    Returns:
        bool: false if removing k and c disconnects the graph
    """
    size = G.num_vertices()
    mask_e = G.new_edge_property("bool")
    for road in k:
        e = G.edge(road[0],road[1])
        assert e, "Invalid Solution: {} is not a valid edge in graph G".format(road)
    G.set_edge_filter(mask_e, inverted=True)
    
    mask_v = G.new_vertex_property("bool")
    for city in c:
        v = G.vertex(city)
        mask_v[v] = 1
    G.set_vertex_filter(mask_v, inverted=True)

    #'Invalid Solution: Source vertex is removed'
    G.vertex(0)
    #'Invalid Solution: Target vertex is removed'
    G.vertex(size - 1)

    is_valid = is_connected(G)

    G.set_edge_filter(None)
    G.set_vertex_filter(None)

    return is_valid

def calculate_score(G, c, k):
    """
    Calculates the difference between the original shortest path and the new shortest path.
    Args:
        G: networkx.Graph
        c: list of cities to remove
        k: list of edges to remove
    Returns:
        float: total score
    """
    assert is_valid_solution(G, c, k)
    node_count = G.num_vertices()
    original_min_dist = gt_topo.shortest_distance(G, G.vertex(0), G.vertex(node_count - 1), weights=G.edge_properties['weight'])

    mask_e = G.new_edge_property("bool")
    for road in k:
        mask_e[G.edge(road[0], road[1])] = 1
    G.set_edge_filter(mask_e, inverted=True)
    mask_v = G.new_vertex_property("bool")
    for city in c:
        mask_v[G.vertex(city)] = 1
    G.set_vertex_filter(mask_v, inverted=True)

    final_min_dist = gt_topo.shortest_distance(G, G.vertex(0), G.vertex(node_count - 1), weights=G.edge_properties['weight'])

    G.set_edge_filter(None)
    G.set_vertex_filter(None)

    difference = final_min_dist - original_min_dist
    return difference
