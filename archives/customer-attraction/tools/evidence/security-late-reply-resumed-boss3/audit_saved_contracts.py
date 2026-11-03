"""Standard-library fixed-input checks; no LP, random search, or original main.

The 60-atom result is compared to an already completed independent reconstruction.
Only the previously unaudited saved 61-atom evaluation is recomputed here, using
the four literal pure evaluator functions extracted from the frozen source AST.
"""
from __future__ import annotations
import ast
from collections import Counter
from fractions import Fraction as F
from functools import lru_cache
from itertools import product, combinations, combinations_with_replacement
import hashlib
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
REPO=HERE.parents[4]
OLD='research/workspaces/customer-attraction/R-c4732bee2f7b4e50a70568170e3334ae'
SRC=HERE/'original'/OLD

def read(p): return json.loads(p.read_text())
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def serial(x):
    if isinstance(x,F): return str(x)
    if isinstance(x,dict): return {str(k):serial(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)): return [serial(v) for v in x]
    return x

def complete_ends(actions,k,n):
    expected={h for d in range(n) for h in product(range(k),repeat=d)}
    assert set(actions)==expected and all(a in range(k) for a in actions.values())
    ends={h:h for h in product(range(k),repeat=n)}
    for d in range(n-1,-1,-1):
        for h in product(range(k),repeat=d): ends[h]=ends[h+(actions[h],)]
    return ends

def late_saved():
    d=read(SRC/'round4_search/late2_m5p7_fixed.json');s=d['selected_exact']
    assert sha(SRC/'round4_search/late_reply_family.py')==d['seed_script_sha256']
    k,n=d['topics'],d['players'];items=s['strategy']['actions']
    actions={tuple(i['history']):i['action'] for i in items};assert len(actions)==len(items)
    ends=complete_ends(actions,k,n);weights=s['integer_clones']
    @lru_cache(None)
    def coeff(z,a):
        return tuple(F(1,sum(bool(mask&(1<<b)) for b in z)) if mask&(1<<a) else F(0) for mask in range(1,1<<k))
    def dot(row): return sum((x*w for x,w in zip(row,weights)),F(0))
    constraints=set();allslacks=[]
    for h,a in actions.items():
        actual=coeff(ends[h],a)
        for b in range(k):
            alt=coeff(ends[h+(b,)],b);row=tuple(x-y for x,y in zip(actual,alt))
            slack=dot(row);assert slack>=0;allslacks.append(slack)
            if b!=a and any(row):constraints.add(row)
    rows=sorted(constraints);assert len(rows)==s['rows']
    root=ends[()];counts=[root.count(a) for a in range(k)]
    assert counts==s['root_counts']==s['strategy']['terminal_counts']
    def cover(support): return tuple(F(any(mask&(1<<a) for a in support)) for mask in range(1,1<<k))
    w=cover(set(root));v=cover(s['portfolio']);W=dot(w)
    opt=max(dot(cover(J)) for J in combinations(range(k),min(n,k)))
    assert W==s['W'] and opt==s['OPT'] and opt/W==F(s['ratio_exact'])
    beta=F(s['dual_bound_exact']);support=[(i,F(mu)) for i,mu in s['dual_support']]
    assert len({i for i,_ in support})==len(support) and all(mu>=0 and i in range(len(rows)) for i,mu in support)
    residual=[beta*w[j]-sum((mu*rows[i][j] for i,mu in support),F(0))-v[j] for j in range(len(w))]
    assert min(residual)>=0 and dot(v)/W==beta
    topic_sets=[tuple(mask for mask,z in enumerate(weights,1) if z and mask&(1<<a)) for a in range(k)]
    classes=[]
    for a,t in enumerate(topic_sets):
        hit=next((C for C in classes if topic_sets[C[0]]==t),None)
        if hit is None:classes.append([a])
        else:hit.append(a)
    which={a:i for i,C in enumerate(classes) for a in C};qk=len(classes)
    virtual={():()};quotient={}
    for depth in range(n):
        for h in product(range(qk),repeat=depth):
            vh=virtual[h];prescribed=actions[vh];qc=which[prescribed];quotient[h]=qc
            for c,C in enumerate(classes):virtual[h+(c,)]=vh+((prescribed if c==qc else C[0]),)
    qe=complete_ends(quotient,qk,n)
    qw={}
    for mask,z in enumerate(weights,1):
        if z:
            qm=sum(1<<c for c,C in enumerate(classes) if mask&(1<<C[0]))
            qw[qm]=qw.get(qm,0)+z
    def qu(t,z):return sum((F(w,sum(bool(mask&(1<<b)) for b in z)) for mask,w in qw.items() if mask&(1<<t)),F(0))
    qs=[qu(t,qe[h])-qu(b,qe[h+(b,)]) for h,t in quotient.items() for b in range(qk)]
    assert min(qs)>=0
    assert len(d['log'])==d['number_nonzero_feasible_policies']==d['number_distinct_policies']==70
    return dict(source_script_sha256=d['seed_script_sha256'],ordered_nodes=len(actions),
        full_comparisons=len(allslacks),nonself_comparisons=len(actions)*(k-1),
        negative_comparisons=0,zero_comparisons=sum(v==0 for v in allslacks),
        root=root,counts=counts,unit_customers=sum(weights),positive_types={i:z for i,z in enumerate(weights,1) if z},
        actual_utilities=[dot(coeff(root,a)) for a in root],W=W,OPT=opt,ratio=opt/W,
        unique_nonzero_exact_rows=len(rows),dual_support=support,dual_all_127_columns_nonnegative=True,
        dual_min_residual=min(residual),dual_zero_residuals=residual.count(F(0)),
        dual_scope='one fixed complete strategy and one saved portfolio; not all portfolios or all policies',
        empty_topics=[a for a,t in enumerate(topic_sets) if not t],all_topic_sets_distinct=len(classes)==k,
        coverage_alias_classes=classes,quotient_nodes=len(quotient),quotient_comparisons=len(qs),
        quotient_minimum_IC=min(qs),quotient_root=qe[()],quotient_positive_types=qw,
        log_entries=len(d['log']),log_rows_range=[min(x['rows'] for x in d['log']),max(x['rows'] for x in d['log'])])

