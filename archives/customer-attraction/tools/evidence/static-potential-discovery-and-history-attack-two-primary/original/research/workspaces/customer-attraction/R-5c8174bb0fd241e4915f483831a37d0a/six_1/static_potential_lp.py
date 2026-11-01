"""Six-slot static potential/terminal-price implication, disjoint optimal themes.

The six optimal themes are exchangeable and disjoint. Type (mask,1) has total
mass over all six labels, split equally among them; (mask,0) has no optimal
membership. All six actual themes are distinct labels with arbitrary overlap.
Potential comparisons include *all* six-tuples from the twelve-theme menu:
symmetry and concavity make the optimal-theme counts balanced, hence 0/1.
This probes only a proposed implication, never a full-SPE instance.
"""
from itertools import product
from math import comb
from fractions import Fraction
import numpy as np
from scipy.optimize import linprog

M=6
TYPES=list(product(range(64),(0,1)))
H=[sum(Fraction(1,j) for j in range(1,k+1)) for k in range(7)]

def compositions_leq(n,k):
    if k==1:
        for a in range(n+1):yield (a,)
    else:
        for a in range(n+1):
            for tail in compositions_leq(n-a,k-1):yield (a,)+tail

def data():
    W=[]; C=[]; u6=[]; prices=[[] for _ in range(7)]
    for mask,opt in TYPES:
        bits=[(mask>>i)&1 for i in range(6)]
        W.append(int(bool(mask)))
        C.append(sum(Fraction(bits[i],1)*(Fraction(1,1+sum(bits[:i]))-Fraction(1,6-i+sum(bits[:i]))) for i in range(6)))
        load=sum(bits)
        u6.append(Fraction(bits[5],load) if bits[5] else Fraction(0))
        for i in range(6):prices[i].append(Fraction(bits[i],1+sum(bits[:5])))
        prices[6].append(Fraction(opt,6*(1+sum(bits[:5]))))
    rows=[]; labels=[]
    for actual in compositions_leq(6,6):
        optslots=6-sum(actual)
        row=[]
        for mask,opt in TYPES:
            load=sum(actual[i]*((mask>>i)&1) for i in range(6))
            # six exchangeable, disjoint optimal themes, each used at most once
            pot=H[load]+Fraction(optslots*opt,6*(load+1))
            row.append(pot)
        rows.append(row);labels.append(actual)
    return (np.array(W,dtype=float),np.array(C,dtype=float),np.array(u6,dtype=float),
            np.array(prices,dtype=float),np.array(rows,dtype=float),labels)

def main():
    W,C,u6,prices,pots,labels=data()
    A=np.vstack([p-W-C for p in pots]+[p-u6 for p in prices]); b=np.zeros(len(A))
    norm=np.array([int(opt) for mask,opt in TYPES],float)
    sol=linprog(2*W,A_ub=A,b_ub=b,A_eq=[norm],b_eq=[1.],bounds=(0,None),method='highs')
    print('status',sol.message,'min2W',sol.fun,'types',len(TYPES),'potential rows',len(pots))
    if not sol.success:return
    print('W',W@sol.x,'C',C@sol.x,'u6',u6@sol.x)
    print('nonzero:')
    for i in np.flatnonzero(sol.x>1e-8):print(TYPES[i],sol.x[i])
    print('price gaps',u6@sol.x-prices@sol.x)
    slack=W@sol.x+C@sol.x-pots@sol.x
    print('active potential',[(labels[i],float(v)) for i,v in enumerate(slack) if v<1e-8][:20], 'count',int((slack<1e-8).sum()),'min',slack.min())
    ids=list(np.flatnonzero(sol.x>1e-8))
    active=[int(i) for i in np.flatnonzero(slack<1e-8)]
    eq=[];rhs=[]
    def exact_columns(j,actual=None):
        mask,opt=TYPES[j];bits=[(mask>>i)&1 for i in range(6)]
        w=int(bool(mask));c=sum(Fraction(bits[i])*(Fraction(1,1+sum(bits[:i]))-Fraction(1,6-i+sum(bits[:i]))) for i in range(6))
        ul=Fraction(bits[5],sum(bits)) if bits[5] else Fraction(0)
        prices_e=[Fraction(bits[i],1+sum(bits[:5])) for i in range(6)]+[Fraction(opt,6*(1+sum(bits[:5])))]
        if actual is None:return w,c,ul,prices_e
        load=sum(actual[i]*bits[i] for i in range(6));slots=6-sum(actual)
        potential=H[load]+Fraction(slots*opt,6*(load+1))
        return potential-w-c
    for i in active:
        eq.append([exact_columns(j,labels[i]) for j in ids]);rhs.append(0)
    for i in range(7):
        if abs(float((prices[i]-u6)@sol.x))<1e-8:
            eq.append([exact_columns(j)[3][i]-exact_columns(j)[2] for j in ids]);rhs.append(0)
    eq.append([int(TYPES[j][1]) for j in ids]);rhs.append(1)
    aug=[[Fraction(v) for v in row]+[Fraction(r)] for row,r in zip(eq,rhs)]
    piv=[]
    for ccol in range(len(ids)):
        pivot=next((i for i in range(len(piv),len(aug)) if aug[i][ccol]),None)
        if pivot is None:continue
        aug[len(piv)],aug[pivot]=aug[pivot],aug[len(piv)]
        p=aug[len(piv)][ccol];aug[len(piv)]=[v/p for v in aug[len(piv)]]
        for i in range(len(aug)):
            if i!=len(piv) and aug[i][ccol]:
                z=aug[i][ccol];aug[i]=[v-z*w for v,w in zip(aug[i],aug[len(piv)])]
        piv.append(ccol)
    print('active rank',len(piv),'variables',len(ids))
    if len(piv)==len(ids):
        xx=[aug[i][-1] for i in range(len(ids))]
        assert all(v>=0 for v in xx)
        assert all(sum(row[j]*xx[j] for j in range(len(ids)))==r for row,r in zip(eq,rhs))
        print('exact masses',[(TYPES[i],str(v)) for i,v in zip(ids,xx)])
        print('exact 2W',sum(2*int(TYPES[i][0]>0)*v for i,v in zip(ids,xx)))
        print('exact min potential slack',min(-sum(exact_columns(j,a)*v for j,v in zip(ids,xx)) for a in labels))
        print('exact prices',[(i,sum((exact_columns(j)[2]-exact_columns(j)[3][i])*v for j,v in zip(ids,xx))) for i in range(7)])

if __name__=='__main__':main()
