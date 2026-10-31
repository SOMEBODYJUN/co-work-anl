#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).parent
E={'charity_probe.py':('db44e5985190561332fc19ef13dfd910102747cf2cea51458f3747f0be872bae',4041,['def ef','def brute','class Flow','def algorithm','mismatches']), 'charity_results.json':('4587f181a3b0e3fa61364f4ea3adc6eaaa4137acbe2289123b0685120886ee6b',256,[]), 'probe.py':('42e30ce279197f7ef176f7eefd2a7b6f5986200d921949eab34271a13c857981',3846,['def verify','def brute','def forest','random_forest_checks','mismatches']), 'results.json':('60be72944ce162aea2849a59aea089cef91189eabb08a920602e7f2be161afc6',1363,[])}
for n,(h,size,marks) in E.items():
 b=(ROOT/n).read_bytes(); assert (hashlib.sha256(b).hexdigest(),len(b))==(h,size),(n,hashlib.sha256(b).hexdigest(),len(b))
 s=b.decode(); assert all(m in s for m in marks)
d=json.loads((ROOT/'charity_results.json').read_text()); assert d['cases']==1200 and d['mismatches']==0 and d['maximum_edges']==8
r=json.loads((ROOT/'results.json').read_text()); assert r['random_forest_checks']['tests']==4200 and r['random_forest_checks']['feasible']==2395 and r['random_forest_checks']['mismatches']==0
(ROOT/'validation.json').write_text(json.dumps({'status':'pass','checks':{'hashes_and_sizes':True,'result_fields':True,'implementation_markers':True},'interpretation':'Finite audit integrity only; no general simple/multigraph fairness theorem.'},ensure_ascii=False,indent=2)+'\n')
print('pass')
