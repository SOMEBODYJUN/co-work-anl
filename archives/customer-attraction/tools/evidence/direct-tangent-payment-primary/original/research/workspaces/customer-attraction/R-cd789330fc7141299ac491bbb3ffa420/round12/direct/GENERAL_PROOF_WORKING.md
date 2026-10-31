# Round12 direct: tangent passivity attempt and unpaid error transfer

2026-10-25. Same actor/clone, following root's round12 task. General target:
arbitrary finite unit clients, arbitrary finite nonempty common catalog,
arbitrary m, every complete ordered-history pure SPE, including empty themes,
duplicate coverage labels and arbitrary history-dependent ties.

**No new positive general amount inequality was proved. Q-CAG-HALF and its
general m=5 instance remain OPEN.** This is a resumable execution checkpoint,
not a statement that the target or these methods are impossible. No finite
probe or computation was run in round12. The branch is now stopped at root's
execution-window instruction; it must not be described as still running.

## 1. Restored boundaries and two immediately abandoned helpers

I read current AGENTS and /workspace/scratch/1ff1149f1493/round12_peer_read.json.
Peer review327 confirms the shared-load and Bregman algebra, but does not pay
the r_beta transfers or earlier resets. Zero-C, even after optimal saddle and
role transport, is already false; it was not reopened here.

Omission-only funding is FALSE, including favorable choice of optimum tuple.
I initially failed to restore its precise source; root supplied it before any
new test. The old71 unit-client, two-player complete SPE has W35, unique
OPT38, optimal omission R36 and actual-only E33. Thus R>W, while net R−E=3
and HALF both hold. Source: R-d22a706a03c5499d941a6a97f94128a8/exchange/
unique_optimum_omission_obstruction.md, independently reviewed at
R-171cd7d518434f36a48cd50df29c9303/coupling/
optimal_omission_independent_review.md. I read both and abandoned R<=W.

A dynamic root threshold cannot be spread over all roles either. Write
alpha_m=max_A min_(credible child) u_root(A,child). With m2 and disjoint
topics of sizes3 and2, after the size3 topic the last player strictly picks
size2 (2>3/2); after size2 it strictly picks size3 (3>1). Thus alpha_2=3,
the unique SPE has utilities(3,2), W5<2 alpha_2. Root and I independently
noticed this immediately; no tests or floor project followed. This does not
refute static aggregate safety or HALF.

## 2. Full static optimum remainder, retained only as algebra

Use the original round11 shared-menu convex body K and a genuine saddle
(p*,L*) of max_p min_(L in K) sum rho/(1+L), with value gamma. Put
t_x=1/(1+L*_x), rho=marginal(p*). Query-side optimality gives
g_t(A)=sum_(x in A)t_x<=gamma for every legal whole theme A, equality on
supp p*. The static background slack is

    Qstat=(m−1)gamma−sum_x L*_x t_x>=0.

Fix an optimal m-tuple T with union C and multiplicities a_x. Retain

    Popt=m gamma−sum_j g_t(T_j)>=0,
    Rep=sum_(x in C)(a_x−1)t_x>=0,
    Out=sum_(x notin C)L*_x t_x>=0.

Then the exact pointwise static identity is

    OPT=(2m−1)gamma−Qstat−Popt−Rep−Out.             (STATIC)

Indeed 1=t_x+L*_x t_x on C, and repeated comparison coverage contributes Rep.
Consequently the Bregman debt Ccorr in the parent's notation could be as large
as I+D+(gamma+Qstat+Popt+Rep+Out)/2 and still prove HALF. Root checked this
clientwise. Including every remainder makes that debt bound equivalent to
the original target; STATIC is not a new payment and was not promoted.

The hoped-for use was to map reply r_beta price gaps or outside-optimum resets
to PARTICULAR terms of STATIC. No such common mapping was constructed.

## 3. A specific actual-load amount which WOULD suffice if paid

For m>=2, actual columns L_i(S_i)=c−1_(S_i) belong to their menus, hence the
shared domain contains ((m−1)/m)c. KKT at L*, with w=rho t^2, gives the already
derived round11 valid constraint

    sum_x rho_x t_x^2 c_x
       <=m/(m−1)[gamma−sum_x rho_x t_x^2].          (ACTUAL-LOAD)

This suggests a definite stronger sufficient payment target, rather than
another covariance-zero assertion:

    Ccorr<=D+I+(m−1)/(2m)sum_x rho_x t_x^2 c_x.     (T-PAY?, unproved)

ACTUAL-LOAD would cap its added amount by gamma/2 and therefore prove the
weaker shared floor W>=(m−1/2)gamma, which is enough for HALF by the old
static bound. There is no proof of T-PAY here. No new actual money was
created by assigning it a name.

At m5 the proposed added actual-load amount is (2/5)sum rho t^2 c. The KKT
bound would make this <=(gamma−sum rho t^2)/2<=gamma/2. Thus if the SAME
general T-PAY argument were proved, it would yield OPT_5<=2W for every
catalog and complete SPE. The missing payment is still present, so there is
no unconditional m5 result.

