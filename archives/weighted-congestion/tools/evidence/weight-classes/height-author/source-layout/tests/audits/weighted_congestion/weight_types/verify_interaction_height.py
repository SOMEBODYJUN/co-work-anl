"""Exact finite audit for the interaction-height triangular potential draft.

All arithmetic uses Fraction. No external input, randomness, or numerical root.
Rational roots are chosen by d-1=t*(1+t+...+t**(k-1)).
This code checks finite fixtures; the general theorem uses the written proof.
"""
from fractions import Fraction as F
from itertools import combinations, product
import json,hashlib,platform,sys
from pathlib import Path


def powerset(n):
    return [frozenset(i for i in range(n) if mask >> i & 1) for mask in range(1 << n)]


def params(k, t):
    A = sum((F(t) ** j for j in range(k)), F(0))
    degree = int(1 + t*A)
    assert 1 + t*A == degree
    lam = [F(t)**j/A for j in range(k)]
    S = [sum(lam[:i+1], F(0)) for i in range(k)]
    assert sum(lam) == 1
    assert all(1+(degree-1)*(S[i-1] if i else 0) == A*S[i] for i in range(k))
    return A, degree, lam, S


def compatible(U, weights, ranks):
    return all(not (weights[i] > weights[j] and ranks[i] >= ranks[j])
               for i in U for j in U)


def potential(U, weights, ranks, cost, k, lam):
    value = F(0)
    for b in range(1, k+1):
        pi = list(range(k, b, -1)) + list(range(1, b+1))
        pos = {r:j for j,r in enumerate(pi)}
        order = sorted(U, key=lambda i:(pos[ranks[i]],i))
        load = F(0)
        part = F(0)
        for i in order:
            load += weights[i]
            part += weights[i]*cost(load)
        value += lam[b-1]*part
    return value


def endpoint_audit(weights, ranks, k, t):
    A, degree, lam, S = params(k,t)
    subsets = powerset(len(weights))
    valid = [U for U in subsets if compatible(U,weights,ranks)]
    checks = 0
    for mode in ('zero','constant','linear','top','mixed','shifted'):
        def cost(x):
            if mode == 'zero': return F(0)
            if mode == 'constant': return F(3,7)
            if mode == 'linear': return F(2,5)*x
            if mode == 'top': return x**degree
            if mode == 'mixed': return F(1,7)+F(2,5)*x+F(1,11)*x**degree
            y=x+F(4,3)
            return F(1,7)+F(2,5)*y+F(1,11)*y**degree
        pots = {U:potential(U,weights,ranks,cost,k,lam) for U in valid}
        for U in valid:
            for i in range(len(weights)):
                if i in U: continue
                V = U|{i}
                if V not in pots: continue
                Y = sum((weights[j] for j in V), F(0))
                h = weights[i]*S[ranks[i]-1]
                delta=pots[V]-pots[U]
                assert h*cost(Y) <= delta <= A*h*cost(Y), (mode,U,i)
                checks += 1
    return {'degree':degree,'k':k,'A':str(A),'weights':list(map(str,weights)),
            'ranks':ranks,'valid_subsets':len(valid),'invalid_subsets':len(subsets)-len(valid),
            'endpoint_marginal_checks':checks}


def global_game_audit():
    # Eight movable players have four distinct weights but interaction height 2.
    weights=list(map(F,[9,9,7,7,5,5,3,3]))
    ranks=[1,1,2,2,1,1,2,2]
    k,t=2,1
    A,d,lam,S=params(k,t)
    shared=[frozenset([0,1,2,3]),frozenset([0,1,6,7]),frozenset([4,5,6,7])]
    users=shared+[frozenset([i]) for i in range(8)]
    assert all(compatible(U,weights,ranks) for U in users)
    # Positive fixed backgrounds include several distinct weights; their count
    # and magnitude do not affect the movable interaction graph.
    background=[F(11,7), F(13,9)+F(17,11), F(0)]+[F(0)]*8
    def cost(e,x):
        if e < 3:
            y=x+background[e]
            return F(e+1,7)+F(2,5)*y+F(1,11)*y**d
        return F((e-2)**2,3)
    actions=[]
    for i in range(8):
        actions.append((frozenset(e for e,U in enumerate(shared) if i in U),frozenset([3+i])))
    def evaluate(s):
        U=[frozenset(i for i in range(8) if e in actions[i][s[i]]) for e in range(len(users))]
        load=[sum((weights[i] for i in V),F(0)) for V in U]
        resource_cost=[cost(e,load[e]) for e in range(len(users))]
        player_cost=[sum((resource_cost[e] for e in actions[i][s[i]]),F(0)) for i in range(8)]
        phi=sum((potential(V,weights,ranks,lambda x,e=e:cost(e,x),k,lam) for e,V in enumerate(U)),F(0))
        return player_cost,phi
    results={s:evaluate(s) for s in product(range(2),repeat=8)}
    checks=0
    for s,(C,phi) in results.items():
        for i in range(8):
            z=list(s);z[i]=1-z[i];z=tuple(z)
            Cz,phiz=results[z]
            h=weights[i]*S[ranks[i]-1]
            assert phiz-phi <= h*(A*Cz[i]-C[i]), (s,i)
            if C[i] > A*Cz[i]: assert phiz<phi
            checks+=1
    minphi=min(v[1] for v in results.values())
    minima=[s for s,v in results.items() if v[1]==minphi]
    for s in minima:
        for i in range(8):
            z=list(s);z[i]=1-z[i];z=tuple(z)
            assert results[s][0][i] <= A*results[z][0][i]
    return {'degree':d,'k':k,'A':str(A),'distinct_movable_weights':len(set(weights)),
            'states':len(results),'deviation_checks':checks,'global_minimizers':minima,
            'background':list(map(str,background))}


