#!/usr/bin/env python3
"""Independent true-budget and facet/column replay; no project-code imports."""
from fractions import Fraction as F
from itertools import product,combinations
from pathlib import Path
import hashlib,json

OUT=Path(__file__).resolve().parent
REPO=OUT.parents[3]
BASE=(F(12425,31104),F(175,432),F(5,12))

def read(name):return json.loads((OUT/name).read_text())
def dump(name,x):(OUT/name).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def payments(e,s):
    # Add each SAFE increment's cap charges explicitly to each preceding source.
    cap={3:F(1,2),4:F(1,2),5:F(1,2),6:F(1)}
    for source,increment in zip((3,4,5),e):
        cap[source]+=increment
        for earlier in range(3,source):
            cap[earlier]+=increment/F(6*(7-source)*(8-source))
    safe={j:BASE[j-3]+e[j-3] for j in (3,4,5)}
    alpha=F(25)+sum(BASE)-s+sum(e)
    return alpha,cap,safe

def wallet(p,c,o,r,e,s):
    alpha,cap,safe=payments(e,s)
    actions=(p,c)+tuple(r)
    load=sum(actions)
    shares=[F(bit,load) if bit else F(0) for bit in actions]
    answer=alpha*shares[1]
    for j,w in cap.items():answer+=w*actions[j-1]
    menu=(o,0,0,0,0,0)
    terminal=sum(F(bit,sum(actions[:5])+1) for bit in menu)/6
    answer+=terminal-shares[5]
    for j,w in safe.items():
        query=sum(F(bit,sum(actions[:j-1])+1+6-j) for bit in menu)/6
        answer+=w*(query-shares[j-1])
    return answer

def anchor(p,c):return (0,0,0,0) if not c else (1,1,1,0) if p else (1,1,1,1)

def residual_polynomial(state):
    p,c,o,r=state
    v0=[F(0)]*4
    def residual(v):return wallet(p,c,o,r,v[:3],v[3])-wallet(p,c,o,anchor(p,c),v[:3],v[3])
    constant=residual(v0)
    co=[]
    for k in range(4):co.append(residual([F(j==k) for j in range(4)])-constant)
    return constant,co

def rank(rows):
    basis={}
    for rr in rows:
        v=list(rr)
        for j in sorted(basis):
            q=v[j]
            if q:v=[a-q*b for a,b in zip(v,basis[j])]
        j=next((j for j,x in enumerate(v) if x),None)
        if j is not None:
            q=v[j];basis[j]=[x/q for x in v]
    return len(basis)

def intersect(selected):
    mat=[q[:]+[-c] for name,c,q in selected]
    for col in range(4):
        pivot=next((r for r in range(col,4) if mat[r][col]),None)
        if pivot is None:return None
        mat[col],mat[pivot]=mat[pivot],mat[col]
        factor=mat[col][col];mat[col]=[x/factor for x in mat[col]]
        for r in range(4):
            if r!=col:
                factor=mat[r][col];mat[r]=[x-factor*y for x,y in zip(mat[r],mat[col])]
    return tuple(mat[j][-1] for j in range(4))

