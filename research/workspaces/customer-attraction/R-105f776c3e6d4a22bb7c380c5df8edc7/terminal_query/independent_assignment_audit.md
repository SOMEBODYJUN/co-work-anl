# Independent exact audit: seq242 optimal-assignment bridge

2026-10-24. **The submitted auxiliary counterexample passes this independent
audit.** It refutes the named seq242 existential static-assignment bridge.
It does not refute Q-CAG-HALF, which remains OPEN. No novelty or external
review claim is made.

## Exact audited assertion

The assertion under attack is: for every true full-history pure SPE terminal
`z`, there exists an optimal m-topic tuple `(T_1,...,T_m)` and a permutation
pi such that

`sum_(i=1)^m u_i(T_pi(i), z_-i) <= W(z)`.

Here `u_i(T,z_-i)` replaces only player i's actual action by T and freezes
all other actual terminal actions. It is a static query; it is not the
SPE deviation with responsive successors. The raw policy is used separately
to verify genuine SPE deviations at every legal ordered history.

## Independence and raw identity

Before writing or running this audit, I read only these two raw files:

- `../dynamic_exchange/assignment_instance.json`, SHA256
  `2ae935f6980037f3526eee447021a6e2d8d5987e0bb2b2c31d4017afad7126c4`.
- `../dynamic_exchange/assignment_full_policy.json`, SHA256
  `1c59b0406e8fdd56e01fc4a2d1c03b9dd15a9aefc0748a556fb08cf593fa27ac`.

I did not read or import the author's derivation, audit, solver, or model
implementation. Parent's provisional numerical expectations were not used
in any acceptance condition. The audit computes every claimed value from
the raw input and checks the raw bytes remain unchanged at the end.

The current frozen instance has m=3, six distinct legal topics, 63 positive
interest types, and **1953 separate unit customers**. The earlier task
message's N=114975 described an earlier bias size; it is not the audited
input. Every topic has 992 customers. All six topics contain positive
singleton-interest blocks and are therefore distinct. None is empty.

## Two exact evaluators

`independent_assignment_audit.py` uses only Python's standard library.

The first evaluator creates a distinct customer identifier for each unit
of every input multiplicity, constructs the six literal customer sets,
and evaluates each terminal by counting its individual client loads.
Payoffs are stored as integers multiplied by lcm(1,2,3)=6.

The second evaluator uses the raw compressed type rows directly, with
`fractions.Fraction`, and divides each multiplicity equally among the
players whose chosen actions interest that type. These two evaluators
agree on every player's payoff and on coverage for **all 216 ordered
legal three-topic tuples**, including every repeated-action tuple. Their
payoffs also sum to coverage in every tuple.

Only legal catalog actions are enumerated; an empty topic is not silently
added to this catalog. The empty profile has zero coverage, and every
nonempty tuple of fewer than three topics can be padded by repetition of
a legal action without changing coverage. Thus the exact-three tuple
enumeration also covers the at-most-three optimum convention.

## Complete SPE check

The raw policy supplies exactly all `1+6+6^2=43` ordered decision histories,
including histories with repeated actions. For every such history h and
every legal forced next action, the audit independently follows the raw
policy to its complete terminal and compares the acting player's payoff
with the prescribed continuation payoff. Successors are allowed to react
according to that same raw policy; none is frozen.

All **258 comparisons**, including self actions, are nonnegative. Among
the **215 nonself comparisons**, 154 are strict and 61 tie. There are no
violations. This certifies a full ordered-history pure SPE, including all
off-path choices and repeated-action histories.

Its actual terminal and exact payoffs are

`z=(0,3,4)`,

`u=(1733/3,1736/3,1736/3)`,

`W=1735`.

## Global optimum and every assignment

Exhausting all 216 legal ordered tuples gives `OPT_3=1740`. There are
exactly six optimal ordered tuples: the permutations of `(1,2,5)`. Thus
the unique optimal support is `{1,2,5}`; repeated-action tuples are not
optimal.

For clarity the relevant static query matrix below has been multiplied
by 3. Column i is the payoff from placing the indicated topic at actual
player i while retaining the other two actual actions from `(0,3,4)`.

| Assigned topic | Player 1 | Player 2 | Player 3 |
| --- | ---: | ---: | ---: |
| 1 | 1736 | 1739 | 1736 |
| 2 | 1733 | 1736 | 1736 |
| 5 | 1736 | 1739 | 1736 |

The audit explicitly checks every optimal ordered tuple and all six slot
permutations, giving 36 quantified cases. They reduce to the following
six distinct assignments of topics to actual players:

| Assignment `(T_for_1,T_for_2,T_for_3)` | Static payoff sum |
| --- | ---: |
| (1,2,5) | 1736 |
| (1,5,2) | 1737 |
| (2,1,5) | 1736 |
| (2,5,1) | 1736 |
| (5,1,2) | 1737 |
| (5,2,1) | 1736 |

Consequently

`min_(optimal tuples T, permutations pi) sum_i u_i(T_pi(i),z_-i)`

`=1736 > 1735=W`.

This is the required strict failure of the existential-assignment bridge.
The half inequality has large positive slack:

`2W-OPT_3=3470-1740=1730 > 0`.

No claim about failure of half, FTA, the free full-terminal menu, or a
general impossibility of proof follows from this auxiliary separation.

## Reproduction and retained evidence

From the repository root:

```
python research/workspaces/customer-attraction/R-105f776c3e6d4a22bb7c380c5df8edc7/terminal_query/independent_assignment_audit.py
```

The script and `independent_assignment_audit.json` retain the raw hashes,
all 216 coverages, all 258 true SPE comparisons with their complete leaves
and rational slacks, the complete static matrix, and all 36 assignment
checks. The audit rewrites only its own output JSON. It performs no solver
search, external action, shared-file edit, commit, or push.
