"""
This solver deals with "most vital edges of a shortest path problem" via iteratively deleting the "most vital edges".
The framework is Graphtool
Author: Xiaofeng Zhao
"""
import graph_tool.draw as gt_draw
import graph_tool as gt
import graph_tool.stats as gt_stat
import graph_tool.topology as gt_topo
import graph_tool.search as gt_sch
import networkx as nx
import parse
import itertools
import utils

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
    for e in G_nx.edges:
        eprop[g.edge(e[0], e[1])] = nx_edge_property[idx]
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
        short_path_tree:
        dist_map:
    """
    shortest_path_tree = gt.Graph(directed=True)
    dist_map, pred_map = gt_topo.shortest_distance(g, source, pred_map=True, weights=g.edge_properties['weight'])
    num_v = g.num_vertices()
    shortest_path_tree.add_vertex(num_v)

    edge_list = zip([x for x in pred_map.a], [x for x in range(num_v)])
    shortest_path_tree.add_edge_list(edge_list)
    gt_stat.remove_self_loops(shortest_path_tree)
    return shortest_path_tree, dist_map


def get_cut_from_SPT(g: gt.Graph, shortest_path_tree: gt.Graph, edge_to_delete):
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
    nodes_of_second_tree = set.union({e.target() for e in gt_sch.dfs_iterator(shortest_path_tree, v)},
                                     {e.source() for e in gt_sch.dfs_iterator(shortest_path_tree, v)})
    nodes_of_second_tree.add(v)

    all_nodes = {v for v in g.vertices()}
    nodes_of_first_tree = all_nodes.difference(nodes_of_second_tree)

    for n_1 in nodes_of_first_tree:
        for n_2 in nodes_of_second_tree:
            cut = g.edge(n_1, n_2)
            if cut is not None:
                cut_list.append(cut)
    # The reason to remove this cut is that the best path of last iteration contains this cut(edge).
    cut_list.remove(edge_to_delete)
    return cut_list


class MVE_solver:
    """
    Usage:
        Set the maximum number of edges to delete                   >>> k = 2
        Initilize a MVE_solver class and specify the target         >>> my_MVE = MVE_solver.MVN_solver(target)
        attain the edges deleted and a resulting graph              >>> edge_list = my_MVE.solver(g, 4)
    """
    def __init__(self, target):
        self.target = target

    def get_shortest_st_path(self, g: gt.Graph):
        """ Return the shortest path from s to t. """
        source = g.vertex(0)
        target = self.target
        _, e_list = gt_topo.shortest_path(g, source, target, weights=g.edge_properties['weight'])
        return e_list

    def solve(self, g: gt.Graph, k):
        """
        MVE_solver
        Args:
            g: The graph where we delete edges and vertices
            k: The maximum number of edges to delete

        Returns:
            edges_to_delete: a list of edges to be removed
        """
        mask_e = g.new_edge_property("bool")
        g.set_edge_filter(mask_e, inverted=True)
        # print([x for x in g.get_edge_filter()])
        list_edge_to_remove = []

        for i in range(k):
            best_edge, stop_indicator = self.best_edge_to_remove(g)
            if stop_indicator:
                break
            else:
                list_edge_to_remove.append((int(best_edge.source()), int(best_edge.target())))
                mask_e[best_edge] = 1

        return list_edge_to_remove

    def best_edge_to_remove(self, g: gt.Graph):
        s_spt_tree, s_dist_map = get_shortest_path_tree(g, g.vertex(0))
        t_spt_tree, t_dist_map = get_shortest_path_tree(g, self.target)
        st_path_edges = self.get_shortest_st_path(g)

        max_min_distance = float("-inf")
        best_edge_to_remove = None
        """
        Note: The <occurrence_empty_cut> records the number of occurrences of empty cut_list, which means this edge 
        cannot be removed, or otherwise the graph would be disconnected. If the removal of each edge on the shortest 
        path would disconnect the graph, then we stop iteration (Set <iter_stop_indicator> to be True).
        """
        occurrence_empty_cut = 0
        iter_stop_indicator = False
        num_edge_of_st_path = len(st_path_edges)
        for e in st_path_edges:

            min_dist = float("inf")
            # The distance of path equals <shortest_path_from_s_to_u>
            # + <edge_weight_u_to_v> + <shortest_path_from_t_to_v>
            cut_list = get_cut_from_SPT(g, s_spt_tree, e)
            if len(cut_list) == 0:
                occurrence_empty_cut += 1
                continue
            for cut in cut_list:
                u = cut.source()
                v = cut.target()
                dist_s_to_u = s_dist_map[u]
                dist_u_to_v = g.edge_properties['weight'][cut]
                dist_v_to_t = t_dist_map[v]
                dist = dist_s_to_u + dist_u_to_v + dist_v_to_t
                # min_dist of specific edge removal
                if dist < min_dist:
                    min_dist = dist
            # The maximum min_dist of all edge removals
            if min_dist > max_min_distance:
                best_edge_to_remove = e
                max_min_distance = min_dist

        if occurrence_empty_cut == num_edge_of_st_path:
            iter_stop_indicator = True

        return best_edge_to_remove, iter_stop_indicator

