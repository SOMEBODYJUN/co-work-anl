"""Exact genuine-IC attack on the static potential/last-price point.

Uses the 13 rational masses from static_potential_lp.py and splits each equally
among six disjoint optimal themes. It probes the actual chronological actions
A1,...,A6, especially the last two positions. This is not an SPE witness.
"""
from fractions import Fraction as F
from itertools import product

MASSES={
    0:F(159279,300121),27:F(156842,4501815),29:F(103968,1500605),
    30:F(103968,1500605),31:F(64046,6302541),32:F(717646,31512705),
    33:F(13112,1086645),34:F(12440,2100847),35:F(1328018,10504235),
    37:F(148268,4501815),38:F(148268,4501815),42:F(27664,4501815),
    44:F(1465682,31512705),
}
assert sum(MASSES.values())==1
TYPES=[(a,opt,z/F(6)) for a,z in MASSES.items() for opt in range(6)]
P=12

def utility(prefix,theme,suffix=()):
    acts=tuple(prefix)+(theme,)+tuple(suffix)
    ans=F(0)
    for mask,opt,z in TYPES:
        def has(a):return ((mask>>a)&1) if a<6 else int(a-6==opt)
        if has(theme):ans+=z/F(sum(has(a) for a in acts))
    return ans

def last_br(prefix):
    vals=[utility(prefix,a) for a in range(P)]
    v=max(vals)
    return [a for a,z in enumerate(vals) if z==v],v

def tail_two(prefix):
    vals=[]
    for a in range(P):
        br,pay=last_br((*prefix,a))
        source=[utility(prefix,a,(b,)) for b in br]
        vals.append((min(source),max(source),br,source,pay))
    return vals

def main():
    actual=(0,1,2,3,4,5)
    print('W',sum(z for mask,opt,z in TYPES if mask))
    print('terminal payoff',utility(actual[:5],5),'BR',last_br(actual[:5]))
    for i in range(5):
        print('actual payoff',i+1,utility(actual[:i],i,actual[i+1:]))
    vals=tail_two(actual[:4]); own=utility(actual[:4],4,(5,))
    print('two-player source actual',own)
    for a,(lo,hi,br,pays,v) in enumerate(vals):
        print('force',a,'minmax',lo,hi,'BR',br,'source payoffs',pays,'terminal payoff',v,'strict gain minimum',lo-own)

if __name__=='__main__':main()
