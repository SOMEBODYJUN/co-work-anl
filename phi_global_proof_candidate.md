> **Historical research note (superseded navigation).** Preserve the derivation below as provenance; use [the current mathematical map](README.md), [claim registry](CLAIMS.md) and [source-status guide](PROVENANCE.md) for current scope.

# Candidate proof of the arbitrary-finite-instance golden-ratio theorem

**Status: complete proof candidate, internally audited; not externally peer reviewed.**

This document records the proof assembled in the present research round. It is a mathematical proof, not a numerical search or a restriction on the number of locations. The separate file `strong_cross_chord_arbitrary_n_proof.md` supplies the complete proof of the two-location mixed-equilibrium lemma used in Section 11. Every other prerequisite is stated and proved below. In particular, the earlier “common heavy customer theorem” is replaced here by an elementary argument, so it is not an external prerequisite.

## 1. Model and theorem

There is a finite set of customers (G), with weights (w_g>0), and a finite nonempty set (S) of locations available to **both** facilities. Customer (g) can use a specified subset of locations. Write

\[
C_s=\{g:g\text{ can use location }s\},\qquad R_s=\sum_{g\in C_s}w_g.
\]

The two facilities first choose locations, possibly the same location. Every customer covered by at least one chosen location then chooses one accessible facility. Customers independently randomize. A customer's expected cost conditional on choosing a facility is its own weight plus the expected weight of the other customers choosing that facility. A facility's payoff is its expected customer weight. Uncovered customers do not contribute to either payoff.

Put

\[
\phi=\frac{1+\sqrt5}{2},\quad q=\phi^{-1},\quad a=q^2=1-q,
\quad c=\phi/2.
\]

**Theorem (candidate).** There are pure facility locations and an exact customer Nash equilibrium after every facility-location profile such that no facility can improve its expected load by a factor greater than \(\phi\).

The theorem allows arbitrary finite numbers of locations and customers and arbitrary positive weights. It concerns existence of a suitable exact continuation selection; it does not assert the claim for every continuation selection.

## 2. Exact criterion and the closed-ring reduction

For an ordered layout \((s,t)\), let \(\mathcal N(s,t)\) be its set of independently mixed customer Nash equilibria and define

\[
m(s,t)=\min_{\sigma\in\mathcal N(s,t)}L_s(\sigma),\qquad
d(t)=\max_{s\in S}m(s,t).
\]

These extrema exist. The finite customer game has a pure equilibrium: the sum of squared facility loads strictly decreases under an improving pure move. Its mixed-equilibrium set is nonempty and compact, and expected loads are continuous.

**Exact criterion.** A \(\phi\)-approximate subgame-perfect equilibrium exists if and only if some layout \((u,v)\) has a customer equilibrium with

\[
L_u\ge qd(v),\qquad L_v\ge qd(u). \tag{2.1}
\]

Necessity holds because every continuation following a deviation to \(s\) against \(v\) gives the deviator at least \(m(s,v)\). For sufficiency choose the displayed on-path equilibrium and, after each unilateral off-path deviation, a customer equilibrium minimizing the deviating facility's load. Different unilateral deviation profiles are distinct labeled facility profiles, except for the original profile itself, so these choices do not conflict. Fill all other profiles with arbitrary exact equilibria.

Suppose no layout satisfies (2.1). Choose, with arbitrary tie breaking,

\[
b(t)\in\arg\max_s m(s,t)
\]

and let \(T\) be any directed cycle of this map. All uses of \(d\) below retain the maximum over the **full** location set \(S\). The cycle maximum \(M=\max_{s\in T}d(s)\) is positive: if \(M=0\), an equal-half co-location equilibrium at any cycle location already satisfies (2.1). Divide all weights and loads by \(M\), so

\[
\max_{s\in T}d(s)=1.
\]

**Scope convention.** Unless explicitly stated otherwise, every location quantified below belongs to \(T\). The value \(d(s)\) continues to maximize over the full set \(S\). In particular, all reach upper bounds and d-value upper bounds below are asserted for cycle locations, not for arbitrary locations outside the cycle. Section 11 is a standalone two-location lemma and states its own hypotheses.

Co-location at \(s\), with all covered customers independently choosing each facility with probability \(1/2\), gives load \(R_s/2\) on each facility. Thus failure of (2.1) implies

\[
d(s)>cR_s,\qquad R_s<2q\quad(s\in T). \tag{2.2}
\]

Let \(R=\max_{s\in T}R_s\). Since \(m(b(s),s)\le R_{b(s)}\) and \(b(T)\subseteq T\),

