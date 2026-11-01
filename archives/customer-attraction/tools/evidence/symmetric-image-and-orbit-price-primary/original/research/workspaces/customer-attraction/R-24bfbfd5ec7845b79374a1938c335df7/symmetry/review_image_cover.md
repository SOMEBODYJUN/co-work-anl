# Independent review: two-block image cover

Reviewer: internal researcher f_adversarial, 2026-10-21. Analytical reconstruction from the statement, without using an SPE proof or finite testing. Verdict: the image-cover theorem is valid, including the strengthened support-size scope below. It is a structural theorem; general Q-CAG-HALF remains OPEN.

## Exact statement

Let the finite common menu consist of two disjoint blocks X and Y, each containing k labels, k>=1. Suppose the multiset of unit-customer incidence types is invariant under every permutation within X, every permutation within Y, and a swap of the two blocks. Theme labels are the actual valid menu sets; this hypothesis does not add duplicate legal sets to the input model.

For a label set D, write F(D) for the number of customers covered by at least one label in D. Let an arbitrary m-provider terminal profile have support A, with d=|A| distinct labels and welfare W=F(A). No equilibrium assumption or restriction on the order is imposed.

Then

    OPT_d <= 2W.                                      (I)

More generally, whenever

    d >= min(k,m),                                    (H)

one has

    OPT_m <= 2W.                                      (II)

Thus every profile using m distinct labels satisfies (II). Repetition is also allowed when m>k and at least k distinct labels appear. There is no need to restrict m<=2k in the strengthened statement; only d<=2k is automatic.

## Independent proof

Incidence invariance gives F(gD)=F(D) for every allowed label permutation g. One direct verification writes

    F(D) = sum_B r_B 1_(B intersects D),

where r_B is the nonnegative integer number of unit customers of incidence type B, including B=empty if present. Reindexing B under g and using r_(gB)=r_B proves the invariance. No customer weight or provider weight is introduced.

Write a=|A intersect X| and b=|A intersect Y|, so a+b=d. Set

    q=min(k,d).

There is an allowed permutation g, obtained by swapping the blocks and then independently permuting within them, such that U=A union gA has exactly q labels in each block. Indeed, in X the sets A and gA must have sizes a and b. Choose their intersection to have size max(0,a+b-k), which is feasible because a,b<=k. Their union then has size min(k,a+b)=q. The same construction independently applies in Y with the sizes reversed. The two within-block permutations can realize these choices simultaneously.

For any comparison support T whose number of labels in each block is at most q, choose a within-block permutation h such that T is contained in hU. Such an h exists because hU may be any q-element subset of each block, independently. Monotonicity, invariance, and coverage subadditivity now give

    F(T) <= F(hU)=F(U)
         <= F(A)+F(gA)=2F(A)=2W.

A support of at most d labels has at most min(k,d)=q labels in either block. Applying the preceding inequality to an optimizer proves (I). An optimizer using at most m labels has at most min(k,m) labels in either block; (H) implies min(k,m)<=q and proves (II). Repeated labels in an optimal m-tuple do not affect its support or coverage.

## Boundary checks and the necessary distinction

* If d>=k, then q=k and U is the whole menu. Thus 2W bounds the coverage of all menu sets at once, including the case m>k.
* If d<k, the conclusion is still OPT_d<=2W. Raising the comparison budget from d to an arbitrary larger m is not justified without another condition.
* Distinctness of the m actual choices cannot simply be dropped while retaining arbitrary m. For k>=2 take 2k pairwise disjoint singleton themes, with one customer per theme. This incidence multiset has the required symmetry. Three providers all selecting one singleton have W=1 but OPT_3=3>2W. This is a profile counterexample, not an SPE counterexample.
* Uncovered customers are the incidence type B=empty, contribute zero to every F, and do not affect the proof.
* Empty themes and zero-customer instances cause no division or exceptional argument. Under the exact requirement that all 2k menu sets are distinct, transitivity forces every theme to be empty if one is empty; for k>=1 this makes the premise infeasible. The proof itself uses only valid incidence invariance and nonnegative coverage, so it makes no hidden nonemptiness assumption on a theme.
* The factor 2 is sharp for arbitrary profiles: take one equally sized private customer block attached to every X theme and another attached to every Y theme. Choosing distinct labels only from X covers one block, while a two-label comparison using X and Y covers both. For k>=2 the literal themes in that basic example have duplicates within a block; adding one private unit customer per label makes all themes distinct and gives a ratio approaching 2 as the two common customer blocks grow. This is a structural-profile sharpness statement and says nothing about SPE sharpness.

The last sharpness construction uses the invariant incidence types X, Y (equal multiplicity M), and each singleton label (multiplicity 1). For m<=k distinct actual X labels, W=M+m; an optimal m-label profile meeting both blocks covers 2M+m, so the ratio tends to 2. For m=1 the conclusion is exact rather than sharp at 2, since theme transitivity gives OPT_1=W.
