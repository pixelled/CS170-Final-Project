"""
This solver deals with "most vital edges of a shortest path problem" via iteratively deleting the "most vital edges".
The framework is Graphtool
Author: Xiaofeng Zhao
"""

import graph_tool as gt
import graph_tool.stats as gt_st
import networkx as nx
import parse

# The path of input files. Modify the path if necessary
input_path = "/home/xiaofeng/CS170/inputs"


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
