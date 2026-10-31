#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json
from fractions import Fraction as F
from pathlib import Path
ROOT=Path(__file__).parent

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

# Optimal-hull long-chain input: exact square matrix, null=unavailable.
d=json.loads((ROOT/'optimal_hull_long_chain_k3d1.json').read_text())
assert d['claim']=='UM-OPT-HULL-LONG-CHAIN-LOCAL-GAP-v1' and d['k']==3 and d['d']==1
M=d['machines']; P=d['processing_times']; assert len(M)==14 and len(P)==len(M)==14 and all(len(r)==13 for r in P)
assert len(set(M))==len(M) and d['ineligible_encoding'].startswith('null means infinity')
vals=[]; finite=0
for row in P:
    for x in row:
        if x is not None:
            assert isinstance(x,str); vals.append(F(x)); finite+=1
assert finite==26 and set(vals)=={F(1),F(1,3),F(5,6)}
assert [sum(x is not None for x in row) for row in P]==[4,2,2,2,2,2,2,1,2,1,2,1,2,1]
long_chain_check={'machines':14,'jobs':13,'finite_entries':26,'values':['1/3','5/6','1'],'row_finite_counts':[4,2,2,2,2,2,2,1,2,1,2,1,2,1]}

# Padded fork: all supplied assignments legal; recompute exact loads.
d=json.loads((ROOT/'padded_fork_k2.json').read_text())
assert d['T']=='1' and d['C']=='3/2' and d['a']=='3/4' and d['t']=='7/12' and d['beta']=='1/6' and d['F_out']=='5/2'
M=d['machine_labels']; J=d['job_labels']; mat=d['finite_processing_matrix']; assert len(M)==19 and len(J)==22 and len(mat)==len(J)
assert d['unlisted_processing_entries']=='infinity' and len(d['initial_assignment'])==len(J)==len(d['optimum_assignment'])
for row in mat:
    assert all(isinstance(k,str) and isinstance(v,str) for k,v in row.items())

def loads(A):
    L=[F(0) for _ in M]
    for j,m in enumerate(A):
        assert str(m) in mat[j], (j,m)
        L[m]+=F(mat[j][str(m)])
    return L
Li=loads(d['initial_assignment']); Lo=loads(d['optimum_assignment'])
assert max(Li)==F(3,2) and max(Lo)==F(1)
padded_check={'machines':19,'jobs':22,'initial_loads':[str(x) for x in Li],'initial_makespan':str(max(Li),'') if False else str(max(Li)),'optimum_loads':[str(x) for x in Lo],'optimum_makespan':str(max(Lo))}

# Pairwise resource-floor fixtures: exact finite sharp cases, independently derive q^{-1} floor.
d=json.loads((ROOT/'pairwise_label_resource_floor.json').read_text())
assert len(d['cases'])==2
for c in d['cases']:
    sets=c['resource_sets']; demands=c['demands']; assert len(sets)==len(demands)
    assert all(isinstance(r,list) and r for r in sets)
    q=len(sets)
    assert F(c['expected_b_star'])==F(1,q)
    if c['name']=='identical_pair_k3': assert demands==[3,3] and sets==[[0,1,2],[0,1,2]]
    else: assert c['name']=='triple_singleton' and demands==[1,1,1] and sets==[[0],[0],[0]]
pair_check={'cases':2,'expected_b_star':['1/2','1/3'],'derivation':'all supplied groups share the same resource support; the singleton collision floor is 1/q for q selected labels'}

manifest={
 'batch':'fixture-inputs-20261031',
 'source_commits':['68fad804ec5946cb296f77dc5b336308a66abf12','aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c'],
 'source_ids':{'optimal_hull_long_chain_k3d1':'b34ae3ca7a190e180641','padded_fork_k2':'c5a89ad13c28b4244ab2','pairwise_label_resource_floor':'e56a02ca3387f97b8f69'},
 'source_sha256':{p.name:sha(p) for p in ROOT.glob('*.json') if p.name!='validation.json'},
 'checks':{'optimal_hull_long_chain_k3d1':long_chain_check,'padded_fork_k2':padded_check,'pairwise_label_resource_floor':pair_check},
 'scope':'exact JSON preservation and finite Fraction/structural checks; no general unrelated-machines theorem inferred'
}
(ROOT/'validation.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(manifest,ensure_ascii=False,indent=2))
