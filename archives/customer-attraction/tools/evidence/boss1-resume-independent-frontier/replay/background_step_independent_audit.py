"""Independent exact audit of the all-A background-profit step obstruction."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json

OUT=Path(__file__).parent

def independent_f(r):
    # Select k copies of A and fill remaining r-1 seats by distinct singletons.
    choices=[F(r*k,k+1)+r-1-k for k in range(r)]
    return max(choices),[k for k,x in enumerate(choices) if x==max(choices)]

def all_history_audit(r):
    # Topic0 A contains r unit customers; each topicj>0 a private unit customer.
    topics=[frozenset(range(r))]+[frozenset({r+j}) for j in range(r-1)]
    def utility(path,i):
        return sum((F(1,sum(x in topics[a] for a in path)) for x in topics[path[i]]),F(0))
    nodes=0; comparisons=0
    for t in range(r):
        for h in product(range(r),repeat=t):
            baseline=h+(0,)*(r-t)
            value=utility(baseline,t)
            assert value>=1
            for a in range(r):
                alternative=h+(a,)+(0,)*(r-t-1)
                assert utility(alternative,t)<=value
                comparisons+=1
            nodes+=1
    return {'r':r,'nodes':nodes,'comparisons':comparisons,'all_valid':True}

def run():
    entries=[]
    for r in range(1,101):
        val,ks=independent_f(r)
        expected=2*r-min(F(j)+F(r,j) for j in range(1,r+1))
        assert val==expected
        entries.append({'r':r,'F_root':2*r-1,'F_child':str(val),'maximizing_k':ks,
                        'delta':str(F(2*r-1)-val),'actual_first_payoff':1})
    squares=[]
    for q in range(1,31):
        r=q*q
        val,ks=independent_f(r)
        assert val==2*r-2*q
        assert ks==[q-1]
        assert F(2*r-1)-val==2*q-1
        squares.append({'q':q,'r':r,'F_child':int(val),'delta':2*q-1,'unique_k':q-1})
    result={'all_history_SPE_checks':[all_history_audit(r) for r in range(1,6)],
            'integer_r_formula_checks':entries,'square_formula_checks':squares,
            'scope':'Finite arithmetic cross-checks only; the all-r proof is in the independent review.'}
    (OUT/'background_step_independent_audit.json').write_text(json.dumps(result,indent=2))
    print(json.dumps({'all_history_SPE_checks':result['all_history_SPE_checks'],
                      'r1':entries[0],'r2':entries[1],'sample_squares':squares[:5],
                      'formula_checks':len(entries),'square_checks':len(squares)},indent=2))

if __name__=='__main__': run()
