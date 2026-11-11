#!/usr/bin/env python3
"""Exact 128-type root-C branch system. No optimizer and no old builder."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product,combinations_with_replacement
import json,hashlib

H=Path(__file__).resolve().parent;WS=H.parent;REPO=WS.parents[2]
K0=F(24376964954228547006,142891298915142483961)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(name,obj):(H/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
def query(label,v):
    if label=='Omean':return F(v['bits'][6],6)
    return F(v['bits'][0 if label=='C' else int(label[1:])-1])
def descriptors():
    rows=[{'name':'ROOT_IC','family':'ROOT_IC'}]
    rows += [{'name':f'CAP_B{j}','family':'CAP','source':j} for j in range(2,7)]
    rows += [{'name':'BRANCH_UNION_OPT','family':'UNION'},{'name':'ROOT_K_FLOOR','family':'FLOOR'}]
    names=['C','B2','B3','B4','B5','B6','Omean']
    rows += [{'name':f'SAFE_j{j}|{q}','family':'SAFE','source':j,'queries':[q]} for j in range(2,7) for q in names]
    rows += [{'name':f'PAIR|{q}|{r}','family':'PAIR','queries':[q,r]} for q,r in combinations_with_replacement(names,2)]
    return rows
def coeff(row,v):
    bits=v['bits'];l=bits[:6];c=sum(l);pay=lambda j:F(l[j-1],c) if c else F(0);fam=row['family']
    if fam=='ROOT_IC':return -pay(1)
    if fam=='CAP':return -F(l[row['source']-1])
    if fam=='UNION':return -F(int(c>0))
    if fam=='FLOOR':return F(0)
    if fam=='SAFE':
        j=row['source'];return pay(j)-query(row['queries'][0],v)/(sum(l[:j-1])+7-j)
    D=sum(l[:4])+1;y,z=l[4:];q,r=[query(q,v) for q in row['queries']]
    return F(y,D+z)+F(z,D+y)+F(y,D*(D+1))-(q+r)/D+q*r/(D*(D+1))
def main():
    H.mkdir(exist_ok=True)
    frozen={}
    for p in sorted((WS/'universal_true_x_tail').rglob('*')):
        if p.is_file():frozen[str(p.relative_to(REPO))]=sha(p)
    rels=['research/workspaces/six-boss1-20261111/universal_true_x_tail.md',
          'research/workspaces/six-boss1-20261111/main_root_near_strengthening.md',
          'research/workspaces/six-boss1-20261111/main_universal_wallet_face.md',
          'research/workspaces/six-boss1-20261111/main_full_average_pair.md',
          'archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md',
          'archives/customer-attraction/state/引理/任意人数近饱和根主题刚性--引理.md',
          'research/workspaces/six-boss1-20261111/universal_union_wallet_lp/exact_input.json',
          'research/workspaces/six-boss1-20261111/universal_union_wallet_lp/exact_certificate.json']
    for rel in rels:frozen[rel]=sha(REPO/rel)
    save('frozen_sources_before.json',frozen)
    old=json.loads((WS/'universal_union_wallet_lp/exact_certificate.json').read_text())
    assert F(old['K'])==K0
    atoms=[{'index':j,'bits':list(bits)} for j,bits in enumerate(product((0,1),repeat=7))]
    rows=descriptors()
    for row in rows:
        row['a']={str(v['index']):str(coeff(row,v)) for v in atoms if coeff(row,v)}
        if row['family'] in ('ROOT_IC','FLOOR'):row['a']['128']='1'
        row['bK']='-1' if row['family']=='CAP' else ('1/6' if row['family']=='FLOOR' else '0')
        row['bO']='-1' if row['family']=='UNION' else '0'
        row['rhs']=str(F(row['bK'])*K0+F(row['bO']))
    eq=[{'name':'C_size','a':{str(v['index']):'1' for v in atoms if v['bits'][0]},'rhs':str(K0),'parameter':'K'},
        {'name':'OPT_union','a':{str(v['index']):'1' for v in atoms if v['bits'][6]},'rhs':'1','parameter':'O'}]
    data={'scope':'All-128-type necessary true maximal-size-C root-branch cone, not a full SPE characterization.',
          'bit_order':['p','y2','y3','y4','y5','z','o'],'atoms':atoms,'root_u_column':128,
          'nonnegative_columns':list(range(129)),'fixed_K':str(K0),'fixed_O':'1',
          'objective':{'128':'1'},'convention':'A*x >= bK*K+bO*O',
          'raw_rows':rows,'equalities':eq,'derivation_sha256':sha(H/'derivation.md'),
          'source_manifest_sha256':sha(H/'frozen_sources_before.json')}
    assert len(rows)==71
    save('exact_input.json',data)
    summary={'columns':129,'all_boolean_atom_types':128,'raw_rows':len(rows),'equalities':2,
             'family_counts':{f:sum(r['family']==f for r in rows) for f in ['ROOT_IC','CAP','UNION','FLOOR','SAFE','PAIR']},
             'raw_zero_rows':[r['name'] for r in rows if not r['a'] and F(r['rhs'])==0],
             'all_raw_rows_retained':True,'input_sha256':sha(H/'exact_input.json'),'optimizer_calls':0}
    save('build_summary.json',summary);print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
