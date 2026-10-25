# Root rigidity retaining the real reply to a penultimate copy

Status: exact 128-membership certificate, independent mathematical review
requested. This uses an additional ordered history and its true last reply.
The five-player half objective remains OPEN here.

## Statement and relation to the two earlier inequalities

In any five-player complete-history pure SPE of the common finite catalog
model, write u for the actual first player's final payoff and choose
M=max_(S in catalog)|S|. For every two legal topics T,Q,

    F_T(Q):=|Q\T|+|Q intersect T|/5
      <= (44/3)u+(13/5)M-(16/3)|T|.                (COPY-M)

The same displayed inequality remains valid for any other common upper
bound M for topic sizes. The chosen true maximum satisfies M<=5u by root
IC, and only this choice (or another upper bound <=5u) gives

    F_T(Q) <= u+(16/3)(5u-|T|).                    (COPY-DELTA)

For the chosen maximum, the right side of (COPY-M) minus the right side of
the 113/21 common-M bound is

    [5|T|-15u-2M]/105 <= [3M-15u]/105 <= 0.

Thus the real copy-reply relation weakly dominates the earlier two valid
root-rigidity inequalities. All ties, repeats, empty topics and equal sets
remain allowed. No anonymous or canonical continuation is imposed.

## Two paths in the same original strategy

Force root action T and follow the original strategy. Its actual branch is

    (T,B_2,B_3,B_4,B_5).

At its genuine penultimate history (T,B_2,B_3), force player 4 to choose the
legal topic B_5 and then use the **same original strategy** to set

    C = sigma_5(T,B_2,B_3,B_5).

The resulting second path is (T,B_2,B_3,B_5,C). Player 4 on that second path
is the specified deviator and is not being treated as an optimizer. Its
last player is a genuine optimizer. If the two ordered histories coincide,
the fixed strategy itself enforces their equal reply; the coefficient proof
allows a wider set of independent memberships, which is safe.

Let r,v_4,v_5 denote the root, penultimate and final payoffs in the first
branch. Let p_x=1_T+1_(B_2)+1_(B_3), b_x=1_(B_4), c_x=1_(B_5), d_x=1_C.
The needed nonnegative slacks are

    R  = u-r,
    K_j = M-|B_j|                          (j=2,3,4,5),
    L  = v_4 - sum_x c_x/(p_x+c_x+d_x),
    ZQ = v_5 - sum_(x in Q) 1/(p_x+b_x+1),
    ZC = v_5 - sum_x d_x/(p_x+b_x+1),
    CQ = sum_x d_x/(p_x+c_x+d_x)
              - sum_(x in Q) 1/(p_x+c_x+1).

Zero numerators over zero terminal loads are zero. L is genuine player-4
IC comparing B_4 with B_5 and retaining its real reply C. ZQ and ZC are
real player-5 comparisons at the first branch against Q and C. CQ is the
real last-player comparison at the copied history against Q. R is root IC,
and K_j use only the common catalog size cap. No size cap on C is needed
by this certificate. In particular, this mechanism retains more information
than replacing L by a worst-denominator floor.

## Exact identity and complete nonnegative type calculation

For a customer write

    t=1_T, q=1_Q, a=1_(B_2)+1_(B_3), b=1_(B_4), c=1_(B_5), d=1_C,
    ell=t+a+b+c,  ell_copy=t+a+c+d,
    r_x=t/ell, v4_x=b/ell, v5_x=c/ell.

Define L_x,ZQ_x,ZC_x,CQ_x by the preceding slack formulas customerwise, and
put

    rho = -(16/3)t-q/(1+4t)+(44/3)r_x
          +a/2+(11/15)b+(13/15)c
          -(4/15)L_x-(14/15)ZQ_x-(2/15)ZC_x-(1/15)CQ_x.   (1)

There is the exact identity

    (44/3)u+(13/5)M-(16/3)|T|-F_T(Q)
      = (44/3)R+(K_2+K_3)/2+(11/15)K_4+(13/15)K_5
        +(4/15)L+(14/15)ZQ+(2/15)ZC+(1/15)CQ+sum_x rho_x.  (2)

The size-cap weights sum to 1+24/15=13/5, proving the M coefficient. The
q coefficient in rho is

    -1/(1+4t)+14/[15(t+a+b+1)]+1/[15(t+a+c+1)].

For t=0 it is nonpositive. For t=1 both query denominators are at most 5,
so it is nonnegative. Thus q=1-t minimizes rho, independently of d. The
following 48 values give the entire remaining calculation. They cover all
128 binary memberships, including both orders when a=1.

| t | a | d | worst q | 900rho, bc=00 | bc=01 | bc=10 | bc=11 |
|---|---|---|---|---:|---:|---:|---:|
|0|0|0|1|0|30|0|630|
|0|0|1|1|60|0|0|540|
|0|1|0|1|0|410|400|1010|
|0|1|1|1|30|410|410|990|
|0|2|0|1|300|835|810|1445|
|0|2|1|1|320|840|820|1440|
|1|0|0|0|8400|2220|2340|760|
|1|0|1|0|8430|2220|2350|740|
|1|1|0|0|2250|590|630|170|
|1|1|1|0|2270|595|640|165|
|1|2|0|0|500|0|0|0|
|1|2|1|0|515|6|9|0|

All values are nonnegative. Equation (2) therefore proves (COPY-M) for every
input in the stated model. The arithmetic is independent of customer count,
catalog size and the number of equalities between displayed action labels.

## Coverage row and maximal-source row for joint use

For any five comparison topics covering O, summing (COPY-M) and using
sum_j F_T(T_j)>=|O|-(4/5)|T| gives

    OPT_5 <= (220/3)u+13M-(388/15)|T|.             (3)

When T is chosen as a topic attaining the common maximum M, (3) becomes

    15 OPT_5 + 193 M <= 1100 u.                    (4)

This choice is always legal since the catalog is finite and nonempty.
Taking M<=5u instead in (3) gives

    OPT_5 <= 9u+(388/15)(5u-|T|).                  (5)

The separate fixed-topic rows, their optimal-query aggregate (3), and the
maximal-source row (4) all retain the same common M. None alone proves the
half bound. The remaining obligation is to pay 2W-OPT_5 jointly with the
actual path and other genuine branches. Parent full-universe work is using
these valid rows; no numerical outcome is incorporated as a theorem here.

## Audit and discovery boundaries

`audit_copy_reply_rigidity.py` computes the raw slack definitions in exact
Fraction arithmetic, checks all 128 coefficient residuals and reconstructs
the full 48-entry table in `audit_copy_reply_rigidity.json`. It imports no
optimizer or old template evaluator. The universal proof is the exact slack
identity and complete membership calculation, not a finite game search.

`probe_copy_reply_rigidity.py` was numerical coefficient discovery only.
A further exploratory attempt to retain the third player's real deviation
to B_5 with its true last-two continuation did not change this particular
relaxed slope. Its floating run is not an impossibility result for other
three-tail uses, a welfare bound or an SPE counterexample.
