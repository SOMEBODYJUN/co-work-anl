#!/usr/bin/env python3
"""Exact averaged source-3 optimal-menu requery layer; no solver."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product,combinations_with_replacement
import json,hashlib

H=Path(__file__).resolve().parent;WS=H.parent;ROOT=WS.parents[2]
OLD_INPUT='3c1a824ed0a17562da812db1d0bb12485f0b1c7f743577af7bc2ecf316d3ab65'
OLD_CERT='80d9267b6ed9b5e47c4f8ea92523aaf1e73754eb28416e4117f8db754b88d771'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(name,obj):(H/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
def query(label,h,q,s):
    bits=h['bits']
    if label=='C':return F(bits[0])
    if label.startswith('B'):return F(bits[int(label[1:])-1])
    if label=='Q':return F(q)
    if label.startswith('R'):return F(s[int(label[1:])-4])
    if label=='Omean':return F(bits[6],6)
    raise ValueError(label)
def base(row,h):
    l=h['bits'][:6];c=sum(l);fam=row['family'];j=3 if fam=='SOURCE_IC' else row.get('source')
    if fam in ('SOURCE_IC','OLD_SAFE'):return F(l[j-1],c) if c else F(0)
    return F(0)
def coefficient(row,h,q,s):
    l=h['bits'][:6];b=l[0]+l[1];fam=row['family']
    if fam=='SOURCE_IC':return F(q,b+1+sum(s))
    if fam=='CAP':return F(s[row['tail']-4])
    if fam=='OLD_SAFE':
        j=row['source'];return F(s[row['tail']-4],sum(l[:j-1])+7-j)
    if fam=='ROOT_SIZE':return F(s[row['tail']-4],6)
    full=[l[0],l[1],q,*s];c=sum(full)
    if fam=='NEW_SAFE':
        j=row['source'];own=F(full[j-1],c) if c else F(0)
        return query(row['queries'][0],h,q,s)/(sum(full[:j-1])+7-j)-own
    if fam=='PAIR':
        d=sum(full[:4])+1;y,z=s[1:];left,right=[query(v,h,q,s) for v in row['queries']]
        wallet=F(y,d+z)+F(z,d+y)+F(y,d*(d+1))
        return (left+right)/d-left*right/(d*(d+1))-wallet
    raise ValueError(fam)
def descriptors():
    rows=[{'name':'SOURCE3_AVERAGE_IC','family':'SOURCE_IC'}]
    rows += [{'name':f'CAP_R{j}','family':'CAP','tail':j} for j in (4,5,6)]
    rows += [{'name':f'OLD_SAFE_j{i}|R{j}','family':'OLD_SAFE','source':i,'tail':j} for i in range(2,7) for j in (4,5,6)]
    rows += [{'name':f'ROOT_SIZE_R{j}','family':'ROOT_SIZE','tail':j} for j in (4,5,6)]
    qs=['C','B2','B3','B4','B5','B6','Q','R4','R5','R6','Omean']
    rows += [{'name':f'NEW_SAFE_j{i}|{q}','family':'NEW_SAFE','source':i,'queries':[q]} for i in (4,5,6) for q in qs]
    rows += [{'name':f'PAIR|{q}|{r}','family':'PAIR','queries':[q,r]} for q,r in combinations_with_replacement(qs,2)]
    assert len(rows)==121;return rows
def main():
    olddir=WS/'maximal_root_tail_wallet'
    assert sha(olddir/'exact_input.json')==OLD_INPUT and sha(olddir/'exact_certificate.json')==OLD_CERT
    old=json.loads((olddir/'exact_input.json').read_text());cert=json.loads((olddir/'exact_certificate.json').read_text())
    release=json.loads((WS/'main_maximal_root_tail_check.json').read_text())
    assert release['status']=='PASS' and release['input_sha256']==OLD_INPUT and release['certificate_sha256']==OLD_CERT
    frozen={}
    for p in sorted(olddir.rglob('*')):
        if p.is_file():frozen[str(p.relative_to(ROOT))]=sha(p)
    for rel in ['research/workspaces/six-boss1-20261111/maximal_root_tail_wallet.md','research/workspaces/six-boss1-20261111/main_maximal_root_tail_check.json',
                'research/workspaces/six-boss1-20261111/main_full_average_pair.md','archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md']:
        frozen[rel]=sha(ROOT/rel)
    save('frozen_sources_before.json',frozen)
    atoms=old['atoms'];mass={int(k):F(v) for k,v in cert['primal'].items() if int(k)<128 and F(v)>0}
    K=F(old['fixed_K']);u=F(cert['objective']);assert len(mass)==10
    cols=[];eq=[]
    for h in sorted(mass):
        indices=[]
        for q in (0,1):
            for s in product((0,1),repeat=3):
                indices.append(len(cols));cols.append({'index':len(cols),'atom':h,'q':q,'tail':list(s)})
        eq.append({'name':f'MASS_h{h}','atom':h,'a':{str(j):'1' for j in indices},'rhs':str(mass[h])})
    rows=descriptors()
    for row in rows:
        row['base_z']={str(h['index']):str(base(row,h)) for h in atoms if base(row,h)}
        row['base_K']='1' if row['family']=='CAP' else '0'
        row['base_u']='1' if row['family']=='ROOT_SIZE' else '0'
        row['rhs']=str(sum((base(row,atoms[h])*m for h,m in mass.items()),F(0))+F(row['base_K'])*K+F(row['base_u'])*u)
        row['a']={str(c['index']):str(coefficient(row,atoms[c['atom']],c['q'],c['tail'])) for c in cols if coefficient(row,atoms[c['atom']],c['q'],c['tail'])}
    for h in sorted(mass):
        o=atoms[h]['bits'][6]
        for fam,sign,coef in [('Q_LOWER',-1,-F(o,6)),('Q_UPPER',1,F(o))]:
            rows.append({'name':f'{fam}_h{h}','family':fam,'atom':h,'base_z':{str(h):str(coef)} if coef else {},'base_K':'0','base_u':'0',
                         'rhs':str(coef*mass[h]),'a':{str(c['index']):str(sign) for c in cols if c['atom']==h and c['q']==1}})
    assert len(cols)==160 and len(rows)==141 and len(eq)==10
    out={'scope':'Necessary average of six genuine source-3 optimal-label requeries at the true root-C prefix; no disjoint-menu assumption.',
         'old_input_sha256':OLD_INPUT,'old_certificate_sha256':OLD_CERT,'all_old_atoms':atoms,'fixed_mass':{str(h):str(m) for h,m in mass.items()},
         'fixed_K':str(K),'fixed_u':str(u),'columns':cols,'nonnegative_columns':list(range(160)),
         'convention':'A*nu <= base_z*w + base_K*K + base_u*u','true_row_count':121,'raw_rows':rows,'equalities':eq,
         'derivation_sha256':sha(H/'derivation.md'),'source_manifest_sha256':sha(H/'frozen_sources_before.json')}
    save('exact_input.json',out)
    summary={'columns':160,'mass_equations':10,'true_rows':121,'moment_bounds':20,'raw_inequalities':141,
             'family_counts':{f:sum(r['family']==f for r in rows) for f in ['SOURCE_IC','CAP','OLD_SAFE','ROOT_SIZE','NEW_SAFE','PAIR','Q_LOWER','Q_UPPER']},
             'input_sha256':sha(H/'exact_input.json'),'optimizer_calls':0,'frozen_files':len(frozen)}
    save('build_summary.json',summary);print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
