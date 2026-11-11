#!/usr/bin/env python3
"""Independent JSON-only literal ordered-menu check, using true payoffs.

No imports/execution of this package's generator or any other project program.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
from collections import Counter
import hashlib
import json

OUT=Path(__file__).resolve().parent
WS=OUT.parent
REPO=OUT.parents[3]

def read(name): return json.loads((OUT/name).read_text())
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def dump(name,x): (OUT/name).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')

def literal(i,p,t,tails,inner_five,theta,alpha):
    actions=[1]*p+[0]*(i-1-p)+[t]+list(tails)
    total=sum(actions)
    pay=[F(bit,total) if bit else F(0) for bit in actions]
    answer=alpha*pay[i-1]
    Kweight=F(0)
    for j in range(i+1,7):
        w=F(1,2) if j<6 else F(1)
        answer+=w*actions[j-1]
        Kweight+=w
    terminal_mean=sum(F(bit,sum(actions[:5])+1) for bit in inner_five)/5
    answer+=terminal_mean-pay[5]
    for j,w in theta.items():
        true_prefix=sum(actions[:j-1])
        query_mean=sum(F(bit,true_prefix+1+6-j) for bit in inner_five)/5
        answer+=w*(query_mean-pay[j-1])
    return answer,Kweight

def main():
    guard=read('source_manifest.json')
    for g in ('source_sha256','prior_frozen_artifact_sha256'):
        for p,h in guard[g].items(): assert sha(REPO/p)==h,p
    family=read('exact_family.json')
    coords=read('coordinate_contract.json')
    domain=json.loads((WS/'all_source_joint_reweighted_safe/parameter_polytopes.json').read_text())['sources']
    vertex={v['id']:(d['source'],v) for d in domain for v in d['vertices']}
    saved_min={(r['vertex'],r['p'],r['d'],r['t']):r for r in read('conditional_minimum_tables.json')}
    saved_state={(r['vertex'],r['p'],r['d'],r['t'],tuple(r['tail'])):r for r in read('hidden_state_checks.json')}
    saved_f={(r['vertex'],r['p'],r['d']):r for r in read('outer_average_tables.json')}
    saved_G={(r['vertex'],r['p']):r for r in read('union_projection_tables.json')}
    minima={}; Gs={}; fs={}; hidden=0; conditional=0
    for vid,(i,v) in vertex.items():
        alpha=F(v['a']); theta={j:F(w) for j,w in zip(range(i+1,6),v['theta'])}
        s=F(v['s']); assert alpha==25+sum(theta.values())-s
        for p in range(i):
            for d in range(7):
                for t in (0,1):
                    if t>d or 1-t>6-d:
                        assert (vid,p,d,t) not in saved_min
                        continue
                    assert 0<=d-t<=5
                    other_bits=[1]*(d-t)+[0]*(5-d+t)
                    table=[]
                    for tails in product((0,1),repeat=6-i):
                        val,Kweight=literal(i,p,t,tails,other_bits,theta,alpha)
                        assert Kweight==F(7-i,2)
                        table.append((tails,val))
                    least=min(val for _,val in table)
                    key=vid,p,d,t
                    minima[key]=least
                    record=saved_min[key]
                    assert F(record['qbar'])==F(sum(other_bits),5)
                    assert F(record['minimum'])==least
                    assert record['all_attaining_tails']==[list(r) for r,val in table if val==least]
                    conditional+=1
                    for r,val in table:
                        record=saved_state[key+(r,)]
                        assert F(record['cost'])==val and F(record['minimum'])==least
                        assert F(record['residual'])==val-least>=0
                        hidden+=1
                # Explicit weighting by the number of actual outer indices.
                branch_values=([minima[vid,p,d,1]]*d if d else [])+([minima[vid,p,d,0]]*(6-d) if d<6 else [])
                value=sum(branch_values)/6
                assert F(saved_f[vid,p,d]['f'])==value
                fs[vid,p,d]=value
            g=min(fs[vid,p,d] for d in range(1,7))
            assert [d for d in range(1,7) if fs[vid,p,d]==g]==[1]
            assert fs[vid,p,0]==0
            assert F(saved_G[vid,p]['G'])==g
            Gs[vid,p]=g
            # Independent closed form, including the loss from the five-query hats.
            loss=max([F(0)]+[theta[j]+sum(theta[ell]/(5*(7-ell)*(8-ell)) for ell in theta if ell>j)-F(2,5) for j in theta])
            D=p+7-i
            expected=(F(7-i,2)+F(24,D)+F(1,p+1)-s/min(D,5)+sum(w/F(p+7-j) for j,w in theta.items()))/6
            expected-=F(5,6)*loss if p==0 else 0
            assert g==expected
    assert hidden==24192 and conditional==1332 and len(Gs)==111
    # Check the machine-readable continuous formula supplied to the separate cell task.
    contract=read('continuous_G_contract.json')
    assert contract['parameter_rows_convex_not_affine'] is True
    assert contract['67_samples_complete_finite_generator'] is False
    assert contract['parent_domain_manifest_sha256']==sha(WS/'all_source_joint_reweighted_safe/freeze_manifest.json')
    assert contract['parent_domain_sha256']==sha(WS/'all_source_joint_reweighted_safe/parameter_polytopes.json')
    contract_count=0
    for item in contract['sources']:
        i=item['i']; js=list(range(i+1,6))
        assert item['theta_sources']==js and F(item['ci'])==F(7-i,2)
        for form in item['loss_affines']:
            j=form['index']; assert j in js and F(form['constant'])==-F(2,5)
            for h in js:
                expected=F(1) if h==j else F(1,5*(7-h)*(8-h)) if h>j else F(0)
                assert F(form['theta_coefficients'][str(h)])==expected
        for vid,(source,v) in vertex.items():
            if source!=i: continue
            theta={j:F(w) for j,w in zip(js,v['theta'])}; s=F(v['s'])
            loss=max([F(0)]+[F(f['constant'])+sum(F(co)*theta[int(j)] for j,co in f['theta_coefficients'].items()) for f in item['loss_affines']])
            for rec in item['G_by_prefix']:
                pref=rec['p']
                val=F(rec['constant'])+F(rec['s_coefficient'])*s+F(rec['loss_coefficient'])*loss
                val+=sum(F(co)*theta[int(j)] for j,co in rec['theta_coefficients'].items())
                assert val==Gs[vid,pref]
                contract_count+=1
    assert contract_count==111
    # All 64 menus and every excluded outer index; explicit inner five shares.
    query_ident=0
    for menu in product((0,1),repeat=6):
        for outer in range(6):
            for denominator in range(1,7):
                inner=sum(F(menu[j],denominator) for j in range(6) if j!=outer)/5
                assert inner==F(sum(menu)-menu[outer],5*denominator)
                query_ident+=1
    menu_count=0
    for r in read('all_64_menu_checks.json'):
        vid,p,menu=r['vertex'],r['p'],r['menu']; d=sum(menu)
        branch=[minima[vid,p,d,bit] for bit in menu]
        assert r['outer_branch_minima']==list(map(str,branch))
        assert r['inner_qbar_by_outer_index']==[str(sum(F(menu[j]) for j in range(6) if j!=k)/5) for k in range(6)]
        value=sum(branch)/6
        assert value==F(r['outer_mean'])==fs[vid,p,d]
        assert F(r['residual'])==value-int(d>0)*Gs[vid,p]>=0
        menu_count+=1
    assert menu_count==7104 and query_ident==2304
    atoms=[]
    for k in range(512):
        bits=tuple((k>>(8-j))&1 for j in range(9))
        atom=coords['atom_columns'][k]
        assert tuple(atom['a'])+(atom['x'],atom['o'],atom['c'])==bits
        assert atom['old_index']==k//2 and atom['index']==k
        atoms.append(bits)
    rows={r['name']:r for r in family['rows']}
    assert len(rows)==67
    coefficients=0
    for row in rows.values():
        vid=row['parent_vertex_id']; i,v=vertex[vid]; a=F(v['a'])
        assert row['source']==i and F(row['source_IC_weight'])==a
        assert row['inner_excludes_same_index'] is True and row['inner_average_divisor']=='5' and row['outer_average_divisor']=='6'
        assert row['numerical_divisor']=='25' and row['rhs']=='0'
        for k,bits in enumerate(atoms):
            own=F(1,sum(bits[:6])) if bits[i-1] else F(0)
            p=sum(bits[:i-1]); o=bits[7]
            assert F(row['a'][str(k)])==a*own-o*Gs[vid,p]
            coefficients+=1
        assert F(row['a']['512'])==F(7-i,2)==F(row['K_weight'])
        coefficients+=1
    assert coefficients==34371
    # Rebuild the old double-mean30 row independently, then every signed identity.
    old_rows=json.loads((WS/'main_all_source25_family/exact_family.json').read_text())['rows']
    old={i:next(r for r in old_rows if r['source']==i and r['T']==8 and r['Q']==8) for i in range(1,5)}
    comparison=read('P25_double30_comparison.json')
    comparison_columns=0
    for entry in comparison['comparisons']:
        new=rows[entry['new']]; i=new['source']; ci=F(7-i,2)
        direct=[]
        for k,bits in enumerate(atoms):
            p=sum(bits[:i-1]); o=bits[7]; own=F(1,sum(bits[:6])) if bits[i-1] else F(0)
            beta=(ci+F(24,p+7-i)+F(1,p+1))/6
            parent=25*own-o*beta
            assert parent==F(old[i]['a'].get(str(k//2),'0'))
            difference=F(new['a'][str(k)])-parent
            assert difference==F(entry['raw_difference_new_minus_old'][k])
            direct.append(difference)
            for name,reverse in [('old_plus_menu_size_certificate',False),('new_plus_menu_size_certificate_for_old',True)]:
                rec=entry[name]
                factor=F(rec['new_row_multiplier' if reverse else 'old_row_multiplier'])
                cap=F(rec['K_minus_O_over6_multiplier']); rem=F(rec['o_remainders_by_p'][p])
                target=parent if reverse else F(new['a'][str(k)])
                start=F(new['a'][str(k)]) if reverse else parent
                assert target-factor*start-cap*(-F(o,6))-o*rem==0
                comparison_columns+=1
        difference=F(new['a']['512'])-F(old[i]['a']['256'])
        assert difference==F(entry['raw_difference_new_minus_old'][512])==0
        direct.append(difference)
        for name,reverse in [('old_plus_menu_size_certificate',False),('new_plus_menu_size_certificate_for_old',True)]:
            rec=entry[name]
            factor=F(rec['new_row_multiplier' if reverse else 'old_row_multiplier'])
            cap=F(rec['K_minus_O_over6_multiplier'])
            assert ci-factor*ci-cap==0
            expected=cap>=0 and min(map(F,rec['o_remainders_by_p']))>=0
            assert rec['all_payments_nonnegative']==expected
            comparison_columns+=1
        expected='equal' if not any(direct) else 'old_implies_new_by_nonnegative_columns' if min(direct)>=0 else 'new_implies_old_by_nonnegative_columns' if max(direct)<=0 else 'coefficientwise_incomparable'
        assert expected==entry['coefficientwise_comparison']
    assert comparison_columns==67*513*2
    # Positive ROOT270 identities, including all independent K columns.
    roots=read('ROOT270_root39_comparison.json')
    B=F(1767904008200582,16877573861922720); C=F(337340181272013,16877573861922720)
    root_columns=0
    for rec in roots['records']:
        row=rows[rec['row']]
        a=F(rec['ROOT270_normalized_multiplier']); cap=F(rec['K_minus_O_over6_multiplier']); rem=F(rec['O_multiplier'])
        assert a==F(row['source_IC_weight']) and cap==3+a*B
        assert rem==a*C+cap/6-F(row['G_by_prefix_load']['0'])
        assert min(a,cap,rem)>0 and rec['all_payments_nonnegative']
        for k,bits in enumerate(atoms):
            u=F(1,sum(bits[:6])) if bits[0] else F(0); o=bits[7]
            residual=F(row['a'][str(k)])-a*(u-C*o)-cap*(-F(o,6))-rem*o
            assert residual==0==F(rec['all_513_residuals'][k])
            root_columns+=1
        assert F(row['a']['512'])-a*(-B)-cap==0==F(rec['all_513_residuals'][512])
        root_columns+=1
    assert root_columns==39*513
    # Diagnostic witness is verified as a feasible old necessary-cone point only.
    diagnostic=read('frozen1003_diagnostic.json')
    inp=json.loads((WS/'visible_maximum_joint_v2/exact_input.json').read_text())
    cert=json.loads((WS/'visible_maximum_joint_v2_solve/exact_certificate.json').read_text())
    z=list(map(F,cert['primal'])); assert len(z)==513 and min(z)>=0
    nz=[k for k,x in enumerate(z) if x]
    for row in inp['raw_rows']:
        assert sum(F(row['a'].get(str(k),'0'))*z[k] for k in nz)>=F(row.get('rhs','0'))
    for eq in inp['equalities']:
        assert sum(F(eq['a'].get(str(k),'0'))*z[k] for k in nz)==F(eq.get('rhs','0'))
    for rec in diagnostic['new_rows']:
        row=rows[rec['row']]; value=sum(F(row['a'][str(k)])*z[k] for k in nz)
        assert value==F(rec['value']) and (value<0)==rec['negative']
    for g in ('source_sha256','prior_frozen_artifact_sha256'):
        for p,h in guard[g].items(): assert sha(REPO/p)==h,p
    summary={'status':'PASS','literal_hidden_states':hidden,'all_conditional_minima_and_ties':conditional,'outer_f_rows':len(fs),'projected_contexts':len(Gs),'continuous_formula_contract_checks':contract_count,'all64_menu_checks':menu_count,'explicit_inner5_denominator_identities':query_ident,'global_literal_coefficients':coefficients,'P25_signed_comparison_columns':comparison_columns,'ROOT270_positive_identity_columns':root_columns,'root39_positive_certificates':39,'frozen1003_rows_verified':1003,'frozen1003_equalities':2,'frozen1003_negative_new_rows':12,'protected_prior_artifacts':130,'optimizer_calls':0,'other_project_code_imported_or_executed':False,'exact_family_sha256':sha(OUT/'exact_family.json')}
    dump('literal_checker_output.json',summary)
    print(json.dumps(summary))

if __name__=='__main__': main()
