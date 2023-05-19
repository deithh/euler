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

    def _generate(self, n: int, factor: float) -> list[list[int]]:
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
        return self.a_mat2a_list(a_mat)
    
    @staticmethod
    def a_mat2a_list(a_mat: list[list[int]]) -> list[list[int]]:
        a_list = []
        for i in range(len(a_mat)):
            adjacencies = []
            for j in range(len(a_mat[i])):
                if a_mat[i][j] == 1:
                    adjacencies.append(j)
            a_list.append(adjacencies)
        return a_list

    def isolate_node(self) -> int:
        n = len(self.graph)
        node = random.randint(1, n) - 1
        self.graph[node] = []
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
        self.graph = self.a_mat2a_list(a_mat)

    def _input_graph(self):  # -> bool | list[list[int]]:
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

        return self.a_mat2a_list(a_mat)


    def is_eulerian(self) -> bool:
        for row in self.graph:
            if len(row)%2 != 0:
                return False
        return True

    def show(self):
        print("adjacency matrix: ")
        for row, nodes in enumerate(self.graph):
            print(f"{row}: {nodes}")
    

    def euler_cycle(self):
        if not self.is_eulerian():
            print("graph is not eulerian.")
            return
        cycle = []
        self._euler_cycle(node = 0, ptrs = [0] * len(self.graph), used = set(), cycle = cycle)
        print(f"found euler cycle: {cycle}")

    def _euler_cycle(self, node, ptrs, used, cycle):
        while ptrs[node] < len(self.graph[node]):
            next_ = self.graph[node][ptrs[node]]
            ptrs[node]+=1
            if (next_, node) in used:
                continue
            used.add((next_, node))
            used.add((node, next_))

            self._euler_cycle(node = next_, ptrs = ptrs, used = used, cycle = cycle)


        cycle.append(node)

    def ham_cycle(self, mode):
        cycle = [0] * len(self.graph)
        nb = [0]
        self._ham_cycle(node = 0, visited = [0] * len(self.graph), cycle = cycle, mode = mode,nb = nb)
        if mode == "count":
            print(*nb, end = "")

    def _ham_cycle(self, node, visited, cycle, nb, mode, ptr = 0): # 0 is set as starting point
        cycle[ptr] = node
        ptr +=1
        if ptr == len(self.graph):
            for next_ in self.graph[node]:
                if next_ == 0:
                    nb[0] += 1
                    if mode == 'all':
                        print(f"cycle: {cycle+[0]}")
        else:
            visited[node] = 1
            for next_ in self.graph[node]:
                if visited[next_] == 0:
                    self._ham_cycle(next_, visited, cycle, nb, mode, ptr)
            visited[node] = 0
        ptr -=1


g = Graph()
g.init_edges(.3, False, 12)
g.isolate_node()
g.ham_cycle("all")