\[
1\le R<2q. \tag{2.3}
\]

For every edge \(s\to t=b(s)\), in **every** customer equilibrium write \(P=L_t\), \(Q=L_s\). Then

\[
P\ge d(s)>cR_s,\qquad Q<qd(t)\le q. \tag{2.4}
\]

Indeed, the responder already exceeds its stability threshold \(qd(s)\); if the incumbent reached \(qd(t)\), (2.1) would hold.

## 3. Pure repair, leveling, and a reach bound for d

### 3.1 Pure repair

The repair operation follows Vos (2023 thesis, Lemma 29); we record the load bounds used later.

Suppose a pure assignment has loads \(A<B\), and each common customer currently at the lower-load facility has weight at least \(B-A\). Repeatedly move a largest-weight improving customer from the originally higher-load facility to the originally lower-load facility. Stop if no such customer exists, or at the first reversal of the load order.

An improving move of weight \(w\) satisfies \(w<B'-A'\), and both new loads lie strictly between the old loads. Before the first reversal the gap decreases. The moved weights are nonincreasing: a customer too heavy to improve cannot become improving while the gap decreases. At the first reversal the new gap is less than the last moved weight; all previously moved customers and all customers originally at the lower side are at least this heavy. Hence the resulting profile is a pure equilibrium. The originally lower side finishes at least at \(A\), and strictly below \(B\); the originally higher side finishes strictly above \(A\).

We also use arbitrary finite pure improvement sequences when both loads already exceed a desired common lower bound. Each improvement keeps both loads inside the previous load interval, so this lower bound is preserved.

### 3.2 Leveling equilibria

This definition and the next two properties are from Vos (2023 thesis, Definition 8.4 and Lemmas 30--31). They are background; the final contradiction does not require a fixed leveling continuation.

For two unequal reaches, select a pure equilibrium maximizing the load of the lower-reach location. For equal reaches, independently split every common customer equally; the private totals are equal, so this is an equilibrium with equal loads.

For unequal reaches the selected pure equilibrium has two properties:

1. The common weight assigned to the lower-reach location is at least that assigned to the higher-reach location.
2. Either the lower-reach facility gets its entire reach, or the higher-reach facility's load is strictly below the lower reach.

For (1), let private weights be \(A<B\), and common weights assigned to the low- and high-reach locations be \(S<T\). The equilibrium gap is \(\Delta=B-A+T-S>0\), so every common customer at the high-load side has weight at least \(\Delta\). Swap the two common sets. The new absolute gap is \(|B-A-(T-S)|<\Delta\). The swapped profile is already an equilibrium if the low-reach side now has the higher load; otherwise the repair lemma applies. Either case increases the low-reach load, contradicting the selection rule.

For (2), put all common customers at the lower-reach location. If its load is no larger than the other load, this is an equilibrium. Otherwise repair, starting with the other location having no common customers. The resulting high-reach load is strictly below the lower reach. The leveling choice minimizes that high-reach load among pure equilibria.

### 3.3 A useful bound on d

\[
R_s\ge q\quad\Longrightarrow\quad d(s)\le R_s. \tag{3.1}
\]

To prove this, suppose \(d(s)>R_s\), and put \(t=b(s)\). Let \(E=w(C_t\setminus C_s)\). If \(E\le R_s\), assign all common customers to \(s\). Either this is an equilibrium or pure repair gives an equilibrium with responder load at most \(R_s\), contradicting \(m(t,s)=d(s)\). Consequently \(E>R_s\). Every common customer then strictly prefers \(s\): its cost there is at most \(R_s\), whereas choosing \(t\) costs at least \(E+w_g\). Thus all equilibria coincide, with responder load \(E=d(s)\) and incumbent load \(R_s\). Equation (2.4) forces \(d(t)>\phi R_s\), and hence \(R_s<q\). This proves (3.1).

The same argument gives the following return rule: if \(d(s)>R_s\), the edge from \(s\) has a unique customer equilibrium, the incumbent receives \(R_s\), and the next d-value exceeds \(\phi R_s\).

## 4. No visible customer has weight at least q

Suppose a customer of weight \(H\ge q\) is visible at a location of \(T\). Whenever its current location is \(s\), (2.4) forces it to remain accessible at \(b(s)\), since otherwise the incumbent load would be at least \(H\ge q\). It therefore covers the entire cycle.

For any edge \(s\to t\), let \(S_{st}\) be the total weight of its common customers other than this customer. If

