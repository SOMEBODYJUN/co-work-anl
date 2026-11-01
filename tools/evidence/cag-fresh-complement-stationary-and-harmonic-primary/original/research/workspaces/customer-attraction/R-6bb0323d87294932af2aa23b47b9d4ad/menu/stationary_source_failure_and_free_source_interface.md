# Successor occupation balance is too rigid for the full-root menu

2026-10-24. Personal checkpoint. General Q-CAG-HALF, free Mfull, and Mpath remain OPEN. The result below rejects one newly specified restriction on the source distribution; it is not a counterexample to any of those three targets. No new SPE instance is claimed. Independent blind review is requested separately.

## Exact candidate being tested

At an arbitrary legal history with r≥2 players left, let Z(A)=(A,Y_A) be the true complete continuation under a fixed full-history pure SPE after forcing its current player to choose A. Define the full extra-query matrix K(T,A)=Σ_(x∈T)1/[1+b_x+c_x(Z(A))], where b is the fixed earlier background. Let u be the current player's prescribed final payoff. Define the column-stochastic successor-topic matrix

    P(T|A)=# occurrences of T in Y_A /(r−1).

A possible method for constructing a non-p source distribution was:

    there exists Q∈Δ(S) with PQ=Q and KQ≤u·1.       (SS-CAP)

It uses all true successors, rather than forcing Q to equal an externally chosen query distribution p. Its motivation is that stationarity makes the average full-terminal topic marginal exactly Q. That motivation does not establish SS-CAP.

## Exact rejection on an already certified complete SPE

Use the complete eight-player, eight-topic, 32-unit-customer strategy DAG in
`R-d22a706a03c5499d941a6a97f94128a8/counterexample/pure_menu_two_block_dag.json`.
The mathematical provenance is the same directory's `pure_full_root_menu_obstruction.md`.
Each of the two disjoint blocks j has topics A_j,B_j,C_j,D_j and customer types
`{A}:2,{B,D}:4,{A,C}:6,{C,D}:3,{A,B,C,D}:1`.
In block coordinates put

    q0=(2,1,1,0), qA=(2,0,1,1), qB=(1,1,1,1),
    qC=(1,0,2,1), qD=(1,0,1,2).

Forcing root T_j gives local qT and q0 in the other block. Actual root is D_0, current payoff u=13/4, and actual W=OPT_8=32. These root terminal specifications alone are not the strategy proof: the supplied DAG has all eight children at every decision state. The independent script here expands the 32 unit customers, checks every edge, target, and all 59,496 local comparisons on all 13,872 DAG nodes. The DAG induces a legal strategy on all 2,396,745 ordered decision histories; minimum IC slack is zero.

Let α be Q's total mass in block 0. Stationarity PQ=Q is equivalent to E_Q c_T(Z(A))=8Q_T, since every complete terminal contains its source A once. The four block-0 coordinate equations are

    7Q_A0=2−α,  7Q_B0=1−α,  7Q_C0=1,  7Q_D0=α.

Summing gives 7α=4−α, hence α=1/2. The other block gives the same equations, so the stationary distribution is unique:

    Q=(3/14,1/14,1/7,1/14) repeated in both blocks.

Direct unit-customer insertion gives

    KQ=(38/15,221/105,831/280,2773/840) repeated twice.

Therefore the only stationary source has

    max_T(KQ)_T =2773/840 =13/4+43/840 >u.

This proves SS-CAP false. It does not show Mfull false: the free source
`Q(C_j)=1/14,Q(D_j)=3/7` for j=0,1 has cap 851/280<13/4. It also does not show a path cap failure: 2773/840 is already below W/8=4.

The exact replay command is

    python research/workspaces/customer-attraction/R-6bb0323d87294932af2aa23b47b9d4ad/menu/audit_stationary_source_failure.py

The audit imports neither the canonical CAG model, a BI oracle, nor the exploratory numerical script. `stationary_successor_test.py/.json` preserve an earlier six-certificate diagnostic, which made no general assertion and is unnecessary for the exact rejection.

## Pivot: retain real successor load amplification, with free Q

The following valid all-input inequality gives a free-Q interface, rather than imposing occupation equality. It is accounting backed by genuine successor IC, not a closed menu bridge.

Fix any source distribution Q over A and any independent query distribution p over legal topics T. Number the r−1 successors within a forced-root branch by j. At its true ordered history, let its original action be S_j(A), and let Z_(A;j,T) be the true full terminal if this successor alone is forced to T and all later players follow the original strategy. Define

    w_j(A)=the original successor's final payoff in Z(A),
    xi_j(T,A)=its payoff in Z_(A;j,T),
    slack_j(T,A)=w_j(A)−xi_j(T,A)≥0,
    epsilon_j(T,A)=K(T,A)−xi_j(T,A).

Every slack is an actual SPE row at an ordered history within the A-child. None compares a frozen successor coalition. Exact summation gives

    (r−1) E_(T~p,A~Q) K(T,A)
      = E_Q[sum_j w_j(A)]
        − sum_j E_(p,Q) slack_j(T,A)
        + sum_j E_(p,Q) epsilon_j(T,A).          (FQ)

In particular,

    (r−1) p^T KQ
      ≤ E_Q[sum_j w_j(A)] + sum_j E epsilon_j^+.

The paid negative terms should be retained whenever possible; replacing them with zero loses genuine successor credit.

There is a useful exact customer-level sign description of epsilon. For x∈T, at this successor history let l_x be the load of the fixed past (including forced root A), a_x=1_(x∈S_j(A)), t_x the original later load, and t'_x the later load after forcing T. Then

    (epsilon_j)_x
      =1/[1+l_x+a_x+t_x]−1/[l_x+1+t'_x]
      =(t'_x−t_x−a_x)
        /[(1+l_x+a_x+t_x)(l_x+1+t'_x)].          (AMP)

Thus positive debt requires the true later response to increase this queried customer's load by more than the coverage of the displaced original action. If a_x=0, at least one extra later coverer is necessary. If a_x=1, at least two are necessary. The last successor has t=t'=0 and therefore epsilon≤0. These assertions use integer loads, allow repeated and empty themes, and preserve arbitrary history-dependent ties. For fixed background b, all terms b are simply included in l.

To connect (FQ) to Mfull one still needs a free Q for which the actual branch tail payoffs, the signed amplification debt, and the successor IC slacks together are at most (r−1)u. That statement is not proved here. For Mpath the relevant tail rows live under every forced actual-path root A; the actual on-path successor rows alone do not supply them. Occupation balance PQ=Q neither supplies these IC rows nor pays their signed response debt, as the exact rejection shows.
