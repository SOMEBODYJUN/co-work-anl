# Target attack after heterogeneous repair: shared omissions and PB transplantation

2026-10-24. Q-CAG-HALF remains OPEN. No path with O-2W>2R+D has been found. This note records two precise attempted economic mechanisms and why the direct versions do not supply a target counterexample. These are not impossibility theorems about general SPE, arbitrary threat trees, or the original target. No broad fixed-cone sweep was run.

## 1. A last-player outside option blocks the direct repeated-punisher family

Consider a proposed arbitrary-size family with a low-welfare collision-free target

    C_1,...,C_k,D,

where the C_i are disjoint blocks of size p, D is disjoint of size t, and all omitted customer blocks Q_i are disjoint from that actual union. An alternative A_i=C_i union Q_i has |Q_i|=q. The last target action D can only be a BR if every legal topic has actual-last marginal value at most t. In particular A_i has value p/2+q, so q<=t-p/2.

If one last punishment action covers only C_i (plus some other reservoir block), the deviator's omitted Q_i is unshared. Sharing C_i once gives deviator payoff at least p/2+q. To cap that deviation by its target p requires q<=p/2. This is the known Q/B collision-free construction's economic ceiling; increasing q directly cannot raise its asymptotic OPT/W beyond 3/2.

The next attempt makes an actual punishment topic H_i contain *all* of A_i plus a reservoir subset E_i subset D of size b, intending several later players to repeat H_i and dilute Q_i too. Actual-last BR then imposes

    p/2+q+b <= t.                                  (L)

Suppose a deviation to A_i is followed by r>=1 copies of H_i, with the final player making the last copy, and all other branch actions avoid D minus E_i as well as A_i. The final prescribed H_i payoff is

    (p+q)/(r+1)+b/r.

Its legal deviation to D instead gives

    (t-b)+b/r.

By (L), t-b>=p/2+q. For q>0 and r>=1,

    (p+q)/(r+1) <= (p+q)/2 < p/2+q <= t-b.

Thus that final punishment action is strictly suboptimal. This failure holds for every number of early groups and every number of repeated punishers; it is not a finite computational observation. If several H_i copies are to be credible, **some other real branch action must first cover D minus E_i**, or the final punishment must use a substantially different topic. Such coverage has a real actual-last outside-option price and cannot be supplied by declaring an arbitrary continuation.

This leaves a concrete new-construction obligation: design a nonstationary sequence of distinct punishment topics whose coverage removes each other's residual reservoir options, while the actual-last BR and the entire off-path tree remain valid. The sharper repair would then test the actual credible floors, not the assumed punishments. There is presently no such sequence yielding a positive repaired half gap.

## 2. Literal no-background PB transplant has incompatible IC scales

The existing arbitrary-background PB-extra counterexample uses regular actions selecting at most k real blocks per segment and k-ell dummy blocks, with k>=2. Its scalar sufficient incentive conditions include

    Greedy:     g(r)>2f(1)-f(2),
    Fill/Copy:  k f(k)>f(t)+(k-1)g(1).

The original real and dummy background loads flatten both reward curves. If background is simply removed and real blocks have size a, dummy blocks size b, then

    f(c)=a/c,  g(c)=b/c.

Greedy forces b>(3/2)ar, whereas Fill/Copy forces

    a>a/t+(k-1)b,
    b<a/(k-1).

These are incompatible for r>=1,k>=2,t>=1 (and t=1 already makes Fill/Copy impossible). The direct no-background mechanism therefore has no legal parameters. This is only an obstruction to those exact sufficient ICs; a different construction or different proof can avoid them.

Beta clones can flatten fresh-label rewards without sunk background, but create a separate credibility issue. For a single original customer at background M>=1, fresh related clone labels have exact per-provider expected mass 1/(M+k) at a k-fresh-label terminal. If all k providers instead use one exact clone label, its inclusion mass is 1/(M+1), and each repeated-label player receives only

    1/[k(M+1)].

