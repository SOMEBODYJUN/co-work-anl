# SC-K-SYMMETRIC-MENU-OBSTRUCTION

**Version 1, 2026-10-02. Status:** proved internally by the argument below;
independently implemented exact regressions accompany it. This is a failed-menu
obstruction, NOT a lower bound on the optimum in the full model.

## Exact statement

For each integer q>=3, let k=q+1. There is an explicit three-site, three-client,
positive-rational instance and a site-uniform lexicographic-maximizing on-path
NE such that:

1. At one actual deviation, EVERY exact NE that is symmetric among co-located
   facilities gives the deviator an improvement ratio q^2/(q-1/4), unbounded as
   q grows.
2. The SAME on-path layout and NE extend, with unrestricted off-path exact NE,
   to an EXACT SPE. In particular alpha^*(I,k)=1.

The statement does NOT say that all on-path layouts fail for a symmetric menu.
It rules out completing this lexicographic witness while insisting on
co-location-symmetric off-path equilibria. It also gives a precise warning
against converting a bad-menu example into a full-quantifier lower bound.

## Input and on-path profile

Use the common catalog {A,B,T} and the following client atoms:

| Client | Weight | Accessible sites |
|---|---:|---|
| H | q^2 | A,T |
| e | 1 | A |
| b | a=q-1/4 | B |

All weights are positive. Multiplying by 4 gives the integer input
(4q^2,4,4q-1). The three atoms are explicitly listed, as are k facility labels;
no multiplicity encodes hidden customers.

Put q facilities at A and one at B. Let H and e independently choose uniformly
among A's q facilities, while b chooses the B facility. Each accessible
facility has the same excluded load for the respective client, so this is an
exact independent mixed client NE. Loads are q+1/q at every A facility and a at
B, with a<q.

This is a global lexicographic maximum in the finite site-uniform family used
in SC-K-2-E, not merely an arbitrary bad layout. Indeed:

* If B is unoccupied, total served weight is at most q^2+1. The minimum facility
  load is at most (q^2+1)/(q+1)<q-1/4=a for q>=3.
* If B has at least two facilities, one (in fact every such facility) has load
  at most a/2<a.
* If B has one facility and A,T are both occupied, the indivisible site
  assignment of H goes to one of A,T. The other site receives total at most 1,
  so some facility has load at most 1<a.
* The only remaining possibilities are one facility at B and the other q all
  at A or all at T. The former has sorted vector (a,q+1/q,...,q+1/q); the latter
  has (a,q,...,q). The former is strictly larger.

## Why every symmetric off-path NE fails at the displayed deviation

Move the B facility to T. Say that a mixed client profile is co-location
symmetric if every client gives equal probabilities to any two accessible
facilities at the same physical site.

Client b becomes uncovered. Client e must choose among A's q facilities; in a
symmetric profile it therefore chooses each with probability 1/q. Client H's
excluded load is 1/q at every A facility and 0 at T. Its actual conditional costs
are q^2+1/q and q^2 respectively. Exact best response FORCES H to choose T with
probability 1. This conclusion treats all symmetric mixed equilibria, including
any proposed cross-site mixing by H; the strict cost inequality excludes it.

Thus every such continuation gives the deviator q^2 rather than its on-path
load a, for ratio

\[
                    \frac{q^2}{q-1/4}>q=k-1.
\]

## Why this is NOT a full-model lower bound

After ANY actual deviation from the displayed on-path layout, at least two
original A facilities remain stationary: q remain if the B facility moves,
and q-1>=2 remain if an A facility moves. Assign H alone to one of these
stationary A facilities and e alone to another. If the original B facility
remains, assign b alone to it; otherwise B is uncovered and b is unserved.
Assign no client to the deviator.

This handles all four types A->B, A->T, B->A and B->T, every facility label, and
both targets in the complete catalog. Every served client has actual cost
exactly its own weight, the absolute minimum possible at any facility. Hence
this is an exact PURE NE. The deviator receives zero.

Different actual deviations yield distinct labeled layouts. Use these pure
profiles there, the specified uniform profile on path, and any pure NE at all
other layouts (the squared-load potential supplies a deterministic default).
This is one complete exact continuation and yields exact facility stability.
As approximation factors are defined to be at least 1, alpha^*(I,k)=1. QED.

## Reusable conclusion and evidence

Retain on-path site symmetry to distribute an atom's EXPECTED weight among
facilities. Do not impose that symmetry after deviations: isolating a large
atom on a stationary facility can completely change the threat. The factor-two
proof uses precisely this legal freedom.

`tests/multi_facility/run_reverse_audit.py` checks q=3,4,5,8,16,31,63 with original conditional
costs and every actual labeled deviation (274 in total). For q=3,4,5 it also
independently enumerates every labeled layout and site assignment to verify
lexicographic optimality. These are finite exact attacks; the preceding
argument, not enumeration, proves the scalable family.
