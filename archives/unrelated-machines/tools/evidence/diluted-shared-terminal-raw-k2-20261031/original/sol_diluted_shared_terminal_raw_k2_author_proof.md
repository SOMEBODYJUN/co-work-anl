# Author proof: diluted shared-terminal raw K2 gap

This proves the exact statement `sol_diluted_shared_terminal_raw_k2_exact_only.md`, SHA256 `25888ec48d8000769bcf5d8d2c4ab9cf29825e9084d1f5bb888de6be7c44210b`. No reviewer has yet received this proof. All objects below are the original jobs and physical machines in that Exact. This is a raw relaxation gap, not computational hardness or a canonical-C2/S3 gap.

## 1. True optimum and complete schedules

Write s=floor(sqrt(k)). An actual schedule of target T<2 places h at some U_i. Each original f job not at U_i is a unit at one of that component's B machines. At most floor(k(T-1)) f jobs can remain at U_i, so at least

    r=k-floor(k(T-1))

f jobs are exported. They occupy distinct B machines because two unit jobs cannot share a row at T<2. Each such B has at most floor(k(T-1)) of its k original e jobs at home, so exports at least r unit jobs to the component's k terminals. Unit capacity at those original terminal rows gives r^2<=k. Thus r<=s, which implies T>=2-s/k. A schedule with T>=2 already satisfies this bound.

Conversely choose any component i, assign h there, and export exactly s f jobs to s distinct B machines. At each selected B export exactly s of its e jobs, using s^2 distinct terminals across those B's; this is possible because s^2<=k. Every other original f and e job, including all jobs in all unselected components, is assigned to its tiny home. The selected U and B rows each have load 1+(k-s)/k=2-s/k. Every other tiny-home row has load at most one, and every terminal has load at most one. This is a complete schedule, and proves the stated exact optimum.

## 2. Global moments and full machine configurations

The Exact's finite law assigns every original job exactly once in every sample. Its expectation therefore satisfies all Boolean and original-job one-hot equations through degree four (indeed through every degree). Its global M2 is PSD because F(q^2)=E[q^2]>=0 for every polynomial q of degree at most two. These statements do not require any global schedule of target T0 in its support.

Conditional on the selector I, component random variables are independent. Selected law H makes all k f jobs unit exports to distinct B's and keeps all e jobs home. Unselected law Q has actual load at most one on every row: in its f-export alternative the selected B has its unit f job and no e jobs, and its k e jobs occupy different terminals; in the single-e-export alternative only one terminal is used. Under H, U has load one, terminal loads are zero, and a B has load two if selected by the injection and one otherwise. Thus only B rows need a separate CONFIG and localizer argument.

The U and terminal CONFIG lists in the Exact are their actual legal row marginals. At a fixed B, write R_j for its original incoming endpoint f_j and Y_ell for its original home e endpoint. Let C=sum_j R_j. With p=ak/L and b0=c0=(1-a)/(4L), its moment-law row marginal has these types:

    unit + k home e:       p;
    unit + no home e:      b0;
    no unit + k-1 home e:  c0;
    no unit + k home e:    1-p-b0-c0.

The incoming unit label is uniform among k possibilities, and in the third type the omitted e label is uniform. Hence its full first and distinct-pair moments are

    F(R_j)=(p+b0)/k,
    F(Y_ell)=1-b0-c0/k,
    F(R_j R_j')=0                    (j!=j'),
    F(R_j Y_ell)=p/k,
    F(Y_ell Y_ell')=1-b0-2c0/k       (ell!=ell').            (2.1)

Diagonals equal first moments. The Exact's five-class legal CONFIG distribution has exactly (2.1): its unit+one-home class has total mass kp and uniform independent labels, so contributes p/k to each mixed pair; its other unit class contributes no mixed pairs. Its two nonempty inactive classes supply the stated home first and pair moments. Direct substitution yields each formula in (2.1).

