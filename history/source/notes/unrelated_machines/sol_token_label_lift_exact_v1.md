# 同菜单标签提升的精确分层合同：M1 正面与 M2 反例

ClaimVersion: SCRATCH-TOKEN-LABEL-M1-POSITIVE-M2-NO-CP-v1.

Status: statement only, with no proof or Schur derivation. A separate author proof and a self-contained exact Fraction audit are supplied separately. No independent read-after review is claimed. This is an abstract common-moment/assignment-matrix claim, not a native scheduling integrality gap, a general scheduling algorithm, or a claim about Bamas's witness. The signed functional used below is not called a true conditional distribution.

## General formal lift and its M1 guarantee

Start with finitely many groups g and any untouched Boolean context variables. Group g has an integer k_g>=1, an integer 0<=r_g<=k_g, h_g=k_g-r_g, one Boolean activity A_g and finitely many Boolean anonymous head occupancies X_g,w. One common functional L is defined through degree four, with L(1)=1 and global M2 PSD on degree-at-most-two monomials. Impose every variable's Boolean ideal through total degree four, and impose

    X_g,w A_g = X_g,w,
    sum_w X_g,w = r_g A_g,

multiplied by every monomial keeping total degree at most four. All variables and all groups share this functional. These are exact hypotheses for this statement; no independent row projections are substituted for them.

Introduce k_g original token labels a at group g, each with a home variable t_g,a and a head variable x_g,a,w for every head w. A monomial is first reduced Booleanly. A token asked to use two different endpoints is incompatible and has lifted moment zero. Two different tokens asked to use the same anonymous head also give zero. Otherwise, for t>=1 specified different head labels/heads and s further different home labels at one group, replace that group's factor by

    (h_g)_s/(k_g)_{s+t} times product_w X_g,w.

For s>=1 home-only requests replace it by

    1 - [1-(h_g)_s/(k_g)_s] A_g.

An empty group factor is one. Here (a)_j is the falling factorial; every nonzero request involves s+t<=k_g, so a denominator is never zero. Multiply these replacements for different groups and the unchanged context variables, then apply L. The resulting linear functional L' is specified on every monomial of total degree at most four and does not raise degree.

(A) Under the stated hypotheses the M1 Gram matrix of L', indexed by the constant and all single original labelled/context variables, is PSD. This includes inactive and active home mixing, any finite collection of groups, k_g=1, r_g=0, and r_g=k_g. It is not a claim that L' has PSD M2.

For k=k_g>=2, A=A_g, X=X_g and h=h_g, its nontrivial first/second coefficients are exactly:

    L' x_a,w = L X_w/k;
    L' t_a = 1-r L A/k;
    L' x_a,w x_b,v = L X_w X_v/[k(k-1)]    (a!=b,w!=v);
    L' x_a,w x_b,w = 0                    (a!=b);
    L' x_a,w x_a,v = 0                    (w!=v);
    L' t_a x_a,w = 0;
    L' t_a x_b,w = h L X_w/[k(k-1)]       (a!=b);
    L' t_a t_b = 1-L A+h(h-1)L A/[k(k-1)] (a!=b).

Every diagonal equals its first moment. For k=1 the prescription is the linear substitution t=1-rA and x_w=X_w. The M1 assertion concerns exactly the displayed moment hypotheses, not a polynomial-support configuration decomposition algorithm or an exact SDP finder.

## A complete rational degree-four counterexample

Let the aggregate variables be Boolean X_1,...,X_10,Y, with sum_i X_i=4. Let nu be the genuine uniform law on all 210 four-subsets of [10]. Let beta be the signed weights on those same four-subsets: 1/8 per subset lying wholly inside {1,...,5} or wholly inside {6,...,10}; -1/400 per subset with two elements in each half; and zero on other subsets. The signed weights sum to one. Set delta=1/100.

Define L on all degree-at-most-four Boolean-reduced monomials by

    L f(X) = E_nu f(X),
    L(Y f(X)) = delta E_beta f(X)  (degree f<=3).

Extend linearly, and reduce powers of Y Booleanly. This completely specifies the functional, with no unknown oracle or moments.

(B) This functional has PSD global M2, of rank55 on the 67 distinct Boolean monomials of degree at most two. It satisfies the Boolean ideal and sum X=4 multiplied through degree four. Its pure-X first/same-row-second moments are realized by the full abstract row law containing all four-subsets uniformly. Its Y first/same-row-second moments are realized by Bernoulli(delta). These are the only two abstract row-configuration distributions asserted: exact-cardinality-four for X and {0,1} for Y. They do not assert a joint true law of X and Y or full original scheduling CONFIG feasibility.

Apply the formal lift with one group k=r=4, h=0, fixed A=1, ten heads X_i, and untouched Y. Put s_i=1 for i<=5 and -1 otherwise. Then

    Q=Y sum_i s_i (x_1,i-x_2,i)

is a degree-two original-variable polynomial and L'(Q^2)=-1/150. Thus the fully specified degree-four formal lift is not PSD.

(C) In fact there is no degree-four original-token extension preserving this whole aggregate functional: introduce a 4-by-10 Boolean assignment matrix x_a,i with each original token's one-hot equation sum_i x_a,i=1 through degree four, retain Boolean Y, require every head's full row configuration to be empty or one original token with matching first/second moments, and impose global M2 PSD. An extension must preserve all aggregate moments through degree four under X_i=sum_a x_a,i. No such extension exists. This is stronger than failure of one proposed kernel, but it concerns this given aggregate point rather than existence of some other point.

(D) One necessary aggregate PSD block for such an original extension, for a group of k labels and untouched Boolean Y, is

    [ k 1_{i=j} L(Y X_i) - L(Y X_i X_j) ]_(i,j) >=PSD 0.

For the point in (B) its half-sign eigenvalue is -2delta/5. Global aggregate M2 and the two stated abstract configuration laws therefore do not imply this original-label contrast condition. It is not claimed that this one extra block suffices for a complete M2 compression.

The coefficients, 210 signed weights, 67-by-67 rational Gram, negative quadratic norm and all finite checks have fixed finite rational encodings. The audit performs direct Fraction PSD elimination and moment checks; it does not use numerical feasibility, an unknown target or a precision oracle. Abstract full-row laws in (B) are explicitly enumerated finite laws. No asymptotic native-family conclusion is part of this ClaimVersion.
