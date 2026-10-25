"""Definition-level exact coefficient audit; no LP or discovery imports."""
from fractions import Fraction as F
from itertools import product
import json


def residual(a,j):
    c,a2,a3,a4,a5=a
    load=sum(a)
    def pay(i):
        return F(a[i],load) if a[i] else F(0)
    # Slack coefficients in the doubled integer certificate.
    G=(-657100*pay(0)+5365*(c-a2)+37045*(c-a3)
       +35065*(c-a4)+28240*(c-a5)
       +31680*(pay(2)-F(a5,c+a2+3))
       +29700*(pay(3)-F(a5,c+a2+a3+2))
       +10730*(5*pay(4)-F(j,c+a2+a3+a4+1)))
    return -112106*c-8584*int(j>0)-2146*j-G


def main():
    table=[]; vals=[]
    for a in product((0,1),repeat=5):
        v=[residual(a,j) for j in range(6)]
        assert min(v)>=0,(a,v)
        # For j>=1 the strong residual slope is explicitly nonnegative.
        slope=F(10730,sum(a[:4])+1)-2146
        assert slope>=0
        assert all(v[j]==v[1]+(j-1)*slope for j in range(1,6))
        table.append({'bits':''.join(map(str,a)),'j0':str(v[0]),'j1':str(v[1]),'slope':str(slope)})
        vals+=v
    print(json.dumps({'status':'pass','states':len(vals),'minimum':str(min(vals)),
       'zero_states':vals.count(0),'claim':'4292*O+1073*J+56053*K <= 328550*r',
       'table':table},indent=2))


if __name__=='__main__':main()
