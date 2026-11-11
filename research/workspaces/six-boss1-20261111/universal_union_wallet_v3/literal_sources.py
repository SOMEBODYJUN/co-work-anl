"""Literal source formulas reused from the prior independent checker; no builder imports."""
from fractions import Fraction as F

def old_rows(v,K=F(0)):
    a=list(v[:6]);x,o=v[6:];c=sum(a);P=sum(a[:4]);D=P+1
    us=[F(q,c) if c else F(0) for q in a]
    pure=a+[x];theta=list(map(F,pure))+[F(o,6)];fs=[q/D for q in theta]
    r={}
    for i in range(6):
        for j in range(8):r[f"SAFE_{i+1}_{j+1}"]=us[i]-theta[j]/(sum(a[:i])+6-i)
    for i,C in enumerate((31,25,19,10)):
        b=sum(a[:i]);cap=b+6-i
        r[f"UP_{i+1}"]=C*us[i]-F((C-1)*x,cap)-F(o*x,6*cap)-F(o*(1-x),6*(b+1))
    for j in list(range(6))+[7]:
        r[f"FMAX_{j+1}"]=fs[6]-fs[j]
        r[f"MX_{j+1}"]=us[4]-theta[j]/(D+x)
    for l in range(8):
        for rr in range(l,8):
            if rr<7:right=F(pure[l]+pure[rr],D)-F(pure[l]*pure[rr],D*(D+1))
            elif l<7:right=F(pure[l],D)+F(o,6*D)-F(pure[l]*o,6*D*(D+1))
            else:right=F(o,3*D)-F(o,36*D*(D+1))
            r[f"RC_{l+1}_{rr+1}"]=us[4]+fs[6]-right
            r[f"PAIR_{l+1}_{rr+1}"]=us[4]+us[5]+F(a[4],D*(D+1))-right
    for omit in range(7):r[f"OPT6_omit_{omit+1}"]=-F(any(bit for j,bit in enumerate(pure) if j!=omit))
    for j in range(7):r[f"K_ge_size_{j+1}"]=K-pure[j]
    r["K_le_1"]=-K
    for i in range(6):r[f"SIZE_FLOOR_{i+1}"]=us[i]-K/6
    r["W_le_1"]=-F(c>0)
    r["ROOT_NEAR"]=150*us[0]-F(139,6)*K-o
    for anchor in range(7):
        for query in range(8):r[f"ROOT_RIG_{anchor+1}_{query+1}"]=25*us[0]+3*K-7*pure[anchor]-theta[query]+F(5,6)*pure[anchor]*theta[query]
    return r

def literal_tail(v,y,t):
    """Weighted original six row LHS, using the actual common branch load."""
    a=list(v[:6]);x,o=v[6:];b=sum(a[:3]);P=b+a[3];D=P+1;d=b+x+1
    load=b+x+y+t;theta=F(o,6)
    v4=F(x,load) if load else F(0)
    fifth=F(y,load) if load else F(0)
    sixth=F(t,load) if load else F(0)
    source_ic=v4
    global_max=F(y,D)
    global_cap=F(t)
    terminal_BR=theta/(b+x+y+1)-sixth
    pair_query=(F(a[5],d)+theta/d-F(a[5],d*(d+1))*theta)
    pair_wallet=fifth+sixth+F(y,d*(d+1))
    actual_RC=F(t,D)+theta/D-F(t,D*(D+1))*theta
    return (4096*source_ic+800*global_max+71*global_cap+384*terminal_BR
            +512*(pair_query-pair_wallet)+900*actual_RC)
