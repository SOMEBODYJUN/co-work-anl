"""Materialize all frozen primary/related inputs into a fresh external runtime."""
from pathlib import Path
import json,shutil,sys,hashlib
S=Path(__file__).resolve().parent
R=Path(sys.argv[1]) if len(sys.argv)>1 else S.parent/'global_prices_runtime'
assert not R.exists(),'Use a fresh runtime; preserve previous events.'
for x in json.loads((S/'source-manifest.json').read_text()):
 p=S/'original'/Path(x['path']).name;assert hashlib.sha256(p.read_bytes()).hexdigest()==x['sha256']
 q=R/x['path'];q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,q)
for x in json.loads((S/'related-and-runtime-manifest.json').read_text()):
 p=S/x['saved_path'];assert hashlib.sha256(p.read_bytes()).hexdigest()==x['sha256']
 q=R/x['path'];q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,q)
print(str(R))
