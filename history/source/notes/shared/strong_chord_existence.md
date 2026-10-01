# Arbitrary finite shared-client cross-chord lemma

Research proof checkpoint, 2026-09-29. The proof below is independent of a global facility cycle. Its application to a cycle must be checked separately. The construction, exchange steps, all mixed-support branches, and boundary cases were independently audited by the pair, core, and triangle agents.

## Statement

Let \(q=(\sqrt5-1)/2\), \(a=q^2=1-q\). Consider two locations with reaches \(R\ge r>\phi R/2\). Their common clients have arbitrary finite positive weights \(w_i\), total \(C\), satisfying

\[
C<qr,\qquad \max_i w_i\le aR.
\]

Each common client chooses a location independently and minimizes expected total weight at its chosen location, including itself. Exclusive clients are forced. Then a possibly mixed Nash equilibrium exists with

\[
L_A\ge qr,\qquad L_B\ge qR.
\]

Here \(A\) is the location with reach \(R\). All probabilities constructed below are individual, independent probabilities; no grouping or correlation of clients is used.

Normalize \(R=1\), write \(r=1-\delta\), so \(0\le\delta<a/2\). Let \(V=2-\delta-C\) be the union weight, and put

\[
U=V-2q=2a-C-\delta,
\qquad Z=V-2qr=2a-C+q^3\delta.
\]

The target interval for the expected load difference \(\Delta=L_A-L_B\) is \([-Z,U]\).

Useful consequences are

\[
U>q^4-a\delta>q^4/2>0,\quad Z\ge U,\quad Z>3\delta/2,\quad V/2>q.
\]

For the third inequality, \(Z>q^4+(q+q^3)\delta\), whose difference from \(3\delta/2\) is positive throughout \([0,a/2]\); at the upper endpoint the difference is \(aq^3/4>0\). For the fourth,
\(V>1+ar>1+q/2>2q\).

## 1. Equilibrium coordinates and three mixers

Give common client \(i\) coordinate \(c_i=w_i(2p_i(A)-1)\). Its equilibrium conditions are

\[
\begin{array}{ll}
c_i=w_i&\Longrightarrow\Delta\le w_i,\\
c_i=-w_i&\Longrightarrow\Delta\ge-w_i,\\
|c_i|<w_i&\Longrightarrow c_i=\Delta.
\end{array}
\]

The load identity is \(\Delta=\delta+\sum_i c_i\). If there are \(k\ge2\) mixed clients and pure masses \(P_A,P_B\), this gives

\[
(k-1)\Delta=-\delta-P_A+P_B.
\]

Every equilibrium with at least three mixed clients already meets both targets. In the constructions below, a designated mixing probability may equal an endpoint; the same coordinate formulas remain valid by continuity, and such a client may be treated as a designated mixer for the mass inequalities. For \(\Delta=d\ge0\), all mixed weights are at least \(d\), and

\[
C\ge \delta+(2k-1)d+2P_A\ge\delta+5d.
\]

Hence \(d\le(C-\delta)/5<U\). Indeed,

\[
6C+4\delta<6q+(4-6q)\delta<5-2q<10a,
\]

where the last strict inequality is \(q<5/8\). For \(\Delta=-e\le0\), similarly

\[
C\ge(2k-1)e-\delta+2P_B\ge5e-\delta,
\]

so \(e\le(C+\delta)/5<Z\). To verify this last inequality,

\[
6C+(1-5q^3)\delta<6q+(6-16q)\delta\le6q<10a.
\]

These numerical mass implications apply even when the equilibrium in question has only two mixers: whenever \(C\ge\delta+5d\) or \(C\ge5e-\delta\), the same conclusion follows.

## 2. Largest client and the maximum-square construction

There is nothing to prove if \(C=0\). Otherwise let \(x\) be a largest common weight and let \(S=C-x\).

If \(\delta>S\), hold \(x\) at \(B\) and choose a pure Nash equilibrium of the remaining clients. Such an equilibrium exists by the usual finite improvement potential. Client \(x\) also has no improvement because

\[
L_B-L_A\le x+S-\delta<x.
\]

Moreover \(L_B\ge r-S>r-\delta=2r-1>q\). If \(L_A<qr\), then \(L_B-L_A>Z>S\), so every remaining shared client must be at \(A\); this gives \(L_A=1-x\ge1-a=q\ge qr\), a contradiction. This settles \(\delta>S\).

Now assume \(\delta\le S\). On the nonempty compact polytope

\[
\mathcal P=\{(c_i)_{i\ne x}: -w_i\le c_i\le w_i,\ \sum_{i\ne x}c_i=-\delta\},
\]

maximize \(\sum_{i\ne x}c_i^2\), choosing a vertex maximizer. A vertex has at most one coordinate strictly between its bounds. If all coordinates are endpoints, assign \(x\) probability \(1/2\); this gives \(\Delta=0\) and is an equilibrium.

