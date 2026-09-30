#!/usr/bin/env python3
"""Direct certificates and subset checks for the four-seed R-menu option."""
import json
import random
from pathlib import Path
from fractions import Fraction as Q
from r_menu_solver import solve,make_menu,verify,serial


def main():
    rng=random.Random(429031)
    counts={'seed':429031,'random_instances':0,'directed_instances':0,
            'full_and_four_seed_certificate_checks':0,'pair_subset_checks':0,
            'six_or_longer_cycles':0,'max_four_seed_menu_entries':0}
    def check(case,compare_pairs=False):
        full=solve(case,maximum_only=False);four=solve(case)
        verify(case,full);verify(case,json.loads(json.dumps(serial(four))))
        counts['full_and_four_seed_certificate_checks']+=2
        counts['six_or_longer_cycles']+=len(four['response_cycle'])>=6
        if compare_pairs:
            weights=list(map(Q,case['weights']));sites=list(map(set,case['locations']))
            for s in case['U1']:
                for t in case['U2']:
                    mfull=make_menu(weights,sites,s,t,maximum_only=False)
                    mfour=make_menu(weights,sites,s,t)
                    assert {tuple(r['prob_first']) for r in mfour['entries']}<={tuple(r['prob_first']) for r in mfull['entries']}
                    counts['pair_subset_checks']+=1
                    counts['max_four_seed_menu_entries']=max(counts['max_four_seed_menu_entries'],len(mfour['entries']))
    # This asymmetric private base retains three distinct four-seed witnesses.
    directed=[
        {'weights':['10','6','3','9'],'locations':[[0,1,2],[0,1,2,3]],'U1':[0],'U2':[1]},
        {'weights':['10','10','3','9'],'locations':[[0,1,2],[0,1,2,3],[],[1,2]],'U1':[0,1],'U2':[0,2,3]},
        {'weights':[],'locations':[[],[]],'U1':[0,1],'U2':[0,1]},
    ]
    for case in directed:
        check(case,True);counts['directed_instances']+=1
    for number in range(1200):
        a=rng.randint(1,7);b=rng.randint(1,7);n=rng.randint(0,14)
        weights=[str(Q(rng.randint(1,40),rng.randint(1,13))) for _ in range(n)]
        sites=[[i for i in range(n) if rng.random()<.5] for _ in range(a+b)]
        case={'weights':weights,'locations':sites,'U1':list(range(a)),'U2':list(range(a,a+b))}
        check(case,number<120);counts['random_instances']+=1
    Path(__file__).with_name('four_seed_verification.json').write_text(json.dumps(counts,indent=2)+'\n')
    print(json.dumps(counts,indent=2))


if __name__=='__main__':
    main()
