"""Definition-level exact audit of the customerwise covariance obstruction."""
from fractions import Fraction as F


def audit(strict=False):
    if strict:
        sets={'A':{'x','z'},'B':{'y1','y2','y3'},'D':{'x','y1','y2','y3'},'E':{'z','w1','w2'}}
    else:
        sets={'A':{'x','z'},'B':{'y'},'D':{'x','y'},'E':{'z','w'}}
    reply={'A':'D','B':'E','D':'E','E':'D'}
    actions=tuple(sets)
    universe=set.union(*sets.values())

    def payoff(a,b):
        return sum((F(1,1+(v in sets[b])) for v in sets[a]),F())

    comparisons=0
    for a in actions:
        prescribed=payoff(reply[a],a)
        for b in actions:
            alternative=payoff(b,a)
            assert prescribed>=alternative
            if strict and b!=reply[a]:
                assert prescribed>alternative
            comparisons+=1
    for a in actions:
        assert payoff('D',reply['D'])>=payoff(a,reply[a])
        if strict and a!='D':
            assert payoff('D',reply['D'])>payoff(a,reply[a])
        comparisons+=1

    p={'A':F(1,2),'B':F(1,2)}
    q={v:sum((p[a] for a in p if v in sets[a]),F()) for v in universe}
    D={v:sum((p[a]*F(v in sets[a],1+(v in sets[reply[a]])) for a in p),F()) for v in universe}
    C={v:sum((p[a]*q[v]/(1+(v in sets[a])+(v in sets[reply[a]])) for a in p),F()) for v in universe}
    H0=F(1,1+('x' in sets[reply['B']]))
    H1=F(1,1+('x' in sets[reply['A']]))
    assert (q['x'],H0,H1,D['x'],C['x'])==(F(1,2),F(1),F(1,2),F(1,4),F(1,3))
    assert C['x']-D['x']==F(1,12)
    J=sum((p[a]*q[v]*F(v in sets[a],(1+(v in sets[reply[a]]))*(2+(v in sets[reply[a]]))) for a in p for v in universe),F())
    slack=sum((p[a]*p[b]*(payoff(reply[a],a)-payoff(reply[b],a)) for a in p for b in p),F())
    assert sum(D.values())-sum(C.values())==slack+J
    if not strict:
        assert (sum(D.values()),sum(C.values()),slack,J)==(F(5,4),F(5,6),F(1,8),F(7,24))
    actual=(sets['D']|sets['E'])
    optimum=max(len(sets[a]|sets[b]) for a in actions for b in actions)
    assert len(actual)==optimum==len(universe)
    print({'strict':strict,'histories':5,'comparisons':comparisons,'W':len(actual),'OPT2':optimum,'Hx0':str(H0),'Hx1':str(H1),'Cx-Dx':str(C['x']-D['x']),'D-C':str(sum(D.values())-sum(C.values()))})


if __name__=='__main__':
    audit()
    audit(strict=True)
