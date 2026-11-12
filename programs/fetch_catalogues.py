"""Fetch Beard's archive into a caller-selected temporary directory."""
import hashlib, io, json, pathlib, sys, urllib.request, zipfile
out=pathlib.Path(sys.argv[1]); out.mkdir(parents=True,exist_ok=True)
meta=json.loads(pathlib.Path('data/catalogue_provenance.json').read_text())
data=urllib.request.urlopen(meta['source_url'], timeout=120).read()
assert hashlib.sha256(data).hexdigest()==meta['archive_sha256']
with zipfile.ZipFile(io.BytesIO(data)) as z:
 for item in meta['extracted']:
  if item['order'] not in (9,11,13): continue
  raw=z.read(item['archive_member'])
  assert hashlib.sha256(raw).hexdigest()==item['sha256']
  (out/f"costas_{item['order']}.txt").write_bytes(raw)
  print(item['order'],item['sha256'])
