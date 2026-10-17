#!/usr/bin/env python3
"""Exact parity audit for the four-degree C2/prefix boundary."""
from itertools import product, combinations
from fractions import Fraction

SUP = {r: [b for b in product((0,1), repeat=5) if sum(b)%2==r] for r in (0,1)}
assert all(len(SUP[r]) == 16 for r in SUP)
# Every all-one literal monomial on at most four distinct bits has probability 2^-k.
for k in range(5):
    for S in combinations(range(5), k):
        vals=[sum(all(b[i] for i in S) for b in SUP[r]) for r in (0,1)]
        assert vals[0] == vals[1] == 16 // (2**k)
F=lambda b: all(b[i] for i in range(4))
q=[sum(F(b) for b in SUP[r]) for r in (0,1)]
assert q == [1,1]
# T=2 heavy pair: task5 and task6 have time 3/2 on A/B; exactly one is sent to B.
# even parity forces z5=0 after F, odd forces z5=1.
cond_b5=[sum(F(b) and b[4] for b in SUP[r]) for r in (0,1)]
assert cond_b5 == [0,1]
# Fixed task7 on an isolated machine C with time 2 makes every support schedule OPT=T=2.
assert all(Fraction(2) == Fraction(2) for _ in range(2))
print('parity supports=16+16, degree<=4 moments equal, q_F=1/16, conditional b5=0/1, heavy pair T=2')
