# Diluted shared-terminal raw K2 gap: Exact only

ClaimVersion: SCRATCH-UM-DILUTED-SHARED-TERMINAL-RAW-K2-GAP-v1.
Status: new author Exact; proof separate and not yet independently reviewed. No hardness, novelty certification, canonical-C2 gap, or stronger conditional-Hall/S3 gap is claimed. All operations concern scratch files only.

## 1. Explicit ordinary matrix

For every integer k>=2 set

    L=2k^2, M=1+60 L k^4=1+120k^6, T0=1+1/k, a=1/M.

There are M disjoint components. Component i has a machine U_i, L machines B_i,b (b in [L]), and k terminals Z_i,t (t in [k]). Different indices and different types denote physically distinct machines. There is one original selector job h, with time one at each U_i. For every i and j in [k], original job f_i,j has time 1/k at U_i and time one at every B_i,b. For every i,b and ell in [k], original job e_i,b,ell has time 1/k at B_i,b and time one at every Z_i,t. All unlisted endpoints are infinite. Every original job is indivisible and assigned exactly once.

Machine count: M(1+L+k). Job count: 1+Mk(1+L). Finite endpoint count:

    M + Mk(1+L) + MLk(1+k).

Processing times are binary rational. There is no external assignment, source promise, good configuration, or oracle in the input.

Claim A: the true ordinary makespan optimum is

    OPT(P_k)=2-floor(sqrt(k))/k.

## 2. Raw system being tested

Use every original finite endpoint indicator x_j,v. There is one common functional F on degree-at-most-four polynomials, F(1)=1, and a global M2 PSD on degree-at-most-two monomials. Impose the original-job quotient x^2=x and xx'=0 for distinct endpoints of the same job, multiplied by every monomial of degree at most two; impose sum_v x_j,v=1 multiplied by every monomial of degree at most three.

At each original machine supply a full CONFIG(T0) distribution agreeing with F in all first and same-machine second endpoint moments. Also impose every GLOBAL affine load localizer

    F[(T0-load_v) q^2] >= 0

for every original machine v and every affine q in all endpoint variables of the entire input. Its degree is at most three, within the common degree-four functional.

No export<=activation inequality, inactive-all-home restriction, exact active-tail count, or common global CONFIG law is required. The point below expressly uses inactive exports. This is the raw K2 contract, not the canonically normalized native C2 system.

Claim B: this raw system has an explicit rational feasible certificate at T0, with the following exact moment law and machine CONFIG distributions. Every degree-four moment, all local CONFIG lists, and all localizer matrices can be generated in deterministic time and total bit length polynomial in the explicitly expanded ordinary input length. This is generation of a specified certificate, not an SDP feasibility algorithm.

## 3. Full finite moment law

Select I uniformly from [M] and assign h to U_I. Conditional on I, independently draw component assignments as follows. Component I uses law H; each other component uses law Q. These are complete assignments of their original jobs.

H: choose uniformly an injection sigma:[k]->[L]. Assign each f_i,j to B_i,sigma(j). Assign every e_i,b,ell to its tiny home B_i,b. Thus the chosen U_i contains h and no f jobs; exactly k B machines contain one unit f job and their full tiny payload.

Q: use these three alternatives.

- With probability 1/2, assign every f and e job to its tiny home.
- With probability 1/4, choose (j,b) uniformly from [k]x[L]. Assign f_i,j to B_i,b and all other f jobs home. Choose uniformly a bijection pi:[k]->[k], and assign e_i,b,ell to Z_i,pi(ell) for every ell. Assign every other e job home.
- With probability 1/4, choose (b,ell,t) uniformly from [L]x[k]x[k]. Assign e_i,b,ell to Z_i,t, and every other f and e job home.

Define F(p)=E[p] under this finite rational law. All original jobs, including every unselected component's jobs, occur in every sample. The support may be exponentially large; the claim concerns the polynomial-size degree-four moment table, not enumeration of the support. The laws involve only partial injections/permutations on the at most four queried heads, and independence conditional on I.

## 4. Machine CONFIG distributions

At U_i, the actual row marginal of the moment law is already supported on legal configurations of load at most one: h alone with probability a; each configuration with exactly f_i,j omitted from the k home f jobs with probability (1-a)/(4k); and all k home f jobs with probability 3(1-a)/4.

At any B_i,b define

    p=ak/L, b0=(1-a)/(4L), c0=(1-a)/(4L).

Use the following five classes of configurations. A unit incoming label means one of the k original f_i,j endpoints at this B, chosen uniformly. Whenever a single home e job is included, choose its label uniformly and independently of the incoming label. Whenever one home e job is omitted, choose its label uniformly.

    one unit + one home e:        total mass k p;
    one unit + no home e:         total mass b0-(k-1)p;
    no unit + no home e:          total mass p;
    no unit + exactly k-1 home e: total mass c0-kp;
    no unit + all k home e:       total mass 1-b0-c0+(k-2)p.

All masses are nonnegative for the stated M, and sum to one. Every configuration has load at most T0. They match all original incoming-unit/home first and pair moments of F; the two laws need not match triples.

At a terminal Z_i,t, use the empty/singleton distribution from the actual moment law. Each of its Lk incoming original e endpoints has singleton probability

    (1-a)(k+1)/(4Lk^2),

and the remaining probability is empty. No two unit jobs share a terminal in a moment-law sample, so all its same-row pair moments are zero.

## 5. Global localizer and complexity scope

The certificate assertion includes the affine localizers for q with variables from arbitrarily many components and all selector endpoints. Their feasibility is not inferred from a fixed-dimension continuity claim. The explicit M above must suffice uniformly in the growing number of global contexts; a proof must handle conditional component means and variances and give a quantitative bound independent of M.

At the selected component's B row, actual moment-law load is two whenever that B is selected by the injection. Thus this is a true-optimum gap candidate, rather than an example whose actual optimum is one but whose moment law contains bad support. Two-event conditioning can detect the bad row: with A_i the selector endpoint and C_i,b the unit incoming occupancy, F[A_i C_i,b (T0-load_B)]<0. Such a stronger conditional inequality is outside the stated raw K2 contract. No claim about that stronger system is made.

Uniformly scaling every finite processing time by k/(k+1) gives a target-one raw K2 certificate, with true optimum

    (2-floor(sqrt(k))/k)/(1+1/k) -> 2.

The scaled large times are k/(k+1), and the scaled tiny times are 1/(k+1). This is a supplied relaxation gap family, not a polynomial hardness reduction or an actual YES/NO source theorem. Software status: no verifier or finite numerical audit is claimed in this Exact; the explicit laws and formulas constitute the proposed mathematical construction.