def mixed_saved():
    overlap=read(SRC/'round4_search/mixed_pair_audit.json')
    cross=read(SRC/'round4_search/mixed_pair_cross_point_audit.json')
    prior_path=REPO/'archives/customer-attraction/tools/evidence/product-background-and-completion-primary/new-product-completion-and-2016.json'
    prior=read(prior_path)['new60_2016']
    names={'AB.R':'AB.1','AB.S':'AB.2','AE.R':'AE.1','AE.S':'AE.2','SB.H':'SB.1','SB.I':'SB.2','SB.J':'SB.3','actual.L':'L.actual','second.L':'L.second','third.L':'L.third'}
    def alias(name):
        a=name.split(':');fam=a[0]
        if a[1]=='mixed-pair':
            x,y=sorted((names.get(a[2],a[2]),names.get(a[3],a[3])))
            key=f'cart:{fam}:{x}:{y}'
            return key if key in prior['total_slacks'] else f'cart:{fam}:{y}:{x}'
        if a[1]=='mixed-index':
            pos={'T':0,'AB.R':1,'AB.S':2,'AE.R':1,'AE.S':2,'SB.H':1,'SB.I':2,'SB.J':3}[a[2]]
            return f'{"diag" if a[4]=="diagonal" else "off"}:{fam}:{pos}:{names.get(a[3],a[3])}'
        if a[1]=='direct': return f'direct:{fam}:{a[2]}:{names.get(a[3][4:],a[3][4:])}'
        assert a[1]=='indexed-terminal'
        return f'direct:L.{fam}:{names.get(a[2][4:],a[2][4:])}'
    assert overlap['source_sha256']==prior['input_sha256']
    mapped={alias(k):F(v) for k,v in overlap['all_rows'].items()}
    prior_values={k:F(v) for k,v in prior['total_slacks'].items()}
    if mapped!=prior_values:
        raise AssertionError({'mapped':len(mapped),'missing':sorted(set(prior_values)-set(mapped))[:5],
            'extra':sorted(set(mapped)-set(prior_values))[:5],
            'different':[(k,str(v),str(prior_values.get(k))) for k,v in mapped.items() if k in prior_values and v!=prior_values[k]][:5]})
    inp=REPO/'archives/customer-attraction/tools/evidence/round4-pricing-resumed-boss2/original/exact_primal_cross_pair.json'
    assert sha(inp)==cross['source_sha256']
    tree=ast.parse((SRC/'round4_search/mixed_pair_audit.py').read_text())
    fs=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in {'query_menus','local_H','branches','rows'}]
    assert len(fs)==4
    ns={'F':F,'product':product,'combinations_with_replacement':combinations_with_replacement}
    exec(compile(ast.Module(body=fs,type_ignores=[]),'frozen-mixed-pair-pure-functions','exec'),ns)
    totals={}
    for atom in read(inp)['atoms']:
        mass=F(atom['exact_mass'])
        for k,v in ns['rows'](atom).items():totals[k]=totals.get(k,F(0))+mass*v
    assert totals=={k:F(v) for k,v in cross['all_rows'].items()}
    neg={k:v for k,v in totals.items() if v<0}
    assert neg=={k:F(v) for k,v in cross['negative_rows'].items()} and len(neg)==2
    return dict(overlap_rows=2016,overlap_total_values_match_prior_independent_audit=True,
        overlap_recomputed=False,prior_path=str(prior_path.relative_to(REPO)),prior_sha256=sha(prior_path),
        cross_input_sha256=sha(inp),cross_atoms=61,cross_rows_recomputed=len(totals),
        cross_all_values_match_frozen_report=True,cross_negative_rows=neg,
        cross_min=min(totals.values()),cross_zero_rows=sum(v==0 for v in totals.values()))

