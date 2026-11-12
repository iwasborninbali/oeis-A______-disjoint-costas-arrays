"""Fetch two cited papers and check their recorded hashes."""
import hashlib, pathlib, sys, urllib.request
out=pathlib.Path(sys.argv[1]); out.mkdir(parents=True,exist_ok=True)
papers=[
 ('packing-costas.pdf','https://cs.uwaterloo.ca/~dstinson/papers/CostasPackings-JCMCC.pdf','2213b07ba5b8de3355948b5a94ccf74f9f2a9031b77911441426cbadd68623c8'),
 ('frank-dinitz.pdf','https://site.uvm.edu/jdinitz/files/2021/04/costasPaper.jcmcc_.pdf','131d94036de68b755749a5edfe7a278e6581f3b163a06a5d5e040570afcdbcd0'),
]
for name,url,expected in papers:
 data=urllib.request.urlopen(url,timeout=60).read()
 actual=hashlib.sha256(data).hexdigest()
 if actual!=expected: raise ValueError((name,actual,expected))
 (out/name).write_bytes(data)
 print(name,actual)
