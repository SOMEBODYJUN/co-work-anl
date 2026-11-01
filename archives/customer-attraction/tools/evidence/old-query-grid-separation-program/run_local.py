"""Reproduce the local grid audit by default; original discover is explicit."""
import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--mode',choices=('local','original'),default='local')
    ap.add_argument('--out',type=Path,required=True)
    args=ap.parse_args()
    here=Path(__file__).resolve().parent;out=args.out.resolve();out.mkdir(parents=True,exist_ok=True)
    manifest=json.loads((here/'manifest.json').read_text())
    for item in manifest['runtime_sources']:
        assert sha(here/item['relative_to_evidence'])==item['sha256']
    point=here/'../all-reply-actual-floors-program/related/all_reply_floors_exact.json'
    cuts=here/'related/old_query_cuts.json'
    rel=Path('research/workspaces/customer-attraction/R-5662d5cb0e5845a980ed10a3b3224cb1/research_3')
    mapping={here/'original/old_query_reply_cuts.py':rel/'old_query_reply_cuts.py',
             here/'related/priced_hidden_reply.py':Path('customer_attraction/priced_hidden_reply.py'),
             point:rel/'all_reply_floors_exact.json'}
    with tempfile.TemporaryDirectory(prefix='old-query-grid-',dir=out) as tmp:
        root=Path(tmp);(root/'work.py').write_text('# Unexecuted path marker.\n')
        for source,dest in mapping.items():
            target=root/dest;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,target)
        before={str(p):sha(root/p) for p in mapping.values()}
        if args.mode=='original':
            command=[sys.executable,'-B',str(rel/'old_query_reply_cuts.py'),str(rel/'all_reply_floors_exact.json'),str(out/'report.json')]
        else:
            command=[sys.executable,'-B',str(here/'audit_old_query_grid.py'),
                     '--source',str(root/rel/'old_query_reply_cuts.py'),'--point',str(root/rel/'all_reply_floors_exact.json'),
                     '--cuts',str(cuts),'--output',str(out/'grid-audit.json')]
        start=time.monotonic();result=subprocess.run(command,cwd=root,text=True,capture_output=True);elapsed=time.monotonic()-start
        after={str(p):sha(root/p) for p in mapping.values()};assert before==after
        event={'scope':'local finite-grid module; no necessary graph build','mode':args.mode,'command':command,
               'cwd':str(root),'python':sys.version,'exit_code':result.returncode,'seconds':elapsed,
               'original_discover_entry_invocations':int(args.mode=='original'),'before':before,'after':after,
               'original_inputs_unchanged':True,'temporary_layout_removed_after_execution':True,
               'layout':'synthetic unexecuted work.py marker and namespace customer_attraction with original priced module only'}
        if args.mode=='original' and result.returncode==0:
            event['output_byte_equal_frozen']=(out/'report.json').read_bytes()==cuts.read_bytes()
    (out/'execution.json').write_text(json.dumps(event,indent=2)+'\n')
    (out/'stdout.txt').write_text(result.stdout);(out/'stderr.txt').write_text(result.stderr)
    print(json.dumps(event,indent=2));print(result.stdout,end='')
    if result.stderr:print(result.stderr,file=sys.stderr,end='')
    raise SystemExit(result.returncode)


if __name__=='__main__':main()