## 4. What tangent passivity would need, and why it was not assumed

For fixed t, put v_A=t 1_A. The exact tangent utility at a terminal profile Z
is

    u_i^tan(Z)=2g_t(Z_i)−v_(Z_i) dot (t c(Z)),
    u_i(Z)=u_i^tan(Z)+E_i^t(Z),
    E_i^t(Z)=sum_(x in Z_i)(1−t_x c_x(Z))^2/c_x(Z)>=0.

Original whole IC at any ORIGINAL history h therefore implies only

    u_i^tan(dev)−u_i^tan(obey)
       <=E_i^t(obey)−E_i^t(dev).                  (T-IC)

In particular the maximum positive tangent regret at that node is at most its
own prescribed square error. Original sigma need not be an SPE of this
quadratic game. Summing the actual-node square errors does not pay errors at
different off-history prescriptions; the same old reset gap remains.

I considered whether a general symmetric PSD quadratic/congestion passivity
theorem could first control the tangent response, and then transfer its
errors using T-IC into the small actual-load amount in T-PAY. No such theorem
was proved or assumed. Tree11 confirmed it had no applicable SPE-to-PNE or
aggregate-demand theorem either.

There is one exact diagnostic about an existing instance, not a new game or
new finite probe. In the old36 catalog (global_security_budget_boundaries.md),
all six themes have size21. Distinct same-group themes overlap9 clients and
cross-group themes overlap13. At constant t_x=tau, tangent comparisons are
equivalent to minimizing total pair overlaps. The old reciprocal SPE chooses
after X0 the second theme Y0 and then Y1, giving the second role overlap cost
13+9=22. Its alternative X1 then prescribed X2 costs9+9=18. It therefore has
a positive tangent deviation gain4 tau^2, although its original reciprocal
IC is a tie. Thus that old reciprocal global-decorrelation counterpolicy is
not a tangent SPE. It cannot by itself refute a tangent-only passivity lemma;
conversely, a tangent lemma would still need T-IC's exact error transfer.

An external primary-literature check also warned against a generic dominance
shortcut: Correa, de Jong, de Keijzer and Uetz, *The Inefficiency of Nash and
Subgame Perfect Equilibria for Network Routing*, MOR44(4),2019, prove
unbounded sequential price of anarchy for symmetric routing with linear
latencies. Primary paper: https://www.dii.uchile.cl/~jcorrea/papers/Journals/CJKU2019.pdf
and publisher abstract: https://pubsonline.informs.org/doi/10.1287/moor.2018.0968 .
This does NOT refute the coherent saddle tangent setting here: its action
base2g, saddle prices and menu constraints are additional restrictions. It
does show that nonnegative PSD incidence interactions alone do not license
an SPE-to-static-welfare shortcut. No external theorem was imported as a
proof of either side of T-PAY.

The precise unfinished task is to map the standalone-error gaps
E[r_beta(B(A))−r_beta(A)] and all changed-prefix error resets into ONE
original actual-load bank (or into identified static optimum credits), while
retaining every original whole-theme IC. Tree11's round11 DEMAND/SWAP
identities remain valid, but no cross-role/cross-history cancellation with
the required amount was constructed here.

## 5. Capped-menu exact penalty observation, without a funding claim

For any finite child-endpoint set and capped shadow maximizer H_cap with
entrant payoff d<=u_i, one can choose a finite scalar mu such that

    H(Y)−mu(d(Y)−u_i)_+<=H_cap

for all credible endpoints Y: take mu at least the maximum positive ratio
(H(Y)−H_cap)_+/(d(Y)−u_i) over violating endpoints. This hinge penalty needs
no concave-frontier assumption, unlike linear pricing by mu d(Y).
Credible12 independently checked the observation and its limitation: every
original cap-feasible query has zero hinge penalty, so it supplies no mu I
bank; a cap-violating reset can have a huge penalty requiring actual payment.
This was not turned into a new route or a claimed amount.

An auxiliary thought about full-load clients and WEAK-Q was also discarded:
matching12 correctly restored the stronger old static comparison
OPT<=Q+(1−1/m)W, which already handles c=m through the actual-overlap bonus.
My proposed tiny full-load correction was an artifact of using a weaker
tax-based comparison; it was unnecessary and produced no claim.

## 6. Final branch status

Only the existing/general algebraic relations STATIC, ACTUAL-LOAD, T-IC and
the finite hinge observation were retained. T-PAY, netROW/SUMROW, the weak
shared-load floor and original HALF are all OPEN. No balanced source flow,
actual positive amount, new unconditional approximation or target
counterexample was obtained. The parent has been told explicitly; this
checkpoint closes the execution window and does not assert impossibility.
No scripts, finite probes, git/work.py actions or credential operations were
performed in round12. All changes are confined to this round12/direct folder.
