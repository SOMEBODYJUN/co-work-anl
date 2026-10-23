"""Independent unit-level audit of the announced maximum-potential obstruction.
Only the announced types and previously independently reconstructed strategy are used.
"""
import json
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import audit_integer_push_34 as model

TYPES={1:12,2:109,4:3,9:86,12:60,16:109,19:18,21:27,22:3,
       26:27,29:36,33:48,36:82,42:36,43:36,45:9,46:36,51:9,53:45}
model.UNITS=[frozenset(a for a in range(6) if mask>>a&1)
             for mask,n in TYPES.items() for _ in range(n)]
model.S=[frozenset(x for x,t in enumerate(model.UNITS) if a in t) for a in range(7)]

def potential(z):
    return sum((sum((F(1,j) for j in range(1,1+sum(x in model.S[a] for a in z))),F(0))
                for x in range(len(model.UNITS))),F(0))

def insert(a,z):
    return sum((F(1,1+sum(x in model.S[b] for b in z)) for x in model.S[a]),F(0))

def main():
    branches={a:model.finish((a,)) for a in range(7)}
    gaps=[]
    for i in range(3):
        for h in product(range(7),repeat=i):
            original=model.pay(model.finish(h),i)
            for a in range(7):
                gap=original-model.pay(model.finish(h+(a,)),i)
                assert gap>=0,(h,a,gap)
                gaps.append(gap)
    actual=model.finish(())
    u=model.pay(actual,0)
    phis={a:potential(z) for a,z in branches.items()}
    ka_b=insert(2,branches[4])
    assert len(model.UNITS)==791 and actual==(0,3,4)
    assert [model.pay(actual,i) for i in range(3)]==[F(187),F(223),F(187)]
    assert ka_b==F(409,2)>u
    assert phis[2]==phis[4]==F(1511,2)==max(phis.values())
    result={'status':'PASS','customers':len(model.UNITS),'players':3,'topics':7,
      'decision_nodes':57,'comparisons_including_self':len(gaps),'true_deviations':342,
      'minimum_gap':str(min(gaps)),'actual_path':actual,
      'actual_payoffs':[str(model.pay(actual,i)) for i in range(3)],
      'W':len(set().union(*(model.S[a] for a in actual))),
      'root_terminal_branches':{str(a):z for a,z in branches.items()},
      'root_branch_payoffs':{str(a):str(model.pay(z,0)) for a,z in branches.items()},
      'potential':{str(a):str(phi) for a,phi in phis.items()},
      'maximum_potential_columns':[a for a,phi in phis.items() if phi==max(phis.values())],
      'bad_query':2,'bad_column':4,'K_bad':str(ka_b),'u':str(u),'K_minus_u':str(ka_b-u),
      'query_matrix':{str(a):[str(insert(a,branches[b])) for b in range(7)] for a in range(7)}}
    Path(__file__).with_name('phi_rise_independent_audit.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('status','customers','comparisons_including_self','W','actual_payoffs','K_bad','u','K_minus_u','maximum_potential_columns','potential')}))

if __name__=='__main__':main()
