"""Definition-level check of ASD/VR on one frozen complete SPE witness.

No discovery scan; does not import the theorem author's or SPE solver code.
Each removed action is taken from the true original forced branch, including
the branch-dependent virtual action when its original position is later.
"""
from fractions import Fraction as F
from hashlib import sha256
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent/'dynamic_exchange'
game_path=SOURCE/'assignment_instance.json'
policy_path=SOURCE/'assignment_full_policy.json'
game=json.loads(game_path.read_text())
raw=json.loads(policy_path.read_text())
policy={tuple(map(int,k.split(','))) if k else ():v
        for k,v in raw['policy'].items()}
clients=[]
for kind in game['customers']:
    clients.extend([frozenset(kind['topics'])]*kind['multiplicity'])
m=game['players']
labels=range(len(game['topics']))

def finish(h):
    while len(h)<m:
        h=h+(policy[h],)
    return h

def utility(z,j,remove=None):
    return sum((F(1,sum(a in x for k,a in enumerate(z) if k!=remove))
                for x in clients if z[j] in x),F())

z=finish(())
c=[sum(a in x for a in z) for x in clients]
b=[[sum(a in x for a in z[:j]) for x in clients] for j in range(m)]
u=[utility(z,j) for j in range(m)]
W=sum(v>0 for v in c)
D=sum(v>=2 for v in c)
allregret=F()
late=F()
refund_late=F()
refund_all=F()
mixed=F()
ksum=F()
rows=[]
for i in range(m):
    for j in range(m):
        if i==j:
            continue
        baseline=utility(z,j,remove=i)
        gains=[utility(finish(z[:j]+(a,)),j,remove=i)-baseline for a in labels]
        regret=max(F(),*gains)
        refund=sum((F(1,load*(load-1)) for x,load in zip(clients,c)
                    if z[i] in x and z[j] in x),F())
        assert regret<=u[j]-refund
        refund_all+=refund
        allregret+=regret
        row={'removed':i+1,'survivor':j+1,'regret':str(regret),'refund':str(refund)}
        if i<j:
            envelope=sum((F(1,past*(past+1)) for x,past in zip(clients,b[j])
                          if z[i] in x),F())
            assert regret<=envelope-refund
            assert regret+refund<=min(u[j],envelope)
            mixed+=min(u[j],envelope)
            ksum+=envelope
            late+=regret
            refund_late+=refund
            row['prefix_envelope']=str(envelope)
        rows.append(row)
price=sum((F(1,past+1) for bg in b for past in bg if past>0),F())
assert ksum==price
assert refund_late==F(D,2)
assert refund_all==D
assert late+F(D,2)<=mixed<=price
assert late<=F((m-1)*W-D,2)
earlier=sum((F(m-1-j)*u[j] for j in range(m)),F())
vr=mixed+earlier-D
assert allregret<=vr<=(m-1)*W-D
report={
    'status':'PASS; exact definition replay of ASD/VR, not a general proof',
    'source_sha256':{p.name:sha256(p.read_bytes()).hexdigest() for p in (game_path,policy_path)},
    'actual':z,'W':W,'D':D,'pair_rows':rows,
    'suffix_regret_sum':str(late),'suffix_refund_sum':str(refund_late),
    'sum_K':str(ksum),'prefix_price_sum':str(price),
    'sum_min_u_K':str(mixed),'whole_virtual_actual_regret_sum':str(allregret),
    'whole_virtual_bound_VR':str(vr)
}
print(json.dumps(report,ensure_ascii=False,indent=2))
if __name__=='__main__':
    import sys
    if '--freeze' in sys.argv:
        (HERE/'suffix_deletion_audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
