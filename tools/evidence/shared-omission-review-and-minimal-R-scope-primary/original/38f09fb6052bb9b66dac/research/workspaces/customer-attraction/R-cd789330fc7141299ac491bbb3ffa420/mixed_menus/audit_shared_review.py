"""Independent direct-terminal checks for the shared-omission family/review.

Does not import author code, the canonical model, BI, or an optimizer.
"""
from fractions import Fraction as F
from itertools import product, combinations_with_replacement
from pathlib import Path
import json


def utility(covers, background, path, position):
    chosen = covers[path[position]]
    return sum((F(1, background[x]+sum(x in covers[a] for a in path))
                for x in chosen), F())


def constant_is_spe(covers, background, remaining):
    checks = 0
    for elapsed in range(remaining):
        for past in product(range(len(covers)), repeat=elapsed):
            truth = past+(0,)*(remaining-elapsed)
            obey = utility(covers, background, truth, elapsed)
            for action in range(len(covers)):
                branch = past+(action,)+(0,)*(remaining-elapsed-1)
                checks += 1
                if obey < utility(covers, background, branch, elapsed):
                    return False, checks
    return True, checks


def criterion_checks():
    all_sets = [frozenset(i for i in range(3) if mask & (1 << i))
                for mask in range(8)]
    cases = checks = true_cases = false_cases = 0
    for bank in all_sets:
        for other in all_sets:
            covers = (bank,) if bank == other else (bank, other)
            for background in product(range(3), repeat=3):
                for remaining in range(1,4):
                    condition = all(
                        sum((F(1, background[x]+remaining) for x in bank-t), F())
                        >= sum((F(1, background[x]+1) for x in t-bank), F())
                        for t in covers)
                    spe, count = constant_is_spe(covers, background, remaining)
                    assert condition == spe
                    cases += 1
                    checks += count
                    true_cases += spe
                    false_cases += not spe
    return dict(cases=cases, direct_deviation_checks=checks,
                passing_conditions=true_cases, failing_conditions=false_cases,
                domain='Every ordered pair of subsets of 3 customers, all backgrounds in {0,1,2}^3, r=1,2,3; includes empty/zero sets. Background audit is a superset of legal-prefix backgrounds.')


def family(m,a):
    bank = frozenset(range(m*a+1))
    covers = [bank]
    for j in range(m-1):
        outside = frozenset(range(len(bank)+j*a,len(bank)+(j+1)*a))
        covers += [outside|{0}, outside|{1}]
    covers = tuple(covers)
    clients = frozenset().union(*covers)
    background = [0]*len(clients)
    spe, count = constant_is_spe(covers, background, m)
    assert spe
    assert len(set(covers)) == 2*m-1
    assert all(not s < t for s in covers for t in covers)
    omitted = clients-bank
    assert len(omitted) == (m-1)*a
    assert all(sum(x in s for s in covers) == 2 for x in omitted)
    optimum = max(len(frozenset().union(*(covers[j] for j in choices)))
                  for choices in combinations_with_replacement(range(len(covers)),m))
    assert optimum == len(clients) == (2*m-1)*a+1
    assert len(bank) == m*a+1
    assert F(optimum,len(bank)) == 2-F(1,m)-F(m-1,m*(m*a+1))
    return dict(players=m,block_size=a,topics=len(covers),
                clients=len(clients),welfare=len(bank),optimum=optimum,
                ratio=str(F(optimum,len(bank))),
                ordered_histories=sum(len(covers)**j for j in range(m)),
                direct_deviation_checks=count)


if __name__ == '__main__':
    report = dict(status='Independent definition-level finite checks passed; general statements rely on analytic proof.',
                  background_criterion=criterion_checks(),
                  shared_families=[family(m,a) for m,a in ((2,1),(3,2),(4,1),(5,1))])
    Path(__file__).with_name('shared_review_audit.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
