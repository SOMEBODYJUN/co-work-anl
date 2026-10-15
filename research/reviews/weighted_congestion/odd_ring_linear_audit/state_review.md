# Independent state audit of the odd-ring certificate

**Review identity:** R1-ODD-RING-STATE-AUDIT-v1, 2026-10-14.
**Status:** general sufficient certificate proved; coefficient feasibility proved exactly; conditional necessity proved; subsequently restored linear-reset proof and interface barrier independently checked. No literature or novelty claim is made.
**Scope:** the specified finite binary-strategy family in WC-TARGET v1, with the cost convention and the closed equilibrium boundary in `MODEL.md`.
**Independence:** the reviewer first read `MODEL.md` and `ACCEPTANCE.md`, reconstructed resource loads directly from the proposed strategies, and did not read a candidate proof. This review records that reconstruction.

## 1. Exact objects and claim

Let the ring length (m\ge1) be odd; indices are modulo (m). For each index (i), choose a hub of positive weight (u_i), (n_i\ge1) lights each of positive weight (v_i), and an integer exponent (0\le k_i\le d), where (d\ge0) is an integer. Let (a_i,b_i>0). All resources named below are distinct.

The two resources (A_i^0,A_i^1) each have cost (a_i z^{k_i}). The resources (B_{ij}^0,B_{ij}^1), for (1\le j\le n_i), each have cost (b_i z^d). Hub (i)'s strategy with bit (h_i) is

\[
\{A_i^{h_i}\}\cup\{B_{i-1,j}^{h_i}:1\le j\le n_{i-1}\}.
\]

Light (ij)'s strategy with bit (l_{ij}) is

\[
\{A_i^{l_{ij}},B_{ij}^{1-l_{ij}}\}.
\]

Fix (\alpha\ge1), and define

\[
x_i=\frac{v_i}{u_i},\quad t_i=\frac{v_i}{u_{i+1}},\quad
p_i=a_i u_i^{k_i},\quad q_i=b_i u_{i+1}^d,
\]

\[
\begin{aligned}
N_i&=(1+x_i)^{k_i}-\alpha(n_i x_i)^{k_i},\\
M_i&=\alpha(1+n_i x_i)^{k_i}-1,\\
P_i&=\alpha(1+t_i)^d-t_i^d,\\
Q_i&=(1+t_i)^d-\alpha.
\end{aligned}
\]

**Certificate.** If, for every (i),

\[
\tag{L_i}p_iN_i>q_iP_i,
\qquad
\tag{H_i}n_iq_iQ_i>p_{i+1}M_{i+1},
\]

then this game has no (\alpha)-PNE. These conditions cover every pure state, including states with partially aligned light groups.

## 2. Direct load calculation for an arbitrary mixed group

For any player, write its deviation surplus as current cost minus (\alpha) times its cost after flipping its bit. A positive surplus is exactly the strict deviation required to exclude an (\alpha)-PNE.

Suppose light (ij) matches its own hub: (l_{ij}=h_i). Let (r_i\ge1) be the number of lights in its group matching that hub, including light (ij). Its current (A)-load is (u_i+r_iv_i); after its flip its new (A)-load is ((n_i-r_i+1)v_i). Its (A)-surplus is therefore

\[
a_i\big[(u_i+r_iv_i)^{k_i}-\alpha((n_i-r_i+1)v_i)^{k_i}\big]
\ge p_iN_i.
\]

Both monotonicities go in the required direction as (r_i) increases. In particular the worst case is (r_i=1), not a fully aligned light group. This is the key mixed-state check.

The only other user of either (B_{ij}) resource is hub (i+1). If (h_{i+1}=h_i), the light's current (B)-load is (v_i), and its load after flipping is (u_{i+1}+v_i). The (B)-surplus is exactly (-q_iP_i). If (h_{i+1}\ne h_i), its (B)-surplus is

\[
q_i\big[(1+t_i)^d-\alpha t_i^d\big].
\]

The latter exceeds or equals (-q_iP_i), since the difference is

\[
q_i(1+\alpha)\big[(1+t_i)^d-t_i^d\big]\ge0.
\]

Consequently every matching light has deviation surplus at least (p_iN_i-q_iP_i>0). Any state containing even one matching light is excluded. The proof does not require the other light groups to be uniform, nor require any hub to move while its own lights remain mixed.

The bound is attained whenever (r_i=1) and (h_{i+1}=h_i). Thus (L_i) is also necessary for the stronger local requirement that **every matching light in group (i) improve in every state where it matches**. That local requirement is stronger than global nonexistence.

