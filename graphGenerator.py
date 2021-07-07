import random
from networkx import *
import matplotlib.pyplot as plt


def get_random_graph(hsize):
    # graph generation
    honest_subgraph = erdos_renyi_graph(hsize, 0.8)
    for i in range(hsize):
        honest_subgraph.nodes[i]["type"] = 'honest'

    # largest connected component
    honest_subgraph = honest_subgraph.subgraph(max(nx.connected_components(honest_subgraph), key=len)).copy()
    diameter = algorithms.distance_measures.diameter(honest_subgraph)
    density = classes.function.density(honest_subgraph)
    honest_size = len(honest_subgraph)

    byzantine_size = (honest_size - 1) // 2  # number of byzantine nodes
    honest_subgraph = convert_node_labels_to_integers(honest_subgraph, first_label=byzantine_size)

    byzantine_subgraph = Graph()
    # adding nodes
    for i in range(byzantine_size):
        byzantine_subgraph.add_node(i, type='byzantine')

    total_size = byzantine_size + honest_size

    byzantine_output = []
    for i in range(byzantine_size):
        byzantine_output.append(i)

    G = compose(honest_subgraph, byzantine_subgraph)

    # byzantine connectivity
    for i in range(byzantine_size):
        for j in range(byzantine_size, byzantine_size + honest_size):
            if random.random() < 0.9:
                G.add_edge(i, j)

    # coloring graph
    colorList = []
    for node in G.nodes(data=True):
        if node[1]["type"] == 'byzantine':
            colorList.append("red")
        else:
            colorList.append("blue")

    # drawing graph
    draw_networkx(G, node_color=colorList)
    plt.savefig("random_graph.png")
    plt.clf()

    # adjacency list generation
    adjList = {}
    for i in range(byzantine_size + honest_size):
        adjList[i] = [n for n in G.neighbors(i)]

    return adjList, byzantine_output, total_size, diameter, density


def get_linear_graph(bsize):
    byzantine_size = bsize  # number of byzantine nodes
    honest_size = 2 * byzantine_size + 1  # number of honest nodes
    diameter = honest_size - 1
    total_size = byzantine_size + honest_size

    byzantine_output = []
    for i in range(byzantine_size):
        byzantine_output.append(i)

    # graph generation
    G = Graph()

    # coloring graph
    colorList = []
    for i in range(byzantine_size):
        colorList.append('r')

    for i in range(honest_size):
        colorList.append('b')

    # adding nodes
    for i in range(byzantine_size):
        G.add_node(i, type='byzantine')

    for i in range(honest_size):
        G.add_node(byzantine_size + i, type='honest')

    # adding edges
    for i in range(byzantine_size):
        for j in range(byzantine_size, byzantine_size + honest_size):
            if random.random() < 0.8:
                G.add_edge(i, j)

    for i in range(honest_size - 1):
        G.add_edge(byzantine_size + i, byzantine_size + i + 1)

    # drawing graph
    draw_networkx(G, node_color=colorList)
    plt.savefig("linear_graph.png")
    plt.clf()

    # adjacency list generation
    adjList = {}

    for i in range(byzantine_size + honest_size):
        adjList[i] = [n for n in G.neighbors(i)]

    density = 2*honest_size/((honest_size-1)*honest_size)

    return adjList, byzantine_output, total_size, diameter, density

