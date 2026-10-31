# Author proof: conditional Hall gap and exact path projection

Author proof for the separately frozen `sol_general_repair_conditional_hall_exact_v2.md`.
This is not an independent reconstruction. Do not send this file or the author
checker to a fresh Exact-first reviewer before that reviewer freezes their
reconstruction. The main target remains OPEN.

## A. Normalized value and the necessary relaxation

For any disjoint bundles choose an attaining indexed state for each group,
export only its owned positive incidences to their resource machines, and
put its selector on that private root. All other incidence jobs, including
all jobs in unselected states, stay on their own private roots. Unselected
private load is one. Selected private load is two minus that group's owned
value, and each resource receives at most one unit job. Thus OPT<=2-V.

Conversely, for any complete schedule of peak C<2, the private root holding
each group's selector must export positive private work of total at least
2-C. Each resource machine holds at most one unit job. Reading only the
positive exports from the actually selected state gives disjoint bundles
of value at least 2-C. Exports from unselected states and zero jobs can only
consume additional resource capacity. OPT<=2 by keeping all incidence
jobs private; consequently the same inequality at the endpoint C=2 gives
OPT=2-V throughout. The nonempty selector set also gives OPT>=1.

For threshold preprocessing, a heavy item alone gives value at least
epsilon. Without a heavy item, every bundle's value is at most the
explicitly computed tail b_g. If b_g>=epsilon, the whole complement of
the heavy items is itself a counterexample to the threshold-unit-demand
property. Hence the test in Exact section 2 is exact.

Given an actual allocation with min value epsilon, retain one attaining
core state per core and only the positive resources used in that state.
Take its lambda to be one and its z to be the corresponding 0/1 ownership.
For every leaf, keep one owned heavy item. Those chosen leaf items form
one integral matching, disjoint from every core's z. Use that matching as
y^0 and as the conditional flow for every positive-lambda core state;
all zero-lambda conditional flows are zero. This proves all necessary
constraints, including the complete conditional columns. All coefficients
and dimensions are explicitly rational and polynomial as counted in the
Exact statement, so a rational LP gives deterministic total-bit polynomial
construction/feasibility. The LP need not output an actual allocation.

## B. Existing path operation: matching with one hole

For d ordered ports u_1,...,u_d, leaf i is adjacent to u_i,u_{i+1}.
For each hole j, match leaf i to u_i when i<j and to u_{i+1} when i>=j.
This is one integral matching of all d-1 leaves onto all ports except u_j.
It also covers d=1, with an empty matching and the unique port as hole.
No leaves are created at d=0, where the original resource is retained.

If pi is any probability distribution on these d holes, the average
matching has each leaf row one and each port column 1-pi_j. This is the
existing adjacent-dummy/path-copy device; its use here does not claim a
new general normalization construction.

## C. Exact basic-polytope projection

Fix any feasible old basic point (lambda,z). On old resource u, index its
positive core neighbors by c_1,...,c_d and put

\[
a_i=\sum_s z_{c_i,s,u}.
\]

The old resource column gives sum_i a_i<=1. Choose a rational hole
distribution pi_i>=a_i by adding all slack to the first coordinate.
Use its average path matching as the global leaf flow for that path.
The new core usage of port i is a_i, so the total column is
a_i+(1-pi_i)<=1. Every global leaf row is one. Different old-resource
paths are disjoint, so these flows together form one complete global
leaf flow. The d=0 resource has no core z or leaf flow.

For a particular core-state h=(c,s), there is at most one core-positive
port on each old-resource path: the one owned by group c, when present.
Choose it as the hole; when c has no port on this path choose an arbitrary
hole. Take this path's single matching and multiply its flow by lambda_h.
The only possible nonzero z_h on the path is at the hole and is bounded
by lambda_h. Thus every conditional port column is at most lambda_h,
and every conditional leaf row is lambda_h. These matchings on different
paths form one matching of all leaves. This argument even works for
fractional z: it leaves the entire own port free, and does not require
z_h=lambda_h. It also works when the own port is absent in that particular
state but present elsewhere in the group's menu. If lambda_h=0, the
scaled matching and z are both zero.

No conditional law is required to average to the separate y^0. No other
core's z enters a conditional column. Those two facts are exactly the
weakness used here.

Conversely, sum all d global port columns of any feasible lifted point.
The d-1 added leaf rows, each equal to one, account for exactly d-1 total
flow on these ports. Therefore

\[
\sum_{i,s}z_{c_i,s,u}+(d-1)\le d,
\]

which is the old resource capacity. Normalizations, bounds and utilities
are unchanged by relabeling a group's original resource as its own port.
At d=1 the single new column is directly the old column; at d=0 the old
column is zero. This proves both projection inclusions for the same point
(lambda,z), not only equivalence of feasibility.

The new number of ports and leaves is at most the number of distinct
positive group-resource incidences, with one retained resource for each
old d=0 resource. The conditional construction multiplies each of a
polynomial number of matching entries by one original lambda. Global
hole probabilities use polynomial-length sums of supplied rationals;
their bit length is polynomial in the total supplied point length.
This proves the stated size bounds without reciprocal-weight expansion.

All old zero incidences are retained by the mapping in the Exact. For a
given old u their coefficient is still zero. Distinct old resource tags
do not merge, and a state cannot acquire two copies of the same old
incidence by this mapping. These zero incidences do not enter the positive
core z support or change any utility or threshold-heavy set.

