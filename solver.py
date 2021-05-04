import networkx as nx

import MVE_solver
from parse import read_input_file, write_output_file
from utils import is_valid_solution, calculate_score
import sys
from os.path import basename, normpath
import glob
import MVE_solver as MVE
import MVN

def solve(g):
    """
    Args:
        G: networkx.Graph
    Returns:
        c: list of cities to remove
        k: list of edges to remove
    """
    size = g.num_vertices()
    if size >= 20 and size <= 30:
        max_cities = 1
        max_roads = 15
    elif size > 30 and size <= 50:
        max_cities = 3
        max_roads = 50
    elif size > 50 and size <= 100:
        max_cities = 5
        max_roads = 100

    t = g.vertex(g.num_vertices() - 1)
    mvn_solver = MVN.MVNSolver(t)
    mve_solver = MVE.MVE_solver(t)
    c = mvn_solver.solve(g, max_cities)
    k = mve_solver.solve(g, max_roads)
    if len(c) < max_cities:
        c1 = mvn_solver.solve(g, max_cities - len(c))
        c.extend(c1)

    g.set_edge_filter(None)
    g.set_vertex_filter(None)
    return c, k


if __name__ == '__main__':
    types = ["small", "medium", "large"]
    for type in types:
        for i in range(1, 10):
            path = f"inputs/{type}/{type}-{i}.in"
            G = read_input_file(path)
            G = MVE_solver.nx2gt(G)
            c, k = solve(G)
            assert is_valid_solution(G, c, k)
            print(f"{i}th input: len(c):{len(c)}, len(k):{len(k)}")
            print("Shortest Path Difference: {}".format(calculate_score(G, c, k)))
            write_output_file(G, c, k, f"outputs/{type}/{type}-{i}.out")

# Here's an example of how to run your solver.
# Usage: python3 solver.py test.in

# if __name__ == '__main__':
#     assert len(sys.argv) == 2
#     path = sys.argv[1]
#     G = read_input_file(path)
#     c, k = solve(G)
#     assert is_valid_solution(G, c, k)
#     print("Shortest Path Difference: {}".format(calculate_score(G, c, k)))
#     write_output_file(G, c, k, 'outputs/small-1.out')


# For testing a folder of inputs to create a folder of outputs, you can use glob (need to import it)
# if __name__ == '__main__':
#     inputs = glob.glob('inputs/*')
#     for input_path in inputs:
#         output_path = 'outputs/' + basename(normpath(input_path))[:-3] + '.out'
#         G = read_input_file(input_path)
#         c, k = solve(G)
#         assert is_valid_solution(G, c, k)
#         distance = calculate_score(G, c, k)
#         write_output_file(G, c, k, output_path)
