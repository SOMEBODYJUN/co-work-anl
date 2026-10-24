# Origin retraction into one shared role budget

2026-10-24. Personal derivation for general Q-CAG-HALF. **The target remains OPEN.** This is a general exact repair theorem for a fixed admissible payment flow, not a proof that every SPE admits a successful repair. No external novelty or independent review is claimed.

## Fixed general data

Use the exact model in `research/current/customer_attraction/model.md`: arbitrary finite unit customers and common finite nonempty catalogue, arbitrary m, and one fixed complete ordered-history pure SPE. Empty actions, repeated actions and every history-dependent tie remain allowed. Let B be its actual leaf, u its actual profits, C its covered set. Fix a comparison tuple T, with O its union and R=O\C.

Start with any point of INIT, I-PAY, R-FLOW from the peer [joint certificate](../../R-cd789330fc7141299ac491bbb3ffa420/round8/residual/linear_joint_payment_certificate.md), without imposing ROLE. In particular d_i<=u_i, H_i+J_i<=u_i, and the common cost before R arrivals is

    A_i=d_i+H_i+J_i <= 2u_i.

The I payment J is fixed throughout this construction. Only R inputs are changed. Let b_i be the total initial R mass sent from comparison owner i. Split the R flow by origin i, using the original edge fractions at every node. This is valid also where histories coalesce: split each output in the proportions of its source-tagged inputs. For mandatory edges that fraction is exactly 1/c_A(x); for common edges it lies in [0,1/c_A(x)]. Thus each origin satisfies the same linear local equations. Define

    K_il = total terminal current at actual role l from R origin i.

Strictly increasing roles give K_il=0 for l<=i and sum_(l>i) K_il=b_i. All entries are nonnegative. Define the original total role cost

    F_l=A_l+sum_(i<l)K_il,           cap_l=2u_l.

The peer mass identity gives sum_l F_l=|O|. No claim F_l<=cap_l has been made.

## General retraction relation

For each i choose y_i in [0,b_i], with y_i=0 when b_i=0. When b_i>0 put theta_i=y_i/b_i. Multiply *every* R input, edge and terminal current bearing source i by 1-theta_i. Retain the removed initial mass y_i at its actual owner i, increasing its initial current to d'_i=d_i+y_i. All H, I inputs and J remain fixed. Then the exact new role costs are

    F'_l = F_l + y_l - sum_(i<l) (K_il/b_i) y_i,       (RETRACT)

where a term with b_i=0 is zero.

Proof. Each source-tagged R system is homogeneous and linear, so source scaling preserves every flow equation and every mandatory/common edge constraint. Summing sources preserves the common edge interval because 0<=z^i<=h^i/c_A. Initial R edges only decrease, so all strengthened initial edge bounds remain valid. Each affected initial coordinate increases its current by precisely the amount removed from its outgoing edges; hence its original customer inventory is unchanged. R current belonging to origin i at role l decreases by theta_i K_il, while owner i receives theta_i b_i=y_i. This proves (RETRACT). All downstream aggregate input densities are dominated by the original ones, so the previously proved density bound remains valid, without combining same-role densities. Total mass is unchanged since sum_l K_il=b_i. QED.

**The deliberate relaxation.** d'_i<=u_i need not hold. The remaining certificate uses the single common requirement F'_i<=2u_i; it pays the additional y_i from the spare part of that same role budget. This does not claim a second application of the old IC or a new per-customer IC. Global soundness uses only inventory, conservation and the verified common role caps. The original constraint d_i<=u_i was sufficient to construct an initial point, not necessary for this final conservation proof.

Consequently, if the role caps in (RETRACT) all hold, then |O|=sum F'_i<=2W. If T is optimal, this proves HALF for that fixed instance and fixed complete SPE. This enlarges the peer certificate; no strict separation on an actual SPE is asserted here.

## Exact maximal-retraction algorithm

Set t_il=K_il/b_i when b_i>0, otherwise zero, and s_l=cap_l-F_l. The repair constraints are exactly

    0<=y_i<=b_i,
    y_l-sum_(i<l)t_il y_i <= s_l.                    (CAP)

Process l=1,...,m. Having chosen earlier y, let

    z_l=s_l+sum_(i<l)t_il y_i.

If z_l<0, stop with failure. Otherwise set

    y_l=min(b_l,z_l).                               (GREEDY)

This greedy procedure succeeds **if and only if** some origin-wise proportional retraction of this fixed routing satisfies all role caps. If it succeeds, its y is componentwise greatest among all feasible repairs.

