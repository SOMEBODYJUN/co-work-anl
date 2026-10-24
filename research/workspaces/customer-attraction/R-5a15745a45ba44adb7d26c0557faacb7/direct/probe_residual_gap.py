"""Attack precise general candidate u_i >= f_U(r)-f_U(r-1).
Finite targeted counterexample search only; no positive theorem inference.
"""
import json, random, itertools, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT))
from customer_attraction import Instance, CustomerType, ExactSPESolver
rng=random.Random(15241)
for trial in range(int(sys.argv[1]) if len(sys.argv)>1 else 1000):
    m=3;k=7
    cs=[]
    # U types only on five query themes; two possible actual outside themes.
    for mask in range(1,1<<5):
        if rng.random()<.24:
            cs.append(CustomerType(frozenset(j+2 for j in range(5) if mask>>j&1),rng.randint(1,9)))
    # C types can involve the actual themes as well as query themes.
    for a in range(2):
        for qmask in range(1<<5):
            if rng.random()<.14:
                topics={a}|{j+2 for j in range(5) if qmask>>j&1}
                if rng.random()<.2:topics.add(1-a)
                cs.append(CustomerType(frozenset(topics),rng.randint(1,9)))
    ins=Instance(tuple(map(str,range(k))),tuple(cs),m)
    solver=ExactSPESolver(ins)
    for target in solver.outcomes():
        # Only actual paths on the designated outside themes.
        if any(target[2:]):continue
        U=[c for c in cs if not any(target[t] for t in c.topics)]
        f=[max((sum(c.multiplicity for c in U if c.topics&set(A)) for A in itertools.combinations(range(k),r)),default=0) for r in range(m+1)]
        for path in solver.ordered_outcomes(target):
            us=ins.player_payoffs(path)
            for i,u in enumerate(us):
                gap=f[m-i]-f[m-i-1]
                if u<gap:
                    cert=solver.certificate(on_path=path)
                    out={'candidate':'residual-optimum gap current floor','trial':trial,'instance':ins.to_dict(),'path':path,'payoffs':list(map(str,us)),'f':f,'bad_position':i+1,'gap':gap,'strategy':cert.to_dict()}
                    dest=Path(__file__).with_name('residual_gap_failure.json');dest.write_text(json.dumps(out,indent=2))
                    print('FOUND',dest,trial,path,list(map(str,us)),f,i+1);raise SystemExit
    if trial%100==0:print('trial',trial,flush=True)
print('NO COUNTEREXAMPLE IN FINITE PROBE')
