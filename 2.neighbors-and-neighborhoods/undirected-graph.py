from typing import List, Set


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

    def get_edge_list(self) -> List[Edge]:
        return list(self.edges.values())


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

    def get_neighbors(self, index: int) -> Set[int]:
        if index < 0 or index >= self.num_nodes:
            raise IndexError
        neighbors = set()
        for edge in self.nodes[index].get_edge_list():
            neighbors.add(edge.to_node)
        return neighbors

    # Local clustering coefficient
    def clustering_coefficient(self, index: int) -> float:
        neighbors = self.get_neighbors(index)
        num_neighbors = len(neighbors)
        count = 0
        for n1 in neighbors:
            for edge in self.nodes[n1].get_edge_list():
                if edge.to_node > n1 and edge.to_node in neighbors:
                    count += 1
        total_possible = (num_neighbors * (num_neighbors - 1)) / 2.0
        if total_possible == 0.0:
            return 0.0
        return count / total_possible

    # There are two types of neighborhood sub-graph
    # Open sub-graph of node v is a graph of all node v's neighbors
    # Closed sub-graph of node v is a graph of all node v's neighbors and node v
    def make_neighborhood_subgraph(self, index: int, closed: bool):
        if not self.undirected:
            raise ValueError

        nodes_to_use = self.get_neighbors(index)
        if closed:
            nodes_to_use.add(index)

        # Sub-graph should use other indexes
        index_map = {}
        for new_index, old_index in enumerate(nodes_to_use):
            index_map[old_index] = new_index

        g_new = Graph(len(nodes_to_use), True)
        for n in nodes_to_use:
            for edge in self.nodes[n].get_edge_list():
                if edge.to_node in nodes_to_use and edge.to_node > n:
                    ind1_new = index_map[n]
                    ind2_new = index_map[edge.to_node]
                    g_new.insert_edge(ind1_new, ind2_new, edge.weight)

        return g_new


g = Graph(6, True)  # 0 -> 5
g.insert_edge(0, 3, 1.0)
g.insert_edge(0, 4, 1.0)
g.insert_edge(0, 1, 1.0)

g.insert_edge(1, 4, 2.0)
g.insert_edge(1, 2, 8.0)

g.insert_edge(2, 4, 1.0)
g.insert_edge(2, 5, 1.0)

g.insert_edge(5, 4, 1.0)

# Print neighbors of each nodes
for node in range(6):
    print(f"Neighbors of node {node} {g.get_neighbors(node)}")

g2 = Graph(3, True)
g2.insert_edge(0, 1, 1.0)
g2.insert_edge(0, 2, 1.0)
g2.insert_edge(1, 2, 1.0)
print(
    f"Clustering coefficient of node 0: {format(g2.clustering_coefficient(0), '.2f')}"
)

g3 = Graph(7, True)
g3.insert_edge(0, 4, 1.0)
g3.insert_edge(0, 1, 1.0)
g3.insert_edge(1, 5, 1.0)
g3.insert_edge(1, 6, 1.0)
g3.insert_edge(1, 2, 1.0)
g3.insert_edge(2, 3, 1.0)
g3.insert_edge(5, 6, 1.0)

# Print graph
for node in range(g3.num_nodes):
    print(f"{node}: {list(g3.nodes[node].edges.keys())}")

# Print sub-graph of 1
print("Sub-graph of node 1")
sub_graph = g3.make_neighborhood_subgraph(1, True)
for node in range(sub_graph.num_nodes):
    print(f"{node}: {list(sub_graph.nodes[node].edges.keys())}")
