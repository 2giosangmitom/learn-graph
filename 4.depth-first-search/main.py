from typing import List


class Node:
    def __init__(self, index: int):
        self.index = index
        self.edges = {}


class Edge:
    def __init__(self, from_node: int, to_node: int, weight: float):
        self.from_node = from_node
        self.to_node = to_node
        self.weight = weight


class Graph:
    def __init__(self, num_nodes: int):
        self.num_nodes = num_nodes
        self.nodes = [Node(i) for i in range(num_nodes)]

    def insert_edge(self, from_node: int, to_node: int, weight: float):
        self.nodes[from_node].edges[to_node] = Edge(from_node, to_node, weight)


def dfs(g: Graph, ind: int, seen: List[bool], last: List[int]):
    seen[ind] = True
    current = g.nodes[ind]

    for edge in current.edges.values():
        neighbor = edge.to_node
        if not seen[neighbor]:
            last[neighbor] = ind
            dfs(g, neighbor, seen, last)


g = Graph(4)
g.insert_edge(0, 1, 2)
g.insert_edge(1, 2, 3)
g.insert_edge(2, 3, 4)

last = [-1] * 4
dfs(g, 1, [False] * 4, last)
print(last)
