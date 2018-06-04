import numpy as np
np.set_printoptions(linewidth=200)
import itertools as it
from scipy.misc import factorial
from Permutation import Permutation,get_standard_form_from_table
from Young_tableaux import YoungDiagram,YoungTableau
from Young_Yamanouchi import YoungYamanouchi

def get_list_integer_partitions(n, max = float("Inf")):
    assert n > 0
    parts = []
    if n <= max: parts.append([n])
    for i in reversed(range(1,min(n,max+1))):
        parts.extend(map(lambda x : [i] + x, get_list_integer_partitions(n-i, max=i)))
    return parts

def get_list_young_diagrams(n):
    return list(map(YoungDiagram, get_list_integer_partitions(n)))

class FourierTransform:
    def __init__(self, n):
        assert n > 0
        self.n = n
        YYs = {yd : YoungYamanouchi(yd) for yd in get_list_young_diagrams(n)}
        col = 0
        fact_n = int(factorial(n))
        self.matrix = np.zeros((fact_n, fact_n))
        for func in it.permutations(range(1,n+1)):
            p = get_standard_form_from_table(func)
            row = 0
            for yd,YY in YYs.items():
                dim = list(YY.repr.values())[0].shape[0]
                for i in range(dim):
                    for j in range(dim):
                        self.matrix[row,col] = np.sqrt(dim / fact_n) * YY.repr[p][i][j]
                        row += 1
            col += 1

    def __str__(self):
        return str(self.matrix)

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 1: n = 3
    else: n = int(sys.argv[1])
    print("Fourier transform of S{}:".format(n))
    U = FourierTransform(n)
    print(U)
    print("Maximal entry-wise difference from unitarity:", np.max(np.max(np.abs(U.matrix @ U.matrix.conj().T - np.eye(U.matrix.shape[0])))))