For large M this is approximately a factor k below the fresh-label payoff. Hence one cannot preserve the old Copy prescription by literally repeating a clone. Using distinct fresh labels avoids that loss on the intended path, but then all repeated-label histories need genuine new SPE continuations; the old background strategy does not automatically provide them. The repository's fixed-strategy Beta-lift failure already demonstrates that this latter completion is a real obligation.

Moreover, the existing PB parameters are in a very large-background regime: f(c)=q/M+O(M^-2) and g(c)=q/M+O(M^-2). All r providers' actual total remaining profit and the maximal r-action fresh-clone coverage have the same leading mass r d k q/M. Thus its first-two-player safety separation, by itself, does not supply any positive old half gap O-2W, let alone one exceeding 2R+D. A successful no-background target attack needs a macroscopic coverage loss in addition to the local PB menu effect.

## 3. Exact stopping point

The completed general tool is `heterogeneous_prefix_repair.md`: any target path with a credible tail and O-2W>2 sum(delta_i)+max(delta_i) compiles to a genuine full-history target counterexample. The two concrete threat ideas above do not meet that strict condition. No unconditional m=5 half bound follows: the same repair at m=5 still requires a proof of the robust inequality or an actual violating path. Continuing only to tune these two scalar families or repeat fixed-cone negative scans would not add a general payment mechanism.

Sources: the audited prefix compiler at `R-65d0f88edf3849b39ca5eb79760e970b/credible_attack/prefix_credible_exit_compiler.md`; the collision-free Q/B family in `research/current/customer_attraction/collision_free_three_halves_family.md`; PB in `R-cd789330fc7141299ac491bbb3ffa420/round5/menu/pair_attack.md`; Beta identities and genuine lift gap in `R-65d0f88edf3849b39ca5eb79760e970b/background_salvage_next/clone_collision_debt_and_credible_gap.md`.

## 4. A concrete legal shared-omission candidate, not a credible threat menu

For arbitrary k>=4 let m=k+1. Take disjoint group blocks X_i of size2 and Q_i of size3, and a disjoint reservoir D=E_0 union E_1, each E_e of size4. Put A_i=X_i union Q_i. The *entire* common catalog is

    C_i=X_i,
    H_i^e=A_i union E_e   (e=0,1),
    P_ij=A_i union A_j   (i<j),
    D.

All sets are actual sets of distinct unit customers, with no invented continuation payoffs. Consider only the target path C_1,...,C_k,D. Its last action is a genuine BR: D pays8, every H_i^e pays1+3+4=8, every P_ij pays2(1+3)=8, and every C_i pays1. Thus this path is a legal j=m-1 input to the repair theorem, regardless of whether its earlier actions are credible. Its exact welfare is W=2k+8. Pair topics cover all groups in at most ceil(k/2) actions; D covers the reservoir. Therefore OPT_m=5k+8 and the old half gap is k-8, positive for k>=9.

The intended economic idea is that a deviator's reservoir half could be covered repeatedly by other-group actions, while punishers choose the complementary reservoir half and share the deviator's A_i. Pair topics could free enough slots to cover every other group. **There is no complete SPE construction establishing that intended threat.** In particular, a low final payoff cannot be assigned to a punisher while fresh pair alternatives remain available.

There is already an exact unavoidable endgame deficit. At the penultimate normal history C_1,...,C_(k-1), force P_(k,j) for any j<k. It attracts5 customers from previously untouched group k and payoff4 from previously touched group j, before the last action. Every last action touching either selected group has payoff at most13/2<8; D and untouched-group alternatives pay8. Hence every last BR avoids both selected groups (or chooses D), and the fixed deviator receives exactly9. Thus

    ell_penultimate(P_(k,j))=9,
    delta_penultimate>=9-2=7,
    2R+D>=21.

So even this candidate's positive old gap is certainly insufficient for k<=29. No estimate is currently proved that controls the other roles' true floors for unbounded k. In particular, taking k large is not a counterexample: R may grow linearly because future punishers retain attractive unused-group alternatives. The concrete all-k catalog is saved as a possible analytical test of genuine continuation-floor mechanisms; no finite negative scan or unvalidated menu is presented as evidence for or against general half.
