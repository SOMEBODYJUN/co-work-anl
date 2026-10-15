# A sharp obstruction to the complementary multicolumn extension

Claim ID: **WC-R1-MULTICOLUMN-2-v1**. Date: 2026-10-14.

Status: complete direct proof below; exact finite checks are separate evidence;
independent internal review requested. This is a restricted-family obstruction,
not an upper bound for WC-TARGET v1 and not an improvement of its lower bound.
Authoring contribution: R1 internal agent `/root/new_lower`.

## Exact objects and scope

Fix integers q >= 3 and n >= 1, a light weight 0 < w <= 1, and any
nonnegative nondecreasing functions f,g on nonnegative loads. There is one
weight-1 heavy player and n weight-w light players. Column j has a main
resource r[j,0] of cost f and n private satellite resources r[j,i] of cost g.
The heavy player chooses all n+1 resources of one column. Light player i
chooses one column j, using its main resource r[j,0] together with its own
satellite r[l,i] in every column l != j. Every player has q strategies.

**Theorem. Every such game has a 2-PNE.** In particular this holds for all
nonnegative-coefficient polynomial f,g of every degree. For q=3 the constant
2 is asymptotically sharp even for f(x)=x and g(x)=beta*x^d.

The weight restriction w <= 1 is an actual hypothesis. No claim is made for
larger light weights, unequal light weights, nonidentical satellite costs,
or a different incidence pattern. Arbitrary zeros of f,g are allowed.

Dependencies: finite discrete minimization and monotonicity only. The
2-column construction in Christodoulou et al., arXiv:2002.07466v3, Section 3,
motivates this extension; its theorem is not used in this proof.
Primary source inspected after independently reconstructing the state costs:
https://arxiv.org/html/2002.07466v3#S3.

## Exact costs

Fix the heavy player's column h. Put

    b = g(w), c = g(1), B = g(1+w), so 0 <= b <= c <= B.

Let t_j be the number of light players choosing main column j, and t=t_h.
A light player on the heavy column, when that column has r light players,
has cost

    A(r) = f(1+r*w) + (q-1)*b.

A light player on another column, when that column has r light players,
has cost

    D(r) = f(r*w) + B + (q-2)*b.

The heavy player's cost when choosing a column containing r light main
choices is

    F(r) = f(1+r*w) + (n-r)*B + r*c.

These formulas include the satellite resources that remain occupied after
a deviation. In particular a light player's new main occupancy is the old
target occupancy plus one; the heavy player's target main occupancy is
unchanged by her move.

## A balanced exact equilibrium of the light players

With h fixed the light players have the finite exact potential

    Psi(t_1,...,t_q)
      = sum_{r=1}^{t_h} A(r)
        + sum_{j != h} sum_{r=1}^{t_j} D(r).

A global minimum is an exact equilibrium among light deviations. Such a
minimum can be selected so that the q-1 nonheavy columns have occupancies
differing by at most one: moving from occupancy u to v when u >= v+2 changes
the potential by D(v+1)-D(u) <= 0. From a global minimum this change is zero;
repeating balancing transfers terminates, for example by decreasing the sum
of squared nonheavy occupancies.

Choose such a balanced minimum. Write v for the smallest nonheavy occupancy.
For every nonheavy target occupancy u,

    v <= u <= v+1,   u <= ceil((n-t)/(q-1)).

The light equilibrium conditions used below are

    A(t) <= D(v+1)       if t > 0,
    D(u) <= A(t+1)       if u > 0.

## Every heavy deviation improves by at most two

All inequalities are written without division, so zero costs are covered.
Fix a nonheavy target column with occupancy u.

If t=u, the heavy costs coincide. If t>u, then t>=1, and
(v+1)*w <= 1+u*w because w<=1 and v<=u. Thus the first light equilibrium
condition gives

    f(1+t*w) - f(1+u*w) <= B-b.

Consequently

    F(t)-F(u)
      <= B-b - (t-u)*(B-c)
      <= c-b
      <= F(u),

where the last inequality follows from F(u)>=n*c>=c and b>=0.

Now suppose t<u. Monotonicity of f gives

    F(t)-F(u) <= (u-t)*(B-c).

If 2*u <= n+t, the right side is at most (n-u)*B <= F(u).
The balancing bound and q>=3 imply

    2*u <= 2*ceil((n-t)/2) <= n-t+1.

Hence 2*u <= n+t unless t=0 and 2*u=n+1. In that exceptional case u>=1,
and the second light equilibrium condition reads

    B-b <= f(1+w)-f(u*w) <= f(1+u*w).

Also f(1+u*w)>=f(1), so

    2*f(1+u*w)-f(1) >= B-b.

Using 2*u=n+1 now yields

    2*F(u)-F(0)
      = 2*f(1+u*w)-f(1) - B + 2*u*c
      >= 2*u*c-b
      >= 0.

Thus F(t)<=2*F(u) for every heavy deviation. The light players are already
at exact best responses, so this selected profile is a 2-PNE. This proves
the theorem for every n, including n=1, and all zero-cost degeneracies.

## Sharper bound at fixed n and q

For n>=2 the same selected state is a U(n,q)-PNE, where

    U(n,q) = min(2,
                 max(1+1/n,
                     n/(n-ceil(n/(q-1))))).