\[
R_t\ge R_s-S_{st},
\]

assign the heavy customer to \(s\) and all other common customers to \(t\). The loads are

\[
Q=R_s-S_{st}\ge H,\qquad P=R_t-H<H\le Q,
\]

where \(R_t<2q\le2H\). The heavy customer is stable because \(Q-H\le P\), equivalently \(Q\le R_t\); the other common customers choose the lower-load side and are stable. This pure equilibrium contradicts \(Q<q\) in (2.4). Thus every edge satisfies

\[
R_t<R_s-S_{st}\le R_s,
\]

which is impossible on a cycle. Therefore

\[
w_g<q\quad\text{for every customer visible on }T. \tag{4.1}
\]

## 5. Heavy pairs: size, avoidance, and a chord lemma

Call a customer **large** if \(w_g>\tau=q/2\), and put

\[
\mathcal H_s=\{g\in C_s:w_g>\tau\}.
\]

### 5.1 At most two large customers at a location

In a pure equilibrium of an edge, two large customers belonging to the source cannot both be assigned to the responder. If they were, with source reach \(r\), then \(Q<r-q\). Both transferred common customers have weight at least \(P-Q\), so

\[
2P\le r+Q<2r-q.
\]

Together with \(2P>\phi r\), this gives \((2-\phi)r>q\), hence \(r>\phi\), contradicting \(r<2q<\phi\).

If a source covered three large customers, \(Q<q\) would force at least two of them to the responder. An equal-reach edge cannot avoid this argument by being mixed: its equal-half equilibrium has equal loads, each at least \(d(s)>\phi R_s/2>3/4>q\), again contradicting (2.4). A pure equilibrium exists in the unequal-reach case. Consequently

\[
|\mathcal H_s|\le2. \tag{5.1}
\]

### 5.2 Avoidance of a large pair

If \(s\) contains two large customers and \(t\) contains neither, then

\[
R_t<qd(s)\le q. \tag{5.2}
\]

The exclusive weight of \(s\) against \(t\) is \(A>q\). Put all common customers at \(t\). If \(R_t\le A\), this is a pure equilibrium with loads \(A,R_t\). If \(R_t>A\), repair gives both loads at least \(A>q\). Hence \(R_t\ge qd(s)\) would satisfy both thresholds in (2.1).

In particular, all large pairs that occur on \(T\) intersect pairwise.

### 5.3 Chord retaining exactly one member of a pair

Suppose \(s\) has large customers \(h,j\), \(t\) contains \(h\) but not \(j\), and \(R_s\le R_t\). Let \(H=w_h,J=w_j\). Assign \(h\) to \(s\) and all other common customers to \(t\). If their other-common total is \(\sigma\), the loads are

\[
U=R_s-\sigma\ge H+J>q,\qquad V=R_t-H.
\]

The customer \(h\) is stable since \(U-H\le V\). If \(V\le U\), this is a pure equilibrium. If \(V>U\), then

\[
V-U\le R_t-2H-J<H,
\]

because \(R_t<2q<3H+J\). Repair then gives both loads above \(q\), a contradiction. Thus the first case must hold, and absence of stability forces

\[
d(s)>\phi(R_t-H). \tag{5.3}
\]

In particular, a pair-source best response cannot have at least the source reach while retaining exactly one member of that pair: the constructed equilibrium has incumbent load above \(q\), while every equilibrium has responding load at least \(d(s)\).

## 6. Capacity of a location containing a large pair

If \(\mathcal H_s=\{h,j\}\), then

\[
R_s<q+\max(H,J). \tag{6.1}
\]

First let \(r=R_s\ge1\). Equal reaches on its edge are impossible by (2.4). In a pure equilibrium, if two or more common customers went forward, then \(2P\le r+Q<r+q\), while \(2P>\phi r\); this would imply \(r<1\). Therefore exactly one common customer goes forward. Since the two large customers cannot both remain at the incumbent, the transferred customer is one of them, say of weight \(H\). Then \(r-H=Q<q\), proving (6.1).

Now suppose \(r<1\) but \(r\ge q+\max(H,J)\). Then \(r>3q/2\) and \(P>\phi r/2>3/4\). Exactly one of the two large customers goes forward, say \(H\), and the other \(J\) remains. If the responder also covered \(J\), it would have the same pair. If its reach were at least one, the already proved case would give its reach \(<q+\max(H,J)\le r<1\), impossible. If its reach were below one, its load would be \(<1-J<1-q/2<3/4\), also impossible. Thus \(J\) is inaccessible to the responder.

