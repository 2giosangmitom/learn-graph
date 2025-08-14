from typing import List, Dict
from queue import Queue


class Node:
    def __init__(self, index: int):
        self.index = index
        self.edges: Dict[int, Node] = {}


class Edge:
    def __init__(self, from_node: int, to_node: int, weight: float):
        self.from_node = from_node
        self.to_node = to_node
        self.weight = weight


class Graph:
    def __init__(self, num_nodes: int):
        self.num_nodes = num_nodes
        self.nodes: List[Node] = [Node(i) for i in range(num_nodes)]

    def insert_edge(self, from_node: int, to_node: int, weight: float):
        self.nodes[from_node].edges[to_node] = Edge(from_node, to_node, weight)


def bfs(g: Graph, start: int):
    seen = [False] * g.num_nodes
    last = [-1] * g.num_nodes
    pending = Queue()

    pending.put(start)
    seen[start] = True

    while not pending.empty():
        index = pending.get()
        current: Node = g.nodes[index]

        for edge in list(current.edges.values()):
            neighbor = edge.to_node
            if not seen[neighbor]:
                pending.put(neighbor)
                seen[neighbor] = True
                last[neighbor] = index

    return last


#     1 -- 2 -- 3
#   /        \
# 0           4
g = Graph(5)
g.insert_edge(0, 1, 1.0)
g.insert_edge(1, 2, 1.0)
g.insert_edge(2, 3, 1.0)
g.insert_edge(2, 4, 1.0)
print(bfs(g, 0))

#     1 --- 2 -- 3
#   /    /    \
# 0 -- 5 -- 6  4
# |      \  |  |
# 7 ------ 8 - 9
g2 = Graph(10)
g2.insert_edge(0, 1, 1.0)
g2.insert_edge(0, 7, 1.0)
g2.insert_edge(0, 5, 1.0)
g2.insert_edge(1, 2, 1.0)
g2.insert_edge(2, 3, 1.0)
g2.insert_edge(2, 5, 1.0)
g2.insert_edge(5, 6, 1.0)
g2.insert_edge(6, 8, 1.0)
g2.insert_edge(5, 8, 1.0)
g2.insert_edge(2, 4, 1.0)
g2.insert_edge(4, 9, 1.0)
g2.insert_edge(8, 9, 1.0)
print(bfs(g2, 0))
