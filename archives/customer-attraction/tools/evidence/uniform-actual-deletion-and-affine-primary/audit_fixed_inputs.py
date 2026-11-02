#!/usr/bin/env python3
"""One definition-level replay of fixed inputs; no discovery/LP/original imports.

Checks the literal canonical policy and, separately, literal stored anchored graphs.
All negative IC values are preserved before the final assertion.
"""
from pathlib import Path
from fractions import Fraction as F
from functools import lru_cache
from itertools import product,combinations_with_replacement
from collections import Counter
from argparse import ArgumentParser
import gzip,hashlib,json

HERE=Path(__file__).resolve().parent

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def terminal_list(k,m):
    return sorted(tuple(z.count(a) for a in range(k)) for z in combinations_with_replacement(range(k),m))

def actual_counts(z,k):
    return tuple(z.count(a) for a in range(k))

def utility(z,actor,types):
    a=z[actor]
    return sum((F(w,sum((mask>>b)&1 for b in z)) for mask,w in types.items() if (mask>>a)&1),F())

def welfare(z,types):
    return sum(w for mask,w in types.items() if any((mask>>a)&1 for a in z))

def expand_saved(data):
    k,m=data['k'],data['m']; terminals=terminal_list(k,m)
    choices={}
    for x in data['choices']:
        key=(tuple(x['q']),x['target'])
        assert key not in choices
        assert set(x)=={'q','target','action','children'}
        assert len(x['children'])==k
        choices[key]=x
    target=terminals.index(tuple(data['record']['q']))
    policy={}; used=set()
    def expand(h,d):
        q=actual_counts(h,k)
        assert all(a<=b for a,b in zip(q,terminals[d]))
        if len(h)==m:
            assert q==terminals[d]
            return
        key=(q,d); x=choices[key]; used.add(key)
        assert x['children'][x['action']]==d
        policy[h]=x['action']
        for a,next_target in enumerate(x['children']):
            expand(h+(a,),next_target)
    expand((),target)
    assert used==set(choices)
    return policy,len(used)

def audit_policy(label,k,m,types,policy,out):
    histories=[h for d in range(m) for h in product(range(k),repeat=d)]
    assert set(policy)==set(histories)
    assert all(type(a) is int and 0<=a<k for a in policy.values())
    @lru_cache(None)
    def finish(h):
        return h if len(h)==m else finish(h+(policy[h],))
    depths=[dict(histories=0,comparisons_including_self=0,nonself_comparisons=0,zeros_including_self=0,strict=0,negative=0,minimum=None) for _ in range(m)]
    rows=['history,chosen,alternative,chosen_terminal,alternative_terminal,payoff,alternative_payoff,slack\n']
    negative=[]
    for h in histories:
        d=len(h); depths[d]['histories']+=1
        own=finish(h);pay=utility(own,d,types)
        for a in range(k):
            dev=finish(h+(a,)); gain=utility(dev,d,types);slack=pay-gain
            q=depths[d];q['comparisons_including_self']+=1;q['nonself_comparisons']+=a!=policy[h]
            q['zeros_including_self']+=slack==0;q['strict']+=slack>0;q['negative']+=slack<0
            if q['minimum'] is None or slack<F(q['minimum']):q['minimum']=str(slack)
            if slack<0:negative.append(dict(history=h,alternative=a,slack=str(slack),actual=own,deviation=dev))
            rows.append(','.join((''.join(map(str,h)),str(policy[h]),str(a),''.join(map(str,own)),''.join(map(str,dev)),str(pay),str(gain),str(slack)))+'\n')
    raw=''.join(rows).encode()
    (out/(label+'-all-IC.csv.gz')).write_bytes(gzip.compress(raw,mtime=0))
    actual=finish(())
    result=dict(label=label,k=k,m=m,types={str(k):v for k,v in types.items()},customers=sum(types.values()),ordered_decision_nodes=len(histories),
        comparisons_including_self=k*len(histories),nonself_comparisons=(k-1)*len(histories),by_depth=depths,negative_comparisons=negative,
        actual_path=actual,actual_counts=actual_counts(actual,k),payoffs=[str(utility(actual,i,types)) for i in range(m)],W=welfare(actual,types),
        all_IC_csv_sha256=hashlib.sha256(raw).hexdigest(),policy_sha256=hashlib.sha256(json.dumps([{'history':h,'action':policy[h]} for h in histories],separators=(',',':')).encode()).hexdigest())
    return result

def static_query(a,B,types):
    return sum((F(w,1+sum((mask>>b)&1 for b in B)) for mask,w in types.items() if (mask>>a)&1),F())

