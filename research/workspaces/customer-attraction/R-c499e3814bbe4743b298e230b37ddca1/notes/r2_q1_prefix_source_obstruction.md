# Exact local obstruction: one fixed A-containing early theme, p>=2

Status: **method obstruction only**, not a Q-CAG-HALF-6 counterexample and not a theorem that the structural class fails.

I tested a strictly richer local certificate than the previously recorded `uniform-K` diagnostic. The model is m=6 with actual terminal themes `(E_1,E_2,E_3,E_4,A,B)`. Exactly one fixed early theme is required to contain A (for A-customers, `e_4=1`); the domain additionally imposes `p=e_1+e_2+e_3+e_4>=2` for every A-customer. For customers outside A all early bits are arbitrary. The comparison/reply counts are enlarged independently over `d,ell=0,...,6` with `max(0,d+ell-6)<=h<=min(d,ell)`.

The row cone contains:

- `t(6S+V)` and `z Z`, where S,Z,V are the common penultimate-menu rows;
- all four true prefix-safe rows `H_i=e_i/c-a/(sum_{j<i}e_j+6-i)`;
- three separate exception rows `K_i=(e_i/c-a/6)+(b/c-e_i/(p+a+1))/5`, i=1,2,3;
- the final-player deviation row `L_A=b/c-a/(p+a+1)`;
- six genuine source-at-player-4 cuts from `early_source_cuts.md`, each querying one of `A,B,E_1,E_2,E_3,E_4`. The source row has left side `u_4+(4/7)u_3+(16/35)u_6`; its per-customer right side is the exact Fraction minimum over hidden `(p,q)` in the reviewed `psi` formula. Each source row is a valid same-strategy true-IC/capacity inequality, but this note only tests their local coefficient cone.

The attached Fraction script `r2_q1_prefix_source_obstruction.py` gives a Farkas witness supported on seven customer columns. In row order `(t,z,H0,H1,H2,H3,K0,K1,K2,L_A,SRC_A,SRC_B,SRC_E1,SRC_E2,SRC_E3,SRC_E4)`, the nonnegative witness masses are:

```text
(0,0,0000,d=1,ell=0,h=0): 5/361
(0,0,0000,d=1,ell=1,h=0): 180/361
(0,1,0000,d=1,ell=0,h=0): 6/361
(0,1,0010,d=1,ell=0,h=0): 44/361
(0,1,0110,d=1,ell=0,h=0): 6/361
(1,0,0101,d=1,ell=0,h=0): 60/361
(1,0,1001,d=1,ell=0,h=0): 60/361
```

They sum to 1. Exact aggregation gives the row dot products

```text
t=z=H0=H1=H2=L_A=0,
H3=10/361,
K0=3/361, K1=23/1805, K2=26/1805,
SRC_A=734/22743,
SRC_B=35759/568575,
SRC_E1=1427/22743,
SRC_E2=34499/568575,
SRC_E3=39119/568575,
SRC_E4=734/22743,
```

all nonnegative, while the weighted target right side is `-9/361`. Thus no nonnegative combination of this entire specified row family can prove the local half inequality, even after adding individual K rows, all prefix denominators, and all six reviewed source cuts. This only rules out that certificate family; additional true cross-source rows, route/membership identities, or a different proof may still close the structural class. It is recorded to prevent repeatedly retrying the same enriched local cone.

Reproduce:

```sh
python research/workspaces/customer-attraction/R-c499e3814bbe4743b298e230b37ddca1/notes/r2_q1_prefix_source_obstruction.py
```

## Stronger replay including source-3 and source-2 cuts

The stronger script `r2_q1_prefix_source_all_obstruction.py` adds the reviewed
source-at-3 cut (left side `u_3+2K/9`, query `A`) and source-at-2 cut (left side
`u_2+3u_6/32+7K/64`, query `A`) to the same row cone. The same seven-column
weights, with the second column changed to `(0,0,0000,d=1,ell=6,h=1)` and
weights `155/361,30/361,6/361,44/361,6/361,60/361,60/361`, still sum to one and
give `b^T y=-9/361`. The additional exact row dot products are

```text
SRC3_A=23267/116964,   SRC2_A=14815/138624,
```

and are nonnegative; all previously listed row dot products remain unchanged.
Thus even the union of the reviewed source-4, source-3 and source-2 cuts does
not close this specified local cone. This remains a boundary for the chosen
certificate family only; it does not rule out new cross-source rows or the
original half claim.

Reproduce the stronger check with:

```sh
python research/workspaces/customer-attraction/R-c499e3814bbe4743b298e230b37ddca1/notes/r2_q1_prefix_source_all_obstruction.py
```
