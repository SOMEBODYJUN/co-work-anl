#!/usr/bin/env python3
"""Source2 true-C branch: jointly pay extra internal SAFE and middle caps.

Exact affine-domain enumeration and complete finite row family. No optimizer,
numeric point, or execution/import of any other project program.
"""
from fractions import Fraction as F
from itertools import product, combinations
from pathlib import Path
import hashlib
import json

OUT=Path(__file__).resolve().parent
WS=OUT.parent
REPO=OUT.parents[3]
THETA=(F(12425,31104),F(175,432),F(5,12))
JS=(3,4,5)
PINS={
 'archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md':'cc4a9dadb09e08b072cb63214d2e084db38db219e4100efbccf9b7f497520e88',
 'research/workspaces/six-boss1-20261111/source2_joint_internal_safe/proof.md':'e4ba6dd0e4cde35a9c899d35e85c53a98a042b257e6bb14a01078726138210e4',
 'research/workspaces/six-boss1-20261111/source2_joint_internal_safe/freeze_manifest.json':'ec51f3eff143d0f555d2601deb1954a06f249aecbd4eabcfab3398d2c45d7b25',
 'research/workspaces/six-boss1-20261111/source2_joint_internal_safe/sixteen_reweighted_vertex_family.json':'a38144bb000e8585d520a731ed4159269a7245e0616d020ca12550d55df3719e',
 'research/workspaces/six-boss1-20261111/all_source_joint_reweighted_safe/coordinate_contract.json':'95621205eab550affe69dc148e9cce49176b8d2c74b9207511583096d1b60b32',
 'research/workspaces/six-boss1-20261111/all_source_ordered_joint_menu/freeze_manifest.json':'eb01d5539bc6b6182871df3e14fa800896e46ba63fa3f52176cb2aee562052fe',
}

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def dump(name,x): (OUT/name).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def strings(xs): return list(map(str,xs))

def guard():
    for p,h in PINS.items(): assert sha(REPO/p)==h,p
    parent=WS/'all_source_ordered_joint_menu/freeze_manifest.json'
    data=json.loads(parent.read_text())
    keep=dict(data['prior_frozen_artifact_sha256'])
    keep.update({p:a['sha256'] for p,a in data['artifacts'].items()})
    for f in ('freeze_manifest.json','SHA256SUMS'):
        path=parent.parent/f;keep[str(path.relative_to(REPO))]=sha(path)
    assert len(keep)==153
    for p,h in keep.items(): assert sha(REPO/p)==h,p
    dump('source_manifest.json',{'source_sha256':PINS,'prior_frozen_artifact_sha256':keep,'prior_protection_mode':'SHA256 only; no old diagnostic point parsed or used.','optimizer_calls':0,'numerical_point_bound':False,'other_project_code_imported_or_executed':False})
    return keep

def gamma(e):
    return [e[k]+sum(e[h]/(6*(7-JS[h])*(8-JS[h])) for h in range(k+1,3)) for k in range(3)]

def genuine_cost(p,c,o,r,e,s,menu_count=None):
    g=gamma(e); a=25+sum(THETA)-s+sum(e)
    load=p+c+sum(r)
    numerator=a*c-r[3]-sum((t+x)*bit for t,x,bit in zip(THETA,e,r[:3]))
    assert load or numerator==0
    val=numerator/load if load else F(0)
    val+=sum((F(1,2)+x)*bit for x,bit in zip(g,r[:3]))+r[3]
    d=o if menu_count is None else menu_count
    val+=F(d,6*(p+c+sum(r[:3])+1))
    val+=sum((t+x)*F(d,6*(p+c+sum(r[:k])+7-j)) for k,(j,t,x) in enumerate(zip(JS,THETA,e)))
    return val

def proposed_minimum(p,c,o,e,s):
    val=F(5,2)*c+F(24*c,p+5)+F(o,6*(p+1+4*c))-s*F(c,5)
    val+=c*sum(gamma(e))
    val+=sum((t+x)*F(o,6*(p+(j-2)*c+7-j)) for j,t,x in zip(JS,THETA,e))
    return val