def outside_compatibility_obstruction():
    # With two unequal same-rank co-users the proposed marginal bound fails;
    # this is outside the theorem hypotheses, demonstrating why ranks cannot
    # be chosen afresh per step without checking the endpoints.
    weights=[F(9),F(5)];ranks=[2,2]
    A,d,lam,S=params(2,1)
    cost=lambda x:x**d
    U=frozenset([1]);V=frozenset([0,1]);i=0
    delta=potential(V,weights,ranks,cost,2,lam)-potential(U,weights,ranks,cost,2,lam)
    h=weights[i]*S[ranks[i]-1]
    lo=h*cost(sum(weights));hi=A*lo
    assert not compatible(V,weights,ranks)
    assert not lo <= delta <= hi
    return {'weights':list(map(str,weights)),'ranks':ranks,'degree':d,
            'lower':str(lo),'delta':str(delta),'upper':str(hi),'outside_hypothesis':True}


def realized_closed_word_audit():
    weights=[F(9),F(7),F(5)]
    ranks=[1,2,2]
    A,d,lam,S=params(2,1)
    word=[0,1,0,1,2,0,2,0]
    states=[frozenset()]
    for i in word: states.append(states[-1]^{i})
    assert states[-1]==states[0]
    arcs={(i,j) for U in states for i in U for j in U if weights[i]>weights[j]}
    assert arcs=={(0,1),(0,2)}
    assert all(compatible(U,weights,ranks) for U in states)
    def cost(x):
        y=x+F(11,7)  # a fixed nonmoving player's exact background
        return F(1,5)+F(2,3)*y+y**d
    phis=[potential(U,weights,ranks,cost,2,lam) for U in states]
    changes=[]
    for a,b,i,pa,pb in zip(states,states[1:],word,phis,phis[1:]):
        ca=cost(sum((weights[j] for j in a),F(0))) if i in a else F(0)
        cb=cost(sum((weights[j] for j in b),F(0))) if i in b else F(0)
        h=weights[i]*S[ranks[i]-1]
        assert pb-pa<=h*(A*cb-ca)
        changes.append(pb-pa)
    assert sum(changes,F(0))==0
    assert not compatible(frozenset([1,2]),weights,ranks)
    return {'weights':list(map(str,weights)),'word':word,'states':[sorted(U) for U in states],
            'actual_arcs':sorted(arcs),'actual_height':2,'potential_height':3,
            'endpoint_potential_telescope':str(sum(changes,F(0))),'steps':len(word),
            'all_steps_strict_improvement':False}


def main():
    fixtures=[
        ([F(9),F(9),F(7),F(7),F(5),F(5),F(3),F(3)],[1,1,2,2,1,1,2,2],2,1),
        ([F(11),F(11),F(9),F(7),F(5),F(3),F(1)],[1,1,2,3,1,2,3],3,2),
        ([F(5),F(5),F(5),F(3),F(1)],[1,2,3,2,3],3,1),
        ([F(2),F(2),F(2)],[1,1,1],1,2),
    ]
    out={'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'python_version':platform.python_version(),'command':' '.join(sys.argv),'seed':None,'method':'Fraction exact; fixed fixtures; no random seed or tolerance',
         'endpoint_fixtures':[endpoint_audit(*f) for f in fixtures],
         'global_game':global_game_audit(),
         'realized_closed_word':realized_closed_word_audit(),
         'outside_compatibility':outside_compatibility_obstruction()}
    boundary=0
    for n in range(1,9):
        w=[F(i+1) for i in range(n)]
        states=list(product((0,1),repeat=n))
        loads=lambda s:[sum((w[i] for i in range(n) if s[i]==b),F()) for b in (0,1)]
        for s0 in states:
            assert max(s0.count(0),s0.count(1)) >= (n+1)//2
        v=min(sum(x*x for x in loads(s0)) for s0 in states)
        for s0 in states:
            ls=loads(s0)
            if sum(x*x for x in ls)!=v:continue
            for d0 in (1,2,3,15):
                for i in range(n):assert ls[s0[i]]**d0 <= (ls[1-s0[i]]+w[i])**d0
                boundary+=1
    out['two_bin_exact_PNE_high_actual_height_checks']=boundary
    print(json.dumps(out,ensure_ascii=False,indent=2))


if __name__=='__main__':main()
