"""Reuse the saved 381-customer SPE to check aggregate strong extra-slot debt.

No discovery optimization and no model/verifier import. The raw saved witness
is read; every ordered-history deviation is recomputed as Fraction. The new
observation concerns a stronger proposed intermediate bound, not FTA or half.
"""
import itertools,json,pathlib
from fractions import Fraction as F

ROOT=pathlib.Path(__file__).resolve().parents[6]
HERE=pathlib.Path(__file__).resolve().parent
SOURCE=ROOT/'research/workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/representation/terminal_pushforward_D_lt_C_exact.json'

def main():
    o=json.loads(SOURCE.read_text());m=o['players'];k=len(o['topics'])
    p=list(map(F,o['query_probability']))
    acts={tuple(r['history']):r['action'] for r in o['certificate']['actions']}
    customers=[r['mask'] for r in o['customer_types'] for _ in range(r['multiplicity'])]
    def end(h):
        while len(h)<m:h=h+(acts[h],)
        return h
    def utility(t,z,extra=0):
        return sum((F(1,extra+sum(bool(c&(1<<a)) for a in z))
            for c in customers if c&(1<<t)),F())
    comparisons=0;minimum=None
    for depth in range(m):
        for h in itertools.product(range(k),repeat=depth):
            own=utility(acts[h],end(h))
            for a in range(k):
                slack=own-utility(a,end(h+(a,)))
                assert slack>=0
                comparisons+=1
                minimum=slack if minimum is None else min(minimum,slack)
    z=end(());rows=[]
    for i in range(m):
        Z=[end(z[:i]+(a,)) for a in range(k)]
        D=sum((p[a]*utility(a,Z[a]) for a in range(k)),F())
        Cplus=sum((p[t]*p[a]*utility(t,Z[a],1)
            for t,a in itertools.product(range(k),repeat=2)),F())
        u=utility(z[i],z)
        rows.append({'position':i+1,'u':str(u),'D':str(D),'Cplus':str(Cplus),
            'delta':str(D-Cplus),'e':str(u-D)})
    W=sum((utility(a,z) for a in z),F())
    Ctotal=sum((F(r['Cplus']) for r in rows),F())
    delta=sum((F(r['delta']) for r in rows),F())
    assert delta==F(-657,400)
    assert W-Ctotal>0
    out={'source':str(SOURCE.relative_to(ROOT)),'kind':'OLD_INPUT_NEW_AGGREGATE_STRONG_CONSEQUENCE',
        'scope':'negates sum_i(D_i-Cplus_i)>=0 only; not FTA, Mpath, Mfull, security, or half',
        'customers':len(customers),'full_ordered_histories':len(acts),'comparisons_including_own':comparisons,
        'min_spe_slack':str(minimum),'actual_path':list(z),'p':list(map(str,p)),
        'rows':rows,'sum_delta':str(delta),'W':str(W),'sum_Cplus':str(Ctotal),'weak_budget_slack':str(W-Ctotal)}
    (HERE/'aggregate_strong_reuse_audit.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))

if __name__=='__main__':main()
