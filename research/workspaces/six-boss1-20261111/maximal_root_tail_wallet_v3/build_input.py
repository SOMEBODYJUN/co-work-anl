#!/usr/bin/env python3
"""Build exactly 72 unchanged symbolic rows + PAIR30/C30 + 196 P25 rows."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
from hashlib import sha256
import json

H=Path(__file__).resolve().parent; WS=H.parent; ROOT=WS.parents[2]
K=F(87254934961879537539921985657780687995,449980920529477462633417363589807278334)
BINDINGS={
 'maximal_root_tail_wallet_v2/exact_input.json':'86a235bf210862ef8f8bbbdea7ac324e71f691a8aa7af455a821e6379cfe117d',
 'universal_union_wallet_v6/exact_certificate.json':'98fa318efae0c6fef36e87b1861d559ede340ab4aaf7ed390c426854e5711f1d',
 'universal_union_wallet_v6/exact_input.json':'49532be5fae2913f2ab56ae641452510d7b0f8f14ff7049de0dd62fa7b9a8936',
 'main_thirty_index_strengthening/proof.md':'d1b3fcec20b3694d76499bcc1566a6a89b80d5b9e738b6bc71d82a5f2bfb42ac',
 'main_thirty_index_strengthening/requery30_envelopes.json':'14ef732b35d0f859113daf92c8dda1f08330413682b057c69a57543a41a360bc',
 'main_all_source25_family/proof.md':'abe4e15a1d07b97ff230514f82415106267ad317bd94ef34ff0f0a3131f46bd0',
 'main_all_source25_family/exact_family.json':'8965ab6534776f0cc9570979128df1e99835e0cc0bf60ce9d4a87b5354d4bec0',
 'main_all_source25_family/manifest.json':'8cebe7796d8c329da25f11a4591d182266a8d69771ffa6c7cf618395ef452015'}
def digest(p): return sha256(p.read_bytes()).hexdigest()
def save(n,o): (H/n).write_text(json.dumps(o,indent=2,ensure_ascii=False)+'\n')
def share(bit,total): return F(bit,total) if total else F(0)

def main():
    assert not (H/'DISCOVERY_CALL_CONSUMED.json').exists(), 'Input is locked after discovery.'
    for p,d in BINDINGS.items(): assert digest(WS/p)==d,(p,digest(WS/p))
    source_dirs=['maximal_root_tail_wallet','maximal_root_tail_wallet_v2','maximal_root_tail_wallet_v2_audit',
                 'maximal_root_opt_requery','main_thirty_index_strengthening','main_all_source25_family']
    files=[p for d in source_dirs for p in (WS/d).rglob('*') if p.is_file()]
    files += [WS/p for p in BINDINGS]
    files += [ROOT/'archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md', WS/'spec.json', WS/'main_universal_wallet_v6_check.json']
    frozen={str(p.relative_to(ROOT)):digest(p) for p in sorted(set(files))}
    save('frozen_sources_before.json',frozen)
    check=json.loads((WS/'main_universal_wallet_v6_check.json').read_text())
    assert check['status']=='PASS_MAIN_ALL867_ROWS257_COLUMNS_AND_INDEPENDENT_P25_REBUILD'
    assert F(check['K'])==K and check['certificate_sha256']==BINDINGS['universal_union_wallet_v6/exact_certificate.json']
    old=json.loads((WS/'maximal_root_tail_wallet_v2/exact_input.json').read_text())
    rows=json.loads(json.dumps(old['raw_rows'])); assert len(rows)==72
    for row in rows: row['rhs']=str(F(row['bK'])*K+F(row['bO']))
    atoms=old['atoms']; env=json.loads((WS/'main_thirty_index_strengthening/requery30_envelopes.json').read_text())
    pair={}; cut={}
    for atom,e in zip(atoms,env):
        h=atom['index']; bits=atom['bits']; l=bits[:6]; total=sum(l); D=1+sum(l[:4]); o=bits[6]
        assert e['h']==h and e['bits']==bits
        v=lambda i:share(l[i-1],total)
        pair[str(h)]=str(v(5)+v(6)+F(l[4],D*(D+1))-F(o,3*D))
        cut[str(h)]=str(126000*v(3)+65719*v(4)+4962*v(6)-F(e['m30']))
    rows.append({'name':'PAIR30|Omean|Omean','family':'PAIR30','queries':['Omean','Omean'],
                 'a':{j:v for j,v in pair.items() if F(v)},'bK':'0','bO':'0','rhs':'0','numerical_divisor':'1'})
    rows.append({'name':'OPT_SOURCE3_REQUERY_30_CUT','family':'REQUERY_30_CUT',
                 'a':{j:v for j,v in cut.items() if F(v)},'bK':'0','bO':'0','rhs':'0','numerical_divisor':'126000'})
    roles=['C','B2','B3','B4','B5','B6','Omean']
    for i in range(2,6):
        n=6-i;c=F(n+1,2)
        for ti,T in enumerate(roles):
            for qi,Q in enumerate(roles):
                coefficients={}
                for atom in atoms:
                    bits=atom['bits'];l=bits[:6];o=bits[6];p=sum(l[:i-1]);D=p+n+1
                    A=c+F(24,D);B=F(1,p+1);Cq=F(n,(p+1)*D)
                    if ti<6 and qi<6:
                        t=l[ti];q=l[qi];cost=A*t+B*q-Cq*t*q
                    elif ti<6: cost=A*l[ti]+F(o,6)*(B-Cq*l[ti])
                    elif qi<6: cost=B*l[qi]+F(o,6)*(A-Cq*l[qi])
                    else: cost=F(o,6)*(A+B)
                    value=25*share(l[i-1],sum(l))-cost
                    if value: coefficients[str(atom['index'])]=str(value)
                rows.append({'name':f'PORTFOLIO25_i{i}|T={T}|Q={Q}','family':'ROOT_BRANCH_PORTFOLIO25',
                             'source':i,'T':T,'Q':Q,'a':coefficients,'bK':str(-c),'bO':'0','rhs':str(-c*K),'numerical_divisor':'25'})
    eq=json.loads(json.dumps(old['equalities']));eq[0]['rhs']=str(K);eq[1]['rhs']='1'
    result={'scope':'True maximal naked-size C root branch; old72 symbolic rows + PAIR30 + C30 + P25 on true sources2..5; O=OPT6 in this cone.',
            'bit_order':old['bit_order'],'semantic_bit_order':['C','B2','B3','B4','B5','B6','o'],
            'atoms':atoms,'root_u_column':128,'nonnegative_columns':list(range(129)),
            'fixed_K':str(K),'fixed_O':'1','objective':{'128':'1'},'convention':'A*x >= bK*K+bO*O',
            'raw_rows':rows,'equalities':eq,'source_bindings':BINDINGS,'old_symbolic_rows_preserved':72,
            'source_review_sha256':digest(H/'source_review.md'),'source_manifest_sha256':digest(H/'frozen_sources_before.json'),
            'numeric_scaling':'Original72 divisors retained; appended PAIR30 /1, C30 /126000, each P25 /25. Original exact rows remain unscaled.'}
    assert len(rows)==270 and len({r['name'] for r in rows})==270
    save('exact_input.json',result)
    out={'status':'BUILT_NOT_SOLVED','rows':270,'columns':129,'equalities':2,'retained_symbolic_rows':72,
         'appended_rows':{'PAIR30':1,'C30':1,'P25':196},'fixed_K':str(K),'fixed_O':'1',
         'input_sha256':digest(H/'exact_input.json'),'source_review_sha256':digest(H/'source_review.md'),
         'source_files_frozen':len(frozen),'optimizer_calls':0}
    save('build_summary.json',out);print(json.dumps(out,indent=2))
if __name__=='__main__':main()