def background_saved():
    d=read(SRC/'security_transport/adaptive_value/background_search_best.json');k=d['topics'];n=d['players']
    rows=d['rows'];a=d['terminal'][0];assert d['terminal']==[a]*n
    def val(t,B):return sum((F(x['weight'],x['background']+1+sum(bool(x['mask']&(1<<b)) for b in B)) for x in rows if x['mask']&(1<<t)),F(0))
    v=val(a,[a]*(n-1));upper=[val(t,[a]*(n-1)) for t in range(k)]
    lower=[val(a,B) for B in combinations_with_replacement(range(k),n-1)]
    assert max(upper)==v==min(lower)
    total=sum((F(x['weight']*n,x['background']+n) for x in rows if x['mask']&(1<<a)),F(0))
    assert total==n*v
    # This does not reconstruct all subgame outcomes or an ordered policy.
    return dict(saved_rows=len(rows),unit_weights_sum=sum(x['weight'] for x in rows),
        background_range=[min(x['background'] for x in rows),max(x['background'] for x in rows)],
        terminal=d['terminal'],static_value=v,remaining_total=total,ratio=total/v,
        pure_query=a,all_21_static_background_lower_bound=min(lower),pure_background=[a]*(n-1),
        all_query_upper_values=upper,ordered_SPE_recomputed=False,
        model='arbitrary per-type external loads; no legal shared-prefix realization asserted')

