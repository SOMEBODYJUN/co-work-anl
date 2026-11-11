#!/usr/bin/env python3
"""Arbitrary nonnegative internal SAFE, coordinatewise minimal middle caps.

Exact boundary-intersection enumeration only; no optimizer or numerical point.
No imports or execution of earlier project programs.
"""
from fractions import Fraction as F
from itertools import product,combinations
from pathlib import Path
import hashlib,json

OUT=Path(__file__).resolve().parent
WS=OUT.parent
REPO=OUT.parents[3]
OLD=WS/'source2_cap_coupled_internal_safe'
PINS={
 'archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md':'cc4a9dadb09e08b072cb63214d2e084db38db219e4100efbccf9b7f497520e88',
 'research/workspaces/six-boss1-20261111/source2_cap_coupled_internal_safe/freeze_manifest.json':'a744e986913415ac964c6fc12dafa51a86f1982983b2a6fcd0507091bfaafd28',
 'research/workspaces/six-boss1-20261111/source2_cap_coupled_internal_safe/proof.md':'d7d2db3a6bfd84667e13fa82a335c2c1e8face2b07d7736c8277482c71f86eb9',
 'research/workspaces/six-boss1-20261111/source2_cap_coupled_internal_safe/parameter_polytope.json':'56fd324d2a3c68e846e7c97ae823e691ffa70fa9f7ba9144712ffa2c4473e102',
 'research/workspaces/six-boss1-20261111/source2_cap_coupled_internal_safe/state_halfspaces.json':'38a85c71cbebecc429bd0a7ff5e69cb7583aff8b306c1c1d4aa50c949a31486c',
 'research/workspaces/six-boss1-20261111/source2_cap_coupled_internal_safe/hidden_state_checks.json':'12762c9d90ca9275a0b75574d5e1fc1fb50fbb3b81c504e140a5027c66c2ca46',
 'research/workspaces/six-boss1-20261111/source2_cap_coupled_internal_safe/exact_family.json':'b5c950664a21da750245cb7115dc3a60721feb494ce7cf1e32771d5aeeba2906',
 'research/workspaces/six-boss1-20261111/source2_cap_coupled_internal_safe/coordinate_contract.json':'e644b3e2d24379432684361168fa4313b41e9452a8dc68348881a9dd86fbb0e1',
}

def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
def read(f):return json.loads(f.read_text())
def dump(name,x):(OUT/name).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def strings(x):return list(map(str,x))

def guard():
    for p,h in PINS.items():assert sha(REPO/p)==h,p
    old=read(OLD/'freeze_manifest.json')
    keep=dict(old['prior_frozen_artifact_sha256'])
    keep.update({p:rec['sha256'] for p,rec in old['artifacts'].items()})
    for name in ('freeze_manifest.json','SHA256SUMS'):
        f=OLD/name;keep[str(f.relative_to(REPO))]=sha(f)
    assert len(keep)==175
    for p,h in keep.items():assert sha(REPO/p)==h,p
    dump('source_manifest.json',{'source_sha256':PINS,'prior_frozen_artifact_sha256':keep,'old_point_files_sha_only_not_parsed':True,'optimizer_calls':0,'numeric_point_read_or_bound':False,'other_project_code_imported_or_executed':False})
    return keep

def beta(tau):
    t3,t4,t5=tau
    return (F(1,12)+t3+t4/72+t5/36,F(1,12)+t4+t5/36,F(1,12)+t5)

def cost(p,c,o,r,tau,s):
    a=25+sum(tau)-s;b=beta(tau);load=p+c+sum(r)
    numerator=a*c-r[3]-sum(t*bit for t,bit in zip(tau,r[:3]))
    assert load or numerator==0
    value=numerator/load if load else F(0)
    value+=sum(w*bit for w,bit in zip(b,r[:3]))+r[3]
    value+=F(o,6*(p+c+sum(r[:3])+1))
    value+=sum(t*F(o,6*(p+c+sum(r[:k])+7-j)) for k,(j,t) in enumerate(zip((3,4,5),tau)))
    return value

def target(p,c,o,tau,s):
    value=c*(1+sum(beta(tau))+F(24,p+5)-s/5)
    value+=F(o,6*(p+4*c+1))
    value+=sum(t*F(o,6*(p+(j-2)*c+7-j)) for j,t in zip((3,4,5),tau))
    return value

def states():
    for p,c,o in product((0,1),repeat=3):
        for r in product((0,1),repeat=4):yield p,c,o,r

def sid(st):return f'p{st[0]}_c{st[1]}_o{st[2]}_r'+''.join(map(str,st[3]))

def form(st):
    p,c,o,r=st
    def residual(v):return cost(p,c,o,r,v[:3],v[3])-target(p,c,o,v[:3],v[3])
    zero=[F(0)]*4;base=residual(zero)
    return base,[residual([F(j==k) for j in range(4)])-base for k in range(4)]

