# Independent reconstruction and precise stop points

## Contract and result

I first read root `AGENTS.md` and `research/current/customer_attraction/model.md`, then the precise Q-CAG-HALF target and research entrance. I initially avoided detailed current candidate derivations. All thoughts below concern arbitrary m and finite common catalogs, with all ordered-history continuations and arbitrary equilibrium ties retained.

No new full-input welfare inequality was proved. The main candidate rediscovered independently is already present as full-terminal-tax/OCC-CAP, and the tempting stronger query bridge is already false. This file records the actual derivation and boundaries so the duplication does not become a new claim.

## 1. Why the genuine obligation is cross-branch

Fix a complete pure SPE sigma and its actual path s. At actual position i, forcing topic T produces a different full leaf z_i(T), and current optimality says

    u_i(s) >= u_i(z_i(T)).

The competition counts in the right side depend on T. Static smoothness would need a single actual opponent multiset, while the SPE inequality gives an adaptive opponent multiset. Any summation that silently replaces the latter by the former has already changed the game.

The exact potential Phi(z)=sum_x H_(c_x(z)) does not eliminate this issue. With the current player deleted,

    u_i(z_i(T)) = Phi(z_i(T)) - Phi(z_i(T) without i).

Thus a true cross-branch IC comparison includes both a full-leaf potential difference and a difference of the two deletion potentials. Dropping the deletion-potential difference freezes precisely the follower effects that the original problem permits. This is not a proof obstacle merely caused by arbitrary tie labels; it persists at the underlying outcome-correspondence level.

The exact anonymous continuation correspondence can be reconstructed without identifying histories. For a prefix-count vector b and action A, let R(b+e_A) be every terminal vector achievable by a complete pure SPE after that action. Define

    ell_A(b) = min_{q in R(b+e_A)} U_A(q),
    M(b) = max_A ell_A(b).

Then

    R(b) = union_A {q in R(b+e_A): U_A(q) >= M(b)}.

Different ordered nodes with the same b can independently select different elements of the same set R(b). This is a set-valued symmetry, not a Markov-selector theorem. Consequently a general proof can seek a structural inequality for the correspondence, but cannot identify the chosen continuations at count-equivalent nodes.

This reconstruction is existing solver mathematics, not a new result.

## 2. The independently rediscovered load formula

The known all-big family approaches ratio two at high actual load. The known collision-free family approaches 3/2 at actual load one. These suggest the full-input expression

    F(c) = sum_(x:c_x>0) [2 - 1/(c_x+1)].

The candidate OPT_m <= F(c) would imply half. Root identified it as the existing full-terminal-tax/OCC-CAP candidate, not new work here.

Its exact static decomposition is useful for diagnosing what a proof would need. Put

    G_c(T) = sum_(x in T) 1/(c_x+1),
    E(c) = sum_(x:c_x>0) c_x/(c_x+1).

Then F(c)=W+E(c). Also

    E(c) = sum_i G_c(S_i)

for the actual topics S_i. If T_1,...,T_m is any comparison tuple with comparison load d_x, clientwise

    1_(d_x>0) <= (d_x+c_x)/(c_x+1),

so

    |union_j T_j| <= sum_j G_c(T_j) + E(c).

The slack in this inequality is exactly

    sum_(c_x>0,d_x>0) (d_x-1)/(c_x+1)
      + sum_(c_x>0,d_x=0) c_x/(c_x+1)
      + sum_(c_x=0,d_x>0) (d_x-1).

Both duplicate comparison charges and actual clients outside the comparison union must therefore remain available as credit. A proof that first demands every optimal query sum <=W may throw away the very slack needed for the result.

The superficially simple sufficient bridge

    m max_T G_c(T) <= W

is already false: `R-3d2531ded15f453daef73b30eef82940/representation/README.md` points to the existing fourteen-customer, two-player complete SPE with W=9 and a missed topic whose G_c value is 5. Repeating that query gives 10>9. This does not refute full-terminal-tax because comparison duplicate slack remains positive.

The proposed replacement by once-charged union queries without outside credit is likewise too strong. The existing 71-client two-player SPE has actual W=35 and unique optimal union with 36 omitted clients, so even its once-charged omitted part exceeds W. The actual coverage outside that optimum is 33; discarding it is the error. Source:

    R-171cd7d518434f36a48cd50df29c9303/global/optimal_omission_exchange_counterexample.md

## 3. Why an apparent multi-punisher amplification did not give a new route

I considered diluting a deviation using several later punishers, each receiving an additional bank of customers, to approach two while actual coverage remained collision-free. Before a complete construction was produced, root pointed to the existing OCC-CAP reconstruction, which already records the same failure: a last punisher with a reusable bank can retain the bank and switch its shared component to a lightly covered group, increasing its share. Making those other groups heavily covered changes E(c) and consumes the very occupancy capacity being tested.

This is a duplicate diagnostic, not a new impossibility theorem. It does not exclude unequal banks, more elaborate credible branches, or a positive proof of full-terminal-tax.

## 4. Finite checks actually performed, and their limited status

All checks were explicitly aimed at the named full-input formula F(c)>=OPT_m; no fixed-m positive theorem or restricted-class project was pursued.

Before duplication was identified:

1. Exact Fraction evaluation of the actual terminal vector in 17 readable existing example/certificate pairs found no violation. This was only evaluation of those selected leaves, not every SPE of those examples.
2. A deterministic direct diagnostic tested 800 finite random instances across several small input dimensions with the canonical all-SPE outcome-set solver. No violation was found. The command was ephemeral; it was not archived as a new evidence asset.
3. `load_candidate_attack.py` generated 154 sampled complete strategies from sparse random instances. For each sampled full policy it retained every ordered-history IC row, allowed all nonempty customer types on the same finite catalog, and optimized the candidate discrepancy with floating LP. A discovered negative point would have had to pass rational reconstruction and independent full-history certificate verification before being saved. No such point was returned. This does **not** establish exact nonnegativity on any sampled cone, much less the full-input candidate. No exact duals were recovered.

Root then identified the existing route and instructed that more cone checks stop. They stopped. These checks add no general theorem and should not be promoted as new progress.

## 5. Existing sources read after independent reconstruction

- `research/customer_attraction/FAILED_ROUTES.md`;
- `research/current/customer_attraction/general_half_proof.md`;
- `research/current/customer_attraction/root_tax_counterexample.md`;
- `R-3d2531ded15f453daef73b30eef82940/GENERAL_PROOF_WORKING.md` and `representation/README.md`;
- `R-27557809587746c59216a46867c9eb07/weak_matching/{acyclic_replacement_lemma.md,partitioned_queries.md}`;
- `R-cd789330fc7141299ac491bbb3ffa420/global_mechanism/README.md`;
- `R-18e993ca519949aba29e030d3d7b15b3/round3_boss/README.md`.

These sources prevent treating static NE, CCE welfare, per-person safety, a fixed query sum, copied on-path opponents, an acyclic-branch existence hypothesis, or terminal-tax as established universal facts.

## 6. Exact remaining obligation

The load expression offers no automatic shortcut. Its proof still requires a genuinely general cross-branch relation which, after summing valid whole-topic IC rows, pays only once for missing comparison customers and retains actual customers outside the comparison union. None of the independent reconstruction above supplies that relation.

The broader safety-value idea also remains only an existing potential direction: a symmetric anonymous game may have individual SPE payoffs below its static hidden-query security value, and only an aggregate insurance statement could survive. No aggregate insurance theorem was derived here.

Current readiness: available for an independent attack of a specific mature general lemma. No new standalone mathematical claim is awaiting promotion.