The automatic threshold partition needs the stated precondition. The
positive coefficients of each old group have only been renamed, so its
threshold-unit-demand test is unchanged. If an old group was already
threshold-unit-demand, the automatic partition would move it to L;
then the polytope with that different designated core set is not the
one just projected. For example, two old singleton groups on the same
resource have a feasible basic point at epsilon=1/2, but their path
instance has three singleton-demand groups on only two ports. Its
automatic all-leaf matching is infeasible. Q_t avoids this issue.

## D. Actual value and FSLP preservation of the path operation

Given any old allocation, discard zero-valued owned resources and keep
each core's actually used positive resources. A resource has at most one
owner. Leave that owner's port as the hole, or an arbitrary port when
there is no owner, and match the path leaves to all other ports. Every
core keeps exactly its old value and every leaf gets value one. Since
old normalized values are at most one, new min value is at least old
min value.

In a new allocation with positive minimum, every path leaf owns at least
one of its two positive ports. Different leaves own different ports.
Thus a path with d ports leaves at most one port for positive use by
all old cores together. Each old core values only its own port; ignore
any of its other zero-valued owned ports. Collapse the remaining core
ports back to the old resource. No positive ownership conflict occurs,
and all old core values are preserved. Hence the new minimum cannot
exceed old V. If old V=0, a positive new allocation would contradict
this projection, so equality includes zero. With d=0, the old and new
unused zero-valued resource is ignored in both directions.

For FSLP, take a core state's full support usage z=lambda. The same
global hole construction gives the added leaf state probabilities and
preserves the original core probabilities. Conversely summing all
ports and subtracting d-1 unit leaf rows gives every old positive-support
column. This is exact projection of FSLP as claimed.

The two full ordinary matrices have different resource endpoints and
added jobs, but both are constructed completely and satisfy OPT=2-V.
The old incidence job identities/private coefficients can all be
retained; no original indexed state or zero job is discarded.

## E. The diffuse-fallback core family

For D=t^2, put probability 1/D on every M row state. Put probability
1-1/D on H_{a,j}'s home state and 1/D on its parking state.
The full-support load on every g_{a,j} is

\[
1/D+(1-1/D)=1,
\]

and the load on every A_{a,h} is D(1/D)=1. This is a genuine FSLP(1)
point. Taking z=lambda makes every state utility equal to lambda, hence
satisfies the basic epsilon=1 relaxation. Sections C-D give its lifted
global flow and all perspective conditional flows. In this particular
point, every global port column is exactly one, and every conditional
flow is one integral matching times its own lambda.

To bound actual value, consider any positive-minimum old allocation and
an attaining M state a. Let r be the number of g_{a,j} owned by M.
Then M's value is r/D. Each of the corresponding r helpers lacks its
home item and must obtain all its positive value from the common t-item
parking pool A_a. Total parking value, summed over those r helpers, is
at most one. If their common minimum is v, then

\[
v\le r/D,\qquad rv\le1,
\qquad v^2\le1/D=1/t^2.
\]

This also covers r=0 by v=0. For attainment choose any row, give M t of
its g items, give the t blocked helpers one distinct A item each, and
give every other helper its own g. Exactly M and the t blocked helpers
have value 1/t; all other cores have value one. The path extension gives
every leaf value one. Thus V=1/t exactly, and full ordinary OPT=2-1/t.

At epsilon=1 the main has no heavy item, so its tail is one. Each H has
its home g as its only heavy item, but its complete parking state gives
tail one. Thus none of these cores is threshold-unit-demand. For any
fixed epsilon>0 and t>1/epsilon, both parking coefficients 1/t and main
coefficients 1/t^2 are below epsilon, so the same test and partition
hold. The already feasible epsilon=1 point remains feasible for epsilon,
while V=1/t<epsilon. Every added leaf is threshold-unit-demand throughout.

## F. Sizes, all jobs, and exact checks

There are D^2 old g resources of positive core degree two, and Dt old A
resources of positive core degree D. Hence there are
P_0=2D^2+D^2t ports and L_0=D^2+Dt(D-1) leaves. There are
K=1+D^2 cores and S_C=D+2D^2 core states. Every port has one core
positive incidence, so core incidence count is P_0. Each leaf contributes
two singleton state incidences, giving I=P_0+2L_0. Every port is incident
to at most one core and two adjacent path leaves. In this family each
core port occurs in exactly one core state, so the same degree-three
bound also holds at the positive indexed-state incidence level.

The schedule explicitly puts every selector at its attained state,
exports exactly its owned positive incidence jobs, and keeps all other
jobs private. Each unselected state has private incidence load one.
Each selected core root has load two minus its attained value, every
selected leaf root has load one, and every resource machine has load
at most one. There are exactly K+L_0 selectors and I incidence jobs,
and none is omitted. Appended zero jobs stay private at time zero;
they cannot improve the lower bound, which uses the original positive
jobs and original selectors only. Unused resource machines and duplicate
states do not change the value argument.

The author script `sol_general_repair_conditional_hall_gap.py` constructs
all menus and verifies global flow rows/columns, the exact threshold
partition, every per-state conditional matching, the attaining allocation,
every full-UM job's finite endpoint and resulting load, the degree bounds,
and the size formulas using `fractions.Fraction`. For t=2,3,4 it additionally
enumerates all assignments of all parking items to r blocked helpers
(or unused), for every r<=t; r>t must leave some blocked helper at zero.
State-row and home-subset symmetry give this closed-form reduction to
a finite one-row check. It is not an independent optimization oracle
enumerating all assignments of the full ordinary processing matrix.

Executed t=2,3,4: 735 core-state conditions and 694275 conditional leaf
rows checked; 1090 reduced parking allocations enumerated. The
exact actual values were 1/2,1/3,1/4. The checker is supplementary
evidence and not the proof of the all-t statement. No repository file,
Work registration, commit or external posting was modified by this work.
