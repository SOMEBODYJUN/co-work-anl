# Partitioned frozen optimal queries

Status: exact algebra and a new sufficient candidate; no general SPE payment
proof. Q-CAG-HALF remains OPEN.

## Definition and exact minimization

Fix an actual ordered terminal profile S=(S_1,...,S_m) and an optimal length-m
comparison portfolio T=(T_1,...,T_m). Repeated labels are allowed; portfolio
occurrences remain distinct. Write C=union_i S_i, O=union_j T_j, c_x the actual
load and k_x the number of comparison occurrences covering x.

Choose a permutation pi matching comparison occurrences to actual positions,
and partition O into blocks P_1,...,P_m with P_j subset T_j. Query only the
assigned block rather than the whole comparison topic:

    R(pi,P) = sum_i sum_{x in P_pi(i)} 1/(c_x+1-1_{x in S_i}).

This is a frozen-opponent accounting expression, not an action that needs to
belong to the catalog and not a true sequential deviation. All omitted duplicate
contributions are nonnegative, so R(pi,P)<=Q(pi).

For fixed pi every client can independently select its cheapest eligible owner.
Consequently, with R(pi)=min_P R(pi,P),

    R(pi) = |O\C| + sum_{x in O intersect C} [ 1/(c_x+1)
       + 1_{all comparison occurrences containing x are assigned to positions
                  whose actual topics contain x}/(c_x(c_x+1)) ].

This identity includes empty blocks and repeated topics. The exceptional event
means every eligible owner would remove an actual cover; otherwise an eligible
owner with no actual cover gives denominator c_x+1.

## Uniform matching and a potential global interface

Under a uniformly random permutation pi, the k_x eligible occurrences occupy a
uniform k_x-subset of the m actual positions. Thus for c_x>0

    E R = |O\C| + sum_{x in O intersect C} [ 1/(c_x+1)
                  + binom(c_x,k_x)/(binom(m,k_x)c_x(c_x+1)) ],

where binom(c,k)=0 for k>c. In particular min_pi R(pi)<=E R. The case k=1
has expected contribution (1+1/m)/(c+1); the case c=m always contributes 1/m.
Compared with adding-query A=sum_x k_x/(c_x+1), partitioned queries remove all
duplicate optimal incidences. The two payment conditions R<=W and A<=W are not
ordered in general: unique-incidence clients can retain a frozen-removal
correction in R, whereas duplicate incidences can make A much larger.

Candidate PFR-OPT-v1: for every CAG-MODEL instance and every complete-history
pure SPE terminal profile, there exists an optimal length-m portfolio and a
matching pi with R(pi)<=W. This candidate is OPEN. If true, it would imply

    OPT_m <= (2-1/m)W

because every missed optimal client contributes 1 to R and every covered
optimal client contributes at least 1/m. It would also imply the full terminal
tax bound

    OPT_m <= W + sum_{x in C} c_x/(c_x+1),

using instead the clientwise lower bound 1/(c_x+1). These are conditional
implications, not proved inequalities for general SPE.

## Sharp-family check

In the standard disjoint-topic lower family, topic 0 has m private clients and
the other m-1 topics have one private client each. There is a complete SPE with
all m players on topic 0. Here W=m and OPT=2m-1; the optimal portfolio uses all
m topics. Its partitioned frozen query equals R=m for every matching: the big
topic contributes 1 and the missed singleton topics contribute m-1. Thus the
candidate cannot generally be improved to R<=(1-epsilon)W.

## Finite evidence

`probe.py --query-mode partition` retains every ordered-history incentive row of
each sampled credible full policy, all m! matchings and every competing
size-m optimal-support comparison. It maximizes min_pi R(pi)/W over the policy
customer multiplicity cone under a strict chosen-optimum margin against every
other size-m support. For p>m, these inequalities also exclude a tied smaller
optimal support, since such a support extends to another size-m support. For
p=m, there is only one size-m support and the margin does not exclude tied
smaller portfolios. A positive floating separator would therefore still
require exhaustive comparison of all optimal portfolios, integer recovery,
and exact all-history verification. Finite negative runs make no universal
claim about ties or all SPE.

The p6m4 run `partition_p6m4_seed104213.json` sampled 196 distinct policies,
588 policy/target pairs, with no floating separation above one; maximal value
was 1 to solver precision. This is finite numerical evidence only.

The p7m5 partition run `partition_p7m5_seed104214.json` sampled 99 policies and
297 policy/target pairs, also with no floating separation. The canonical
example run `partition_examples_seed104216.json` adds selected complete
policies from existing counterexamples with at most seven topic labels; its
exact tested dimensions and targets are recorded per LP. These runs do not
prove the candidate.

## Exact source-policy certificates

For the old 52-client strong-Q obstruction, `dual_probe.py` recovers and
checks a rational dual proving

    R_(4,5,0,1) <= (281295/345586) W

for every nonnegative multiplicity vector making that fixed full policy SPE.
The recovered certificate uses no optimality multiplier and only one
assignment. Its 63 type residuals are nonnegative in exact Fraction arithmetic;
see `source_partition_dual.json`. This is a fixed-policy result, not a
universal matching theorem.

More usefully, [the acyclic replacement lemma](acyclic_replacement_lemma.md)
gives a general sufficient branch condition and a four-unit-row proof of
R_(4,5,0,1)<=W for that same policy. Its independent definition-level replay is
`acyclic_source_audit.py`. The acyclic condition itself is not universal; the
known two-player real-portfolio failure already rules out that existence claim.
