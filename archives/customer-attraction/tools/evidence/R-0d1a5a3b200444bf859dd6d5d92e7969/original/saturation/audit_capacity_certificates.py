"""Exact independent customer-type audits of RC+ and AP-capacity cuts.

No imports from discovery solvers or the parent implementation.  The finite
state space is exact: a bit for each of five root-branch topics and the indexed
OPT membership count 0..5.  This is a universal coefficient certificate, not a
finite collection of example games.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json


def div(n,d):
    return F(n,d) if n else F(0)


def raw(b,j):
    c,a2,a3,a4,a5=b
    total=sum(b)
    uu=[div(z,total) for z in b]
    ans={f'size{i+1}':c-b[i] for i in range(1,5)}
    ans['IC3_to_last']=uu[2]-div(a5,c+a2+3)
    ans['IC4_to_last']=uu[3]-div(a5,c+a2+a3+2)
    ans['last_OPT']=5*uu[4]-div(j,c+a2+a3+a4+1)
    for i in range(1,4):
        old=sum(b[:i]);k=5-i;a=8*(k-1)+k*k
        s=div(a5,old+k)
        f=j*(div(a5,old+k)+div(1-a5,old+1))
        ans[f'AP{i+1}_last_OPT']=5*a*uu[i]-5*(a-2)*s-2*f
    return uu[0],ans


certs={
 'parent_RC_plus':{
  'alpha':F(65710,1073),'beta':-F(56053,5365),
  'weights':{
   'size2':F(1,2),'size3':F(7409,2146),
   'size4':F(7013,2146),'size5':F(2824,1073),
   'IC3_to_last':F(3168,1073),'IC4_to_last':F(2970,1073),
   'last_OPT':F(1),
  },
 },
 'AP_capacity':{
  'alpha':F(32025287102,569802301),
  'beta':-F(26897066393,2849011505),
  'weights':{
   'size2':F(3587181193,1139604602),
   'size3':F(3414947593,1139604602),
   'size4':F(3269541343,1139604602),
   'size5':F(1093474931,569802301),
   'AP2_last_OPT':F(7581354,569802301),
   'AP3_last_OPT':F(11533500,569802301),
   'AP4_last_OPT':F(23203125,569802301),
   'last_OPT':F(485166343,569802301),
  },
 },
}

def audit(cert):
    alpha,beta,weights=cert['alpha'],cert['beta'],cert['weights']
    assert alpha>=0 and all(v>=0 for v in weights.values())
    ordinary=[];strong=[];tight=[]
    for b in product([0,1],repeat=5):
        for j in range(6):
            v,rr=raw(b,j)
            rho=alpha*v+beta*b[0]-int(j>0)-sum(w*rr[n] for n,w in weights.items())
            rho_plus=rho-F(j-int(j>0),5)
            assert rho_plus>=0,(b,j,rho_plus)
            ordinary.append(rho);strong.append(rho_plus)
            if rho_plus==0:tight.append({'branch_bits':''.join(map(str,b)),'optimal_count':j})
    return {'states':len(strong),'minimum_residual':str(min(ordinary)),
            'minimum_repetition_credit_residual':str(min(strong)),
            'tight_repetition_credit_types':tight,
            'alpha':str(alpha),'beta':str(beta),
            'weights':{n:str(w) for n,w in weights.items()}}


if __name__=='__main__':
    out={n:audit(c) for n,c in certs.items()}
    target=Path(__file__).with_name('capacity_exact_audits.json')
    target.write_text(json.dumps(out,indent=2)+'\n')
    for name,a in out.items():
        print(name,a['states'],'states; min',a['minimum_residual'],
              'min with J credit',a['minimum_repetition_credit_residual'],
              'tight',len(a['tight_repetition_credit_types']))
