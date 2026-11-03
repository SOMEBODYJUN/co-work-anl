# Round 13 adversarial work: status and exact scope

Main target: arbitrary common finite catalog, exactly five unit providers,
arbitrary finite unit clients, full ordered-history pure SPE, `OPT5 <= 2W`.
**Still OPEN.** No counterexample or new universal payment bound was found here.

## Candidate triage

The known 728-row bad point was already excluded by the joint AB-to-AE
`(R,S)` OO condition. The relevant existing proof is
`R-c4732bee2f7b4e50a70568170e3334ae/round5_coupling/README.md` and
`exact_joint_728_separation.json`. The old 2016-row audits also already include
easy own-family diagonal/offdiagonal splits. These were read, not rediscovered
or re-audited here.

Direct13 then proposed the strong static optimal-portfolio matching bridge
`min_pi sum_i u_i(T_pi(i), s_-i) <= W`. The finite attacks below were stopped
when the parent recovered two existing full-SPE counterexamples:

* old52, m=4, W=47, OPT=52, every optimal matching costs at least 48;
* old1953, m=3, W=1735, OPT=1740, every optimal matching costs at least 1736.

Their exact sources are
`R-a0bb57fa24044a8794bc7991918a19c6/static_matching/optimal_static_matching_counterexample.md`
and
`R-105f776c3e6d4a22bb7c380c5df8edc7/dynamic_exchange/static_optimal_assignment_counterexample.md`.
They exclude even choosing a favorable optimal portfolio. The weaker
`Q <= (1+1/m)W` remains OPEN. No strategy-cone LP was started here.

The candidate `u_i >= u_m/2` for every i<m is also already FALSE: the existing
seven-client m=3 full SPE `(0,1,3)` has payoffs `(3/2,2,7/2)`.
See `R-18e993ca519949aba29e030d3d7b15b3/next_boss/terminal_clone_counterexample.md`.
The aggregate `u_m <= 2W/(m+1)` was not disproved by that example; its OPEN
status is unchanged. No finite negative result here supports a universal claim.

## Frozen finite work

`attack_static_matching.py` verifies the supplied complete policy before
checking every optimal length-m topic multiset by exact assignment DP.
`static_matching_frozen.json` records 17 certificates from the old examples
directory. All pass, because the counterexamples above reside in other
personal workspaces; this is not evidence overriding those counterexamples.

`attack_static_matching_outcomes.py` checks every pure-SPE terminal count
returned by the existing set-valued exact BI solver on 20 named prior
instances, against every optimal length-m multiset. Matching cost is unchanged
by permuting actual player rows, so terminal counts suffice for this diagnostic.
`static_matching_all_outcomes.json` freezes the exact results, including the
five-provider ten-topic instance's 124 endpoints and 216 optimal multisets.
No universal inference is made from these finite non-refutations.

## Representation observation

For an indexed incidence template invariant under simultaneous permutation
of five comparison indices, a rational incidence realization can be averaged
over S5 by cloning each client over all 120 permutations. This preserves every
recorded symmetric orbit sum and makes all individual inequalities *within a
single S5 orbit* have equal aggregate values. Different equality-pattern
orbits must remain separate: diagonal and offdiagonal comparisons are not one
orbit. Therefore merely splitting a retained single-orbit sum into individual
index inequalities adds no incidence restriction after this symmetrization.
Missing cross-menu coupling, different equality-pattern sums, missing true
response histories, and same-topic/same-history consistency remain additional
obligations. This observation is not an SPE-completion theorem.

No git/work.py operations were performed by this internal subagent.