def facets():
    fs=[]
    for k,j in enumerate((3,4,5)):
        v=[F(0)]*4;v[k]=1;fs.append((f'tau{j}_nonnegative',F(0),v))
    fs.extend([('s_nonnegative',F(0),[F(0),F(0),F(0),F(1)]),('s_at_most9',F(9),[F(0),F(0),F(0),F(-1)])])
    for k,j in enumerate((3,4,5)):
        v=[F(0)]*4;v[k]=-F(4,5)
        for h in range(k+1,3):v[h]=-F(1,6*(4-h)*(5-h))
        fs.append((f'p1_missing_middle{j}',F(43,60),v))
        v=[F(0)]*4;v[k]=-F(3,4);v[3]=-F(1,20)
        for h in range(k+1,3):v[h]=-F(1,6*(4-h)*(5-h))
        fs.append((f'p0_missing_middle{j}_mixed_s',F(67,60),v))
    return fs

def solve(rows):
    m=[list(v)+[-c] for name,c,v in rows]
    for j in range(4):
        k=next((k for k in range(j,4) if m[k][j]),None)
        if k is None:return None
        m[j],m[k]=m[k],m[j];v=m[j][j];m[j]=[x/v for x in m[j]]
        for k in range(4):
            if k!=j:
                v=m[k][j];m[k]=[a-v*b for a,b in zip(m[k],m[j])]
    return tuple(m[k][-1] for k in range(4))

def av(c,v,x):return c+sum(a*b for a,b in zip(v,x))

