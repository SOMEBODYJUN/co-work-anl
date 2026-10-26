# Actual-suffix potential envelope: independent exact audit

2026-10-26. Scope: `CA-SIX-ACTUAL-SUFFIX-POTENTIAL-ENVELOPE-OBSTRUCTION-v1`.
I read only `../parent/suffix_envelope_input.json` before constructing and
running `audit_suffix_envelope_independent.py`. I did not import or read the
parent verifier. The audit expands the 6,000 distinct unit customers, uses
integer arithmetic in units of 1/60, and enumerates all 18,563 comparison
multisets independently. The final report is
`suffix_envelope_independent_audit.json`.

**Result: the proposed boundary is correct.** The twelve themes are valid
distinct customer subsets. The nominated path is `(A1,...,A6)`, and

`u=(717/2,416,871/2,957/2,1093/2,705)`, `W=2940`, `OPT_6=6000`.

Each customer belongs to exactly one T-theme, so `(T1,...,T6)` covers every
customer and certifies OPT. Thus `OPT_6-2W=120>0`. This statement concerns
the nominated path and the specified necessary inequalities; it is not a
counterexample to the SPE half-coverage claim.

At position i let `b_i(x)` be the actual prefix load and `r=7-i`. All 72
safe inequalities

`u_i >= sum_(x in Q) 1/(b_i(x)+r)` for every catalog theme Q

hold. Their minimum slack is zero.

For a legal r-multiset D define its relative harmonic potential by

`Phi_b(D)=sum_x sum_(j=1)^c_D(x) 1/(b_i(x)+j)`.

The tested suffix envelope is precisely

`Phi_b(D) <= sum_(j=i)^6 u_j + C_i`,

where

`C_i=sum_(j=i)^6 sum_(x in A_j) [1/(b_j(x)+1)-1/(b_j(x)+7-j)]`.

This uses the actual full-terminal final profits and actual prefixes. It
does not replace them by hypothetical optimal-tail profits or freeze a
deviating tail.

| Start i | r | Multisets | Maximum relative potential | Budget | Minimum slack |
|---|---:|---:|---:|---:|---:|
| 1 | 6 | 12376 | 18019/3 | 60213/10 | 449/30 |
| 2 | 5 | 4368 | 13147/3 | 21989/5 | 232/15 |
| 3 | 4 | 1365 | 12887/4 | 16171/5 | 249/20 |
| 4 | 3 | 364 | 34016/15 | 11421/5 | 247/15 |
| 5 | 2 | 78 | 42863/30 | 7227/5 | 499/30 |
| 6 | 1 | 12 | 705 | 705 | 0 |

Order does not affect a comparison tuple's loads or relative potential,
so multiset enumeration covers every ordered r-tuple, including all
repetitions. Every actual prefix and all twelve catalog themes are
included. The input has no empty theme, which is allowed for an explicit
counterexample to the sufficiency of a universal necessary-condition
system; the full target retains empty themes.

**The nominated path is strictly incompatible with SPE.** At the actual
four-theme prefix, if player five changes to any T_j, the unique last best
reply is A6. The deviator receives `20003/30`, exceeding its nominated
profit `1093/2` by `1804/15>0`. Alternatively changing to A6 has the six
T-themes as all last best replies, and every one yields the deviator
`42917/60`, a gain `10127/60>0`. Consequently no choice of ties or any
completion of off-path histories can turn this nominated path into a
complete SPE.

**Accepted conclusion and its exact limit.** Safe prefix guarantees,
actual last best response, and the entire family of all actual-suffix
harmonic-potential/self-copy envelopes are jointly insufficient to imply
`OPT_6<=2W`. This does not refute the unproved proposition that every real
SPE satisfies those envelopes. It also does not refute adding true early
branch IC, cross-branch reply identities, or a different joint payment.
The audit is an internal independent finite verification, not external
review or a new universal welfare theorem.
