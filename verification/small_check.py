"""Independent direct permutation and packing decision check, orders 1..8."""
import itertools

def arrays(n):
    for p in itertools.permutations(range(n)):
        vectors=[(j-i,p[j]-p[i]) for i in range(n) for j in range(i+1,n)]
        if len(vectors)==len(set(vectors)): yield p

def packing_exists(rows,k):
    # In each recursive step choose a candidate and discard conflicting cells.
    def visit(candidates, need):
        if need==0: return True
        if len(candidates)<need: return False
        while len(candidates)>=need:
            p=candidates.pop()
            compatible=[q for q in candidates if all(p[i]!=q[i] for i in range(len(p)))]
            if visit(compatible,need-1): return True
        return False
    return visit(list(rows),k)
for n in range(1,9):
    a=list(arrays(n)); result=next(k for k in range(n,0,-1) if packing_exists(a,k))
    print(f'n={n} arrays={len(a)} maximum={result}',flush=True)
