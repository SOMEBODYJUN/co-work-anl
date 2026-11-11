#!/usr/bin/env python3
"""Ordered outer-six / inner-five genuine menus. Exact enumeration; no solver.

No old affine minimum is used to calculate the new hidden-tail minimum.
Only this new package is written. Project programs are never imported.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
from collections import Counter
import hashlib
import json

OUT = Path(__file__).resolve().parent
WS = OUT.parent
REPO = OUT.parents[3]
PARENT = WS / 'all_source_joint_reweighted_safe'
PINS = {
 'archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md': 'cc4a9dadb09e08b072cb63214d2e084db38db219e4100efbccf9b7f497520e88',
 'research/workspaces/six-boss1-20261111/main_all_source25_family/proof.md': 'abe4e15a1d07b97ff230514f82415106267ad317bd94ef34ff0f0a3131f46bd0',
 'research/workspaces/six-boss1-20261111/main_all_source25_family/exact_family.json': '8965ab6534776f0cc9570979128df1e99835e0cc0bf60ce9d4a87b5354d4bec0',
 'research/workspaces/six-boss1-20261111/all_source_joint_reweighted_safe/freeze_manifest.json': '3f08170af4b678688317bdebfd8468a8c62e8a801923b3e86f7612a8873825eb',
 'research/workspaces/six-boss1-20261111/all_source_joint_reweighted_safe/parameter_polytopes.json': '1bb37527940d7765fe4b88d26eacc71198e76d78b25d50454f6080892d7d7841',
 'research/workspaces/six-boss1-20261111/all_source_joint_reweighted_safe/proof.md': '1a72e75cbcfa36d215c5030d1b86426746d068c1afc806894272b5c9aca60f70',
 'research/workspaces/six-boss1-20261111/all_source_joint_reweighted_safe/coordinate_contract.json': '95621205eab550affe69dc148e9cce49176b8d2c74b9207511583096d1b60b32',
 'research/workspaces/six-boss1-20261111/maximal_root_tail_wallet_v3/proof.md': 'f5d47adde14fd247eeb55a4d1afa282400030ff361966e47c62deeabd1810851',
 'research/workspaces/six-boss1-20261111/visible_maximum_joint_v2/exact_input.json': '0d80f56ac0b1f82350ae5e307370d9860b21382c7059b688904230a3b80f20a4',
 'research/workspaces/six-boss1-20261111/visible_maximum_joint_v2_solve/exact_certificate.json': 'b9c1d5339b21823b5f448f8c8242bf8b1394b181c099c2bf7d87c68d3f227aea',
}

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def dump(name, obj):
    (OUT/name).write_text(json.dumps(obj, ensure_ascii=False, indent=2)+'\n')

def read(path):
    return json.loads(path.read_text())

def guard_sources():
    for p,h in PINS.items(): assert sha(REPO/p)==h,p
    parent = read(PARENT/'freeze_manifest.json')
    keep = dict(parent['prior_frozen_artifact_sha256'])
    keep.update({p:a['sha256'] for p,a in parent['artifacts'].items()})
    for f in ('freeze_manifest.json','SHA256SUMS'):
        path=PARENT/f
        keep[str(path.relative_to(REPO))]=sha(path)
    assert len(keep)==130
    for p,h in keep.items(): assert sha(REPO/p)==h,p
    dump('source_manifest.json',{'source_sha256':PINS,'prior_frozen_artifact_sha256':keep,'optimizer_calls':0,'other_project_programs_imported_or_executed':False})
    return keep

def cost(i,p,t,q,r,theta,a):
    L=p+t+sum(r)
    numerator=a*t-r[-1]-sum(w*bit for w,bit in zip(theta,r[:-1]))
    assert L or numerator==0
    ans=numerator/L if L else F(0)
    ans+=F(sum(r[:-1]),2)+r[-1]
    ans+=q/(p+t+sum(r[:-1])+1)
    for k,j in enumerate(range(i+1,6)):
        ans+=theta[k]*q/(p+t+sum(r[:k])+7-j)
    return ans

def physical_pairs():
    for d in range(7):
        for t in (0,1):
            if (d==0 and t==1) or (d==6 and t==0): continue
            yield d,t,F(d-t,5)

def main():
    protected=guard_sources()
    domains=read(PARENT/'parameter_polytopes.json')['sources']
    columns=read(PARENT/'coordinate_contract.json')
    minima,states,averages,projections,menus,hat_records=[],[],[],[],[],[]
    lookup={}
    projected={}
    vertices={}
    closed_formula_checks=0
    state_counts=Counter()
    for domain in domains:
        i=domain['source']; n=6-i; ci=F(n+1,2)
        for v in domain['vertices']:
            vid=v['id']; theta=list(map(F,v['theta'])); a=F(v['a']); s=F(v['s'])
            assert a==25+sum(theta)-s and a>0 and all(F(0)<=w<=F(5,12) for w in theta)
            vertices[vid]=(i,theta,a,s)
            ell=[theta[k]+sum(theta[h]/(5*(7-(i+1+h))*(8-(i+1+h))) for h in range(k+1,len(theta)))-F(2,5) for k in range(len(theta))]
            loss=max([F(0)]+ell)
            hat_records.append({'vertex':vid,'source':i,'ell_by_internal_source':{str(j):str(x) for j,x in zip(range(i+1,6),ell)},'L':str(loss),'zero_tail_anchor_valid_at_p0_q1_over5':loss==0})
            for p in range(i):
                local={}
                for d,t,q in physical_pairs():
                    table=[(r,cost(i,p,t,q,r,theta,a)) for r in product((0,1),repeat=n)]
                    m=min(x[1] for x in table)
                    key=(vid,p,d,t); lookup[key]=m; local[d,t]=m
                    minima.append({'vertex':vid,'source':i,'p':p,'d':d,'t':t,'qbar':str(q),'minimum':str(m),'all_attaining_tails':[list(r) for r,z in table if z==m]})
                    for r,z in table:
                        states.append({'vertex':vid,'source':i,'p':p,'d':d,'t':t,'qbar':str(q),'tail':list(r),'cost':str(z),'minimum':str(m),'residual':str(z-m)})
                        state_counts[i]+=1
                ff={}
                for d in range(7):
                    # Do not form either physically impossible absent conditional branch.
                    f=(F(6-d)*local[d,0] if d<6 else F(0))+(F(d)*local[d,1] if d>0 else F(0))
                    ff[d]=f/6
                    averages.append({'vertex':vid,'source':i,'p':p,'d':d,'f':str(ff[d]),'t0_weight':str(F(6-d,6)),'t1_weight':str(F(d,6)),'m0':str(local[d,0]) if d<6 else None,'m1':str(local[d,1]) if d>0 else None})
                g=min(ff[d] for d in range(1,7))
                assert ff[0]==0 and [d for d in range(1,7) if ff[d]==g]==[1]
                projected[vid,p]=g
                D=p+n+1
                m1_expected=ci+F(24,D)-s/min(D,5)
                zero_anchor=F(1,5)*(F(1,p+1)+sum(w/F(p+7-j) for j,w in zip(range(i+1,6),theta)))
                m0_expected=zero_anchor-(loss if p==0 else 0)
                assert local[1,1]==m1_expected and local[1,0]==m0_expected
                expected=(ci+F(24,D)+F(1,p+1)-s/min(D,5)+sum(w/F(p+7-j) for j,w in zip(range(i+1,6),theta)))/6-(F(5,6)*loss if p==0 else 0)
                assert g==expected
                assert m1_expected>=F(227,63) and local[1,0]<=F(221,720)
                for d in range(2,7):
                    assert ff[d]-ff[1]>=F(d-1,6)*(local[1,1]-local[1,0])>=F(d-1)*F(16613,30240)
                projections.append({'vertex':vid,'source':i,'p':p,'G':str(g),'all_attaining_d':[1],'m_t1_q0':str(local[1,1]),'m_t0_q1_over5':str(local[1,0]),'zero_tail_anchor':str(zero_anchor),'loss_L':str(loss),'closed_formula':str(expected),'d2_to6_gaps':[str(ff[d]-g) for d in range(2,7)]})
                closed_formula_checks+=1
                # All 64 menu patterns, retaining the actual excluded index k.
                for bits in product((0,1),repeat=6):
                    d=sum(bits); branch=[]; qbars=[]
                    for k,t in enumerate(bits):
                        inner=[bits[l] for l in range(6) if l!=k]
                        qbar=sum(F(bit) for bit in inner)/5
                        assert qbar==F(d-t,5)
                        qbars.append(str(qbar)); branch.append(lookup[vid,p,d,t])
                    value=sum(branch)/6
                    assert value==ff[d]
                    o=int(any(bits)); residual=value-o*g
                    assert residual>=0
                    menus.append({'vertex':vid,'source':i,'p':p,'menu':list(bits),'d':d,'inner_qbar_by_outer_index':qbars,'outer_branch_minima':list(map(str,branch)),'outer_mean':str(value),'union_projected_cost':str(o*g),'residual':str(residual)})
    assert len(states)==24192 and len(minima)==1332 and len(averages)==777
    assert len(projections)==111 and len(menus)==7104 and closed_formula_checks==111
    assert F(1,5)*(1+F(5,12)*(F(1,5)+F(1,4)+F(1,3)+F(1,2)))==F(221,720)
    assert F(1,5)*(F(1,2)+F(5,12)*(F(1,6)+F(1,5)+F(1,4)+F(1,3)))==F(43,240)
    assert F(227,63)/6-F(221,144)/6==F(695,2016)
    assert (F(227,63)-F(221,720))/6==F(16613,30240)
    dump('hidden_state_checks.json',states)
    dump('conditional_minimum_tables.json',minima)
    dump('outer_average_tables.json',averages)
    dump('union_projection_tables.json',projections)
    dump('all_64_menu_checks.json',menus)
    dump('five_query_hat_analysis.json',hat_records)
    # Full 513-coordinate family, with no C equality or point normalization.
    rows=[]
    for vid,(i,theta,a,s) in vertices.items():
        ci=F(7-i,2); co={}
        for atom in columns['atom_columns']:
            aa=atom['a']; load=sum(aa); ui=F(aa[i-1],load) if load else F(0)
            p=sum(aa[:i-1]); value=a*ui-atom['o']*projected[vid,p]
            co[str(atom['index'])]=str(value)
        co['512']=str(ci)
        rows.append({'name':f'ORDERED_JOINT_MENU_{vid}','family':'ORDERED_OUTER6_INNER5_TRUE_BRANCH_JOINT_MENU','source':i,'parent_vertex_id':vid,'theta_by_source':{str(j):str(w) for j,w in zip(range(i+1,6),theta)},'s':str(s),'source_IC_weight':str(a),'K_weight':str(ci),'G_by_prefix_load':{str(p):str(projected[vid,p]) for p in range(i)},'outer_average_divisor':'6','inner_average_divisor':'5','inner_excludes_same_index':True,'terminal_BR_average_weight':'1','a':co,'rhs':'0','numerical_divisor':'25'})
    assert len(rows)==67
    dump('exact_family.json',{'schema':'all_source_ordered_joint_menu_67x513_v1','status':'GENERATED_NO_SOLVE_NO_POINT_INPUT','rows':rows,'raw_row_count':67,'variables':513,'K_column':512,'bit_order':columns['bit_order'],'inequality_convention':'a dot z >= 0','numerical_positive_divisor':'25','scope':'67 authorized parameter samples of a continuous nonlinear family; not a complete finite generator for that family.','parent_vertex_family_manifest_sha256':sha(PARENT/'freeze_manifest.json'),'optimizer_calls':0})
    dump('coordinate_contract.json',{'bit_order':columns['bit_order'],'atom_columns':columns['atom_columns'],'variables':513,'K_column':512,'normalization_used':False})
    # Exact comparison with the four old P25 double-mean30 rows.
    old_family=read(WS/'main_all_source25_family/exact_family.json')['rows']
    old={i:next(r for r in old_family if r['source']==i and r['T']==8 and r['Q']==8) for i in range(1,5)}
    old_vectors={}
    for i in range(1,5):
        v={}
        for atom in columns['atom_columns']:
            aa=atom['a']; load=sum(aa); p=sum(aa[:i-1]); ci=F(7-i,2)
            beta=ci/6+F(4,p+7-i)+F(1,6*(p+1))
            expected=25*(F(aa[i-1],load) if load else F(0))-atom['o']*beta
            assert expected==F(old[i]['a'].get(str(atom['old_index']),'0'))
            v[str(atom['index'])]=expected
        v['512']=F(old[i]['a']['256'])
        assert v['512']==F(7-i,2)
        old_vectors[i]=v
    comparison=[]
    for row in rows:
        vid=row['parent_vertex_id']; i,theta,a,s=vertices[vid]; ci=F(7-i,2)
        diff=[F(row['a'][str(k)])-old_vectors[i][str(k)] for k in range(513)]
        classification='equal' if not any(diff) else 'old_implies_new_by_nonnegative_columns' if min(diff)>=0 else 'new_implies_old_by_nonnegative_columns' if max(diff)<=0 else 'coefficientwise_incomparable'
        multiplier=a/25; cap_weight=ci*(1-multiplier)
        remainders=[cap_weight/6+multiplier*(ci/6+F(4,p+7-i)+F(1,6*(p+1)))-projected[vid,p] for p in range(i)]
        reverse_multiplier=25/a; reverse_cap_weight=ci*(1-reverse_multiplier)
        reverse_remainders=[reverse_cap_weight/6+reverse_multiplier*projected[vid,p]-(ci/6+F(4,p+7-i)+F(1,6*(p+1))) for p in range(i)]
        comparison.append({'new':row['name'],'old':old[i]['name'],'source':i,'raw_difference_new_minus_old':list(map(str,diff)),'coefficientwise_comparison':classification,'old_plus_menu_size_certificate':{'old_row_multiplier':str(multiplier),'K_minus_O_over6_multiplier':str(cap_weight),'o_remainders_by_p':list(map(str,remainders)),'all_payments_nonnegative':cap_weight>=0 and min(remainders)>=0},'new_plus_menu_size_certificate_for_old':{'new_row_multiplier':str(reverse_multiplier),'K_minus_O_over6_multiplier':str(reverse_cap_weight),'o_remainders_by_p':list(map(str,reverse_remainders)),'all_payments_nonnegative':reverse_cap_weight>=0 and min(reverse_remainders)>=0}})
    dump('P25_double30_comparison.json',{'status':'EXACT_SIGNED_IDENTITIES','old_rows_lifted_and_checked':4,'old_columns_checked':2052,'comparisons':comparison,'raw_classifications':dict(Counter(x['coefficientwise_comparison'] for x in comparison)),'old_plus_size_dominates_count':sum(x['old_plus_menu_size_certificate']['all_payments_nonnegative'] for x in comparison),'new_plus_size_dominates_old_count':sum(x['new_plus_menu_size_certificate_for_old']['all_payments_nonnegative'] for x in comparison),'not_claimed':'Coefficientwise incomparability is not a claim of nonimplication by the full old cone.'})
    # Root39 are tested by an explicit positive identity, not one-point evaluation.
    B=F(1767904008200582,16877573861922720); C=F(337340181272013,16877573861922720)
    root_records=[]
    for row in rows:
        if row['source']!=1: continue
        a=F(row['source_IC_weight']); G=F(row['G_by_prefix_load']['0'])
        cap=3+a*B; remainder=a*C+cap/6-G
        residuals=[]
        for atom in columns['atom_columns']:
            aa=atom['a']; root_share=F(aa[0],sum(aa)) if sum(aa) else F(0); o=atom['o']
            rhs=a*(root_share-C*o)+cap*(-F(o,6))+remainder*o
            residual=F(row['a'][str(atom['index'])])-rhs
            assert residual==0
            residuals.append(str(residual))
        residual=F(row['a']['512'])-(-a*B+cap)
        assert residual==0
        residuals.append(str(residual))
        root_records.append({'row':row['name'],'ROOT270_normalized_multiplier':str(a),'K_minus_O_over6_multiplier':str(cap),'O_multiplier':str(remainder),'all_payments_nonnegative':min(a,cap,remainder)>=0,'all_513_residuals':residuals})
    dump('ROOT270_root39_comparison.json',{'status':'EXACT_IDENTITIES','ROOT270_proof_sha256':PINS['research/workspaces/six-boss1-20261111/maximal_root_tail_wallet_v3/proof.md'],'normalized_ROOT270':{'u1':'1','K':str(-B),'O':str(-C)},'identity':'new = a*(u1-B*K-C*O) + (3+a*B)*(K-O/6) + [a*C+(3+a*B)/6-G]*O','records':root_records,'nonnegative_certificates':sum(x['all_payments_nonnegative'] for x in root_records),'negative_payment_failures':[x['row'] for x in root_records if not x['all_payments_nonnegative']]})
    # Only the explicitly released frozen1003 point is used for diagnostics.
    inp=read(WS/'visible_maximum_joint_v2/exact_input.json')
    certificate=read(WS/'visible_maximum_joint_v2_solve/exact_certificate.json')
    z=list(map(F,certificate['primal'])); support=[j for j,x in enumerate(z) if x]
    assert len(z)==513 and min(z)>=0
    base_slacks=[]
    for row in inp['raw_rows']:
        slack=sum(F(row['a'].get(str(k),'0'))*z[k] for k in support)-F(row.get('rhs','0'))
        assert slack>=0
        base_slacks.append(slack)
    for eq in inp['equalities']:
        assert sum(F(eq['a'].get(str(k),'0'))*z[k] for k in support)==F(eq.get('rhs','0'))
    diagnostics=[]
    for row in rows:
        value=sum(F(row['a'][str(k)])*z[k] for k in support)
        diagnostics.append({'row':row['name'],'value':str(value),'negative':value<0})
    dump('frozen1003_diagnostic.json',{'input_sha256':sha(WS/'visible_maximum_joint_v2/exact_input.json'),'certificate_sha256':sha(WS/'visible_maximum_joint_v2_solve/exact_certificate.json'),'old_primal_rows_checked':len(base_slacks),'old_equalities_checked':len(inp['equalities']),'old_nonnegativity_checked':len(z),'new_rows':diagnostics,'negative_count':sum(x['negative'] for x in diagnostics),'lowest_value':str(min(F(x['value']) for x in diagnostics)),'role':'Diagnostic feasible necessary-cone point only; not an SPE or an input to a new solve.','no_1586_point_bound':True})
    summary={'status':'PASS','samples':67,'prefix_contexts':111,'physical_conditional_minima':len(minima),'hidden_states':len(states),'hidden_states_by_source':dict(state_counts),'outer_average_rows':len(averages),'all64_menu_patterns_per_context':len(menus),'outer_index_checks':6*len(menus),'all_unique_minimum_d':1,'continuous_d1_proof_constant':'16613/30240','closed_G_formula_checks':111,'global_rows':67,'global_columns':513,'global_coefficients':67*513,'old_P25_comparison':dict(Counter(x['coefficientwise_comparison'] for x in comparison)),'root39_nonnegative_certificates':sum(x['all_payments_nonnegative'] for x in root_records),'frozen1003_negative_count':sum(x['negative'] for x in diagnostics),'prior_frozen_artifacts_unchanged':len(protected),'optimizer_calls':0,'other_project_code_executed_or_imported':False,'continuous_family_finitely_generated_by_these67':False}
    dump('derivation_result.json',summary)
    guard_sources()
    print(json.dumps(summary))

if __name__=='__main__':
    main()
