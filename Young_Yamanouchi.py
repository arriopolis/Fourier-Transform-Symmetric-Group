import numpy as np
import itertools as it
from Permutation import Permutation,get_standard_form_from_table
from Young_tableaux import YoungDiagram,YoungTableau

def get_list_standard_tableau_numbers(yd, n, nums):
    assert isinstance(yd, YoungDiagram)
    assert n > 0 and n <= yd.n
    tabls = []
    for i in range(len(yd.l)):
        if len(nums[i]) < yd.l[i] and (i == 0 or len(nums[i]) < len(nums[i-1])):
            new_nums = [n.copy() for n in nums]
            new_nums[i].append(n)
            if n == yd.n: tabls.append(new_nums)
            else: tabls.extend(get_list_standard_tableau_numbers(yd, n+1, new_nums))
    return tabls

def get_list_young_tableaux(yd):
    return list(map(lambda x : YoungTableau(yd, x), get_list_standard_tableau_numbers(yd, 1, [[] for _ in range(yd.n)])))

class YoungYamanouchi:
    def __init__(self, yd):
        assert isinstance(yd, YoungDiagram)
        self.yd = yd
        yts = get_list_young_tableaux(yd)
        tms = []
        for i in range(1,yd.n):
            tm = np.zeros((len(yts), len(yts)))
            for col,yt in enumerate(yts):
                yi = [i in r for r in yt.nums].index(True)
                xi = yt.nums[yi].index(i)
                yj = [i+1 in r for r in yt.nums].index(True)
                xj = yt.nums[yj].index(i+1)
                dy = yj - yi
                dx = xj - xi
                axial_dist = dx - dy
                tm[col,col] = 1/axial_dist
                if abs(axial_dist) != 1:
                    new_yt = yt.copy()
                    new_yt.nums[yi][xi] = i+1
                    new_yt.nums[yj][xj] = i
                    row = yts.index(new_yt)
                    tm[row,col] = np.sqrt(1 - 1 / np.square(axial_dist))
            tms.append(tm)
        self.repr = {}
        for func in it.permutations(range(1,yd.n+1)):
            p = get_standard_form_from_table(func)
            tp = p.get_neighboring_transposition_product()
            m = np.eye(len(yts))
            for i,_ in tp.cycles:
                m = m @ tms[i-1]
            self.repr[p] = m

    def __str__(self):
        s = ["Diagram:\n{}\n".format(str(self.yd))]
        for p,m in self.repr.items():
            s.append("{}\n{}\n".format(p,m))
        return '\n'.join(s)

if __name__ == "__main__":
    yd = YoungDiagram([2,1])
    print(YoungYamanouchi(yd))
