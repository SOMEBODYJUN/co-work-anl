# 奇数环单成员群组：实际游戏存在界的独立证明

Status: complete internal proof in the stated subclass; independently
reconstructed from the single-conflict state graph. This is an upper bound,
not a sharp-threshold claim. It does not cover any cohort with more than one
player and does not establish a universal upper bound for MODEL.

## Statement

Let $m\ge3$ be odd, $n_i=1$ at every index, and retain the original
two-action ring strategies, positive weights, nonnegative polynomial fees
of degree at most $d\ge2$, and symmetric action copies. Shapes may vary
between ring groups. For every $\alpha\ge T_d$ there is an
$\alpha$-PNE. In fact one can find such an equilibrium among the $2m$
single-conflict states modulo global action exchange.

This statement can be combined with any independently verified stronger
upper bound that applies to this subclass. It does not assert attainment of
$T_d$ from below.

## Single-conflict states

Put the $2m$ resource positions around a cycle in order

$$
A_0,B_0,A_1,B_1,\ldots,A_{m-1},B_{m-1}.
$$

The $A_i$ position is a conflict if hub $H_i$ and light $L_i$ choose
the same action; its selected copy then contains both weights. The $B_i$
position is a conflict if $L_i$ and $H_{i+1}$ choose opposite actions.
Each player's two incident resource positions are consecutive on the cycle.

No-conflict requirements flip the bit across each $A_i$ and preserve it
across each $B_i$. Their product flips a bit $m$ times and is inconsistent
because $m$ is odd. If any one requirement is reversed, the conditions
become consistent. Consequently each possible conflict position gives
exactly one single-conflict state modulo exchanging every action bit.
These are $2m$ states, and global exchange preserves every cost.

At a single-conflict state, a player incident to the conflict moves it to its
other incident position by flipping. Every other player flips two
non-conflicts into conflicts: both of its resource loads increase, so
monotonicity implies its deviation cost is at least its current cost.
Such a player cannot strictly improve by a factor $\alpha\ge1$.

Therefore all possible strict improvements among single-conflict states
move the defect along one edge of a $2m$-vertex cycle. Each cycle edge
corresponds to one player. The two directions along that edge exchange
that player's current and deviation costs, so at most one direction can
be a strict $\alpha$-improvement for $\alpha\ge1$, including when costs
are zero.

If every single-conflict state had a strict improvement, the directed cycle
would have outdegree at least one at every vertex. There are only $2m$
edges and each supports at most one arc. Counting arcs forces exactly one
outgoing arc at every vertex and every edge to be oriented. This is possible
only if the entire cycle is coherently oriented.

## A coherent orientation is exactly the two-test system

In the direction $A_i\longrightarrow B_i\longrightarrow A_{i+1}$,
the $A_i$ defect is moved by $L_i$. Its exact current and deviation
costs are

$$
a_iF_i(u_i+v_i)+b_iG_i(v_i),\qquad
a_iF_i(v_i)+b_iG_i(u_{i+1}+v_i).
$$

The strict inequality is precisely $a_iN_i>b_iP_i$ with $n_i=1$.
The $B_{i-1}$ defect is moved by $H_i$, whose exact costs are

$$
a_iF_i(u_i)+b_{i-1}G_{i-1}(u_i+v_{i-1}),\qquad
a_iF_i(u_i+v_i)+b_{i-1}G_{i-1}(u_i).
$$

Its strict inequality is $b_{i-1}Q_{i-1}>a_iM_i$.
Thus a coherent orientation in this direction provides all strict uniform
tests. Zero shapes cannot satisfy this complete set, as the polynomial
review proves. With nonzero shapes, the polynomial envelope forbids the
tests when $\alpha\ge T_d$.

For the opposite orientation, it is essential to reverse the ring order,
not merely shift the alternating hub/light labeling. Define a new index
$j$ corresponding to old index $i=-j\pmod m$, and set

$$
H'_j=L_i,\qquad L'_j=H_i,\qquad
u'_j=v_i,\quad v'_j=u_i,\qquad
h'_j=l_i,\quad l'_j=h_i,
$$

$$
(A'_j)^b=A_i^b,\qquad
(B'_j)^b=B_{i-1}^{\,1-b},\qquad
F'_j=F_i,\quad G'_j=G_{i-1}.
$$

The new hub $L_i$ uses $A_i^{l_i}$ and the incoming
$B_i^{1-l_i}$, while the new light $H_i$ uses $A_i^{h_i}$ and
$B_{i-1}^{h_i}$. These are exactly their original strategies. The new
forward cycle $A'_j\to B'_j\to A'_{j+1}$ is the original reverse
cycle $A_i\to B_{i-1}\to A_{i-1}$. The new shapes still have
nonnegative coefficients and degree at most $d$, and $n'_j=1$.
Hence the same polynomial-envelope obstruction forbids this orientation.

Both coherent orientations are impossible. Thus some single-conflict state
has no outgoing strict improvement. Nonincident players cannot improve
either, so that state is an $\alpha$-PNE. The weak equilibrium inequality
correctly retains equality cases at $\alpha=T_d$.

## Limit of the argument

When $n_i>1$, the common resource $A_i$ may contain several lights.
A player's flip can create, remove, or alter a partially aligned cohort;
single-conflict positions no longer form the $2m$-vertex cycle above.
The arc-counting reduction therefore does not establish an existence bound
for general cohorts. This missing reduction must be proved separately, or
an exact counterexample found, before assigning any actual-topology upper
claim to the larger class.

The companion check_singleton_graph.py checks $m=3,5$ and $d=2,4$
with rational weights, nonnegative polynomial shapes, and a zero-fee resource.
It verifies the $2m$ state count, neighboring cost exchange, nonincident
monotonicity, mutual exclusion of opposite arcs, and the exact reverse-ring
map. The existence tests use the safely larger factor $\alpha=d$; the
general proof above supplies the sharper $\alpha=T_d$ endpoint.


---
整理来源与当前文件用途见[逐文件登记](../../../weighted_congestion_frontier/FILES.md)。程序统一通过 `python3 tests/audits/weighted_congestion/replay.py --list` 选择；历史命令、输出摘要与源码哈希属于原冻结版本。
