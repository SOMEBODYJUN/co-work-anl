"""Diagnostic of the weak portfolio bridge on existing finite certificates.
Not a general proof. Exact Fraction arithmetic; only writes own workspace.
"""
import json, sys
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations_with_replacement
from functools import lru_cache
ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT))
from customer_attraction.model import Instance
from customer_attraction.certificate import StrategyCertificate,verify_certificate


def evaluate(inst, cert):
    m,k=inst.players,inst.topic_count
    @lru_cache(None)
    def term(h):
        return h if len(h)==m else term(h+(cert.actions[h],))
    actual=term(())
    W=inst.welfare(inst.counts(actual))
    V=tuple(tuple(inst.player_payoffs(term(actual[:i]+(a,)))[i] for a in range(k)) for i in range(m))
    def match(profile):
        @lru_cache(None)
        def dp(i,p):
            if i==m:return F(0)
            return max(V[i][a]+dp(i+1,p[:j]+p[j+1:]) for j,a in enumerate(p))
        return dp(0,profile)
    opt=inst.optimal_welfare()
    profiles=[p for p in combinations_with_replacement(range(k),m) if inst.welfare(inst.counts(p))==opt]
    scores=[(match(p),p) for p in profiles]
    best=max(scores)
    worst=min(scores)
    return dict(actual=actual,W=W,OPT=opt,best_matching=str(best[0]),worst_matching=str(worst[0]),best_slack=str(W+best[0]-opt),worst_slack=str(W+worst[0]-opt),best_profile=best[1],worst_profile=worst[1],V=[[str(v) for v in row] for row in V])

if __name__=='__main__':
    result={}
    for p in sorted((ROOT/'evidence/certificates/customer_attraction').glob('*.json')):
        inp=ROOT/'examples/customer_attraction'/p.name
        if not inp.exists():continue
        try:
            inst=Instance.from_dict(json.loads(inp.read_text()))
            cert=StrategyCertificate.from_dict(json.loads(p.read_text()))
            if inst.players>6 or inst.topic_count>8:continue
            check=verify_certificate(inst,cert)
            if not check.valid:continue
            result[p.name]=evaluate(inst,cert)
            print(p.name,result[p.name]['best_slack'],result[p.name]['worst_slack'],flush=True)
        except (KeyError,ValueError,TypeError) as e:print('skip',p.name,str(e),flush=True)
    Path(__file__).with_name('weak_matching_existing.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
