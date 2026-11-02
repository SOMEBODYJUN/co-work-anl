"""One fixed-input, standard-library audit; no original discovery code is imported.

Read only the 36 rational records and two preserved starting inputs. Reuse the
exact frozen ordered action maps, and construct a separate constant-zero policy
for each starting input. No LP, random search, or outcome-set solver is called.
"""
from pathlib import Path
from fractions import Fraction as F
from functools import lru_cache
from itertools import product, combinations_with_replacement
from math import gcd, lcm
from hashlib import sha256
import argparse
import json


def read_json(path):
    return json.loads(path.read_text())


def dump(obj):
    return json.dumps(obj,ensure_ascii=False,indent=2)


def audit(evidence, repository):
    primary=read_json(evidence/'source-manifest.json')
    dependencies=read_json(evidence/'dependency-manifest.json')
    maps={}
    checked_inputs=[]
    for row in primary+dependencies:
        path=repository/row['preserved_path']
        # During staged execution, the new files live under a parallel stage.
        if not path.is_file():
            candidate=evidence
            while candidate.name!='archives' and candidate.parent!=candidate:
                candidate=candidate.parent
            path=candidate.parent/row['preserved_path']
        data=path.read_bytes()
        assert len(data)==row['size'] and sha256(data).hexdigest()==row['sha256'],row['path']
        maps[row['path']]=path
        checked_inputs.append({'id':row['id'],'path':row['preserved_path'],'sha256':row['sha256']})

    result_path=next(maps[r['path']] for r in primary if r['id']=='e281e231e324f13a58c3')
    groups=read_json(result_path)
    all_records=[]
    all_compared=0
    policy_groups={}
    complete_histories=0
    for group in groups:
        name=group['name']
        game=read_json(maps[f'examples/customer_attraction/{name}.json'])
        cert=read_json(maps[f'evidence/certificates/customer_attraction/{name}.json'])
        k=len(game['topics']);m=game['players'];assert (k,m)==(group['topics'],group['players'])
        actions=cert['strategy']['actions']
        policy={tuple(row['history']):row['action'] for row in actions}
        assert len(policy)==len(actions)
        expected={h for n in range(m) for h in product(range(k),repeat=n)}
        assert set(policy)==expected and all(type(a) is int and 0<=a<k for a in policy.values())
        policy_hash=sha256(json.dumps([[list(h),policy[h]] for h in sorted(policy,key=lambda h:(len(h),h))],separators=(',',':')).encode()).hexdigest()
        policy_groups.setdefault(policy_hash,[]).append(name)

        @lru_cache(None)
        def leaf(h):
            return h if len(h)==m else leaf(h+(policy[h],))

        actual=leaf(())
        assert list(actual)==group['path']
        assert group['rows']==len(policy)*(k-1)
        assert len(group['records'])==k and sorted(r['query'] for r in group['records'])==list(range(k))
        for record in group['records']:
            weights={int(t):F(v) for t,v in record['weights'].items()}
            assert all(0<t<(1<<k) and v>=0 for t,v in weights.items())

            @lru_cache(None)
            def payoff(action, terminal):
                return sum((w/sum((t>>a)&1 for a in terminal) for t,w in weights.items() if (t>>action)&1),F(0))

            slacks=[]
            strict=tie=0
            for h in sorted(policy,key=lambda h:(len(h),h)):
                chosen=policy[h];u=payoff(chosen,leaf(h))
                for alt in range(k):
                    if alt==chosen:
                        continue
                    gap=u-payoff(alt,leaf(h+(alt,)))
                    assert gap>=0,(name,record['query'],h,alt,str(gap))
                    slacks.append(gap)
                    strict+=gap>0;tie+=gap==0
            complete_histories+=len(policy)
            all_compared+=len(slacks)
            W=sum((w for t,w in weights.items() if any((t>>a)&1 for a in actual)),F(0))
            caps=[sum((w/(1+F(m-1,m)*sum((t>>b)&1 for b in actual)) for t,w in weights.items() if (t>>a)&1),F(0)) for a in range(k)]
            q=record['query'];gap=F(2*m-1,2)*caps[q]-W
            assert W==F(record['W'])==1
            assert caps[q]==F(record['cap']) and gap==F(record['gap_exact'])
            assert min(slacks,default=F(0))==F(record['minimum_spe_slack'])
            denominator=lcm(*(w.denominator for w in weights.values()))
            ints={t:int(w*denominator) for t,w in weights.items() if w}
            common=gcd(*ints.values())
            scale=F(denominator,common)
            expanded={t:n//common for t,n in ints.items()}
            maximum=max(caps)
            all_records.append({'name':name,'query':q,'ordered_histories':len(policy),
                                'proper_comparisons':len(slacks),'strict':strict,'ties':tie,
                                'minimum_slack':str(min(slacks,default=F(0))),
                                'W':str(W),'selected_cap':str(caps[q]),'selected_gap':str(gap),
                                'all_query_caps':list(map(str,caps)),'actual_M':str(maximum),
                                'true_max_gap':str(F(2*m-1,2)*maximum-W),
                                'query_is_exact_maximizer':caps[q]==maximum,
                                'integer_scale':str(scale),'integer_customer_count':sum(expanded.values()),
                                'integer_weights':{str(t):v for t,v in expanded.items()},
                                'policy_actions_sha256':policy_hash})

    seeds=[]
    seed_proper=seed_all=seed_states=0
    for sid in ['dfe2c1e7207d75851eae','b73ad56a5c2291c6b719']:
        r=next(r for r in primary if r['id']==sid)
        packet=read_json(maps[r['path']]);assert len(packet['records'])==1
        record=packet['records'][0];m=packet['players'];k=packet['topics']
        w=record['weights'];assert len(w)==(1<<k)-1 and all(type(v) is int and v>=0 for v in w)
        expected=[0]*len(w);expected[0]=m
        for a in range(1,min(k,m)):expected[(1<<a)-1]=1
        assert w==expected and record['trial']==0
        counts=tuple(record['counts']);assert counts==(m,)+(0,)*(k-1)
        types={t:v for t,v in enumerate(w,1) if v}

        def terminal_payoff(action,c):
            return sum((F(v,sum(c[a] for a in range(k) if (t>>a)&1)) for t,v in types.items() if (t>>action)&1),F(0))

        strict=ties=proper=including=states=0
        for d in range(m):
            for seq in combinations_with_replacement(range(k),d):
                prefix=tuple(seq.count(a) for a in range(k))
                states+=1
                # Explicit complete policy sigma(h)=0 for every ordered h.
                chosen=list(prefix);chosen[0]+=m-d
                u=terminal_payoff(0,chosen)
                for alt in range(k):
                    z=list(prefix);z[alt]+=1;z[0]+=m-d-1
                    diff=u-terminal_payoff(alt,z)
                    assert diff>=0,(sid,prefix,alt,str(diff))
                    including+=1
                    if alt:
                        proper+=1;strict+=diff>0;ties+=diff==0
        W=sum(v for t,v in types.items() if (t&1))
        caps=[sum((F(v)/(1+F(m-1,m)*sum(counts[b] for b in range(k) if (t>>b)&1)) for t,v in types.items() if (t>>a)&1),F(0)) for a in range(k)]
        q=record['query'];ratio=F(2*m-1,2)*caps[q]/W
        assert W==record['W']==m and F(record['cap'])==caps[q]==max(caps)==1
        assert ratio==F(record['ratio'])
        seed_proper+=proper;seed_all+=including;seed_states+=states
        seeds.append({'source_id':sid,'players':m,'topics':k,'unit_customers':sum(w),
                      'source_trial':0,'actual_counts':list(counts),'W':W,'all_query_caps':list(map(str,caps)),
                      'ratio':str(ratio),'optimum':sum(w),'half_margin':2*W-sum(w),
                      'new_explicit_policy':'sigma(h)=0 at every legal ordered decision history',
                      'checked_count_states':states,'count_state_proper_comparisons':proper,
                      'count_state_comparisons_including_self':including,'strict':strict,'ties':ties,
                      'represented_ordered_histories':sum(k**d for d in range(m)),
                      'why_count_check_covers_this_policy':'Payoff depends only on counts, and the newly explicit constant-zero policy uses the same continuation at every such history; this does not impose Markov policies on the original outcome-set search.',
                      'not_a_recovered_original_policy_or_complete_search_replay':True})

    return {'status':'PASS','scope':'fixed preserved rational points plus two separately constructed constant-zero policies; no optimization or original search replay',
            'input_fingerprints':checked_inputs,'primary_record_count':len(all_records),
            'ordered_histories_across_records':complete_histories,'proper_comparisons':all_compared,
            'comparisons_including_self':all_compared+complete_histories,
            'distinct_complete_policy_maps':len(policy_groups),'policy_name_groups':policy_groups,
            'records':all_records,'seed_policy_records':seeds,
            'seed_count_states':seed_states,'seed_count_state_proper_comparisons':seed_proper,
            'seed_count_state_comparisons_including_self':seed_all,
            'old_LP_runs':0,'old_randomized_scans':0,'old_backend_selftests':0,
            'universal_weak_bridge_not_certified':True}


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--evidence',type=Path,required=True);ap.add_argument('--repository',type=Path,required=True)
    args=ap.parse_args()
    print(dump(audit(args.evidence,args.repository)))
