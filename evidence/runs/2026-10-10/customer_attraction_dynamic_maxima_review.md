# Independent review: dynamic maximal-theme budget

Review date: 2026-10-10. This review first reconstructed the mathematical
argument independently, before reading the author's candidate manuscript;
it then reviewed the final `research/current/customer_attraction/dynamic_maxima_bound.md`
line by line. Initial source reading was limited to the CAG model, AGENTS.md,
and the earlier universal superset-seat interface. The existing two-, three-,
and four-provider bounds were checked when reviewing the all-player corollary.
No public registrations, commits, or pushes were made by this reviewer.

Final reviewed proof SHA256:
`557148e9bf55b36d72d42f3544cdd4fd0c431f9eed23c0060f45195d3097e5b5`.

## Verdict and exact scope

**No fatal objection found.** The proposed dynamic threshold and its five-player
private/shared refinement have complete independent proofs below. They preserve
arbitrary internal subthemes, omitted cores, arbitrary legal ordered prefixes,
all history-dependent pure SPE continuations, and every tie. The five-maxima
half-coverage corollary is valid for all positive player counts when combined
with the already established arbitrary-catalog results for one through four
players. The strengthened full-union inequality `U <= 2W-c` is established here
only for `n >= 5`; it must not be extended to smaller player counts.

The separate four-maxima union strengthening in the author's equations (4)
and (14) is valid for `n>=3`, including `n<s`. The author's exact s=4 harmonic
formula (15), general mixed envelopes (21)–(23), and five-maxima Jensen
calculation (28)–(30) all passed the final manuscript review. The canonical
proof uses conservative routed prefix loads `p_I`, whereas the initial
independent reconstruction below uses the actual prefix load `a_x<=p_I`;
both yield the same stated inequalities. The canonical audit checks both.

The base theorem also allows `n=1` with `s>=2`: `D_0=s`, and the last-player
budget alone proves `u_1>=c+(U-c)/s`. The general mixed formulas apply as well:
the single raw private coefficient is `1/s` and the shared coefficient is
`2/s`; monotone envelopes have only one element. No induction step is needed.

## 1. Independent reconstruction of the dynamic budget

Let the distinct inclusion-maximal themes be `B_1,...,B_s`, `s>=2`; let `C`
be their intersection, `c=|C|`, and `U=|union B_j|`. Fix any routing of each
catalog action to one containing maximal theme. Each maximal theme necessarily
routes to itself. At an arbitrary ordered prefix of length `t`, let `p_j` be
the routed action counts, `r=n-t`, and `a_x` the actual number of prefix actions
covering customer `x`. For the incidence set `I_x={j:x in B_j}`, always
`a_x <= sum_{j in I_x} p_j`. This remains true when prefix actions omit private
customers, shared customers, or core customers.

For each `j`, define

`g_j = sum_{x in B_j, |I_x|=1} 1/(p_j+1)
       + sum_{x in B_j\C, |I_x|>=2} 1/(a_x+r)`.

If the current player chooses the whole `B_j` and no later player routes to
`j`, its total terminal payoff is at least `c/n + g_j`. Indeed a globally
private customer can only be covered by a routed-`j` action and therefore has
terminal multiplicity at most `p_j+1`; a shared customer has multiplicity at
most `a_x+r`; every core customer has multiplicity at most `n`.

For `r>=2`, set `y_j=p_j+r/2`, so `Q=sum y_j=t+sr/2`. A private customer pays
the coefficient `y_j/(p_j+1)>=1`. A noncore shared customer pays

`sum_{j in I_x} y_j/(a_x+r)
 = (sum_{j in I_x}p_j + |I_x|r/2)/(a_x+r) >= 1`.

Consequently `sum_j y_j g_j >= U-c`, and one `j` satisfies
`g_j >= (U-c)/Q`. For `r=1`, use `y_j=p_j+1` and `Q=t+s=n+s-1`; the same
customer budget remains valid (a shared incidence contributes at least two
added weights while its denominator has only one added current player).

Set `D_t=max(t+s(n-t)/2,n+s-1)` and
`theta_t=c/n+(U-c)/D_t`. Since `s>=2`, `D_t` is nonincreasing in `t`, so
`theta_t` is nondecreasing. The chosen `j` therefore gives the current player
at least `theta_t` if no successor routes to `j`. If a successor routes to
`j`, its action `A` is a subset of the current player's whole `B_j`; at that
same terminal outcome, `u(B_j)>=u(A)`. Backward induction gives that successor
at least `theta_l>=theta_t`, where `l>t` is its prefix length. This uses
**total payoff dominance**, so successors may omit the core. Removing the core
before this dominance comparison would require a separate argument and is
unnecessary.

The last-player case follows from the `r=1` budget and ordinary best-response
optimality. Every off-path deviation uses the given complete SPE's actual
continuation at that exact ordered history, which is again an SPE. Current
SPE optimality transfers the deviation guarantee to the current player. This
proves the threshold at all prefixes, with all ties allowed. Summing its
root-path version gives `W >= c+(U-c) sum_{t=0}^{n-1}1/D_t`.

The maximum with `n+s-1` is needed by this induction: at `r=2` the unmodified
budget is `n+s-2`, while at `r=1` it is `n+s-1`, producing the wrong threshold
direction without the maximum.

## 2. Five-player, at most five maxima refinement

Assume `n=5`, `2<=s<=5`; partition the residual union into globally private
customers (`P` total) and noncore shared customers (`V` total), so
`U=c+P+V`. For `r>=2`, the same weights satisfy

`y_j/(p_j+1) >= alpha_t=(5+t)/(2(t+1))`,
`Q <= Z_t=t+5(5-t)/2`.

