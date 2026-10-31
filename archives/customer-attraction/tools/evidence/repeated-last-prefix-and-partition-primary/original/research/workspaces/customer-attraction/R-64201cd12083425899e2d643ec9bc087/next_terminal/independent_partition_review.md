# Independent audit: fourteen-client PFR-OPT-v1 counterexample

Result, 2026-10-21: **the stated PFR-OPT-v1 auxiliary bridge is refuted**.
The input remains a legal two-player common-catalog CAG with fourteen distinct
unit customers. This does not refute Q-CAG-HALF or the two-player welfare
bound. No global minimality or external review is asserted.

I read the nine customer types and the strategy from
`../next_boss/partition_attack/small_exact_witness.json`. The independent
standard-library program `independent_partition_audit.py` expands the fourteen
unit clients, imports neither the author's audit nor the canonical CAG
implementation, and uses no stored payoff, welfare, optimum, or partition
values from the source JSON.

The strategy chooses 0 at the root; the replies after 0,...,5 are respectively
1,4,4,5,5,4. Recalculation at all seven ordered decision nodes gives the root
action values

    (4,7/2,4,4,4,4).

At the six last nodes the prescribed actions attain respectively
4,11/2,5,5,4,4, and each is a maximum over all six legal actions. Thus all
42 exact action comparisons hold, including every off-path history and tie.
The actual path is (0,1), with payoffs (4,4) and W=8.

All 36 ordered length-two comparison tuples were checked, including every
repetition. The only optimal ordered tuples are (2,3) and (3,2), both covering
ten customers; every other tuple covers at most nine. Repetitions therefore
cannot supply a different optimal portfolio, and both possible orders have
been covered.

There is a short direct check of the universal partition quantifier. Themes
2 and 3 are disjoint, each containing five customers. Hence every covered
client has exactly one eligible optimal occurrence, and its partition owner
is forced. Each optimal theme contains exactly two customers of actual theme
0 and no customer of actual theme 1; its other three customers are uncovered
by the actual profile. Matching an optimal theme to actual player 0 costs
2+3=5, since its two actual covers are removed. Matching the other optimal
theme to player 1 costs 2/2+3=4. Consequently every matching has minimum
partitioned frozen query

    R=5+4=9>8=W.

Swapping the optimal order produces the same two matchings. There is no
hidden fractional or per-type partition option: eligibility is unique for
each individual client. Even allowing a fractional split cannot lower this
value when there is only one eligible occurrence.

The exact independently generated report is
`independent_partition_small_audit.json`. The original 127-client discovery
was independently checked first and is preserved in
`independent_partition_audit.json`; it also passed all histories, all 36 ordered
comparison tuples, and all optimal matching/partition choices. The fourteen
client version is the primary reviewed witness.

Half coverage holds with strict slack 2W-OPT=16-10=6. The accurate conclusion
is failure of the stronger existence-of-optimal-portfolio partition-payment
bridge, not failure of the original sequential half-coverage conjecture.
