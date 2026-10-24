# Independent review of occupation reserve and current-gap payment

2026-10-24. **Passed, within the exact algebraic scope below.** I first reconstructed the two identities and the strengthening from the statement, then read `relay/working.md` §§8–9. The proofs agree. The new inequality is valid for arbitrary complete plans; it does not itself use successor SPE optimality and does not settle a menu cap, derivative implication, or Q-CAG-HALF. All those general targets remain OPEN.

## 1. Exact objects and quantifiers

Fix any finite unit-customer common catalog, any legal integer prefix load b_x>=0, and n>=1 remaining future unit providers after the current provider. A complete plan specifies, after each forced current action A, a true future profile of n legal topics. It need not be SPE. For each customer x put

    a_A(x)=1_(x in A),   k_A(x)=number of future providers covering x,
    d_A(x)=1+b_x+a_A(x)+k_A(x).

Thus a_A is binary, k_A is an integer in [0,n], and d_A>=1. Define the full-terminal extra-query matrix

    K(T,A)=sum_(x in T) 1/d_A(x).

Let p be an arbitrary distribution on current root actions/independent query topics. Let q be the average empirical future-topic distribution when A is sampled from p. Precisely, n q_x=E_A k_A(x), where q_x is the probability that a q-topic covers x. In column-stochastic notation q=Pp. No stationarity q=p is assumed.

The three scalar quantities are

    G=p^T Kp,
    D=E_A sum_(x in A) 1/[b_x+1+k_A(x)],
    V_tail^+=E_A sum_x k_A(x)/d_A(x).

D is the current provider's mean genuine final utility under forced roots. V_tail^+ is the future providers' utility after adding one independent ghost load in every queried denominator; it is not their actual total profit and not total coverage. Its precise definition must be retained when using the inequalities.

## 2. Occupation identity and nonnegative reserve

For one fixed customer suppress x, write f_A=1/d_A, and let A,T be iid p. Direct expansion of q gives the customer's contribution to the left-hand side:

    n q_x E_A f_A = (E k_A)(E f_A).

Consequently

    n q^T Kp - V_tail^+
      = sum_x [(E k_A)(E f_A)-E(k_A f_A)]
      = (1/2) sum_x E[(k_A-k_T)(f_T-f_A)].

Since

    f_T-f_A = [(k_A-k_T)+(a_A-a_T)]/(d_A d_T),

we obtain exactly

    n q^T Kp = V_tail^+ + I,

    I=(1/2) sum_x E[Delta k(Delta k+Delta a)/(d_A d_T)].

This verifies the factor 1/2, both denominators, and the signs. Delta k is an integer and Delta a belongs to {-1,0,1}. Therefore Delta k(Delta k+Delta a)>=0 for every ordered pair, including Delta k=0 and the adjacent-load zero cases. Thus I>=0. No incentive condition has been used.

## 3. Stronger reserve bound I>=G-D

Again work with one customer. Define the safe self-tax expression

    Q_self=E[1_(a_A=1)/((b+1+k_A)(b+2+k_A))].

This expression avoids an undefined zero-load ratio when a_A=0. Because a_A=1 gives the genuine current denominator d_A-1=b+1+k_A,

    G_x-D_x = (E a_A)(E f_A)-E(a_A f_A)-Q_self.

The covariance identity gives

    (E a_A)(E f_A)-E(a_A f_A)
      =(1/2)E[Delta a(Delta a+Delta k)/(d_A d_T)].

Subtracting this equation from the reserve equation yields

    I_x-(G_x-D_x)
      =Q_self+(1/2)E[(Delta k^2-Delta a^2)/(d_A d_T)].

For k=0,...,n let p_(0,k)=Pr(a_A=0,k_A=k). The only possibly negative terms in the last expectation have Delta k=0 and Delta a=+/-1. For a given covered state A with k_A=k, its two ordered pairings with the uncovered same-k class have total probability 2 p_A p_(0,k). The outside factor 1/2 cancels that factor two. Both denominators multiply to (b+1+k)(b+2+k). Hence the exact positive decomposition is

    I_x-(G_x-D_x)
      =sum_(A:a_A=1) p_A[1-p_(0,k_A)]
                         /[(b+1+k_A)(b+2+k_A)]
       +(1/2)E[1_(Delta k!=0)
                  (Delta k^2-Delta a^2)/(d_A d_T)].

The first line is nonnegative because 0<=p_(0,k)<=1. In the second line, nonzero integer Delta k has Delta k^2>=1>=Delta a^2. Every term is nonnegative. This proves, after summing customers,

    I>=G-D.

The cancellation uses one self-tax budget once; there is no missing or duplicated factor of two.

## 4. Valid consequence and exact stopping point

Combining the two proved statements gives

    G+V_tail^+ <= D+n q^T Kp.

This is valid for every complete plan. If the current node is optimal against its true prescribed continuations, each forced-root payoff is at most its actual payoff u, and averaging gives D<=u. Only at that point do we obtain

    G+V_tail^+ <= u+n q^T Kp.

This last step uses current IC, not future-player IC. The preceding reserve theorem remains valid for nonoptimal arbitrary plans, so it cannot be described as a theorem extracted from genuine successor rationality.

For the proposed derivative direction q-p,

    (q-p)^T(K+K^T)p
      =(V_tail^+ + I)/n + p^T Kq - 2G.

The identities supply a positive occupation-side reserve, and if G>u then I>=G-D>=G-u>0. They do not control p^T Kq, the term obtained by resetting a future topic at the current root and taking a new true continuation. Its unpaid sign/size is exactly what prevents this component from establishing the derivative implication or a freely mixed root cap. Replacing V_tail^+ by actual tail welfare, treating q=p, or importing off-branch payoffs into the actual branch would change the statement.

## 5. Independent finite checks and integrality boundary

`check_occupation_reserve.py` imports only standard-library Fraction and reads no model solver or previous audit output. It checks both exact identities, the grouped positive decomposition and both signs on 4,095 deterministic scalar distributions, with b=0,...,4, n=1,...,6, all one-state and rational two-state distributions in those domains, plus two full-support distributions per domain. Minimum observed I and strengthened reserve are both zero. These are implementation regressions; the general proof is the displayed algebra.

The same code checks two enlarged-model fractional-load boundaries, which are not legal original unit-player profiles:

1. b=0, equally likely states (a,k)=(0,1/2),(1,0) give I=-1/48. Thus the reserve's pairwise sign proof cannot be transferred to arbitrary fractional future masses.
2. b=0, states (a,k)=(0,0) with probability 9/10 and (1,1/4) with probability 1/10 give I=1/80, G=17/180, D=2/25 and I-(G-D)=-7/3600. Thus the strengthening also depends on the integer-load contract; nonnegative I alone would not rescue it for arbitrary fractional masses.

These boundaries only delimit the stated unit-player algebra. They make no claim about impossibility of another weighted or fractional method.

## 6. Audit disposition

- OCC identity and I>=0: passed by independent reconstruction.
- Strengthening I>=G-D and the grouped decomposition: passed.
- Current-IC corollary G+V_tail^+<=u+nq^TKp: passed with its explicit extra assumption.
- Successor-IC derivative payment, free Mfull, and general half: not proved by this component.

Artifacts are `check_occupation_reserve.py` and `occupation_reserve_checks.json`. No git operations or shared claim promotion were performed.