Hence the single simultaneous budget, rather than separate choices of `j`,
gives `max g_j >= alpha_t P/Z_t + V/Z_t`. For `t=0,1,2,3`,

| t | alpha_t/Z_t | 1/Z_t |
|---|---|---|
| 0 | 1/5 | 2/25 |
| 1 | 3/22 | 1/11 |
| 2 | 7/57 | 2/19 |
| 3 | 1/8 | 1/8 |

All private coefficients are at least `1/9`. At `r=1`, `Q=4+s<=9`; every
shared incidence has `d>=2`, `p_I<=4`, and `a_x<=p_I`, giving

`(p_I+d)/(a_x+1) >= (p_I+2)/(p_I+1) >= 6/5`.

Thus `max g_j >= P/9 + 2V/15`. The shared coefficients
`b=(2/25,1/11,2/19,1/8,2/15)` are strictly increasing, and the private
coefficient is held constant. The same total-payoff dominance induction gives
the current-player floor `c/5+P/9+b_t V`. Summing yields

`W >= c+5P/9+(67027/125400)V >= (U+c)/2`.

The numerical shared coefficient is approximately `0.53450558`, greater than
one half. With at most five maxima, `OPT_5=U`. A single maximal theme is a
separate trivial case: the last player strictly prefers the whole maximal
theme to every proper subset, hence full union coverage. The definitions of
`P` and `C` overlap when there is only one maximum, so the partition formula
should not be applied there.

## 3. All player counts with at most five maxima

For `n>=6` and `s<=5`,

`D_t <= n+max(3r/2,4)`, with `r=n-t=1,...,n`.

For `n>=2`, summing the upper denominators gives exactly
`(7n^2+3n+14)/4`: the `r=1,2` terms are both raised to four, and all terms
`r>=3` use `3r/2`. Cauchy/Jensen therefore gives

`sum 1/D_t >= 4n^2/(7n^2+3n+14) >= 1/2`,

where the final condition is `n^2-3n-14>=0`, true for every integer `n>=6`.
Consequently `W>=(U+c)/2`, and `OPT_n=U` since `n>=s`.

For `n=1,2,3,4`, the established arbitrary-catalog welfare results imply
`OPT_n<=2W`, which is the required half-coverage conclusion. Those results
must not replace `OPT_n` by `U`: for `n=3`, use five disjoint maxima of sizes
`3,1,1,1,1`. Always choosing the size-three maximum is a complete SPE:
at every node its worst final payoff is one, while each size-one action has
payoff at most one. The root welfare is `W=3`, while `U=7>2W`.

## 4. Exact finite attack

The standalone `tests/audits/customer_attraction_dynamic_maxima_independent.py`
imports no repository solver, model, main audit, or previous audit. It implements a
Fraction-valued complete continuation-menu recurrence, accepting all root
actions supported by independently selectable child SPE outcomes. This
set-valued recurrence preserves ordered-history-dependent ties; it does not
force two histories with the same counts to select the same continuation.
At every legal prefix count state, it checks each supported current action
and final outcome against the dynamic threshold, the general mixed envelope,
and the five-player private/shared floor when applicable. It also checks root
welfare and weighted budgets for three independent legal routing choices.
These budget checks include the author's exact `p_I+r` denominators, not just
the stronger actual-load version. Selected roots are expanded into complete
ordered-history strategies and replayed against every legal one-step deviation.

It exhausts small catalogs on two and three unit customers; adds seeded
larger random catalogs with arbitrary internal omissions and empty actions;
and specifically attacks crossing cycle/complete-graph customer incidences
with no private customers, optional omitted common cores, and internal
subthemes with multiple maximal parents. It also checks `n=1`, singleton
maxima, empty coverage, duplicated action labels, exact s=4 harmonic values,
and the Jensen denominator sum for integers 2 through 100. The frozen output
is `evidence/runs/2026-10-10/customer_attraction_dynamic_maxima_independent.json`:

* 637 catalog/player cases;
* 95,294 exact continuation states;
* 105,805 supported current-payoff comparisons;
* 104,864 general mixed-envelope comparisons;
* 16,657 five-player refined-floor comparisons;
* 1,544 root terminal outcomes;
* 128,481 actual-load prefix-budget/routing comparisons;
* 127,323 author-form routed-load budget comparisons;
* 313 complete ordered-history strategies;
* 1,379 ordered decision histories and 5,596 direct deviation comparisons;
* 357 singleton-last-player comparisons and 15 duplicate-label cases.

All passed. These finite checks audit the reconstruction and attack possible
counterexamples; the universal conclusion rests on Sections 1–3, not on the
finite sample. No external peer review or literature-novelty review is claimed.

Run from the repository root:

```sh
python3 tests/audits/customer_attraction_dynamic_maxima_independent.py
```

Default execution only prints its report. `--output <path>` creates a new
report and refuses to overwrite any existing frozen report. The report records
the current script and proof SHA256 hashes. Its frozen script hash is
`f482fee613d11f91eb3865893ffdedf68314f09c78d250467f9d30c2accdc76b`.

## 5. Singleton wording and final promotion decision

The author's unique-maximum discussion is correct in the unit-customer model.
For clarity, the direct argument is: at any last-player prefix, replacing a
proper subset by the whole unique maximum leaves every already selected
customer's share unchanged and adds a strictly positive share from each
omitted customer. Every best response therefore has the full maximal coverage;
duplicate fullmax labels can tie as actions, but their coverage is identical.
If the maximum is empty, every catalog coverage is empty. This is an editorial
clarification, not an unresolved proof obligation or required mathematical fix.

**Final decision: promotion to complete universal proof with independent internal
review is supported for the exact claims stated in the final manuscript.**
Finite audit, universal proof, and external-review/novelty status remain separate.