Reassign only \(H\) forward and all other common customers to the incumbent. Let their total be \(\sigma\); the loads are

\[
Q_0=r-H\ge q,\qquad P_0=R_{b(s)}-\sigma,
\]

and

\[
\sigma\le r-H-J,\qquad P_0\ge d(s)-r+H+J.
\]

The original equilibrium condition for \(H\) implies \(P_0\le r\), so \(H\) is still stable. If \(P_0\ge Q_0\), the new profile is a pure equilibrium, contradicting (2.4). If \(P_0<Q_0\), then

\[
Q_0-P_0<(2-\phi/2)r-2H-J<H,
\]

using \(r<1\) and \(3H+J>2q>2-\phi/2\). Repair produces a responder load strictly below \(Q_0\). But

\[
Q_0=r-H<\phi r/2<d(s),
\]

since \(H>q/2>ar/2\). This contradicts the definition of \(d(s)=m(b(s),s)\), proving (6.1).

## 7. No edge connects two locations with the same large pair

Let two locations have the same pair of weights \(H\ge J>q/2\). Write their private weights as \(A\le B\), the total of other common customers as \(W\), and label their reaches \(r_\ell\le r_h\). Thus

\[
r_\ell=A+H+J+W,\qquad r_h=B+H+J+W.
\]

Set \(D=B-A+W\). Capacity gives

\[
0\le D\le B+W=r_h-H-J<q-J<J\le H.
\]

Assign all common customers other than the large pair to the higher-reach location. Let each large customer of weight \(w\in\{H,J\}\) choose the lower-reach location with probability \((1+D/w)/2\). This is an equilibrium: both large customers are indifferent and all other common customers choose the lower expected-load side. Its loads are

\[
L_h=r_\ell-W-(H+J)/2,\qquad L_\ell=r_h-(H+J)/2.
\]

In either possible orientation as source and responder, the responder load is at most

\[
R_{\rm source}-(H+J)/2<cR_{\rm source}<d({\rm source}).
\]

Here \(H+J>q>aR_{\rm source}\), because \(R_{\rm source}<2q\) and \(2aq<q\). This contradicts a best-response edge. Hence

\[
\boxed{\text{No b-edge joins two locations with the same large pair.}} \tag{7.1}
\]

The same capacity proof also shows the selected source-to-responder pure allocation cannot keep both large customers at the responder; Section 5 already provides the sharper version needed elsewhere.

## 8. The large-pair family is a star

Let \(\mathcal E=\{\mathcal H_s:|\mathcal H_s|=2\}\). Its members pairwise intersect by (5.2). A pairwise-intersecting family of two-element sets either has a common member or contains exactly the three pair types of a triangle. Suppose such a triangle occurs, on customers \(h,j,k\).

Every location of reach at least \(q\) must meet all three pair types, by (5.2). By (5.1) its own large set is therefore one of the triangle pairs. Choose a maximum-reach location \(A\), of reach \(R\ge1\), and suppose it has pair \(\{h,j\}\).

Both \(H\) and \(J\) exceed \(a\). For example, if \(H\le a\), choose another triangle-pair location containing \(h\) but not \(j\). Apply Section 5.3 with \(A\) as the higher-reach endpoint. Its load \(R-H\ge1-a=q\), and the other endpoint's load exceeds \(q\); either the displayed profile or repair is stable, a contradiction.

Every pair location \(s\) has \(d(s)>q\). Otherwise (2.2) gives \(R_s<2a\). It cannot have the same pair as \(A\), whose two weights exceed \(a\). If it has another triangle pair, sharing \(g\) with \(A\), then \(w_g<q\), so

\[
R-w_g>1-q=a\ge qd(s).
\]

Section 5.3 again constructs a stable equilibrium, a contradiction.

Thus pair locations form a nonempty b-closed subset: their responders have reach at least their d-value, hence above \(q\), and so must again be pair locations. An edge to a different pair cannot weakly increase reach by Section 5.3. An edge to the same pair is impossible by (7.1). Hence every edge in this finite closed subset strictly decreases reach, a contradiction. The triangle is impossible, proving

\[
\mathcal E\ne\varnothing\quad\Longrightarrow\quad\bigcap_{E\in\mathcal E}E\ne\varnothing. \tag{8.1}
\]

## 9. Common-h chords, transport, and two-anchor covering

The rest of the proof repeatedly uses a customer \(h\), of weight \(H\), satisfying

