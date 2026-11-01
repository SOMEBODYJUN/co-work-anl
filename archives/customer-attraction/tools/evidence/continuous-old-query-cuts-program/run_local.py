"""Prepare the minimal frozen layout and run the local audit by default.

--mode original explicitly repeats the author's floating discovery CLI.
No combined graph builder is invoked in either mode.
"""
import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', choices=('local', 'original'), default='local')
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    here = Path(__file__).resolve().parent
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=True)
    rel = Path('research/workspaces/customer-attraction/R-5662d5cb0e5845a980ed10a3b3224cb1/research_3')
    mapping = {
        'original/continuous_old_query_cuts.py':rel/'continuous_old_query_cuts.py',
        'related/old_query_reply_cuts.py':rel/'old_query_reply_cuts.py',
        'related/priced_hidden_reply.py':Path('customer_attraction/priced_hidden_reply.py'),
        'related/all_reply_query_cuts_exact.json':rel/'all_reply_query_cuts_exact.json',
    }
    manifest = json.loads((here/'manifest.json').read_text())
    expected = {s['local_path']:s['sha256'] for s in manifest['sources']}
    for source in mapping:
        assert sha(here/source) == expected[source]
    with tempfile.TemporaryDirectory(prefix='continuous-local-', dir=out) as tmp:
        root = Path(tmp)
        (root/'work.py').write_text('# Path marker only; never executed.\n')
        for source, target in mapping.items():
            dst = root/target
            dst.parent.mkdir(parents=True,exist_ok=True)
            shutil.copyfile(here/source,dst)
        before = {str(target):sha(root/target) for target in mapping.values()}
        if args.mode == 'original':
            command = [sys.executable,'-B',str(rel/'continuous_old_query_cuts.py'),
                       str(rel/'all_reply_query_cuts_exact.json'),str(out/'report.json')]
        else:
            command = [sys.executable,'-B',str(here/'verify_continuous_rows.py'),
                       '--source',str(root/rel/'continuous_old_query_cuts.py'),
                       '--cuts',str(here/'related/continuous_old_query_cuts.json'),
                       '--point',str(root/rel/'all_reply_query_cuts_exact.json'),
                       '--output',str(out/'local-row-audit.json')]
        start=time.monotonic()
        result=subprocess.run(command,cwd=root,text=True,capture_output=True)
        elapsed=time.monotonic()-start
        after={str(target):sha(root/target) for target in mapping.values()}
        assert before == after
        event={'scope':'local continuous module only; no combined graph', 'mode':args.mode,
               'command':command,'cwd':str(root),'python':sys.version,'exit_code':result.returncode,
               'seconds':elapsed,'original_discovery_entry_invocations':int(args.mode=='original'),
               'before':before,'after':after,'original_inputs_unchanged':True,
               'layout':'synthetic unexecuted work.py marker; namespace customer_attraction with exact priced module only',
               'temporary_layout_removed_after_execution':True}
        if args.mode == 'original' and result.returncode == 0:
            event['report_byte_equal_frozen']=(out/'report.json').read_bytes()==(here/'related/continuous_old_query_cuts.json').read_bytes()
    (out/'execution.json').write_text(json.dumps(event,indent=2)+'\n')
    (out/'stdout.txt').write_text(result.stdout)
    (out/'stderr.txt').write_text(result.stderr)
    print(json.dumps(event,indent=2))
    print(result.stdout,end='')
    if result.stderr:print(result.stderr,file=sys.stderr,end='')
    raise SystemExit(result.returncode)


if __name__ == '__main__':
    main()
