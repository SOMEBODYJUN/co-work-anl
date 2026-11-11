#!/usr/bin/env python3
"""Independent true-share, minimal-cap, full-domain and inclusion verification."""
from fractions import Fraction as F
from itertools import product,combinations
from pathlib import Path
import json,hashlib

OUT=Path(__file__).resolve().parent
WS=OUT.parent
REPO=OUT.parents[3]
OLD=WS/'source2_cap_coupled_internal_safe'

def read(name):return json.loads((OUT/name).read_text())
def dump(name,x):(OUT/name).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()

def price(tau,s):
    cap={j:F(1,12) for j in (3,4,5)}
    cap[6]=F(1)
    for j,t in zip((3,4,5),tau):
        cap[j]+=t
        for k in range(3,j):cap[k]+=t/F(6*(7-j)*(8-j))
    return F(25)+sum(tau)-s,cap,{j:t for j,t in zip((3,4,5),tau)}

def literal(p,c,o,r,tau,s,override=None):
    a,cap,safe=price(tau,s)
    if override is not None:
        for j,v in zip((3,4,5),override):cap[j]=v
    actions=(p,c)+tuple(r);load=sum(actions)
    share=[F(bit,load) if bit else F(0) for bit in actions]
    answer=a*share[1]+sum(w*actions[j-1] for j,w in cap.items())
    menu=(o,0,0,0,0,0)
    answer+=sum(F(q,1+sum(actions[:5])) for q in menu)/6-share[5]
    for j,w in safe.items():
        query=sum(F(q,sum(actions[:j-1])+1+6-j) for q in menu)/6
        answer+=w*(query-share[j-1])
    return answer

def anchor(p,c):return (0,0,0,0) if c==0 else (1,1,1,0) if p else (1,1,1,1)

def residual_form(p,c,o,r):
    def value(v):return literal(p,c,o,r,v[:3],v[3])-literal(p,c,o,anchor(p,c),v[:3],v[3])
    base=value([F(0)]*4)
    return base,[value([F(j==k) for j in range(4)])-base for k in range(4)]

def affine_rank(rows):
    basis={}
    for row in rows:
        v=list(row)
        for j,b in sorted(basis.items()):
            q=v[j]
            if q:v=[x-q*y for x,y in zip(v,b)]
        pivot=next((j for j,x in enumerate(v) if x),None)
        if pivot is not None:
            q=v[pivot];basis[pivot]=[x/q for x in v]
    return len(basis)

def solve4(selected):
    a=[q[:]+[-c] for name,c,q in selected]
    for col in range(4):
        pivot=next((r for r in range(col,4) if a[r][col]),None)
        if pivot is None:return None
        a[col],a[pivot]=a[pivot],a[col];q=a[col][col];a[col]=[x/q for x in a[col]]
        for r in range(4):
            if r!=col:
                q=a[r][col];a[r]=[x-q*y for x,y in zip(a[r],a[col])]
    return tuple(a[j][-1] for j in range(4))

