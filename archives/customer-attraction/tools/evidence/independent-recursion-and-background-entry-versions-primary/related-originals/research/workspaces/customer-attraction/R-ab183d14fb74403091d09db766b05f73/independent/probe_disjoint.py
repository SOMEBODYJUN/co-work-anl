import random,json,sys,time
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[5]))
from customer_attraction import Instance,ExactSPESolver
rng=random.Random(9475)
for n in range(2000):
    m=3; q=6
    bases=[]; c=0
    for j in range(m):
        sz=rng.randrange(1,7); bases.append(set(range(c,c+sz)));c+=sz
    N=list(range(c+rng.randrange(0,6)))
    sets=bases+[set(x for x in N if rng.random()<rng.choice([.2,.4,.6,.8])) for _ in range(q-m)]
    ins=Instance.from_topic_sets(sets,m)
    sol=ExactSPESolver(ins)
    tar=(1,)*m+(0,)*(q-m)
    if tar not in sol.outcomes():continue
    for h in sol.ordered_outcomes(target_counts=tar):
        u=ins.player_payoffs(h)
        if any(2*u[i]<u[-1] for i in range(m-1)):
            cert=sol.certificate(on_path=h)
            out={'instance':ins.to_dict(),'sets':[sorted(x) for x in sets],'path':h,'u':[str(x) for x in u],'certificate':cert.to_dict()}
            Path(__file__).with_name('disjoint_low_early.json').write_text(json.dumps(out,indent=2))
            print('FOUND',n,h,[str(x) for x in u],flush=True);raise SystemExit
    if n%100==0:print('step',n,flush=True)
print('none')
