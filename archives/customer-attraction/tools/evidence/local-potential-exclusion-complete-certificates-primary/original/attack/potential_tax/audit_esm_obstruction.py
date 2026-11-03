"""Exact all-ordered-history audit of a finite ESM candidate obstruction.

Reads only weights and the explicit second/last action tables from discovery.
Does not import the discovery MILP or any SPE oracle.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product,combinations_with_replacement
from math import lcm,gcd
from functools import reduce
import json
HERE=Path(__file__).resolve().parent

def audit():
    discovery=json.loads((HERE/'milp_p5_target123_bempty.json').read_text())
    rationals=[F(w).limit_denominator(1000000) for w in discovery['weights']]
    denom=lcm(*(w.denominator for w in rationals));integer=[int(w*denom) for w in rationals]
    common=reduce(gcd,integer);integer=[w//common for w in integer]
    types=[(tuple(j for j,v in enumerate(t) if v),w) for t,w in zip(discovery['types'],integer) if w]
    p=5;m=3;B=discovery['second_actions'];C=discovery['last_actions']
    def action(h):return 0 if not h else B[h[0]] if len(h)==1 else C[h[0]][h[1]]
    def finish(h):
        h=tuple(h)
        while len(h)<m:h+=action(h),
        return h
    def utility(a,z):return sum(F(w,sum(t in members for t in z)) for members,w in types if a in members)
    def potential(z):return sum(w*sum((F(1,j) for j in range(1,sum(t in members for t in z)+1)),F(0)) for members,w in types)
    rows=[]
    for length in range(m):
        for h in product(range(p),repeat=length):
            actual=finish(h);i=length;u=utility(actual[i],actual)
            for a in range(p):
                deviated=finish(h+(a,));v=utility(a,deviated)
                rows.append({'history':list(h),'action':a,'actual_terminal':list(actual),
                    'deviation_terminal':list(deviated),'slack':str(u-v)})
                assert u>=v,(h,a,u,v)
    path=finish(());u=utility(path[0],path);safe=F(sum(w for members,w in types if 0 in members),3)
    profiles=list(combinations_with_replacement(range(p),m))
    P=max(map(potential,profiles));PA=max(potential(z) for z in profiles if 0 in z)
    E=P-PA;assert E>u-safe
    welfare=lambda z:sum(w for members,w in types if any(t in members for t in z))
    W=welfare(path);OPT=max(map(welfare,profiles))
    tax=F(0)
    local=[]
    for i,a in enumerate(path):
        past=path[:i];r=m-i
        f=sum(F(w,1+sum(t in past for t in members)) for members,w in types if a in members)
        s=sum(F(w,r+sum(t in past for t in members)) for members,w in types if a in members)
        pp=max(potential(past+q)-potential(past) for q in combinations_with_replacement(range(p),r))
        ppa=max(potential(past+q)-potential(past) for q in combinations_with_replacement(range(p),r) if a in q)
        margin=utility(a,path)-s-(pp-ppa)
        local.append({'position':i+1,'potential_forcing_loss':str(pp-ppa),'profit_minus_safe':str(utility(a,path)-s),'ESM_margin':str(margin)})
        tax+=f-s
    # Coverage sets are pairwise distinct, so this really is a set catalog.
    for a in range(p):
        for b in range(a):assert any((a in members)!=(b in members) for members,w in types)
    packet={'claim':'CA-POTENTIAL-EXCLUSION-SAFETY-MARGIN-CANDIDATE-v1 is FALSE already at r=3, b=0',
        'scope':'auxiliary ESM only; not a target half counterexample or a counterexample to the total potential/copy-tax candidate',
        'unit_customers':sum(integer),'players':3,'topics':['A','B','C','D','E'],
        'customers':[{'topics':members,'multiplicity':w} for members,w in types],
        'strategy':[{'history':h,'action':action(h)} for k in range(m) for h in product(range(p),repeat=k)],
        'root_action':0,'second_actions':B,'last_actions':C,'actual_path':path,
        'actual_payoffs':[str(utility(a,path)) for a in path],
        'full_histories':sum(p**j for j in range(m)),'full_IC_comparisons':len(rows),
        'minimum_IC_slack':str(min(F(r['slack']) for r in rows)),
        'P3':str(P),'P3_containing_actual_A':str(PA),'forcing_loss':str(E),
        'actual_root_profit':str(u),'root_safe_copy_floor':str(safe),'root_profit_surplus':str(u-safe),
        'ESM_violation':str(E-u+safe),'all_P3_maximizers':[z for z in profiles if potential(z)==P],
        'all_P3_A_maximizers':[z for z in profiles if 0 in z and potential(z)==PA],
        'W':W,'OPT3':OPT,'tax':str(tax),'W_plus_tax_minus_P3':str(W+tax-P),
        'local_ESM_margins':local,'IC_rows':rows}
    (HERE/'esm_exact_obstruction.json').write_text(json.dumps(packet,indent=2)+'\n')
    print(json.dumps({k:v for k,v in packet.items() if k not in ['IC_rows','customers','last_actions']},indent=2))
    return packet
if __name__=='__main__':audit()
