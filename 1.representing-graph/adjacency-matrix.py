# Adjacency matrix representation of a graph
class Graph:
    def __init__(self, num_nodes: int, undirected: bool = False):
        self.num_nodes = num_nodes
        self.undirected = undirected
        self.connections = [
            [0.0] * num_nodes for _ in range(num_nodes)
        ]  # A '0' indicate there are no edge here, other are consider the weight

    def get_edge(self, from_node: int, to_node: int) -> float:
        if from_node < 0 or from_node >= self.num_nodes:
            raise IndexError
        if to_node < 0 or to_node >= self.num_nodes:
            raise IndexError
        return self.connections[from_node][to_node]

    def set_edge(self, from_node: int, to_node: int, weight: float):
        if from_node < 0 or from_node >= self.num_nodes:
            raise IndexError
        if to_node < 0 or to_node >= self.num_nodes:
            raise IndexError
        self.connections[from_node][to_node] = weight
        if self.undirected:
            self.connections[to_node][from_node] = weight


g = Graph(5, False)
g.set_edge(0, 1, 1.0)
g.set_edge(0, 3, 3.0)
g.set_edge(0, 4, 3.0)
g.set_edge(1, 2, 2.0)
g.set_edge(1, 4, 1.0)
g.set_edge(3, 4, 3.0)
g.set_edge(4, 2, 3.0)
g.set_edge(4, 3, 3.0)
print(g.connections)