def all_states():
    for p,c,o in product((0,1),repeat=3):
        for r in product((0,1),repeat=4): yield p,c,o,r

def state_id(p,c,o,r): return f'p{p}_c{c}_o{o}_r'+''.join(map(str,r))

def affine_residual(state):
    p,c,o,r=state;zero=[F(0)]*3
    const=genuine_cost(p,c,o,r,zero,F(0))-proposed_minimum(p,c,o,zero,F(0))
    coefficients=[]
    for k in range(4):
        v=[F(j==k) for j in range(4)]
        value=genuine_cost(p,c,o,r,v[:3],v[3])-proposed_minimum(p,c,o,v[:3],v[3])
        coefficients.append(value-const)
    return const,coefficients

def facets(include_mixed=True):
    ff=[]
    for k,j in enumerate(JS):
        q=[F(0)]*4;q[k]=F(1)
        ff.append((f'e{j}_nonnegative',F(0),q))
    ff.append(('s_nonnegative',F(0),[F(0),F(0),F(0),F(1)]))
    ff.append(('s_at_most9',F(9),[F(0),F(0),F(0),F(-1)]))
    for k,j in enumerate(JS):
        q=[F(0)]*4;q[k]=-F(4,5)
        for h in range(k+1,3):q[h]=-F(1,6*(7-JS[h])*(8-JS[h]))
        ff.append((f'p1_missing_middle{j}',F(3,10)+THETA[k]/5,q))
        if include_mixed:
            q=[F(0)]*4;q[k]=-F(3,4);q[3]=-F(1,20)
            for h in range(k+1,3):q[h]=-F(1,6*(7-JS[h])*(8-JS[h]))
            ff.append((f'p0_missing_middle{j}_mixed_s',F(7,10)+THETA[k]/4,q))
    return ff

def solve(rows):
    a=[q[:]+[-c] for _,c,q in rows]
    for col in range(4):
        pivot=next((k for k in range(col,4) if a[k][col]),None)
        if pivot is None:return None
        a[col],a[pivot]=a[pivot],a[col]
        divisor=a[col][col];a[col]=[x/divisor for x in a[col]]
        for k in range(4):
            if k!=col:
                factor=a[k][col];a[k]=[x-factor*y for x,y in zip(a[k],a[col])]
    return tuple(a[k][-1] for k in range(4))

def av(c,q,x): return c+sum(a*b for a,b in zip(q,x))

def vertices(ff):
    found=set();attempts=0
    for pick in combinations(ff,4):
        attempts+=1;v=solve(pick)
        if v is not None and all(av(c,q,v)>=0 for _,c,q in ff):found.add(v)
    return sorted(found),attempts

