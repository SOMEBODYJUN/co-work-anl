# Independent review: global mean cap gives weighted original IC credit

2026-10-25, credible12. Review of
`../tree/mean_cap_credible_shadow_working.md`, sections 1 and 3--5.
Original arbitrary-m finite common catalog, unit clients/providers, every
complete ordered-history pure SPE. **No fatal issue in its stated scope.**
Internal analytic review only; no external novelty or HALF claim.

This branch independently derived the mean-cap analytical enlargement and
its finite-LP cap dual before reading tree12's full note. It then
independently reconstructed root's cap-slack relation before comparison
with the note. Tree12 acknowledges the parallel mean-cap derivation.

## 1. Static mixtures versus pure threat completion

Fix original sigma, actual ordered leaf B, prefixes h_i and utilities u_i.
For forced A different from B_i, a raw record is a complete pure tail-SPE
endpoint after the exact history h_i A, with entering utility d and
deleted-entering-slot load ell. Keep the actual-action column fixed as in
tree12. Every ell is the load of m-1 legal catalog choices.

Pointwise selections with d<=u_i can be completed to a pure SPE because
different first-deviation children are disjoint ordered subtrees. This is
the old freedom in canonical `credible_continuations.md`, section 1,
capped menu (2), not new payment.

The global analytical row instead permits a lottery q over raw tagged
`(A,endpoint)` records with only E_q d<=u_i. Its mean load remains a
legal fractional catalog load of mass m-1, even if some individual record
has d>u_i. Such a lottery need not be any new pure or mixed SPE. Tree12
correctly claims only a larger static-background proof domain.

Global mean cap does not imply a conditional cap for each action A.
Therefore SOURCE query leaves must remain ORIGINAL sigma leaves in the
credit proof below. Their original whole IC supplies I_i>=0; it is not
inferred from the independent background lottery.

## 2. Exact finite dual and KKT sign

At a shared minimizer set t=(1+L*)^-1, rho_x=Pr_p[x in A], and
w_x=rho_x t_x^2. The role-i shadow maximization over its feasible mean-cap
row is a feasible bounded finite LP. Its dual has mu_i>=0 and unrestricted
eta_i, with

    H_i=eta_i+mu_i u_i,
    w dot ell_e <= eta_i+mu_i d_e      for every raw endpoint e.       (D)

The Lagrangian is `mu_i u_i+max_e(w dot ell_e-mu_i d_e)`, so the sign is
correct. No eta_i>=0, mu_i<=1, or separate funding of mu_i u_i is assumed.

Minimizing F_p over the independent Minkowski row domain has gradient
-w. Thus w dot(L-L*)<=0, every row in a realization of L* maximizes its
own shadow, and

    sum_i H_i=m w dot L*.

At a joint query/background saddle gamma=F_p(L*) is the maximum whole-theme
t-price, with equality on query support. Also

    w dot L*=gamma-sum_x rho_x t_x^2.

Zero rho coordinates and nonunique row decompositions cause no problem.

## 3. The actual nonnegative credit

For ORIGINAL source records `(ell_i^0(A),d_i^0(A))`, define

    r_i(A)=eta_i+mu_i d_i^0(A)-w dot ell_i^0(A)>=0,
    I_i=u_i-E_p d_i^0(A)>=0.

Membership in the raw domain gives reduced-cost nonnegativity; original
SPE IC gives I_i. Substitution in (D) yields the exact row relation

    H_i-E_p[w dot ell_i^0(A)]=mu_i I_i+E_p r_i(A).

Consequently

    G=m w dot L*-sum_i E_p[w dot ell_i^0(A)]
     =sum_i mu_i I_i+R >=sum_i mu_i I_i,
    R=sum_i E_p r_i(A)>=0.                                      (CREDIT)

The positive sign on mu I matters: large cap prices here multiply
original IC slack as additional nonnegative credit. This is a genuine
cap-frontier amount relation within the KKT gap, without a claim that its
banks already pay covariance.

## 4. Balance, static slack, and m=5 boundary

Use ORIGINAL source leaves for C,D, and define

    Cov=sum_(i,x)t_x^2 Cov_p(1_(x in A),ell_i^0(A)_x).

Algebra gives the GLOBAL identity C=Cov-G. A rowwise version with the
same common L* is not needed. The Bregman balance becomes

    W-m gamma=D-Cov+sum_i(1+mu_i)I_i+R.                         (BAL)

The source I,C,D records and the enlarged background witnesses are kept
separate throughout. At the joint saddle, fractional catalog legality
gives

    Qstat=(m-1)gamma-sum_xL*_xt_x>=0,
    OPT_m<=(2m-1)gamma-Qstat.

Hence the still unproved sufficient payment is

    Cov<=D+sum_i(1+mu_i)I_i+R+(gamma+Qstat)/2.                 (PAY?)

At m=5 the same CREDIT holds for every catalog and original complete SPE,
but the outstanding sufficient comparison is still `9gamma-Qstat<=2W`. No formula above
bounds Cov by PAY?'s right side, so no unconditional five-player or all-m
HALF follows.

For m=1 the deleted loads are zero and the identities reduce correctly.
Empty topics and zero clients produce zero sums; all reciprocal denominators
are at least one. No finite computation or special-size project was used.

## 5. Review conclusion

Domain legality, absence of a lottery-completion claim, finite duality,
KKT signs, reduced costs, CREDIT and BAL pass. In particular actual source
IC is not obtained from global background CAP. The remaining issue is a
genuine cross-history covariance payment, not another price identity.

## 6. Independent check of aggregate12's full-slot extension

Aggregate12 subsequently supplied the exact full-slot contract by message;
this subsection reconstructs that contract before reading a full source
note. For a tagged endpoint use full load `ell+1_A` in the BACKGROUND row,
while its cap remains the original entering payoff `d=F_A(ell)`. Keep
ORIGINAL deleted source ell in the reciprocal expansion at the selected
full-load point L*. The same global mean-cap LP dual gives

    Gplus=m w dot L*-sum_i E_p[w dot(ell_i^0(A)+1_A)]
         =sum_i mu_i I_i+R.

Put z_x=rho_x t_x. Since E_p[1_A]=rho,

    Gplus=m w dot L*-sum_i E_p[w dot ell_i^0(A)]-m sum_x z_x^2.

Thus the DELETED-source covariance expansion has

    C0=Cov0-Gplus-m sum_x z_x^2,
    W-m gamma_plus=sum_i(1+mu_i)I_i+R+D0-Cov0+m sum_x z_x^2.

The positive sign and factor m on the self-norm are correct. Source I
must still use `1+ell`, not `1+ell+1_A`; otherwise it is no longer the
original whole-query IC. A selected full background has provider mass m,
so Qplus=`m gamma_plus-sum L*t` is nonnegative and
`OPT_m<=2m gamma_plus-Qplus`. Its sufficient payment is therefore

    Cov0<=sum_i(1+mu_i)I_i+R+D0+m sum_x z_x^2+Qplus/2.

The scalar fact `m z_x^2>=z_x/2` when `z_x>=1/(2m)` correctly pays half of
that coordinate's gamma contribution; it is not by itself a welfare or
private-seat assertion. This check establishes the proposed extension's
algebraic scope, not its remaining covariance amount, including at m=5.
