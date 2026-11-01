# 集合包含原矩的 raw SH3 入口容量切：精确合同

ClaimVersion: SCRATCH-UM-INCLUSION-ENTRY-SH3-CUT-v1. 2026-10-18. Statement only; author proof and finite binomial arithmetic are separate. No independent review is asserted. This is a necessary-capacity certificate for an explicit family, not a general unrelated-machines approximation, computational hardness, or an assertion that the original paper's hierarchy theorem is false.

## 1. Complete original input

Let q be a positive multiple of four and m an integer with m>=100q, and write

    N=binom(m,q), C=binom(m-q,q), K=binom(2q,q), G=binom(m,2q)=NC/K.

Choose positive integers s1,s2 for which

    d1=floor(C/(K s1))>=1, d2=floor(K/s2)>=1.

There are separate physical machines U_S for every q-subset S of [m], B_W for every 2q-subset W, and Z_R for every q-subset R. They number 2N+G. All original jobs are independent, indivisible, and have binary rational processing times:

- One selector h has time one at every U_S.
- Each U_S owns d1 distinct jobs f_S,j, each with time 1/d1 at U_S and time one at every B_W with S subset W.
- Each B_W owns d2 distinct jobs e_W,l, each with time 1/d2 at B_W and time one at every Z_R with R subset W.
- Every other processing time is infinity. There are no other jobs or preloads.

All N d1+G d2+1 original jobs must be assigned. There are N+N d1(1+C)+G d2(1+K) finite entries. In particular d1,d2 are numbers of explicitly present original jobs, not binary demands with a free expansion.

## 2. Specified raw SH3 necessary system

For rational 1<=T<2, take one common degree-at-most-six functional L on the original finite assignment endpoints, with L(1)=1, original Boolean and job-one-hot ideals through degree six, M3 positive semidefinite, and

    L((T-load_v) p^2)>=0

for every physical machine v and every real polynomial p of degree at most two. Every row's first and same-row second moments must agree with a distribution over its complete legal CONFIG(T) subsets. No inactive-export restriction, canonical export<=activity cut, ancestor variable, or extension of a supplied lower-order point is assumed.

Every complete actual T-schedule gives a feasible Dirac functional for this system. General exact SDP feasibility is not assumed to have a polynomial-bit algorithm.

## 3. Finite rational cut and algorithm

Put delta=2-T and

    H=sum_(j=q/4)^q binom(q,j) binom(m-q,q-j),
    M=sum_(j=0)^(q/4-1) binom(q,j)^2.

For every U_S whose selector endpoint A_S has L(A_S)>0, the specified common system necessarily satisfies

    delta d1 (delta d2-M) <= H.                 (3.1)

If the strict reverse inequality holds, every selector endpoint has zero mass, contradicting its original one-hot identity. Hence the specified raw SH3 system is infeasible and the original input satisfies OPT>T.

An exact algorithm checks the promised explicit input and computes the displayed integers and rational inequality. It returns FAIL when the strict reverse inequality holds and UNKNOWN otherwise. Its arithmetic and verification time are polynomial in the total bit length of the explicit original matrix and T. FAIL is sound even without finding or optimizing any moment point. UNKNOWN does not certify the existence of a schedule or a hierarchy point. No source solution is an input.

The same numerical inequality is necessary for a complete actual schedule at T. The original input has CONFIG(1) feasible and CONFIG optimum exactly one. A complete assignment of all original jobs with peak

    max(1,2-1/d1,2-1/d2)

is obtained by choosing one selector U_S, sending one of its original f jobs to one B_W containing S, sending one original e job there to one Z_R contained in W, and keeping every other f/e job at its own original home.

## 4. Quantified family and boundaries

For any fixed real a,b>=0 and fixed delta in (0,1], uniformly over positive integers s1<=q^a and s2<=q^b, all sufficiently large multiples q of four have d1,d2>=1 and violate (3.1) at T=2-delta. Thus this explicit family has actual OPT tending to two, CONFIG optimum one, and the specified raw SH3 necessary system already has no point at any fixed T<2. These are different statements: this family is not a raw SH3 integrality-gap example.

Useful finite bounds, including floor payment, are

    H/C < (8/49)^(q/4),
    M/K <= (q+1)(2q+1)(256/729)^(q/4),
    K/C <= (4/99)^q,
    K >= 4^q/(2q+1).

These yield the quantified conclusion without assigning free exact values to noninteger demands. The restriction q/m<=1/100 is part of this input family. No particular constant is attributed to the source paper's unspecified sufficiently-small rho, nor asserted to satisfy every estimate in that paper. Fixed polylogarithmic scaling factors are covered only when an explicit bound by fixed powers of q has been verified. At any fixed rho=q/m in (0,1/100], q and the logarithm of the explicit inclusion graph's size are within constant factors.

An external native source layer can be attached without changing this local cut, provided its only interaction with U/B/Z is additional original unit arrivals at U, the U/B home jobs and their menus remain as stated, and some original unit endpoint into U is forced to have positive mass. Such an attachment requires its own proof of that last premise and complete accounting of its original jobs. This statement does not supply it for an arbitrary reduction.
