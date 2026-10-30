"""Five-player maximal-root branch envelope; exact dual verification required.

An atom is membership in the maximum root theme and its four genuine replies,
plus membership count in five optimal themes. Full-state domain has 192 atoms.
"""
from fractions import Fraction as F
from itertools import product,combinations_with_replacement
from pathlib import Path
import numpy as np,json
from scipy.optimize import linprog
Q=lambda n,d:F(n,d) if n else F(0)
ATOMS=[(b,d) for b in product((0,1),repeat=5) for d in range(6)]

def rows(b,d):
    load=sum(b);v=[Q(x,load) for x in b];K=F(b[0]);o=F(d>0);rr={}
    for j in range(1,5):rr[f'size:{j}']=K-b[j]
    rr['size:opt']=5*K-d
    for i in range(1,5):
        p=sum(b[:i]);k=5-i
        for j in range(5):rr[f'IC:{i}:{j}']=v[i]-Q(b[j],p+k)
        rr[f'opt:{i}']=5*v[i]-Q(d,p+k)
    pref=sum(b[:3]);H=v[3]+v[4]+Q(b[3],(pref+1)*(pref+2))
    rr['r2:O']=F(5,2)*H+Q(pref,pref+1)-o
    rr['r2:opt']=10*H-Q(d*(5-d),pref+1)-Q(d*(d-1),pref+2)
    for j,k in combinations_with_replacement(range(5),2):
        x,y=b[j],b[k]
        rr[f'r2:pair:{j}:{k}']=H-Q(x+y-2*x*y,pref+1)-Q(2*x*y,pref+2)
    bg=b[0]+b[1]
    g3=Q(d*(5-d)*(4-d),2*(bg+1))+Q(d*(d-1)*(5-d),bg+2)+Q(d*(d-1)*(d-2),2*(bg+3))
    rr['r3:opt']=50*sum(v[2:])-3*g3
    g4=Q(d*(d-1),b[0]+d-1)+Q((5-d)*d,b[0]+d)
    rr['r4:opt']=7495*sum(v[1:])-750*g4
    rr['r4:binary']=29985*sum(v[1:])-4985*(b[0]-v[0])-3000*g4
    return rr

def solve_exact(A,y,guess):
    # Rational elimination of all exact active coefficient equations.
    mat=[list(row)+[rhs] for row,rhs in zip(A,y)];n=len(guess);pivot=[];r=0
    for col in range(n):
        hit=next((i for i in range(r,len(mat)) if mat[i][col]),None)
        if hit is None:continue
        mat[r],mat[hit]=mat[hit],mat[r];z=mat[r][col];mat[r]=[x/z for x in mat[r]]
        for i in range(len(mat)):
            if i!=r and mat[i][col]:
                z=mat[i][col];mat[i]=[a-z*b for a,b in zip(mat[i],mat[r])]
        pivot.append(col);r+=1
    if any(not any(row[:n]) and row[n] for row in mat):raise ValueError('inconsistent active equations')
    out=[F(float(x)).limit_denominator(10**7) for x in guess]
    for i,j in enumerate(pivot):out[j]=mat[i][n]-sum(mat[i][k]*out[k] for k in range(n) if k not in pivot)
    return out

def run():
    table=[rows(b,d) for b,d in ATOMS];names=list(table[0]);R=[[t[n] for t in table] for n in names]
    K=[F(b[0]) for b,d in ATOMS];V=[Q(b[0],sum(b)) for b,d in ATOMS];O=[F(d>0) for b,d in ATOMS]
    records=[]
    for rho in map(F,['1/5','21/100','11/50','23/100','6/25','1/4','13/50','7/25','3/10','2/5','1/2']):
        R0=[rho*k-v for k,v in zip(K,V)];allR=[R0]+R;allnames=['root-IC']+names
        mat=np.asarray(allR,dtype=float)
        out=linprog(-np.asarray(O,dtype=float),A_ub=-mat,b_ub=np.zeros(len(allR)),A_eq=[list(map(float,K))],b_eq=[1.],bounds=(0,None),method='highs')
        assert out.success,out.message
        lam=-out.ineqlin.marginals;beta=-out.fun;ids=[i for i,x in enumerate(lam) if x>1e-8]
        residual=beta*np.asarray(K,dtype=float)-np.asarray(O,dtype=float)-lam@mat
        tight=[j for j,x in enumerate(residual) if abs(x)<1e-7]
        A=[[K[j]]+[-allR[i][j] for i in ids] for j in tight]
        exact=solve_exact(A,[O[j] for j in tight],[beta]+[lam[i] for i in ids]);eb=exact[0];els=exact[1:]
        assert min(els)>=0
        rem=[eb*K[j]-O[j]-sum(l*allR[i][j] for l,i in zip(els,ids)) for j in range(len(ATOMS))]
        assert min(rem)>=0,(rho,min(rem))
        l0=next((l for l,i in zip(els,ids) if i==0),F(0));C=l0*rho-eb
        rec={'rho':str(rho),'value':str(eb),'B':str(l0),'C':str(C),'multipliers':{allnames[i]:str(l) for l,i in zip(els,ids)},'minimum_residual':str(min(rem)),'checked_atoms':len(ATOMS)}
        records.append(rec);print(json.dumps({k:rec[k] for k in ['rho','value','B','C','minimum_residual']}),flush=True)
    result={'status':'exact-duals-verified','scope':__doc__,'atoms':[(list(b),d) for b,d in ATOMS],'row_names':names,'records':records,'meaning':'O <= B*r-C*K for same five-player SPE; row semantics require mathematical review; no HALF(5) claim'}
    Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
if __name__=='__main__':run()
