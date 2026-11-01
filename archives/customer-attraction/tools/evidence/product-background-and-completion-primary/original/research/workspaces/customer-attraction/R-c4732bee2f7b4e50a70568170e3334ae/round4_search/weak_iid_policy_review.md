# Independent blind review: core, B, and petal full-history policy

Status: the policy is a genuine pure SPE for every integer **m>=2, K>=2**.
This was reconstructed before reading the author's proof. The result concerns
an auxiliary iid benchmark; it is not a counterexample to Q-CAG-HALF.

## Instance and complete policy

There are two core clients A, a disjoint B block with 2(m-1) unit clients,
and K distinct private petal clients. The common catalog consists of C=A,
B, and P_j=A union {private j}, j=1,...,K. All clients and providers have
unit weight. In particular, multiplicities encode distinct unit clients.

Player 1 chooses C. At every ordered history, every player i with 2<=i<m
chooses B. At every final history h, put t=number of non-B actions in h.
The last player chooses P_1 if t=0; B if t=1 and the unique non-B action is
C; another P_k, k!=j, if the unique non-B action is P_j; and B if t>=2.
For definiteness choose P_1 when j!=1 and P_2 when j=1. This defines one action
at every ordered history, including histories never reached by earlier policy.
The proof evaluates every such history directly. Choosing a policy that happens
to depend only on these statistics does not restrict the underlying SPE model.

## Last-player optimality at every ordered history

Let r_j be the number of copies of P_j in a final prefix, let t be its number
of non-B actions, and b=m-1-t its B count. Because every non-B topic contains
both core clients, the final player's payoffs are exactly

- B: 2(m-1)/(m-t);
- C: 2/(t+1);
- P_j: 2/(t+1)+1/(r_j+1).

If t=0, every petal pays 3, C pays 2, and B pays 2(m-1)/m<2. If t=1 with
unique C, B and every petal pay 2 while C pays 1. If t=1 with unique P_j,
B and every other petal pay 2, P_j pays 3/2, and C pays 1. Thus the specified
choices are optimal in all three cases. If t>=2, necessarily m>=3; B pays
strictly more than 2 while any petal pays at most 1+2/3. Hence B is uniquely
optimal. This argument includes arbitrary repeated petals and arbitrary order.

## All earlier nonroot players, including every off-path history

Fix any i with 2<=i<m and any ordered history of length i-1. Let t count
its non-B actions. All later nonfinal players choose B under the given full
policy, whatever i does.

If t=0 and i chooses B, the last player selects a petal. There are m-1 total
B players and i earns 2. If i chooses C, the final player selects B and i
earns 2 from the core. If i chooses P_j, the final player selects another
petal and i earns 1 from the core plus 1 from its private client. Thus all
alternatives pay exactly 2.

If t>=1 and i chooses B, its payoff is at least 2. More explicitly it is 2
when t=1 with sole C, 2(m-1)/(m-2)>2 when t=1 with sole petal, and
2(m-1)/(m-t)>2 when t>=2. These denominators are positive because i<m and
therefore t<=m-2. If i chooses any non-B topic, the final prefix has t+1>=2
non-B actions, so the last player chooses B. A C deviation earns 2/(t+1).
A petal deviation earns at most 2/(t+1)+1<=2, including the possible repeated
private-client overlap. No deviation is profitable.

For m=2 there are no such intermediate players; nothing in this step is used.

## Root and actual welfare

Root C gives the path C B^(m-1) and payoff 2. Root B leads to B^(m-1) P_1 and
also payoff 2. Root P_j leads to P_j B^(m-2) P_k with k!=j and gives payoff
2. Therefore C is optimal, and all ordered-history optimality requirements
are met. Root indifference is allowed by the model.

The actual welfare is W=2m. Exact optimal welfare is
OPT_m=2m+min(K,m-1), achieved by B and as many distinct petals as the
remaining m-1 slots permit. An all-petal profile covers at most 2+min(K,m),
which is no larger. Consequently this family's inefficiency is below 3/2.

The stated parameter range matters. At m=1, choosing C is not optimal because
a petal pays 3 rather than 2, and B's block is empty. K>=2 supplies the required
other petal after a lone P_j. No assertion is made for K=1 or a zero-client
instance. For the valid range all terminal payoffs above have positive actual
denominators, and W>0.

## Iid benchmark crossing, with its precise separate role

For m>=2 write

