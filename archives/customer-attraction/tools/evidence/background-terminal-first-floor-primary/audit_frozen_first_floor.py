"""Exact audit of the saved seven-label policy, not a new discovery scan."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product,combinations_with_replacement
from functools import lru_cache
from collections import Counter
import json,hashlib
H=Path(__file__).resolve().parent
P=H/'original/research/workspaces/customer-attraction/R-e6796fb9db2a4ae9994cee93ac9bd152/background/first_floor_best_5_7.json'
def main():
    raw=P.read_bytes();d=json.loads(raw);m=d['m'];k=d['k'];assert(m,k)==(5,7)
    acts={tuple(q):a for q,a in d['acts']};assert len(acts)==len(d['acts'])==330
    expected=set()
    for depth in range(m):
        for h in product(range(k),repeat=depth):expected.add(tuple(h.count(a)for a in range(k)))
    assert set(acts)==expected and all(len(q)==k and 0<=a<k for q,a in acts.items())
    weights={int(mask):F(str(w))for mask,w in d['weights']};assert weights=={4:F(1),27:F(5),32:F(1),64:F(1)}
    def plus(q,a):return q[:a]+(q[a]+1,)+q[a+1:]
    @lru_cache(None)
    def finish(q):return q if sum(q)==m else finish(plus(q,acts[q]))
    def pay(q,a):return sum((w/F(sum(q[b]for b in range(k)if mask>>b&1))for mask,w in weights.items()if mask>>a&1),F(0))
    count_checks=ordered_checks=nonself=0;minimum=None;layers=[]
    for depth in range(m):
        cs=[q for q in acts if sum(q)==depth];cmin=None
        for q in cs:
            a=acts[q];u=pay(finish(q),a)
            for b in range(k):
                gap=u-pay(finish(plus(q,b)),b);assert gap>=0;count_checks+=1;cmin=gap if cmin is None else min(cmin,gap)
        histories=0;omin=None
        for h in product(range(k),repeat=depth):
            histories+=1;q=tuple(h.count(a)for a in range(k));a=acts[q];u=pay(finish(q),a)
            for b in range(k):
                gap=u-pay(finish(plus(q,b)),b);assert gap>=0;ordered_checks+=1;nonself+=int(a!=b);omin=gap if omin is None else min(omin,gap)
        minimum=omin if minimum is None else min(minimum,omin)
        layers.append(dict(depth=depth,count_states=len(cs),count_action_comparisons=len(cs)*k,ordered_decision_histories=histories,ordered_comparisons_including_self=histories*k,min_count_slack=str(cmin),min_ordered_slack=str(omin)))
    q=(0,)*k;path=[]
    for i in range(m):a=acts[q];path.append(a);q=plus(q,a)
    assert list(q)==d['out']
    welfare=sum(w for mask,w in weights.items()if any(mask>>a&1 for a in path));profits=[pay(q,a)for a in path]
    coverage=[]
    for choice in combinations_with_replacement(range(k),m):coverage.append((sum(w for mask,w in weights.items()if any(mask>>a&1 for a in choice)),choice))
    opt=max(x[0]for x in coverage);savedchoice=tuple(d['opt']);savedvalue=next(v for v,t in coverage if t==savedchoice)
    assert opt==savedvalue==8 and welfare==5 and profits==[F(1)]*5 and opt/profits[0]==F(str(d['ratio']))==8
    likes={a:tuple(mask for mask in weights if mask>>a&1)for a in range(k)}
    core=[a for a in range(k)if likes[a]==(27,)]
    assert core==[0,1,3,4]and all(a in core for a in acts.values())
    assert ordered_checks==19607 and nonself==16806 and count_checks==2310 and sum(x['ordered_decision_histories']for x in layers)==2801
    assert P.read_bytes()==raw
    out=dict(status='exact fixed-input seven-label SPE audit passed',source_sha256=hashlib.sha256(raw).hexdigest(),players=m,labels=k,unit_customers=sum(int(w)for w in weights.values()),weights=[[mask,str(w)]for mask,w in weights.items()],stored_count_state_action_entries=330,ordered_decision_histories=2801,count_action_comparisons_including_self=count_checks,ordered_action_comparisons_including_self=ordered_checks,ordered_nonself_comparisons=nonself,minimum_exact_IC_slack=str(minimum),layers=layers,actual_path=path,actual_counts=list(q),actual_payoffs=list(map(str,profits)),W=str(welfare),OPT_m=str(opt),optimal_multisets_checked=len(coverage),saved_optimal_multiset=list(savedchoice),root_opt_ratio=str(opt/profits[0]),weak_threshold_2m_minus_1=2*m-1,ratio_strictly_below_weak_threshold=True,equal_coverage_label_classes=[core,[2],[5],[6]],prescribed_label_counts=dict(Counter(acts.values())),all_prescribed_actions_cover_core=True,labels_merged=False,original_discovery_main_executions=0,scipy_calls=0,scope='Exact certification of this one fixed stored policy in its seven-label extension; Markov counts expand to all ordered histories, no restriction on general SPE. No general first-player floor or HALF counterexample is proved.')
    (H/'frozen-first-floor-exact-audit.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps(out,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