Otherwise let the unique interior coordinate have weight \(z\le x\) and value \(d\). Assign \(x\) coordinate \(d\), so \(x\) and \(z\) both mix independently with probability \((1+d/w)/2\). The load identity gives \(\Delta=d\). For a pure \(A\) client of weight \(v\), decreasing its coordinate and increasing the pivot is locally feasible, and maximality gives \(d\le v\). For a pure \(B\) client, the opposite perturbation gives \(d\ge-v\). Thus this is a Nash equilibrium.

Global maximality gives stronger exchange conditions. If \(d>0\), every pure \(A\) client has weight at least \(z\); every pure \(B\) client of weight below \(z\) has weight at most \(d\).

For the first assertion, consider a pure \(A\) client of weight \(v\). If \(2v\ge z-d\), move the pivot to \(z\) and its coordinate from \(v\) to \(v-(z-d)\). The change in the squared objective is

\[
2(z-d)(z-v),
\]

so \(v\ge z\). If \(2v<z-d\), flip its coordinate to \(-v\) and increase the pivot to \(d+2v\). The gain \(4v(d+v)>0\) is impossible.

For a pure \(B\) client of weight \(v<z\), if \(2v\ge z+d\), moving the pivot to \(-z\) and its coordinate to \(-v+(z+d)\) gives positive gain \(2(z+d)(z-v)\), impossible. Otherwise flipping it to \(+v\) and moving the pivot to \(d-2v\) has gain \(4v(v-d)\), forcing \(v\le d\).

For negative gap \(-e\), the symmetric statements hold: every pure \(B\) client has weight at least \(z\); pure \(A\) clients below \(z\) have weight at most \(e\).

## 3. A bad positive gap cannot persist

Suppose the constructed equilibrium has gap \(d>U\). If a pure \(A\) client exists, its weight is at least \(z\ge d\). With pure masses \(P_A,P_B\), the two-mixer balance gives \(P_B=\delta+P_A+d\), and hence

\[
C=x+z+2P_A+\delta+d\ge\delta+5d.
\]

Section 1 rules this out. Therefore all other clients are pure \(B\), with total weight \(\delta+d\).

Call such a client large if its weight is at least \(z\); every other one has weight at most \(d\). If some latter client has weight \(v\in[d/3,d]\), mix it with \(x,z\). The new gap is \((d-v)/2\), which is within all three weights, and every remaining client stays pure \(B\). This is a three-mixer equilibrium and meets the targets. We can therefore assume every nonlarge client has weight below \(d/3\).

There must be a large client. Otherwise order the small weights decreasingly and take the prefix just before its running sum first reaches \(d\). Let its sum be \(T<d\), and let \(v\) be the next weight. Then \(d-T\le v\), and every weight in the prefix is at least \(v\). Mix this prefix together with \(x,z\), keeping all others at \(B\). If the prefix contains \(m\) clients, the new gap is \((d-T)/(m+1)\), feasible for every mixer. Since each small weight is below \(d/3\), the prefix is nonempty; the resulting equilibrium has at least three mixers and meets the targets.

We next show \(d\le\delta\). If at least two large clients exist, \(\delta+d\ge2z\ge2d\). If exactly one exists, call its weight \(y\ge z\) and let the small total be \(T=\delta+d-y\). If \(\delta+T\le2z\), mix \(x,y,z\) and place every small client at \(A\); the gap is \(-(\delta+T)/2\), feasible for all three mixers, and gives the targets. Otherwise

\[
2\delta+d\ge\delta+T+z>3z\ge3d,
\]

which gives \(\delta>d\).

Change to the pure profile with \(x\) at \(A\) and all other common clients at \(B\). Since \(C=x+z+\delta+d\), its loads are

\[
L_A=r-z-d,\qquad L_B=r-x.
\]

In fact \(L_B\ge q\). Otherwise \(x+\delta>a\), and hence \(C>a+2d\). Together with \(C<qr\) this gives

\[
d<\frac{q^3-q\delta}{2}.
\]

But \(d>U>q^4-a\delta\); combining these inequalities forces \(\delta>a\), contrary to \(\delta<a/2\). Also, since \(x\ge z\) and \(\delta\ge d\),

\[
2(z+d)\le C<qr,
\qquad L_A>(1-q/2)r>qr.
\]

Repair this pure profile by successive strict improvements. If its initial gap \(G=x-z-d\) is nonnegative, both loads are at least \(q\), and every improvement leaves both new loads strictly between the previous two loads, so both quotas remain satisfied.

If \(G<0\), its magnitude is at most \(d\). The clients \(x,z\) and all large clients have weights at least \(d\), and cannot improve; only the small clients, each below \(d/3\), can move. Before the first sign reversal \(L_A\) increases and \(L_B\ge V/2>q\). At the first reversal the positive gap is smaller than the moved weight, hence below

\[
d/3\le\delta/3<a/6<q^4/2<U.
\]

At this point both loads exceed \(q\), and remain so during all later improvements. The finite potential ensures termination at a pure Nash equilibrium meeting the targets.

## 4. A bad negative gap cannot persist

