# Minimal implementation of a adjacency-list representation graph
class Edge:
    def __init__(self, from_node: int, to_node: int, weight: float):
        self.from_node = from_node
        self.to_node = to_node
        self.weight = weight


class Node:
    def __init__(self, index: int):
        self.index = index
        self.edges = {}

    def add_edge(self, to_node: int, weight: float):
        self.edges[to_node] = Edge(self.index, to_node, weight)


class Graph:
    def __init__(self, num_nodes: int, undirected: bool = False):
        self.num_nodes = num_nodes
        self.undirected = undirected
        self.nodes = [Node(i) for i in range(num_nodes)]

    def insert_edge(self, from_node: int, to_node: int, weight: float):
        if from_node < 0 or from_node >= self.num_nodes:
            raise IndexError
        if to_node < 0 or to_node >= self.num_nodes:
            raise IndexError
        self.nodes[from_node].add_edge(to_node, weight)
        if self.undirected:
            self.nodes[to_node].add_edge(from_node, weight)

    def get_out_neighbors(self, index: int) -> set:
        if index < 0 or index >= self.num_nodes:
            raise IndexError
        neighbors = set()
        for edge in self.nodes[index].edges.values():
            neighbors.add(edge.to_node)
        return neighbors

    def get_in_neighbors(self, index: int) -> set:
        if index < 0 or index >= self.num_nodes:
            raise IndexError
        neighbors = set()
        for node in self.nodes:
            if index in node.edges:
                neighbors.add(node.index)
        return neighbors

    def get_out_degree(self, index: int) -> int:
        if index < 0 or index >= self.num_nodes:
            raise IndexError
        return len(self.nodes[index].edges)

    def get_in_degree(self, index: int) -> int:
        if index < 0 or index >= self.num_nodes:
            raise IndexError
        counter = 0
        for node in self.nodes:
            if index in node.edges:
                counter += 1
        return counter


# The neighbors of a directed graph has two main types: in-neighbors and out-neighbors
# The in-neighbors are all nodes that have edges with v as the destination. In other words,
# the edge is incomming from node v's perspective.
# The out-neighbors are all nodes to which v has an outgoing edge.

# The degree of a graph is the number of times edges connect to a node
# In directed graph, it has two types: in-degree and out-degree, and it similar to the neighbors concept
g = Graph(6)

g.insert_edge(0, 3, 1.0)
g.insert_edge(0, 4, 1.0)
g.insert_edge(0, 1, 1.0)

print(f"Out-neighbors of node 0 {g.get_out_neighbors(0)}")
print(f"In-neighbors of node 0 {g.get_in_neighbors(0)}")
print(f"In-neighbors of node 4 {g.get_in_neighbors(4)}")
print(f"Out-degree of node 0 {g.get_out_degree(0)}")
print(f"Out-degree of node 3 {g.get_out_degree(3)}")
print(f"In-degree of node 3 {g.get_in_degree(3)}")
print(f"In-degree of node 0 {g.get_in_degree(0)}")