## 3. All lights opposite their hubs

It remains to examine states satisfying (l_{ij}=1-h_i) for all (i,j). A cyclic binary sequence of odd length cannot have every adjacent pair unequal. Choose an edge (i\to i+1) with (h_i=h_{i+1}).

Hub (i+1)'s own (A)-resource has load (u_{i+1}). After its bit flip, its new (A)-resource has load (u_{i+1}+n_{i+1}v_{i+1}), so its (A)-surplus is

\[
-p_{i+1}M_{i+1}.
\]

Each incoming light (ij) uses (B_{ij}^{h_i}). Because the two hubs have equal bits, hub (i+1) currently shares every incoming (B)-resource with its light, at load (u_{i+1}+v_i). After flipping, it uses the other member of each pair alone, at load (u_{i+1}). Its incoming (B)-surplus is exactly (n_iq_iQ_i). Its total deviation surplus is

\[
n_iq_iQ_i-p_{i+1}M_{i+1}>0.
\]

This establishes the certificate for every state. The indexing is asymmetric but correct: (n_i,q_i,Q_i) come from the predecessor's light group, while (p_{i+1},M_{i+1}) come from the deviating hub's own (A)-group.

## 4. Exact feasibility of positive coefficients

For (\alpha\ge1), (P_i\ge0) and (M_i\ge0). If the strict inequalities (L_i,H_i) hold, they force (N_i>0) and (Q_i>0). The former excludes (k_i=0); the latter excludes (d=0). Thus every feasible certificate has (k_i\ge1,d\ge1), and then (P_i,M_i>0).

Assume henceforth (N_i,Q_i>0). Define

\[
F_i=\frac{n_iN_iQ_i}{M_iP_i},\qquad T=\prod_iF_i.
\]

The strict inequalities admit positive (p_i,q_i) **if and only if** (T>1).

Necessity follows by eliminating (q_i):

\[
\frac{p_{i+1}M_{i+1}}{n_iQ_i}<q_i<\frac{p_iN_i}{P_i}
\quad\Longrightarrow\quad
\frac{p_{i+1}}{p_i}<A_i:=\frac{n_iN_iQ_i}{P_iM_{i+1}}.
\]

Multiplying cyclically gives (1<\prod_iA_i=T).

For sufficiency, let (\rho=T^{1/m}>1), choose any (p_0>0), and recursively set

\[
p_{i+1}=\frac{A_i}{\rho}p_i.
\]

The product of these ratios is one, so the cyclic recursion is consistent. It makes every displayed interval for (q_i) nonempty. Choose, for example, the arithmetic midpoint of that interval. Finally set

\[
a_i=p_i/u_i^{k_i},\qquad b_i=q_i/u_{i+1}^d.
\]

All coefficients are positive and both families of inequalities are strict. Arbitrary positive real coefficients and weights are allowed by the model, so taking a real (m)-th root presents no model issue.

At (T=1), all strict inequalities are impossible. Replacing the product test by (T\ge1), or replacing either player inequality by a weak one, would not prove nonexistence under the required closed (\alpha)-PNE definition.

## 5. Sharper necessity inside the light-forcing regime

There is a useful necessity statement beyond coefficient algebra. Assume all (L_i), but do not assume the (H_i).

First, every light is (\alpha)-stable in every all-opposite state. To check its least favorable case, take (h_{i+1}=h_i), and write its current cost and deviation cost as

\[
C_0=p_i(n_ix_i)^{k_i}+q_i(1+t_i)^d,
\qquad
C_1=p_i(1+x_i)^{k_i}+q_it_i^d.
\]

Condition (L_i) is precisely (C_1>\alpha C_0). Since (\alpha\ge1) and these costs are positive, this implies (C_0<\alpha C_1). When (h_{i+1}\ne h_i), the current (B)-cost decreases and the deviation (B)-cost increases, so the light remains stable.

Second, in an all-opposite state a hub (i+1) with (h_i\ne h_{i+1}) has surplus

\[
-p_{i+1}M_{i+1}
+n_iq_i\big[1-\alpha(1+t_i)^d\big]\le0.
\]

For every chosen edge (i\to i+1), an odd ring has a binary coloring with this edge as the **unique** equal adjacent pair: assign equal bits there and alternate on the other (m-1) edges. If (H_i) fails, the associated all-opposite state has no profitable hub flip, and by the preceding paragraph has no profitable light flip. It is an (\alpha)-PNE, including the equality case of (H_i).

