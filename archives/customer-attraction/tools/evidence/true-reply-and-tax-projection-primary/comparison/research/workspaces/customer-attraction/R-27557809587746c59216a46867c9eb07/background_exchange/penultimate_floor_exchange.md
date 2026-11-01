# Root near-saturation exchange: penultimate credibility and a sharp projection boundary

Status: analytic candidate, 2026-10-21. The proof below uses a genuine comparison
branch of a complete ordered-history pure SPE. It is not a proof of Q-CAG-HALF,
which remains OPEN. The sharp examples in Section 3 are explicitly projections,
not SPE examples. No external review or novelty claim is made.

## 1. Exact statement

Use CAG-MODEL: common finite catalog, unit clients/providers, arbitrary complete
ordered-history pure SPE and arbitrary history-dependent ties. Let m>=3,
K=max_T |T|, and let u be the actual root player's payoff. For any size-K topic C,
and any legal topic D, put E=m u-K. Define

    H=3m^2-7m+2,
    c_m=1+m(m-1)/2 + m(m-3)(m-1)^2/H
       =(m-1)^2-m^2(m-3)^2/(2H).

Then E>=0 and

    m|D\C|+|D intersect C| <= K+c_m E.             (1)

For m=3,4,5 the coefficients are respectively 4,95/11,311/21. For every m>=4,
c_m<(m-1)^2, the previous terminal-only coefficient. At m=2 the previously proved
coefficient 1 remains available; the present proof is only for m>=3.

By the existing non-recount union argument, (1) implies

    OPT_m <= (2-1/m)K+c_m E.

This still does not bound E by a global welfare budget.

## 2. Proof retaining the penultimate floor

At the root, really choose C and then follow the given complete strategy. Write
this comparison branch as C,A_2,...,A_(m-2),P,L. Its root payoff is v<=u. Every
client of C has branch load q_x>=1. Define

    e=m v-K >=0,
    d=sum_(x in C)(m-q_x),
    d_P=|C\P|, d_L=|C\L|, r=|L\C|,
    a=(m-2)/(m-1), beta=(m+1)/(2(m-1)).

The standard exact denominator identity gives d<=(m-1)e. Maximality of |C| gives
|A_j\C|<=|C\A_j| for every action, so r<=d_L and the outside-C incidence of the
m-3 intermediate actions preceding P is at most d-d_P-d_L.

Let p,t be the penultimate and final players' actual payoffs on this branch.
On P intersect C, p and v have identical summands. On C\P the load is at most
m-1, while each client in P\C contributes at most 1. Consequently

    p-v <= |P\C|-d_P/(m-1) <= a d_P.           (2)

At the true penultimate node, deviation to L has worst-response floor
sum_(x in L)1/(b_x+2). On L intersect C this is at least (K-d_L)/m. For a client
of L\C, b_x counts only the m-3 intermediate actions before P. Integer z>=0
satisfies

    1/(z+2) >= 1/2-z/6.                       (3)

(The difference is z(z-1)/(6(z+2))>=0.) Using the outside incidence budget,
penultimate optimality therefore gives

    p >= (K-d_L)/m+r/2-(d-d_P-d_L)/6.

Combine with (2), v=K/m+e/m, d_P<=d-d_L and a-1/6>0:

    r <= 2e/m+2a d-2(a-1/m)d_L.              (4)

This is the new credibility restriction. The original root proof merely used
r<=d_L.

For the final player, cancellation on L intersect C gives

    t-v <= r-d_L/(m-1).

At the same true terminal history, deviation to D has payoff at least

    |D intersect C|/m + |D\C| -(d-d_L)/2.

Here 1/(z+1)>=1-z/2 for every integer z>=0, and the preceding outside-C incidence
is at most d-d_L. Terminal optimality yields, with Q=m|D\C|+|D intersect C|,

    Q/m <= v+d/2+r-beta d_L.                 (5)

For m>=3 we have 1-beta>=0. Set A=2e/m+2a d and B=2(a-1/m)>0. The two bounds
r<=d_L and r<=A-B d_L imply for every d_L>=0

    r-beta d_L <= min{(1-beta)d_L, A-(B+beta)d_L}
               <= (1-beta) A/(1+B).

There is no assumption that the crossover lies in [0,d]; extending the domain
can only weaken this upper bound. Since 1+B=H/[m(m-1)], (5) implies

    Q/m <= v+d/2 +(m-3)e/H
                       +m(m-2)(m-3)d/[(m-1)H]
         <= K/m+e[1/m+(m-1)/2+(m-3)(m-1)^2/H].

