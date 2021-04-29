import numpy as np
from parse import *

def init_path(num_v):
    """
    Initial a path from 's' to 't'.
    """
    len_path = np.random.randint(1, num_v - 1)
    path = np.array([x for x in range(1, num_v-1)])
    np.random.shuffle(path)
    path = path[0:len_path]
    return path


def init_graph(num_v, p_sparse, path):
    graph = np.random.randint(1, 50, size=(num_v, num_v))

    # copy of weights of the path from s to t
    tmp_mat = np.zeros(shape=(num_v, num_v))
    tmp_mat[0, path[0]] = graph[0, path[0]]
    tmp_mat[path[len(path)-1], num_v-1] = graph[path[len(path)-1], num_v-1]
    for i in range(0, len(path)-1):
        x = path[i]
        y = path[i+1]
        tmp_mat[x,y] = graph[x,y]

    # make graph sparse
    sparse_mat = np.random.binomial(n=1, size=(num_v, num_v), p=p_sparse)
    graph = np.multiply(graph, sparse_mat)

    graph += tmp_mat.astype(int)
    # Make matrix symmetric(unweighted graph)
    graph += graph.T
    return graph


def mat2output(graph):
    output = ""
    n = np.size(graph[0,:])
    output += str(n)
    output += "\n"
    for i in range(n):
        for j in range(i+1, n):
            if graph[i, j] != 0:
                output += str(i) + " " + str(j) + " " + str(graph[i, j]) + "\n"

    return output


if __name__ == '__main__':
    num_v = 30
    p_sparse = 0.1
    list_path = init_path(num_v)
    graph = init_graph(num_v, p_sparse, list_path)
    output = mat2output(graph)
    text_file = open(f"{num_v}.in", "w")
    text_file.write(output)
    text_file.close()
    G = read_input_file(f"{num_v}.in")
