"""Integer all-SPE-outcome oracle and finite early-price search.

Discovery uses the canonical set-valued BI recurrence with exact scaled integer
payoffs. It does not force equal-count histories to select the same outcome.
Finite zero violations do not establish a universal inequality.
"""
import argparse,itertools,json,math,random
from pathlib import Path
import numpy as np
from scipy.optimize import linprog

def states(k,n):
    if k==1:
        yield (n,);return
    for a in range(n+1):
        for q in states(k-1,n-a):yield (a,)+q

class Oracle:
    def __init__(self,k,m):
        self.k=k;self.m=m;self.L=math.lcm(*range(1,m+1));self.masks=np.arange(1,2**k)
        self.member=np.array([[(b>>a)&1 for b in self.masks] for a in range(k)],dtype=np.int64)
        self.term=list(states(k,m));self.idx={q:i for i,q in enumerate(self.term)}
        den=np.array(self.term)@self.member
        self.coeff=np.array([np.floor_divide(self.L*self.member[a],den,out=np.zeros_like(den),where=den>0) for a in range(k)]).transpose(1,0,2)
        self.cover=(den>0).astype(np.int64)
        self.support=np.array(self.term)>0
        self.compcov=np.array([(self.member[list(t)].sum(axis=0)>0).astype(np.int64) for t in itertools.combinations(range(k),min(k,m))])
        self.layers=[list(states(k,d)) for d in range(m)]
        self.child={q:[q[:a]+(q[a]+1,)+q[a+1:] for a in range(k)] for layer in self.layers for q in layer}

    def solve(self,mass):
        self.mass=mass;self.U=self.coeff@mass;self.W=self.cover@mass;self.OPT=int(max(self.compcov@mass));self.out={q:np.array([i],dtype=int) for i,q in enumerate(self.term)};self.floor={}
        for layer in reversed(self.layers):
            for q in layer:
                ch=[self.out[t] for t in self.child[q]]
                floor=max(int(min(self.U[c,a])) for a,c in enumerate(ch));self.floor[q]=floor
                self.out[q]=np.unique(np.concatenate([c[self.U[c,a]>=floor] for a,c in enumerate(ch)]))
        root=self.out[(0,)*self.k]
        mins=np.min(np.where(self.support[root],self.U[root],np.iinfo(np.int64).max),axis=1)
        weak=self.OPT-self.W[root]-self.m*mins/self.L
        strong=self.OPT-self.W[root]-(self.m-1)*mins/self.L
        j=int(np.argmax(weak));j2=int(np.argmax(strong))
        return {'weak':float(weak[j]),'weak_terminal':self.term[root[j]],'strong':float(strong[j2]),'strong_terminal':self.term[root[j2]],'root_outcomes':len(root),'root':root,'minpay_scaled':mins}

    def price(self,v):
        k,n=self.member.shape
        a=linprog(np.r_[np.full(k,v),-self.mass],A_ub=np.c_[-self.member.T,np.eye(n)],b_ub=np.zeros(n),bounds=[(0,1)]*k+[(0,1)]*n,method='highs')
        assert a.success
        return float(-a.fun),a.x[:k]

def main():
    p=argparse.ArgumentParser();p.add_argument('--topics',type=int,default=7);p.add_argument('--players',type=int,default=5);p.add_argument('--trials',type=int,default=1000);p.add_argument('--seed',type=int,default=2026102125);p.add_argument('--output',required=True);args=p.parse_args()
    O=Oracle(args.topics,args.players);rng=random.Random(args.seed);n=len(O.masks);records=[];best=-1e99
    for t in range(args.trials):
        if t%3==0:
            mass=np.zeros(n,dtype=np.int64);mass[0]=args.players*20
            for a in range(1,min(args.players,args.topics)):mass[2**a-1]=20
            for _ in range(rng.randrange(1,12)):mass[rng.randrange(n)]+=rng.randrange(1,8)
        elif t%3==1:
            mass=np.array([rng.choice([0,0,0,0,1,2,3,8,20]) for _ in range(n)],dtype=np.int64)
        else:
            mass=np.zeros(n,dtype=np.int64)
            for _ in range(rng.randrange(4,20)):
                b=sum(1<<a for a in range(args.topics) if rng.random()<rng.choice([.2,.3,.5,.7]));
                if b:mass[b-1]+=rng.randrange(1,25)
        r=O.solve(mass)
        # B is decreasing in price; for each terminal only its least-used payoff
        # can maximize a violation among actual providers at that terminal.
        bbest=-1e99;zbest=None;term=None;vbest=None
        for idx,v0 in zip(r['root'],r['minpay_scaled']):
            v=float(v0/O.L);b,z=O.price(v);gap=b-float(O.W[idx])+v
            if gap>bbest:bbest=gap;zbest=z.tolist();term=O.term[idx];vbest=v
        rec={a:b for a,b in r.items() if a not in ['root','minpay_scaled']};rec.update({'trial':t,'price_strong_gap':bbest,'price_terminal':term,'price':vbest,'queries':zbest,'weights':{str(mask):int(v) for mask,v in zip(O.masks,mass) if v}})
        if bbest>best+1e-7:
            best=bbest;records.append(rec);print(json.dumps({a:b for a,b in rec.items() if a!='weights'}),flush=True)
        if t%100==0:print('completed',t,'best',best,flush=True)
        Path(args.output).write_text(json.dumps({'scope':__doc__,'parameters':vars(args),'completed':t+1,'record_improvements':records},indent=2)+'\n')
        if bbest>1e-7 or r['weak']>0:break
if __name__=='__main__':main()
