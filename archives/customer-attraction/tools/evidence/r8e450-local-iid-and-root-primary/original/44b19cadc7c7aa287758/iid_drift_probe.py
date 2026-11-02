"""Exploratory numerical test of local symmetric-iid benchmark drift; not proof."""
import sys,json,random,math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[5]))
import numpy as np
from scipy.optimize import minimize
from customer_attraction import Instance,CustomerType,ExactSPESolver

def benchmark(ins,r,prefix):
    k=ins.topic_count
    if r==0:return 0,np.ones(k)/k
    mat=np.array([[int(a in c.topics) for a in range(k)] for c in ins.customers])
    weights=np.array([c.multiplicity for c in ins.customers])
    b=mat@np.array(prefix)
    hs=np.zeros((len(weights),r+1))
    for j in range(1,r+1):hs[:,j]=hs[:,j-1]+1/(b+j)
    def vals(q):
        t=mat@q
        probs=np.array([math.comb(r,j)*t**j*(1-t)**(r-j) for j in range(r+1)]).T
        f=np.sum(probs*hs,axis=1)@weights
        gs=sum(math.comb(r-1,j)*t**j*(1-t)**(r-1-j)/(b+1+j) for j in range(r))
        return f,r*mat.T@(weights*gs)
    result=minimize(lambda q:-vals(q)[0],np.ones(k)/k,jac=lambda q:-vals(q)[1],bounds=[(0,1)]*k,constraints=[{'type':'eq','fun':lambda q:q.sum()-1,'jac':lambda q:np.ones(k)}],method='SLSQP',options={'ftol':1e-10,'maxiter':300})
    if not result.success:raise RuntimeError(result.message)
    q=result.x;t=mat@q
    welfare=sum(math.comb(r,j)*t**j*(1-t)**(r-j)*j/(b+j) for j in range(1,r+1))@weights
    return welfare,q

def main():
    rng=random.Random(8913)
    best=(1e99,None)
    for trial in range(200):
        k=rng.choice([4,5,6]);m=rng.choice([3,4,5])
        cs=tuple(CustomerType(frozenset(a for a in range(k) if mask>>a&1),rng.randrange(1,11)) for mask in range(1,1<<k) if rng.random()<.28)
        if not cs:continue
        ins=Instance(tuple(map(str,range(k))),cs,m); solver=ExactSPESolver(ins)
        roots=solver.outcomes();v,q=benchmark(ins,m,(0,)*k);floor=solver.threshold((0,)*k)
        for a in range(k):
            pref=tuple(int(j==a) for j in range(k));admiss=[c for c in solver.outcomes(pref) if ins.topic_payoff(a,c)>=floor]
            if not admiss:continue
            c=min(admiss,key=lambda c:ins.topic_payoff(a,c));u=ins.topic_payoff(a,c)
            z,qp=benchmark(ins,m-1,pref);drift=float(u)+z-v
            if drift<best[0]:
                best=(drift,{'trial':trial,'instance':ins.to_dict(),'counts':c,'action':a,'u':str(u),'Z':v,'Znext':z,'q':q.tolist(),'qnext':qp.tolist()})
                print(json.dumps({'best':best}),flush=True)
            if drift < -1e-5:
                Path(__file__).with_name('iid_drift_candidate.json').write_text(json.dumps(best[1],indent=2));return
    print('DONE',json.dumps(best))
if __name__=='__main__':main()
