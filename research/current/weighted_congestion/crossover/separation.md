# A finite-degree separation from the full symmetric two-column topology

Claim: **WC-R3-CROSS32-TOPOLOGY-SEPARATION-v1**.

## Exact identity

Objects/domain: MODEL.md weighted atomic polynomial congestion games. Let
T_32 be the supremum of the best equilibrium factors of all degree-at-most-32
games in the one-weight-1/equal-light two-column topology of
WC-R3-FULL-TOPOLOGY-REDUCTION-v3. Principal and side latencies can be arbitrary
nonnegative-coefficient polynomials, and the common light weight can be any
positive real number. Let G be exactly the four-player, fourteen-resource
game in [README.md](README.md), with the displayed rational weights, resource
memberships, and coefficients.

Conclusion, with all parameters fixed as above:

    T_32 <= 89/50 < 9/5 < B(G),
    B(G) = min_s max{1, max_i C_i(s)/C_i(flip_i(s))}.

All costs occurring in this game's ratios are strictly positive. Equivalently,
every pure state of G has a strict 9/5-improving deviation, while every game
of the symmetric topology has an 89/50-PNE. There are no hidden restrictions
to rational inputs in the symmetric-topology upper bound.

## Proof and dependencies

The source formula-(3) supremum satisfies F_32<=89/50 by the complete
[real-parameter elimination and Bernstein proof](../source_degree32/PROOF.md).
That proof reduces a putative strict violation to n<=55, then proves the
necessary polynomial negative on every corresponding real closed interval.
The intervals are not sampled: all Bernstein coefficients on each covering
leaf are strictly negative integers after positive rescaling.

The previously frozen
[full topology reduction v3](../source_topology/proof.md) gives
T_32<=max{rho,F_32}, where rho=(1+sqrt(3))/2. To check the constant comparison
without rounded radicals, t=89/50>1 and 2t(t-1)=3471/1250>1, while
rho is the unique root above 1 of 2x(x-1)=1. Hence rho<t.
Together these imply T_32<=89/50.

For G, [degree32_certificate.json](../../../../evidence/certificates/weighted_congestion/crossover/degree32_certificate.json) records the
literal rational costs for all sixteen pure states and all sixty-four flips.
Each state has a stored player with C_i-(9/5)D_i>0. The state set is finite,
so B(G)>9/5. Its exact minimum ratio and the two minimizing states are
recorded; the endpoint B(G) is an equilibrium factor because the definition
uses weak inequalities. Finally 9/5-89/50=1/50>0.

## Independent attack and evidence

The crossover reviewer rebuilt literal resource costs without using the
candidate search program. The main researcher independently rebuilt explicit
strategy sets and resource loads in [main_check.py](../../../../tests/audits/weighted_congestion/crossover/main_check.py), compared
every stored cost, and reproduced every strict margin and the minimum.

For the source upper bound, the main researcher separately checked each step
of elimination and the n-bound. Its second verifier reconstructs the integer
polynomials without importing the author's code, transforms them directly on
each of the 1768 leaf intervals, checks strict negativity, and checks complete
interval coverage. It does not use the first verifier's midpoint recursion or
hashes as a substitute for inequalities. The actual second verification is
in [main_check_results.json](../../../../evidence/runs/weighted_congestion/crossover/main_check_results.json).

The same second reconstruction checks the degree-40 counterexample to
fixed-parameter persistence and the exact fixed-weight limiting factor
5235403/2930833. Thus simply increasing the six degrees does not preserve
the 9/5 nonexistence certificate.

Status: complete finite-instance proof and certificate-assisted real-domain
upper proof, independently internally reconstructed. No external peer review
or global priority certification. Truth is settled for these exact statements;
value is a concrete separation and reproducible certificate; novelty is
unassessed; mechanism is asymmetric resource incidence and mixed degrees;
ambition remains the unrestricted WC-TARGET problem.

## Frontier and failure scope

This is a fixed-degree separation. Neither a full-class o(d) upper bound nor
an infinite nonexistence family exceeding the original envelope follows.
The four-player bound prevents this fixed player count from producing an
unbounded equilibrium threshold. The fixed-weight degree-extension route
fails even to retain 9/5, as the exact degree-40 and limiting certificates
show. Reweighting, additional players, and new high-support resources remain
open mechanisms. Any parameterized limiting construction is registered
separately with its own quantifiers and review status.

Source equation (3): Christodoulou et al., arXiv:2002.07466v3, Section 3.
The source and subsequent related work were checked on 2026-10-14; this
limited search does not certify priority. The conjunction of source32,
full-topology v3, and the literal G certificate is the entire dependency.


---
整理来源与当前文件用途见[逐文件登记](../../../weighted_congestion_frontier/FILES.md)。程序统一通过 `python3 tests/audits/weighted_congestion/replay.py --list` 选择；历史命令、输出摘要与源码哈希属于原冻结版本。