g_m(z)=E[1/(1+Bin(m-1,z))]=(1-(1-z)^m)/(m z),

with g_m(0)=1. It is strictly decreasing in z. For the static iid adversarial
benchmark min_q max_T E[u_T(T,a_-i)], mass on C can be shifted to petals without
changing the core coverage probability and while weakly decreasing the maximum
petal payoff. At fixed B mass t, a uniform distribution among petals maximizes
the minimum petal mass and hence minimizes the maximum petal payoff. The C
payoff is below every petal payoff. Thus the minimax value is exactly

rho=min_(0<=t<=1) max{2(m-1)g_m(t), 2g_m(1-t)+g_m((1-t)/K)}.

The first function decreases strictly, the second increases strictly. At t=0
the first is strictly larger, and at t=1 it is strictly smaller, so rho is their
unique crossing value. This is a static iid quantity, not the aggregate of true
subgame security values.

For m=K=100, exact rational evaluation at t=1969/2000 gives both functions
strictly above 2011/1000, which is strictly above 400/199. Monotonicity implies
the crossing value rho>2011/1000, whether the crossing lies to the left or right
of this test point. Hence, with Z_100=100 rho,

(1-1/(2*100)) Z_100=(199/2)rho > 200+189/2000 > W.

This refutes precisely the weak iid bridge W>=(1-1/(2m))Z_m. A prefix containing
98 copies of B and one P_1 has one player left and best obtainable payoff exactly
2: B and P_2 pay 2, C pays 1, and P_1 pays 3/2. Thus a global cap defined by the
minimum true next-player security across all histories is <=2; replacing it by
rho>2 would change the benchmark.

## Explicit infinite family: m=K>=53

The isolated m=100 computation can be replaced by an all-parameter rational
certificate. Put K=m, x=3/(2m), and choose the crossing test point t=1-x.
The threshold needed to refute the weak bridge is c_m=4m/(2m-1), because
(m-1/2)c_m=2m=W.

The B payoff at this cut satisfies, for m>=3,

alpha_B = [2(m-1)/m] (1-x^m)/(1-x)
        >= [2(m-1)/m](1+x+x^2)
        = 2(m-1)(m^2+3m/2+9/4)/m^3.

This is just truncation of a positive geometric sum. Subtracting c_m from
the last expression gives exactly

(4m^2-21m+9)/(2m^3(2m-1)) > 0 for m>=5.

Indeed its numerator equals 4 at m=5 and has forward difference 8m-17>0
thereafter. No approximation of x^m is needed.

For the core part of the petal payoff, (1-x)^m<exp(-3/2). The strict rational
estimate exp(3/2)>sum_(j=0)^5 (3/2)^j/j!=5711/1280>40/9 gives

2g_m(x)=(4/3)[1-(1-x)^m] > (4/3)(1-9/40)=31/30.

For the private part put y=x/m=3/(2m^2). Bernoulli's inequality in the
geometric representation g_m(y)=(1/m)sum_(j=0)^(m-1)(1-y)^j yields

g_m(y)>=1-(m-1)y/2
       =1-3(m-1)/(4m^2)>1-3/(4m).

Consequently alpha_P>61/30-3/(4m). Its lower bound minus c_m equals

(4m^2-212m+45)/(60m(2m-1)) > 0 for m>=53.

The numerator is 45 at m=53 and has forward difference 8m-208>0 thereafter.
Both cut payoffs therefore exceed c_m for every integer m>=53. Since the B
function decreases and the petal function increases, their crossing value
rho is at least the smaller cut payoff and hence strictly above c_m. Thus
for every m=K>=53 the same genuine full-history SPE satisfies

W=2m < (m-1/2)rho = (1-1/(2m)) Z_m.

All strict inequalities are justified above; the iid bridge failure is an
infinite family, with no claim that 53 is the smallest possible parameter.

## Independent finite exact checks

`weak_iid_policy_review.py` builds the actual common catalog, expands every
ordered history, invokes the canonical complete-certificate verifier, and also
checks every ordered-history one-step deviation independently by following the
supplied policy to its actual terminal. It checks (m,K)=(2,2),(3,2),(3,3),
(4,4),(5,5),(6,4). These finite checks supplement, rather than replace, the
all-parameter proof above. It also checks the two rational iid test-point
inequalities exactly and the rational constants and algebraic gap identities
in the infinite-family certificate. Results are frozen in `weak_iid_policy_review.json`.
