#!/usr/bin/env python3
"""Rebuild the original source layout in an isolated directory and replay it."""
from pathlib import Path
import hashlib, json, os, shutil, subprocess, sys, tempfile
packet=Path(__file__).resolve().parent
mode='kappa'
common=packet if mode=='kappa' else packet.parent/'kappa-prices-finite-audit-Boss8'
with tempfile.TemporaryDirectory(prefix='replay-',dir=packet) as folder:
 root=Path(folder)
 if mode!='credible':
  shutil.copytree(common/'runtime',root,dirs_exist_ok=True,ignore=shutil.ignore_patterns('__pycache__'))
 else:
  shutil.copytree(packet/'runtime',root,dirs_exist_ok=True)
 srcname={'kappa':'kappa_prices.py','credible':'probe_extra_slot_floor.py','flow':'probe_flow_matching.py'}[mode]
 section='credible' if mode=='credible' else 'transport'
 target=root/'research/workspaces/customer-attraction/R-3d2531ded15f453daef73b30eef82940'/section/srcname
 target.parent.mkdir(parents=True,exist_ok=True)
 source=packet/srcname if mode!='flow' else packet/'source'/srcname
 shutil.copy2(source,target)
 env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
 run=subprocess.run([sys.executable,str(target)],cwd=root,env=env,capture_output=True)
 sys.stderr.buffer.write(run.stderr)
 if run.returncode: raise SystemExit(run.returncode)
 actual=target.with_name('kappa_existing_audit.json').read_bytes() if mode=='kappa' else run.stdout
 expected=(packet/('kappa_existing_audit.json' if mode=='kappa' else 'replay_exact_source.json' if mode=='credible' else 'run.stdout')).read_bytes()
 print(json.dumps({'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'output_sha256':hashlib.sha256(actual).hexdigest(),'matches_saved_bytes':actual==expected,'records':len(json.loads(actual)) if mode!='flow' else None},ensure_ascii=False,indent=2))
 if mode in ('kappa','flow') and actual!=expected: raise SystemExit('Exact deterministic output differs')
