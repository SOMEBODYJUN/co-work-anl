# Weighted endpoint price family and the unresolved early-player transfer

Working note, 2026-10-21. Status: direct analytical derivation; no general
half-coverage proof, no independent review yet. The main target remains OPEN.
This note uses the exact common-catalogue, unit-customer CAG-MODEL, including
all ordered histories, arbitrary history-dependent ties, repeated themes and
empty themes. It is a parameterized refinement of the existing penultimate
price calculation, not a new global claim.

## 1. Price functional and the general missing statement

For nonnegative target customer weights q_x and a price v>=0, write

    B_q(v)=max_{z_T>=0} [sum_x q_x min(1,d_x)-v tau],
    d_x=sum_{T contains x}z_T,  tau=sum_T z_T.

The target weights q are coefficients in a comparison functional; they do not
change the original game or any player's utility. Finite LP duality gives

    B_q(v)=min sum_x y_x
    subject to 0<=y_x<=q_x,
               sum_{x in T}(q_x-y_x)<=v for every catalogue topic T.

For q=1, a general B_1(min_i u_i)<=W would imply half coverage: assign weight
one to each of an optimal m-topic tuple, obtaining
OPT_m<=B_1(min u)+m min u<=2W. This early-player statement remains unproved.
The dual interpretation is that removing at most W units of customer mass
would make every residual topic have mass at most the lowest actual payoff.
Using the actual covered set as the removed mass only certifies this for the
last player's payoff; transporting the price to an earlier player needs real
cross-branch inequalities.

## 2. Parameterized two-player endpoint lemma

Fix any legal ordered prefix, with customer load p_x>=0, and exactly two
players remaining in a given complete-history pure SPE. Let their actual
topics be A,B, and their actual original-game payoffs be v=u_A and w=u_B.
For every eta>=0 set

    theta_eta(p,a)=min{1/(p+1), 1/(p+2)+eta/(p+a+1)},
    a=1_A(x).

Then, for every q_x>=0,

    B_q(v) <= eta w + sum_x (q_x-theta_eta(p_x,1_A(x)))_+.       (T)

Equivalently, the single core inequality is

    B_theta_eta(v) <= eta w.                                   (C)

Indeed, (T) implies (C) by q=theta_eta. Conversely, for every f in [0,1],
q f<=theta f+(q-theta)_+, so (C) implies the whole family (T).

For eta=0, theta=1/(p+2), and (C) is just the robust pure deviation floor.
For eta=1/2,

    theta=1/(p+1)      when p>=1,
    theta=3/4          when p=0,a=1,
    theta=1            when p=0,a=0.

The core LP dual gives an existential price lift: one can delete at most
eta*w mass from these theta-weighted customers, leaving every residual topic
with mass at most the actual penultimate payoff v. This is an endpoint
statement with exactly two remaining players.

## 3. True branch rows and exact cancellation

For every comparison topic T, let R_T be the specified last player's true
reply after T at the fixed original prefix. Write

    U_p(X,Y)=sum_{x in X}1/(p_x+1+1_Y(x)).

For a nonnegative portfolio z of total weight tau>0, these are true
nonnegative SPE slacks:

    S=tau*v-sum_T z_T U_p(T,R_T),
    Z=tau*w-sum_T z_T U_p(R_T,A),
    V=sum_{T,Q}z_T z_Q[U_p(R_T,T)-U_p(R_Q,T)].

The last term compares two legal single topics at the last-player node after
T. It does not compare frozen future portfolios. Thus

    G_eta=S+(eta/tau)Z+V/tau >=0.

For one customer put a=1_A, b=1_B, d=sum_T z_T 1_T,
ell=sum_T z_T 1_(R_T), D=(p+1)(p+2), and
alpha=a/(p+a+b), beta=b/(p+a+b), with zero numerator shares taken as zero.
The joint-membership term sum_T z_T 1_T 1_(R_T) cancels exactly, leaving

    (G_eta)_x = tau*alpha+eta*beta-d/(p+1)
                 -eta*ell/[tau*(p+a+1)]+d*ell/(tau*D).          (1)

Therefore

    sum_x q_x min(1,d_x)-tau*v <= eta*w+sum_x r_x,

where

    r=q min(1,d)-d/(p+1)
        -eta*ell/[tau*(p+a+1)]+d*ell/(tau*D).                   (2)

## 4. Full-parameter corner proof

Assume tau>=1. The rectangle 0<=d,ell<=tau splits at d=1, and r is bilinear
on each piece. It suffices to consider d in {0,1,tau} and ell in {0,tau}.
The d=0 maximum is zero. The d=1 corners are

    q-1/(p+1),
    q-1/(p+2)-eta/(p+a+1).

The d=tau,ell=0 corner is dominated by d=1,ell=0. The d=tau,ell=tau corner
is q-tau/(p+2)-eta/(p+a+1), whose difference from its d=1 counterpart is
(1-tau)/(p+2)<=0. Thus the exact rectangle maximum is

    max{0,q-1/(p+1),q-1/(p+2)-eta/(p+a+1)}
      =(q-theta_eta(p,a))_+.

Substituting into (2) proves (T) for tau>=1. For 0<tau<1, normalize z by
tau. The normalized d values are at most one, so the objective scales
exactly by tau; the proposed right side is nonnegative, so the same bound
follows. tau=0 has objective zero. All parameters p>=0, a in {0,1}, eta>=0,
q>=0 have been retained analytically; no finite experiments prove this.

## 5. Clone slack and relation to the known unweighted endpoint bound

The actual last player can clone A, so

    L=w-H_A>=0,  H_A=sum_{x in A}1/(p_x+2).

Adding lambda*L to G_eta for lambda>=0 yields the valid bound

    B_q(v) <= (eta+lambda)w-lambda H_A
                +sum_x(q_x-theta_eta(p_x,1_A(x)))_+.

As a raw customer-sum estimate, this only adds the nonnegative quantity
lambda*(w-H_A). Its utility is that a choice such as eta=lambda=1/2 can
make a subsequent pointwise comparison with actual incumbent profits
particularly simple. The existing full endpoint result
B_1(v)<=W-v+E<=W-v/2 follows by that pointwise organization; this note does
not claim the clone row strengthens the exact raw sum bound.

eta<1/2 gives a smaller coefficient of w, but theta_eta(p=0,a=0)=1/2+eta<1.
Consequently q=1 then charges customers uncovered by the actual prefix and
A. This prevents dropping eta below 1/2 in an unweighted global budget
without a new way to pay those customers. For composed targets q<=1/2+eta
on those customers, the smaller-eta family may still be usable.

## 6. Precise general obstruction retained

The exact harmonic potential Phi(s)=sum_x H_(c_x(s)) satisfies, for a true
current-player comparison between terminal profiles z and z',

    u_current(z)-u_current(z')
      =Phi(z)-Phi(z')-[Phi(z minus current)-Phi(z' minus current)].

The two deleted-player potentials use their own branch-specific suffixes.
Replacing either with the actual suffix, or treating an off-branch follower
portfolio as a single legal action, is invalid. A general charging proof
must pay this branch variation or construct cancellation using complete-tree
rows. The endpoint proof above succeeds because its final follower chooses
one legal topic; no analogous general deletion of multi-follower variation
has been justified here.
