"""Broader true second->D rows, with a separately exposed pricing decomposition."""
import itertools
from fractions import Fraction as F
from two_D_completion import extras
from third_D_completion import THIRD, SECOND, sh

LABELS="ABCDEUVWXY"
TRIPLES=list(itertools.combinations_with_replacement(LABELS,3))


def rows(atom,r,s,t):
    out=extras(atom,0,0,r,s,t,0,0)
    # Dummy third-D/menu symbols were used only to reuse the direct evaluator.
    out={name:value for name,value in out.items()
         if not(name.startswith("thirdD:") or name.startswith("Dmenu:")
                or name.endswith(":Dmenu") or name.endswith(":K:P")
                or name.endswith(":K:Q") or name=="D2:threeprofit:BPQ")}
    b=dict(zip(LABELS,map(int,atom["bits"])));bg=b["A"]+b["D"]
    total=r+s+t
    for triple in TRIPLES:
        count=sum(b[label] for label in triple)
        out["D2:threeprofit:fixed:"+"".join(triple)]=F(5,3)*sh(total,bg+total)-sh(count,bg+count)
    return out


def decomposition(bits,r,s,t,weights):
    """Return raw constant_by_j, local scaled-feature coefficients, menu coefficients.

    All local features in `features` are interpreted as 120 times their raw
    per-client quantity; all constants/menu coefficients returned here are raw.
    """
    import numpy as np
    b=dict(zip(LABELS,bits));a=b["A"];d=b["D"];bg=a+d
    z={"R":r,"S":s,"T":t};ns=(r,s,t);total=bg+sum(ns)
    const=np.zeros(6);ec=np.zeros(3);hc=np.zeros(3)
    features={tag:{} for tag in ("AB","AE","Sbranch")}
    paths={"actual":"ABCDE","secondE":"AEUVW","thirdE":"ABEXY"}
    def add(tag,feature,value):features[tag][feature]=features[tag].get(feature,0)+value
    def payoff(n,den):return n/den if n else 0.
    for name,weight in weights:
        sp=name.split(":")
        if name=="F2D":const+=weight*(payoff(b["B"],sum(bits[:5]))-payoff(d,total))
        elif sp[0]=="D2" and sp[1].isdigit():
            pos=int(sp[1])-3;own=payoff(ns[pos],total);den=bg+sum(ns[:pos])+3-pos
            if sp[2]=="K":
                value=z[sp[3]] if sp[3] in z else b[sp[3]]
                const+=weight*(own-payoff(value,den))
            elif sp[2]=="sumopt":const+=weight*(5*own-np.arange(6)/den)
            elif sp[2].startswith("oldmenu"):
                menu=int(sp[2][-1]);const+=weight*5*own;ec[menu]-=weight/den
            elif sp[2]=="menu":
                fam="Sbranch" if sp[3]=="second" else sp[3]
                alphabet="UVW" if fam=="Sbranch" else "XY"
                feature="count-"+alphabet[int(sp[4])-1]
                const+=weight*5*own;add(fam,feature,-weight/den)
            else:raise ValueError(name)
        elif sp[0] in paths:
            path=paths[sp[0]];pos=int(sp[1])-1
            own=payoff(b[path[pos]],sum(b[label] for label in path))
            den=sum(b[label] for label in path[:pos])+5-pos
            const+=weight*(own-payoff(z[sp[3]],den))
        elif sp[0].startswith("oldmenu"):
            menu=int(sp[0][-1]);path=("ABCDE","AEUVW","ABEXY")[menu]
            pp=sum(b[label] for label in path[:3]);dd=(pp+1)*(pp+2);value=z[sp[2]]
            ec[menu]+=weight/(pp+1);hc[menu]-=weight/dd
            const+=weight*(-5*value/(pp+1)+np.arange(6)*value/dd)
        elif sp[0] in ("AB","AE"):
            own,den=("zx","dx") if sp[1]=="4" else ("zy","dy")
            add(sp[0],own,weight);add(sp[0],den,-weight*z[sp[2]])
        elif sp[0]=="secondindexed":
            own,den={"3":("zu","du"),"4":("zv","dv"),"5":("zw","dw")}[sp[1]]
            add("Sbranch",own,weight);add("Sbranch",den,-weight*z[sp[2]])
        elif name=="D2:threeprofit:opt":
            import math
            const+=weight*(50/3)*payoff(sum(ns),total)
            for j in range(6):
                value=0.
                for count in range(1,4):
                    if count<=j and 3-count<=5-j:
                        value+=math.comb(j,count)*math.comb(5-j,3-count)*count/(bg+count)
                const[j]-=weight*value
        elif name.startswith("D2:threeprofit:fixed:"):
            count=sum(b[label] for label in sp[3])
            const+=weight*(5/3*payoff(sum(ns),total)-payoff(count,bg+count))
        else:raise ValueError(name)
    return const,features,ec,hc