Therefore, **conditional on all light-forcing inequalities (L_i), the game has no (\alpha)-PNE if and only if all (H_i) hold.** The product criterion exactly characterizes feasibility of this forcing mechanism. It does not, without further argument, characterize every nonexistence instance supported by the resource topology when some (L_i) fails.

## 6. Weight consistency and other limits

The ratios (x_i,t_i) cannot be chosen independently. They satisfy

\[
\frac{t_i}{x_i}=\frac{u_i}{u_{i+1}},\qquad
\prod_i t_i=\prod_i x_i.
\]

Conversely, any positive arrays (x_i,t_i) with this product equality are realized by positive weights: choose (u_0>0), set (u_{i+1}=u_ix_i/t_i), and set (v_i=x_iu_i). The product equality closes the cycle. A numerical optimization over independent (x_i,t_i) without this constraint does not yield an instance.

Other boundaries are as follows:

- The game belongs to the degree-at-most-(d) target class only when all (k_i\le d).
- Each (n_i) is a positive integer. Relaxing it to a real optimization variable requires a later integer realization.
- Odd parity is essential to this certificate. If the ring length is even and all (L_i) hold, alternating hub bits with all lights opposite their hubs yield an (\alpha)-PNE, by the stability checks above.
- The proof works also for the one-vertex cyclic convention (m=1), with the displayed (A) and (B) resources distinct. If “ring” is defined to require at least three vertices, simply restrict the statement to odd (m\ge3).
- All occupied-resource costs in this construction are positive, so no deviation ratio uses (0/0). The proof nevertheless uses cost differences, which directly respect the model's boundary convention.
- This review proves a conditional nonexistence theorem. An actual lower bound still requires realizable parameters meeting the strict product condition over the claimed degree range, and a separate comparison with a verified literature baseline.

## 7. Independent finite arithmetic check

A direct resource-list evaluator was run with exact Python `Fraction` arithmetic, recomputing loads after every unilateral flip. It did not use the derived surplus formulas to compute player costs. Four parameter sets were enumerated:

| (m) | (n) | (u) | (v) | (a) | (b) | (k) | (d) | (\alpha) | States |
|---|---|---|---|---|---|---|---:|---:|---:|
| 3 | (1,2,1) | (2,3,5) | (1,2,3) | (1,2,4) | (3,1,2) | (1,2,3) | 3 | 3/2 | 128 |
| 3 | (2,3,1) | (1,4,2) | (3,1,2) | (2,3,1) | (1,4,3) | (2,0,1) | 2 | 1 | 512 |
| 1 | (3) | (2) | (1) | (2) | (3) | (2) | 2 | 2 | 16 |
| 3 | (1,1,1) | (2,1,3) | (1,2,1) | (1,1,1) | (1,1,1) | (0,0,0) | 0 | 1 | 64 |

All 720 states passed: 1,912 matching-light surplus lower bounds, equality of those bounds in their specified worst states, and 74 exact all-opposite hub surplus identities. The degenerate exponent cases were included to check algebra outside the feasible certificate region. These finite checks corroborate indexing and load updates; the general proof above supplies the theorem.

**Objection status:** no fatal objection to the stated sufficient certificate. The material scope restrictions are the cyclic weight constraint, strict inequalities at the equilibrium boundary, and the distinction between feasibility of this forcing mechanism and global optimality of the topology.

## 8. Subsequent attack on the restored linear-reset proof

Only after completing the independent reconstruction above, the reviewer read the restored `odd_cycle/general_lower_bound.md` (OC-AMPLIFIER-LIMIT-v1) and `odd_cycle/INTERFACE_BARRIER.md` (OC-INTERFACE-BARRIER-v1). The restored source uses (q_i) for the main-resource scale and (p_i) for the side-resource scale; sections 1–7 above use the opposite naming convention. The mathematical quantities and all inequalities agree after that symbol swap.

### The (H_d(t)) trigger and finite ring length

Set (y=(1+t)^d), (P=\alpha y-t^d), (Q=y-\alpha), and (B=Q/P). For (d\ge1), (0<t<1), and (\alpha>1), (P>0). Direct rearrangement gives

\[
\alpha<\frac{y+t^{d+1}}{1+ty}
\iff y-\alpha>t(\alpha y-t^d)
\iff Q>tP.
\]

Thus (Q>0), (B/t>1), and both denominators in the proposed lower bounds on (R), namely (\ln(1/t)) and (\ln(B/t)), are strictly positive. Their numerators are finite. There is a finite integer (R\equiv1\pmod4), (R\ge5), exceeding both thresholds; then (m=(R+1)/2\ge3) is odd. No limiting or infinite game is needed.

