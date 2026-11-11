#!/usr/bin/env python3
"""Independent audit of SYMBOLIC751 P25+C30, without executing any producer.

Literal customer shares generate the P25 minima. Explicit six/30-index sums
generate the menu costs. The 507 added P25 contracts and the C30 map are then
checked over all8192 outer states by streaming, without allocating a matrix.
The producer's stored boundary fixtures are compared separately. No point,
optimizer, Main/builder module, or prior audit program is loaded as code.
"""
from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
WS = HERE.parent
REPO = WS.parents[2]
SRC = WS/'actual_source2_nested_requery'
BASE = WS/'actual_source2_opt_requery'
P25 = WS/'main_all_source25_family'
C30 = WS/'main_thirty_index_strengthening'
ACTUAL = tuple('A%d'%i for i in range(1,7))
TAILS = ('R3','R4','R5','R6')
PURE = ACTUAL+('X','Q')+TAILS
QUERIES = PURE+('Omean',)
PROFILE_ROLES = ('A1','Q','R3','R4','R5','R6')
PINS = {
    'actual_source2_nested_requery/freeze_manifest.json':
        '1090ce67dec8ee30e27014d634d883ad67864a20f94b9bc33e36c94909106d70',
    'actual_source2_nested_requery/row_catalogue.json':
        '028a6de290df6e69213439fb702dd7c3357350e2bc628846a924255d8a6f3cdc',
    'actual_source2_nested_requery/symbolic_coefficients.py':
        '8dfd7b79a7d1d497c890f7164ba6ea119be74121af40135716b818fdfe4d6629',
    'actual_source2_opt_requery/row_catalogue.json':
        '724a117332bdfed603990210daf83b5637828bf0a24cb8fc30b55c1344bd3ee0',
    'actual_source2_opt_requery/symbolic_coefficients.py':
        '3b8a00fa72b2b15678656f7f2f21f18610ab2f1586d850b080a1d61235e4a205',
    'main_all_source25_family/proof.md':
        'abe4e15a1d07b97ff230514f82415106267ad317bd94ef34ff0f0a3131f46bd0',
    'main_all_source25_family/exact_family.json':
        '8965ab6534776f0cc9570979128df1e99835e0cc0bf60ce9d4a87b5354d4bec0',
    'main_all_source25_family/manifest.json':
        '8cebe7796d8c329da25f11a4591d182266a8d69771ffa6c7cf618395ef452015',
    'main_thirty_index_strengthening/requery30_envelopes.json':
        '14ef732b35d0f859113daf92c8dda1f08330413682b057c69a57543a41a360bc',
}


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def load(path):
    return json.loads(path.read_text())


def share(bit, prefix, followers=0):
    assert bit in (0,1) and prefix >= 0 and followers >= 0
    return F(1,prefix+1+followers) if bit else F(0)


def payoff(sequence, index):
    return share(sequence[index],sum(sequence[:index]),sum(sequence[index+1:]))


def p25_hidden_cost(prefix, t, query, tail):
    # 25 source share, half-price intermediate sizes, full-price last size,
    # minus the true last share, plus its queried-action share.
    return (25*share(t,prefix,sum(tail))+F(sum(tail[:-1]),2)+tail[-1]
            -share(tail[-1],prefix+t+sum(tail[:-1]))
            +share(query,prefix+t+sum(tail[:-1])))


def pair_cost(t,q,prefix):
    return share(t,prefix,q)+share(q,prefix)


def pair_wallet(profile):
    prefix=sum(profile[:4]);y,z=profile[4:]
    return (payoff(profile,4)+payoff(profile,5)
            +share(y,prefix)-share(y,prefix,1))


PAIR30={}
for D,o in product(range(1,6),(0,1)):
    menu=(o,0,0,0,0,0)
    PAIR30[D,o]=sum((pair_cost(menu[k],menu[l],D-1)
                     for k in range(6) for l in range(6) if k!=l),F(0))/30
    assert PAIR30[D,o]==F(o,3*D)


def c30_hidden_cost(history, inner):
    """Rebuild the nine paid rows at an arbitrary genuine two-action history."""
    old,o=history[:6],history[6]
    query,r4,r5,r6=inner
    new=old[:2]+(query,r4,r5,r6)
    value=126000*payoff(new,2)
    for bit,weight in zip((r4,r5,r6),(43,31218,34458)):
        value+=weight*share(bit,sum(old[:3]),2)
    for bit in (r4,r5,r6):
        value+=1654*share(bit,sum(old[:5]))
    value+=5400*(share(o,sum(new[:5]))/6-payoff(new,5))
    value+=7740*(PAIR30[1+sum(new[:4]),o]-pair_wallet(new))
    return value


