"""Independent Fraction audit of the random optimal permutation boundary."""
from fractions import Fraction as F
from itertools import product, permutations
from pathlib import Path
import hashlib
import json

N=3
THEMES=(frozenset({0,1}),frozenset({2,3}),frozenset({4}))
POLICY={():0,(0,):1,(1,):0,(2,):0,
        (0,0):1,(0,1):1,(0,2):1,
        (1,0):0,(1,1):0,(1,2):0,
        (2,0):1,(2,1):0,(2,2):0}

def complete(prefix):
    h=tuple(prefix)
    while len(h)<N:h+=(POLICY[h],)
    return h

def loads(path):
    return tuple(sum(x in THEMES[a] for a in path) for x in range(5))

def utility(path,seat):
    c=loads(path)
    return sum((F(1,c[x]) for x in THEMES[path[seat]]),F(0))

def potential(path):
    return sum((sum((F(1,k) for k in range(1,c+1)),F(0))
                for c in loads(path)),F(0))

def coverage(path):return sum(c>0 for c in loads(path))

def audit():
    histories=[h for k in range(N) for h in product(range(3),repeat=k)]
    assert set(POLICY)==set(histories)
    comparisons=0
    for h in histories:
        actual=complete(h)
        for a in range(3):
            alternative=complete(h+(a,))
            assert utility(actual,len(h))>=utility(alternative,len(h))
            comparisons+=1
    actual=complete(())
    assert actual==(0,1,1)
    assert [utility(actual,i) for i in range(N)]==[F(2),F(1),F(1)]
    assert coverage(actual)==4
    optimum=max(coverage(s) for s in product(range(3),repeat=N))
    comparison=(0,1,2)
    assert coverage(comparison)==optimum==5
    optimal_supports={frozenset(s) for s in product(range(3),repeat=N)
                      if coverage(s)==optimum}
    assert optimal_supports=={frozenset({0,1,2})}
    newest=[];prefix=[];ordered=[]
    for indices in permutations(range(N)):
        forced=tuple(comparison[j] for j in indices[:2])
        z=complete(forced)
        ordered.append((forced,z))
        newest.append(utility(z,1))
        prefix.append(utility(z,0)+utility(z,1))
    expected_newest=sum(newest,F(0))/6
    expected_prefix=sum(prefix,F(0))/6
    assert expected_newest==F(4,3)
    assert all(x==3 for x in prefix)
    assert expected_prefix==F(3)
    assert expected_prefix/2-expected_newest==F(1,6)>0
    # Ordered prefixes AB and BA have equal loads and optimal last values.
    ab=complete((0,1));ba=complete((1,0))
    assert loads((0,1))==loads((1,0))
    assert ab[-1]!=ba[-1]
    assert utility(ab,2)==utility(ba,2)==F(1)
    assert potential(ab)==potential(ba)==F(5)
    assert utility(ab,0)==F(2) and utility(ab,1)==F(1)
    # Direct true-deviation uniform interface check for this example.
    V=[]
    for i in range(N):
        V.append([utility(complete(actual[:i]+(theme,)),i) for theme in comparison])
    gap=F(N*optimum-(N-1)*coverage(actual))-sum((x for row in V for x in row),F(0))
    assert gap==F(-4)
    return {'complete_decision_histories':len(histories),'SPE_comparisons':comparisons,
            'index_permutations':len(ordered),'OPT_3':optimum,'actual_path':actual,
            'actual_welfare':coverage(actual),'comparison_tuple':comparison,
            'unique_optimal_support':[0,1,2],
            'expected_newest_payoff':str(expected_newest),
            'expected_prefix_total':str(expected_prefix),
            'exchangeability_deficit':str(expected_prefix/2-expected_newest),
            'same_load_last_payoff':str(utility(ab,2)),
            'same_load_terminal_potential':str(potential(ab)),
            'uniform_interface_violation_objective':str(gap),
            'all_checks_passed':True,
            'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}

if __name__=='__main__':
    out=audit()
    print(json.dumps(out,indent=2))