The explicit weights in the source satisfy every prescribed ratio, including both cyclic joins:

\[
u_0=1,\quad u_i=t^{2(m-i)},\quad
v_0=t^{2m-1},\quad v_i=t^{2(m-i)-1}\quad(1\le i<m).
\]

They give (x_0=t^R), (x_i=1/t) for (i\ge1), and (t_i=t) at every index. In particular the extreme reset ratio and the cyclic weight constraint are compatible.

### The reset floor and strict product margin

Write (x=t^R) and (n=\lfloor1/(2\alpha x)\rfloor). The first threshold gives (x<1/(4\alpha)). For (z=1/(2\alpha x)>2), (\lfloor z\rfloor\ge z-1>z/2); hence

\[
\frac1{4\alpha x}<n\le\frac1{2\alpha x}.
\]

With reset degree one,

\[
N_0=1+x-\alpha nx>\tfrac12,
\quad 0<M_0=\alpha(1+nx)-1\le\alpha-\tfrac12<\alpha,
\]

so (A_0=nN_0/M_0>1/(8\alpha^2x)). At each buffer, (n_i=1,k_i=d,x_i=1/t), which gives (N_i=t^{-d}Q), (M_i=t^{-d}P), and (F_i=B^2). Therefore the source's exact product formula is correct:

\[
G=A_0B^{2m-1}=A_0B^R
>\frac{(B/t)^R}{8\alpha^2}>1.
\]

Both strict inequalities survive rounding (n) downward. No sign reversal or omitted reset factor occurs.

### The rational coefficient recipe

In the source's notation, take (K_i=n_iN_iQ/(PM_{i+1})), (q_0=1), and (q_{i+1}=K_iq_i/\delta) only for (0\le i\le m-2), with (q_m=q_0). The first (m-1) strict ratio conditions hold because (\delta>1). The final one holds precisely when

\[
\frac{G}{\delta^{m-1}}>1.
\]

Starting at (\delta=2) and repeatedly replacing it by (1+(\delta-1)/2) produces rational values strictly above one converging to one. Since (G>1), the stopping condition is reached after finitely many iterations. The midpoint choices for the source's (p_i) then lie strictly between their lower and upper bounds. When (t,\alpha) are rational, powers, floors, this recurrence, and the midpoint choices all preserve rationality. A real-valued target such as (d/(\ln d+2)) is legal directly; rationality of that endpoint is not asserted or needed.

### The all-(d\ge4) lower bound

For (D=\ln d), (t=D/d), elementary differentiation gives

\[
\ln(1+t)>t-t^2/2,
\qquad \sup_{d\ge1}\frac{(\ln d)^2}{2d}=\frac2{e^2}<\ln2.
\]

Consequently (y=(1+t)^d>d/2), and the positive numerator correction in (H_d(t)) gives

\[
H_d(t)>\frac1{t+1/y}>\frac{d}{\ln d+2}.
\]

The target factor (d/(\ln d+2)>1) for every integer (d\ge4). Therefore it satisfies the strict trigger, and the finite construction excludes an (\alpha)-PNE at that exact factor. The claim (a_*(d)\ge d/(\ln d+2)) follows without assuming the universal threshold infimum is attained. No mathematical gap was found in this derivation.

## 9. Independent check of the interface barrier

The barrier allows main degrees (k_i) and side degrees (D_i), all between one and (d). Put (z=\alpha^{1/d}>1) and (L=z-1). Its first implication is valid:

\[
N_i>0\Longrightarrow n_ix_i<(1+x_i)\alpha^{-1/k_i}
\le(1+x_i)/z.
\]

Because (n_i\ge1), this gives (x_i<1/L). Likewise (Q_i>0) gives (t_i>\alpha^{1/D_i}-1\ge L). Using the cyclic weight closure,

\[
\prod_i n_i
<\frac{\prod_i(1+x_i)}{z^m\prod_i x_i}
<\frac{(1+1/L)^m}{z^mL^m}=L^{-2m}.
\]

Both factor bounds used next are correct:

\[
M_i\ge(\alpha-1)(1+x_i)^{k_i},\qquad
N_i<(1+x_i)^{k_i},
\]

and, writing (y_i=(1+t_i)^{D_i}), (r_i=t_i^{D_i}),

\[
P_i-(\alpha-1)Q_i=y_i-r_i+\alpha(\alpha-1)>0.
\]

It follows that