def main():
    guard=read('source_manifest.json')
    for key in ('source_sha256','prior_frozen_artifact_sha256'):
        for p,h in guard[key].items():assert sha(REPO/p)==h,p
    domain=read('parameter_polytope.json')
    assert list(map(F,domain['theta_star']))==list(BASE)
    saved_half={x['state']:x for x in read('state_halfspaces.json')}
    polys={}
    for p,c,o in product((0,1),repeat=3):
        for r in product((0,1),repeat=4):
            key=f'p{p}_c{c}_o{o}_r'+''.join(map(str,r))
            constant,co=residual_polynomial((p,c,o,r));polys[key]=(constant,co)
            saved=saved_half[key]
            assert F(saved['constant'])==constant and list(map(F,saved['e3_e4_e5_s_coefficients']))==co
    # Derive the nontrivial facets from real hidden-state residuals, rather than
    # copying their display coefficients from the generator.
    recovered=[]
    for k,j in enumerate((3,4,5)):
        co=[F(0)]*4;co[k]=F(1);recovered.append((f'e{j}_nonnegative',F(0),co))
    for name,key,factor in [('s_nonnegative','p1_c1_o0_r1111',F(30)),('s_at_most9','p0_c1_o0_r1110',F(20))]:
        c,q=polys[key];recovered.append((name,factor*c,[factor*x for x in q]))
    for k,j in enumerate((3,4,5)):
        tail=''.join(str(int(h!=k)) for h in range(3))+'1'
        c,q=polys[f'p1_c1_o0_r{tail}'];recovered.append((f'p1_missing_middle{j}',c,q))
        c,q=polys[f'p0_c1_o0_r{tail}'];recovered.append((f'p0_missing_middle{j}_mixed_s',c,q))
    stored={f['name']:(F(f['constant']),list(map(F,f['coefficients']))) for f in domain['facets']}
    assert {name:(c,q) for name,c,q in recovered}==stored
    found=set()
    for pick in combinations(recovered,4):
        point=intersect(pick)
        if point is not None and all(c+sum(x*y for x,y in zip(q,point))>=0 for name,c,q in recovered):found.add(point)
    listed={tuple(map(F,v['e3_e4_e5']+[v['s']])) for v in domain['vertices']}
    assert found==listed and len(found)==28
    facet_ranks=[]
    for name,c,q in recovered:
        on=[p for p in found if c+sum(x*y for x,y in zip(q,p))==0]
        affine_rank=rank([[x-y for x,y in zip(p,on[0])] for p in on[1:]])
        assert affine_rank==3,(name,affine_rank)
        facet_ranks.append({'facet':name,'affine_dimension':affine_rank,'vertices_on_facet':len(on)})
    saved_states={(x['vertex'],x['state']):x for x in read('hidden_state_checks.json')}
    saved_min={(x['vertex'],x['p'],x['c'],x['o']):x for x in read('minimum_tables.json')}
    minima={};weights={};state_count=0
    for v in domain['vertices']:
        vid=v['id'];e=list(map(F,v['e3_e4_e5']));s=F(v['s'])
        a,caps,safe=payments(e,s);tailK=sum(caps.values());mu=tailK-s/5
        assert a==F(v['source_IC_weight']) and tailK==F(v['true_tail_K_weight']) and mu==F(v['C_size_free_multiplier'])
        assert a>0 and min(caps.values())>0 and min(safe.values())>0
        weights[vid]=(a,caps,safe,mu,s)
        for p,c,o in product((0,1),repeat=3):
            values=[(r,wallet(p,c,o,r,e,s)) for r in product((0,1),repeat=4)]
            minimum=min(x for r,x in values)
            assert wallet(p,c,o,anchor(p,c),e,s)==minimum
            minima[vid,p,c,o]=minimum
            rec=saved_min[vid,p,c,o]
            assert F(rec['minimum'])==minimum
            assert rec['all_attaining_tails']==[list(r) for r,value in values if value==minimum]
            for r,value in values:
                sid=f'p{p}_c{c}_o{o}_r'+''.join(map(str,r))
                rec=saved_states[vid,sid]
                assert F(rec['cost'])==value and F(rec['target'])==minimum
                assert F(rec['residual'])==value-minimum>=0
                state_count+=1
    assert state_count==3584 and len(minima)==224
    family=read('exact_family.json');coord=read('coordinate_contract.json')
    assert len(family['rows'])==28 and family['complete_finite_generator_for_specified_affine_domain']
    identities=[];columns=0
    for row in family['rows']:
        a,caps,safe,mu,s=weights[row['vertex_id']]
        assert F(row['source_IC_weight'])==a
        assert list(map(F,row['middle_CAP_weights']))==[caps[j] for j in (3,4,5)]
        assert list(map(F,row['theta3_theta4_theta5']))==[safe[j] for j in (3,4,5)]
        assert F(row['C_size_free_multiplier'])==mu and row['C_size_equality']=='|C|-K=0'
        assert row['numerical_divisor']=='25' and row['rhs']=='0'
        residuals=[]
        for k in range(512):
            bits=tuple((k>>(8-j))&1 for j in range(9))
            atom=coord['atom_columns'][k]
            assert tuple(atom['a'])+(atom['x'],atom['o'],atom['c'])==bits
            actual_income=F(1,sum(bits[:6])) if bits[1] else F(0)
            # Raw true budget minus literal minimum, then signed C-size equality.
            raw_atom=a*actual_income-minima[row['vertex_id'],bits[0],bits[8],bits[7]]
            expected=raw_atom+mu*bits[8]
            residual=F(row['a'][str(k)])-expected
            assert residual==0
            residuals.append(str(residual));columns+=1
        rawK=sum(caps.values());expectedK=rawK-mu
        assert expectedK==s/5
        residual=F(row['a']['512'])-expectedK
        assert residual==0
        residuals.append(str(residual));columns+=1
        identities.append({'row':row['name'],'true_tail_K_payment':str(rawK),'C_size_free_multiplier':str(mu),'final_K_coefficient':str(expectedK),'all_513_residuals':residuals})
    assert columns==14364
    # Quantitative bridge to the two already frozen base wallets, without any
    # numerical point or assumption that their slacks vanish.
    old_path=OUT.parent/'source2_joint_internal_safe/sixteen_reweighted_vertex_family.json'
    old=json.loads(old_path.read_text())
    base_rows={F(r['s']):r for r in old if list(map(F,r['theta3_theta4_theta5']))==list(BASE)}
    assert set(base_rows)=={F(0),F(9)}
    bridge=[]
    for row in family['rows']:
        e=list(map(F,row['e3_e4_e5']));s=F(row['s']);residuals=[]
        for k in range(512):
            bits=tuple((k>>(8-j))&1 for j in range(9))
            u=F(1,sum(bits[:6])) if bits[1] else F(0)
            p,c,o=bits[0],bits[8],bits[7]
            base=(1-s/9)*F(base_rows[F(0)]['a'].get(str(k),'0'))+(s/9)*F(base_rows[F(9)]['a'].get(str(k),'0'))
            extra=sum(w*(u-F(o,6*(p+(j-2)*c+7-j))) for j,w in zip((3,4,5),e))
            residual=F(row['a'][str(k)])-base-extra
            assert residual==0
            residuals.append(str(residual))
        baseK=(1-s/9)*F(base_rows[F(0)]['a']['512'])+(s/9)*F(base_rows[F(9)]['a']['512'])
        assert F(row['a']['512'])==baseK
        residuals.append('0')
        bridge.append({'row':row['name'],'base_s0':base_rows[F(0)]['name'],'base_s9':base_rows[F(9)]['name'],'base_weights':[str(1-s/9),str(s/9)],'e3_e4_e5':row['e3_e4_e5'],'all_513_residuals':residuals})
    dump('base_wallet_comparison.json',{'status':'PASS','identity':'new = (1-s/9)*base_s0 + (s/9)*base_s9 + sum_j e_j*(u2-Nj)','base_family_sha256':sha(old_path),'records':bridge,'columns_checked':14364,'interpretation':'Signed algebraic comparison only; individual u2-Nj terms are not asserted nonnegative.'})
    # Explicit six-index menu identities for every actual hidden prefix.
    menu_checks=0
    for p,c in product((0,1),repeat=2):
        for r in product((0,1),repeat=4):
            actions=(p,c)+r
            for menu in product((0,1),repeat=6):
                d=sum(menu);o=int(any(menu))
                denominators=[sum(actions[:5])+1]+[sum(actions[:j-1])+1+6-j for j in (3,4,5)]
                for den in denominators:
                    exact=sum(F(bit,den) for bit in menu)/6
                    assert exact-F(o,6*den)==F(d-o,6*den)>=0
                menu_checks+=1
    assert menu_checks==4096
    # Preserve the failure rather than silently strengthening the original guess.
    e=(F(0),F(0),F(23,48));state=(0,1,0,(1,1,0,1))
    bad=wallet(*state,e,F(9))-wallet(0,1,0,anchor(0,1),e,F(9))
    assert bad==-F(1,192)
    assert all(c+sum(x*y for x,y in zip(q,e+(F(0),)))>=0 for name,c,q in recovered)
    rejection=read('rejected_product_candidate.json')
    assert rejection['simple_nonproduct_witness']['s9_residual']==str(bad)
    for case in rejection['negative_hidden_states']:
        constant,co=polys[case['state']]
        v=list(map(F,case['e']+[case['s']]))
        value=constant+sum(x*y for x,y in zip(co,v))
        assert value==F(case['residual'])<0
    dump('literal_free_equality_checks.json',{'status':'PASS','identity':'final row = true budget sum + menu weakening + hidden residuals + mu*(|C|-K)','records':identities,'all_columns_checked':columns})
    dump('literal_domain_checks.json',{'status':'PASS','facets_rederived_from_true_budget_states':8,'weight_nonnegative_facets':3,'vertices_independently_reenumerated':28,'all_facets_irredundant':facet_ranks,'residual_polynomials_reconstructed':128,'vertex_state_checks':state_count,'minima_and_all_ties':224,'nonproduct_simple_failure':str(bad)})
    for key in ('source_sha256','prior_frozen_artifact_sha256'):
        for p,h in guard[key].items():assert sha(REPO/p)==h,p
    result={'status':'PASS','full_dimension':4,'true_facets':11,'complete_vertices':28,'affine_hidden_forms':128,'vertex_hidden_states':3584,'all_minimum_and_tie_tables':224,'all_literal_coefficients':14364,'all_free_C_equality_identity_columns':14364,'base_wallet_signed_identity_columns':14364,'six_index_menu_patterns':4096,'rejected_product_negative_states':12,'no_point_read_or_bound':True,'optimizer_calls':0,'other_project_code_imported_or_executed':False,'prior_frozen_artifacts_unchanged':153,'exact_family_sha256':sha(OUT/'exact_family.json')}
    dump('literal_checker_output.json',result);print(json.dumps(result))

if __name__=='__main__':main()
