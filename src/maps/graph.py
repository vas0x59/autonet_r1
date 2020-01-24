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