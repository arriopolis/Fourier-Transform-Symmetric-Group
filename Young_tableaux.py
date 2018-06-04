class YoungDiagram:
    def __init__(self, l):
        assert isinstance(l, list)
        for i,x in enumerate(l[:-1]): assert x >= l[i+1]
        self.n = sum(l)
        self.l = l

    def __hash__(self):
        return hash((self.n,tuple(self.l)))

    def __eq__(self, other):
        assert isinstance(other, YoungDiagram)
        return self.n == other.n and len(self.l) == len(other.l) and all(x == y for x,y in zip(self.l,other.l))

    def __neq__(self, other):
        assert isinstance(other, YoungDiagram)
        return self.n != other.n or len(self.l) != len(other.l) or any(x != y for x,y in zip(self.l,other.l))

    def __str__(self, symbols = None):
        if symbols is None:
            symbols = [' ' * w for w in self.l]
        s = ['+' + '+'.join('-'*self.l[0]) + '+']
        for i,w in enumerate(self.l):
            s.append('|' + '|'.join(map(str,symbols[i])) + '|')
            s.append('+' + '+'.join('-'*w) + '+')
        return '\n'.join(s)

    def copy(self):
        return YoungDiagram(self.l.copy())

class YoungTableau:
    def __init__(self, diagram, nums):
        assert isinstance(diagram, YoungDiagram)
        for l,n in zip(diagram.l, nums): assert l == len(n)
        for n in nums:
            for i,m in enumerate(n[:-1]):
                assert m < n[i+1]
        for i in range(len(nums[0])):
            for j in range(len(nums)-1):
                if len(nums[j+1]) <= i: break
                assert nums[j][i] < nums[j+1][i]
        self.diagram = diagram
        self.nums = nums

    def __hash__(self):
        return hash((self.diagram, tuple(map(tuple,self.nums))))

    def __eq__(self, other):
        assert isinstance(other, YoungTableau)
        return self.diagram == other.diagram and all(all(x == y for x,y in zip(c,d)) for c,d in zip(self.nums, other.nums))

    def __neq__(self, other):
        assert isinstance(other, YoungTableau)
        return self.diagram != other.diagram and any(any(x != y for x,y in zip(c,d)) for c,d in zip(self.nums, other.nums))

    def __str__(self):
        return YoungDiagram.__str__(self.diagram, symbols = self.nums)

    def copy(self):
        return YoungTableau(self.diagram.copy(), [n.copy() for n in self.nums])

if __name__ == "__main__":
    yd = YoungDiagram([6,4,1])
    yt = YoungTableau(yd, [[1,2,3,4,5,6],[7,9,10,11],[8]])
    print(yt)
