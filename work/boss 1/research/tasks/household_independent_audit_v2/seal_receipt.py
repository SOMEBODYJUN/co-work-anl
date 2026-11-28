"""Bind the verified local independent outputs to the immutable formal Git blob."""
import datetime as dt
import gzip
import hashlib
import json
import subprocess
from pathlib import Path

HERE=Path(__file__).resolve().parent
FORMAL_COMMIT='4bc7d156d327e45b85ebc64359250e3382980a43'
HTML_HASH='f0c72e3baa689bdbb6e7c4e75e12186e0fc1e2f6d2d59308ecdd39013a3ca049'
ENGINE_HASH='e89e241afd96b9ce24b5df343ea9d1e8b14880f17ab265a31690d34b379dbeaa'

def sha(x):return hashlib.sha256(x).hexdigest()
def load(name):return json.loads((HERE/name).read_text())

formal_bytes=subprocess.check_output(['git','show',FORMAL_COMMIT+':work/boss 1/formal/calculator.html'],cwd=HERE)
assert sha(formal_bytes)==HTML_HASH
matrix=load('audit_matrix.json');raw=load('numeric_report.json');ext=load('extended_report.json');legacy=load('legacy_equivalence.json')
assert matrix['binding']['engine']==ENGINE_HASH and matrix['binding']['packagedHTML']==HTML_HASH
assert matrix['numericEngineVerdict']=='pass' and matrix['offlineUIVerdict']=='blocked'
assert raw['checksRun']==raw['passed']==179 and raw['failed']==0
assert ext['checks']==ext['passed']==36 and ext['failed']==0
assert load('offline_attempt.json')['actions']==[]
assert raw['inputSHA256']==sha((HERE/'independent_input.json').read_bytes()) and ext['inputSHA256']==sha((HERE/'extended_inputs.json').read_bytes())
for path,key in [('observed_engine_output.json.gz',raw),('extended_outputs.json.gz',ext)]:
    assert key['uncompressedOutputSHA256']==sha(gzip.decompress((HERE/path).read_bytes()))
assert not legacy['differences'] and legacy['maximumAbsoluteNumericDifference']==0
assert sha((HERE.parent/'household_independent_audit'/'engine_receipt.json').read_bytes())=='1e37a9a574b155abc1dbf71da21433c3c3ac47e423389b9e527585d5d5420ffc'
receipt=HERE/'engine_receipt.json'
files={p.name:sha(p.read_bytes()) for p in sorted(HERE.iterdir()) if p.is_file() and p!=receipt}
output={'schema':'independent-household-numeric-receipt.v2','reviewer':'/root/household_independent_audit','implementationAuthor':'/root/household_engine','projectActor':'boss 1','verdict':'pass','scope':'Synthetic household engine and standalone inline code','offlineUI':'blocked before real browser creation; zero interactions / screenshots / downloads', 'checkedAtUtc':dt.datetime.now(dt.timezone.utc).isoformat(), 'formalCodeCommit':FORMAL_COMMIT,'versionBinding':matrix['binding'],'replayedOldRequests':87,'oldChecksPassed':179,'newRequests':25,'newChecksPassed':36,'allChecksPassed':215,'allChecksFailed':0,'comparisonToOldEconomicValues':legacy['totals'],'maxOldNumericDifference':legacy['maximumAbsoluteNumericDifference'],'artifacts':files};receipt.write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n')
assert all(sha((HERE/f).read_bytes())==h for f,h in files.items())
print('receipt',sha(receipt.read_bytes()),'matrix',files['audit_matrix.json'],'analysis',files['analysis.md'],'artifacts',len(files))