def main():
    keep=guard();fs=facets();vv=set()
    for chosen in combinations(fs,4):
        v=solve(chosen)
        if v is not None and all(av(c,q,v)>=0 for name,c,q in fs):vv.add(v)
    vv=sorted(vv);assert len(vv)==28
    assert all(av(c,q,[F(1,10)]*3+[F(1)])>0 for name,c,q in fs)
    forms={};half=[]
    for st in states():
        base,co=form(st);forms[sid(st)]=(base,co)
        half.append({'state':sid(st),'p':st[0],'c':st[1],'o':st[2],'tail':list(st[3]),'constant':str(base),'tau3_tau4_tau5_s_coefficients':strings(co)})
    witnesses=[]
    for name,state,factor in [('s_nonnegative',(1,1,0,(1,1,1,1)),F(1,30)),('s_at_most9',(0,1,0,(1,1,1,0)),F(1,20))]:
        witnesses.append((name,state,factor))
    for k,j in enumerate((3,4,5)):
        r=tuple(int(h!=k) for h in range(3))+(1,)
        witnesses.extend([(f'p1_missing_middle{j}',(1,1,0,r),F(1)),(f'p0_missing_middle{j}_mixed_s',(0,1,0,r),F(1))])
    witness_records=[]
    for name,st,factor in witnesses:
        c,q=next((c,q) for label,c,q in fs if label==name)
        a,b=forms[sid(st)]
        assert a==factor*c and b==[factor*x for x in q]
        witness_records.append({'facet':name,'state':sid(st),'scale':str(factor),'residual_constant':str(a),'residual_coefficients':strings(b)})
    vrecords=[];checks=[];mins=[]
    for index,v in enumerate(vv):
        vid=f'V{index:02d}';tau=v[:3];s=v[3];b=beta(tau);a=25+sum(tau)-s
        Kpayment=1+sum(b);mu=Kpayment-s/5
        assert a>=16 and min(b)>=F(1,12)
        vrecords.append({'id':vid,'tau3_tau4_tau5':strings(tau),'s':str(s),'beta3_beta4_beta5':strings(b),'source_IC_weight':str(a),'true_tail_K_weight':str(Kpayment),'C_size_free_multiplier':str(mu),'final_K_weight':str(s/5),'active_facets':[name for name,c,q in fs if av(c,q,v)==0]})
        for p,c,o in product((0,1),repeat=3):
            expected=target(p,c,o,tau,s);values=[]
            for r in product((0,1),repeat=4):
                value=cost(p,c,o,r,tau,s);residual=value-expected
                assert residual>=0,(vid,p,c,o,r,residual)
                cc,q=forms[sid((p,c,o,r))];assert residual==av(cc,q,v)
                checks.append({'vertex':vid,'state':sid((p,c,o,r)),'cost':str(value),'target':str(expected),'residual':str(residual)})
                values.append((r,value))
            anchor=(0,0,0,0) if c==0 else (1,1,1,1) if p==0 else (1,1,1,0)
            assert min(x for r,x in values)==cost(p,c,o,anchor,tau,s)==expected
            mins.append({'vertex':vid,'p':p,'c':c,'o':o,'minimum':str(expected),'common_anchor':list(anchor),'all_attaining_tails':[list(r) for r,x in values if x==expected]})
    dump('parameter_polytope.json',{'status':'COMPLETE_SPECIFIED_MINIMAL_CAP_AFFINE_MIN_DOMAIN','parameter_order':['tau3','tau4','tau5','s'],'dimension':4,'facets':[{'name':name,'constant':str(c),'coefficients':strings(q)} for name,c,q in fs],'facet_convention':'constant+coefficients dot(tau3,tau4,tau5,s)>=0','strict_interior':['1/10','1/10','1/10','1'],'facet_intersections':330,'vertices':vrecords})
    dump('state_halfspaces.json',half);dump('necessary_facet_witnesses.json',witness_records)
    dump('hidden_state_checks.json',checks);dump('minimum_tables.json',mins)
    # Build the exact old-domain translation and full affine state identities.
    old_domain=read(OLD/'parameter_polytope.json');shift=list(map(F,old_domain['theta_star']))+[F(0)]
    assert beta(shift[:3])==(F(1,2),)*3
    oldfacets={f['name']:(F(f['constant']),list(map(F,f['coefficients']))) for f in old_domain['facets']}
    translated=[]
    for name,c,q in fs:
        if name.startswith('tau'):
            # Replace tau>=0 by the tighter slice boundary tau>=theta*.
            j=int(name[3]);c-=shift[j-3];oldname='e'+name[3:]
        else:oldname=name
        translated_const=av(c,q,shift)
        assert (translated_const,q)==oldfacets[oldname]
        translated.append({'new_or_slice_facet':name,'old_facet':oldname,'shifted_constant':str(translated_const),'coefficients':strings(q),'all_five_coefficient_residuals':['0']*5})
    oldhalf=read(OLD/'state_halfspaces.json');state_identity=[]
    for rec in oldhalf:
        c,q=forms[rec['state']]
        assert av(c,q,shift)==F(rec['constant']) and q==list(map(F,rec['e3_e4_e5_s_coefficients']))
        state_identity.append({'state':rec['state'],'constant_residual':'0','four_linear_coefficient_residuals':['0']*4})
    dump('old_domain_slice_identity.json',{'status':'PASS','identity':'old domain = new domain intersect {tau>=theta*}, with tau=theta*+e and unchanged s','theta_star':strings(shift[:3]),'beta_at_theta_star':['1/2']*3,'facets':translated,'all_128_affine_state_identities':state_identity,'facet_coefficient_checks':55,'state_coefficient_checks':640})
    coord=read(OLD/'coordinate_contract.json');rows=[]
    for v in vrecords:
        tau=list(map(F,v['tau3_tau4_tau5']));s=F(v['s']);a=F(v['source_IC_weight']);co={}
        for atom in coord['atom_columns']:
            aa=atom['a'];load=sum(aa);u=F(aa[1],load) if load else F(0)
            p,c,o=aa[0],atom['c'],atom['o']
            value=a*u-F(24*c,p+5)-F(o,6*(p+4*c+1))
            value-=sum(t*F(o,6*(p+(j-2)*c+7-j)) for j,t in zip((3,4,5),tau))
            co[str(atom['index'])]=str(value)
        co['512']=str(s/5)
        rows.append({'name':f'SOURCE2_MINIMAL_CAP_INTERNAL_SAFE_{v["id"]}','family':'SOURCE2_MAXIMUM_C_MINIMAL_CAP_TRUE_INTERNAL_SAFE','vertex_id':v['id'],'source':2,'forced_label':'C_maximum_size_K','tau3_tau4_tau5':v['tau3_tau4_tau5'],'s':v['s'],'source_IC_weight':v['source_IC_weight'],'middle_CAP_weights':v['beta3_beta4_beta5'],'terminal_CAP_weight':'1','terminal_BR_average_weight':'1','true_tail_K_weight':v['true_tail_K_weight'],'C_size_free_multiplier':v['C_size_free_multiplier'],'C_size_equality':'|C|-K=0','a':co,'rhs':'0','numerical_divisor':'25'})
    dump('exact_family.json',{'schema':'source2_minimal_cap_safe_28x513_v1','status':'GENERATED_NO_SOLVE_NO_POINT','raw_rows':28,'variables':513,'K_column':512,'rows':rows,'inequality_convention':'a dot z >=0','complete_finite_generator_for_specified_affine_domain':True,'C_is_genuine_maximum_required':True,'free_equality_multipliers_may_be_negative':True,'optimizer_calls':0})
    dump('coordinate_contract.json',coord)
    # Preserve the negative free multiplier as an explicit sign regression case.
    negative=[v for v in vrecords if F(v['C_size_free_multiplier'])<0]
    assert len(negative)==1 and negative[0]['tau3_tau4_tau5']==['0']*3 and negative[0]['s']=='9'
    assert negative[0]['C_size_free_multiplier']=='-11/20'
    dump('signed_free_multiplier_cases.json',{'status':'VALID_SIGNED_EQUALITY','negative_cases':negative,'meaning':'The C-size equality multiplier is free; no nonnegative-budget assumption applies to it.'})
    output={'status':'PASS','facets':11,'vertices':28,'affine_hidden_states':128,'vertex_state_checks':3584,'minimum_tables_and_all_attainers':224,'necessary_state_witnesses':8,'old_slice_facet_coefficient_identities':55,'old_slice_state_coefficient_identities':640,'new_rows':28,'columns':513,'coefficients':14364,'negative_free_equality_multipliers':1,'negative_free_multiplier':'-11/20','source_IC_minimum':'16','no_point_read_or_bound':True,'optimizer_calls':0,'prior_frozen_artifacts_unchanged':len(keep)}
    dump('derivation_result.json',output);guard();print(json.dumps(output))

if __name__=='__main__':main()
