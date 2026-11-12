from pathlib import Path
from hashlib import sha256
import base64,zlib,json,struct,textwrap
w=Path(__file__).parent
logfiles=list(w.glob('*.log')) or list((w/'logs').glob('*.log'))
logs={p.name:p.read_text(encoding='utf-8') for p in sorted(logfiles)}
logs_data=json.dumps(logs,ensure_ascii=True,sort_keys=True,separators=(',',':')).encode('utf8')
logs_payload=base64.b85encode(zlib.compress(logs_data,9)).decode('ascii')
logs_manifest='\n'.join(f'{sha256(v.encode()).hexdigest()}  logs/{k}' for k,v in logs.items())
(w/'restore_logs.py').write_text('''#!/usr/bin/env python3
"""Restore original byte-exact run logs from an embedded zlib+base85 text bundle."""
from pathlib import Path
import base64, hashlib, json, zlib
PAYLOAD = (
'''+''.join(f'    "{line}"\n' for line in textwrap.wrap(logs_payload,100))+''')
LOG_SHA256 = """\n'''+logs_manifest+'''\n""".strip().splitlines()

def main():
    data = json.loads(zlib.decompress(base64.b85decode(PAYLOAD)).decode("utf8"))
    dest = Path(__file__).resolve().parent / "logs"
    dest.mkdir(parents=True, exist_ok=True)
    expected = dict((row.split("  ",1)[1].removeprefix("logs/"), row.split("  ",1)[0]) for row in LOG_SHA256)
    assert set(data) == set(expected)
    for name, content in data.items():
        raw = content.encode("utf8")
        assert hashlib.sha256(raw).hexdigest() == expected[name], name
        (dest / name).write_bytes(raw)
    print(f"Restored and SHA-256-checked {len(data)} logs in {dest}")

if __name__ == "__main__":
    main()
''')
r=w/'checkpoints/n13k12'
roots=[p for p in r.glob('root_*.done')]
ps=sorted([p for p in r.glob('prefix_*') if p.is_dir()])
n=12828; stride=(n+7)//8
rootset={int(p.stem.split('_')[1]) for p in roots}
root_special={int(p.stem.split('_')[1]):p.read_text() for p in roots if p.read_text()!='nodes=1 leaves=0\n'}
sets=[rootset]+[{int(p.stem.split('_')[1]) for p in d.glob('second_*.done')} for d in ps]
bitfields=[]
for s in sets:
 b=bytearray(stride)
 for v in s: b[v//8]|=1<<(v%8)
 bitfields.append(bytes(b))
records=[]
for i,d in enumerate(ps):
 for p in d.glob('second_*.done'):
  text=p.read_text()
  if text!='nodes=1 leaves=0\n':
   assert text.startswith('nodes=') and text.endswith(' leaves=0\n')
   records.append((i,int(p.stem.split('_')[1]),int(text.split(' ')[0].split('=')[1])))
records.sort()
packed=b''.join(bitfields)+struct.pack('>I',len(records))+b''.join(struct.pack('>BHI',*v) for v in records)
checkpoint_payload=base64.b85encode(zlib.compress(packed,9)).decode('ascii')
checklist='\n'.join(sorted(str(p.relative_to(r))+'\x00'+p.read_text() for p in r.rglob('*.done'))).encode()
checksha=sha256(checklist).hexdigest()
(w/'restore_checkpoints.py').write_text('''#!/usr/bin/env python3
"""Lossless restoration of original text .done checkpoints for n=13,k=12."""
from pathlib import Path
import base64, hashlib, struct, zlib
N=12828
PREFIX_ROOTS = '''+repr([int(p.name.split('_')[1]) for p in ps])+'''
STRIDE=(N+7)//8
EXPECTED_ROOT_COUNT='''+str(len(rootset))+'''
ROOT_SPECIAL = '''+repr(root_special)+'''
EXPECTED_PREFIX_COUNTS='''+repr([len(s) for s in sets[1:]])+'''
EXPECTED_SNAPSHOT_SHA256="'''+checksha+'''"
PAYLOAD = (
'''+''.join(f'    "{line}"\n' for line in textwrap.wrap(checkpoint_payload,100))+''')

def main():
    raw=zlib.decompress(base64.b85decode(PAYLOAD))
    bitmaps=[raw[i*STRIDE:(i+1)*STRIDE] for i in range(6)]
    offset=6*STRIDE
    count=struct.unpack_from(">I", raw, offset)[0]
    offset+=4
    special={}
    for i in range(count):
        key,second,nodes=struct.unpack_from(">BHI",raw,offset)
        offset+=7
        special[key,second]=nodes
    assert offset==len(raw)
    dest=Path(__file__).resolve().parent/"checkpoints"/"n13k12"
    data={}
    for i,bmap in enumerate(bitmaps):
        for value in range(N):
            if bmap[value//8] & (1<<(value%8)):
                if i==0:
                    path=f"root_{value}.done"
                    data[path]=ROOT_SPECIAL.get(value,"nodes=1 leaves=0\\n")
                else:
                    path=f"prefix_{PREFIX_ROOTS[i-1]}/second_{value}.done"
                    data[path]=f"nodes={special.get((i-1,value),1)} leaves=0\\n"
    roots=sum(x.startswith("root_") for x in data)
    assert roots==EXPECTED_ROOT_COUNT
    counts=[sum(x.startswith(f"prefix_{p}/") for x in data) for p in PREFIX_ROOTS]
    assert counts==EXPECTED_PREFIX_COUNTS
    check=hashlib.sha256("\\n".join(sorted(k+"\\0"+v for k,v in data.items())).encode()).hexdigest()
    assert check==EXPECTED_SNAPSHOT_SHA256,(check,EXPECTED_SNAPSHOT_SHA256)
    for path,content in data.items():
        p=dest/path
        p.parent.mkdir(parents=True,exist_ok=True)
        p.write_text(content,encoding="utf8")
    print(f"Restored and SHA-256-checked {len(data)} text checkpoints ({roots} roots) in {dest}")

if __name__=="__main__":
    main()
''')
print('logs count',len(logs),'log bundle size',len(logs_payload),'logs script', (w/'restore_logs.py').stat().st_size)
print('checkpoints count',len(list(r.rglob('*.done'))),'cp bundle size',len(checkpoint_payload),'cp script',(w/'restore_checkpoints.py').stat().st_size)
print('snapshot sha',checksha)
