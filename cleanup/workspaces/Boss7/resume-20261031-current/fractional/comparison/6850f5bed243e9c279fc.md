# Fractional rematching extension — research statement-only Exact v1

Date: 2026-10-18. Prepared by general_query_response_review after independent reconstruction and comparison with root's separately reconstructed statement. Scratch only; not a registered mature asset.

This file gives definitions and exact conclusions only. It contains no proof, matching construction strategy, derivation, or experiment. The fractional extension is an additional mathematical candidate, not a claim that the DLRV paper stated a log-CONFIG integrality-gap theorem. The conditional external-backend conclusions below are separate from the standalone matching statement.

## A. Standalone fractional-benchmark matching statement

### A1. Finite object and rational input

Let n>=1 be an integer. There is a finite item set U and an explicitly specified subset H of exactly n distinct items. Write B=U\H.

For each agent i in [n], v_i:2^U -> Q_{\ge0} is finite, monotone and subadditive, with v_i(empty)=0. These are semantic hypotheses on the valuations. The explicit application may represent them as normalized XOS clause tables. More generally, a value-query interface may be used, with all queried rational values returned in finite binary encoding. Running time below is charged for the actual input and the polynomially many queried rational values; no enumeration of 2^U is required.

Give nonnegative binary rationals V_i and a binary rational c>=1. Put A={i:V_i>0}. For each i outside A, require v_i(B)=0.

Give a finite explicit rational configuration list y=(y_{i,S}) with y_{i,S}>=0, such that
\[
\sum_{S\subseteq U}y_{i,S}=1\quad(i\in[n]),\qquad
\sum_{i,S:j\in S}y_{i,S}\le1\quad(j\in U).
\tag{A1}
\]
Only nonzero entries need be listed, and every entry y_{i,S}>0 must have v_i(S)>0. The value on each listed configuration may be supplied or obtained by a value query. Configurations are ordinary subsets of the original items, not independent coordinate labels.

### A2. Fractional residual welfare premise

Assume that every feasible fractional configuration family z=(z_{i,T}) for the agents in A on item set B satisfies
\[
\sum_{i\in A}\sum_{T\subseteq B}
 z_{i,T}\frac{v_i(T)}{V_i}\le c n,
\tag{A2}
\]
where feasibility means
\[
z_{i,T}\ge0,\quad
\sum_{T\subseteq B}z_{i,T}=1\ (i\in A),\quad
\sum_{i\in A,T:j\in T}z_{i,T}\le1\ (j\in B).
\]
This is a semantic bound for all fractional families, not just integral allocations. If A is empty it is vacuous. A stronger bound c|A| also suffices.

The theorem does not claim that its algorithm verifies this global premise or obtains the V_i. They are hypotheses of the matching interface. In a downstream application they must be supplied by an independently justified backend.

Define the positive benchmark
\[
\mathcal B(y)=
\exp\left(\frac1n\sum_{i,S}y_{i,S}\ln v_i(S)\right).
\tag{A3}
\]

### A3. Exact matching conclusion and finite-bit construction

There exists a bijection pi:[n] -> H satisfying
\[
\left(\prod_{i=1}^n
 [V_i+v_i(\{\pi(i)\})]\right)^{1/n}
\ge\frac{\mathcal B(y)}{c+1}.
\tag{A4}
\]
In particular every factor on the left is strictly positive.

Such a pi can be found deterministically in total bit-polynomial time, using only the finite rational numbers V_i and the n^2 singleton values on H, apart from any input/promise checks. One may compute a true maximum-product perfect matching with factors V_i+v_i({h}). This assertion does not require an exact representation of logarithms or of the generally irrational benchmark B(y).

The finite-bit statement includes zero singleton values and V_i=0: zero-factor matching edges may be excluded, and the conclusion asserts feasibility of a perfect matching using positive-factor edges. It also includes B empty, A empty, and repeated configuration subsets represented by different list entries.

An approximate version is also allowed: for each explicit rational epsilon>0, a deterministic algorithm may instead return pi satisfying
\[
\left(\prod_i[V_i+v_i(\{\pi(i)\})]\right)^{1/n}
\ge\frac{\mathcal B(y)}{(c+1)(1+\epsilon)},
\tag{A5}
\]
with total bit-polynomial complexity in the input and the precision parameter. No guarantee of exact comparison of arbitrary transcendental expressions is assumed.

## B. Conditional external-backend consequence

This section is a separate conditional contract. It is not asserted to be the literal theorem statement of any paper.

