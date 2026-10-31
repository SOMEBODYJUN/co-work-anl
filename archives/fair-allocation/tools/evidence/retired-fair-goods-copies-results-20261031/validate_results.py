#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).parent
p=ROOT/'copies_exhaustive_results.json'; b=p.read_bytes(); assert hashlib.sha256(b).hexdigest()=='6698e99b16641989d53412fd86a3ad1da67160868e262e0d7baedb0e269059b8' and len(b)==693
d=json.loads(b); assert d['profiles_checked']==9216 and d['minimum_witness_count']==9 and d['all_instances_have_sd_ef1'] is True
w=d['worst']; assert w['copies']==[1,1,2,2] and w['count']==9 and w['rankings']==[[0,1,2,3],[0,2,1,3],[0,2,1,3]]
assert 'finite theorem verified by exhaustive Python' in d['boundary'] and 'no independent formal proof' in d['boundary']
(ROOT/'validation.json').write_text(json.dumps({'status':'pass','checks':{'hash_and_size':True,'finite_scope_fields':True,'worst_profile_fields':True,'boundary_note':True},'interpretation':'Finite exhaustive verification only; does not prove universal goods-with-copies SD-EF1.'},ensure_ascii=False,indent=2)+'\n')
print('pass')
