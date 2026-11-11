#!/usr/bin/env python3
"""Exact new layer; imports no old builders and never optimizes."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product, combinations_with_replacement
import json, hashlib, gzip

HERE=Path(__file__).resolve().parent
WS=HERE.parent
REPO=WS.parents[2]
EXPECTED={
 'universal_union_wallet_lp/exact_input.json':'f87a60372dee7449332b17721be6aa70012fb3aca251825cb2e9dd755ff01e41',
 'universal_union_wallet_lp/exact_certificate.json':'ccc085060427e2999a8e4f00ac3414d7e20a1c6e66aeba8d3e658ae34cb16c85',
}

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(path,obj):
    data=(json.dumps(obj,ensure_ascii=False,indent=2)+'\n').encode()
    if path.suffix=='.gz':
        with path.open('wb') as raw:
            with gzip.GzipFile(fileobj=raw,mode='wb',mtime=0,filename='') as f: f.write(data)
    else: path.write_bytes(data)
def qvalue(q,v,s):
    if q=='X': return F(v['x'])
    if q=='Omean': return F(v['o'],6)
    if q.startswith('A'): return F(v['a'][int(q[1:])-1])
    if q.startswith('T'): return F(s[int(q[1:])-1])
    raise ValueError(q)
def basecoef(row,v):
    a=v['a']; c=sum(a); u=lambda j:F(a[j-1],c) if c else F(0)
    P=sum(a[:4]); fam=row['family']
    if fam=='IC': return u(row['source'])
    if fam=='SAFE': return u(row['actual_source'])
    if fam=='MAX': return F(v['x'],P+1)
    if fam=='CAP' or fam=='BR' or fam=='PAIR': return F(0)
    if fam=='MX': return u(5)
    if fam=='RC': return u(5)+F(v['x'],P+1)
    raise ValueError(fam)
def coefficient(row,v,s):
    i=row['source']; a=v['a']; x=v['x']; P=sum(a[:4]); b=sum(a[:i-1]); fam=row['family']
    if fam=='IC': return F(x,b+1+sum(s))
    q=qvalue(row['queries'][0],v,s)
    if fam=='SAFE':
        j=row['actual_source']; return q/(sum(a[:j-1])+7-j)
    if fam=='MAX': return q/(P+1)
    if fam=='CAP': return q
    if fam=='MX': return q/(P+1+x)
    if fam=='BR': return (q-s[-1])/(b+x+sum(s[:-1])+1)
    r=qvalue(row['queries'][1],v,s)
    d=P+1 if fam=='RC' else b+x+sum(s[:-2])+1
    lhs=(q+r)/d-q*r/(d*(d+1))
    if fam=='PAIR':
        z,t=s[-2:]; lhs-=F(z,d+t)+F(t,d+z)+F(z,d*(d+1))
    return lhs
def descriptors():
    rows=[]
    def add(fam,i,qs=(),j=None):
        name=f'{fam}_i{i}'+(f'_j{j}' if j else '')+('|'+'|'.join(qs) if qs else '')
        r={'name':name,'family':fam,'source':i,'queries':list(qs)}
        if j is not None:r['actual_source']=j
        rows.append(r)
    for i in range(1,5):
        tails=[f'T{k}' for k in range(1,7-i)]
        old=[f'A{k}' for k in range(1,7)]+['X','Omean']
        add('IC',i)
        for q in tails:
            for j in range(1,7):add('SAFE',i,[q],j)
            for f in ['MAX','CAP','MX']:add(f,i,[q])
        for q in old+tails[:-1]:add('BR',i,[q])
        for q,r in combinations_with_replacement(old+tails,2):add('PAIR',i,[q,r])
        for q,r in combinations_with_replacement(tails,2):add('RC',i,[q,r])
        for q in tails:
            for r in old:add('RC',i,[q,r])
    return rows

def main():
    for rel,h in EXPECTED.items():assert sha(WS/rel)==h,(rel,sha(WS/rel))
    old=json.loads((WS/'universal_union_wallet_lp/exact_input.json').read_text())
    cert=json.loads((WS/'universal_union_wallet_lp/exact_certificate.json').read_text())
    atoms=old['atom_columns']; masses={int(k):F(v) for k,v in cert['primal'].items() if int(k)<256 and F(v)>0}
    K=F(cert['K']); support=[v for v in atoms if v['index'] in masses]
    assert len(support)==13
    frozen={}
    for d in ['universal_union_wallet_lp','early_shared_x_joint','early_shared_x_menu_pair_closure']:
        for p in sorted((WS/d).rglob('*')):
            if p.is_file():frozen[str(p.relative_to(WS))]=sha(p)
    for rel in ['main_universal_union_wallet_check.json','early_shared_x_joint.md','early_shared_x_menu_pair_closure.md','main_full_average_pair.md','universal_union_wallet_lp.md']:
        frozen[rel]=sha(WS/rel)
    dump(HERE/'frozen_sources_before.json',frozen)
    cols=[]; eq=[]
    for i in range(1,5):
        for v in support:
            indices=[]
            for s in product((0,1),repeat=6-i):
                indices.append(len(cols)); cols.append({'index':len(cols),'source':i,'atom':v['index'],'tail':list(s)})
            eq.append({'name':f'MASS_i{i}_v{v["index"]}','source':i,'atom':v['index'],'a':{str(k):'1' for k in indices},'rhs':str(masses[v['index']])})
    rows=descriptors()
    for row in rows:
        row['base_z']={str(v['index']):str(basecoef(row,v)) for v in atoms if basecoef(row,v)}
        row['base_K']='1' if row['family']=='CAP' else '0'
        row['rhs']=str(sum((basecoef(row,v)*masses[v['index']] for v in support),F(0))+F(row['base_K'])*K)
        row['a']={str(c['index']):str(coefficient(row,atoms[c['atom']],c['tail'])) for c in cols if c['source']==row['source'] and coefficient(row,atoms[c['atom']],c['tail'])}
    assert len(cols)==780 and len(eq)==52 and len(rows)==608
    families={f:sum(r['family']==f for r in rows) for f in ['IC','SAFE','MAX','CAP','MX','BR','PAIR','RC']}
    data={'claim':'Necessary four-forced-X true-tail completion at a released universal atom point; no full-SPE claim.',
          'convention':'A mu <= base_z*z + base_K*K', 'point_input_sha256':EXPECTED['universal_union_wallet_lp/exact_input.json'],
          'point_certificate_sha256':EXPECTED['universal_union_wallet_lp/exact_certificate.json'],
          'derivation_sha256':sha(HERE/'derivation.md'),'all_base_atoms':atoms,
          'fixed_positive_mass':{str(k):str(v) for k,v in masses.items()},'fixed_K':str(K),
          'columns':cols,'inequalities':rows,'equalities':eq,'family_counts':families,
          'nonnegative_columns':list(range(780)), 'forbidden_inference':'Feasibility is not SPE; infeasibility is not half or an SPE counterexample.'}
    dump(HERE/'exact_input.json.gz',data)
    summary={'columns':len(cols),'mass_equations':len(eq),'raw_inequalities':len(rows),'family_counts':families,
             'inequality_nonzeros':sum(len(r['a']) for r in rows),'source_sha256':EXPECTED,
             'input_sha256':sha(HERE/'exact_input.json.gz'),'frozen_files':len(frozen),'optimizer_calls':0}
    dump(HERE/'build_summary.json',summary); print(json.dumps(summary,indent=2))
if __name__=='__main__': main()
