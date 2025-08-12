from typing import List, Dict


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


def dfs_cc_helper(g: Graph, ind: int, component: List[int], curr_comp: int):
    component[ind] = curr_comp
    current = g.nodes[ind]

    for edge in current.edges.values():
        neighbor = edge.to_node
        if component[neighbor] == -1:
            dfs_cc_helper(g, neighbor, component, curr_comp)


def dfs_cc(g: Graph) -> List[int]:
    component = [-1] * g.num_nodes
    curr_comp = 0

    for ind in range(g.num_nodes):
        if component[ind] == -1:
            dfs_cc_helper(g, ind, component, curr_comp)
            curr_comp += 1

    return component


g = Graph(4)
g.insert_edge(0, 1, 2)
g.insert_edge(1, 2, 3)
g.insert_edge(2, 3, 4)

last = [-1] * 4
dfs(g, 1, [False] * 4, last)
print(last)

print(dfs_cc(g))

g2 = Graph(8)
g2.insert_edge(0, 4, 1.0)
g2.insert_edge(0, 1, 2.0)
g2.insert_edge(1, 2, 3.0)
g2.insert_edge(3, 7, 5.0)
g2.insert_edge(5, 6, 8.0)

print(dfs_cc(g2))
