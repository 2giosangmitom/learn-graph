from typing import Dict, List

# A path through a graph is a sequence of nodes that are connected by edges.
# Paths have directionality, even on undirected graph.


# Minimal implementation of a adjacency-list representation graph
class Edge:
    def __init__(self, from_node: int, to_node: int, weight: float):
        self.from_node = from_node
        self.to_node = to_node
        self.weight = weight


class Node:
    def __init__(self, index: int):
        self.index = index
        self.edges: Dict[int, Edge] = {}

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

    def is_edge(self, a: int, b: int) -> bool:
        if a < 0 or a >= self.num_nodes:
            raise IndexError
        if b < 0 or b >= self.num_nodes:
            raise IndexError
        return b in self.nodes[a].edges


# List of nodes
def check_node_valid(g: Graph, path: List[int]) -> bool:
    num_nodes = len(path)
    if num_nodes == 0:
        return True
    prev_node = path[0]
    if prev_node < 0 or prev_node >= g.num_nodes:
        return False
    for step in range(1, num_nodes):
        next_node = path[step]
        if not g.is_edge(prev_node, next_node):
            return False
        prev_node = next_node
    return True


g = Graph(4)
g.insert_edge(0, 1, 1.0)
g.insert_edge(1, 2, 3.0)
g.insert_edge(2, 3, 2.0)
print(check_node_valid(g, [0, 1, 3]))  # False
print(check_node_valid(g, [0, 1, 2, 3]))  # True


# List of edges
def check_node_valid_edge(g: Graph, path: List[Edge]) -> bool:
    if len(path) == 0:
        return True

    prev_node = path[0].from_node
    if prev_node < 0 or prev_node >= g.num_nodes:
        return False

    for edge in path:
        if edge.from_node != prev_node:
            return False
        next_node = edge.to_node
        if not g.is_edge(prev_node, next_node):
            return False
        prev_node = next_node

    return True


edges = [g.nodes[0].edges[1], g.nodes[1].edges[2]]
print(check_node_valid_edge(g, edges))  # True


# List of previous nodes
def check_last_path_valid(g: Graph, last: List[int]) -> bool:
    if len(last) != g.num_nodes:
        return False
    for to_node, from_node in enumerate(last):
        if from_node != -1 and not g.is_edge(from_node, to_node):
            return False
    return True


prev_node_lists = [-1, 0, 1, 2]
print(check_last_path_valid(g, prev_node_lists))  # True


# Translate a previous-node list into a list of nodes
def make_node_path_from_last(last: List[int], dest: int) -> List[int]:
    reversed_path = []
    current = dest

    while current != -1:
        reversed_path.append(current)
        current = last[current]

    path = list(reversed(reversed_path))
    return path


print(make_node_path_from_last([-1, 0, 1, 2, 2, 0, 5, 0, 5, 8], 4))
print(make_node_path_from_last([-1, 0, 4, 1, 0], 2))

graph = Graph(4)
graph.insert_edge(0, 1, 4.0)
graph.insert_edge(0, 2, 2.0)
graph.insert_edge(1, 3, 2.0)
graph.insert_edge(2, 3, 2.0)

path1 = [-1, -1, 0, 2]
path2 = [-1, 0, -1, 1]


def calculate_cost(g: Graph, last: List[int]):
    if not check_last_path_valid(g, last):
        raise BaseException("Oi doi oi")

    cost = 0.0

    for curr, prev in enumerate(last):
        if prev == -1:
            continue
        cost += g.nodes[prev].edges[curr].weight

    return cost


print(calculate_cost(graph, path1))  # 4.0
print(calculate_cost(graph, path2))  # 6.0