\[
H>aR,\qquad K:=R-H<q,\qquad H<q. \tag{9.1}
\]

In particular \(R<3H\).

### 9.1 An upward common-h chord

For locations \(s,t\) containing \(h\) and \(R_s\le R_t\), assign \(h\) to \(s\) and all other common customers to \(t\). Their loads are

\[
U=R_s-\sigma\ge H,\qquad V=R_t-H.
\]

The customer \(h\) is stable. If \(V\le U\), the profile is an equilibrium. If \(V>U\), then \(V-U\le R-2H<H\), so repair applies and the final load at \(t\) is at most \(V\). Therefore

\[
m(t,s)\le R_t-H\le K. \tag{9.2}
\]

### 9.2 A common-h edge with d above q has unique transport

Suppose \(s\to t\), both contain \(h\), and \(d(s)>q\). Equation (9.2) first implies \(R_t<R_s\). Take a pure equilibrium. If \(h\) stayed at the source, responder load would be at most \(R_t-H\le K<q\), impossible. If another common customer accompanied \(h\) forward, their equilibrium conditions would give

\[
2P\le R_s+Q\le2R_s-H,
\]

so \(P\le R_s-H/2<cR_s<d(s)\), using \(H>aR\ge aR_s\). Thus \(h\) is the only common customer going forward.

Let \(\sigma\) be the other-common total, and \(\Delta=R_s-R_t>0\). The pure loads are \(Q=R_s-H\), \(P=R_t-\sigma\), with \(\sigma<R-q<H\). If \(\sigma\ge\Delta\), the reverse assignment, placing \(h\) at the source and all other common customers at the responder, would be a pure equilibrium with responder load \(R_t-H\le K<q\), impossible. Consequently \(\sigma<\Delta\).

This last inequality makes \(h\) strictly prefer the responder regardless of other choices: its minimum source cost is \(R_s-\sigma>R_t\). Given this choice, every other common customer strictly prefers the source, whose maximum load is \(R_s-H\le K<q\), below the responder's minimum load \(R_t-\sigma\ge d(s)>q\). Thus **all**, including mixed, customer equilibria coincide, and

\[
d(s)=R_t-\sigma,\quad Q=R_s-H,\quad 0\le\sigma<R_s-R_t. \tag{9.3}
\]

### 9.3 General two-anchor covering lemma

The overlap-counting method has a precursor in Vos (2023 thesis, Theorem 19); the present version uses full-game deviation guarantees and is applied to an arbitrary closed cycle.

Suppose an edge \(X\to Y\) has the unique transport (9.3). Write

\[
x=R_X>y=R_Y,\quad \delta=d(X)=y-\sigma,\quad \varepsilon=d(Y),
\quad B=\phi(y-H).
\]

Assume

\[
\delta>B,\quad \varepsilon>B,\quad \delta>\phi H,\quad \varepsilon\le y. \tag{9.4}
\]

Then there is no h-containing location \(t\) with

\[
B<R_t\le y,\qquad d(t)\le B. \tag{9.5}
\]

For each anchor \(i\in\{X,Y\}\), assign \(h\) to \(t\) and the other common customers to \(i\). If their total \(\sigma_{it}\) satisfied \(\sigma_{it}\le R_t-qd(i)\), the initial loads would be

\[
U_t=R_t-\sigma_{it}\ge qd(i),\qquad V_i=R_i-H\ge y-H=qB\ge qd(t).
\]

The customer \(h\) is stable since \(R_t\le R_i\). If \(V_i\le U_t\), this is an equilibrium. Otherwise repair applies because \(R<3H\); both final loads are at least \(U_t\), which exceeds both required thresholds because \(d(i)>B\ge d(t)\). Thus no solution forces

\[
\sigma_{Xt}>R_t-q\delta,\qquad \sigma_{Yt}>R_t-q\varepsilon.
\]

Their intersection, excluding \(h\), has weight at most \(\sigma\), so

\[
\sigma_{Xt}+\sigma_{Yt}\le R_t-H+\sigma.
\]

It follows that

\[
R_t<L:=q(\delta+\varepsilon)-H+\sigma.
\]

But

\[
B-L=\delta-q\varepsilon+q\sigma-qH
\ge a\delta-qH>0,
\]

where only \(\varepsilon\le y=\delta+\sigma\) is used. Hence \(R_t<B\), contradicting (9.5). No assumption \(\varepsilon\le\delta\) is needed.

## 10. Abstract center theorem and nondegenerate stars

### 10.1 Abstract center theorem

