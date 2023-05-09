#import networkx as nx
#import matplotlib.pyplot as plt
import numpy as np
import math
import random


class Graph:

    def __init__(self) -> None:
        self.graph = None
        self.factor = None
        self.n = None

    def init_edges(self, factor: float, user=False, n: int = None) -> None:
        self.factor = factor
        self.n = n
        if not user:
            self.graph = self._generate(n=n, factor=factor)
            return
        if a_mat := self._input_graph():
            self.graph = a_mat

    def new_edges(self):
        self.graph = self._generate(n=len(self.graph), factor=self.factor)

    @staticmethod
    def _generate(n: int, factor: float) -> list[list[int]]:
        # generates random connected graph with hamilton cycle
        possible_edges = n * (n - 1) / 2
        fill_edges = math.floor(factor * possible_edges) - n
        a_mat = [[0 for _ in range(n)] for _ in range(n)]

        nodes = [i for i in range(n)]
        np.random.shuffle(nodes)
        last = nodes[-1]
        for node in nodes:
            a_mat[last][node] = 1
            a_mat[node][last] = 1
            last = node

        for i in range(fill_edges):
            while 1:
                a, b = random.choice(nodes), random.choice(nodes)
                if a_mat[a][b] != 1 and a != b:
                    a_mat[a][b] = 1
                    a_mat[b][a] = 1
                    break
        return a_mat

    def isolate_node(self) -> int:
        n = len(self.graph)
        node = random.randint(1, n) - 1

        for i in range(n):
            self.graph[i][node] = 0
            self.graph[node][i] = 0
        return node

    def generate_eulerian(self, n=None, factor=None) -> None:
        if n is None:
            n = self.n
        if factor is None:
            factor = self.factor
        possible_edges = n * (n - 1) / 2
        fill_edges = math.floor(factor * possible_edges) - n
        if fill_edges - 1 < 0:
            input("Cant do this [any]:")
        a_mat = [[0 for _ in range(n)] for _ in range(n)]

        nodes = [i for i in range(n)]
        np.random.shuffle(nodes)
        last = nodes[-1]
        end_of_cycle = last
        nodes = nodes[:-1]
        for node in nodes:
            a_mat[last][node] = 1
            a_mat[node][last] = 1
            last = node

        for i in range(fill_edges - 1):
            while 1:
                next = random.choice(nodes)
                if a_mat[last][next] != 1 and last != next:
                    if i == fill_edges - 2 and next == end_of_cycle or a_mat[next][end_of_cycle]:
                        continue
                    a_mat[last][next] = 1
                    a_mat[next][last] = 1
                    last = next
                    break
        a_mat[last][end_of_cycle] = 1
        a_mat[end_of_cycle][last] = 1
        self.graph = a_mat

    @staticmethod
    def _input_graph():  # -> bool | list[list[int]]:
        a_mat = []
        n = int(input("Set size [int]: "))
        print("input adjacency matrix:")
        for i in range(n):
            try:
                temp = list(map(int, input().split()))
                if len(temp) != n:
                    print("Invalid size.")
                    return False
                a_mat.append(temp)
            except ValueError:
                print("One or more not integer values.")
                return False

        return a_mat

    # def plot(self) -> None:
    #     mat = np.array(self.graph)
    #     G = nx.Graph(mat)
    #     pos = nx.circular_layout(G)
    #     nx.draw(G, pos=pos, with_labels=True)
    #     plt.show()
    #
    # def is_eulerian(self) -> bool:
    #     mat = np.array(self.graph)
    #     G = nx.Graph(mat)
    #     return nx.is_eulerian(G)

    def show(self):
        print("adjacency matrix: ")
        for row in self.graph:
            print(row)
