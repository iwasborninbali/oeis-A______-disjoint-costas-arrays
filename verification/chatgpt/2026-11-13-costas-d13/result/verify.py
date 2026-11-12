#!/usr/bin/env python3
"""Independently verify Costas certificates and binary catalogue membership."""
import argparse, json, pathlib
BASE=pathlib.Path(__file__).resolve().parent

def costas(p):
    n=len(p)
    if sorted(p)!=list(range(n)): return False
    seen=set()
    for i in range(n):
        for j in range(i+1,n):
            v=(j-i,p[j]-p[i])
            if v in seen: return False
            seen.add(v)
    return True

def catalogue(n):
    raw=(BASE/'catalogues'/f'costas{n}.bin').read_bytes()
    assert len(raw)%n==0
    return [tuple(raw[i:i+n]) for i in range(0,len(raw),n)]

def main():
    for n in range(1,14):
        cat=catalogue(n)
        assert len(cat)==len(set(cat))
        assert cat == sorted(cat)
        assert all(costas(p) for p in cat)
        print(f'catalogue n={n}: {len(cat)} independent checks passed')
    for f in sorted((BASE/'verification'/'certificates').glob('witness*.json')):
        obj=json.loads(f.read_text())
        n=obj['order']; a=[tuple(p) for p in obj['arrays']]
        cat=catalogue(n)
        assert obj['size']==len(a)
        assert all(costas(p) for p in a)
        assert all(all(p[i]!=q[i] for i in range(n)) for j,p in enumerate(a) for q in a[j+1:])
        assert all(cat[k]==p for k,p in zip(obj['catalogue_row_indices'],a))
        print(f'{f.name}: PASS, order={n}, size={len(a)}, Costas/disjoint/catalogue indices')
if __name__=='__main__': main()