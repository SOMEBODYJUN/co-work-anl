"""Exact targeted checks of recovered finite CAG witnesses; no search or LP solve."""
from pathlib import Path
from fractions import Fraction
from functools import lru_cache
from itertools import combinations_with_replacement, product
import gzip, hashlib, json
BASE = Path(__file__).resolve().parent

def audit(entry, source, label):
    strategy = entry['strategy']; rows = strategy['actions']; p = 7; m = 5
    policy = {tuple(r.get('history',r.get('h'))): r.get('action',r.get('a')) for r in rows}
    expected = {h for depth in range(m) for h in product(range(p), repeat=depth)}
    assert len(rows)==len(policy)==2801 and set(policy)==expected
    assert all(type(a) is int and 0<=a<p for a in policy.values())
    masses = entry['integer_clones']; assert len(masses)==127
    assert all(type(w) is int and w>=0 for w in masses)
    customers = [(mask,w) for mask,w in enumerate(masses,1) if w]
    @lru_cache(None)
    def finish(h):
        if len(h)==m: return h
        return finish(h+(policy[h],))
    @lru_cache(None)
    def payoff(action,counts):
        return sum((Fraction(w, sum(c for j,c in enumerate(counts) if mask>>j&1))
                    for mask,w in customers if mask>>action&1),Fraction(0))
    def counts(h): return tuple(h.count(a) for a in range(p))
    def welfare(c): return sum(w for mask,w in customers if any(mask>>a&1 and c[a] for a in range(p)))
    checks=0; min_slack=None
    for h,a in policy.items():
        own=payoff(a,counts(finish(h)))
        for b in range(p):
            if b==a: continue
            difference=own-payoff(b,counts(finish(h+(b,))))
            assert difference>=0, (label,h,a,b,str(difference))
            min_slack=difference if min_slack is None else min(min_slack,difference)
            checks+=1
    actual=finish(()); W=welfare(counts(actual))
    optimum=max(welfare(counts(t)) for t in combinations_with_replacement(range(p),m))
    assert W==entry['welfare'] and optimum==entry.get('optimal_welfare',entry.get('optimum'))
    raw=source.read_bytes()
    return {'label':label,'source_file':source.name,'source_sha256':hashlib.sha256(raw).hexdigest(),
            'players':m,'topics':p,'nonzero_customer_types':customers,'total_customers':sum(masses),
            'actual_actions':actual,'actual_counts':counts(actual),'actual_payoffs':[str(payoff(a,counts(actual))) for a in actual],
            'welfare':W,'optimal_welfare':optimum,'ratio':str(Fraction(optimum,W)),
            'complete_nodes':len(policy),'nonself_deviation_checks':checks,'minimum_IC_slack':str(min_slack),
            'LP_optimality_rechecked':False}

qpath=BASE/'sym_m5p7_q32_Jout.json'; q=json.loads(qpath.read_text())['exact_candidate']
results=[audit(q,qpath,'q32')]
cpath=BASE/'shared_cycle_cone_attack.json.gz'; c=json.loads(gzip.decompress(cpath.read_bytes()))
for i,row in enumerate(c['results']):
    result=audit(row,cpath,'shared-cycle-'+str(i));result['portfolio']=row['portfolio'];results.append(result)
report={'scope':'Recovered exact unit-customer instances and all ordered policy actions; targeted source-consistency check, not a new search or LP proof.',
        'checks':results,'not_checked':['LP dual row enumeration/optimality','abstract full_history_walk moment cone','universal mathematical claims']}
(BASE/'audit_finite_cag.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'status':'exact-finite-policies-verified','policies':len(results),'nodes':sum(r['complete_nodes'] for r in results),'deviation_checks':sum(r['nonself_deviation_checks'] for r in results)},ensure_ascii=False))
