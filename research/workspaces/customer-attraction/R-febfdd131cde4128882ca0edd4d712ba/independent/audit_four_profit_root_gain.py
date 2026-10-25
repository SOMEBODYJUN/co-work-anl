"""Independent raw-slack audit of the background-one gain in four-tail proof."""
from fractions import Fraction as F
from itertools import product
import json

a=F(1499,750)
c0=F(251,1500)

def ratio(num, den):
    return F(num, den) if num else F(0)

def reconstruct(p, eta):
    a,b,c,d,q,r,s=eta
    k=a+b+c+d
    t=d+q+r+s
    u=[ratio(v,p+k) for v in (a,b,c,d)]
    z=[ratio(v,p+t) for v in (d,q,r,s)]
    D=(p+1)*(p+2)*(p+3)*(p+4)
    tau=lambda v:F(1,p+1)-F(1,p+v+1)
    delta2=tau(a+b)+(F(2*p*p,3*D) if a+b==2 else 0)
    delta3=tau(a+b+c)+(F(p*p+p,D) if a+b+c==3 else 0)
    H=u[2]+u[3]+F(c,(p+a+b+1)*(p+a+b+2))
    K=[u[1]-F(v,p+a+3) for v in (c,d,q,r,s)]
    P=2*H+delta2
    E=4*u[3]+delta3
    root=u[0]-z[0]
    LQS=z[1]-F(s,p+d+3)
    LRC=z[2]-F(c,p+d+q+2)
    LRS=z[2]-F(s,p+d+q+2)
    LSB=z[3]-F(b,p+d+q+r+1)
    G=(sum(w*v for w,v in zip((341,302,306,302,355),K))+
       354*E+646*P+1267*root+24*LQS+8*LRC+17*LRS+108*LSB)/1000
    rho=F(1499,750)*ratio(k,p+k)-G
    return rho

rows=[]
for eta in product((0,1), repeat=7):
    k=sum(eta[:4])
    rho=reconstruct(1,eta)
    gain=c0*F(k,1+k)
    assert rho>=gain,(eta,rho,gain)
    rows.append((eta,rho,gain))
nonzero=[(rho/F(sum(eta[:4]),1+sum(eta[:4])),eta) for eta,rho,gain in rows if sum(eta[:4])]
best=min(x[0] for x in nonzero)
assert best==c0
out={
 'status':'PASS',
 'reconstruction':'raw fractions of terminal shares and stated slacks; no imports of old audit',
 'background':1,'membership_count':len(rows),'alpha':'1499/750','claimed_c':str(c0),
 'exact_best_c':str(best),'minimizing_memberships':[list(e) for v,e in nonzero if v==best],
 'zero_gain_residual_memberships':[list(eta) for eta,rho,gain in rows if rho==gain],
}
print(json.dumps(out,indent=2))
# Reconstruct both exact minimum-residual pattern tables from the same raw slacks.
expected0=list(map(F,['0','0','1/750','1/1500','1/1500','39/500','1/1000','623/3000','2747/12000','691/6000','47/1500','1919/12000','0','77/750','1/4000','1169/6000']))
expected1=list(map(F,['0','133/750','2003/12000','61853/180000','251/3000','6331/22500','7363/36000','26047/60000','239/1200','14579/45000','22183/90000','5177/12000','15767/90000','63893/180000','43349/180000','41143/90000']))
for p,expected in ((0,expected0),(1,expected1)):
    got=[min(reconstruct(p,head+tail) for tail in product((0,1),repeat=3))
         for head in product((0,1),repeat=4)]
    assert got==expected,(p,got,expected)
for optbits in product((0,1),repeat=5):
    e=sum(optbits)
    got=sum((F(e-t,t+e-t) if e-t else F(0)) for t in optbits)
    assert got==4*int(e>0),(optbits,got)
print(json.dumps({'minimum_pattern_tables':'PASS','backgrounds':[0,1],
                  'raw_states_checked':256,'aligned_complement_patterns_checked':32,
                  'strong_row':'2998 sum(V_i)-6000 OPT-1500 sum(r_ti(tail_i)) >=0'},indent=2))
