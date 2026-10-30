"""Independent exact rebuild of the AP/root-capacity certificate.

No imports from saturation discovery or its row evaluator.
"""
from fractions import Fraction as F
from itertools import product
import json


def main():
    den=569802301
    alpha=F(32025287102,den);gamma=-F(26897066393,5*den)
    sizes=[F(3587181193,2*den),F(3414947593,2*den),
           F(3269541343,2*den),F(1093474931,den)]
    aps=[F(7581354,den),F(11533500,den),F(23203125,den)]
    last=F(485166343,den)
    allrho=[]; out=[]
    for a in product((0,1),repeat=5):
        total=sum(a)
        pay=[F(v,total) if v else F(0) for v in a]
        for j in range(6):
            G=sum((sizes[i-1]*(a[0]-a[i]) for i in range(1,5)),F(0))
            for i in range(1,4):
                k=5-i;bg=sum(a[:i]);ak=8*(k-1)+k*k
                sc=F(a[4],bg+k)
                ff=j*(F(a[4],bg+k)+F(1-a[4],bg+1))
                row=5*ak*pay[i]-5*(ak-2)*sc-2*ff
                G+=aps[i-1]*row
            G+=last*(5*pay[4]-F(j,sum(a[:4])+1))
            rho=alpha*pay[0]+gamma*a[0]-int(j>0)-F(j-int(j>0),5)-G
            assert rho>=0,(a,j,rho)
            allrho.append(rho)
            if rho==0:out.append({'a':list(a),'j':j})
    print(json.dumps({'status':'pass','states':len(allrho),'minimum':str(min(allrho)),
      'zero_states':out,'claim':'569802301*(4*O+J)+26897066393*K <=160126435510*r'},indent=2))


if __name__=='__main__':main()
