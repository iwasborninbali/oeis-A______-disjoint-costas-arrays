#!/usr/bin/env python3
"""Independent exhaustive set-packing audit for orders at most 7.
Enumerates all candidate sets in index order, without square symmetries,
coloring bounds, or using any code from exact.cpp.
"""
from verify import catalogue, costas

def has_packing(orders, target):
    n=len(orders[0]); visited=0
    def rec(cands, required):
        nonlocal visited
        visited += 1
        if required==0: return True
        if len(cands)<required: return False
        for i, aidx in enumerate(cands):
            p=orders[aidx]
            filt=[j for j in cands[i+1:] if all(p[r]!=orders[j][r] for r in range(n))]
            if rec(filt, required-1): return True
        return False
    result=rec(list(range(len(orders))), target)
    return result,visited

if __name__=='__main__':
    for n in range(1,8):
        a=catalogue(n)
        win=1 if n==1 else n if n%2==0 else n-1
        yes,nodes=has_packing(a,win)
        assert yes
        impossible=False
        failure_nodes=0
        if win<n:
            impossible,failure_nodes=has_packing(a,win+1)
            assert not impossible
        print(f'n={n} D={win} positive_nodes={nodes} failed_target_nodes={failure_nodes}')