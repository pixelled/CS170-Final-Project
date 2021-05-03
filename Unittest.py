import unittest
import parse
import os
import networkx as nx
import MVE_solver
import graph_tool.topology as gt_topo
import graph_tool as gt
import graph_tool.draw as gt_draw
import graph_tool.stats as gt_stat

class MyTestCase(unittest.TestCase):
    def get_graph_sample(self):

        # Modify the idx if you want to try another sample
        idx = 0
        # parse the sample
        small_input_path = os.getcwd() + "/inputs" + "/small"
        inputs = os.listdir(small_input_path)
        input = small_input_path + "/" + inputs[idx]
        g_nx = parse.read_input_file(input)
        g = MVE_solver.nx2gt(g_nx)
        return g

    def get_test_sample(self):
        inputs = os.getcwd() + "/test.in"
        g_nx = parse.read_input_file(inputs)
        gt = MVE_solver.nx2gt(g_nx)
        return gt

    def test_get_test_sample(self):
        inputs = os.getcwd() + "/test_2.in"
        g_nx = parse.read_input_file(inputs)
        g = MVE_solver.nx2gt(g_nx)
        max_dist = -1
        edge_to_remove = None
        best_path = None
        for e in g.edges():
            source = e.source()
            target = e.target()
            g.remove_edge(e)
            _, path = gt_topo.shortest_path(g, g.vertex(0), g.vertex(g.num_vertices() - 1), weights=g.edge_properties['weight'])
            dist = gt_topo.shortest_distance(g, g.vertex(0), g.vertex(g.num_vertices() - 1), weights=g.edge_properties['weight'])
            print(dist)
            #gt_draw.graph_draw(g, vertex_text=g.vertex_index)
            if dist > max_dist:
                max_dist = dist
                edge_to_remove = (source, target)
                best_path = path
            g.add_edge(source, target)

        print([x for x in best_path])
        print(str(edge_to_remove))
        print(max_dist)

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
        print([str(e) for e in e_list])

    def test_add_edge_list(self):
        small_input_path = os.getcwd() + "/inputs" + "/small"
        inputs = os.listdir(small_input_path)
        input = small_input_path + "/" + inputs[0]
        g_nx = parse.read_input_file(input)
        g = MVE_solver.nx2gt(g_nx)
        v_list, e_list = gt_topo.shortest_path(g, g.vertex(0), g.vertex(13), weights=g.edge_properties['weight'])

        new_g = gt.Graph()
        new_g.add_vertex(g.num_vertices())
        new_g.add_edge_list(set(e_list))

        for e in new_g.edges():
            print(e)
            a = list(e)[1]
            b = e

    def test_cut(self):
        g = self.get_graph_sample()

        st_path = MVE_solver.get_shortest_st_path(g)
        print([e for e in st_path])

    def test_draw_graph(self):
        g = self.get_graph_sample()
        spt = MVE_solver.get_shortest_path_tree(g, g.vertex(0))
        gt_draw.graph_draw(spt, vertex_text=spt.vertex_index)

    def test_get_cut(self):
        g = self.get_graph_sample()
        st_path = MVE_solver.get_shortest_st_path(g)
        spt, _ = MVE_solver.get_shortest_path_tree(g, g.vertex(0))

        e = st_path[0]
        cuts = MVE_solver.get_cut_from_SPT(g, spt, e)
        print([e for e in cuts])

    def test_short_distance(self):
        g = self.get_graph_sample()
        dist_map, pred_map = gt_topo.shortest_distance(g, g.vertex(0), weights=g.edge_properties['weight'], pred_map=True)

        print(dist_map.a)
        print(pred_map.a)
        list = [x for x in pred_map.a]
        zip_list = zip(list, [x for x in range(len(list))])
        print([x for x in zip_list])

    def test_mask(self):
        g = self.get_test_sample()
        print([x for x in g.edge_properties['weight']])
        best_edge_to_remove = MVE_solver.best_edge_to_remove(g)

        new_min_dist = gt_topo.shortest_distance(g, g.vertex(0), g.vertex(g.num_vertices() - 1),
                                                 weights=g.edge_properties['weight'])
        print(new_min_dist)
        pass

    def test_solver(self):
        g = self.get_test_sample()
        edge_to_remove = MVE_solver.solver(g, 15)
        gt_draw.graph_draw(g, vertex_text=g.vertex_index)
        print(gt_topo.shortest_distance(g, g.vertex(0), g.vertex(g.num_vertices() - 1), weights=g.edge_properties['weight']))
        print(edge_to_remove)
        pass


if __name__ == '__main__':
    unittest.main()


