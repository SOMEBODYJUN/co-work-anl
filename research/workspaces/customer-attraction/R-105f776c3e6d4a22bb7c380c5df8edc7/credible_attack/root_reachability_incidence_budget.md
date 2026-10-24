# Incidence-budget obstruction to an actual SPE prefix

2026-10-24. **General lemma, direct proof; independent review pending.** This is a root-reachability component for the original unit-client, common-catalogue, complete ordered-history pure-SPE model. It does not prove Q-CAG-HALF, an extra-one security floor, or any welfare comparison between mutually exclusive branches.

## 1. General statement

Partition the client universe as `N=R disjoint-union D`, with both parts nonempty. A **D-singleton action** is a catalogue topic `{x}` with `x in D`. Fix positive integers `alpha,a,q` such that:

1. Every catalogue action is either a D-singleton or contains at least `alpha` clients of R.
2. Every action that touches D and is not a D-singleton contains at least `a` clients of R.
3. At least one legal topic T contains at least `q` clients of R.

Let h be an arbitrary legal ordered prefix, let b be its client-load vector, and let r be the number of players after h. Define

\[
 I=\sum_{x\in R}b_x,\qquad
 \beta=\max_{x\in R}b_x,\qquad
 B=\min_{x\in D}b_x.
\]

Suppose

\[
 B>I/a,\qquad
 qB>\beta+\lfloor I/\alpha\rfloor+r+1.\tag{RB}
\]

Then **h cannot be the actual prefix of any complete ordered-history pure SPE** of the game with `|h|+r` players. This quantifies every possible ordered realization h of b in the stated catalogue, and permits arbitrary history-dependent off-path continuations and arbitrary ties.

The conclusion concerns this load vector and this catalogue. It does not exclude altered background loads, altered client encodings, an enlarged catalogue, or added incentives.

## 2. Proof

First, some D-singleton action must occur in h. Otherwise a fixed client x in D is covered only by actions that each consume at least a R-incidences. There are at most `I/a` such actions in the entire prefix, so `b_x<=I/a`, contrary to `b_x>=B>I/a`.

Let i be the **last** D-singleton action in h, and write that action as `{x}`. Let L be the number of subsequent actions in h. Each of these L actions is not a D-singleton and therefore contributes at least alpha R-incidences. Hence

\[
 L\le\lfloor I/\alpha\rfloor.\tag{1}
\]

Under any continuation after h, player i's prescribed final payoff is at most

\[
 \frac1{b_x}\le\frac1B.\tag{2}
\]

At player i's decision node there are `L+r+1` players still to act, including i. Before i acts, every R-client has load at most beta, because all actual prefix loads only increase on the way to b. Force player i instead to select the legal topic T from assumption 3, and then follow **any** continuation whatsoever. Every client of `T intersect R` has final load at most

\[
 \beta+L+r+1
 \le\beta+\lfloor I/\alpha\rfloor+r+1.
\]

Therefore this deviation's final payoff is at least

\[
 \frac{q}{\beta+\lfloor I/\alpha\rfloor+r+1}
 >\frac1B.\tag{3}
\]

The strict inequality is exactly the second inequality of (RB). Equations (2)-(3) give a profitable deviation at an actual node. In particular no continuation threats, credible or otherwise, can restore SPE optimality there. This contradiction proves the lemma.

The argument compares the prescribed branch with its true deviating continuation only through a continuation-independent denominator bound. It never freezes later actions or transports a payoff between branches.

## 3. Exact specialization to the round-5 PB background

Source: `R-cd789330fc7141299ac491bbb3ffa420/round5/menu/pair_attack.md`, sections 2-3. Keep its exact catalogue and exact target background b. The source constructs an arbitrary-background subgame counterexample; it does not claim that b occurs on an actual root-SPE path.

Take R to be all real-block clients and D all dummy-block clients. The parameters are

\[
 d=20,\quad Q=2063,\quad q_{\rm block}=12,\quad
 H=100000,\quad M=10^9,\quad r=2475.
\]

Every non-D-singleton action is a real singleton or a regular action, so `alpha=1`. Every regular action covers at least one complete real block in each of the d segments; in particular every non-D-singleton that touches D covers at least `a=240` real clients. A regular topic supplies `q=240` in assumption 3. The exact background has

\[
\begin{aligned}
 I&=dQ(q_{\rm block}M+1)
   =495120000041260,\\
 \beta&=M+1=1000000001,\\
 B&=HM=100000000000000.
\end{aligned}
\]

The first strict inequality follows from

\[
 aB=24000000000000000>I=495120000041260.
\]

The second strict inequality is

\[
 qB=24000000000000000
 >\beta+I+r+1=495121000043737.
\]

Consequently **no legal ordered prefix in that exact catalogue realizing that exact b can be an actual root-SPE prefix with r=2475 players left.** This is stronger than ruling out only the literal all-singleton realization. It does not dispute the valid arbitrary-background SPE construction: every such prefix is still a legal history and may be off path.

## 4. Root-welfare accounting and remaining boundary

For any actual prefix, let `H_b={x:b_x>0}`, and let J be the clients first covered by its continuation. For that one actual complete terminal history,

\[
 W=|H_b|+|J|,
\]

and, exactly,

\[
 \sum_{\text{prefix }i}u_i
 =\sum_{x\in H_b}\frac{b_x}{b_x+d_x},\qquad
 \sum_{\text{tail }i}u_i
 =|J|+\sum_{x\in H_b}\frac{d_x}{b_x+d_x},
\]

where d is the continuation load. Thus the already-covered support is one welfare pool, divided between prefix profits and continuation rents. It cannot be omitted from a root efficiency calculation or charged twice.

For any comparator union C using at most the full game's player count,

\[
 |C|-2W
 =|C\setminus H_b|-|H_b|-2|J|-|H_b\setminus C|.\tag{4}
\]

In particular, the round-5 background covers the entire original client universe, so its original instance cannot have a positive root half deficit, independently of reachability. The incidence-budget lemma adds a separate strategic obstruction to making its exact background an actual prefix.

Neither (RB) nor (4) proves a useful uniform inequality for arbitrary reachable backgrounds. Backgrounds that fail (RB) remain unrestricted by this lemma. A genuine Q-CAG-HALF construction must retain the full optimal m-topic constraint, all already-covered welfare, and actual-prefix incentive compatibility; none of these has been eliminated in the general case.

## 5. Status and next useful question

No finite search is used. The proof is the general incidence count and the universal forced-action payoff floor; the displayed specialization uses exact integer arithmetic. No claim of external review or novelty is made.

This provides one necessary condition on actual root-SPE reachability. It does not establish that every bad arbitrary-background security gadget incurs enough root welfare to prove half. A worthwhile next step would be a general inequality relating the support/rent budget of a reachable background to its omitted optimal coverage; that inequality is not proved here.
