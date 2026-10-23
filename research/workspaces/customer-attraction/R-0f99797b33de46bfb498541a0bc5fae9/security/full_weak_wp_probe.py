"""Finite diagnostic for the stronger full-root, all-p weak insertion bridge.
Not Mfull: testing p^T K p <= u, not min_b p^T K[:,b] <= u.
"""
from extra_iid_probe import *
def test(k,r,pol,base,p):
    gamma,d,mem,bb,z=matrices(k,r,pol,base)
    K=np.array([mem/(bb+1+mem[list(z[(a,)])].sum(axis=0)) for a in range(k)]).transpose(1,0,2)
    c=np.einsum('a,b,abx->x',p,p,K)
    lp=linprog(d-c,A_ub=-gamma,b_ub=np.zeros(len(gamma)),A_eq=np.ones((1,len(d))),b_eq=[1],bounds=(0,None),method='highs')
    return lp,K

def main():
    rng=np.random.default_rng(235091)
    best=0;report=[]
    for case in range(80):
        k=4 if case<50 else 5;r=[3,4,5][case%3];base=[0]*k
        if case%4==1:base[int(rng.integers(k))]=1
        if case%4==2:
            for _ in range(2):base[int(rng.integers(k))]+=1
        w=rng.integers(0,12,size=(1<<k)-1);w[rng.random(len(w))<.5]=0
        if not any(w):continue
        pol,u=policy(k,r,w,base,case)
        gamma,d,mem,bb,z=matrices(k,r,pol,base)
        K=np.array([mem/(bb+1+mem[list(z[(a,)])].sum(axis=0)) for a in range(k)]).transpose(1,0,2)
        for mask in range(1,1<<k):
            p=np.array([int(mask>>a&1) for a in range(k)],float);p/=sum(p)
            c=np.einsum('a,b,abx->x',p,p,K)
            lp=linprog(d-c,A_ub=-gamma,b_ub=np.zeros(len(gamma)),A_eq=np.ones((1,len(d))),b_eq=[1],bounds=(0,None),method='highs')
            if lp.success and -lp.fun>best+1e-9:
                best=-lp.fun;print('BEST',case,r,k,best,flush=True)
            if lp.success and -lp.fun>1e-7:
                rec=dict(case=case,k=k,r=r,base=base,p=p.tolist(),weights=lp.x.tolist(),gap=-lp.fun,policy={','.join(map(str,h)):a for h,a in pol.items()})
                (HERE/'full_weak_wp_positive_float.json').write_text(json.dumps(rec,indent=2)+'\n');return
        report.append(dict(case=case,k=k,r=r))
        if case%10==0:print('case',case,'best',best,flush=True)
    (HERE/'full_weak_wp_report.json').write_text(json.dumps(dict(scope='finite diagnostic only; all-p WP not Mfull',best=best,cases=report),indent=2)+'\n')
if __name__=='__main__':main()
