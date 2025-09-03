from typing import Dict, Union
import math


class Edge:
    def __init__(self, from_node: int, to_node: int, weight: int):
        self.from_node = from_node
        self.to_node = to_node
        self.weight = weight


class Node:
    def __init__(self, index: int):
        self.index = index
        self.edges: Dict[int, Edge] = {}


class Graph:
    def __init__(self, num_nodes):
        self.nodes = [Node(i) for i in range(num_nodes)]
        self.num_nodes = num_nodes

    def insert_edge(self, from_node: int, to_node: int, weight: float):
        self.nodes[from_node].edges[to_node] = Edge(from_node, to_node, weight)


class HeapItem:
    def __init__(self, value, priority: float):
        self.value = value
        self.priority = priority

    def __lt__(self, other):
        return self.priority < other.priority

    def __gt__(self, other):
        return self.priority > other.priority


class PriorityQueue:
    def __init__(self, size=100, min_heap=False):
        self.array_size = size
        self.heap_array: list = [None] * (
            size + 1
        )  # <-- extra slot for 1-based indexing
        self.is_min_heap = min_heap
        self.last_index = 0
        self.indices = {}

    def size(self):
        return self.last_index

    def is_empty(self):
        return self.last_index == 0

    def in_queue(self, value):
        return value in self.indices

    def get_priority(self, value: int) -> Union[float, None]:
        if value not in self.indices:
            return None
        ind = self.indices[value]
        return self.heap_array[ind].priority

    def _elements_inverted(self, parent: int, child: int):
        if parent <= 0 or child > self.last_index or self.heap_array[child] is None:
            return False
        if self.is_min_heap:
            return self.heap_array[parent] > self.heap_array[child]
        return self.heap_array[parent] < self.heap_array[child]

    def _swap_element(self, index1: int, index2: int):
        item1 = self.heap_array[index1]
        item2 = self.heap_array[index2]
        self.heap_array[index2] = item1
        self.heap_array[index1] = item2

        self.indices[item1.value] = index2
        self.indices[item2.value] = index1

    def _propagate_up(self, index: int):
        while index > 1:
            parent = index // 2
            if self._elements_inverted(parent, index):
                self._swap_element(parent, index)
                index = parent
            else:
                break

    def _propagate_down(self, index: int):
        while True:
            swap = index
            left = 2 * index
            right = 2 * index + 1

            if self._elements_inverted(swap, left):
                swap = left
            if self._elements_inverted(swap, right):
                swap = right

            if index != swap:
                self._swap_element(index, swap)
                index = swap
            else:
                break

    def enqueue(self, value, priority: float):
        if value in self.indices:
            self.update_priority(value, priority)
            return

        if self.last_index == self.array_size:
            old_array: list = self.heap_array
            self.heap_array = [None] * (self.array_size * 2 + 1)
            for i in range(self.last_index + 1):
                self.heap_array[i] = old_array[i]
            self.array_size = self.array_size * 2

        self.last_index += 1
        self.heap_array[self.last_index] = HeapItem(value, priority)
        self.indices[value] = self.last_index
        self._propagate_up(self.last_index)

    def dequeue(self):
        if self.last_index == 0:
            return None

        result: HeapItem = self.heap_array[1]
        new_top = self.heap_array[self.last_index]
        self.heap_array[1] = new_top
        if new_top is not None:
            self.indices[new_top.value] = 1

        self.heap_array[self.last_index] = None
        self.indices.pop(result.value)
        self.last_index -= 1

        self._propagate_down(1)

        return result.value

    def update_priority(self, value: int, priority: float):
        if value not in self.indices:
            return None

        index: int = self.indices[value]
        old_priority: float = self.heap_array[index].priority
        self.heap_array[index].priority = priority

        if self.is_min_heap:
            if priority < old_priority:
                self._propagate_up(index)
            else:
                self._propagate_down(index)
        else:
            if priority > old_priority:
                self._propagate_up(index)
            else:
                self._propagate_down(index)


def Dijkstra(g: Graph, start_index: int) -> list:
    cost: list = [math.inf] * g.num_nodes
    last: list = [-1] * g.num_nodes
    pq = PriorityQueue(min_heap=True)

    pq.enqueue(start_index, 0.0)
    for i in range(g.num_nodes):
        if i != start_index:
            pq.enqueue(i, math.inf)
    cost[start_index] = 0.0

    while not pq.is_empty():
        index = pq.dequeue()

        for edge in g.nodes[index].edges.values():
            new_cost = cost[index] + edge.weight
            if new_cost < cost[edge.to_node]:
                cost[edge.to_node] = new_cost
                last[edge.to_node] = index
                pq.update_priority(edge.to_node, new_cost)

    return last


g = Graph(5)
g.insert_edge(0, 1, 3.5)
g.insert_edge(0, 2, 0.5)
g.insert_edge(0, 3, 2.0)
g.insert_edge(1, 0, 2.5)
g.insert_edge(1, 4, 0.5)
g.insert_edge(2, 3, 1.0)
g.insert_edge(3, 4, 3.0)
g.insert_edge(3, 1, 0.5)
g.insert_edge(4, 1, 1.0)

print(Dijkstra(g, 0))