def affine_count_definition():
    k=m=4;types={1:3,2:1,4:2,7:1,8:2,10:1}; records={}
    def pay(q,a):
        return sum((F(w,sum(q[b] for b in range(k) if mask>>b&1)) for mask,w in types.items() if mask>>a&1),F())
    @lru_cache(None)
    def menu(q):
        if sum(q)==m:return frozenset({q})
        kids=[menu(q[:a]+(q[a]+1,)+q[a+1:]) for a in range(k)]
        threshold=max(min(pay(z,a) for z in child) for a,child in enumerate(kids))
        out=frozenset(z for a,child in enumerate(kids) for z in child if pay(z,a)>=threshold)
        records[q]=(threshold,out)
        return out
    root=menu((0,)*k)
    minima=[min(pay(z,a) for z in menu(tuple(int(a==b) for b in range(k)))) for a in range(k)]
    threshold=max(minima)
    E=sorted({(q,pay(q,0),sum(w for mask,w in types.items() if sum(q[a] for a in range(k) if mask>>a&1))) for q in menu((1,0,0,0))})
    assert E==[((1,1,1,1),F(10,3),10),((2,0,1,1),F(11,6),9)]
    pure=min(W for q,p,W in E if p>=threshold);lam=F(2,3)
    dual=min(F(W)-lam*(p-threshold) for q,p,W in E)
    report=dict(types=types,root_minima=list(map(str,minima)),threshold=str(threshold),
        child0_points=[dict(q=q,p=str(p),W=W) for q,p,W in E],pure_filtered_min=pure,lambda_value=str(lam),dual_value=str(dual),
        convex_weights=['4/9','5/9'],convex_payoff=str(F(4,9)*F(10,3)+F(5,9)*F(11,6)),convex_W=str(F(4,9)*10+F(5,9)*9),
        count_states=menu.cache_info().currsize,root_terminal_counts=sorted(root),
        all_nonterminal_menus=[dict(q=q,threshold=str(t),outcomes=sorted(o)) for q,(t,o) in sorted(records.items())])
    assert threshold==F(5,2) and pure==10 and dual==F(85,9)
    return report

def main():
    parser=ArgumentParser(description=__doc__);parser.add_argument('--output',required=True);args=parser.parse_args()
    out=Path(args.output);out.mkdir(parents=True,exist_ok=False)
    original=HERE/'original'
    instance=json.loads((original/'boss/uniform_deletion_failure_instance.json').read_text())
    cert=json.loads((original/'boss/uniform_deletion_failure_certificate.json').read_text())
    types={sum(1<<a for a in row['topics']):row['multiplicity'] for row in instance['customers']}
    literal={tuple(row['history']):row['action'] for row in cert['actions']}
    assert len(literal)==len(cert['actions'])
    canonical=audit_policy('literal-canonical',6,5,types,literal,out)
    assert canonical['actual_counts']==tuple(cert['terminal_counts'])
    graphs=[];policies=[]
    for filename,scale,inttypes in [('deletion_cone_k6_m5.json',25,types),('deletion_cone_k5_m3.json',6,{4:1,8:1,13:2,18:4})]:
        data=json.loads((original/'boss'/filename).read_text());policy,states=expand_saved(data)
        report=audit_policy('saved-'+str(data['k'])+'-'+str(data['m']),data['k'],data['m'],inttypes,policy,out)
        expected=[F(inttypes.get(mask,0),scale) for mask in range(1,1<<data['k'])]
        # Float identity is diagnostic only; all IC signs above use exact integer input.
        error=max(abs(float(f)-v) for f,v in zip(expected,data['weights']))
        assert error<1e-12
        q=report['actual_path'];query=data['record']['query'];m=data['m']
        mean=sum((static_query(query,q[:i]+q[i+1:],inttypes) for i in range(m)),F())/m
        report.update(anchored_states=states,float_weight_scale=scale,maximum_float_recovery_error=error,
                      saved_query=query,uniform_query=str(mean),normalized_bridge_ratio=str(mean*F(2*m-1,2)/report['W']),
                      canonical_action_differences=sum(policy[h]!=literal[h] for h in literal) if data['k']==6 else None)
        graphs.append(report);policies.append(policy)
    z=tuple(canonical['actual_path']);B=[z[:i]+z[i+1:] for i in range(5)]
    matrix=[[static_query(a,b,types) for b in B] for a in range(6)]
    uniform=[sum(row,F())/5 for row in matrix]
    optimum=max(welfare(z0,types) for z0 in combinations_with_replacement(range(6),5))
    assert optimum==30 and canonical['W']==25 and max(uniform)==F(28,5)
    assert matrix[0]==[F(6),F(5),F(6),F(6),F(5)]
    assert max(row[1] for row in matrix)==5 and min(matrix[0])==5
    deletion=dict(backgrounds=B,query_by_deleted_position=[[str(v) for v in row] for row in matrix],uniform_values=list(map(str,uniform)),
                  maximum_uniform_value=str(max(uniform)),threshold=str(F(25,1)/F(9,2)),strict_gap=str(max(uniform)-F(50,9)),ratio=str(max(uniform)*F(9,2)/25),
                  optimal_actual_deletion_support_cap='5',upper_certificate_deleted_position=1,lower_certificate_query=0,OPT5=optimum)
    affine=affine_count_definition()
    report=dict(scope='one fixed-input definition reconstruction; no original mathematical code imported; no LP/discovery',
        literal_canonical=canonical,saved_cone_graphs=graphs,deletion_kernel=deletion,affine_independent_count_menus=affine,
        source_fingerprints={str(p.relative_to(HERE)):sha(p) for p in sorted(original.rglob('*')) if p.is_file()},
        claimed_original_verify_certificate_call=False,LP_calls=0,discovery_entrypoint_calls=0)
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    assert all(not x['negative_comparisons'] for x in [canonical,*graphs]),'negative IC preserved in report'
    print(json.dumps(dict(status='PASS',literal_nodes=canonical['ordered_decision_nodes'],literal_comparisons=canonical['comparisons_including_self'],
        saved_graphs=[{k:r[k] for k in ('k','m','anchored_states','ordered_decision_nodes','normalized_bridge_ratio','canonical_action_differences')} for r in graphs],
        uniform_max=deletion['maximum_uniform_value'],strict_gap=deletion['strict_gap'],deletion_support_cap='5',affine_count_states=affine['count_states'],LP_calls=0),indent=2))

if __name__=='__main__':main()
