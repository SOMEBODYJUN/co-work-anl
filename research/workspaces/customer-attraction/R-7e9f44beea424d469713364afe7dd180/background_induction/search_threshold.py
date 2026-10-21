from search_background import *
from itertools import product
rng=random.Random(104818)
for trial in range(1000):
    q,r=5,4
    weights={mask:rng.randrange(1,7) for mask in rng.sample(range(1,1<<q),rng.randrange(5,20))}
    sol=BackgroundSolver(q,r,[0]*q,weights)
    bad=[]
    for c,theta in sol.thresholds.items():
        if sum(c)==r-1:continue
        for a in range(q):
            d=list(c);d[a]+=1;d=tuple(d)
            if sol.thresholds[d]<theta:
                # admissible root-current transition along some pure SPE from c
                child=sol.solve(d); ok=False
                while child:
                    bit=child&-child;i=bit.bit_length()-1;child-=bit
                    if sol.pays[i][a]>=theta:ok=True;break
                if ok:bad.append((c,a,theta,sol.thresholds[d]))
    if bad:
        obj={'trial':trial,'q':q,'r':r,'weights':weights,'bad':bad,'scale':sol.scale}
        (ROOT/'threshold_monotonicity_counterexample.json').write_text(json.dumps(obj,indent=2));print(obj);break
else: print('none')
