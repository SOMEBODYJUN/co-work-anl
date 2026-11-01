"""Run the unchanged author's --export entry once in its original path layout."""
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import time

CODE_REL = Path('research/workspaces/customer-attraction/R-5662d5cb0e5845a980ed10a3b3224cb1/research_2/tail3_B_projection.py')
POINT_REL = Path('research/workspaces/customer-attraction/R-c4f1ef099fad483c9f81283b61eb0b53/six_astra/full_new_reply_closure_exact.json')
SHA = ('63677e14e8c9f257b32f385642bfdf47c71932ce7b251c5970013cf1993c6d01',
       '24a2f9fa7e7a47e26e065b41ada98e1788a5b448251fb8c1e881557c1f7c9f11',
       '4d34cd746ce35dd48827c9014a85106c5defac30fc5f1159ae6085d4fd8fa1df')

def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def run(source, point, expected, output):
    if sys.flags.optimize:raise RuntimeError('assertions must remain enabled')
    inputs=(source.resolve(),point.resolve(),expected.resolve())
    assert tuple(map(digest,inputs)) == SHA
    output.mkdir(parents=True,exist_ok=False)
    started=datetime.now(timezone.utc).isoformat()
    with tempfile.TemporaryDirectory(prefix='tail3-B-original-',dir=Path.cwd()) as temp:
        root=Path(temp)
        code=root/CODE_REL; old=root/POINT_REL
        code.parent.mkdir(parents=True);old.parent.mkdir(parents=True)
        shutil.copyfile(inputs[0],code);shutil.copyfile(inputs[1],old)
        assert digest(code)==SHA[0] and digest(old)==SHA[1]
        argv=[sys.executable,'-B',str(code),'--export']
        before=time.monotonic()
        result=subprocess.run(argv,cwd=root,capture_output=True,check=False)
        seconds=time.monotonic()-before
        (output/'stdout.json').write_bytes(result.stdout)
        (output/'stderr.txt').write_bytes(result.stderr)
        assert result.returncode==0 and not result.stderr
        generated=code.with_name('tail3_B_projection_certificate.json')
        assert generated.read_bytes()==inputs[2].read_bytes()
        rebuilt=json.loads(generated.read_text())
        assert json.loads(result.stdout)=={k:v for k,v in rebuilt.items() if k!='table'}
        shutil.copyfile(generated,output/'tail3_B_projection_certificate.json')
        assert digest(code)==SHA[0] and digest(old)==SHA[1]
        record={'scope':'One unchanged original --export CLI, all 448 coefficients and old-point separation; no discovery LP or parent-auditor execution.',
                'started_utc':started,'python':sys.version,'executable':sys.executable,
                'assertions_enabled':True,'argv':argv,'temporary_cwd':str(root),
                'exit_code':result.returncode,'wall_seconds':seconds,
                'inputs':[{'path':str(p),'bytes':p.stat().st_size,'sha256':digest(p)} for p in inputs],
                'stdout_bytes':len(result.stdout),'stdout_sha256':hashlib.sha256(result.stdout).hexdigest(),
                'stderr_bytes':len(result.stderr),'certificate_bytes':generated.stat().st_size,
                'certificate_sha256':digest(generated),'certificate_byte_equal_frozen':True,
                'stdout_equals_all_non_table_certificate_fields':True}
    assert tuple(map(digest,inputs))==SHA
    record['temporary_directory_removed']=not Path(record['temporary_cwd']).exists()
    record['finished_utc']=datetime.now(timezone.utc).isoformat()
    (output/'execution.json').write_text(json.dumps(record,indent=2)+'\n')

if __name__=='__main__':
    if len(sys.argv)!=5:raise SystemExit('usage: run.py SOURCE OLD_POINT FROZEN_CERTIFICATE NEW_OUTPUT_DIR')
    run(*(Path(s) for s in sys.argv[1:]))
