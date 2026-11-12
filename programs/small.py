"""Exact maximum packing for orders 1..8; independently executable."""
from itertools import permutations

def costas(p):
    return all(len({p[i+d]-p[i] for i in range(len(p)-d)}) == len(p)-d for d in range(1,len(p)))

def maximum(n):
    a=[p for p in permutations(range(n)) if costas(p)]
    adj=[0]*len(a)
    for i in range(len(a)):
        for j in range(i):
            if all(x!=y for x,y in zip(a[i],a[j])):
                adj[i]|=1<<j; adj[j]|=1<<i
    best=0
    def search(candidates, depth):
        nonlocal best
        if depth>best: best=depth
        while candidates and depth+candidates.bit_count()>best and best<n:
            bit=candidates & -candidates; candidates-=bit
            search(candidates & adj[bit.bit_length()-1],depth+1)
    search((1<<len(a))-1,0)
    return len(a),best
for n in range(1,9):
    count,value=maximum(n)
    print(f'n={n} arrays={count} maximum={value}',flush=True)