def rational_potential_member():
    """A separately defined rational member of the saved point's two-parameter pattern."""
    raw=read(SRC/'security_transport/adaptive_value/general_potential_best.json')
    k=n=3;a=F(1,5);c=F(1,10)
    triples=list(combinations_with_replacement(range(k),n));backs=list(combinations_with_replacement(range(k),n-1))
    ff={z:(a if z==(0,0,0) else F(1) if z==(1,1,1) else F(0)) for z in triples}
    cc={B:(-F(1) if B==(0,1) else -c if 2 in B else F(0)) for B in backs}
    actions={tuple(x['history']):x['action'] for x in raw['sigma']};ends=complete_ends(actions,k,n)
    def u(t,z):
        B=list(z);B.remove(t);return ff[tuple(sorted(z))]-cc[tuple(sorted(B))]
    slacks=[u(t,ends[h])-u(b,ends[h+(b,)]) for h,t in actions.items() for b in range(k)]
    allu=[u(t,B+(t,)) for B in backs for t in range(k)]
    assert min(slacks)>=0 and min(allu)>=0 and max(allu)<=1
    p=[F(1,2),c,F(2,5)];values=[sum((p[t]*u(t,B+(t,)) for t in range(k)),F(0)) for B in backs]
    assert sum(p)==1 and min(values)==c
    upper=[u(t,(0,2,t)) for t in range(k)];assert upper==[c]*k
    root=ends[()];us=[u(t,root) for t in root];assert sum(us)==2*c
    assert u(1,(1,1,1))>u(1,(1,1,2))
    return dict(identity='separately defined exact rational member; not exact interpretation of saved float values',
        a=a,c=c,F=ff,C=cc,ordered_nodes=len(actions),comparisons=len(slacks),
        minimum_IC_slack=min(slacks),all_18_utilities_range=[min(allu),max(allu)],
        root=root,utilities=us,total=sum(us),query=p,all_background_query_values=values,
        static_value=c,upper_background=[0,2],aggregate_margin=sum(us)-3*c,
        clone_domination_failure={'u_1_at_111':u(1,(1,1,1)),'u_1_at_112':u(1,(1,1,2))})

def reports():
    out={}
    for p in sorted(SRC.rglob('*.json')):
        d=read(p)
        def walk(x):
            if isinstance(x,dict): return 1+sum(walk(k)+walk(v) for k,v in x.items())
            if isinstance(x,list): return 1+sum(map(walk,x))
            return 1
        item={'sha256':sha(p),'bytes':p.stat().st_size,'top_fields':list(d),'all_recursive_nodes_consumed':walk(d)}
        if 'trials' in d and isinstance(d['trials'],list):
            ts=d['trials'];vals=[v for t in ts for v in t['objectives']]
            item.update(records=len(ts),trial_ids=[min(x['trial'] for x in ts),max(x['trial'] for x in ts)],
                args=d['args'],objectives=len(vals),objective_range=[min(vals),max(vals)],best_objective=d['best_objective'])
        if 'records' in d:
            ts=d['records'];assert [t['trial'] for t in ts]==list(range(len(ts)))
            item.update(arguments=d['arguments'],completed=d['completed'],records=len(ts),
                record_max_gap=max(x['best_gap'] for x in ts),menus_range=[min(x['menus'] for x in ts),max(x['menus'] for x in ts)],
                menu_frequency=dict(Counter(x['menus'] for x in ts)),top_best_gap=d['best_gap'])
        out[str(p.relative_to(SRC))]=item
    return out

def main():
    result={'status':'PASS','scope':'fixed saved inputs, standard-library exact arithmetic and record binding; no search or LP',
        'late':late_saved(),'mixed':mixed_saved(),'background':background_saved(),
        'rational_potential_member':rational_potential_member(),'all_JSON_reports':reports(),
        'executed_original_main':0,'LP_or_SLSQP_calls':0,'random_search_calls':0,
        'fractional_drift_note':'original -log minimizer and its KKT are not the free min-max optimizer in general'}
    (HERE/'fixed-input-audit.json').write_text(json.dumps(serial(result),ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(serial({k:v for k,v in result.items() if k!='all_JSON_reports'}),ensure_ascii=False))

if __name__=='__main__':main()