Assume a randomized backend for finite monotone subadditive valuations with positive singleton-matching feasibility has the following interfaces.

E1. It chooses a maximum-product positive singleton matching tau from the n agents to the full U and sets H=tau([n]), B=U\H. It obtains rational V_i, with V_i>0 exactly on agents with positive value on B, such that the full fractional residual premise (A2) holds, for some absolute constant c>=1. Obtaining V_i and a polynomial-support residual fractional solution must be justified externally.

E2. After the residual rounding and final rematching stages, it outputs a feasible actual allocation (S_i) with a positive absolute success probability p_0, satisfying, for every comparison matching pi:[n]->H,
\[
\left(\prod_i v_i(S_i)\right)^{1/n}
\ge\frac1{20000d^2}
 \left(\prod_i[V_i+v_i(\{\pi(i)\})]\right)^{1/n},
\tag{B1}
\]
where d>=1 is an absolute constant. It suffices that the same comparison guarantee holds for the best matching in (A4). No independent fractional configuration y is used as an integral allocation.

E3. All oracle calls, support computations, numerical approximations, and random sampling have polynomial total bit cost on the explicit finite-rational application, with a fixed constant slack allowed in the final factor.

If E1-E3 are valid and (A1)-(A2) hold for a finite positive benchmark y, the same backend has the conditional guarantee
\[
\left(\prod_i v_i(S_i)\right)^{1/n}
\ge\frac{\mathcal B(y)}
 {20000(c+1)d^2}
\tag{B2}
\]
with constant success probability, with an additional fixed numerical-slack factor if E3 requires it.

For the intended DLRV-type application, the candidate parameters are c=2 and d=5/2, giving the displayed factor 375000 before safety slack. Attribution must remain precise: the published DLRV main theorem is an approximation relative to integral NSW optimum; E1-E2 and their use with A are additional dependency checks, rather than a quotation of a published log-CONFIG theorem.

## C. Conditional normalized-XOS / unit-FSLP specialization

Let agents be explicit indexed normalized XOS menus:
\[
v_i(S)=\max_{s\in\mathcal S_i}\sum_{j\in S}p_{i,s,j},
\qquad p_{i,s,j}\ge0,\qquad\sum_{j\in U}p_{i,s,j}=1.
\]
All clause entries are binary rationals and all menus and items are explicit. Zeros and duplicate indexed clauses are allowed. Put P_{i,s}={j:p_{i,s,j}>0}.

Give a finite rational unit-FSLP certificate lambda with
\[
\sum_s\lambda_{i,s}=1,\quad \lambda_{i,s}\ge0,\quad
\sum_{i,s:j\in P_{i,s}}\lambda_{i,s}\le1.
\]
The corresponding finite benchmark y on the positive clause supports is asserted to have B(y)=1. The normalized utility satisfies 0<=v_i(S)<=1. The log-CONFIG LP with item capacities at most one has optimum value zero; the item-equality version has the same optimum for these monotone utilities.

Conditional on E1-E3, there is an absolute integer rho>1 and a randomized total-bit-polynomial actual allocation finder with constant success probability and NSW>=1/rho for this family. A sufficiently conservative fixed rho, such as 10^12 for the indicated constants and fixed numerical slack, may be used only after the backend interfaces are validated. This is not an unconditional quotation of DLRV Theorem 10.

For each positive integer K, every successful output with NSW>=1/rho has
\[
\#\{i:v_i(S_i)<\rho^{-K}\}< n/K.
\tag{C1}
\]
Hence for each fixed eta in (0,1), choosing K=ceil(1/eta) gives fewer than eta n agents below the rational threshold rho^{-K}. Maximizing-clause lookup for each actual S_i returns an original indexed state attaining its XOS value; no independent label assembly is permitted or needed.

This does not guarantee all groups have a constant utility. It therefore does not by itself bound the ordinary minimum V away from zero. It concerns a fixed-fraction robust-small-utility obstruction.

## D. Scope

A is a standalone fractional rematching statement with explicit hypotheses and an output matching. B-C are conditional consequences requiring exact external randomized backend interfaces. None of these statements may be attributed as a literal original-paper theorem without separately verifying the relevant source guarantee.

General XOS is not assumed submodular. A submodular-only NSW theorem does not supply E1-E3 for all explicit XOS menus. No source hardness, NP-versus-RP claim, software execution, global novelty, or mature asset registration is part of this statement-only file. A separate proof and independent review are required before use as an established new lemma.
