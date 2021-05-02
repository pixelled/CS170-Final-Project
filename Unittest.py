import unittest
import parse
import os
import networkx as nx
import MVE_solver
import graph_tool.topology as gt_topo


class MyTestCase(unittest.TestCase):

    def test_get_nx(self):
        small_input_path = os.getcwd() + "/inputs" + "/small"
        inputs = os.listdir(small_input_path)
        input = small_input_path + "/" + inputs[0]
        g_nx = parse.read_input_file(input)
        print(len(g_nx.edges))
        g = MVE_solver.nx2gt(g_nx)
        print(g.edge_properties)
        v_list, e_list = gt_topo.shortest_path(g, g.vertex(0), g.vertex(13), weights=g.edge_properties['weight'])
        print([str(v) for v in v_list])


if __name__ == '__main__':
    unittest.main()


