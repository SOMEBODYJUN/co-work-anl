# Independent review: parametric terminal price lift

2026-10-21. Reviewer: charging-duality branch of the current Boss4 team.
Status: direct independent reconstruction of the real SPE rows, the cancellation,
and the full-parameter optimization. No fatal objection found. No external
review or novelty claim. The unrestricted Q-CAG-HALF target remains OPEN.

## Reviewed statement

Fix any legal ordered prefix of the original unit-customer common-catalogue
game, and a given complete-history pure SPE with exactly two remaining players.
Write p_x for prefix load, A,B for actual final topics, and v=u_A,w=u_B for
their original-game terminal payoffs. The original utilities and policies are
not changed by the target weights q_x below. Define

    B_q(v)=max_{z_T>=0} [sum_x q_x min(1,d_x)-v tau],
    d_x=sum_{T contains x}z_T, tau=sum_T z_T,
    theta_eta(p,a)=min{1/(p+1),1/(p+2)+eta/(p+a+1)}.

For every eta>=0 and q_x>=0, the statement is

    B_q(v) <= eta*w + sum_x(q_x-theta_eta(p_x,1_A(x)))_+.       (T)

In particular,

    B_theta_eta(v) <= eta*w.                                  (C)

The q-family and the core bound are equivalent: (T) implies (C) by setting
q=theta_eta; (C) implies (T) using q f<=theta f+(q-theta)_+ for f in [0,1].
There is no restriction on total provider count, catalogue size, arbitrary
history-dependent ties, internal topics, empty topics, or repeated topics.
Only the number of *remaining* players is two.

## Independent reconstruction of the three real row families

Let R_T be the given strategy's actual last reply following the legal
penultimate choice T at the fixed original prefix. Put

    U_p(X,Y)=sum_{x in X}1/(p_x+1+1_Y(x)).

For any z>=0 of positive total tau, the following quantities are nonnegative:

    S=tau*v-sum_T z_T U_p(T,R_T),
    Z=tau*w-sum_T z_T U_p(R_T,A),
    V=sum_{T,Q}z_T z_Q[U_p(R_T,T)-U_p(R_Q,T)].

S uses penultimate optimality at the actual fixed prefix. Z uses last-player
optimality at the actual last node following A; R_T is a legal topic there.
V uses last-player optimality at each real last node following T, comparing
its designated topic R_T against the legal topic R_Q. In particular, no
off-branch portfolio has been frozen and no multi-player continuation has
been treated as one legal move. Nonnegative real weights preserve all signs.

Thus G_eta=S+(eta/tau)Z+V/tau>=0 for every eta>=0.

For one customer independently put

    a=1_A, b=1_B, d=sum_T z_T 1_T, ell=sum_T z_T 1_(R_T),
    h=sum_T z_T 1_T 1_(R_T), D=(p+1)(p+2),
    alpha=a/(p+a+b), beta=b/(p+a+b).

Zero numerator shares are zero, including p=a=b=0. The separate customer
contributions are

    S_x=tau*alpha-d/(p+1)+h/D,
    (eta/tau)Z_x=eta*beta-eta*ell/[tau*(p+a+1)],
    V_x/tau=-h/D+d*ell/(tau*D).

The h terms cancel exactly. Hence

    (G_eta)_x=tau*alpha+eta*beta-d/(p+1)
                  -eta*ell/[tau*(p+a+1)]+d*ell/(tau*D).        (1)

Summing (1), and using G_eta>=0, reduces (T) to the pointwise bound for

    r=q min(1,d)-d/(p+1)-eta*ell/[tau*(p+a+1)]
                       +d*ell/[tau*(p+1)(p+2)].             (2)

This reconstruction checks the sign of V and the factor 1/tau explicitly;
reversing either would invalidate the cancellation.

## Full-parameter optimization, rather than finite extrapolation

For tau>=1, the permissible region lies in 0<=d,ell<=tau. On each of the two
rectangles cut by d=1, r is bilinear. Its rectangle maximum occurs at the six
corners d in {0,1,tau}, ell in {0,tau}. This enlarges the actual attainable
(d,ell) region, which is safe for an upper bound.

At d=0 the maximum is zero. At d=1 the two values are

    q-1/(p+1),
    q-1/(p+2)-eta/(p+a+1).

The d=tau,ell=0 value is q-tau/(p+1), no larger than the first d=1 value.
The d=tau,ell=tau value is q-tau/(p+2)-eta/(p+a+1); its difference from
the second d=1 value is (1-tau)/(p+2)<=0. Therefore the exact enlarged-region
maximum is

    max{0,q-1/(p+1),q-1/(p+2)-eta/(p+a+1)}
      =(q-theta_eta(p,a))_+.

This proves the pointwise bound for every p>=0, a in {0,1}, eta>=0 and q>=0.
The argument needs no bound on eta and no finite-grid verification.

For 0<tau<1 normalize z'=z/tau. Then every normalized d'_x<=1, so

    sum_x q_x min(1,d_x)-v tau
       =tau[sum_x q_x min(1,d'_x)-v].

The tau'=1 bound applies to the bracket. The proposed uniform RHS
C=eta*w+sum(q-theta_eta)_+ is nonnegative, hence tau*C<=C. For tau=0 the
objective is zero. This closes the small-total-weight case without assuming
the maximizing portfolio has tau>=1.

## Endpoints, dual meaning, and clone comparison

eta=0 gives theta_0=1/(p+2) and B_theta_0(v)=0: penultimate deviation to T
always guarantees at least sum_(x in T)1/(p_x+2), so every such weighted topic
mass is at most v. This agrees exactly with the robust pure deviation floor.

eta=1/2 gives the explicit thresholds

    p>=1:        theta=1/(p+1),
    p=0,a=1:     theta=3/4,
    p=0,a=0:     theta=1.

For the first line, the difference between the second and first candidate
thresholds is eta/(p+a+1)-1/[(p+1)(p+2)], which is nonnegative at eta=1/2
for p>=1. The two p=0 cases give 3/4 and 1 directly.

Finite LP duality gives

    B_q(v)=min{sum_x y_x: 0<=y_x<=q_x,
                         sum_(x in T)(q_x-y_x)<=v for all T}.

Thus (C) means that deleting at most eta*w mass from the theta_eta-weighted
customers can leave every residual topic with mass at most v. The LP has a
finite compact representation: in the primal, each z_T can be clipped to
one without reducing truncated coverage or increasing nonnegative cost.

The additional actual-last clone row is

    L=w-C_A>=0, C_A=sum_(x in A)1/(p_x+2).

Adding lambda*L to G_eta yields RHS

    eta*w+sum(q-theta_eta)_+ + lambda*(w-C_A), lambda>=0.

Consequently the clone addition weakens the exact raw customer-sum bound by
a nonnegative quantity. It may simplify a later pointwise comparison with
actual old-player profits, but must not be advertised as a strengthening of
(T). The no-clone parameter theorem is the primary result. Previously known
unweighted tax-type corollaries can be retained as weaker organized forms.

## Scope and remaining obstruction

Every incentive row used above belongs to the given complete original SPE.
The proof does not identify equal-load histories, assume anonymous ties, or
replace the actual ordered policy by a count-dependent one. It also handles
zero payoffs and the zero-customer instance without dividing by v or w.

The parameter family alone does not control earlier players. When eta<1/2,
theta_eta(0,0)=1/2+eta<1; q=1 then charges customers absent from both the
fixed prefix and A. Paying those charges through real multi-follower
continuations is still missing. The statement B_1(u_i)<=W for arbitrary
early i, and hence the unrestricted half-coverage target, remains open.
