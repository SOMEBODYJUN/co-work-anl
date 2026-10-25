# N5 induction: a paid root-share interface extracted from four-remaining slack

Status: direct derivation from the already proved arbitrary-background four-remaining
certificate; exact local arithmetic self-audited. It proves a conditional five-player
half bound, not the unrestricted target. No finite game search is used as proof.

Input: CAG-MODEL, five providers, arbitrary finite common catalog, every fixed full
ordered-history pure SPE. Empty/repeated themes and all history-dependent ties remain.
Write the actual path `(A,B,C,D,E)`, root profit `u1`, total welfare `W`, tail profit
`V=W-u1`, and any optimal five-tuple `(T1,...,T5)` with union size `O=OPT5`.
For a customer write `a=1_A`, `v=(b,c,d,e_actual)`, `k=|v|`, and
`j=sum_i 1_Ti`. Thus `u1_x=a/(a+k)` with zero numerator interpreted as zero.

The four-remaining theorem used here is
`research/current/customer_attraction/four_remaining_profit_bound.md`,
CA-FOUR-REMAINING-PROFIT-1499-750, including its corrected background terms.
Its exact identity is

    beta R_actual(p) - R_p(Q1,Q2,Q3,Q4)
      = G(p; actual, internal true deviation) + sum_x rho_p(actual_x,q_x,r_x,s_x),
    beta=1499/750, G>=0.

The same four-remaining SPE and its same internal true deviation can be used for all
comparison tuples. In particular, no independent branches or selectable replies are
being combined. Define

    r_p(v) = min_{q,r,s in {0,1}} rho_p(v,q,r,s),   p in {0,1}.

The original certificate's formula (11), or the direct independent reconstruction in
`audit_root_share_interface.py`, is the precise definition of rho. The complete exact
minima are:

| v | r_0(v) | r_1(v) |
| --- | ---: | ---: |
| 0000 | 0 | 0 |
| 0001 | 0 | 133/750 |
| 0010 | 1/750 | 2003/12000 |
| 0011 | 1/1500 | 61853/180000 |
| 0100 | 1/1500 | 251/3000 |
| 0101 | 39/500 | 6331/22500 |
| 0110 | 1/1000 | 7363/36000 |
| 0111 | 623/3000 | 26047/60000 |
| 1000 | 2747/12000 | 239/1200 |
| 1001 | 691/6000 | 14579/45000 |
| 1010 | 47/1500 | 22183/90000 |
| 1011 | 1919/12000 | 5177/12000 |
| 1100 | 0 | 15767/90000 |
| 1101 | 77/750 | 63893/180000 |
| 1110 | 1/4000 | 43349/180000 |
| 1111 | 1169/6000 | 41143/90000 |

All minima are nonnegative. Consequently, for every four comparison themes,

    R_a(Q1,Q2,Q3,Q4) <= beta V - sum_x r_a(v_x).                 (1)

This keeps a nonuniform background-sensitive payment absent from the simple total
profit interface. It is a consequence of the existing certificate, not a new premise.

## Exact optimal multiplicity and root-share payment

Apply (1) to each of the five four-subtuples of the fixed optimal five-tuple.
A customer with multiplicity j contributes

    f_a(j) = sum_{omitted i} (j-1_Ti)/(a+j-1_Ti)
           = (j-1) + (5-j)j/(a+j), if a=1, j>0;
    f_0(1)=4, f_0(j)=5 for j>=2; f_a(0)=0.

Equivalently for a=1 the positive-j values are `2,3,7/2,19/5,4`.
Define the exact nonnegative multiplicity credit

    delta(a,j)=f_a(j)/4 - 1_{j>0} + (a/2)1_{j>0}.

Then

    O <= (1499/600)V + |A intersect union(Ti)|/2
         - (5/4) sum_x r_a(v_x) - sum_x delta(a_x,j_x).        (2)

This is an exact paid improvement over the old coarse subset bound. For j>=2 the
positive delta is retained, rather than treating all optimal multiplicities as one.

Put `gamma=20233/24000`. Directly from the complete table,

    (1/2 - (5/4)r_1(v)) (1+|v|) <= gamma,                    (3)

with equality exactly at v=1100. Define another nonnegative customer credit on A:

    eta(v)=gamma/(1+|v|) - 1/2 + (5/4)r_1(v).

Let the single shared paid remainder be

    D = (1/2)|A minus union(Ti)|
        + sum_{x in A} eta(v_x)
        + (5/4)sum_{x not in A} r_0(v_x)
        + sum_x delta(a_x,j_x).                              (4)

Every term is nonnegative and all are computed from the same actual path and optimal
tuple. Combining (2), (3), and `sum_{x in A}1/(1+k_x)=u1` gives the unconditional
root-sensitive interface

    OPT5 <= (1499/600)W - (39727/24000)u1 - D.                (5)

In particular the five-player half bound is proved in the explicitly paid regime

    (39727/24000)u1 + D >= (299/600)W.                        (6)

A simpler sufficient condition is

    u1 >= (11960/39727)W  ~ 0.301054698316 W.                 (7)

No statement asserts (6) for every SPE. This extracted budget is not claimed to be outside the old 437-row indexed
slack cone: that template already includes the required actual second-to-last
theme deviation and its successor IC comparisons.

Closing the remaining low-root-share regime
requires a further shared payment; the ratio-only four-tail theorem does not provide
it. In particular, minimization of the certificate remainder deliberately discarded
the true internal reply labels, and those may be necessary for that final payment.

## Verification

Run `python audit_root_share_interface.py` from this directory, or the full path
from the repository root. The audit independently reconstructs the original exact
rho from its SPE slack definitions, checks all 256 local states for p=0,1, checks the
32 table entries and the exact maximizer in (3), and directly checks all optimal
membership subsets for the f and delta formulas. These are complete customer-wise
algebraic cases, not a finite-instance SPE search.
