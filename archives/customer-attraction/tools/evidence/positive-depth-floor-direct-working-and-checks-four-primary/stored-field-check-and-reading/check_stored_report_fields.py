"""Only stored-number and count-vector consistency; never imports the model."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib,sys
report=Path(sys.argv[1]);manifest=Path(sys.argv[2]);out=Path(sys.argv[3])
before=hashlib.sha256(report.read_bytes()).hexdigest();data=json.loads(report.read_text());models={x['path']:json.loads(Path(x['local_path']).read_text()) for x in json.loads(manifest.read_text())};records=[]
for row in data['records']:
 model=models[row['input']];assert model['players']==row['players'] and len(model['topics'])==row['topics']
 values=list(map(F,row['depth_floors']));assert len(values)==row['players'] and sum(values)==F(row['floor_sum']) and 2*sum(values)-row['opt']==F(row['candidate_gap'])
 assert len(row['prefix_witnesses'])==row['players']
 for depth,c in enumerate(row['prefix_witnesses']):assert len(c)==row['topics'] and all(type(a) is int and a>=0 for a in c) and sum(c)==depth
 records.append(dict(input=row['input'],stored_sum_consistent=True,stored_gap_consistent=True,witness_count_vectors_legal=True,reported_gap_nonnegative=F(row['candidate_gap'])>=0))
after=hashlib.sha256(report.read_bytes()).hexdigest();assert before==after
result=dict(status='pass',scope='stored rational sums/gaps and legal count-vector dimensions only; no OPT, threshold, witness minimality, SPE or IC validation',report_sha256_before=before,report_sha256_after=after,record_count=len(records),depth_values=sum(len(x['depth_floors']) for x in data['records']),witness_vectors=sum(len(x['prefix_witnesses']) for x in data['records']),witness_integer_slots=sum(len(c) for x in data['records'] for c in x['prefix_witnesses']),model_or_solver_imports=0,threshold_calls=0,IC_replays=0,records=records)
out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False))
