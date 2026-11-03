# N5 induction: a paid two-prefix interface from the sharp three-tail certificate

Status: new exact interface extracted from the existing arbitrary-background
three-remaining certificate. A self-contained Fraction audit passes. It proves a
conditional half bound, and does not claim that all five-player SPE meet its condition.

Input and quantifiers are CAG-MODEL: five unit providers, arbitrary finite unit clients
and common finite catalog, any fixed full ordered-history pure SPE, all ties, all
empty/repeated themes. Actual path `(A,B,C,D,E)`, actual welfare `W`, prefix final
profit `P=u1+u2`, tail final profit `V=u3+u4+u5=W-P`. For a customer put
`p=1_A+1_B` and `v=(c,d,e)=(1_C,1_D,1_E)`, `k=|v|`. Thus
`P_x=p/(p+k)`, with zero numerator interpreted as zero. For a fixed optimal five-tuple,
let `j` be that customer's multiplicity and `o=1_{j>0}`.

## Exact retained remainder

Use CA-THREE-REMAINING-PROFIT-5-3 in
`research/current/customer_attraction/three_remaining_profit_bound.md`, together with
its exact quadratic coefficient identity, not just its total-profit conclusion.
For any three comparison themes, write their customer multiplicity `d in {0,1,2,3}`.
The certificate gives

    (5/3)V - R_p(T1,T2,T3) = G/30 + sum_x N_x/(30D3(p_x)),
    G>=0, D3(p)=(p+1)(p+2)(p+3).

Here `q,r` are the two true replies following a deviation to this subgame's actual
last theme, and `ell` is the sum of its three true final replies to the comparison
queries. The exact numerator is the following self-contained formula. Put

    P0(p)=0, P1(p)=p²+5p+6, P2(p)=p²+4p+3, P3(p)=p²+3p+2.

For v=(a,b,c), s=a+b+c,

    N(p;v,q,r,d,ell)
      = (50s-29a-36b-57c) P_s(p) - 30d P_d(p)
        + (6q+9r) P_3(p) + (17d+2ell) P_(a+b+1)(p)
        + 12d P_(a+1)(p) - 4d ell (3-2a+p)
        + (14c-3r) P_(c+q+r)(p) + d P_(c+q+1)(p).

The existing theorem proves N>=0 for every p>=0 and all these legal memberships.
Define its retained, comparison-sensitive remainder

    r3(p,v,d)=min_{q,r in {0,1}, ell in {0,1,2,3}}
                    N(p;v,q,r,d,ell)/(30D3(p)).                 (1)

There are 16 minimization states per (p,v,d), 96 minima for p=0,1,2. Their complete
exact values are in `audit_two_prefix_interface.json`; the accompanying standalone
script reconstructs them from the displayed formula. This enlarges the true reply
range for minimization and therefore cannot assume selectable/fake true replies.
It only discards positive credit. The same original true three-tail SPE supports
all comparisons.

For global optimal multiplicity j define

    H3(p,v,j)=sum_{d=0}^3 C(j,d) C(5-j,3-d)
                          [d/(p+d)+r3(p,v,d)].                 (2)

Illegal binomial terms and zero-numerator profit terms are zero. Summing the sharp
three-tail certificate for the ten optimal indexed triples proves the valid row

    (50/3)V >= sum_x H3(p_x,v_x,j_x).                           (3)

Keeping r3's dependence on d is important: it retains even the d=0 remainders from
triples that do not cover a customer. This is stronger than applying the uniform
5/3 ratio to the same ten triples.

## Shared prefix payment

For p>0, put

    M(p,v,j)=(1_{j>0}-H3(p,v,j)/6)*(p+|v|)/p.

Direct substitution of (1), (2) gives the following complete maxima over j=0,...,5.
Each maximum is attained at j=1; no game or strategy enumeration is involved.

| v | max_j M(1,v,j) | max_j M(2,v,j) |
| --- | ---: | ---: |
| 000 | 1/2 | 2/3 |
| 001 | 401/540 | 59/72 |
| 010 | 37/90 | 491/720 |
| 011 | 17/40 | 11/15 |
| 100 | 7/45 | 43/80 |
| 101 | 17/72 | 109/180 |
| 110 | 13/72 | 521/900 |
| 111 | -2/135 | 193/360 |

The largest value is gamma=59/72. At p=0, `H3/6 >= 1_{j>0}`:
the uncorrected optimal-triple profile is at least 6 for j>0 and r3>=0.
Thus for every customer the single paid credit

    D3_x = gamma P_x - 1_{j>0} + H3(p_x,v_x,j_x)/6             (4)

is nonnegative, including customers outside the actual coverage. Put D3=sum_x D3_x.
Divide (3) by six, and use the actual identity `V+P=W`, obtaining

    OPT5 <= (25/9)W - (47/24)(u1+u2) - D3,  D3>=0.            (5)

In particular half coverage holds in the explicit paid regime

    (47/24)(u1+u2) + D3 >= (7/9)W.                            (6)

A simpler sufficient condition is

    u1+u2 >= (56/141)W = 0.397163120567... W.                  (7)

This complements the first-prefix interface in `root_share_interface.md`, which
proves half when u1>=11960/39727 W, and has its own stronger fine-credit condition.
Neither interface by itself proves that every SPE is in one of the paid regimes.
For the actual tail, its sharp-three root deviation and final menus are already
present in the old 437-row indexed template. Thus this extracted budget need not
add a new constraint to that larger template; it strengthens the ratio-only API,
not a demonstrated best all-SPE bound. Exact testing by the branch-geometry agent
found its actual/second/indexed-tail instances strictly feasible at the old
437-row primal, so this payment does not eliminate that known relaxation point.
The remaining obligation is a shared payment for paths with simultaneously low
first-prefix profit, low two-prefix profit, and insufficient fine credits.

## Audit and scope

`audit_two_prefix_interface.py` uses Fraction arithmetic and imports no prior audit,
LP package, or SPE search. It checks all 1536 exact local numerator/remainder states,
all 96 minima, all 144 (p,v,j) profiles, the exact maxima above and all customer-level
identities turning (3) into (5). It independently checks the N formula against the
expanded slack formula, retaining zero terms correctly. The complete finite local
algebraic table is a universal client-wise certificate; it is not evidence from
finitely many games.
