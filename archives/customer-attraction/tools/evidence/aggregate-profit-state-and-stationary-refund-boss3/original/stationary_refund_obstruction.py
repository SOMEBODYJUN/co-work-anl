"""Exact algebra audit for an unbounded per-customer stationary refund defect.
No SPE certification is claimed for these routing matrices.
"""
from fractions import Fraction as F
import json

def audit(ell,q):
    assert ell>=2 and 1<=q<ell
    t=ell-q; k=2*(t+1);M=[[0]*k for _ in range(k)]
    # Internal labels 0,1; outside labels 2+i*t+s, i=0,1; s=0,...,t-1.
    for i in range(2):
        M[1-i][i]+=q
        for s in range(t):M[2+i*t+s][i]+=1
    for v in range(2,k):
        i=(v-2)//t;M[i][v]+=1
        w=2+(v-2+1)%(k-2);M[w][v]+=ell-1
    assert all(M[i][i]==0 for i in range(k))
    assert all(sum(row)==ell for row in M)
    assert all(sum(M[j][i] for j in range(k))==ell for i in range(k))
    for start in range(k):
        seen={start};todo=[start]
        while todo:
            i=todo.pop()
            for j in range(k):
                if M[j][i] and j not in seen:seen.add(j);todo.append(j)
        assert len(seen)==k
    dbar=pbar=taxbar=F(0)
    loads=[]
    for i in range(k):
        I=int(i<2);K=sum(M[j][i] for j in range(2));loads.append(K)
        d=F(I,I+K) if I+K else F(0)
        p=F(K,ell*(I+K)) if I+K else F(0)
        tax=F(I*K,K*(K+1)) if K else F(0)
        dbar+=d/k;pbar+=p/k;taxbar+=tax/k
    delta=pbar-dbar
    assert loads[:2]==[q,q] and loads[2:]==[1]*(2*t)
    assert dbar==F(1,(t+1)*(q+1))==taxbar
    assert delta==F(q*t,ell*(t+1)*(q+1))
    assert delta/taxbar==F(q*t,ell)
    return {'remaining_players':ell+1,'tail_slots':ell,'q':q,'t':t,'maxima':k,
      'scope':'irreducible stationary routing; not a certified SPE',
      'mean_root_payoff':str(dbar),'mean_tail_payoff_per_player':str(pbar),
      'mean_root_dilution_tax':str(taxbar),'negative_flux':str(delta),
      'flux_to_entire_refund_ratio':str(delta/taxbar)}

if __name__=='__main__':
    print(json.dumps([audit(l,q) for l,q in [(2,1),(4,2),(8,4),(20,10),(100,50)]],indent=2))
