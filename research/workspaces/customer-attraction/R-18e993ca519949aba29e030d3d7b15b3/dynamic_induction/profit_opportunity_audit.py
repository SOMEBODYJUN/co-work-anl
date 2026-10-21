"""Independent Fraction replay; no customer_attraction import."""
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
from math import isqrt
import json
P=Path(__file__).parent

def comps(n,k):
    if k==1:
        yield (n,); return
    for a in range(n+1):
        for tail in comps(n-a,k-1): yield (a,)+tail

def utility(I,h,player):
    ans=Q(0); a=h[player]
    for C in I['customers']:
        if a in C['topics']:
            c=sum(t in C['topics'] for t in h)
            ans+=Q(C['multiplicity'],c)
    return ans

def replay(I,action):
    n=I['players'];k=len(I['topics']);checked=0;deviations=0
    def terminal(h):
        while len(h)<n:h=h+(action(h),)
        return h
    for depth in range(n):
        for h in product(range(k),repeat=depth):
            z=terminal(h);u=utility(I,z,depth)
            for a in range(k):
                alt=terminal(h+(a,))
                assert u>=utility(I,alt,depth),(h,a,u,utility(I,alt,depth))
                deviations+=1
            checked+=1
    return {'histories':checked,'action_comparisons_including_chosen':deviations,
            'path':terminal(()),'profits':list(map(str,[utility(I,terminal(()),i) for i in range(n)]))}

def F(I,b):
    n=I['players'];r=n-sum(b);k=len(b);best=Q(-1);arg=[]
    for d in comps(r,k):
        val=Q(0)
        for C in I['customers']:
            B=sum(b[a] for a in C['topics']);D=sum(d[a] for a in C['topics'])
            if D:val+=Q(C['multiplicity']*D,B+D)
        if val>best:best=val;arg=[d]
        elif val==best:arg.append(d)
    return best,arg

def main():
    records=[]
    for n in range(2,7):
        I={'players':n,'topics':['A']+[f'L{i}' for i in range(1,n)],
           'customers':[{'topics':[0],'multiplicity':n}]+[{'topics':[i],'multiplicity':1} for i in range(1,n)]}
        rec=replay(I,lambda h:0)
        f,args=F(I,(1,)+(0,)*(n-1));q=isqrt(n)
        direct=max(Q(n*j,j+1)+n-1-j for j in range(n))
        delta=min(Q(j)+Q(n,j) for j in range(1,n+1))-1
        short=min(Q(q)+Q(n,q),Q(q+1)+Q(n,q+1))-1
        assert f==direct and 2*n-1-f==delta==short
        assert delta>=2*q-1
        rec.update({'players':n,'F_after_first':str(f),'delta':str(delta),'argmax_counts':args})
        records.append(rec)
    I=json.loads((P/'background_step_instance.json').read_text())
    C=json.loads((P/'background_step_certificate.json').read_text())
    actions={tuple(row['history']):row['action'] for row in C['actions']}
    rec=replay(I,lambda h:actions[h]);f4,a4=F(I,(0,0,1));f3,a3=F(I,(1,0,1))
    assert f4==11 and f3==Q(41,6) and f4-f3==Q(25,6)>4
    rec.update({'F4_C':str(f4),'F3_CA':str(f3),'gap':str(f4-f3),'F4_argmax':a4,'F3_argmax':a3})
    out={'status':'PASS','family_full_tree_checks':records,'background_certificate':rec,
         'scope':'Finite replay and formula implementation audit; general boundary is proved analytically in profit_opportunity_boundary.md.'}
    (P/'profit_opportunity_audit.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'status':'PASS','family_histories':sum(r['histories'] for r in records),'background':rec},indent=2))
if __name__=='__main__':main()
