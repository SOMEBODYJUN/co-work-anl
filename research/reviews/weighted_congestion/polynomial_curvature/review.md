# 前缀阶跃模拟：三负载曲率的独立反向审查

Reviewer: delegated independent mathematical attack, 2026-10-14.

**Verdict: PASS for the precise local obstruction stated in proof.md.**
No counterexample or missing assumption was found in its stated domain.
This is a verification of a basic convexity tool and its application, with no
claim of novelty or new approximate-equilibrium threshold.

## Independence and reconstruction order

Before reading the candidate proof, I reconstructed the claim from its precise
statement and reported the following alternative route to the parent agent.
For q_k=a_k H^k/p(H), r=L/H, s=U/H, and
gamma=log(s)/log(1/r), the q_k form a probability distribution and

    p(L)/p(H)=E[r^K],
    p(U)/p(H)=E[(r^K)^(-gamma)].

Jensen's inequality for the strictly convex function z -> z^(-gamma) gives

    p(U)/p(H) >= (p(L)/p(H))^(-gamma) >= epsilon^(-gamma).

Also E[r^K]>=r^d gives the necessary degree bound. This reconstruction,
the three load witnesses, the m=2 counterexample below, and the sharp
adjacent-monomial optimization were sent before the frozen proof was read.
Only after being notified that proof.md was frozen did I read proof.md,
verify.py, and results.json and write this review.

## Items checked

1. **Source identity and strategies.** I independently opened
   https://arxiv.org/html/2002.07466v3 and checked Section 6, Theorem 5,
   especially the weights, prefix strategy sets, and satellite threshold.
   These agree with the construction used in proof.md.
2. **Actual loads.** On a_1 the load is

       1_{s_0=A} + (1/2)1_{s_1=B}
         + sum_{j=2}^m 2^(-j)1_{s_j=A},

   where A is the first listed strategy and B the second. Thus
   (A,A,A,...,A), (A,B,B,...,B), and (A,B,A,...,A) give L,H,U.
   Independent exact Fraction checks for m=3,...,12 passed before review.
3. **Normalization and signs.** Nonzero nonnegative coefficients imply
   p(x)>0 for x>0. Thus every logarithm and ratio is valid. The variance
   expression for F'' is correct and the ordered secant-slope inequality
   has the correct direction. Because p is nondecreasing, the rational
   consequence p(U)p(L)^r>=p(H)^(r+1) also follows without a leakage
   assumption.
4. **Uniform exponent.** For delta<=1/8, proof.md correctly proves
   gamma>=33/(128 delta)>1/(4 delta). Its estimates use lower bounds on
   the numerator and upper bounds on the positive denominator. My
   independent route gave the slightly stronger elementary estimate
   gamma>=11/(40 delta), but no strengthening is needed for the claim.
5. **Degree.** The coefficientwise bound
   p(H)<=(H/L)^d p(L) is correct. If d denotes an upper bound rather than
   the actual degree, the necessary inequality still holds. Constants
   cannot satisfy epsilon<1.
6. **Regression evidence.** I inspected the literal strategy encoding in
   verify.py and checked that the 728 coefficient vectors are exactly
   {0,1,2}^6 minus the zero vector. The exact comparisons test the stated
   consequences; the finite checks are correctly described as regression
   evidence rather than a universal proof.
7. **Scope.** The conclusion excludes a single nonnegative-coefficient
   polynomial with both small relative leakage and a bounded relative
   high plateau on these three attainable loads. It does not exclude
   other polynomial nonexistence constructions, other weight geometries,
   or a new deviation proof on this topology that uses the overshoot.

## Boundary attack and sharpness

The hypothesis m>=3 matters for the displayed exponent. At m=2 choose

    p(x)=x, epsilon=5/6,
    L=5/4, H=3/2, U=7/4.

Then p(L)=epsilon p(H), but

    p(U)=7/4 < 9/5=epsilon^(-1)p(H).

This is an exact rational counterexample to extending the asserted
2^(m-2) exponent to m=2; it is not a counterexample to the actual claim.

For epsilon=0 no admitted polynomial can meet the premise. At epsilon=1
the conclusion extends trivially by monotonicity. The excluded zero
polynomial would make the normalized expressions undefined. Negative
coefficients fall outside the argument's domain.

The sharper general exponent gamma=log(U/H)/log(H/L) is attained by
monomials whenever epsilon=(L/H)^k. It is therefore optimal as a single
power exponent valid for all epsilon. For a prescribed arbitrary epsilon,
the exact optimum is usually strictly stronger and is attained by two
adjacent monomials; see extension.md and extension_verify.py. These are
standard convex-envelope consequences, retained as a reusable tool and
not presented as a novelty result.


---
整理来源与当前文件用途见[逐文件登记](../../../weighted_congestion_frontier/FILES.md)。程序统一通过 `python3 tests/audits/weighted_congestion/replay.py --list` 选择；历史命令、输出摘要与源码哈希属于原冻结版本。
