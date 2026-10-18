# 实际处理时间矩阵平方将二分之三NO精确变为YES

Frozen statement: 2026-10-18. Candidate only; no repository claim or novelty certification.

## Objects

The base ordinary unrelated-machine instance P has eight machines. In their fixed order they are

    S00,S01,S10,S11,R00,R01,R10,R11.

The two selector jobs A_g (g in F_2) have processing time 1 at S_g0 and S_g1 and infinity elsewhere. For each (g,l,a) in F_2^3 there is a different incidence job B_gla with processing time 1/2 at S_gl and time 1 at R_a,b, where b=l+g*a in F_2. All other entries are infinity. The job order is A_0,A_1, followed by B_000,B_001,B_010,B_011,B_100,B_101,B_110,B_111.

For t>=1, P^[t] is the actual processing-matrix Kronecker power: machines are all t-tuples of original machines; jobs are all t-tuples of original jobs; a tuple machine is eligible iff each coordinate machine is eligible for the corresponding coordinate job; its processing time is the product of all coordinate times. No mixed job type is discarded, and there are no extra consistency requirements.

## Exact candidate statement

1. OPT(P)=3/2.
2. P^[2] has 64 machines, 100 original tuple jobs, and 400 finite machine-job entries. It has a complete schedule with load exactly 1 at every one of its 64 machines. Consequently OPT(P^[2])=1.
3. For every integer k>=1, OPT(P^[2k])=1, using the ordinary tensor product of k copies of the square schedule. All jobs and machines of the indicated full powers remain present.
4. The unpruned assignment-LP optimum of P equals 1. More generally the unpruned assignment-LP optimum is exactly multiplicative under Kronecker products of nonnegative finite/infinite processing matrices, provided each job has an eligible machine. This is a separate elementary identity, not a claim about integral OPT.

Thus the universal implication

    OPT(P)>=3/2, assignment-LP(P)<=1
    => OPT(P^[t]) >= f_t(3/2) with f_2(3/2)>1

is false for this explicit product, even though the product preserves OPT<=1 YES schedules. This statement does not rule out a reduction-specific hard image, other products, substitution gadgets, extra physical consistency constraints, or near-2 hardness. No NP-hard source is encoded here.

## Frozen actual input and witness

`square_input.json` records the complete sparse 64x100 matrix in exact rational text, all tuple-machine identities, and all tuple-job identities. `square_certificate.json` records one destination for every original tuple job and every exact machine load. Its assignment was first found by MILP; its mathematical validity uses only eligibility and exact rational addition, not the MILP optimality status. `verify_certificate.py` reconstructs the base and square independently of the search program and verifies every entry, destination, and load.

`PROOF.md` is separate from this statement. No repository file has been modified.