def main():
    for name,want in PINS.items():
        assert digest(WS/name)==want,name
    bindings=load(SRC/'source_bindings.json')
    for key,entry in bindings.items():
        if isinstance(entry,dict) and 'path' in entry:
            assert digest(WS/entry['path'])==entry['sha256'],key
    assert bindings['point_input'] is None and bindings['point_certificate'] is None
    catalog=load(SRC/'row_catalogue.json')
    base_catalog=load(BASE/'row_catalogue.json')
    rows=catalog['rows'];base_rows=base_catalog['rows']
    assert len(rows)==751 and len(base_rows)==243
    assert rows[:243]==base_rows
    # Canonical byte identity includes row order, field names, values and order.
    serialize=lambda value:json.dumps(value,ensure_ascii=False,separators=(',',':')).encode()
    assert serialize(rows[:243])==serialize(base_rows)
    assert tuple(catalog['query_descriptors'])==QUERIES
    assert [r['index'] for r in rows]==list(range(751))
    assert len({r['name'] for r in rows})==751
    added=rows[243:750]
    assert [(r['source'],*r['queries']) for r in added]==[
        (i,t,q) for i in (3,4,5) for t in QUERIES for q in QUERIES]
    averages=Counter()
    for row in added:
        i=row['source'];n=6-i;t,q=row['queries']
        assert row['family']=='NESTED_SOURCE25'
        assert row['name']=='NESTED_SOURCE25_j%d|%s|%s'%(i,t,q)
        assert row['true_prefix']==list(PROFILE_ROLES[:i-1])
        assert row['remaining_inner_tail_count']==n
        assert row['rhs']=={'K':str(F(n+1,2))}
        assert row['suggested_positive_numerical_divisor']=='25'
        assert row['inner_size_cap_weights']=={'middle_each':'1/2','terminal':'1'}
        assert row['emitted_coefficients']=='unscaled'
        assert row['own_Q_extension'] is False
        marker=('mean_mean_inner30' if t==q=='Omean' else
                'meanT_pureQ_inner6' if t=='Omean' else
                'pureT_meanQ_inner6' if q=='Omean' else 'pure_same_outer_index')
        assert row['inner_averaging']==marker
        averages[marker]+=1
    assert averages=={'pure_same_outer_index':432,'pureT_meanQ_inner6':36,
                      'meanT_pureQ_inner6':36,'mean_mean_inner30':3}
    c_row=rows[-1]
    assert c_row['family']=='NESTED_C30' and c_row['index']==750
    assert c_row['name']=='NESTED_C30|A1|Q'
    assert c_row['true_history']==['A1','Q'] and c_row['source_payoffs']==[3,4,6]
    assert c_row['h_bits']==['a1','q','r3','r4','r5','r6','o']
    assert c_row['queries']==[] and c_row['rhs']=={}
    assert c_row['suggested_positive_numerical_divisor']=='126000'
    assert c_row['inner_averaging']=='projected_true_C30_with_inner30'

    # All five source-theorem local domains; only sources3..5 are appended.
    source_family=load(P25/'exact_family.json')
    stated_min={(r['i'],r['p'],r['t'],r['q']):F(r['minimum'])
                for r in source_family['minima']}
    stated_states={(r['i'],r['p'],r['t'],r['q'],tuple(r['tails'])):r
                   for r in load(P25/'literal_states.json')}
    minima={};hidden_checks=local_hidden_checks=0
    for i in range(1,6):
        n=6-i
        for p in range(i):
            for t,q in product((0,1),repeat=2):
                values={tail:p25_hidden_cost(p,t,q,tail)
                        for tail in product((0,1),repeat=n)}
                m=min(values.values());minima[i,p,t,q]=m
                assert m==stated_min[i,p,t,q]
                assert m==F(n+1,2)*t+F(24*t,p+n+1)+F(q,p+1+n*t)
                assert values[(t,)*n]==m
                for tail,value in values.items():
                    declared=stated_states[i,p,t,q,tail]
                    assert F(declared['cost'])==value
                    assert F(declared['residual'])==value-m>=0
                    hidden_checks+=1;local_hidden_checks+=i>=3
    assert hidden_checks==456 and local_hidden_checks==200

    # Query code2 denotes an inner-menu descriptor, not a fractional pure action.
    def literal_cost(i,p,t,q,o):
        menu=(o,0,0,0,0,0)
        if t<2 and q<2:return minima[i,p,t,q]
        if t==2 and q<2:return sum((minima[i,p,b,q] for b in menu),F(0))/6
        if t<2 and q==2:return sum((minima[i,p,t,b] for b in menu),F(0))/6
        return sum((minima[i,p,menu[k],menu[l]] for k in range(6)
                    for l in range(6) if k!=l),F(0))/30

    def declared_cost(i,p,t,q,o):
        # An independently written mathematical transcription of the pinned
        # kernel's documented algebra, compared against literal minimization.
        n=6-i;D=p+n+1
        A=F(n+1,2)+F(24,D);B=F(1,p+1);C=F(n,(p+1)*D)
        if t==q==2:return F(o,6)*(A+B)
        if t==2:return B*q+F(o,6)*(A-C*q)
        if q==2:return A*t+F(o,6)*(B-C*t)
        return A*t+B*q-C*t*q

    local_menu30=local_mixed=0
    for i in (3,4,5):
        n=6-i
        for p in range(i):
            A=F(n+1,2)+F(24,p+n+1);B=F(1,p+1);C=F(n,(p+1)*(p+n+1))
            assert A-C>0 and B-C>0
            for menu in product((0,1),repeat=6):
                d=sum(menu);o=int(d>0)
                for pure in (0,1):
                    costT=sum((minima[i,p,t,pure] for t in menu),F(0))/6
                    costQ=sum((minima[i,p,pure,q] for q in menu),F(0))/6
                    assert costT>=literal_cost(i,p,2,pure,o)
                    assert costQ>=literal_cost(i,p,pure,2,o)
                    assert costT==B*pure+F(d,6)*(A-C*pure)
                    assert costQ==A*pure+F(d,6)*(B-C*pure)
                    local_mixed+=2
                both=sum((minima[i,p,menu[k],menu[l]] for k in range(6)
                          for l in range(6) if k!=l),F(0))/30
                assert both==F(d,6)*(A+B)-F(d*(d-1),30)*C
                assert both>=literal_cost(i,p,2,2,o)
                local_menu30+=1
    assert local_menu30==768 and local_mixed==3072

    # Precompute every local typed cost/payoff contract, including repeated roles.
    profiles=list(product((0,1),repeat=6))
    exact_A={};contract_A={}
    for seq,o,i,t,q in product(profiles,(0,1),(3,4,5),range(3),range(3)):
        p=sum(seq[:i-1])
        literal=literal_cost(i,p,t,q,o)-25*payoff(seq,i-1)
        total=sum(seq)
        direct=declared_cost(i,p,t,q,o)-(F(25*seq[i-1],total) if total else F(0))
        assert literal==direct
        exact_A[seq,o,i,t,q]=literal
        contract_A[seq,o,i,t,q]=direct

    # Independently rebuild the full C30 min table from the nine true budgets.
    table=load(C30/'requery30_envelopes.json')
    assert len(table)==128
    c30_cost={};c30_m={};c30_cut={}
    c30_positive=c30_zero=0
    for h,bits in enumerate(product((0,1),repeat=7)):
        entry=table[h]
        assert entry['h']==h and tuple(entry['bits'])==bits
        am=[]
        for query in (0,1):
            vals=[]
            for tail in product((0,1),repeat=3):
                state=(query,)+tail
                value=c30_hidden_cost(bits,state)
                c30_cost[h,state]=value;vals.append(value)
            am.append(min(vals))
        a0,a1=am;o=bits[6]
        delta=max(a1-a0,F(0));gamma=max(a0-a1,F(0))
        m=a0 if not o else min((5*a0+a1)/6,a1)
        assert m==a0+delta*o/6-gamma*o
        for key,value in [('a0',a0),('a1',a1),('delta',delta),('gamma',gamma),('m30',m)]:
            assert F(entry[key])==value,(h,key)
        wallet=126000*payoff(bits[:6],2)+65719*payoff(bits[:6],3)+4962*payoff(bits[:6],5)
        cut=wallet-m
        assert F(entry['cut'])==cut
        c30_m[bits]=m;c30_cut[bits]=cut
        for state in product((0,1),repeat=4):
            residual=c30_cost[h,state]+(gamma-delta)*state[0]-a0
            assert residual>=0
            c30_positive+=residual>0;c30_zero+=residual==0

    # Stream ALL8192 old-type/new-state combinations, not a fixed-support matrix.
    p25_stream_checks=c30_stream_checks=0
    c30_preimages=Counter()
    prefix_differences=Counter();payoff_differences=Counter()
    q_not_old_a2_detection=0
    # Group the507 rows once; all row-specific provenance has been checked above.
    groups={i:[r for r in added if r['source']==i] for i in (3,4,5)}
    for old,new in product(product((0,1),repeat=8),product((0,1),repeat=5)):
        a=old[:6];x,o=old[6:];outer_q=new[0];tail=new[1:]
        seq=(a[0],outer_q)+tail
        role_values=dict(zip(ACTUAL,a));role_values.update(X=x,Q=outer_q)
        role_values.update(zip(TAILS,tail));role_values['Omean']=2
        for i in (3,4,5):
            p=sum(seq[:i-1])
            assert p==sum(role_values[r] for r in PROFILE_ROLES[:i-1])
            prefix_differences[i]+=p!=sum(a[:i-1])
            payoff_differences[i]+=payoff(seq,i-1)!=payoff(a,i-1)
            for row in groups[i]:
                t,q=(role_values[r] for r in row['queries'])
                value=exact_A[seq,o,i,t,q]
                assert value==contract_A[seq,o,i,t,q]
                p25_stream_checks+=1
        hbits=seq+(o,)
        h=sum(bit*(1<<(6-j)) for j,bit in enumerate(hbits))
        assert table[h]['bits']==list(hbits)
        expanded=c30_m[hbits]-126000*payoff(seq,2)-65719*payoff(seq,3)-4962*payoff(seq,5)
        assert expanded==-c30_cut[hbits]==-F(table[h]['cut'])
        wrong=(a[0],a[1])+tail+(o,)
        q_not_old_a2_detection+=c30_cut[hbits]!=c30_cut[wrong]
        c30_preimages[h]+=1;c30_stream_checks+=1
    assert p25_stream_checks==507*8192
    assert c30_stream_checks==8192 and set(c30_preimages.values())=={64}
    assert len(c30_preimages)==128 and q_not_old_a2_detection>0
    assert all(prefix_differences[i]>0 and payoff_differences[i]>0 for i in (3,4,5))

    # Compare actual serialized fixtures, separately from the symbolic contract.
    samples=load(SRC/'literal_samples.json');base_samples=load(BASE/'literal_samples.json')
    assert samples['state_count']==base_samples['state_count']==12
    assert samples['rows_per_state']==751 and base_samples['rows_per_state']==243
    new_scalar_checks=old_scalar_inheritance=0
    for current,previous in zip(samples['states'],base_samples['states']):
        for key in ('id','atom','q','tail'):assert current[key]==previous[key]
        assert current['coefficients'][:243]==previous['coefficients']
        assert serialize(current['coefficients'][:243])==serialize(previous['coefficients'])
        old_scalar_inheritance+=243*3
        a=tuple(current['atom']['a']);x=current['atom']['x'];o=current['atom']['o']
        q=current['q'];tail=tuple(current['tail']);seq=(a[0],q)+tail
        role_values=dict(zip(ACTUAL,a));role_values.update(X=x,Q=q)
        role_values.update(zip(TAILS,tail));role_values['Omean']=2
        assert len(current['coefficients'])==751
        for row,stored in zip(rows[243:],current['coefficients'][243:]):
            assert stored['row']==row['name']
            if row['family']=='NESTED_SOURCE25':
                i=row['source'];t,q=(role_values[r] for r in row['queries'])
                expected=(exact_A[seq,o,i,t,q],F(0),F(7-i,2))
            else:
                expected=(-c30_cut[seq+(o,)],F(0),F(0))
            assert tuple(F(stored[k]) for k in ('A','b_atom','b_K'))==expected
            new_scalar_checks+=3
    assert new_scalar_checks==18288 and old_scalar_inheritance==8748

    template=load(SRC/'symbolic_template.json')
    release=load(SRC/'main_point_release_template.json')
    interface=load(SRC/'audit_interface.json')
    assert template['optimizer_calls']==0 and template['matrix_constructed'] is False
    assert template['numerically_scaled_rows_created'] is False
    for key in ('fixed_input','fixed_matrix','fixed_rhs','full8192_matrix','certificate','projection_weights'):
        assert template[key] is None
    allowed_nonnull={'status','source_history','required_common_X_semantics',
                     'required_symbolic_catalogue','point_role'}
    for key,value in release.items():
        if key not in allowed_nonnull:assert value is None,(key,value)
    assert template['moment_rows']==load(BASE/'symbolic_template.json')['moment_rows']
    assert interface['point_bound'] is False and interface['optimizer_calls']==0
    assert interface['averaging']['direct_inner30_rows']==4
    assert interface['averaging']['projected_C30_rows_with_inner30_payment']==1
    assert template['dimensions_at_positive_support_s']=={
        'nonnegative_columns':'32*s','mass_equations':'s','q_moment_inequalities':'2*s',
        'genuine_inequalities':751,'raw_inequalities':'751+2*s'}

    # Signed outer-moment elimination is unchanged; keep both possible signs.
    for a0,a1,o in product((F(-7,3),F(-1),F(0),F(2,5),F(11)),
                           (F(-7,3),F(-1),F(0),F(2,5),F(11)),(0,1)):
        delta=max(a1-a0,F(0));gamma=max(a0-a1,F(0))
        m=a0+delta*o/6-gamma*o
        assert m==(a0 if not o else min((5*a0+a1)/6,a1))
        for q in (0,1):
            aq=a1 if q else a0
            assert -aq+(delta-gamma)*q+a0==0
        assert -delta*o/6+gamma*o-a0==-m

    paths=[WS/name for name in PINS]
    paths += [SRC/n for n in ('derivation.md','source_review.md','source_bindings.json',
                              'audit_interface.json','symbolic_template.json',
                              'main_point_release_template.json','literal_samples.json')]
    paths += [BASE/'literal_samples.json',BASE/'symbolic_template.json',
              P25/'literal_states.json',WS/'actual_source2_nested_requery.md',
              C30/'proof.md',C30/'requery30_states.json',
              REPO/'archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md',
              REPO/'archives/customer-attraction/state/引理/共享真实末回复的组合查询投影与同源重配权--引理.md']
    result={
        'status':'PASS_INDEPENDENT_SYMBOLIC751_P25_C30_SOURCES_AND_INTERFACES',
        'genuine_rows':751,'inherited_rows':243,'new_P25_rows':507,'new_C30_rows':1,
        'inherited_catalogue_canonical_bytes_identical':True,
        'inherited_kernel_SHA_guarded_and_read_not_executed':True,
        'all_P25_source_hidden_states':hidden_checks,'all_P25_source_minima':len(minima),
        'appended_source_hidden_states':local_hidden_checks,'appended_source_minima':48,
        'appended_source_literal_inner30_cases':local_menu30,
        'appended_source_literal_single_mean_cases':local_mixed,
        'P25_local_profile_query_contracts':len(exact_A),
        'P25_full_outer_state_contract_evaluations':p25_stream_checks,
        'C30_literal_hidden_states':len(c30_cost),'C30_full_envelopes':128,
        'C30_hidden_residuals_positive':c30_positive,'C30_hidden_residuals_zero':c30_zero,
        'C30_outer_state_maps_and_signs':c30_stream_checks,
        'C30_preimages_per_table_entry':64,
        'total_added_row_state_contract_evaluations':p25_stream_checks+c30_stream_checks,
        'detects_old_a2_instead_of_outer_q_in_states':q_not_old_a2_detection,
        'actual_prefix_differences_by_source':dict(prefix_differences),
        'actual_payoff_differences_by_source':dict(payoff_differences),
        'new_boundary_row_triples':6096,'new_boundary_scalar_checks':new_scalar_checks,
        'inherited_boundary_row_triples':2916,'inherited_boundary_scalar_entries_identical':old_scalar_inheritance,
        'total_boundary_row_triples':9012,'total_boundary_scalar_entries':27036,
        'direct_inner30_descriptor_rows':4,'additional_projected_C30_rows':1,
        'outer_moment_direction_and_free_mass_sign':'PASS',
        'source_sha256':{str(p.relative_to(REPO)):digest(p) for p in paths},
        'scope':'Necessary symbolic layer for the original complete ordered-history six-player pure SPE, any six legal query labels and their union; inherited actual-X budgets keep actual prefix, additions use genuine inner continuations.',
        'full_stream_scope':'All508 added mathematical A contracts were streamed over all8192 states. Literal minima/index sums were compared with an independently written transcription of the pinned kernel algebra; the producer kernel was not executed. No emitted full matrix exists to compare.',
        'point_bound':False,'fixed_or_full_matrix_allocated':False,'optimizer_calls':0,
        'Main_builder_or_prior_audit_code_executed_or_imported':False,
        'not_claimed':['fixed-point feasibility or infeasibility','candidate Farkas or universal projected cut',
                       'full751x8192 producer-matrix replay','complete SPE realization',
                       'v6 or other numerical point audit','new welfare bound or optimality'],
        'outstanding_errors':[],
    }
    (HERE/'audit_result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    keys=('status','genuine_rows','new_P25_rows','new_C30_rows',
          'appended_source_hidden_states','appended_source_minima',
          'P25_full_outer_state_contract_evaluations','C30_outer_state_maps_and_signs',
          'total_added_row_state_contract_evaluations','total_boundary_scalar_entries',
          'outstanding_errors')
    print(json.dumps({k:result[k] for k in keys},indent=2))


if __name__=='__main__':
    main()
