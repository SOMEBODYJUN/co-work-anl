# Raw SH3 的共同 root 条件流：窄终端递归稀释的精确切除

2026-10-18. Scratch boundary for the subsequent strengthening of the diluted raw K2 gap. It does not change that gap's degree-four/affine-localizer claim. No independent review is asserted. The genuine-law assertion and its M3 extension below have proofs; they are not an original K2 assertion or a general approximation theorem.

## 1. Exact native scope

Every internal row v owns k_v>=1 distinct original home tokens, each with time 1/k_v at v and only time-one alternatives elsewhere. Thus its complete home budget is one. Let H_v be the sum of its home indicators, O_v the sum of all its original unit-export endpoints, and C_v the sum of all original unit arrivals at v, including selector endpoints. Original one-hot gives H_v+O_v=k_v and

    load_v=C_v+H_v/k_v,
    g_v=T-load_v=T-1-C_v+O_v/k_v.                 (1.1)

Fix 1<=T<2. Rows with only unit arrivals, such as terminals, have no home payload. Every unit row has complete CONFIG(T) first/pair agreement, so L(R_j R_j')=0 for any two different incoming original unit endpoints. No canonical export<=activity restriction, inactive-all-home rule, or ancestor variable is assumed. Two-tiny-home jobs, nonuniform home times within a row, and other unrelated processing-time patterns are outside this theorem.

## 2. Genuine-law theorem

Suppose L is expectation under one true complete original assignment law. Its same-unit-row pair zeros imply C_v<=1 almost surely. Suppose all global load localizers L(g_v q^2)>=0 hold for every polynomial q of degree at most two. For any original selector endpoint A and internal row v,

    L(A O_v)>=k_v(2-T)L(A C_v).                  (2.1)

For every unit-only terminal z,

    0<=L(A C_z)<=L(A).                           (2.2)

These are common conditional inequalities across every layer, not assertions that a specified event is a full source solution.

**Proof.** Use q=A R_j separately for each original incoming endpoint at v. These are degree-two polynomials in the original global variables. Since the law is Boolean, q^2=A R_j. Sum their localizers and use C_v^2=C_v:

    0<=L(A C_v g_v)
      =L(A C_v O_v)/k_v-(2-T)L(A C_v).          (2.3)

Since 0<=C_v<=1 and O_v>=0, L(A O_v)>=L(A C_v O_v). This proves (2.1). The terminal claim is the same pointwise unit capacity. No number of inactive exports can reverse this inequality: those exports are nonnegative terms in O_v.

## 3. Exact non-genuine M3 extension

The same theorem holds when L is not a true law, provided it is a common degree-at-most-six functional with M3 PSD, original Boolean/one-hot ideals through degree six, the stated unit-row pair zeros, and all global degree-two load localizers. The step L(A O_v(1-C_v))>=0 is paid by M3; it is not taken as a free RLT inequality.

For distinct incoming endpoints R_j,R_j', the degree-two vector R_j R_j' has norm squared L(R_j R_j')=0. M3 PSD makes it orthogonal to every polynomial of degree at most three. In particular C_v^2=C_v inside all expectations needed below.

For one original export endpoint x in O_v, set

    p=A x(1-C_v),  degree(p)<=3.

After Boolean reduction,

    L(p^2-p)=L(A x(C_v^2-C_v))=0.               (3.1)

Every summand on the right is an inner product of the null vector R_j R_j' with the degree-two polynomial A x. Thus

    L(A x(1-C_v))=L(p^2)>=0.                    (3.2)

Sum over the original export endpoints x. This is exactly the comparison needed after (2.3). Similarly the degree-two polynomial A(1-C_z) has squared norm L(A(1-C_z))>=0, proving the terminal bound. Also L(A C_z)>=0 follows from the norm of the degree-two polynomial A C_z. The load-localizer reduction q^2=A R_j uses the stipulated original ideals through degree six. This proves (2.1)-(2.2) for raw SH3 in this explicit M3 sense. A common M2 alone does not provide the degree-three norm (3.2).

## 4. Layered shared-terminal consequence and bit complexity

Suppose a physical component has internal layers 0,...,h-1 and N distinct unit-only terminals at layer h. Its original unit-export alternatives go only to the next layer within this component. Each layer i has common home-token count k_i. A selector endpoint A places the unit root in its unique layer-zero machine; original selector one-hot makes the other layer-zero selector endpoints vanish conditioned on A. For L(A)>0, repeated summation of (2.1), using the exact original-job identity

    sum_(w in next layer) C_w=sum_(v in layer) O_v,

gives

    product_(i=0)^(h-1) [k_i(2-T)] <= N.         (4.1)

Inactive-Q exports only add terms to the middle sums and cannot provide a negative correction. The same proof applies to the genuine law and the M3 functional. It does not require a path product, full ancestor history, or an independent source decoder.

For the original two-level diluted family at T=1+1/k, (4.1) requires (k-1)^2<=k. Hence for k>=3 it has no raw SH3 extension of the stated kind, although its raw K2 point exists. Replacing T by 1+s/k and the terminal count by Dk requires (k-s)^2<=Dk; for fixed s,D this still fails for all sufficiently large k. Recursive layer insertion must provide enough terminal width for the full conditional product, not merely lengthen the apparent bad event.

This is a finite algebraic certificate: it adds polynomially many original localizers and M3 square/null identities, then multiplies rational coefficients across h layers. If h grows with the explicit input, the coefficient bit length is O(h) times the bit lengths of T and k_i. No list of paths or exponentially large support is generated. A strict violation of (4.1), together with positive selector mass, rules out this relaxation point. If every possible selector component violates it, selector one-hot rules out the entire system. This statement does not say that every single rejected point implies OPT>T; only infeasibility of the universally necessary system gives that conclusion.

## 5. Smaller row-local obstruction at T=1+1/k

There is an even shorter genuine-law obstruction at that exact threshold. For any incoming original unit endpoint R_j and original home endpoint Y_l, q=R_j Y_l has degree two. When q=1, H_v>=1 and

    g_v=(1-H_v)/k<=0.

It is strictly negative when H_v>=2. Consequently its nonnegative localizer forces zero probability of every such bad event. Over all j,l, any row with a unit arrival has at most one retained home token almost surely; rows without a unit arrival have home load at most one. Thus the global law is supported on complete T schedules. This is independent of depth. The M3 product argument also pays these degree-two-event norms in a pseudo-functional, but the assertion of support is reserved for a genuine law.

At T=1+s/k with integer s>=1, a product of one incoming endpoint and s distinct retained-home endpoints is the analogous genuine-law separator of degree s+1. Increasing s can defeat this particular low-degree support argument, while (4.1) still applies. A candidate with enough root-conditioned fractional flow but conflicting shared integer ownership is not excluded by this note.

## 6. Fixed-d interpretation

More generally, with a common M_d, original ideals through degree 2d, unit-row pair zeros and global load localizers of degree at most d-1, the same proof works with any compatible literal cylinder E of degree at most d-2 replacing A. Use q=E R_j and the M_d norm of E x(1-C_v), of degree at most d. Boolean reduction again gives the required nonnegative conditional inactive-export term. If L(E)>0, the normalized original export marginals therefore satisfy the exact naive assignment-flow cover with demand k_v(2-T), unit packing, and nonnegative entries conditioned on E. This implication alone does not impose canonical export<=activation or prove an actual forest decoder.

The remaining main candidate must therefore hide a genuine shared-ownership obstruction after these low-degree conditioned fractional flows are already feasible. A path-length heuristic or a one-component terminal-count deficit does not meet that obligation.