For nonnegativity, b0-(k-1)p and c0-kp have, over denominator 4ML, numerators M-1-4k(k-1) and M-1-4k^2. Both are nonnegative since M-1=60Lk^4. The last mass is at least 1-b0-c0>0 because k>=2. All masses sum to one. Active configurations have at most one home e in addition to one unit, so load at most 1+1/k=T0; inactive configurations have load at most one. This verifies every original row's full CONFIG first and same-row pair contract without matching higher moments between the local CONFIG laws and the global moment law.

## 3. A quantitative one-component bound

All that remains is to prove every GLOBAL affine load localizer. Put tau=1/k. Fix a B row in component i and let g=T0-load_B. Under Q, every row has load at most one, so g>=tau pointwise. Under H,

    g=tau-1{the injection selects this B},
    E_H[g]=tau-k/L=1/(2k)=mu>0,
    |g|<=1.                                               (3.1)

Use nonhome endpoint variables F_jb for the f jobs and G_b,ell,t for the e jobs of one component. Original home variables can be eliminated linearly by their original-job one-hot identities. Thus a general affine expression in that component is

    q=beta + sum_(j,b) c_jb F_jb + sum_(b,ell,t) d_b,ell,t G_b,ell,t.

Write ||c||^2=sum_(j,b)c_jb^2. The following two inequalities hold uniformly in beta and d:

    E_Q[q^2] >= ||c||^2/(30Lk^3),                         (3.2)
    E_H[g q^2] >= -2||c||^2.                              (3.3)

Here in (3.3) the constant beta is arbitrary and can differ from the constant in (3.2). These are quantitative inequalities for the fixed component laws, independent of M and the number of global variables.

To prove (3.2), let q0=beta be q in the all-home Q state; let qN_b,ell,t=beta+d_b,ell,t be q in a single-e-export Q state; and let

    qF_jb,pi=beta+c_jb+sum_ell d_b,ell,pi(ell)

be q in a single-f-export Q state with permutation pi. For each j,b,pi,

    c_jb=qF_jb,pi-sum_ell qN_b,ell,pi(ell)+(k-1)q0.

The square of a sum of three terms is at most three times their squared norms, and (sum_ell qN)^2<=k sum_ell qN^2. Average over pi and sum over j,b. Since each pi(ell) is uniform and there are k choices of j, this gives

    ||c||^2 <= 3 sum_(j,b) E_pi[qF_jb,pi^2]
               +3k sum_(b,ell,t) qN_b,ell,t^2
               +3kL(k-1)^2 q0^2.

The three Q alternatives show respectively that the first sum is at most 4kL E_Q[q^2], the noise sum is at most 4Lk^2 E_Q[q^2], and q0^2<=2E_Q[q^2]. Consequently

    ||c||^2 <= (12kL+12Lk^3+6kL(k-1)^2)E_Q[q^2]
             <=30Lk^3 E_Q[q^2].

This proves (3.2) with no rank or determinant assumption.

For (3.3), all G variables vanish under H. Set S=sum_j c_j,sigma(j). Then, without needing independence of the injected labels,

    E_H[S^2] <= k E_H[sum_j c_j,sigma(j)^2]
              =(k/L)||c||^2.

Using (3.1) and completing the square in the arbitrary constant beta,

    E_H[g(beta+S)^2]
      >= E_H[g S^2]-(E_H[g S])^2/mu
      >= -(1+1/mu)E_H[S^2]
      >= -(1+2k)(k/L)||c||^2
      >= -2||c||^2.

The middle inequality uses |g|<=1 and Cauchy-Schwarz. This proves (3.3).

## 4. Every global affine context, with no dimension factor

Let q be an arbitrary affine polynomial in every endpoint of the entire original input. Rewrite each component's home variables as one minus its nonhome endpoints. The selector's endpoints are A_h=1{I=h}. Therefore q can be written as a constant, a selector-dependent constant, and a sum of affine component expressions. Conditional on I=h, all component random choices are independent.

Continue to fix a B row in component i. Center every other component expression by its conditional mean given I=h. The resulting centered random variables have conditional mean zero, are independent of each other and of component i, and their conditional variances are nonnegative. Their means, including those of a selected other component, are absorbed into a number beta_h. Because the original selector is one-hot, these numbers are allowed to depend arbitrarily on h. If q_i denotes the part in component i with fixed coefficient arrays c,d, then

    E[g q^2 | I=h]
      = E[g(beta_h+q_i)^2 | I=h]
        + E[g | I=h] sum_(j!=i) Var(q_j | I=h).             (4.1)