Suppose instead the constructed equilibrium has gap \(-e<-Z\). Every pure \(B\) client has weight at least \(z\ge e\). If any exists, the two-mixer balance \(P_A-P_B=e-\delta\) gives

\[
C=x+z+2P_B+e-\delta\ge5e-\delta,
\]

which Section 1 rules out. Thus all remaining clients are at \(A\), with total \(T=e-\delta\le e\). If some has weight \(v\ge e/3\), mix it with \(x,z\), giving gap \(-(e-v)/2\). This is a valid designated-three-client equilibrium and meets the targets. We may therefore assume every remaining weight is below \(e/3\).

Since \(C=x+z+e-\delta\ge2z+e-\delta\) and \(e>Z\),

\[
2z<C-Z+\delta=2C-2a+2a\delta<2q^3r.
\]

Consequently \(e\le z<q^3r\). Moreover

\[
U>q^4-a\delta>q^3r/3>e/3.
\]

For the middle inequality, multiply by three and use

\[
3q^4-q^3-(3a-q^3)\delta>
3q^4-q^3-(3a-q^3)a/2=(5-8q)/2>0.
\]

Change to the pure profile with \(x\) at \(B\), and every other common client at \(A\). Its loads are

\[
L_A=1-x\ge1-a=q,\qquad L_B=1-z-e.
\]

If \(L_B\ge q\), successive pure improvements preserve both lower bounds. Otherwise the gap \(G=z+e-x\) is positive and satisfies

\[
U<G\le e.
\]

Clients \(x,z\), having weights at least \(e\), cannot improve. Only the remaining tiny clients can move. While the gap is positive, \(L_A\ge V/2>q\), and \(L_B\) increases. At the first negative sign reversal the new absolute gap is below the weight moved, hence below \(e/3<U\le Z\); both loads then exceed \(q\), and all later improvements are safe.

If the process terminates without reaching \(L_B\ge q\), its positive gap is still larger than \(U>e/3\). No tiny client can remain at \(A\), because every one would have a strict improvement. Thus all tiny clients must be at \(B\), and \(L_B=r-z\). But

\[
\delta+z<q^3+(1-q^3)\delta
=q^3+2a\delta<q^3+a^2=a,
\]

so \(L_B=r-z>q\), a contradiction. The final equilibrium therefore meets both targets.

This proves the lemma for arbitrary finite numbers of shared clients.

## 5. Exact strengthening without a maximum-weight assumption

The argument gives the following stronger characterization. Retain only
\(r>\phi/2\) and \(C<qr\), and let \(x\) be a largest common weight. A target equilibrium exists if and only if

\[
C-x\ge1-r\quad\hbox{or}\quad x\le1-qr.
\]

For \(C=0\), existence is immediate. Otherwise the outer argument in Section 2 needs only \(x\le1-qr\), because its contradiction is \(L_A=1-x\ge qr\). When the maximum-square polytope is nonempty, the weight bound is unnecessary. Sections 1 and 3 never use it. In Section 4 a bad negative gap itself implies \(x<1-qr\): if \(x\ge1-qr\), then

\[
C=x+z+e-\delta\ge ar+2e,
\]

so \(e<q^3r/2\le q^3/2<q^4<Z\), a contradiction. Thus the modified pure profile still has \(L_A=1-x>qr\). If its gap is nonpositive, that profile is already a pure equilibrium: the only common client at the high-load location \(B\) is \(x\), and its load advantage from moving is smaller than \(x\), since \(L_B-L_A=x-z-e<x\). If the gap is positive and \(L_B\ge q\), both loads exceed \(q\), so repair is safe. If \(L_B<q\), the repair from Section 4 applies unchanged.

Conversely, suppose \(S=C-x<\delta\) and \(x>1-qr\). Client \(x\) strictly prefers \(B\) for every profile of the other clients: its smallest possible cost at \(A\) is \(1-S>r\), while its largest possible cost at \(B\) is \(r\). Once \(x\) is at \(B\), every other shared client strictly prefers \(A\): its cost at \(A\) is at most \(1-x<qr\le q\), while its cost at \(B\) is greater than \(r-S>2r-1>q\). Therefore the unique equilibrium is pure, with

\[
(L_A,L_B)=(1-x,r-S),
\]

and it fails the first target. This proves the exact characterization. In unnormalized units, its two conditions are \(C-x\ge R-r\) or \(x\le R-qr\).

This refinement was independently derived and checked by the pair and independent research agents. It is not needed for the preceding \(x\le aR\) theorem.

## Pure-repair fact used above

If a shared client of weight \(w\) strictly improves by leaving a facility of load \(H\) for one of load \(L<H\), then \(w<H-L\). The new loads \(H-w,L+w\) both lie strictly between \(L,H\). The absolute load gap strictly decreases; if its sign reverses, the new absolute gap is less than \(w\). The potential \(L_A^2+L_B^2\) strictly decreases, so any sequence of strict pure improvements terminates in this finite game. All constructions and repairs above therefore use ordinary independent mixed equilibria or pure equilibria.