Under (9.1), suppose every location without \(h\) has reach at most \(\phi H\). Then the no-solution closed cycle is impossible.

First, every h-containing location has \(d(s)>H\). Suppose instead \(u\) contains \(h\) and \(d(u)\le H\). Then \(R_u<2qH<\phi H\). For any \(t\) with \(R_t>\phi H\), the assumption makes \(t\) an h-location. If \(d(t)\le\phi H\), put \(h\) at \(u\) and other common customers at \(t\). The loads satisfy \(U\ge H\ge qd(t)\) and \(V=R_t-H>qH\ge qd(u)\). The common-h chord construction, with repair if necessary, gives stability. Thus all locations of reach above \(\phi H\) have d-value above \(\phi H\). This set is nonempty since \(R\ge1>\phi H\), and it is b-closed. It consists entirely of h-locations. On it (9.2) forbids every nondecreasing-reach edge, since \(K<q<\phi H\), a contradiction.

If \(u\to v\) leaves \(h\), (2.4) gives

\[
d(v)>\phi H\ge R_v.
\]

The return rule of Section 3.3 makes the next edge's equilibrium unique. Its target \(w\) has reach at least \(d(v)>\phi H\), hence contains \(h\), and

\[
d(w)>\phi R_v\ge\phi d(u)>\phi H. \tag{10.1}
\]

Choose an h-location \(X\) maximizing d among h-locations, and put \(\delta=d(X)\). We have \(\delta>cR\), since the maximum-reach location contains \(h\), and \(\delta>\phi H\): if there is an exit, use (10.1); otherwise all locations contain \(h\), so \(\delta=1>\phi H\). The responder \(Y=b(X)\) contains \(h\); otherwise (10.1) would produce an h-location with d exceeding \(\phi\delta>\delta\).

Since \(\delta>\phi H>q\), Section 9.2 applies. Use its notation \(x,y,\sigma,\varepsilon\). Set \(B=\phi(y-H)\). Then \(\varepsilon>\phi(x-H)>B\). Since \(\varepsilon\le\delta\), we also have \(x<H+q\delta\) and hence \(B<\delta\). Moreover \(B>K\): if \(H\le R/2\), use \(y\ge\delta>cR\); if \(H\ge R/2\), use \(y\ge\delta>\phi H\), which gives \(B>H\ge K\). The covering lemma applies because \(y>q\) and hence \(\varepsilon\le y\).

Starting at \(Y\), as long as the path remains among h-locations with d above \(B\), (9.2) forces strictly decreasing reach. A first h-location with d at most \(B\) would still have reach above \(B\) and at most \(y\), contradicting Section 9.3. The path must therefore leave \(h\). At that exit its source has d above \(B\); (10.1) gives a returning h-location with d above \(\phi B\). But

\[
\phi B-\delta
=\phi(\delta-\phi H)+\phi^2\sigma>0,
\]

contradicting the choice of \(\delta\). This proves the abstract center theorem.

### 10.2 Nondegenerate stars satisfy its assumptions

Suppose \(\mathcal E\) contains at least two distinct pairs, with unique common customer \(h\). Every location of reach at least \(q\) contains \(h\): otherwise it must meet two different pairs by covering their two leaves, producing the triangle already excluded in Section 8. Thus every no-h reach is below \(q\).

Apply the maximum-reach first-edge argument of Section 12.1 below (that argument itself does not assume an empty or single-pair family). It gives a unique forward customer \(g\) on \(A\to b(A)\), of weight exceeding \(R-q\), and other-common weight

\[
\sigma<R-cR=aR/2<aq=q^3<q/2.
\]

Both endpoints have reach above \(q\), so both contain the star center \(h\). If \(g\ne h\), the weight of \(h\), which exceeds \(q/2\), would be included in \(\sigma\), impossible. Thus \(g=h\), and \(H>R-q\ge aR\), while \(H<q\) by Section 4. In particular \(\phi H>q\). All no-h reaches are below \(q<\phi H\), and the abstract center theorem rules out this case for arbitrary cycle length.

## 11. Strong cross-chord lemma for arbitrarily many common customers

The complete proof is in the companion file `strong_cross_chord_arbitrary_n_proof.md`, Sections 1–5, including the exact mixed-equilibrium coordinates, maximum-square section construction, all positive and negative gap cases, and the finite pure repairs. The statement used below is:

**Strong cross-chord lemma.** Consider two locations with reaches \(U\ge V>cU\). Let \(C\) be the total common-customer weight. If

