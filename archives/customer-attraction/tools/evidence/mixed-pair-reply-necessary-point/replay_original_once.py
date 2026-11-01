"""One unchanged 5043-row verifier on this exact point; no optimization."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

def digest(p):
    b=p.read_bytes()
    return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}

def main():
    a=argparse.ArgumentParser()
    for k in ('repo','point','runtime','out'):a.add_argument('--'+k,type=Path,required=True)
    args=a.parse_args();args.runtime.mkdir(parents=True,exist_ok=False);args.out.mkdir(parents=True,exist_ok=False)
    manifest=args.repo/'archives/customer-attraction/tools/evidence/continuous-query-refinement-program/source-manifest.json'
    records=json.loads(manifest.read_text())['runtime_sources'];copied=[]
    for record in records:
        source=args.repo/record['stored_path'];d=digest(source)
        assert (d['bytes'],d['sha256'])==(record['size'],record['sha256'])
        target=args.runtime/record['path'];target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(source.read_bytes())
        copied.append({'path':record['path'],'stored_path':record['stored_path'],**d})
    prefix=Path('research/workspaces/customer-attraction/R-5662d5cb0e5845a980ed10a3b3224cb1/research_3')
    target=args.runtime/prefix/'all_reply_mixed_pair_exact.json'
    assert not target.exists();target.write_bytes(args.point.read_bytes())
    assert digest(target)['sha256']=='83b469f45e6017c024d1f87c614c5b1e968be94bb171ed27bb913c7119843613'
    copied.append({'path':str(target.relative_to(args.runtime)),'stored_path':'primary source 6f7ed6d3ddc75a71d85e',**digest(target)})
    (args.runtime/'work.py').write_text('# ROOT-location marker only; never imported or executed.\n')
    argv=[sys.executable,'-B',str(args.runtime/prefix/'all_reply_actual_floors.py'),'--priced','--optimum','--old-query-cuts','--mixed-pair','--verify']
    started=datetime.now(timezone.utc).isoformat();t=time.monotonic()
    p=subprocess.run(argv,cwd=args.runtime,capture_output=True)
    elapsed=time.monotonic()-t
    (args.out/'stdout.txt').write_bytes(p.stdout);(args.out/'stderr.txt').write_bytes(p.stderr)
    unchanged=all(digest(args.runtime/r['path'])=={k:r[k] for k in ('bytes','sha256')} for r in copied)
    report={'scope':'one unchanged all_reply_actual_floors.py with priced,optimum,old-query,mixed-pair,verify; exact point 6f7ed6d3ddc75a71d85e only; no optimization',
            'argv':argv,'cwd':str(args.runtime),'started_utc':started,'finished_utc':datetime.now(timezone.utc).isoformat(),
            'wall_seconds':elapsed,'python':sys.version,'exit_code':p.returncode,'assertions_enabled':not sys.flags.optimize,
            'runtime_sources_count':len(copied),'source_manifest':str(manifest.relative_to(args.repo)),
            'source_manifest_sha256':digest(manifest)['sha256'],'entrypoint_sha256':digest(args.runtime/prefix/'all_reply_actual_floors.py')['sha256'],
            'primary_sha256':digest(target)['sha256'],'all_frozen_input_bytes_unchanged':unchanged,
            'stdout':digest(args.out/'stdout.txt'),'stderr':digest(args.out/'stderr.txt'),
            'ROOT_marker':'new marker only; not imported or executed','optimization_runs':0}
    (args.out/'execution.json').write_text(json.dumps(report,indent=2)+'\n')
    (args.out/'runtime-inputs.json').write_text(json.dumps(copied,indent=2)+'\n')
    print(p.stdout.decode(),end='');print(json.dumps(report,indent=2))
    assert p.returncode==0 and unchanged and not p.stderr

if __name__=='__main__':main()
