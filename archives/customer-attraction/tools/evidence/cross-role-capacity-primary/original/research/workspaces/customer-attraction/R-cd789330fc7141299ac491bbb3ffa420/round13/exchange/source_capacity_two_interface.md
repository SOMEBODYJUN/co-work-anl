# Five-player exchange: signed capacity-two interface

2026-10-25. Original finite common-catalog unit-customer game, five ordered
providers, every complete-history pure SPE; empty/repeated themes and all
off-path ties retained. **HALF(5), WEAK-Q(5), and covariance payment remain
OPEN.** Conditional interface only; no unconditional welfare improvement,
SPE counterexample, external review, or novelty claim.

## Raw swap with its boundary retained

In one actual-prefix row h_i use the uniform raw-tail domain

    C_i(z)=d_i(z)+sum_(k>i)[M(z_<k)-u_k(z)],
    r_i(z)=eta_i+mu C_i(z)-a dot ell_i(z)>=0,
    K_i(A)=M(h_i,A), P_i(A)=a dot 1_A+mu K_i(A).

Here mu>=0 is the common cap price, a>=0 the fixed shadow, ell deletes the
entering role, and r is nonnegative on EVERY raw terminal order. For
z=(h_i,A,B,Y) and z^s=(h_i,B,A,Y), final counts and all deeper prefix counts
coincide. Round12 SWAP, directly expanded, is

    r_i(z^s)-r_i(z)=2mu[v_i(z)-d_i(z)]+P_i(B)-P_i(A).

For arbitrary source weights theta>=0, r_i(z^s)>=0 gives

    mu sum theta(d-v)
      <= sum theta r/2
         +sum theta a dot(1_B-1_A)/2
         +mu sum theta[K_i(B)-K_i(A)]/2.           (U)

No action balance is assumed. The price and canonical-threshold boundaries
remain signed. This is not a bound on positive parts of d-v.

## Atomwise capacity two pays one reduced-cost bank

Let p_(i,z) be a specified original source inventory, each row of mass one,
and set R=sum p r. If

    0<=theta_(i,z)<=kappa p_(i,z)                 (CAP)

ATOMWISE, then sum theta r/2<=kappa R/2. Thus kappa=2 suffices to spend at
most one complete R bank. One interlayer move per individual packet does
not imply CAP: several origins may merge at the same original source.

Put gamma_a=max_T a dot 1_T and assume each row's entering marginal is q.
Since a dot(B-A)<=gamma_a-a dot A>=0, CAP also gives

    sum theta a dot(B-A)
      <=5kappa[gamma_a-E_q a dot A].              (PRICE)

It is valid to use the five-row upper bound when a flow uses fewer rows.
Writing Delta_K=sum theta[K_i(B)-K_i(A)], obtain

    mu sum theta(d-v)<=kappa R/2
      +(5kappa/2)[gamma_a-E_q a dot A]+mu Delta_K/2.

For q uniform on an optimal five-tuple, define
Popt_a=5gamma_a-sum_j a dot T_j>=0; the price term is kappa Popt_a/2.
Usually a=rho t^2, whereas existing static portfolio slack uses t-prices.
Popt_a is NOT Popt_t. Replacing the saddle query by the optimal tuple also
changes its source/KKT gap; the new R is not automatically the funded R.

For the FULL-slot raw domain, a dot(B-A) vanishes because both full loads
coincide. Its bound is kappa R_plus/2+mu Delta_K/2, with that full domain's
OWN dual/inventory. Deleted and full banks cannot both be spent.

## A concrete row-wise teleport construction (tree13)

Fix a finite first-follower Markov kernel T(A,B) in this SAME row. Pick a
distribution r supported on argmax P_i. There is a unique distribution

    p=(r+pT)/2=sum_(k>=0) 2^(-k-1) r T^k.

Then pT<=2p coordinatewise and

    E_p[P_i(B)-P_i(A)]=E_p P_i-E_r P_i<=0.

Taking the source edge flow to be p(A)T(A,B) gives the original balanced
HALF-R payment without requiring stationarity: its total boundary has a
good sign and its source capacity is one. The arrival domination pT<=2p is
an additional exact property. This finite geometric-series argument does
not assert that the different rows have a common p, or that these p's are
the welfare saddle's original source queries. Tree13 supplied this lemma;
exchange13 checked its signs and records it here to avoid duplicate files.

## Exact cost of changing the query rows

Suppose row queries p_i are selected JOINTLY with a new reference domain,
rho_i(x)=Pr_(p_i)[x in A], rho=mean_i rho_i, t=(1+L)^(-1), a=rho t^2.
Set gamma=max_T sum_(x in T)t_x and

    Qinput=5gamma-sum_i E_(p_i) sum_(x in A)t_x>=0,
    Cov=sum_(i,x) E_(p_i)[(1_(x in A)-rho_x)t_x^2 ell_i(A)_x].

Direct reciprocal expansion and the SAME new KKT gap give

    W-5gamma=I+G+D-Cov-Qinput.

In the full-slot version add 5||rho t||^2 on the right, using its own G.
Hence changing queries has a full Qinput cost before any further static
slack is split. If Qplus=5gamma-Hbg is used in the full static comparison,
the sufficient payment is Cov<=B-Qinput+Qplus/2. Writing
Qplus=Qinput+(sum_i E_(p_i)g_t-Hbg) rewrites this as
B-Qinput/2+(sum_i E_(p_i)g_t-Hbg)/2; the latter residual is not freely
nonnegative. A genuine extra static comparison can reduce that debt, but
does not follow merely from teleportation.

If an OLD reference shadow rho0 t^2 is held fixed while p_i change, the new
mean rho cannot be substituted into its G. Relative to that old shadow an
extra term sum_i (rho_i-rho0)t^2 E_(p_i)ell_i remains. This is why the
row-wise construction cannot retain the old covariance bank for free.

## Remaining target obligations

The shared covariance must be represented by the SAME signed d-v sources;
CAP must be proved on original atoms despite mergers/witness changes; and
the canonical-threshold boundary plus query-price debt must be paid from
the same bank. No such combined map/payment was found here. In particular
the prior min-Q positive-loss gate has not gained an amount bound: the old
1953-customer complete SPE already has excess165 and net loss2. No finite
scan or nonseparation is used as evidence for the formulas above.
