from fractions import Fraction as Q
from pathlib import Path
import json

def u(d):return min(2*d[0]+Q(3,2)*d[2],2*d[1]+Q(3,2)*d[2])
old=(Q(1,4),Q(1,4),Q(1,2));new=(Q(0),Q(0),Q(1))
assert u(old)==Q(5,4) and u(new)==Q(3,2)
checks=0
for player in [0,1]:
    fixed=list(old);fixed[player]-=Q(1,4)
    # All simplex grid points with unit 1/400 and total budget 1/4.
    for a in range(101):
        for b in range(101-a):
            z=(Q(a,400),Q(b,400),Q(100-a-b,400))
            assert u(tuple(fixed[j]+z[j] for j in range(3)))<=u(old)
            checks+=1
out=dict(old_total=[str(t) for t in old],old_utility=str(u(old)),merged_deviation_total=[str(t) for t in new],merged_utility=str(u(new)),finite_strategy_checks=checks,exact_full_best_response_certificate='For clone a, active first linear branch coefficient max is 2 at its current project. For b, use second branch. See CLONING_AND_SEPARABLE_TOYS.md.')
print(json.dumps(out,indent=2))
Path(__file__).with_name('cloning_certificate.json').write_text(json.dumps(out,indent=2))
