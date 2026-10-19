# 全矩阵平方的环式初态与十五件交换证明

This is an additional closed-form proof of the frozen EXACT_ONLY.md statement. It does not modify the original certificate. No MILP fact is used below.

## Related restricted assignment interpretation

Give every state machine speed 2, every resource machine speed 1, each selector job size 2, and every incidence job size 1. On its existing eligible endpoints, each processing time is exactly job size divided by machine speed. Total job size and total machine speed both equal 12. In the square, speeds are 4,2,1 and job sizes are 4,2,1. Total size and total speed both equal 144. A makespan-one square schedule is an exact packing of these capacities.

## A uniform formula for 100 starting destinations

Write A_g for a selector and B_gla for an incidence, with b=l+ga, all bits in F_2. For two incidence jobs write the second one B_hkc with d=k+hc. Use the following complete initial assignment sigma_0:

| Tuple job | Initial destination |
| --- | --- |
| (A_g,A_h) | (S_gh,S_hg) |
| (A_g,B_hkc) | (S_gh,R_cd) |
| (B_gla,A_h) | (R_ab,S_hg) |
| (B_gla,B_hkc), l=h and k=g | (R_ab,R_cd) |
| (B_gla,B_hkc), otherwise | (S_gl,S_hk) |

Every entry is an actual eligible endpoint of the full matrix. All 4+16+16+64 original tuple jobs are included.

Each selected state-state machine (S_gh,S_hg) contains its one unit selector-selector job; its four incidence-incidence jobs were moved to resources. Each of the other twelve state-state machines contains four jobs of size 1/4. The selector-incidence mapping bijects its sixteen jobs onto the sixteen state-resource machines, with time 1 each. The incidence-selector mapping similarly fills all sixteen resource-state machines.

For resource-resource machines, fixing (a,c), the selected incidence-incidence mapping is

    (g,h) -> (b,d)=(h+a*g, g+c*h).

Its determinant is 1+a*c. Unless a=c=1 it is invertible, so every such resource-resource machine receives exactly one unit job. For a=c=1 its image is b=d, each image point has two preimages, and the two off-diagonal targets are empty. Consequently every one of the 64 initial machine loads is 1 except

    (R10,R10), (R11,R11): load 2;
    (R10,R11), (R11,R10): load 0.

Thus the whole product defect has become two units on the diagonal of one 2x2 resource block.

## Fifteen explicit reassignments repair that defect

Use the frozen machine indices 0..7 and job indices 0..9. Replace the destination of exactly the following tuple jobs. All other destinations remain sigma_0.

| Tuple job | Old destination | New destination |
| --- | --- | --- |
| (0,7) | (1,7) | (0,2) |
| (2,1) | (4,2) | (0,3) |
| (2,6) | (0,2) | (4,2) |
| (2,7) | (0,2) | (4,2) |
| (2,8) | (0,3) | (4,3) |
| (3,9) | (0,3) | (6,3) |
| (4,7) | (5,7) | (1,7) |
| (5,7) | (7,7) | (1,7) |
| (6,1) | (4,3) | (2,3) |
| (6,8) | (2,3) | (4,3) |
| (7,9) | (2,3) | (7,6) |
| (8,7) | (3,2) | (5,7) |
| (9,1) | (6,3) | (3,2) |
| (9,7) | (3,2) | (6,7) |
| (9,9) | (6,6) | (6,3) |

Every new destination is eligible by the explicit base endpoint formulas. At the affected machines, the processing load removed and added is:

| Machine pair(s) | Removed | Added |
| --- | --- | --- |
| (0,2), (0,3), (2,3), (3,2) | 1/2 each | 1/2 each |
| (1,7), (4,2), (4,3), (5,7), (6,3) | 1 each | 1 each |
| (6,6), (7,7) | 1 each | 0 |
| (6,7), (7,6) | 0 | 1 each |

This table follows just by using 1/4 for incidence-incidence at state-state, 1/2 for incidence-incidence at mixed machines or selector-incidence at state-state, and 1 for their unit destinations. Hence every intermediate machine has zero net change and the two units move from the overloaded diagonal to the empty off-diagonal. The final load is exactly one on all 64 machines.

The argument supplies a fixed formula plus a fixed 15-entry replacement table, rather than relying on a 100-entry opaque optimizer output. `verify_structural_schedule.py` reconstructs every job, both assignments, every processing time and the removed/added totals from these formulas using Fraction. It imports neither the search code nor the old witness. The original frozen witness is an independent complete schedule of the same full matrix.

## Why mixed jobs matter

The old bare Cartesian-menu product has only one selected tuple state plus its incidence layer, and its best value is 5/4 at t=2. The actual matrix product also creates selector-incidence and incidence-selector jobs, and the state-resource/resource-state machines on which they can run. The exact exchange above uses those jobs and machines to route the two missing units. Discarding these mixed tuple types would change the product being studied.

The construction extends to every even actual power by tensoring the repaired square schedule. It does not provide a near-two source or establish any claim about odd powers, arbitrary seeds, or reduction-specific hard images. Its purpose is to close the naive universal actual-Kronecker amplification contract with a complete genuine NO-to-YES counterexample.
