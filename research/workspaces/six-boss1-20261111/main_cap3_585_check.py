"""Main independently reconstructs the 585 raw endpoint rows from true shares."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
from functools import lru_cache
from hashlib import sha256
from collections import Counter
import json
import re

W=Path(__file__).resolve().parent
P=W/'source2_cap3_full_delta_rows'
def read(path): return json.loads(path.read_text())
def digest(path): return sha256(path.read_bytes()).hexdigest()
assert digest(P/'freeze_manifest.json')=='bc0d03e6cb05fc6c270fc14ec2e547a3333cf36b924dd883e8d25cd3ad450c8f'
assert digest(P/'exact_family.json')=='4a31f3ff6847a355442807aa8d03fffad43c92c6849229f63299556da8c00c8b'
manifest=read(P/'freeze_manifest.json')
for item in manifest['files']:
    f=P/item['path'];assert f.stat().st_size==item['bytes'];assert digest(f)==item['sha256']
family=read(P/'exact_family.json');rows=family['rows']
assert len(rows)==585 and family['column_count']==513 and family['original_scale']
atoms=list(product((0,1),repeat=9))
tails=list(product((0,1),repeat=4))
registry={r['vertex_key']:r for r in read(P/'vertex_registry.json')['records']}
assert len(registry)==225
condition_checks=cost_checks=column_checks=0
counts=Counter()

@lru_cache(None)
def parameters(delta,h,s,q0):
    x=F(5977,6912)-delta;y=F(43,48)+delta
    source=25+x+y-s; cap0=q0*(F(1,2)+x/12+y/6)
    beta=(cap0-h,q0/2+x+q0*y/6,q0/2+y)
    assert 0<=delta<=F(5977,6912) and 0<=h<=cap0
    assert all(v>=0 for v in beta)
    return x,y,source,beta,1+sum(beta,F(0))

@lru_cache(None)
def true_values(delta,h,s,q0,p,t,q):
    x,y,a,beta,S=parameters(delta,h,s,q0)
    values=[]
    for r3,r4,r5,z in tails:
        load=p+t+r3+r4+r5+z
        source_pay=a*F(t,load) if load else F(0)
        terminal_pay=F(z,load) if load else F(0)
        internal4=x*F(r4,load) if load else F(0)
        internal5=y*F(r5,load) if load else F(0)
        value=source_pay-terminal_pay-internal4-internal5
        value+=sum((v*b for v,b in zip(beta,(r3,r4,r5))),F(0))+z
        value+=q/F(p+t+r3+r4+r5+1)
        value+=x*q/F(p+t+r3+3)+y*q/F(p+t+r3+r4+2)
        values.append(value)
    return tuple(values)

@lru_cache(None)
def minimum(delta,h,s,q0,p,t,q): return min(true_values(delta,h,s,q0,p,t,q))

@lru_cache(None)
def ordered(delta,h,s,p):
    q0=F(1,5); f=[]
    for d in range(7):
        value=F(0)
        if d: value+=F(d,6)*minimum(delta,h,s,q0,p,1,F(d-1,5))
        if d<6: value+=F(6-d,6)*minimum(delta,h,s,q0,p,0,F(d,5))
        f.append(value)
    assert f[0]==0 and all(f[d+1]>f[d] for d in range(1,6))
    return min(f[1:])

for key,record in registry.items():
    vertex=record['source_vertex_record'];header=record['source_slice_header']
    delta,h=map(F,vertex['point']);s=F(header['s']);q0=F(header['q0'])
    for name,condition in vertex['conditions'].items():
        p,t,n=map(int,re.fullmatch(r'p([01])_t([01])_n([0-6])',name).groups())
        q=F(n,6) if header['mode']=='pure' else F(n-t,5)
        values=true_values(delta,h,s,q0,p,t,q);m=min(values)
        assert F(condition['value'])==m,(key,name)
        weak=[''.join(map(str,tail)) for tail,v in zip(tails,values) if v==m]
        assert condition['tails']==weak,(key,name)
        condition_checks+=1;cost_checks+=len(values)

for row in rows:
    assert row['column_count']==513 and row['numerical_divisor']=='25'
    assert row['divisor_applied'] is False and row['raw_scale'] is True
    delta,h,s,q0=map(F,[row['delta'],row['h'],row['s'],row['q0']])
    record=registry[row['vertex_key']];header=record['source_slice_header'];vertex=record['source_vertex_record']
    assert row['source_vertex_id']==vertex['id'] and row['slice_id']==header['id']
    assert list(map(F,vertex['point']))==[delta,h] and F(header['s'])==s and F(header['q0'])==q0
    x,y,a,beta,S=parameters(delta,h,s,q0)
    assert [F(row['tau'][str(i)]) for i in (3,4,5)]==[F(0),x,y]
    assert [F(row['beta_actual'][str(i)]) for i in (3,4,5)]==list(beta)
    rb=row['real_budget'];assert F(rb['source_IC'])==a
    assert [F(rb['intermediate_CAP'][str(i)]) for i in (3,4,5)]==list(beta)
    assert [F(rb['internal_SAFE'][str(i)]) for i in (3,4,5)]==[F(0),x,y]
    assert F(rb['terminal_CAP'])==F(rb['terminal_BR'])==1
    assert F(rb['inner_query_average'])==q0
    assert rb['outer_average']==('1/6' if row['mode']=='ordered' else None)
    mu=S-s/5 if row['row_kind']=='C-only' else F(0)
    assert F(row['free_EC'])==mu and F(row['raw_K'])==S
    expected=[]
    for atom in atoms:
        p=atom[0];o=atom[7];c=atom[8];load=sum(atom[:6])
        value=a*(F(atom[1],load) if load else F(0))
        if row['mode']=='ordered': value-=o*ordered(delta,h,s,p)
        else:
            target=row['target'];ix=int(target[1:])-1 if target.startswith('A') else {'X':6,'C':8}[target]
            value-=minimum(delta,h,s,q0,p,atom[ix],F(o,6))
            value+=mu*c
        expected.append(value)
    expected.append(S-mu)
    assert expected==list(map(F,row['a'])),row['id']
    assert F(row['K'])==S-mu
    column_checks+=513;counts[row['row_kind']]+=1
assert (condition_checks,cost_checks,column_checks)==(4680,74880,300105)
assert counts=={'general':360,'C-only':45,'ordered':180}
result={'status':'PASS_MAIN_585_FULL_RAW_ROWS_TRUE_SHARES_WEAK_STATES_METADATA',
    'source_vertices':len(registry),'rows':len(rows),'columns_each':513,
    'all_coefficient_identities':column_checks,'true_tail_costs':cost_checks,
    'complete_weak_state_sets':condition_checks,'interface_counts':dict(counts),
    'all_manifest_files_byte_verified':len(manifest['files']),
    'all_original_scale_and_free_EC_identities_checked':True,
    'points_or_faces_read':False,'optimizer_calls':0,
    'family_sha256':digest(P/'exact_family.json'),'manifest_sha256':digest(P/'freeze_manifest.json')}
with (W/'main_cap3_585_check.json').open('x') as out: out.write(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False))
