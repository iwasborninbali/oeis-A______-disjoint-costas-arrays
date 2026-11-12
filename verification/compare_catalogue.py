"""Compare an enumerator's rows with the ordered Beard input."""
import sys
from pathlib import Path
n=int(sys.argv[1]); generated=Path(sys.argv[2]); catalogue=Path(sys.argv[3])
a=[tuple(map(int,line.split())) for line in generated.read_text().splitlines() if line.strip()]
b=[tuple(map(int,line.split())) for line in catalogue.read_text().splitlines() if line.strip()]
assert b[0]==(n,len(b)-1)
assert len(a)==len(set(a)) and len(b[1:])==len(set(b[1:]))
assert set(a)==set(b[1:])
print(f'order={n} generated={len(a)} catalogue={len(b)-1} identical_sets=True')