Proof. Every feasible repair satisfies y_1<=min(b_1,s_1). Inductively, if its earlier coordinates are bounded by greedy, nonnegativity of t makes its upper bound for y_l at most z_l from greedy. Thus it cannot have a nonnegative y_l when greedy z_l<0; otherwise its y_l is at most min(b_l,z_l). Conversely a completed greedy vector explicitly satisfies (CAP). QED.

This is stronger than an arbitrary choice of proportional pruning: retaining more at an earlier role consumes only that role's available budget and weakly decreases *every* later role's cost. An earlier maximal retention cannot obstruct a later repair. It does not redistribute J or change the underlying routing K, so it is a restricted repair theorem, not an exact decision procedure for all joint certificates.

## Explicit nonnegative price witness when this repair fails

For every lambda>=0 define q_i=sum_(l>i)lambda_l t_il. Any feasible (CAP) must satisfy

    sum_l lambda_l s_l + sum_i b_i (q_i-lambda_i)_+ >= 0.   (CUT)

Indeed multiply CAP by lambda and minimize sum_i(lambda_i-q_i)y_i over the box 0<=y<=b. This uses the *same* common role cap once, including initial and all incoming current costs.

At the first greedy failure j there is an explicit violating price. Put lambda_j=1 and lambda_l=0 for l>j. Recursively downward for i<j, compute q_i and put

    lambda_i=q_i  if y_i<b_i,
    lambda_i=0    if y_i=b_i.

Then the left side of (CUT) is exactly z_j<0. To verify, use y_j=0 for this calculation. At an unsaturated earlier coordinate y_i=z_i, so its priced slack is zero; at a saturated coordinate lambda_i=0, so it contributes only b_i q_i from the box minimum. The sum telescopes to z_j. This is an exact rational dual certificate that **no origin-wise proportional retraction of this routing** can work. It is not a HALF counterexample, not a separator for all optional-common choices, and not a claim that no optimal T works.

## What this adds and what it does not pay

The new general relation is RETRACT plus the exact greedy/cut theorem. It lets an overloaded later role give back all of the part of its current demand traceable to an earlier source, paid from the earlier role's unused share of its same two-wallet budget. It uses the already retained source labels and never gives each context a separate u_l.

No general theorem here proves greedy success on SPE data. The proof uses no new off-history incentive restriction: it takes the peer admissible flow and its actual profits as input. In particular sum F'=|O| still makes the constant-price total requirement exactly the original unknown |O|<=2W. The unresolved obligation is to use the complete SPE rows, or to choose T/initialization/routing, to ensure all greedy z_l are nonnegative (or to bypass this sufficient family).

## m=5 pressure test of this same general derivation

Write rho_i=1-y_i/b_i when b_i>0 and rho_i=1 otherwise. The five role caps after greedy are exactly

    A_1+y_1 <= 2u_1,
    A_2+rho_1 K_12+y_2 <= 2u_2,
    A_3+rho_1 K_13+rho_2 K_23+y_3 <= 2u_3,
    A_4+rho_1 K_14+rho_2 K_24+rho_3 K_34+y_4 <= 2u_4,
    A_5+rho_1 K_15+rho_2 K_25+rho_3 K_35+rho_4 K_45 <= 2u_5.

Here b_5=y_5=0. The first cap is unconditional from A_1<=2u_1 and greedy; the other four are **not proved automatic** by the present general mechanism. Therefore this does not unconditionally derive OPT_5<=2W. The exact newly usable outcome is either a successful capacity repair for a fixed certificate or a precise CUT locating the failure of that fixed repair. No five-player special optimization or special positive theorem is proposed.

## Boundary and tie checks

* All-zero customers: u,A,b,K,F are zero, greedy y=0 and every cap is equality. No ratio of welfare or 0/0 is used.
* Empty actions: they carry no positive R source coordinate or current; all definitions and scaling remain valid. If b_i=0 its t row and y_i are explicitly zero.
* A full-universe theme is present: choosing T=B=(N,...,N) at the all-full SPE gives b=H=J=0, d_i=u_i=|N|/m, hence no repair is needed. Backward induction makes each actual prescribed coverage full at every history when N is nonempty: once later players take full, any strict subtheme loses a positive contribution, so the current best reply is full. Empty N reduces to the zero case. Equivalent labels retain ties.
* Arbitrary complete ordered-history ties: no action, completion leaf, history or tie is changed by retraction. We scale proof amounts only. Histories with identical customer counts are never identified. Thus all original complete SPE choices remain intact; the repair theorem is uniform over them.

The accompanying exact audit uses a fixed existing full-SPE fixture and the established all-big m=5 family only to check this candidate construction, not as evidence of universal success.