This is an equality by conditional independence. Both possible means E[g|I=h] are positive: they are mu for h=i, and at least tau for h!=i. The variance term in (4.1) can therefore be discarded in a lower bound. This step introduces no factor depending on M or the number of variables.

For h!=i, component i has law Q, with g>=1/k. Applying (3.2), uniformly in beta_h, gives

    E_Q[g(beta_h+q_i)^2] >= ||c||^2/(30Lk^4).

For h=i, (3.3) gives a lower bound -2||c||^2, also uniformly in beta_i. Averaging over the selector yields

    F[g q^2] >= ((1-a)/(30Lk^4)-2a)||c||^2=0,

because a=1/M and M-1=60Lk^4. This proves the B row's localizer for every global affine q, even when q involves arbitrarily many other components and all selector endpoints. The argument also covers c=0 directly.

At U rows and terminal rows, every sample of the global law has load at most one, so T0-load>=1/k pointwise. Their global affine localizers hold immediately. Every original machine is accounted for.

## 5. Finite size, rational generation, and exact limitations

There are polynomially many original jobs and finite endpoints in k, with the counts in the Exact; L and M are explicit polynomials in k. For every monomial of degree at most four, expand home indicators using the one-hot affine identities if necessary. This expands into at most a fourth power of the finite-endpoint count. Repeated endpoint factors reduce Booleanly; incompatible endpoints of one job give zero.

For a nonhome-head monomial, condition on the selector I. Components factor. Under H, any e head gives zero; compatible distinct f-job heads to distinct B's have probability 1/(L)_r, with r<=4, and incompatible heads have probability zero. Under Q, at most one distinct f head can occur. If one occurs, only its selected B's e heads can occur, and their probability is 1/(4kL) times the corresponding partial-permutation probability 1/(k)_s, s<=4. With no f head, the f-export alternative contributes 1/(4L) times 1/(k)_s if all e heads use one B and form a partial bijection; the single-e-export alternative contributes 1/(4Lk^2) only to one distinct e head. The empty monomial has probability one. These rules include the zero cases when r>k or s>k. Selector endpoints either fix I, with weight 1/M, or are absent and require a sum over the M choices.

These formulas evaluate every degree-four moment using polynomially many rational operations in the expanded input. All relevant falling-factorial orders are at most four, with logarithmic bit lengths in k,L; the sums and products and selector weight have polynomial bit lengths. Even the unreduced finite laws have rational probabilities whose bit lengths are polynomial in k. The number of degree-at-most-four moment entries and all machine affine localizer entries is polynomial in the finite-endpoint count. No exponential support enumeration is needed.

Every U CONFIG has at most k+2 configurations. Every B CONFIG has at most k^2+2k+2 configurations after expanding the stated uniform labels. Every terminal CONFIG has Lk singleton alternatives plus empty. All masses are the explicit rational formulas above and can be generated in polynomial time and total bit length. The global M2 and localizers are certified analytically by the finite law and Sections 3-4; no exact SDP optimization procedure or floating numerical test is part of the proof.

Scaling all processing times by k/(k+1) preserves the moment functional and CONFIG lists, and multiplies each load-localizer polynomial by the positive factor k/(k+1). It produces a target-one raw certificate with actual optimum approaching two.

Finally this point fails the stronger two-event conditional capacity cut. With A_i the selector endpoint and C_i,b the unit occupancy of a B row, the selected law has load two whenever A_i C_i,b=1, so

    F[A_i C_i,b(T0-load_B)] = a(k/L)(T0-2)<0.

That inequality is outside the stipulated affine-q PSD contract. The point also uses exports in inactive components and is not asserted to satisfy canonical export<=activation restrictions. These limitations are essential and do not detract from the stated raw full-CONFIG + common M2 + global affine-load-localizer gap.
