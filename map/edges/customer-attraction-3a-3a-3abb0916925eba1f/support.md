# 七客户基准点：全历史行、遗漏总题与回复闭包

## Exact finite input

The input has five unit providers and seven indexed labels.  Let (H) be five
unit customers and let (s,t) be two further unit customers.  The coverage map
is

\[
S_0=S_3=S_4=S_5=H,\qquad S_1=\{s\},\qquad
S_2=\{t\},\qquad S_6=H\cup\{s,t\}.
\]

The benchmark query alphabet is (J=\{0,1,2,3,4\}).  It covers all seven
customers, so \(\mathrm{OPT}_5=7\).  The integerized saved masses are
\(w_{66}=w_{68}=1,w_{121}=5\), i.e. the original normalized masses
\((1/5,1/5,1)); the actual strategy leaf is 00344 and gives every provider
payoff (1), hence (W=5).

## Full strategy and exact profile scan

The saved strategy has one action for every ordered history of lengths
0,1,2,3,4.  The number of rows is
\[
1+7+49+343+2401=2801.
\]
The fixed profile file has SHA256
`479da7e6cdc570a6dfb5443d71a7a9d45733e12cabed5553ea00c6cd2e1955c7`.
For every row it stores the prescribed payoff, all seven forced-action
payoffs, and the seven exact integer IC slacks (prescribed minus forced).

Parsing all 2801 rows gives 19607 comparisons.  For labels 0--4 (the J rows)
the counts are 0 negative, 7412 positive, and 6593 zero.  Label 5 is also
nonnegative on every row (712 positive and 2089 zero).  Label 6 has 2089
negative and 712 zero rows.  Thus every J comparison succeeds, but the full
catalog does not: the root row already has
\[
 (u(0),u(1),u(2),u(3),u(4),u(5),u(6))
   =(1,1,1/2,1,1,1,2),
\]
so the root deviation to label 6 increases payoff from 1 to 2.  All negative
rows are label-6 rows; the first is the root with slack (-1).  The exact scan
also reproduces 14005 J comparisons, 2089 full-catalog negatives, and the
original first twelve negative examples.

The benchmark is therefore a finite **restricted-IC counterexample**, not a
SPE counterexample.  The strategy is not a complete SPE, and the point does
not violate the half welfare inequality: (\mathrm{OPT}_5/W=7/5) and

\[
2W-\mathrm{OPT}_5=10-7=3>0.
\]

## Why the omitted action is structurally reachable

The full ordered action table contains
\(σ(0,3)=5\) and \(σ(0,0,0,0)=6\).  Hence the reply closure from
\(C_0=J\) adds both omitted labels and reaches
\[
C_*=\{0,1,2,3,4,5,6\}.
\]
This is exactly the hypothesis boundary in the reply-closed-catalog lemma:
restricting to (J) is safe only after all replies generated from (J) are
included and every (C_*)-action row is nonnegative.  Here the closure is the
whole catalog, and the label-6 root row remains negative, so the lemma does not
certify this strategy.

## Relation to the general obstruction

The asymptotic obstruction object uses a different explicit family (disjoint
blocks (J_i,A_i) and one union action (R)) and proves an unbounded
\(m/H_m\) ratio.  The seven-client point is not a parameter instance of that
family: it has two omitted labels, repeated H coverage, and a different policy.
It independently checks the same logical boundary—retaining all historical
rows for a chosen benchmark alphabet does not retain the omitted union action.
No claim of SPE or half failure transfers between the two objects.

## Audit records that do not pay a second strategy

The original audit preserves four full-tree records for (m=1,2,3,4), 36090
background scalar checks, and five arithmetic family summaries.  The exact
seven-client record is the only saved point with masses and all 2801 actions.
The step-22 and step-30 records store `exact:false` rationalized values and no
masses/actions; they cannot be reconstructed into complete strategies or
additional counterexamples.  No original generator/LP was rerun here.
