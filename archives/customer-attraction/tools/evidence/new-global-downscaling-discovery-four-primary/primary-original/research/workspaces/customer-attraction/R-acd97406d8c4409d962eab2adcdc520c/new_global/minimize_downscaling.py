import json,random
from customer_attraction.model import Instance,CustomerType
from customer_attraction.exact import ExactSPESolver
path='research/workspaces/customer-attraction/R-acd97406d8c4409d962eab2adcdc520c/new_global/'
d=json.load(open(path+'downscaling_candidate.json'));q=tuple(d['target']);n=4
raw={sum(1<<a for a in c['topics']):c['multiplicity']//2 for c in d['original']['customers']}
covered=lambda mask:any(q[a] and mask>>a&1 for a in range(n))
def inst(w,t):
 return Instance(tuple(map(str,range(n))),tuple(CustomerType(frozenset(a for a in range(n) if mask>>a&1),v*(2 if covered(mask) else t)) for mask,v in w.items() if v and (covered(mask) or t)),3)
def okay(w):
 return all((q in ExactSPESolver(inst(w,t)).outcomes())==want for t,want in [(2,True),(1,False),(0,True)])
assert okay(raw)
rng=random.Random(1554)
while True:
 changed=False;keys=list(raw);rng.shuffle(keys)
 for k in keys:
  while raw[k]:
   raw[k]-=1
   if okay(raw): changed=True
   else:raw[k]+=1;break
 if not changed:break
raw={k:v for k,v in raw.items() if v}
base=inst(raw,2); small=inst(raw,1);zero=inst(raw,0)
s=ExactSPESolver(base)
out={'purpose':'auxiliary nonmonotone SPE-outcome survival under scaling missed customers','target':q,'raw':raw,'original':base.to_dict(),'scaled':small.to_dict(),'zero':zero.to_dict(),'original_certificate':s.certificate(q).to_dict(),'zero_certificate':ExactSPESolver(zero).certificate(q).to_dict(),'scaled_outcomes':[list(x) for x in sorted(ExactSPESolver(small).outcomes())]}
print(json.dumps(out,indent=2))
