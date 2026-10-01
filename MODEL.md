# Model, quantifiers, and notation

This file fixes the objects shared by the research branches. A changed catalog, participation rule, cost function, or continuation concept creates a **different claim**. The graph nodes in [`research/graph.json`](research/graph.json) refer to these definitions by ID.

## M1. Two-stage incidence game

Let $I$ be a finite set of $n$ *atomic* customers, with positive weights $w_i$. A finite set of physical sites $V$ has customer-reach sets $C_s\subseteq I$. Facilities 1 and 2 have nonempty finite allowed sets $U_1,U_2\subseteq V$. They choose labeled locations $(s,t)\in U_1\times U_2$ simultaneously. A site available to both may be selected by both; the two facilities remain distinct. An incidence family includes the graph-neighborhood model of the cited paper, but some incidence inputs need not correspond to its particular host-graph convention.

At a fixed layout, a customer covered by neither facility has no action and contributes zero. A customer covered by exactly one must patronize it; one covered by both must patronize one of them. There is **no exit option for a covered customer**. Each customer's cost is the expected *realized total customer weight at the facility it chooses*, including its own weight. Each facility's payoff is its expected served customer weight. Customers choose independently; their Nash continuations may be mixed.

The **shared-catalog** restriction is $U_1=U_2=S\ne\varnothing$. The **heterogeneous-catalog** model permits unequal and even disjoint $U_1,U_2$. The latter contains the former as a class, but a lower-bound family with unequal sets is not a lower bound within the shared class.

## M2. Local customer equilibrium

At a labeled pair $(s,t)$, let $A=w(C_s\setminus C_t)$, $B=w(C_t\setminus C_s)$, and list the $k$ distinct common customers with weights $(w_1,\ldots,w_k)$. Customer $i$ chooses facility 1 with probability $p_i\in[0,1]$. Write

$$
 x=A+\sum_i w_ip_i,\qquad y=B+\sum_i w_i(1-p_i),\qquad
 V=A+B+\sum_iw_i,\qquad \Delta=x-y.
$$

The two conditional costs to customer $i$ differ by

$$
 \operatorname{cost}_1(i)-\operatorname{cost}_2(i)
 =\Delta+w_i(1-2p_i).
$$

Therefore an **exact independent mixed customer NE** satisfies

$$
 p_i=1\Rightarrow\Delta\le w_i;\quad
 p_i=0\Rightarrow\Delta\ge-w_i;\quad
 0<p_i<1\Rightarrow\Delta=w_i(2p_i-1).\tag{NE}
$$

This is an exact equivalence, not a necessary-only relaxation. In particular, a declared mixer at an endpoint may duplicate a pure action without making an invalid NE. Define $c_i=w_i(2p_i-1)$; then $\Delta=A-B+\sum_i c_i$. The one-mixer support can form a *closed interval* of feasible gaps, whereas zero or at least two designated mixers yield a point after support conditions are imposed. See [`math/LOCAL_GAME.md`](math/LOCAL_GAME.md).

## M3. Continuation selection and approximation

A full continuation rule assigns **one** exact local customer NE to every labeled $(s,t)\in U_1\times U_2$. Different layouts may use different equilibria. At an on-path layout $(s,t)$ with loads $(x,y)$, it is an $\alpha$-approximate pure-location SPE, $\alpha\ge1$, if each legal unilateral deviation gives its mover at most $\alpha x$ or $\alpha y$, respectively. A unilateral move by facility 1 to $r\in U_1\setminus\{s\}$ reaches $(r,t)$; a move by facility 2 to $r\in U_2\setminus\{t\}$ reaches $(s,r)$. These labeled off-path families do not conflict. Equilibrium *selection* is existential; no theorem here asserts stability under every possible customer continuation.

For arbitrary catalogs, set

$$
 m_1(s,t)=\min_{e\in\mathrm{NE}(s,t)}L_1(e),\quad
 m_2(s,t)=\min_{e\in\mathrm{NE}(s,t)}L_2(e),
 \quad D_1(t)=\max_{r\in U_1}m_1(r,t),\quad D_2(s)=\max_{r\in U_2}m_2(s,r).
$$

Because local NE sets are nonempty and compact here, the minima are attained. A specified on-path NE can be extended to an $\alpha$-SPE **if and only if** $D_1(t)\le\alpha x$ and $D_2(s)\le\alpha y$: choose an attaining minimum separately after each actual unilateral deviation, and fill other layouts with any exact NE. Including the on-path action inside $D_j$ adds no condition because $(m_j(s,t)\le L_j(s,t)\le\alpha L_j(s,t))$.

This exact criterion is mathematically useful but computing its $m_j$ is weakly NP-hard in general under binary weights. The shared-catalog polynomial candidate uses a *different* object: a fixed finite menu $F(s,t)\subseteq\mathrm{NE}(s,t)$, $u(s,t)=\min_{e\in F(s,t)}L_s(e)$, and $d_F(t)=\max_{s\in S}u(s,t)$. Thus $m(s,t)\le u(s,t)$, with equality **not** asserted. Its menu quota criterion is sufficient; it is not claimed necessary for every SPE. Neither $D_j$ nor $d_F$ may be silently restricted to locations on a chosen response cycle.

## M4. Input and theorem scope

The existence arguments are stated for positive real weights. Claimed bit-polynomial algorithms assume **explicit incidence and positive binary rational weights**, with $N_j=|U_j|$ and total input bit length $L$. Their displayed $O(\cdot)$ bounds count exact rational arithmetic operations; the proof must separately bound intermediate bit lengths. Numerical experiments and exact certificates for finitely many inputs cannot establish these universal bounds.

Primary sources for the model and published baseline: [Krogmann et al., IJCAI 2024](https://www.ijcai.org/proceedings/2024/0315.pdf); the integrated shared draft is [`manuscripts/shared_phi/main.tex`](manuscripts/shared_phi/main.tex), and the heterogeneous draft is [`manuscripts/heterogeneous/main.tex`](manuscripts/heterogeneous/main.tex). Their theorem claims remain internal research drafts.
