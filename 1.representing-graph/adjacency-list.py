from typing import Union


# Edge (or link) in a graph is a connection between two nodes.
class Edge:
    def __init__(self, from_node: int, to_node: int, weight: float):
        self.from_node = from_node  # Index of the node where the edge starts
        self.to_node = to_node  # Index of the node where the edge ends
        self.weight = (
            weight  # Weight of the edge, can be used to represent distance or cost
        )


# Node in a graph is an entity that can have edges to other nodes.
class Node:
    def __init__(self, index: int, label=None):
        self.index = index  # Index of the node in the graph
        self.edges = {}  # Dictionary to hold edges, where key is the neighbor node index and value is the Edge object
        self.label = label  # Optional label for the node, can be used for identification or categorization

    def num_edges(self) -> int:
        return len(self.edges)

    def get_edge(self, neightbor: int) -> Union[Edge, None]:
        return self.edges.get(neightbor)

    def add_edge(self, neighbor: int, weight: float):
        self.edges[neighbor] = Edge(self.index, neighbor, weight)

    def remove_edge(self, neighbor: int):
        if neighbor in self.edges:
            del self.edges[neighbor]

    def get_edge_list(self) -> list:
        return list(self.edges.values())

    def get_sorted_edges_list(self) -> list:
        result = []
        neighbors = sorted(self.edges.keys())

        for n in neighbors:
            result.append(self.edges[n])

        return result


# Graph is a collection of nodes and edges that connect them.
class Graph:
    def __init__(self, num_nodes: int, undirected: bool = False):
        self.num_nodes = num_nodes  # Total number of nodes in the graph
        self.undirected = undirected  # Indicate the graph is undirected or directed
        self.nodes = [Node(j) for j in range(num_nodes)]  # Initialize nodes

    def get_edge(self, from_node: int, to_node: int) -> Union[Edge, None]:
        if from_node < 0 or from_node >= self.num_nodes:
            raise IndexError
        if to_node < 0 or to_node >= self.num_nodes:
            raise IndexError
        return self.nodes[from_node].get_edge(to_node)

    def is_edge(self, from_node: int, to_node: int) -> bool:
        return self.get_edge(from_node, to_node) is not None

    def make_edge_list(self) -> list:
        all_edges = []
        for node in self.nodes:
            for edge in node.edges.values():
                all_edges.append(edge)
        return all_edges

    def insert_edge(self, from_node: int, to_node: int, weight: float):
        if from_node < 0 or from_node >= self.num_nodes:
            raise IndexError
        if to_node < 0 or to_node >= self.num_nodes:
            raise IndexError
        self.nodes[from_node].add_edge(to_node, weight)
        if self.undirected:
            self.nodes[to_node].add_edge(from_node, weight)

    def remove_edge(self, from_node: int, to_node: int):
        if from_node < 0 or from_node >= self.num_nodes:
            raise IndexError
        if to_node < 0 or to_node >= self.num_nodes:
            raise IndexError
        self.nodes[from_node].remove_edge(to_node)
        if self.undirected:
            self.nodes[to_node].remove_edge(from_node)


g = Graph(5, False)
g.insert_edge(0, 1, 1.0)
g.insert_edge(0, 3, 1.0)
g.insert_edge(0, 4, 3.0)
g.insert_edge(1, 2, 2.0)
g.insert_edge(1, 4, 1.0)
g.insert_edge(3, 4, 3.0)
g.insert_edge(4, 2, 3.0)
g.insert_edge(4, 3, 3.0)

# Print the graph
result = []
for node in g.nodes:
    to_nodes = []
    for edge in node.edges.keys():
        to_nodes.append(edge)
    result.append(to_nodes)
print(result)


def make_graph_copy(g: Graph) -> Graph:
    res = Graph(g.num_nodes, g.undirected)
    for node in g.nodes:
        res.nodes[node.index].label = node.label
        for edge in node.edges.values():
            res.insert_edge(edge.from_node, edge.to_node, edge.weight)
    return res


# Cloned graph
g2 = make_graph_copy(g)
result = []
for node in g2.nodes:
    to_nodes = []
    for edge in node.edges.keys():
        to_nodes.append(edge)
    result.append(to_nodes)
print(result)
