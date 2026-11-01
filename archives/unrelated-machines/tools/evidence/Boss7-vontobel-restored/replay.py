"""Exact finite checks of VK2005 v1 examples and a printed Lemma 24 error.
This is not a decoder, a generic LP solver, or a scheduling reduction.
"""
from fractions import Fraction as F
from itertools import product
import hashlib,json
from pathlib import Path

ROOT=Path(__file__).resolve().parent

def realizes(H,nu,local):
    # local[j] lists (local codeword over row support, rational multiplicity).
    def lcm(a,b):
        from math import gcd
        return a*b//gcd(a,b)
    M=1
    for rows in local:
        for _,q in rows:M=lcm(M,q.denominator)
    for q in nu:M=lcm(M,q.denominator)
    ones=[int(M*q) for q in nu]
    labels=[[int(a<ones[i]) for a in range(M)] for i in range(len(nu))]
    permutations={}
    for j,row in enumerate(H):
        I=[i for i,a in enumerate(row) if a]
        expanded=[]
        for word,q in local[j]:
            assert len(word)==len(I) and sum(word)%2==0
            expanded += [word]*int(M*q)
        assert len(expanded)==M
        for k,i in enumerate(I):
            pools={0:iter(range(ones[i],M)),1:iter(range(ones[i]))}
            permutations[j,i]=[next(pools[word[k]]) for word in expanded]
            assert sorted(permutations[j,i])==list(range(M))
        for a in range(M):
            assert sum(labels[i][permutations[j,i][a]] for i in I)%2==0
    assert [F(sum(x),M) for x in labels]==list(nu)
    return {'degree':M,'ones_per_type':ones,'permutations_check_to_bit':{f'{j},{i}':p for (j,i),p in permutations.items()},'all_cover_parities_even':True,'projection':[str(x) for x in nu]}

H=[[1,1,1,0],[0,1,1,1]]
nu=[F(2,3),F(2,3),F(2,3),F(0)]
local=[[(w,F(1,3)) for w in [(0,1,1),(1,0,1),(1,1,0)]], [((0,0,0),F(1,3)),((1,1,0),F(2,3))]]
cover=realizes(H,nu,local)
# Motivating example P(H)={(t,t,t):0<=t<=2/3}; test exact endpoints.
H0=[[1,1,0],[1,1,1],[0,1,1]]
code=[w for w in product([0,1],repeat=3) if all(sum(x*y for x,y in zip(w,r))%2==0 for r in H0)]
assert code==[(0,0,0)]
assert 3*F(2,3)==2
# Printed Lemma24 equality fails: z is in the cone but cannot project from a cover.
z=[1,1,1]
cone=all(z[i]<=sum(z[k] for k in range(3) if k!=i) for i in range(3))
assert cone and sum(z)%2==1
# Every unscaled cover count has even sum for the sole parity check,
# by summing all M lifted parity equations modulo 2, for every M.
result={'source_sha256':hashlib.sha256((ROOT/'vontobel-koetter-2005-v1.pdf').read_bytes()).hexdigest(),'scope':'Exact finite examples and a universal parity obstruction; no generic solver or algorithmic theorem','example4_7_57':cover,'motivating_example':{'codewords':code,'nonzero_polytope_endpoint':['2/3']*3},'lemma24_printed_equality_counterexample':{'H':[[1,1,1]],'z':z,'cone_inequalities':cone,'z_parity':sum(z)%2,'not_an_unscaled_cover_pseudocodeword':'For every M the sum of all lifted even-check equations forces total ones even; z has total ones 3.'}}
(ROOT/'replay-output.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False,indent=2))
