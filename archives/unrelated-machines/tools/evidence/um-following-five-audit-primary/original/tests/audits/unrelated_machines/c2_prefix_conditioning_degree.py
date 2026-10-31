#!/usr/bin/env python3
"""四阶真实one-hot矩的前缀负载不可识别；实际全机器负载审计。"""
from itertools import product, combinations
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import platform


def audit():
    bits = {r:[b for b in product((0,1),repeat=5) if sum(b)%2==r] for r in (0,1)}
    # Machines A=0,B=1,C=2. Every job has at least one finite edge.
    P = [[F(0)]*4+[F(1),F(0),None],
         [F(0)]*4+[F(1),F(0),None],
         [None]*6+[F(2)]]
    schedules = {r:[tuple(0 if b[j] else 1 for j in range(4))+
                      (1 if b[4] else 0,0,2) for b in bits[r]] for r in (0,1)}
    E = [(i,j) for i in range(3) for j in range(7) if P[i][j] is not None]
    moments = 0
    for degree in range(5):
        for S in combinations(E,degree):
            count = [sum(all(a[j]==i for i,j in S) for a in schedules[r]) for r in (0,1)]
            assert count[0] == count[1]
            moments += 1
    loads = {}
    conditional = []
    for r in (0,1):
        loads[r] = []
        for a in schedules[r]:
            ls = [sum((P[i][j] for j in range(7) if a[j]==i),F(0)) for i in range(3)]
            assert max(ls) == 2  # anchor gives OPT>=2; every support attains2.
            loads[r].append(ls)
        indices = [k for k,a in enumerate(schedules[r]) if a[:4]==(0,0,0,0)]
        assert len(indices)==1
        conditional.append(sum((loads[r][k][1] for k in indices),F(0))/len(indices))
    assert conditional == [F(0),F(1)]
    # Old witness had TWO complementary jobs, each3/2, hence full B always3/2.
    old_full_B = []
    for r in (0,1):
        chosen = [b for b in bits[r] if all(b[:4])]
        old_full_B.append(sum((F(3,2)*b[4]+F(3,2)*(1-b[4]) for b in chosen),F(0))/len(chosen))
    assert old_full_B == [F(3,2),F(3,2)]
    return {'python':platform.python_version(),'arithmetic':'fractions.Fraction',
            'support_sizes':[len(schedules[r]) for r in (0,1)],
            'legal_endpoint_count':len(E),'all_endpoint_subsets_degree_le4':moments,
            'prefix_probability':'1/16','conditional_FULL_B_loads':list(map(str,conditional)),
            'old_witness_FULL_B_loads':list(map(str,old_full_B)),
            'true_OPT':'2','code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'scope':'source-specific information boundary; no algorithmic impossibility'}


if __name__=='__main__':
    print(json.dumps(audit(),ensure_ascii=False,indent=2))
