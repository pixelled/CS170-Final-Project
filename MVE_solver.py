"""
This solver deals with "most vital edges of a shortest path problem" via iteratively deleting the "most vital edges".
The framework is Graphtool
Author: Xiaofeng Zhao
"""

import graph_tool as gt
import graph_tool.stats as gt_st
import graph_tool.topology as gt_topo
import graph_tool.search as gt_sch
import networkx as nx
import parse
import itertools

# The path of input files. Modify the path if necessary
input_path = "/home/xiaofeng/CS170/inputs"


class Visitor_all_reachable_vertices(gt_sch.DFSVisitor):
    def __init__(self, v_list: list):
        self.v_list = v_list

    def add_to_list(self):
        self.v_list.append(self)

def nx2gt(G_nx: nx.Graph):
    """
    Transform a networkX graph to a corresponding graph_tool graph.
    """

    g = gt.Graph(directed=False)
    g.add_vertex(len(G_nx.nodes))
    g.add_edge_list(G_nx.edges)
    nx_edge_property = list(nx.get_edge_attributes(G_nx, 'weight').values())
    eprop = g.new_edge_property(value_type='double')

    # associate each edge with a weight.
    idx = 0
    for edge in g.edges():
        eprop[edge] = nx_edge_property[idx]
        idx += 1
    g.edge_properties["weight"] = eprop

    return g


def get_shortest_path_tree(g: gt.Graph, source):
    """
    Construct a shortest path tree from source
    Args:
        g: The graph
        source:

    Returns:
        short_path_tree
    """
    shortest_path_tree = gt.Graph(directed=True)

    dist_map, pred_map = gt_topo.shortest_distance(g, source, pred_map=True)

    return shortest_path_tree


def get_shortest_st_path(g: gt.Graph):
    """ Return the shortest path from s to t. """
    source = g.vertex(0)
    target = g.vertex(g.num_vertices() - 1)
    _, e_list = gt_topo.shortest_path(g, source, target)
    return e_list


def get_cut_from_SPT(g:gt.Graph, shortest_path_tree: gt.Graph, edge_to_delete):
    """
    After deleting <edge_to_delete>, we will have 2 trees. The 2 trees divide the node set of
    graph <g> into two subsets. The function returns the cut that forms these two node subsets.
    Args:
        shortest_path_tree:
        edge_to_delete:

    Returns:

    """
    # Assuming the edge_to_delete is (u,v), v is the root of the second tree.
    cut_list = []
    v = edge_to_delete.source()
    nodes_of_second_tree = set.union({v.target() for v in gt_sch.dfs_iterator(shortest_path_tree, v)},
                                     {v.source() for v in gt_sch.dfs_iterator(shortest_path_tree, v)})
    all_nodes = {v for v in g.vertices()}
    nodes_of_first_tree = all_nodes.difference(nodes_of_second_tree)

    for n_1 in nodes_of_first_tree:
        for n_2 in nodes_of_second_tree:
            cut = g.edge(n_1, n_2)
            if cut is not None:
                cut_list.append(cut)

    return cut_list


def solver(g, k, c):
    """
    MVE_solver
    Args:
        g: The graph where we delete edges and vertices
        k: The maximum number of edges to delete
        c: The maximum number of nodes to delete

    Returns:
        edges_to_delete: a list of edges to be removed
    """


""" The following are abandoned methods """
def get_shortest_path_tree_v1(g: gt.Graph, source):
    """
    Construct a shortest path tree from source
    Args:
        g: The graph
        source:

    Returns:
        short_path_tree
    """
    shortest_path_tree = gt.Graph(directed=True)

    target_list = [v for v in g.vertices()]
    target_list.remove(g.vertex(0))

    SPT_edges = set()
    for v in target_list:
        _, e_list = gt_topo.shortest_path(g, source, v)
        SPT_edges = SPT_edges.union(set(e_list))
    shortest_path_tree.add_edge_list(SPT_edges)

    shortest_path_tree.set_reversed(is_reversed=True)

    return shortest_path_tree
