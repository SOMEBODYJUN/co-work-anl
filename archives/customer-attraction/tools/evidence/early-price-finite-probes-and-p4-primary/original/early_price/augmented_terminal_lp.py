"""Numerical pointwise certificate test; no claim of universal feasibility."""
import itertools,json
from scipy.optimize import linprog

def residue(p,a,b,d,e,tau,t,s,l):
    P=p/(p+a+b) if p+a+b else 0
    beta=b/(p+a+b) if p+a+b else 0
    D=(p+1)*(p+2)
    return P+(1-t-l)*beta-min(1,d)+d/(p+1)+(t/tau)*e/(p+a+1)-(s/tau)*d*e/D-(1-s)*e/(p+1)+(1-s)*tau*b/(p+1)-(1-s)*b*d/D+l*a/(p+2)

if __name__=='__main__':
    for tau in [1,1.1,1.5,2,3,5,10,100]:
        rows=[];rhs=[]
        for p,a,b,d,e in itertools.product(range(31),range(2),range(2),[0,1,tau],[0,tau]):
            base=residue(p,a,b,d,e,tau,0,0,0)
            rows.append([base-residue(p,a,b,d,e,tau,*z) for z in [(1,0,0),(0,1,0),(0,0,1)]])
            rhs.append(base)
        ans=linprog([0,0,0],A_ub=rows,b_ub=rhs,bounds=[(0,None),(0,1),(0,None)],method='highs')
        print(tau,ans.success,ans.x if ans.success else ans.message)
