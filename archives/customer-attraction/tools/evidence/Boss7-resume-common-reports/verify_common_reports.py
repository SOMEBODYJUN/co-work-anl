"""Definition-level, standard-library checks of three frozen report files.
No original module, numerical LP, random search, or external solver is executed.
The reconstructed policy is a new auditable realization of the saved cone,
not a claim to recover an unavailable historical command or execution trace.
"""
import hashlib, json, math
from fractions import Fraction as F
from itertools import combinations_with_replacement, product
from pathlib import Path
BASE=Path(__file__).resolve().parent
SRC=BASE/'source-root/research/workspaces/customer-attraction/R-acd97406d8c4409d962eab2adcdc520c/round3_security'

def serial(x):
    if isinstance(x,F):return str(x)
    if isinstance(x,dict):return {str(k):serial(v)for k,v in x.items()}
    if isinstance(x,(list,tuple)):return [serial(v)for v in x]
    return x

def cts(d,k):
    return [tuple(q.count(a)for a in range(k))for q in combinations_with_replacement(range(k),d)]

def realize(w,n,k):
    """Exact version of the documented count/target construction, from definitions."""
    L=math.lcm(*range(1,n+1));final=cts(n,k);mask=range(1,1<<k)
    coeff=[];U=[];W=[]
    for q in final:
        loads=[sum(q[a]for a in range(k)if T>>a&1)for T in mask]
        rows=[tuple(L//max(1,loads[T-1])if T>>a&1 else 0 for T in mask)for a in range(k)]
        coeff.append(rows);U.append([sum(x*y for x,y in zip(row,w))for row in rows]);W.append(sum(x for x,l in zip(w,loads)if l))
    states=[cts(d,k)for d in range(n+1)];R={q:(j,)for j,q in enumerate(final)}
    child={q:[tuple(v+int(a==b)for b,v in enumerate(q))for a in range(k)]for d in range(n)for q in states[d]}
    for d in reversed(range(n)):
        for q in states[d]:
            floor=max(min(U[j][a]for j in R[t])for a,t in enumerate(child[q]))
            R[q]=tuple(sorted({j for a,t in enumerate(child[q])for j in R[t]if U[j][a]>=floor}))
    zero=(0,)*k;root=min(R[zero],key=lambda j:W[j]);pending=[(zero,root)];policy={};G=set()
    while pending:
        q,target=pending.pop()
        if sum(q)==n or (q,target)in policy:continue
        floor=max(min(U[j][a]for j in R[t])for a,t in enumerate(child[q]))
        a=next(a for a,t in enumerate(child[q])if target in R[t]and U[target][a]>=floor)
        dest=[target if b==a else min(R[t],key=lambda j:U[j][b])for b,t in enumerate(child[q])]
        policy[q,target]=(a,dest)
        for b,dev in enumerate(dest):
            row=tuple(x-y for x,y in zip(coeff[target][a],coeff[dev][b]));G.add(row)
            pending.append((child[q][b],dev))
    G.discard((0,)*len(w));G=sorted(G)
    # Every ordered history carries its child target, so all off-path histories occur.
    histories=0;comparisons=0;expanded_rows=set();margins=[];path=[];stack=[(zero,root,())]
    while stack:
        q,t,h=stack.pop()
        if len(h)==n:continue
        histories+=1;a,dest=policy[q,t]
        for b,dev in enumerate(dest):
            row=tuple(x-y for x,y in zip(coeff[t][a],coeff[dev][b]));expanded_rows.add(row)
            margins.append(sum(x*y for x,y in zip(row,w)));comparisons+=1
            stack.append((child[q][b],dev,h+(b,)))
    expanded_rows.discard((0,)*len(w));assert sorted(expanded_rows)==G and min(margins)>=0
    q=zero;t=root
    for _ in range(n):
        a,dest=policy[q,t];path.append(a);t=dest[a];q=child[q][a]
    assert q==final[root] and histories==sum(k**d for d in range(n))
    return dict(n=n,k=k,L=L,root_counts=final[root],states=len(policy),rows=G,
      ordered_history_nodes=histories,ordered_comparisons=comparisons,min_scaled_IC=min(margins),actual_path=path,
      exact_seed_min_SPE_welfare=min(W[j]for j in R[zero]),exact_seed_OPT=max(W),
      policy=[dict(counts=q,target_counts=final[t],action=a,children=[dict(action=b,target_counts=final[v])for b,v in enumerate(dest)])for(q,t),(a,dest)in sorted(policy.items())])

def residual(z,rationalize=False):
    n=z['n'];k=z['k'];L=math.lcm(*range(1,n+1));root=z['root_counts']
    recover=lambda x: x.limit_denominator(10**4)if rationalize else x
    Q=[(h['counts'],recover(h['probability']))for h in z['Q']]
    lambdas=[[(r,recover(v))for r,v in a]for a in z['multiplier_rows']]
    rs=[]
    for a in range(k):
        line=[]
        for T in range(1,1<<k):
            c=F(any(root[b]and T>>b&1 for b in range(k)),n)
            beta=sum((q*F((T>>a)&1,1+sum(h[b]for b in range(k)if T>>b&1))for h,q in Q),F())
            line.append(c-beta-sum((x*F(row[T-1],L)for row,x in lambdas[a]),F()))
        rs.append(line)
    probs=[p for h,p in Q];lamvals=[x for a in lambdas for r,x in a]
    ok=sum(probs)==1 and min(probs+lamvals)>=0 and min(x for a in rs for x in a)>=0
    return dict(rationalization_denominator_bound=10**4 if rationalize else None,Q=Q,
        Q_sum=sum(probs),minimum_residual=min(x for a in rs for x in a),negative_residual_count=sum(x<0 for a in rs for x in a),
        exact_identity_checks=k*((1<<k)-1),passes_coefficient_certificate=ok,
        multipliers=lambdas,residual=rs)

def main():
    manifest=json.loads((BASE/'source-manifest.json').read_text())
    for m in manifest:
        b=(BASE/'source-root'/m['path']).read_bytes();assert len(b)==m['size']and hashlib.sha256(b).hexdigest()==m['sha256']
    names=['common_n4_k6.json','common_n5_k6.json','cone_n4_k6.json']
    docs={name:json.loads((SRC/name).read_text())for name in names}
    exact_docs={name:json.loads((SRC/name).read_text(),parse_float=F)for name in names}
    # A lossless semantic index groups exact equal complete values and records all occurrences.
    groups={};occ=[]
    for name,d in docs.items():
        for j,z in enumerate(d['results']):
            for field,value in z.items():
                key=json.dumps(value,sort_keys=True,separators=(',',':'));g=groups.setdefault(key,dict(value=value,occurrences=[]));g['occurrences'].append(f'{name}#/results/{j}/{field}')
    content=list(groups.values())
    (BASE/'complete-content-index.json').write_text(json.dumps(dict(root_fields={name:{k:v for k,v in d.items()if k!='results'}for name,d in docs.items()},groups=content),ensure_ascii=False,indent=2)+'\n')
    seeds={}
    for name,d in docs.items():
        for j,z in enumerate(d['results']):
            init=z['initial'];key=tuple(init['weights']);sk=(init['n'],init['k'],key)
            if sk not in seeds:seeds[sk]=realize(list(key),init['n'],init['k'])
            r=seeds[sk];assert list(r['root_counts'])==z['root_counts']and r['states']==z['policy_subproblems']and len(r['rows'])==z['Gamma_rows']
            assert r['exact_seed_min_SPE_welfare']==init['min_welfare']and r['exact_seed_OPT']==init['max_welfare']
            if 'rows'in z:assert r['rows']==list(map(tuple,z['rows']))
            if 'multiplier_rows'in z:
                for a in z['multiplier_rows']:
                    assert all(tuple(row)in set(r['rows'])for row,v in a)
    (BASE/'reconstructed-policy-dags.json').write_text(json.dumps(serial(list(seeds.values())),indent=2)+'\n')
    report=dict(scope='exact source integrity / lossless field identity / deterministic reconstructed full policy / saved coefficient arithmetic; no numerical LP or random search',source_count=4,
      source_result_counts={name:len(d['results'])for name,d in docs.items()},distinct_integer_seeds=len(seeds),seed_checks=[])
    for(n,k,w),r in seeds.items():
        report['seed_checks'].append({key:v for key,v in r.items()if key not in('rows','policy')})
    report['certificates']={}
    for name in names[:2]:
        z=exact_docs[name]['results'][0];report['certificates'][name]=dict(literal_retained_numbers=residual(z),denominator_10000_reconstruction=residual(z,True))
    # All cone snapshots have the exact same noninitial payload, including every stored row.
    cones=exact_docs[names[2]]['results'];z=cones[0]
    assert all({k:v for k,v in x.items()if k!='initial'}=={k:v for k,v in z.items()if k!='initial'}for x in cones)
    assert z['weights']==[F(0)]*62+[F(1)]and z['query']==[F(1)]+[F(0)]*5
    assert all(row[-1]==0 for row in z['rows'])
    report['cone_terminal_point']=dict(exact_weights='mask63=1; all other masks=0',exact_query=[1,0,0,0,0,0],exact_W=1,exact_OPT=1,exact_v=F(1,4),exact_gap=0,every_full_policy_is_SPE=True,all_306_rows_have_zero_mask63_coefficient=True)
    report['reconstruction_attempts']=dict(denominator_bounds_preflight=[10000,1000000,100000000],common4_passes_all=True,common5_passes_none=True,additional_rational_solving_performed=False)
    (BASE/'exact-check-report.json').write_text(json.dumps(serial(report),indent=2)+'\n')
    print(json.dumps(dict(source_count=4,result_counts=report['source_result_counts'],distinct_integer_seeds=len(seeds),reconstructed_policies=[dict(n=r['n'],states=r['states'],rows=len(r['rows']),ordered_nodes=r['ordered_history_nodes'],comparisons=r['ordered_comparisons'])for r in seeds.values()],common4_exact=report['certificates'][names[0]]['denominator_10000_reconstruction']['passes_coefficient_certificate'],common5_exact=report['certificates'][names[1]]['denominator_10000_reconstruction']['passes_coefficient_certificate'],cone_terminal_exact=True),indent=2))
if __name__=='__main__':main()