def main():
    guard=read('source_manifest.json')
    for key in ('source_sha256','prior_frozen_artifact_sha256'):
        for p,h in guard[key].items():assert sha(REPO/p)==h,p
    domain=read('parameter_polytope.json');forms={};c0records=[];c1records=[]
    saved={x['state']:x for x in read('state_halfspaces.json')}
    for p,c,o in product((0,1),repeat=3):
        for r in product((0,1),repeat=4):
            sid=f'p{p}_c{c}_o{o}_r'+''.join(map(str,r))
            base,q=residual_form(p,c,o,r);forms[p,c,o,r]=(base,q)
            assert base==F(saved[sid]['constant']) and q==list(map(F,saved[sid]['tau3_tau4_tau5_s_coefficients']))
            if c==0:
                assert base>=0 and min(q[:3])>=0 and q[3]==0
                c0records.append({'state':sid,'constant':str(base),'tau_coefficients':list(map(str,q[:3]))})
    for p in (0,1):
        for r in product((0,1),repeat=4):
            c1,q1=forms[p,1,1,r];c0,q0=forms[p,1,0,r]
            d=c1-c0;co=[x-y for x,y in zip(q1,q0)]
            assert d>=0 and min(co[:3])>=0 and co[3]==0
            c1records.append({'p':p,'tail':list(r),'constant_difference':str(d),'tau_coefficient_differences':list(map(str,co[:3]))})
    # Minimal cap is necessary coordinate by coordinate, from a single-middle
    # c=0,p=0,o=1 state with each cap treated as an independent variable.
    minimal_records=[]
    for k,j in enumerate((3,4,5)):
        r=tuple(int(h==k) for h in range(3))+(0,)
        def residual(v):
            tau=v[:3];caps=v[3:6]
            return literal(0,0,1,r,tau,F(0),caps)-literal(0,0,1,(0,0,0,0),tau,F(0),caps)
        constant=residual([F(0)]*6)
        co=[residual([F(h==ell) for h in range(6)])-constant for ell in range(6)]
        expected=[F(0)]*6;expected[k]=-1;expected[3+k]=1
        for h in range(k+1,3):expected[h]=-F(1,6*(4-h)*(5-h))
        assert constant==-F(1,12) and co==expected
        minimal_records.append({'source':j,'state_tail':list(r),'constant':str(constant),'tau3_tau4_tau5_beta3_beta4_beta5_coefficients':list(map(str,co))})
    dump('analytic_c0_and_query_checks.json',{'status':'PASS','c0_forms_nonnegative_for_all_tau_ge0':c0records,'c1_o1_minus_o0_nonnegative_forms':c1records,'coordinatewise_minimal_cap_necessary_forms':minimal_records,'scope':'Minimality is for the specified zero-C affine anchor, not all possible SPE wallets.'})
    recovered=[]
    for k,j in enumerate((3,4,5)):
        q=[F(0)]*4;q[k]=1;recovered.append((f'tau{j}_nonnegative',F(0),q))
    for name,state,mult in [('s_nonnegative',(1,1,0,(1,1,1,1)),F(30)),('s_at_most9',(0,1,0,(1,1,1,0)),F(20))]:
        c,q=forms[state];recovered.append((name,c*mult,[x*mult for x in q]))
    for k,j in enumerate((3,4,5)):
        r=tuple(int(h!=k) for h in range(3))+(1,)
        for p,label in [(1,f'p1_missing_middle{j}'),(0,f'p0_missing_middle{j}_mixed_s')]:
            c,q=forms[p,1,0,r];recovered.append((label,c,q))
    assert {n:(c,q) for n,c,q in recovered}=={r['name']:(F(r['constant']),list(map(F,r['coefficients']))) for r in domain['facets']}
    vertices=set()
    for chosen in combinations(recovered,4):
        v=solve4(chosen)
        if v is not None and all(c+sum(x*y for x,y in zip(q,v))>=0 for name,c,q in recovered):vertices.add(v)
    assert vertices=={tuple(map(F,v['tau3_tau4_tau5']+[v['s']])) for v in domain['vertices']}
    assert len(vertices)==28
    facet_records=[]
    for name,c,q in recovered:
        on=[v for v in vertices if c+sum(x*y for x,y in zip(q,v))==0]
        dim=affine_rank([[a-b for a,b in zip(v,on[0])] for v in on[1:]])
        assert dim==3;facet_records.append({'facet':name,'affine_dimension':dim,'vertex_count':len(on)})
    stored_states={(x['vertex'],x['state']):x for x in read('hidden_state_checks.json')}
    stored_min={(x['vertex'],x['p'],x['c'],x['o']):x for x in read('minimum_tables.json')}
    minima={};prices={};state_count=0
    for v in domain['vertices']:
        vid=v['id'];tau=list(map(F,v['tau3_tau4_tau5']));s=F(v['s']);a,caps,safe=price(tau,s)
        H=sum(caps.values());mu=H-s/5
        assert a>=16 and min(caps.values())>=F(1,12) and min(safe.values())>=0
        assert a==F(v['source_IC_weight']) and H==F(v['true_tail_K_weight']) and mu==F(v['C_size_free_multiplier'])
        # mu is a free equality multiplier; its negative values must be retained.
        prices[vid]=(a,caps,safe,H,mu,s)
        for p,c,o in product((0,1),repeat=3):
            values=[(r,literal(p,c,o,r,tau,s)) for r in product((0,1),repeat=4)]
            low=min(x for r,x in values);minima[vid,p,c,o]=low
            assert literal(p,c,o,anchor(p,c),tau,s)==low
            rec=stored_min[vid,p,c,o]
            assert F(rec['minimum'])==low and rec['all_attaining_tails']==[list(r) for r,x in values if x==low]
            for r,value in values:
                sid=f'p{p}_c{c}_o{o}_r'+''.join(map(str,r));saved=stored_states[vid,sid]
                assert F(saved['cost'])==value and F(saved['target'])==low and F(saved['residual'])==value-low>=0
                state_count+=1
    assert state_count==3584
    family=read('exact_family.json');coord=read('coordinate_contract.json');identities=[];columns=0
    for row in family['rows']:
        a,caps,safe,H,mu,s=prices[row['vertex_id']]
        assert F(row['source_IC_weight'])==a and F(row['C_size_free_multiplier'])==mu
        assert list(map(F,row['middle_CAP_weights']))==[caps[j] for j in (3,4,5)]
        residuals=[]
        for k in range(512):
            bits=tuple((k>>(8-j))&1 for j in range(9));atom=coord['atom_columns'][k]
            assert tuple(atom['a'])+(atom['x'],atom['o'],atom['c'])==bits
            actual_share=F(1,sum(bits[:6])) if bits[1] else F(0)
            expected=a*actual_share-minima[row['vertex_id'],bits[0],bits[8],bits[7]]+mu*bits[8]
            residual=F(row['a'][str(k)])-expected;assert residual==0
            residuals.append(str(residual));columns+=1
        assert H-mu==s/5==F(row['a']['512'])
        residuals.append('0');columns+=1
        identities.append({'row':row['name'],'true_K_payment':str(H),'signed_C_equality_multiplier':str(mu),'final_K_coefficient':str(H-mu),'all_513_residuals':residuals})
    assert columns==14364 and sum(mu<0 for a,b,t,H,mu,s in prices.values())==1
    negative=next(x for x in prices.values() if x[4]<0)
    assert negative[4]==-F(11,20) and negative[3]==F(5,4) and negative[5]==9
    dump('signed_free_C_identity_checks.json',{'status':'PASS','identity':'final=true_budget+menu_weakening+hidden_residual+mu*(|C|-K)','records':identities,'columns_checked':columns})
    # Exact old-domain slice and old whole-customer rows, using only frozen data.
    old_domain=json.loads((OLD/'parameter_polytope.json').read_text());theta=list(map(F,old_domain['theta_star']))
    old_states={(x['vertex'],x['state']):x for x in json.loads((OLD/'hidden_state_checks.json').read_text())}
    old_rows={r['vertex_id']:r for r in json.loads((OLD/'exact_family.json').read_text())['rows']}
    old_records=[];old_cost_count=0;old_column_count=0
    for v in old_domain['vertices']:
        e=list(map(F,v['e3_e4_e5']));s=F(v['s']);tau=[x+y for x,y in zip(theta,e)];point=tau+[s]
        assert all(c+sum(x*y for x,y in zip(q,point))>=0 for name,c,q in recovered)
        a,caps,safe=price(tau,s);mu=sum(caps.values())-s/5
        assert a==F(v['source_IC_weight']) and mu==F(v['C_size_free_multiplier'])
        for j in (3,4,5):assert caps[j]==F(1,2)+F(v['Gamma3_Gamma4_Gamma5'][j-3])
        for p,c,o in product((0,1),repeat=3):
            for r in product((0,1),repeat=4):
                value=literal(p,c,o,r,tau,s);sid=f'p{p}_c{c}_o{o}_r'+''.join(map(str,r))
                assert value==F(old_states[v['id'],sid]['cost']);old_cost_count+=1
        row=old_rows[v['id']];residuals=[]
        for k in range(512):
            bits=tuple((k>>(8-j))&1 for j in range(9));p,c,o=bits[0],bits[8],bits[7]
            u=F(1,sum(bits[:6])) if bits[1] else F(0)
            minimum=literal(p,c,o,anchor(p,c),tau,s)
            expected=a*u-minimum+mu*c
            residual=F(row['a'][str(k)])-expected;assert residual==0
            residuals.append(str(residual));old_column_count+=1
        assert F(row['a']['512'])==s/5
        residuals.append('0');old_column_count+=1
        old_records.append({'old_vertex':v['id'],'tau':list(map(str,tau)),'s':str(s),'old_row':row['name'],'new_domain_membership':True,'all_513_row_residuals':residuals})
    assert old_cost_count==3584 and old_column_count==14364
    oldforms=json.loads((OLD/'state_halfspaces.json').read_text())
    for r in oldforms:
        key=(r['p'],r['c'],r['o'],tuple(r['tail']));c,q=forms[key]
        assert c+sum(x*y for x,y in zip(q[:3],theta))==F(r['constant'])
        assert q==list(map(F,r['e3_e4_e5_s_coefficients']))
    oldf={x['name']:(F(x['constant']),list(map(F,x['coefficients']))) for x in old_domain['facets']}
    for name,c,q in recovered:
        if name.startswith('tau'):
            j=int(name[3]);c-=theta[j-3];oldname='e'+name[3:]
        else:oldname=name
        assert (c+sum(x*y for x,y in zip(q[:3],theta)),q)==oldf[oldname]
    dump('old_slice_literal_checks.json',{'status':'PASS','exact_slice':'tau>=theta*, tau=theta*+e','facet_coefficient_identities':55,'affine_state_coefficient_identities':640,'literal_old_costs_checked':old_cost_count,'old_row_columns_checked':old_column_count,'records':old_records,'not_claimed':'Old vertices need not be vertices of the larger new domain.'})
    menu_count=0
    for p,c in product((0,1),repeat=2):
        for r in product((0,1),repeat=4):
            actions=(p,c)+r
            for menu in product((0,1),repeat=6):
                d=sum(menu);o=int(any(menu))
                for j in (3,4,5,6):
                    den=sum(actions[:j-1])+1+(6-j)
                    avg=sum(F(bit,den) for bit in menu)/6
                    assert avg-F(o,6*den)==F(d-o,6*den)>=0
                menu_count+=1
    assert menu_count==4096
    dump('literal_domain_checks.json',{'status':'PASS','facets_from_true_states':8,'weight_nonnegative_facets':3,'all_facets_irredundant':facet_records,'vertices_reenumerated':28,'all_hidden_forms':128,'state_checks':3584,'all_minima_and_ties':224})
    for key in ('source_sha256','prior_frozen_artifact_sha256'):
        for p,h in guard[key].items():assert sha(REPO/p)==h,p
    result={'status':'PASS','dimension':4,'facets':11,'vertices':28,'affine_hidden_forms':128,'vertex_state_checks':3584,'all_minima_and_ties':224,'c0_nonnegative_coefficient_forms':64,'c1_o1_minus_o0_nonnegative_forms':32,'minimal_cap_necessary_state_forms':3,'new_literal_coefficients':14364,'signed_C_identity_columns':14364,'old_slice_facet_coefficients':55,'old_slice_state_coefficients':640,'old_literal_costs_checked':3584,'old_row_columns_checked':14364,'menu_patterns':4096,'negative_free_equality_multiplier':'-11/20','optimizer_calls':0,'numeric_point_read_or_bound':False,'other_project_code_imported_or_executed':False,'prior_frozen_artifacts_unchanged':175,'exact_family_sha256':sha(OUT/'exact_family.json')}
    dump('literal_checker_output.json',result);print(json.dumps(result))

if __name__=='__main__':main()