\[
\prod_iF_i
<\frac{\prod_i n_i}{(\alpha-1)^{2m}}
<\big[(\alpha-1)(\alpha^{1/d}-1)\big]^{-2m}.
\]

Thus (G>1) forces ((\alpha-1)(\alpha^{1/d}-1)<1). Since (e^s-1\ge s), it also forces ((\alpha-1)\ln\alpha<d). For any fixed (\varepsilon>0), substitution of (\alpha=(1+\varepsilon)d/\ln d) violates this last inequality for sufficiently large (d). Combined with the construction's ((1-o(1))d/\ln d) lower factor, this proves the claimed leading constant one **within the coefficient-certificate mechanism**.

The qualification is indispensable. The barrier is not a universal equilibrium-existence theorem and does not rule out other state-covering arguments for the same resource topology. Section 5 gives a stronger conditional statement: if all light-forcing inequalities already hold, then beyond the barrier some hub inequality must fail and an all-opposite profile with a unique equal edge is an (\alpha)-PNE. Without the light-forcing premise, that conclusion has not been proved here.

## 10. Exact checks of the restored recipe

An additional independent `Fraction` calculation chose the least (R\equiv1\pmod4), (R\ge5), satisfying the equivalent rational tests (t^R<1/(4\alpha)) and ((B/t)^R>8\alpha^2). It then constructed all weights and all coefficient scales with the source's halving recipe and checked every strict coefficient inequality exactly.

| (d) | (t) | (\alpha) | (R) | (m) | Reset count (n) | Final (\delta) | Result |
|---:|---:|---:|---:|---:|---:|---:|---|
| 2 | 1/2 | 11/10 | 69 | 35 | 268316277435775296232 | 33/32 | All strict inequalities pass |
| 4 | 1/2 | 4/3 | 25 | 13 | 12582912 | 17/16 | All strict inequalities pass |
| 8 | 1/4 | 2 | 13 | 7 | 16777216 | 9/8 | All strict inequalities pass |

The weight identities and equality of the independently multiplied (\prod K_i) with (A_0B^R) also passed exactly. These checks deliberately avoid enumerating the enormous state spaces; sections 2–3 provide their full-state coverage. No external theorem or literature claim was imported into this review.

## 11. Saved reproducible verification and explicit PNE witnesses

The two originally executed inline audits have now been reconstructed into the standalone standard-library script `verify_state_review.py` in this directory and rerun from that saved file. It imports neither the original construction's verifier nor its attack scripts. Its literal evaluator builds every player's resource list and recomputes loads after each flip. The output `state_verification.json` records all parameters, exact rational values, the script SHA-256, full compressed rational amplifier games, and results.

Run from the repository root:

```bash
python tests/audits/weighted_congestion/odd_ring_linear_audit/verify_state_review.py
```

An optional `--output PATH` writes the same structured results elsewhere. The saved run reproduced the original 720 profiles, 1,912 matching-light bounds, and 74 all-opposite hub identities, and additionally counted 502 exact worst-state equalities. It reproduced all three amplifier constructions above and checked their 110 strict coefficient inequalities.

The saved script also adds 15 independent failed-edge witness cases: each edge of a three-vertex and five-vertex ring is made the sole failed hub inequality in turn; three cases place the selected hub inequality at exact equality; three use (\alpha=1); and one uses a one-vertex ring. Every case satisfies all strict light-forcing inequalities. The reusable function `unique_equal_edge_state(game, edge)` constructs the asserted (\alpha)-PNE, and direct costs verify every player's deviation at that state. The JSON contains each witness's bits, all parameters, and every exact current cost, deviation cost, and surplus.

All states of those 15 small witness games were also enumerated independently. For each state, literal player costs verified the characterization

\[
s\text{ is an }\alpha\text{-PNE}
\iff
\text{all lights oppose their hubs and every equal hub edge has }\Delta_i\le0,
\]

where (\Delta_i=n_iq_iQ_i-p_{i+1}M_{i+1}) is the hub surplus. This added audit covered 5,700 profiles and 54,664 unilateral deviations. The exact-equality cases confirm the closed (\alpha)-PNE boundary: a zero hub surplus does not exclude equilibrium. All assertions passed; these additional finite checks support, but do not replace, the general proof in section 5.


---
整理来源与当前文件用途见[逐文件登记](../../../weighted_congestion_frontier/FILES.md)。程序统一通过 `python3 tests/audits/weighted_congestion/replay.py --list` 选择；历史命令、输出摘要与源码哈希属于原冻结版本。
