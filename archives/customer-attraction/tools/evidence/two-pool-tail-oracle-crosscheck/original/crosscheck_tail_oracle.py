"""Cross-check the vectorized three-mover oracle against the canonical solver."""
from pathlib import Path
from fractions import Fraction
import json
import random
import sys
ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT))
from customer_attraction import CustomerType, Instance, ExactSPESolver
from two_pool_tail_search import coefficient_tables,test_parameters


def instance(pars,old=3):
    x,a,b1,d1,b2,d2=pars
    k=old+1
    topics=tuple(f'{kind}{i}' for i in range(k) for kind in ('A','B1','B2','C'))+('D1','D2')
    types=[]
    for i in range(k):
        types.extend((CustomerType(frozenset(range(4*i,4*i+4)),x),
                      CustomerType(frozenset({4*i}),a)))
    for r,(b,d) in enumerate(((b1,d1),(b2,d2))):
        if b: types.append(CustomerType(frozenset([4*i+1+r for i in range(k)]+[4*k+r]),b))
        if d: types.append(CustomerType(frozenset({4*k+r}),d))
    return Instance(topics,tuple(types),old+3)


def main():
    rng=random.Random(104729)
    pars=[(6,3,3,3,3,3),(6,4,5,2,5,2),(6,4,5,2,4,3),
          (6,4,12,2,4,3)]
    pars += [(6,4,*[rng.randrange(19) for _ in range(4)]) for _ in range(8)]
    tables=coefficient_tables(3)
    ok,floor,tail=test_parameters(pars,tables)
    results=[]
    for i,par in enumerate(pars):
        game=instance(par)
        solver=ExactSPESolver(game)
        prefix=tuple(4*j+3 for j in range(3))
        counts=game.counts(prefix)
        threshold=solver.threshold(counts)
        assert threshold==Fraction(int(floor[i]),12),(par,threshold,floor[i])
        path=prefix+(15,16,17)
        target=game.counts(path,terminal=True)
        child=game.counts(prefix+(15,))
        last_prefix=game.counts(prefix+(15,16))
        tail_exact=(target in solver.outcomes(last_prefix)
                    and game.topic_payoff(16,target)>=solver.threshold(child))
        assert tail_exact==bool(tail[i])
        path_supported=tail_exact and threshold<=6
        assert path_supported==bool(ok[i])
        row={'parameters':par,'canonical_threshold':str(threshold),
             'vectorized_threshold':str(Fraction(int(floor[i]),12)),
             'target_D1_D2_tail_supported':tail_exact,
             'target_C_D1_D2_path_supported':path_supported,
             'canonical_count_states':solver.stats.count_states}
        results.append(row)
        print(par,threshold,path_supported,flush=True)
    output={'seed':104729,'samples':results,'all_exact_checks_passed':True,
            'scope':'tail oracle cross-check only; no full initial-game certificate'}
    Path(__file__).with_name('tail_oracle_crosscheck.json').write_text(json.dumps(output,indent=2)+'\n')


if __name__=='__main__':main()