Indeed, for t>u the preceding difference bound c-b, together with F(u)>=n*c,
implies F(t)<=(1+1/n)*F(u), including c=0. For t<u, if B=0 then F(t)<=F(u).
Otherwise F(u)>0 and

    F(t)/F(u) <= (n-t)/(n-u)
                  <= n/(n-ceil(n/(q-1))).

The denominator is positive for n>=2 and q>=3. The last inequality follows
from n-t<=n and u<=ceil(n/(q-1)). Taking the better of this bound and 2 gives
the formula. For each fixed q>=3, U(n,q) tends to (q-1)/(q-2) as n grows.

## Explicit polynomial family approaching the constant two

Take q=3 and any integer n>=4, and set

    d=n^3,  w=1/n^2,  f(x)=x,
    beta = 1/[2*(1+w)^d],   g(x)=beta*x^d,
    L_n = 2*n/(n+3).

These are legal WC-TARGET polynomial games with rational positive weights
and coefficients. Here B=1/2, c=beta, b=beta*w^d. The binomial inequality
(1+1/n^2)^(n^3) >= 1+n gives beta<1/(2*n).

Consider **every** pure profile. If some light player chooses the heavy
column, that player's current cost is at least 1. After moving to either
other column her main load is at most n*w=1/n, while the satellite cost is
B+b. Her deviation cost is strictly less than

    1/n + 1/2 + 1/(2*n) = (n+3)/(2*n).

Her improvement factor is therefore strictly greater than L_n.

Otherwise the heavy column has zero light players. Of the two other
columns one has u>=n/2 light players. Since

    w+beta < 1/n^2 + 1/(2*n) <= 1/2,

the heavy player moving to that column has cost

    F(u) = 1+n/2-u*(1/2-w-beta)
         <= 1+n/4+n*(w+beta)/2
          < (n^2+5*n+2)/(4*n).

Her current cost is F(0)=(n+2)/2, so the improvement factor is greater than

    2*n*(n+2)/(n^2+5*n+2) > 2*n/(n+3) = L_n.

Thus this family has no L_n-PNE (and, in particular, no alpha-PNE for
1<=alpha<L_n). Since L_n tends to 2 and the upper bound is 2, the supremum
of the best-equilibrium approximation factors in the q=3 complementary
multicolumn family equals 2. This establishes sharpness of the topology
obstruction, not a new superconstant lower bound for the full model.

## Asymptotic sharpness for every fixed q

Fix q>=3 and put m=q-1, lambda=m/(m-1), B=1/lambda. For the same d=n^3,
w=n^-2, f(x)=x, take beta=B/(1+w)^d. Then beta tends to zero and
b=beta*w^d tends to zero. If an aligned light player exists, its improvement
factor is at least

    1/[1/n+B+(q-2)*b] -> lambda.

If no aligned player exists, a nonheavy column has u>=n/m. For all
sufficiently large n, B-w-beta>0, and the heavy deviation ratio is at least

    (1+n*B)/[1+n*B*(1-1/m)+n*(w+beta)/m] -> lambda.

Both bounds cover every profile. Combined with U(n,q), this proves that
the worst best-equilibrium factor among these q-column n-light-player
games tends to (q-1)/(q-2) as n tends to infinity. The supremum here allows
all nonnegative nondecreasing f,g and 0<w<=1; the matching lower examples
are polynomial, with their degree increasing with n.

## A separate asymmetric two-column sufficient condition

For reference, the original incidence pattern also permits unequal light
weights w_i>0 and private satellite coefficients beta_i>=0. Let W=sum_i w_i,
the two main costs be x^k, and satellite i cost beta_i*x^d. The following
explicit inequalities suffice for nonexistence of alpha-PNE:

    1+sum_i beta_i*(1+w_i)^d
      > alpha*((1+W)^k+sum_i beta_i),

    (1+w_i)^k+beta_i*w_i^d
      > alpha*(W^k+beta_i*(1+w_i)^d)     for every i.

If no light player shares the heavy main resource, the first inequality
attacks the heavy player. Otherwise any sharing light player i has current
cost at least the second left side and deviation cost at most the second
right side divided by alpha. This is a sufficient all-profile criterion,
not a statement of necessity or a claim that asymmetry improves the known
optimized symmetric family. The multicolumn obstruction does not cover
this asymmetric family.

## Evidence and remaining obligations

`verify.py` checks the displayed cost formulas against direct resource-load
recomputation on all small pure profiles, finds the selected balanced light
equilibria, and verifies the 2 and U bounds using exact rational arithmetic.
It also verifies the explicit sharpness inequalities on a finite n range.
`evidence.json` records the actual completed run. These checks neither
replace nor extend the quantified proof above.

Counterevidence/objections: none known to the stated theorem; extension to
unequal weights is not justified. Main-target ambition remains open: one
must change the incidence pattern or exploit another asymmetry, since
merely adding complementary columns creates balanced escape profiles.

Related files: `verify.py`, `evidence.json`; `../../../MODEL.md` and
`../../../PRIOR_ASSETS.md` are the target model and prior-mechanism entry.


---
整理来源与当前文件用途见[逐文件登记](../../../weighted_congestion_frontier/FILES.md)。程序统一通过 `python3 tests/audits/weighted_congestion/replay.py --list` 选择；历史命令、输出摘要与源码哈希属于原冻结版本。
