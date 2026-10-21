"""Fixed full-history policy cones; floating discovery only."""
from pathlib import Path
from itertools import product
import sys, json, random
import numpy as np
from scipy.optimize import linprog
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[4]
sys.path.insert(0,str(ROOT))
sys.path.insert(0,str(HERE))
from customer_attraction import Instance, ExactSPESolver
from pair_security_probe import Probe

def get_policy(probe,w,rng):
    instance={"topics":[str(a) for a in range(probe.p)],"players":probe.r,
              "customers":[{"topics":list(B),"multiplicity":int(v)}
                           for B,v in zip(probe.types,w) if v]}
    ins=Instance.from_dict(instance)
    solver=ExactSPESolver(ins)
    q=rng.choice(tuple(sorted(solver.outcomes())))
    h=rng.choice(tuple(solver.ordered_outcomes(q)))
    cert=solver.certificate(on_path=h,
             action_selector=lambda history,candidates:rng.choice(candidates),
             continuation_selector=lambda history,candidates:rng.choice(candidates))
    return cert.actions

def cone_data(probe,policy):
    def terminal(h):
        while len(h)<probe.r: h=h+(policy[h],)
        q=tuple(h.count(a) for a in range(probe.p))
        return h,probe.index[q]
    root_h,root_i=terminal(())
    gamma=[]
    for h,a in policy.items():
        _,qi=terminal(h)
        for b in range(probe.p):
            _,qj=terminal(h+(b,))
            gamma.append(probe.forms[qi,a]-probe.forms[qj,b])
    firstpair=(probe.forms[root_i,root_h[0]]+probe.forms[root_i,root_h[1]])/probe.L
    cover=np.asarray([int(any(a in B for a in root_h)) for B in probe.types],dtype=float)
    static=np.asarray([[probe.forms[inds[a],a] for inds in probe.security_indices]
                       for a in range(probe.p)],dtype=float)/probe.L
    return np.asarray(gamma,dtype=float)/probe.L,firstpair,cover,static,root_h

def saddle_p(static,w):
    A=static@w
    p=A.shape[0]
    result=linprog([0.]*p+[-1.],A_ub=np.column_stack([-A.T,np.ones(A.shape[1])]),
            b_ub=np.zeros(A.shape[1]),A_eq=[[1.]*p+[0.]],b_eq=[1.],
            bounds=[(0,None)]*(p+1),method="highs")
    assert result.success,result.message
    return result.x[:-1],result.x[-1]

def attack(probe,policy,w,rng):
    gamma,pair,cover,static,path=cone_data(probe,policy)
    starts=[saddle_p(static,np.asarray(w,dtype=float))[0],np.ones(probe.p)/probe.p]
    for _ in range(3):
        z=np.asarray([rng.random() for _ in range(probe.p)])
        starts.append(z/z.sum())
    best=None
    n=len(probe.types)
    for start in starts:
        p=start
        for iteration in range(8):
            query=np.einsum('a,acb->cb',p,static)
            A=np.vstack([np.column_stack([-gamma,np.zeros(len(gamma))]),
                         np.column_stack([-query,np.ones(len(query))])])
            result=linprog(np.r_[pair,-2.],A_ub=A,b_ub=np.zeros(len(A)),
                    A_eq=[np.r_[cover,0.]],b_eq=[1.],
                    bounds=[(0,None)]*(n+1),method="highs")
            assert result.success,result.message
            if best is None or result.fun<best["margin"]:
                best={"margin":float(result.fun),"path":path,"query":p.tolist(),
                      "weights":result.x[:-1].tolist(),"security_floor":float(result.x[-1]),
                      "first_pair":float(pair@result.x[:-1]),"p":probe.p,"r":probe.r,
                      "policy":[{"history":h,"action":a} for h,a in sorted(policy.items(),key=lambda z:(len(z[0]),z[0]))]}
            if result.fun < -1e-7: return best
            p2,v=saddle_p(static,result.x[:-1])
            if np.linalg.norm(p2-p,ord=1)<1e-10: break
            p=p2
    return best

def main():
    rng=random.Random(341209)
    report=[]
    original=json.loads((ROOT/'examples/customer_attraction/individual_security_failure.json').read_text())
    p=6;r=3
    probe=Probe(p,r,(0,)*p)
    w=[0]*len(probe.types)
    for c in original['customers']:
        mask=sum(1<<a for a in c['topics'])
        w[mask-1]=c['multiplicity']
    obj=json.loads((ROOT/'evidence/certificates/customer_attraction/individual_security_failure.json').read_text())
    policy={tuple(z['history']):z['action'] for z in obj['strategy']['actions']}
    result=attack(probe,policy,w,rng)
    report.append({"source":"individual_security_failure","result":result})
    print(json.dumps({"source":"individual_security_failure","margin":result['margin']}),flush=True)
    for p,r,npolicies in [(5,4,20),(4,5,20),(6,3,30)]:
        probe=Probe(p,r,(0,)*p)
        for i in range(npolicies):
            w=[rng.choice([0,0,0,1,1,2,3,5,8]) for _ in probe.types]
            policy=get_policy(probe,w,rng)
            result=attack(probe,policy,w,rng)
            report.append({"source":[p,r,i],"result":result})
            print(json.dumps({"source":[p,r,i],"margin":result['margin']}),flush=True)
            if result['margin'] < -1e-7: break
        if result['margin'] < -1e-7: break
    (HERE/'pair_security_cone_probe_report.json').write_text(json.dumps({"seed":341209,"method":"Floating alternating LPs in fixed full-history policy cones; no universal certificate","policies":report},indent=2)+"\n")

if __name__=='__main__': main()
