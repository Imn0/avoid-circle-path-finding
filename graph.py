from node import Node
from queue import PriorityQueue
from tqdm import tqdm

class Graph:
    def __init__(self, num_of_vertices):
        self.v = num_of_vertices
        self.edges = [[-1 for i in range(num_of_vertices)] for j in range(num_of_vertices)]
        self.visited = []

    def add_edge(self, node1:Node, node2:Node, cost: float):
        self.edges[node1.index][node2.index] = cost
        self.edges[node2.index][node1.index] = cost

    def dijkstra(self, start_vertex, end_vertex):
        distances = [float('infinity')] * self.v
        distances[start_vertex] = 0
        visited = [False] * self.v

        for _ in tqdm(range(self.v)):
            min_distance = float('infinity')
            min_index = -1
            for i in range(self.v):
                if not visited[i] and distances[i] < min_distance:
                    min_distance = distances[i]
                    min_index = i

            visited[min_index] = True

            for i in range(self.v):
                if (
                    not visited[i]
                    and self.edges[min_index][i] != -1
                    and distances[i] > distances[min_index] + self.edges[min_index][i]
                ):
                    distances[i] = distances[min_index] + self.edges[min_index][i]

        path = []
        current_vertex = end_vertex

        while current_vertex != start_vertex:
            path.insert(0, current_vertex)
            for i in range(self.v):
                if (
                    self.edges[current_vertex][i] != -1
                    and distances[current_vertex] == distances[i] + self.edges[current_vertex][i]
                ):
                    current_vertex = i
                    break

        path.insert(0, start_vertex)
        return path, distances[end_vertex]

