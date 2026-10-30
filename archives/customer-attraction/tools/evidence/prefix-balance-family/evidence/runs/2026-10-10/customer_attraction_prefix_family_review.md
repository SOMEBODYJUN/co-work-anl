# Independent review of the all-n prefix-balance family

Reviewer: `/root/security_bridge_v2`, independently of the construction author. Date: 2026-10-10. Reviewed the construction draft and [canonical proof](../../../research/current/customer_attraction/prefix_balance_family.md), with the same construction, equations and history classification.

**Conclusion: passed.** No gap was found in the claimed family for every integer n >= 4, or in its quantified failure for every fixed real multiplier alpha < 2. This is an internal review, with no external review recorded. The result concerns the specified first-prefix inequalities; it does not refute root half coverage, root total tax, or the unrestricted security bridges.

## Universal algebra reviewed

The customer groups were recomputed directly: every normal leaf has x private, one A-shared and x B-shared customers; the special leaf has x private, x B-shared and n-1 A/B-shared customers, where x=n-2. They partition all customers, with total 2n(n-2)+2(n-1).

The complete last-player classification was checked against these customer groups. In the first two classes the Jensen bound has denominator (n-2)b+2(n-1)-a-ell_j, and its simpler bound follows from b <= n-1-a-ell_j. The delicate normal-leaf comparison at a=ell_j=0 reduces to (n-1)^2(n-4) >= 0, including permitted equality at n=4. The A comparisons reduce respectively to n^2-2n-1 >= 0 and n^2-4n+2 >= 0. The three remaining classes have the displayed explicit terminal payoffs and strict comparisons. The tie rule always has an available fresh normal leaf.

All four nonlast history classes were checked using the actual prescribed continuation after each possible current action. The common B-background argument is valid only in its stated class: every follower's actual rule chooses B after every deviation. In the one-normal-leaf class the B continuation value is x+2x/(n-1)+(n-1)/x. In the one-special-leaf class it is n+1-1/(n-1)-1/n. Their comparisons, and the all-B/root comparisons, are correct and exhaust every nonlast ordered history. Thus the universal pure-SPE conclusion follows from the algebraic classes, including off-path histories.

The path values were independently recomputed as u_1=n-1/n, u_i=n-1/n-1/(n-1) for i>=2 and W=n^2-2. Positive private leaf groups force the unique optimal support to contain all n leaves, giving OPT=2n^2-2n-2. The maximum extension after A is F_(n-1)(A)=2(n-1)^2, by separately considering whether B is included. Consequently B_1=4-n-1/n<0. The required first-prefix multiplier tends to 2 from below; for 0<=alpha<2, n>4/(2-alpha) suffices, while alpha<0 already fails at n=4. The half-coverage slack 2(n-1) and root-tax slack (n-3)/2+1/(n-1)+1/n are positive.

## Independent finite exact replay

[independent audit](../../../tests/audits/customer_attraction_prefix_family_independent.py) does not import author code. It builds the customer types directly, computes utility using an exact common denominator, follows every current action through the complete specified continuation, and checks the last-player classification. It exhausts n=4,...,8 count states and applies their permutation multiplicities to represent all ordered histories of this particular count-based strategy. This does not impose count-based strategies on general pure SPE.

The replay passed 26,154 count-state decision nodes and 252,635 action comparisons, representing 11,749,491 ordered decision nodes and 116,812,702 ordered action comparisons. It also independently checked W, OPT, F, u_1, B_1 and the tax/half slacks for every audited n. The exact JSON output is [frozen exact report](customer_attraction_prefix_family_independent.json). Finite replay supplements the universal algebraic proof; finite replay alone is not a proof for every n.
