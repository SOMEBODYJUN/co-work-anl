"""Materialize legal NEW instances from the non-SPE obstruction.

Theme unions and omissions change the game; no old IC or ratio is retained.
JSONs use the repository Instance schema and six unit players.
"""
from collections import defaultdict
from fractions import Fraction as F
from math import gcd,lcm
from pathlib import Path
import json


def main():
    root=Path(__file__).parent
    data=json.loads((root/'potential_menu_joint.json').read_text())
    types=[(t,F(v)) for t,v in data['positive_types']]
    scale=lcm(*(v.denominator*6 for t,v in types))
    original=[]
    for (mask,d,ell,h),mass in types:
        assert d==1
        for owner in range(6):
            reply=0 if ell==0 else (1<<owner if ell==1 else (63^(1<<owner) if ell==5 else 63))
            interest={i for i in range(6) if mask>>i&1}|{6+owner}|{12+i for i in range(6) if reply>>i&1}
            original.append((interest,int(mass*scale/6)))
    def write(name,groups):
        counts=defaultdict(int)
        for interest,mass in original:
            new=tuple(i for i,g in enumerate(groups) if interest.intersection(g))
            if new:counts[new]+=mass
        divisor=gcd(*counts.values())
        out={'players':6,'topics':['U'+str(i) for i in range(len(groups))],
             'customers':[{'topics':list(k),'multiplicity':v//divisor} for k,v in sorted(counts.items())],
             '_scope':'NEW instance for true SPE target attack; no old obstruction ratio/IC retained',
             '_source_groups':groups}
        (root/(name+'.json')).write_text(json.dumps(out,indent=2)+'\n')
        return {'name':name,'topics':len(groups),'types':len(counts),'customers':sum(counts.values())//divisor}
    records=[]
    records.append(write('seed_full18',[[i] for i in range(18)]))
    records.append(write('seed_union8',[[2],[3],[4],[5],[6,7,8],[9,10,11],[12,13,14],[15,16,17]]))
    records.append(write('seed_reply_representatives8',[[2],[3],[4],[5],[6,7,8],[9,10,11],[12],[15]]))
    records.append(write('seed_union_actual8',[[0,1],[2,3],[4],[5],[6,7,8],[9,10,11],[12,13,14],[15,16,17]]))
    (root/'target_attack_seed_index.json').write_text(json.dumps(records,indent=2)+'\n')
    print(json.dumps(records,indent=2))


if __name__=='__main__':main()
