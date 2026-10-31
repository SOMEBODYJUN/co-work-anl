import json
from fractions import Fraction
from itertools import product
p='/workspace/scratch/3b26e30034a3/co-work-anl/archives/customer-attraction/tools/evidence/collision-free/audit_collision_free_occupancy.json'
x=json.load(open(p))
t=[set(v) for v in x['topics']]
f=tuple(x['follower']); root=x['root']
def u(path,i):
 return sum((Fraction(1,sum(v in t[a] for a in path)) for v in t[path[i]]), Fraction())
def finish(h):
 if len(h)==0:return (root,f[root])
 if len(h)==1:return (h[0],f[h[0]])
 return h
sl=[]
for a in range(4):
 vals=[u((a,b),1) for b in range(4)]
 assert vals[f[a]]==max(vals)
 sl.extend(vals[f[a]]-v for v in vals)
vals=[u(finish((a,)),0) for a in range(4)]
assert vals[root]==max(vals)
sl.extend(vals[root]-v for v in vals)
actual=finish(())
loads=[sum(i in t[a] for a in actual) for i in range(5)]
assert all(c<=1 for c in loads)
opt=max(len(set().union(*(t[a] for a in path))) for path in product(range(4),repeat=2))
assert opt==x['OPT']==5
assert len(set().union(*(t[a] for a in actual)))==x['W']==4
assert min(sl)==0 and sum(s>0 for s in sl)==9
print(json.dumps({'status':'pass','histories':5,'comparisons':20,'nonself':15,'strict':9,'min_slack':'0','W':4,'OPT':5,'actual':actual,'loads':loads},indent=2))