\[
C<qV,\qquad \max_{g\text{ common}}w_g\le aU,
\]

then there is an independently mixed customer Nash equilibrium with

\[
L_U\ge qV,\qquad L_V\ge qU. \tag{11.1}
\]

There is no restriction on the number of common customers. The proof must allow three or more customers to mix; reducing to pure or two-mixer equilibria is invalid.

The companion proof also establishes the sharper exact characterization, not required for the final theorem: under \(U\ge V>cU\) and \(C<qV\), let \(x\) be the largest common weight. An equilibrium satisfying (11.1) exists if and only if

\[
x\le U-qV\quad\text{or}\quad C-x\ge U-V.
\]

When both inequalities fail, the customer game has a unique equilibrium: the largest common customer strictly chooses the lower-reach location and every other common customer strictly chooses the higher-reach location. Its loads are \(U-x,V-(C-x)\), and it fails the first target.

## 12. The first edge and selection of a single-large-customer anchor

Section 12.1 is a general first-edge lemma, valid for every large-pair family; its forward use in Section 10.2 has no dependency on the conclusions of that section. From Section 12.2 onward, only \(\mathcal E=\varnothing\) or \(\mathcal E=\{\{h,j\}\}\) remains after Section 10. In this section “h-only” means that \(h\) is the location's only **large** customer; it may have any number of small customers.

### 12.1 The maximum-reach first edge

Choose \(A_0\) of reach \(R\), and put \(A_1=b(A_0)\). Equation (2.4) gives responder load \(P\ge d(A_0)>cR\) and incumbent load \(Q<q\). An equal-reach responder is impossible because the equal-half equilibrium has \(P=Q\). Thus \(R_1<R\), and take a pure equilibrium.

There must be at least one common customer assigned forward, since otherwise \(Q=R\ge1\). If at least two went forward, their equilibrium conditions would give

\[
2P\le R+Q<R+q,
\]

which, with \(2P>\phi R\), would imply \(R<1\). Therefore exactly one customer \(h\) goes forward. Its weight is

\[
H=R-Q>R-q\ge aR>q/2. \tag{12.1}
\]

Section 4 gives \(H<q\), so (9.1) holds. If \(\sigma_0\) is the other-common weight, then \(P=R_1-\sigma_0>q\), so \(\sigma_0<R-q<H\). As in Section 9.2, \(\sigma_0\ge R-R_1\) would make the reverse pure assignment an equilibrium with responder load \(R_1-H<K<q\). Therefore \(\sigma_0<R-R_1\), all equilibria coincide, and

\[
d(A_0)=R_1-\sigma_0,\qquad d(A_1)>\phi(R-H)=\phi K. \tag{12.2}
\]

If there is a unique large pair, \(h\) belongs to it. Indeed, a maximum-reach location must meet that pair by (5.2); the presence of a different large customer would create another pair.

### 12.2 A high h-only anchor always exists

If \(A_0\) is h-only, use it. Otherwise it has the unique pair, so \(A_1\) is h-only by (7.1), since it contains \(h\). In either case an h-only location \(Z\) has reach

\[
R_Z>cR. \tag{12.3}
\]

### 12.3 The case H at least R/2

Suppose \(H\ge R/2\). Use the h-only anchor \(Z\) above, with reach \(z\). If any no-h location \(t\) had reach \(r_t>\phi H\), then

\[
r_t>cz,\qquad z>cR\ge cr_t.
\]

Its common weight with \(Z\) satisfies

\[
C\le z-H\le H<qr_t,\qquad C\le z/2<qz.
\]

Every common customer is small, with weight at most \(q/2<a z\), because \(z>cR\ge c\) and \(ac=q/2\). Both reaches exceed \(c^2R>q\). Apply Section 11 and then (3.1): the resulting loads meet \(qd(t)\) and \(qd(Z)\), giving stability.

Thus every no-h reach is at most \(\phi H\), and the abstract center theorem gives a contradiction. This rules out \(H\ge R/2\).

### 12.4 Selecting consecutive anchors when H is below R/2

Henceforth \(H<R/2\). By (12.2),

\[
d(A_1)>\phi K>cR. \tag{12.4}
\]

If \(A_1\) is h-only, select \(X=A_0,Y=A_1\).

The only other possibility is that \(A_0\) is h-only and \(A_1\) has the unique pair. Let \(A_2=b(A_1)\). If \(A_2\) lacked \(h\), then

\[
R_2\ge d(A_1)>\phi K>cR.
\]

