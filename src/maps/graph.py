import numpy as np
from scipy.sparse.csgraph import shortest_path

class Graph:
    def __init__(self, conn):
        self.p = list(conn.keys())
        self.M = np.zeros((len(self.p), len(self.p)))
        for c in conn:
            for c1 in conn[c]:
                i = self.p.index(c)
                j = self.p.index(c1[0])
                # print(c1[1])
                self.M[i, j] = c1[1]

    def find_path(self, p1, p2):
        i = self.p.index(p1)
        j = self.p.index(p2)
        D, Pr = shortest_path(self.M, directed=True, method='FW', return_predecessors=True)
        path = [j]
        k = j
        while Pr[i, k] != -9999:
            path.append(Pr[i, k])
            k = Pr[i, k]
        return [self.p[l] for l in path[::-1]], D[i, j]
    def find_path_2(p1, p2s, p3):
        # path = []
        paths12 = []
        for p2 in p2s:
            path2, d = self.find_path(p1, p2)
            paths12.append((p2, d, path2))
        paths23 = []
        for p2 in p2s:
            path3, d = self.find_path(p2, p3)
            paths23.append((p2, d, path3))
        paths123 = []
        for pp12 in paths12:
            for pp23 in paths23:
                if pp12[0] == pp23[0]:
                    paths123.append((pp12[0], pp12[1] + pp23[1], pp12[2] + pp23[2]))
        path = min(paths123, key=lambda x: x[1])
        return path[2], path[1], path[0]