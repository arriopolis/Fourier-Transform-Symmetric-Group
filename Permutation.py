def get_standard_form_from_table(func, singletons = False):
    n = len(func)
    todo = list(range(1,n+1))
    cycles = []
    while todo:
        x = todo.pop(0)
        cycle = [x]
        f = x
        while x != func[f-1]:
            f = func[f-1]
            todo.remove(f)
            cycle.append(f)
        if singletons or len(cycle) > 1:
            cycles.append(cycle)
    return Permutation(n, cycles)

class Permutation:
    def __init__(self, n, cycles):
        assert isinstance(cycles, list)
        for c in cycles: assert isinstance(c, list)
        self.n = n
        self.cycles = cycles

    def __eq__(self, other):
        assert isinstance(other, Permutation)
        return self.n == other.n and len(self.cycles) == len(other.cycles) \
            and all(len(c) == len(d) for c,d in zip(self.cycles,other.cycles)) \
            and all(all(x == y for x,y in zip(c,d)) for c,d in zip(self.cycles,other.cycles))

    def __neq__(self, other):
        assert isinstance(other, Permutation)
        return self.n != other.n or len(self.cycles) != len(other.cycles) \
            or any(len(c) != len(d) for c,d in zip(self.cycles,other.cycles)) \
            or any(any(x != y for x,y in zip(c,d)) for c,d in zip(self.cycles,other.cycles))

    def __hash__(self):
        return hash((self.n,tuple(map(tuple,self.cycles))))

    def __mul__(self, other):
        assert isinstance(other, Permutation) and self.n == other.n
        return Permutation(self.n, self.cycles + other.cycles)

    def __str__(self):
        if len(self.cycles) == 0: return '(1)'
        return ''.join('({})'.format(','.join(str(num) for num in c)) for c in self.cycles)

    def get_table(self):
        func = []
        for i in range(1,self.n+1):
            x = i
            for c in self.cycles[::-1]:
                if x in c:
                    x = c[(c.index(x)+1)%len(c)]
            func.append(x)
        return func

    def get_standard_form(self, singletons = False):
        return get_standard_form_from_table(self.get_table(), singletons = singletons)

    def get_cycle_type(self):
        return [len(c) for c in self.get_standard_form(singletons = True).cycles]

    def get_transposition_product(self):
        standard_form = self.get_standard_form(singletons = False)
        cycles = []
        for c in standard_form.cycles:
            for i,x in enumerate(c[:-1]):
                cycles.append(sorted([x,c[i+1]]))
        return Permutation(self.n, cycles)

    def get_neighboring_transposition_product(self):
        tp = self.get_transposition_product()
        cycles = []
        for [x,y] in tp.cycles:
            for i in range(x,y):
                cycles.append([i,i+1])
            for i in range(y-1,x,-1):
                cycles.append([i-1,i])
        return Permutation(self.n, cycles)

if __name__ == "__main__":
    sigma = Permutation(7, [[1,2,4],[3,4]]) * Permutation(7, [[5,6]])
    print(sigma)
    print(sigma.get_standard_form())
    print(sigma.get_transposition_product())
    print(sigma.get_neighboring_transposition_product())
