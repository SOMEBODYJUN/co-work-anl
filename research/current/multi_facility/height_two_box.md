# SC-K-HEIGHT-TWO-BOX-EXISTS: opening-directed light graphs with paths of at most two edges

2026-10-03. Derived independently from the three-site exchange of Sol Box. Sol Box independently checked the algebra and feasibility; a further reviewer check is pending. No polynomial minimization assertion.

## Scope

At a positive-reach greedy layout, freeze every customer with weight at least gamma and every customer with one occupied option. Assume every remaining light customer has exactly two occupied options. Orient each edge from the site opened earlier to the site opened later. The resulting directed graph is acyclic. Suppose every directed path has at most two edges. Arbitrarily many sites, arbitrary degrees, and arbitrary positive light weights below gamma are allowed. In particular, both branching and merging are allowed.

Claim: every global minimum of exact customer potential P among full-box assignments of these light clients is an exact customer NE. This is an existence/finite-selector theorem, not a bit-polynomial constructor.

For an assignment `J_t` of customers to occupied site `t`, let `W_t` be
their total weight and `q_t` its facility count. The exact site-uniform
potential is

    P(J) = sum_t (W_t^2 - sum_{i in J_t} w_i^2)/(2q_t).

The full boxes are `q_t gamma <= W_t <= (q_t+1)gamma`. Greedy's initial
assignment lies in all of them, so their finite feasible assignment set is
nonempty. A weight-w transfer from s to v changes this potential by
`w[W_v/q_v-(W_s-w)/q_s]`, exactly the sign of the client's improvement.

## All potential blocked deviations

Every client starts at its earlier-opened endpoint, whose q is at least that of the later endpoint by GREEDY-MAX-MULT. Any strict forward move preserves the complete box. Any strict backward move whose target has no incoming light edges is also upper-feasible: that site's clients are a subset of its original pool, so adding one original client keeps its total at most its original total. Source lower bounds are preserved by every strict move between box states.

Thus suppose a constrained minimum has a blocked strict backward move of a client of weight w, from later site v back to its original site u. Write q=q_u, M=W_u, E=(W_v-w)/q_v. Then

    E > M/q,
    delta=M+w-(q+1)gamma > 0.

Because u has the outgoing edge u->v and directed paths have length at most two, every incoming neighbor h of u is a source (has no incoming edge). Source u itself was already handled.

## Select entire incoming pools

For each incoming source h, let X_h be all h-origin customers now at u, with total S_h and squared-weight total T_h. Let Q_h=q_h>=q, A_h=W_h. Since h has no incoming light clients, all of its current clients are from its original pool. Consequently

    0 <= S_h <= gamma,
    A_h+S_h <= W_h^0 <= (Q_h+1)gamma.

The first inequality follows because its total outbound weight W_h^0-A_h is at most gamma, by original upper and current lower boxes.

Let I=sum_h S_h. If R is the total original-u client weight currently at later endpoints, then M=W_u^0-R+I. Because the proposed returning customer belongs to that set, R>=w, hence

    I=M-W_u^0+R >= M-(q+1)gamma+w = delta.

Ignore zero pools. Choose source pools in any order until their cumulative total S first reaches delta. Each selected pool is at most gamma, so

    delta <= S < delta+gamma.

Return all clients in the selected X_h pools to their original h, and return the weight-w customer from v to u. At each h the load rises but stays at most its initial upper-box load. The new u load equals

    M-S+w=(q+1)gamma+delta-S,

which lies strictly above q gamma and at most (q+1)gamma. The v load falls by w; its new normalized load E is above M/q>=gamma. Thus the whole exchange remains in every box.

## Exact potential calculation

Let T=sum_h T_h and cross=sum_{h<j} S_h S_j, summing only selected pools in their chosen order. The exact potential difference is

    Delta P = sum_h [A_h S_h/Q_h + (S_h^2-T_h)/(2Q_h)]
              - M S/q + (S^2+T)/(2q)
              + w[(M-S)/q-E].

Use E>M/q to bound the final term strictly from above by -wS/q. Then use A_h+S_h<=(Q_h+1)gamma and M+w=(q+1)gamma+delta. Collecting terms gives

    Delta P < sum_h (1/q-1/Q_h)
                        [(S_h^2+T_h)/2-S_h gamma]
              + (cross-S delta)/q.

Every bracket is nonpositive: T_h<=S_h^2 and S_h<=gamma. Every coefficient is nonnegative because Q_h>=q. Finally, the cumulative sum before each selected pool is strictly less than delta, by the first-crossing selection rule. Therefore

    cross = sum_h S_h (sum_{j before h} S_j) < delta sum_h S_h = delta S.

The final potential difference is strictly negative, contradicting constrained global minimality.

Every light client is therefore stable. Frozen heavy clients are stable by the full boxes and weight>=gamma; singleton-option clients are automatic. Uniform independent mixing inside the assigned sites gives exact original-model client NE. The existing BOX-TO-2 interface gives a complete factor-two continuation once the finite optimizer is supplied.

The argument also gives a polynomially evaluable **local** neighborhood on
full-box assignments. Include every box-feasible strictly improving single
client move. For each strict backward improvement blocked only by its target
upper box, use a fixed order of incoming source sites and the first-crossing
whole-pool exchange above. Every listed neighbor stays boxed and lowers the
exact potential, so any local minimum is a client NE. The initial greedy
assignment is feasible. Clear the rational denominators of the potential
with a polynomial-bit product to obtain the usual finite PLS formulation;
this supplies no polynomial bound on the number of improving steps. It also
does not turn the global constrained minimization used above into an
input-bit-polynomial algorithm.

## Strict multi-parent and unequal-edge witness

Take sites `H1,H2,M,L`, `k=10`, private weights respectively
`183,140,89,41`, and light clients of weights `15,1` on H1--M,
`13` on H2--M and `6` on M--L. Greedy strictly chooses
`H1,H2,H1,M,H2,H1,H2,H1,M,L` with scores
`199,153,199/2,95,153/2,199/3,51,199/4,95/2,41`.
Thus `q=(4,3,2,1)`, `gamma=41` and original totals
`(199,153,95,41)`. The opening-directed graph has both
`H1->M` and `H2->M`, then `M->L`, and two different weights on H1--M.
Of the 16 assignments of four variable clients, 15 satisfy all boxes.
The unique constrained-potential minimum assigns the first two clients
to H1, the weight-13 client to M and the weight-6 client to L. Its site
totals are `(199,140,102,47)`, potential `6241/4`, and all exact client
NE inequalities hold. The graph has no earlier-opened star center and is
not a directed path; per-edge equality, uniform light weight, RANGE and
the double-LPT first packing check all fail. The [integer input](../../../examples/multi_facility/greedy_height_two_unequal.json)
and [independent exact arithmetic audit](../../../tests/audits/kfac_height_two.py)
verify this **one** witness; the exchange above is the universal proof.

## Remaining obligations

1. This proof neither supplies polynomial global potential minimization nor proves the all-input greedy box conjecture.
2. For a directed path of length three or more, a parent of a possible blocked-return target can itself have incoming light weight. Then S_h need not be <=gamma, and the nonpositive bracket proof can fail. That remains the specific generalization barrier.