The common weight between \(A_0\) and \(A_2\) is at most \(K<qR_2\), and all these common customers are small because \(A_0\) is h-only. Their weights are at most \(q/2<aR\). The strong cross-chord lemma gives stability, using (3.1) at both endpoints, a contradiction. Therefore \(A_2\) contains \(h\). Equation (7.1) makes it h-only. Since \(d(A_1)>q\), Section 9.2 gives unique h-transport along \(A_1\to A_2\). Select \(X=A_1,Y=A_2\).

In either selection, write

\[
x=R_X>y=R_Y>cR,\quad \delta=d(X)=y-\sigma>cR>\phi H,
\quad \varepsilon=d(Y).
\]

The selected edge has unique h-transport, \(0\le\sigma<x-y\), and \(Y\) is h-only. Furthermore

\[
y>\phi K. \tag{12.5}
\]

For \(Y=A_1\), this follows from \(d(A_1)>\phi K\) and \(d(A_1)\le R_1\). For \(Y=A_2\), it follows from \(R_2\ge d(A_1)>\phi K\). The use of (3.1) in the first case is valid because \(R_1>cR>q\).

## 13. Final two-anchor closure for the empty and single-pair cases

Use \(X,Y,x,y,\delta,\varepsilon,\sigma\) from Section 12.4, and set

\[
B=\phi(y-H).
\]

The edge inequality gives \(\varepsilon>\phi(x-H)>B\). Also \(\varepsilon\le y\) by (3.1), so \(x<H+qy\). Therefore

\[
\delta=y-\sigma>2y-x>(2-q)y-H>B,
\]

where the last difference is \(q(H-ay)>0\). Finally, (12.5) gives

\[
B-K>\phi(R-2H)>0. \tag{13.1}
\]

Thus all assumptions (9.4) of the two-anchor covering lemma hold.

If \(H\ge y/2\), any no-h location of reach above \(\phi H\) forms a stable strong cross-chord with the h-only anchor \(Y\), exactly as in Section 12.3: both reach ratios exceed \(c\), common weight is below \(q\) times either reach, and common weights are at most \(q/2<a y\). Hence all no-h reaches are at most \(\phi H\), and the abstract center theorem is a contradiction.

It remains that \(H<y/2\). Now

\[
B>cy>c^2R>q. \tag{13.2}
\]

Any no-h location \(t\) with reach \(r_t>B\) forms a stable strong cross-chord with \(Y\). Indeed,

\[
r_t>cy,\qquad y>cR\ge cr_t,
\]

and, since \(H>aR\ge ay\),

\[
C(Y,t)\le y-H<qy,\qquad C(Y,t)\le y-H<qr_t.
\]

All common customers are small, with weight at most \(q/2<a y\). Both reaches exceed \(q\), so (3.1) upgrades the cross-chord reach thresholds to the exact global d-thresholds. Thus no solution forces

\[
h\notin C_t\quad\Longrightarrow\quad R_t\le B. \tag{13.3}
\]

Start at \(Y\), which has \(d(Y)>B\), and follow \(b\). As long as a source has d above \(B\), its responder has reach at least that d-value and hence above \(B\). By (13.3) it contains \(h\). An h-to-h edge with d above \(B>K\) strictly decreases reach by (9.2).

If the path never encountered a d-value at most \(B\), this would give strict reach descent around a finite closed cycle. Otherwise let \(t\) be the first such location. Its reach is above \(B\), because the preceding source has d above \(B\), and is at most \(y\), by the preceding strict decreases. It contains \(h\), and \(d(t)\le B\). This contradicts the two-anchor covering lemma, Section 9.3.

The empty-pair and single-pair cases are impossible. The nondegenerate-star case was ruled out in Section 10, and Section 8 excludes all other pair families. Thus the no-solution assumption is false. The exact criterion in Section 2 supplies the desired \(\phi\)-approximate subgame-perfect equilibrium.

## 14. Audit checklist and scope

The proof uses full-game d-values throughout. No favorable tie breaking for \(b\) is assumed. No bound on the number of locations, the length of a best-response cycle, or the number of common customers is imposed. The strong cross-chord proof explicitly permits arbitrary independently mixed customer equilibria and does not aggregate distinct small customers into a splittable mass.

Internal adversarial audits checked the companion strong cross-chord proof, the normalized inequality \(c^2>q\), the no-heavy-customer argument in Section 4, and the exact labeled-profile continuation construction in Section 2. External mathematical peer review remains outstanding. The proof does not depend on the earlier computer-assisted four-location result.
