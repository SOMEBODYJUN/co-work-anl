"""Execute the frozen 1416-byte parent auditor once; never import it."""
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import time

WORKSPACE = Path('research/workspaces/customer-attraction/R-5662d5cb0e5845a980ed10a3b3224cb1')
POINT = Path('research/workspaces/customer-attraction/R-c4f1ef099fad483c9f81283b61eb0b53/six_astra/full_new_reply_closure_exact.json')
SHAS = ['51fe3c73f7c394ce14517678b31dbd72d3c1e08aa5221728d93c7bdf74a67462',
        '4d34cd746ce35dd48827c9014a85106c5defac30fc5f1159ae6085d4fd8fa1df',
        '24a2f9fa7e7a47e26e065b41ada98e1788a5b448251fb8c1e881557c1f7c9f11']

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def run(source, certificate, old_point, root_marker, frozen_review, prior_audit, output):
    if sys.flags.optimize:raise RuntimeError('assertions must remain enabled')
    inputs=[p.resolve() for p in (source,certificate,old_point,root_marker,frozen_review,prior_audit)]
    before_hashes=list(map(sha,inputs))
    assert before_hashes[:3]==SHAS
    assert before_hashes[4]=='b7f89f0eb5ab9ba1ecc03302f637a73fb02ad16ad78231bc6a1988338f6f01bc'
    assert before_hashes[5]=='544aede7b50eae50d02293e06974f913203d8f528d7a1a3e1592aac137ca6758'
    output.mkdir(parents=True,exist_ok=False)
    started=datetime.now(timezone.utc).isoformat()
    with tempfile.TemporaryDirectory(prefix='tail3-B-parent-original-',dir=Path.cwd()) as temp:
        root=Path(temp)
        destinations=[root/WORKSPACE/'audit_tail3_B_projection.py',root/WORKSPACE/'research_2/tail3_B_projection_certificate.json',root/POINT,root/'work.py']
        for p,dest in zip(inputs,destinations):
            dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,dest)
        assert [sha(p) for p in destinations]==before_hashes[:4]
        argv=[sys.executable,'-B',str(destinations[0])]
        start=time.monotonic();result=subprocess.run(argv,cwd=root,capture_output=True,check=False);elapsed=time.monotonic()-start
        (output/'stdout.json').write_bytes(result.stdout);(output/'stderr.txt').write_bytes(result.stderr)
        assert result.returncode==0 and not result.stderr
        observed=json.loads(result.stdout)
        assert set(observed)=={'states','visible_types','point_value','old_sha256'}
        cert=json.loads(inputs[1].read_text());review=json.loads(inputs[4].read_text());prior=json.loads(inputs[5].read_text())
        expected={'states':21504,'visible_types':448,'point_value':cert['old_point_value'],'old_sha256':SHAS[2]}
        assert observed==expected
        mapping={'states':'raw_states_with_overlap','visible_types':'visible_types','point_value':'old_point_value','old_sha256':'old_point_sha256'}
        assert all(observed[k]==review[v] for k,v in mapping.items())
        assert observed['states']==prior['raw_overlap_states'] and observed['visible_types']==prior['visible_cells']
        assert observed['point_value']==prior['old_point_value'] and observed['old_sha256']==prior['old_point_sha256']
        assert result.stdout!=inputs[4].read_bytes()
        assert [sha(p) for p in destinations]==before_hashes[:4]
        record={'scope':'One unchanged parent-auditor entry; exact 448-cell raw-menu and one old-margin check. Original projection generator and prior independent auditor were not executed.',
                'started_utc':started,'python':sys.version,'assertions_enabled':True,'argv':argv,'temporary_cwd':str(root),
                'exit_code':result.returncode,'wall_seconds':elapsed,
                'inputs':[{'path':str(p),'bytes':p.stat().st_size,'sha256':before_hashes[i],
                           'role':('original program','original certificate data','original old-point data','ancestor-location marker only; copied but never imported or executed','historical review comparison only','prior independent-report comparison only')[i]} for i,p in enumerate(inputs)],
                'stdout_bytes':len(result.stdout),'stdout_sha256':hashlib.sha256(result.stdout).hexdigest(),'stderr_bytes':len(result.stderr),
                'four_output_fields_exactly_equal_expected':True,'historical_review_field_mapping':mapping,
                'historical_review_mathematical_fields_equal':True,'stdout_byte_equal_historical_review':False,
                'prior_independent_report_four_mathematical_fields_equal':True,'input_bytes_unchanged':True}
    assert list(map(sha,inputs))==before_hashes
    record['temporary_directory_removed']=not Path(record['temporary_cwd']).exists()
    record['finished_utc']=datetime.now(timezone.utc).isoformat()
    (output/'execution.json').write_text(json.dumps(record,indent=2)+'\n')

if __name__=='__main__':
    if len(sys.argv)!=8:raise SystemExit('usage: run.py SOURCE CERTIFICATE OLD_POINT ROOT_WORK_PY FROZEN_REVIEW PRIOR_AUDIT NEW_OUTPUT_DIR')
    run(*(Path(s) for s in sys.argv[1:]))
