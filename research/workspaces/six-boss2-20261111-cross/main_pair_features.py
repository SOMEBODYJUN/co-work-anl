"""Frozen independent Main feature identities, shared by exact audits."""
from fractions import Fraction as F

def pay(a,b):return F(a,b) if a else F(0)

def terms(p,ell,t,q,b,c,j,v,s=0,ss=0,k=3):
    u={'t':F(t),'q':F(q),'b':F(b),'c':F(c),'j':F(j),'v':F(v)}
    z1=p+t+s+b+c;z2=p+c+ss+j+v
    e={'sourceT':pay(t,z1),'sourceC':pay(c,z2)}
    cost={'sourceT':(1,0,0),'sourceC':(1,0,0)}
    for label in 'bcjv':e['price:'+label]=u[label]/(ell+1);cost['price:'+label]=(0,1,0);e['cap:'+label]=u[label];cost['cap:'+label]=(0,0,1)
    for name,den,own,z,qs in [('last1',p+t+s+b+1,c,z1,'tqbjv'),('last2',p+c+ss+j+1,v,z2,'tqbcj'),('safeB',p+t+s+2,b,z1,'tqcjv'),('safeJ',p+c+ss+2,j,z2,'tqbcv')]:
        for a in qs:e[name+':'+a]=u[a]/den-pay(own,z);cost[name+':'+a]=(0,0,0)
    for a,count in [('s',s),('ss',ss)]:e['price:'+a]=F(count,ell+1);e['cap:'+a]=F(count);cost['price:'+a]=(0,k-3,0);cost['cap:'+a]=(0,0,k-3)
    labels=['t','q','b','c','j','v']
    for which,beta,first,last,z in [(1,p+t+s,b,c,z1),(2,p+c+ss,j,v,z2)]:
        for ai,aa in enumerate(labels):
            for bb in labels[ai:]:
                overlap=u[aa] if aa==bb else u[aa]*u[bb]
                key=f'pair{which}:{aa},{bb}'
                e[key]=(u[aa]+u[bb])/(beta+1)-(overlap+first)/((beta+1)*(beta+2))-pay(first+last,z)
                cost[key]=(0,0,0)
    return e,cost