def main():
    protected=guard()
    ff=facets();vv,attempts=vertices(ff)
    assert len(ff)==11 and len(vv)==28 and attempts==330
    assert all(av(c,q,[F(1,10)]*3+[F(1)])>0 for _,c,q in ff)
    spaces=[];state_forms={}
    for st in all_states():
        const,co=affine_residual(st);state_forms[st]=(const,co)
        p,c,o,r=st
        spaces.append({'state':state_id(*st),'p':p,'c':c,'o':o,'tail':list(r),'constant':str(const),'e3_e4_e5_s_coefficients':strings(co)})
    witnesses=[]
    def witness(name,st,scale):
        fc,fq=next((c,q) for label,c,q in ff if label==name)
        rc,rq=state_forms[st]
        assert rc==scale*fc and rq==[scale*x for x in fq]
        witnesses.append({'facet':name,'state':state_id(*st),'scale':str(scale),'residual_constant':str(rc),'residual_coefficients':strings(rq)})
    witness('s_nonnegative',(1,1,0,(1,1,1,1)),F(1,30))
    witness('s_at_most9',(0,1,0,(1,1,1,0)),F(1,20))
    for k,j in enumerate(JS):
        tail=tuple(int(h!=k) for h in range(3))+(1,)
        witness(f'p1_missing_middle{j}',(1,1,0,tail),F(1))
        witness(f'p0_missing_middle{j}_mixed_s',(0,1,0,tail),F(1))
    checks=[];minimums=[];vrecords=[]
    for index,v in enumerate(vv):
        vid=f'V{index:02d}';e=v[:3];s=v[3];g=gamma(e);a=25+sum(THETA)-s+sum(e)
        tailK=F(5,2)+sum(g);mu=tailK-s/5
        assert a>0 and mu>0 and min(g)>=0
        vrecords.append({'id':vid,'e3_e4_e5':strings(e),'s':str(s),'Gamma3_Gamma4_Gamma5':strings(g),'theta3_theta4_theta5':strings([t+x for t,x in zip(THETA,e)]),'source_IC_weight':str(a),'true_tail_K_weight':str(tailK),'C_size_free_multiplier':str(mu),'final_K_weight':str(s/5),'active_facets':[name for name,c,q in ff if av(c,q,v)==0]})
        for p,c,o in product((0,1),repeat=3):
            target=proposed_minimum(p,c,o,e,s);values=[]
            for r in product((0,1),repeat=4):
                cost=genuine_cost(p,c,o,r,e,s);rho=cost-target
                assert rho>=0,(vid,p,c,o,r,rho)
                constant,co=state_forms[p,c,o,r]
                assert rho==av(constant,co,v)
                checks.append({'vertex':vid,'state':state_id(p,c,o,r),'cost':str(cost),'target':str(target),'residual':str(rho)})
                values.append((r,cost))
            assert min(z for r,z in values)==target
            anchor=(0,0,0,0) if c==0 else (1,1,1,1) if p==0 else (1,1,1,0)
            assert genuine_cost(p,c,o,anchor,e,s)==target
            minimums.append({'vertex':vid,'p':p,'c':c,'o':o,'minimum':str(target),'common_anchor':list(anchor),'all_attaining_tails':[list(r) for r,z in values if z==target]})
    # Preserve the rejected product candidate, including its exact simple failure.
    naive,_=vertices(facets(False));failures=[]
    for v in naive:
        for st,(const,co) in state_forms.items():
            value=av(const,co,v)
            if value<0: failures.append({'e':strings(v[:3]),'s':str(v[3]),'state':state_id(*st),'residual':str(value)})
    assert len(naive)==16 and len(failures)==12
    e=(F(0),F(0),F(23,48));badstate=(0,1,0,(1,1,0,1))
    bad=av(*state_forms[badstate],e+(F(9),))
    assert bad==-F(1,192)
    assert all(av(c,q,e+(F(0),))>=0 for _,c,q in ff)
    dump('rejected_product_candidate.json',{'status':'REJECTED','candidate':'e>=0 and three p1 caps, times s in [0,9]','candidate_vertices':16,'negative_hidden_states':failures,'simple_nonproduct_witness':{'e':['0','0','23/48'],'s0_feasible':True,'s9_infeasible':True,'state':state_id(*badstate),'s9_residual':'-1/192'}})
    dump('parameter_polytope.json',{'status':'COMPLETE_SPECIFIED_AFFINE_MIN_DOMAIN','parameter_order':['e3','e4','e5','s'],'theta_star':strings(THETA),'dimension':4,'facet_convention':'constant+coefficients dot(e3,e4,e5,s)>=0','facets':[{'name':name,'constant':str(c),'coefficients':strings(q)} for name,c,q in ff],'strict_interior':['1/10','1/10','1/10','1'],'facet_intersections_attempted':attempts,'vertices':vrecords,'is_product_E_times_0_9':False})
    dump('state_halfspaces.json',spaces)
    dump('necessary_facet_witnesses.json',witnesses)
    dump('hidden_state_checks.json',checks)
    dump('minimum_tables.json',minimums)
    # Exact menu weakening identity, checked coefficientwise in e,s.
    menu_cases=0
    for p,c in product((0,1),repeat=2):
        for r in product((0,1),repeat=4):
            for menu in product((0,1),repeat=6):
                d=sum(menu);o=int(any(menu))
                terminal=sum(F(bit,p+c+sum(r[:3])+1) for bit in menu)/6
                assert terminal-F(o,6*(p+c+sum(r[:3])+1))==F(d-o,6*(p+c+sum(r[:3])+1))
                for k,j in enumerate(JS):
                    den=p+c+sum(r[:k])+7-j
                    actual=sum(F(bit,den) for bit in menu)/6
                    assert actual-F(o,6*den)==F(d-o,6*den)
                menu_cases+=1
    assert menu_cases==4096 and len(checks)==3584 and len(minimums)==224
    # C is a genuine maximum; apply only E_C=|C|-K after true cap payment.
    coord=json.loads((WS/'all_source_joint_reweighted_safe/coordinate_contract.json').read_text())
    rows=[]
    for v in vrecords:
        e=list(map(F,v['e3_e4_e5']));s=F(v['s']);a=F(v['source_IC_weight'])
        co={}
        for atom in coord['atom_columns']:
            aa=atom['a'];p=aa[0];c=atom['c'];o=atom['o'];load=sum(aa)
            ui=F(aa[1],load) if load else F(0)
            value=a*ui-F(24*c,p+5)-F(o,6*(p+4*c+1))
            value-=sum((t+x)*F(o,6*(p+(j-2)*c+7-j)) for j,t,x in zip(JS,THETA,e))
            co[str(atom['index'])]=str(value)
        co['512']=str(s/5)
        rows.append({'name':f'SOURCE2_CAP_COUPLED_INTERNAL_SAFE_{v["id"]}','family':'TRUE_SOURCE2_MAXIMUM_C_CAP_COUPLED_INTERNAL_SAFE','vertex_id':v['id'],'source':2,'forced_label':'C_maximum_size_K','e3_e4_e5':v['e3_e4_e5'],'s':v['s'],'theta3_theta4_theta5':v['theta3_theta4_theta5'],'source_IC_weight':v['source_IC_weight'],'middle_CAP_weights':strings([F(1,2)+F(g) for g in v['Gamma3_Gamma4_Gamma5']]),'terminal_CAP_weight':'1','terminal_BR_average_weight':'1','true_tail_K_weight':v['true_tail_K_weight'],'C_size_free_multiplier':v['C_size_free_multiplier'],'C_size_equality':'|C|-K=0','a':co,'rhs':'0','numerical_divisor':'25'})
    dump('coordinate_contract.json',{'variables':513,'K_column':512,'bit_order':coord['bit_order'],'atom_columns':coord['atom_columns'],'C_size_equality':{'a':{str(x['index']):str(x['c']) for x in coord['atom_columns']}|{'512':'-1'},'rhs':'0'}})
    dump('exact_family.json',{'schema':'source2_cap_coupled_internal_safe_28x513_v1','status':'GENERATED_NO_POINT_NO_SOLVE','rows':rows,'raw_rows':28,'variables':513,'K_column':512,'inequality_convention':'a dot z >=0','complete_finite_generator_for_specified_affine_domain':True,'uses_genuine_maximum_C':True,'raw_scale':'terminal BR mean weight1','numerical_positive_divisor':'25','optimizer_calls':0})
    output={'status':'PASS','complete_domain_facets':11,'parameter_vertices':28,'facet_intersections':330,'all_affine_hidden_states':128,'vertex_state_checks':3584,'minimum_tables_and_all_attainers':224,'necessary_hidden_state_witnesses':8,'original_product_candidate_rejected_states':12,'simple_product_failure':'-1/192','menu_cases':4096,'global_rows':28,'global_columns':513,'global_coefficients':28*513,'source_IC_minimum':str(min(F(v['source_IC_weight']) for v in vrecords)),'no_numerical_point_read_or_bound':True,'optimizer_calls':0,'prior_frozen_artifacts_unchanged':len(protected)}
    dump('derivation_result.json',output)
    guard();print(json.dumps(output))

if __name__=='__main__':main()
