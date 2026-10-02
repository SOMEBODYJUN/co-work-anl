# SC-K-LEXMAX-BARRIER: the selected layout can genuinely need almost two

**Version 1, 2026-10-02; complete internal proof.** This is a sharp limitation of
the *on-path layout selection* used by SC-K-2-E. It is NOT a sharpness lower bound
for the full game: the constructed instances all have alpha^*=1.

## Exact statement and explicit input

For every integer k>=2 and h>=2, there is an instance with k labeled facilities,
a common catalog of k sites, and k explicitly listed positive rational clients.
Every layout maximizing the sorted load vector of a site-uniform profile has
optimal full-continuation factor exactly

\[
                   \beta_h=\frac{2h}{h+1}\longrightarrow2.
\]

This remains a lower bound even if one chooses ANY exact independent mixed
customer NE at that selected layout, not merely the site-uniform one, and ANY
legal off-path continuations. Nevertheless the full instance admits an exact
SPE at a different layout. Thus lowering the universal bound below two by
changing ONLY off-path selection, or only the on-path NE at the same lexmax
layout, cannot work in general, even for each fixed k.

Let the sites be A,T,Z_2,...,Z_{k-1}, with the Z-list empty for k=2. Use clients
H of weight h covering {A,T}, e of weight 1 covering {A}, and, for every j>=2,
a client z_j of weight M=3(h+1)/4 covering only {Z_j}. Put a=(h+1)/2, so
M=3a/2, 1<a and h>a. Multiplying by 4 gives integer weights 4h,4,3(h+1),...,3(h+1).
Encoding is explicit with O(k) atoms and labels and O(k log h+k log k) bits
for sparse incidence. No customer is represented by a compressed multiplicity.

## 1. All site-uniform lexicographic maxima have the same occupancy

The layout with two facilities at A and one at each Z_j, with H and e each
independently uniform between the two A facilities, has sorted vector
(a,a,M,...,M).

In any competing site-uniform profile, an anchor site with two or more
facilities has per-facility load <=M/2=3a/4<a. If every occupied anchor instead
has just one facility, at most k-2 facilities are there, so at least two are in
{A,T}. The total client weight assignable to {A,T} is at most h+1=2a. Three or
more facilities there therefore give a coordinate <a.

To attain minimum at least a, exactly two facilities must be in {A,T} and all
anchors must be occupied once. Two at T lose e and have load h/2<a. With one
at A and one at T, a site-pure assignment of H leaves either the T facility
empty or the A facility with only e; the minimum is at most 1<a. Hence the two
must both be at A. This proves uniqueness of the maximizing OCCUPANCY, up to
labels, and gives the displayed uniform profile. No tie-breaking loophole
remains.

## 2. Every on-path NE at that occupancy has an unavoidable beta_h threat

At any such occupancy, only the two A facilities can serve H and e; the total
of their revenues is h+1. In EVERY on-path customer NE, one of them has revenue
at most a. Move that labeled facility to T.

Client e is forced to the remaining single A facility. At T, H's excluded load
is zero; at A it is exactly 1. Thus its conditional cost is h at T versus h+1
at A. EVERY exact mixed customer NE strictly forces H to the deviator. Anchor
clients are forced to their respective single facilities and do not change
this strict inequality. The deviator's revenue is h in every continuation.
Thus any feasible factor at the original layout is at least h/a=beta_h.

This lower argument uses the total revenue and a strict best response, so it
excludes all on-path equilibria and all off-path equilibria at the selected
layout, not just an implementation or a finite menu.

## 3. The selected occupancy attains beta_h

Use the uniform on-path profile. At either A->T deviation, use the forced NE
just described, with deviator revenue h. At either A->Z_j deviation, H and e
are forced to the single remaining A facility; let z_j use the stationary Z_j
facility, so the deviator receives zero.

At any anchor facility's deviation to A, T, or another anchor, place H alone
on one stationary A facility and e alone on the other. Keep every remaining
anchor client on its stationary anchor; the vacated-anchor client becomes
unserved. The deviator receives zero. Every served client is alone and incurs
its own weight, the minimum possible cost, so this is an exact pure NE.
These are all possible deviation types in the full common catalog. Complete
other layouts with the finite pure-NE default. Hence the optimal factor at
this occupancy is exactly beta_h.

## 4. A different layout has an exact SPE

Put one facility at T, one at A, and one at each anchor. On path let H choose T,
e choose A, and each z_j choose its own anchor. All served clients are alone,
so this is an exact pure customer NE.

For any deviation other than T->A, assign every still-covered client to a
stationary accessible facility, choosing T for H when a stationary T exists.
The deviator receives zero. This is a pure NE: typically clients are alone;
in the exceptional T->Z_j case, H and e are both forced to the sole remaining
A facility, so neither has an alternative. Vacated private clients become
unserved as required.

For T->A, place H alone on the stationary A facility and e alone on the
deviator. This is a pure NE, with deviator revenue 1<=h, its on-path revenue.
Again, all common-catalog targets and all labels are covered, and the distinct
actual deviation layouts can be completed with the pure default. This is an
exact SPE; therefore alpha^*(I,k)=1. QED.

## Consequence for the frontier

For any c<2, choosing an integer h>c/(2-c) gives beta_h>c. Hence the *same*
lexmax layout rule cannot prove a universal factor c, regardless of its
continuation solver or alternative exact on-path NE. This is stronger than
the scalar packing-interface obstruction. A sub-two theorem must permit a
different layout selection on these inputs. It does not follow that the full
model's sharp constant is two; these inputs are globally exact-stable.

`tests/multi_facility/run_lexmax_barrier_audit.py` checks both complete sets of
actual deviation witnesses at 20 (k,h) pairs, independently enumerates all
labeled site-uniform profiles in its small subdomain, and verifies all costs
using the independent definition-level checker. The scalable result is the
argument above, not the finite test.