The second step uses d<=(m-1)e and nonnegative coefficients. This proves
Q<=K+c_m e<=K+c_m E. Empty C or all-zero instances cause no division by K or e.
Every comparison used the given strategy's actual response at the stated
ordered history; no terminal action was frozen after an earlier deviation.

## 3. How much credibility has been used: an exact sharp projection

The coefficient c_m is sharp for the following retained-row system: maximum
sizes, exact comparison-branch root payoff, all-topic worst-response floors at
the penultimate node, and all-topic true terminal best responses. This statement
is about that necessary projection only, not about a full SPE.

For integer m>=3 define six disjoint unit-client groups with membership among
four legal topics C,P,L,D as follows:

| Group | Interested topics | Number of clients |
|---|---|---:|
| X_1 | C,P | X=4(m-1)^3 |
| X_2 | L,D | X |
| Y_1 | C,L | Y=2m(m-1)(m-3) |
| Y_2 | P,D | Y |
| Z | C,P,L | Z=m(m-3)(m^2-3m+4) |
| F | D | F=4(m-3) |

Consider the branch C^(m-2),P,L. Its first m-2 actions all use C. The three
branch topics have common size K=X+Y+Z. Topic D has size X+Y+F<=K, because
Z-F=(m-3)(m-2)(m^2-m+2)>=0. Put J=H/2, a positive integer. The root value is

    v=(X+Y)/(m-1)+Z/m,
    e=m v-K=(X+Y)/(m-1)=4J.

Here v is the root value ON THIS PROJECTION BRANCH; it is not asserted to be the
root payoff of a full SPE. Since D is disjoint from C,

    [m|D\C|+|D intersect C|-K]/e = c_m.        (6)

The useful parameter identities are

    Y/X=m(m-3)/[2(m-1)^2],
    Z/m=F+Y(1/2-1/(m-1)).

The penultimate payoff is p=X/(m-1)+Y+Z/m. Its worst-response floors for C,P,L,D
are respectively

    K/m, (X+Z)/m+Y/2, (Y+Z)/m+X/2, (X+Y+F)/2.

The last two equal p, and the first two do not exceed p. Thus *every* legal
penultimate floor holds. The final payoff is t=X+Y/(m-1)+Z/m. Terminal deviations
to C,P,L,D have values

    X/m+Y/(m-1)+Z/m,
    X/m+Y/2+Z/m,
    t,
    X+F+Y/2.

The last equals t; the first two do not exceed t (Y<X/2 and (m-1)/m>=2/3 suffice).
Therefore all actual terminal best responses hold. All maxima and all these
floors/BRs coexist with exact equality (6).

This family can fail genuine penultimate optimality despite passing all floors.
For m=4, X=108,Y=24,Z=32,F=4, the branch is C,C,P,L and p=68. After penultimate
deviation D, the final player's unique best topic is L, giving the deviator
108/2+24+4=82>68. Thus this branch is not a complete SPE. The six-group family
sharpens the boundary: a better coefficient than c_m requires some additional
intermediate strategic comparison, rather than more exact treatment of the
same floors and terminal BRs.

## 4. Relation to the old terminal-only boundary

Even before penultimate floors, the old coefficient (m-1)^2 is exact for its
retained system: two disjoint topics C,L, each of size m-1, and branch
C^(m-1),L. The comparison-branch root value is v=1, K=m-1, e=1; D=L gives
Q-K=(m-1)^2, and L is a strict terminal best response. For m>=4 the penultimate
player can instead choose L; the final player then strictly chooses L, and the
penultimate deviation payoff (m-1)/2 exceeds 1. These are projections, not SPE
or half-coverage counterexamples. This explains exactly why polishing the
terminal constants cannot improve the old coefficient.

## 5. Computation and remaining obligation

`exact_terminal_projection.py` numerically recovers the old coefficient for
m=2,...,8. `middle_floor_projection.py` numerically recovers c_m from all
last-two floors and terminal BRs for m=3,...,9; additional earlier branch floors
improve it further from m=5 onward. `two_remaining_projection.py` adds every
retained-overlap two-remaining tax row; at these tested sizes it does not improve
those projection optima. These are floating-point experiments, not universal
proofs. The analytic proof and integer family above establish (1) and its stated
projection sharpness without those computations.

The unresolved global issue remains a common payment of near-saturation errors
across genuine branches, or another global mechanism. Neither (1) nor projection
sharpness closes the arbitrary-m half-coverage question.
