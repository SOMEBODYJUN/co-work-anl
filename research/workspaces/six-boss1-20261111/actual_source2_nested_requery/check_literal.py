#!/usr/bin/env python3
"""JSON-only independent nested-source check; hidden-tail minima and literal indices."""
from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
from pathlib import Path
import json

HERE=Path(__file__).resolve().parent
WS=HERE.parent
ROOT=HERE.parents[3]
BASE=WS/'actual_source2_opt_requery'
def load(path):return json.loads(path.read_text())
def digest(path):return sha256(path.read_bytes()).hexdigest()
def save(name,obj):(HERE/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')

def main():
    assert digest(WS/'main_all_source25_family/proof.md')=='abe4e15a1d07b97ff230514f82415106267ad317bd94ef34ff0f0a3131f46bd0'
    assert digest(WS/'main_all_source25_family/exact_family.json')=='8965ab6534776f0cc9570979128df1e99835e0cc0bf60ce9d4a87b5354d4bec0'
    source_hashes=load(HERE/'frozen_sources_before.json')['file_sha256']
    assert all(digest(ROOT/p)==h for p,h in source_hashes.items())
    catalogue=load(HERE/'row_catalogue.json');rows=catalogue['rows']
    base_catalogue=load(BASE/'row_catalogue.json')
    assert len(rows)==751 and rows[:243]==base_catalogue['rows']
    assert [r['index'] for r in rows]==list(range(751))
    assert len({r['name'] for r in rows})==751
    queries=[f'A{i}' for i in range(1,7)]+['X','Q','R3','R4','R5','R6','Omean']
    appended=rows[243:750]
    assert len(appended)==507
    assert {(r['source'],*r['queries']) for r in appended}=={
        (i,t,q) for i in (3,4,5) for t in queries for q in queries}
    assert all(r['family']=='NESTED_SOURCE25' and r['source'] in (3,4,5) for r in appended)
    assert all(r['rhs']=={'K':str(F(7-r['source'],2))} and r['remaining_inner_tail_count']==6-r['source'] for r in appended)
    assert all(r['true_prefix']==['A1','Q','R3','R4'][:r['source']-1] for r in appended)
    assert all(r['emitted_coefficients']=='unscaled' and r['suggested_positive_numerical_divisor']=='25' for r in appended)
    assert all(r['inner_size_cap_weights']=={'middle_each':'1/2','terminal':'1'} for r in appended)
    kind_counts=dict(Counter(r['inner_averaging'] for r in appended))
    assert kind_counts=={'pure_same_outer_index':432,'pureT_meanQ_inner6':36,
        'meanT_pureQ_inner6':36,'mean_mean_inner30':3}
    c30row=rows[750]
    assert c30row['family']=='NESTED_C30' and c30row['rhs']=={}
    assert c30row['h_bits']==['a1','q','r3','r4','r5','r6','o']
    assert c30row['true_history']==['A1','Q'] and c30row['source_payoffs']==[3,4,6]
    assert c30row['suggested_positive_numerical_divisor']=='126000'

    # Rebuild m from actual hidden-share sums, before using any closed form.
    minima={};hidden_states=[];parent_dominance_checks=0
    for i in (3,4,5):
        n=6-i
        for p in range(i):
            for t,q in product((0,1),repeat=2):
                candidates=[]
                for hidden in product((0,1),repeat=n):
                    total=p+t+sum(hidden)
                    source_share=F(t,total) if total else F(0)
                    last_share=F(hidden[-1],total) if total else F(0)
                    query_share=F(q,p+t+sum(hidden[:-1])+1)
                    value=25*source_share+F(sum(hidden[:-1]),2)+hidden[-1]-last_share+query_share
                    candidates.append(value)
                    hidden_states.append((i,p,t,q,hidden,value))
                m=min(candidates)
                assert m==F(n+1,2)*t+F(24*t,p+n+1)+F(q,p+1+n*t)
                old31=n*t+F(30*t,p+n+1)+F(q,p+1+n*t)
                assert old31-m==F(n-1,2)*t+F(6*t,p+n+1)
                parent_dominance_checks+=1
                minima[i,p,t,q]=m
                assert all(v>=m for v in candidates)
    assert len(hidden_states)==200 and len(minima)==48

    # Explicit six/30 index averages; no product of artificial marginals.
    menu_checks=0;single_checks=0
    for i in (3,4,5):
        n=6-i
        for p in range(i):
            A=F(n+1,2)+F(24,p+n+1);B=F(1,p+1);C=F(n,(p+1)*(p+n+1))
            for menu in product((0,1),repeat=6):
                d=sum(menu);o=int(d>0)
                exact=sum((minima[i,p,menu[k],menu[l]] for k in range(6) for l in range(6) if k!=l),F(0))/30
                weak_menu=[o,0,0,0,0,0]
                weak=sum((minima[i,p,weak_menu[k],weak_menu[l]] for k in range(6) for l in range(6) if k!=l),F(0))/30
                assert exact==F(d,6)*(A+B)-C*F(d*(d-1),30)
                assert weak==F(o,6)*(A+B) and exact>=weak
                menu_checks+=1
                for bit in (0,1):
                    pure_mean=sum((minima[i,p,bit,v] for v in menu),F(0))/6
                    mean_pure=sum((minima[i,p,v,bit] for v in menu),F(0))/6
                    weak_pure_mean=sum((minima[i,p,bit,v] for v in weak_menu),F(0))/6
                    weak_mean_pure=sum((minima[i,p,v,bit] for v in weak_menu),F(0))/6
                    assert weak_pure_mean==A*bit+F(o,6)*(B-C*bit)<=pure_mean
                    assert weak_mean_pure==B*bit+F(o,6)*(A-C*bit)<=mean_pure
                    single_checks+=2
    assert menu_checks==768 and single_checks==3072

    c30path=WS/'main_thirty_index_strengthening/requery30_envelopes.json'
    assert digest(c30path)=='14ef732b35d0f859113daf92c8dda1f08330413682b057c69a57543a41a360bc'
    c30=load(c30path)
    assert len(c30)==128
    for h,entry in enumerate(c30):
        bits=list(map(int,format(h,'07b')));profile=bits[:6];total=sum(profile)
        assert entry['h']==h and entry['bits']==bits
        wallet=F(126000*profile[2]+65719*profile[3]+4962*profile[5],total) if total else F(0)
        assert F(entry['cut'])==wallet-F(entry['m30'])

    def memberships(label,state):
        if label=='Omean':return [state['atom']['o'],0,0,0,0,0]
        if label=='Q':return [state['q']]
        if label=='X':return [state['atom']['x']]
        if label in [f'A{i}' for i in range(1,7)]:return [state['atom']['a'][int(label[1:])-1]]
        return [state['tail'][int(label[1:])-3]]
    def literal_new(row,state):
        profile=[state['atom']['a'][0],state['q']]+state['tail'];total=sum(profile)
        if row['family']=='NESTED_C30':
            bits=profile+[state['atom']['o']];h=sum(bit*(2**(6-j)) for j,bit in enumerate(bits))
            wallet=F(126000*profile[2]+65719*profile[3]+4962*profile[5],total) if total else F(0)
            return F(c30[h]['m30'])-wallet,F(0),F(0)
        i=row['source'];n=6-i;p=sum(profile[:i-1])
        T,Q=row['queries'];left=memberships(T,state);right=memberships(Q,state)
        if T==Q=='Omean':
            costs=[minima[i,p,left[k],left[l]] for k in range(6) for l in range(6) if k!=l]
        else:costs=[minima[i,p,t,q] for t in left for q in right]
        cost=sum(costs,F(0))/len(costs)
        wallet=F(profile[i-1],total) if total else F(0)
        return cost-25*wallet,F(0),F(n+1,2)

    samples=load(HERE/'literal_samples.json')['states']
    old_samples=load(BASE/'literal_samples.json')['states']
    assert len(samples)==len(old_samples)==12
    new_row_evaluations=0;inherited_row_evaluations=0;c30_sample_evaluations=0
    for state,old in zip(samples,old_samples):
        assert {k:state[k] for k in ['id','atom','q','tail']}=={k:old[k] for k in ['id','atom','q','tail']}
        assert len(state['coefficients'])==751
        assert state['coefficients'][:243]==old['coefficients'];inherited_row_evaluations+=243
        for row,out in zip(rows[243:],state['coefficients'][243:]):
            assert out['row']==row['name']
            wanted=literal_new(row,state)
            assert wanted==tuple(F(out[k]) for k in ['A','b_atom','b_K']),(state['id'],row['name'])
            new_row_evaluations+=1
            c30_sample_evaluations+=row['family']=='NESTED_C30'
    assert new_row_evaluations==6096 and inherited_row_evaluations==2916 and c30_sample_evaluations==12
    template=load(HERE/'symbolic_template.json');release=load(HERE/'main_point_release_template.json')
    assert template['dimensions_at_positive_support_s']=={
        'nonnegative_columns':'32*s','mass_equations':'s','q_moment_inequalities':'2*s',
        'genuine_inequalities':751,'raw_inequalities':'751+2*s'}
    assert template['optimizer_calls']==0 and template['matrix_constructed'] is False
    assert template['numerically_scaled_rows_created'] is False
    assert all(template[k] is None for k in ['fixed_input','fixed_matrix','fixed_rhs','full8192_matrix','certificate','projection_weights'])
    fields=['point_version','exact_input_path','exact_input_sha256','primal_certificate_path',
        'primal_certificate_sha256','baseline_row_catalogue_path','baseline_row_catalogue_sha256',
        'baseline_old36_actual_RC_version','baseline_Omean_Omean_averaging','common_X_semantics',
        'K','O','all256_masses','positive_support','positive_support_size','phase_I_authorization']
    assert all(release[k] is None for k in fields)
    assert not (HERE/'exact_input.json').exists() and not (HERE/'exact_certificate.json').exists()
    changed=[p for p,h in source_hashes.items() if digest(ROOT/p)!=h]
    assert not changed
    checked_files=['derivation.md','symbolic_coefficients.py','row_catalogue.json',
        'audit_interface.json','symbolic_template.json','main_point_release_template.json',
        'literal_samples.json','source_bindings.json','frozen_sources_before.json']
    result={
        'status':'PASS_SYMBOLIC751_UNBOUND_TRUE_INTERNAL_P25_AND_C30',
        'genuine_rows':751,'inherited_rows_identical':243,'nested_source25_rows':507,
        'nested_C30_rows':1,'nested_source25_averaging_counts':kind_counts,
        'hidden_inner_tail_states':200,'exact_source25_minima':48,
        'P31_weaker_parent_pure_cost_comparisons':parent_dominance_checks,
        'distinct30_menu_checks':menu_checks,'single_inner6_checks':single_checks,
        'all128_C30_wallet_sign_checks':128,
        'static_sample_states':12,'new_static_row_evaluations':new_row_evaluations,
        'inherited_static_row_evaluations_matched':inherited_row_evaluations,
        'total_sample_fraction_entries':3*(new_row_evaluations+inherited_row_evaluations),
        'point_bound':False,'matrix_constructed':False,'optimizer_calls':0,
        'full8192_verification':False,'read_only_frozen_sources_checked':len(source_hashes),
        'changed_old_files':changed,
        'verification_limit':'Exact generic sources, all128 C30 wallet signs and twelve boundary states; no fixed point, LP or all8192 certificate.',
        'file_sha256':{n:digest(HERE/n) for n in checked_files}}
    save('literal_symbolic_check.json',result)
    print(json.dumps({k:v for k,v in result.items() if k!='file_sha256'},indent=2))

if __name__=='__main__':main()
