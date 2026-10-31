"""Full ordered-tree Fraction checks of the arbitrary-marked insurer.

No repository model/solver imports. This validates the code for finite m;
the all-m statement is proved in heterogeneous_prefix_repair.md.
"""
from fractions import Fraction as Q
from functools import lru_cache
from itertools import combinations
from pathlib import Path
import json


def audit(m, marks):
    k = len(marks)
    d = m-k
    # banks 0,...,k-1; reservoir k; leaves k+1,...,m-1
    sizes = (Q(2),)*k + (Q(d),) + (Q(1),)*(d-1)
    bank_at = {i:a for a,i in enumerate(marks)}
    normal = tuple(bank_at.get(i, k) for i in range(m))

    def counts(h):
        return tuple(h.count(a) for a in range(m))

    def inc(c,a):
        return c[:a]+(c[a]+1,)+c[a+1:]

    def pay(c,a):
        return sizes[a]/c[a] if c[a] else Q(0)

    @lru_cache(None)
    def bi(c):
        if sum(c)==m:
            return c
        return bi(inc(c, bi_action(c)))

    @lru_cache(None)
    def bi_action(c):
        return max(range(m), key=lambda a:(pay(bi(inc(c,a)),a),-a))

    checks = states = exits = 0
    worst_cap = Q(0)
    min_margin = None
    for i in range(m):
        prefix = normal[:i]
        for forced in range(m):
            start = prefix+(forced,)
            prior = counts(prefix)
            mode = 'BI' if (forced>k or (forced<k and prior[forced])) else 'Y' if forced==k else 'F'
            F = forced

            def choose(h, permanent_bi=False):
                c=counts(h)
                if permanent_bi or mode=='BI':
                    return bi_action(c)
                empty=[a for a in range(k) if not c[a]]
                if empty:
                    return empty[0]
                if mode=='Y' or c[k]<d-1:
                    return k
                return F

            def child_is_bi(h,a,permanent_bi):
                if permanent_bi or mode=='BI':
                    return True
                c=counts(h+(a,))
                # Final designated duplicate F is terminal, so may be marked
                # as BI without affecting anything.
                return any(v>1 for v in c[:k]) or any(c[k+1:]) or c[k]>(d if mode=='Y' else d-1)

            @lru_cache(None)
            def terminal(h,permanent_bi=False):
                if len(h)==m:
                    return h
                a=choose(h,permanent_bi)
                return terminal(h+(a,),child_is_bi(h,a,permanent_bi))

            def visit(h,permanent_bi=False):
                nonlocal checks, states, min_margin
                if len(h)==m:
                    return
                states+=1
                a=choose(h,permanent_bi)
                prescribed=pay(counts(terminal(h,permanent_bi)),a)
                for b in range(m):
                    nxt=h+(b,)
                    status=child_is_bi(h,b,permanent_bi)
                    alternative=pay(counts(terminal(nxt,status)),b)
                    margin=prescribed-alternative
                    assert margin>=0,(m,marks,i,forced,h,a,b,margin)
                    min_margin=margin if min_margin is None else min(min_margin,margin)
                    checks+=1
                    visit(nxt,status)

            end=terminal(start)
            cap=pay(counts(end),forced)
            assert cap<=1,(m,marks,i,forced,cap,end)
            worst_cap=max(worst_cap,cap)
            exits+=1
            visit(start)

    # All marked/unmarked normal nodes can use the audited low exits.
    # At the normal leaf own payoff is exactly2 / exactly1 by its role.
    nc=counts(normal)
    assert tuple(pay(nc,a) for a in normal)==tuple(Q(2) if i in marks else Q(1) for i in range(m))
    W=sum(sizes[a] for a in set(normal))
    O=sum(sizes)
    assert W==m+k and O==2*m-1
    return {'m':m,'marked_positions_zero_based':marks,'W_bank':str(W),'OPT_bank':str(O),'normal_order':normal,'exit_children':exits,'ordered_decision_histories_in_exit_children':states,'all_action_comparisons':checks,'maximum_forced_exit_payoff':str(worst_cap),'minimum_IC_margin':str(min_margin)}


if __name__=='__main__':
    records=[]
    for m in range(2,6):
        for k in range(1,m):
            for marks in combinations(range(m-1),k):
                records.append(audit(m,marks))
    summary={'scope':'all m=2,...,5; every nonempty marked subset excluding the last role; every forced action at every normal position; all later ordered histories and actions','bank_games':len(records),'exit_children':sum(r['exit_children'] for r in records),'ordered_decision_histories':sum(r['ordered_decision_histories_in_exit_children'] for r in records),'all_action_comparisons':sum(r['all_action_comparisons'] for r in records),'all_passed':True,'general_statement_proved_by':'heterogeneous_prefix_repair.md, Sections 2-5','records':records}
    Path(__file__).with_suffix('.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps({k:v for k,v in summary.items() if k!='records'}))
