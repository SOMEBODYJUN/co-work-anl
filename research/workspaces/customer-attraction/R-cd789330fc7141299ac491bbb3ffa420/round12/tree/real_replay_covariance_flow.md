# Exact real-replay flow for adaptive deleted-load covariance

2026-10-25, tree12 continuation requested by root. Arbitrary original finite
common catalog, arbitrary m, every complete ordered-history pure SPE sigma.
**General HALF and the covariance payment remain OPEN.** This note proves
the actual nonnegative replay-flow coefficients and fixed-potential
telescoping to the selected endpoint law. It does not bound the adaptive
edge work by the available profit/variance banks.

## 1. Fixed row and passive query label

Fix actual role i, its exact original actual prefix h_i, and a query law p.
Let z_A=finish_sigma(h_i,A) be its original forced-A endpoint. For any row-i
terminal profile z, ell_i(z) deletes the SAME entering role i. Set

    a_A(x)=1_(x in A), rho_x=Pr_p[x in A],
    w_A(x)=a_A(x)t_x^2, w(x)=rho_x t_x^2,
    Cov_i=E_(A~p)[(w_A-w) dot ell_i(z_A)].

t is one fixed reference vector for the whole construction. It can be the
deleted or full background saddle t; no minimizer is needed for the flow
identity. Let Q_i be the actual selected endpoint probability law in row i,
not a newly invented terminal wallet. Its endpoints keep h_i but may have
any entering action. Raw endpoint domains must free the actual-action tag
to include the hybrids below; a pointwise fixed-actual tag is insufficient.

Draw A~p and y~Q_i independently. The A label is passive source metadata; no
player observes it as a new signal. Write the target tail as y_(i+1),...,y_m.

## 2. Real replay path and exact coefficients

Start z^i(A,y)=z_A. For j=i+1,...,m define

    g_j=(h_i,A,y_(i+1),...,y_(j-1)),
    z^(j-1)=finish_sigma(g_j),
    z^j=finish_sigma(g_j,y_j).

The recursively defined preceding endpoint is exactly finish_sigma(g_j),
so every j-edge is a GENUINE original future-j deviation at its exact legal
ordered history. Its entire continuation follows the same original sigma.
Full-history SPE supplies its whole-row slack

    Gamma_j(A,y)=u_j(z^(j-1))-u_j(z^j)>=0.

No source is priced by a customer-weighted IC, and the deleted role i never
changes. The edge mass on every such labeled target path is exactly

    f_i(A,y,j)=p_A Q_i(y)>=0.                        (COEFF)

Self-loops can be retained or omitted. Augmenting states with the replay
phase j makes the finite path flow acyclic even if two profiles happen to
coincide. It is unit-conservative: initial joint law is
p_A delta_(z_A), and each interior state has matching incoming/outgoing mass.

After the last future intervention,

    zpre(A,y)=(h_i,A,y_(i+1),...,y_m).

Finally replace its entering action A by y_i while FREEZING the target tail.
The resulting full endpoint is exactly y. This last static edge has no
entering-role IC claim, but

    ell_i(zpre(A,y))=ell_i(y),

so its deleted-load shadow work is POINTWISE ZERO. The final labeled law is
p_A Q_i(y): the selected endpoint is independent of the passive query label.

## 3. Exact covariance-work identity

The hybrid deleted load depends only on y and is independent of A. Hence
E_(A,y)[(w_A-w) dot ell_i(zpre)]=0. Summing all real future edges gives

    Cov_i=-sum_(A,y,j>i) p_A Q_i(y)
                    (w_A-w) dot[ell_i(z^j)-ell_i(z^(j-1))]. (COV-FLOW)

Thus the replay expansion really has explicit nonnegative, unit-conservative
coefficients and ends at the selected endpoint law. It is not an arbitrary
assertion that some desired covariance flow exists. If entering action is
rewritten FIRST instead, every subsequent state is independent of A and all
future adaptive work averages to zero; the whole debt stays on the entering
rewrite with no future IC. The tail-first order above avoids that failure.

## 4. Fixed canonical/net potential telescopes on the SAME flow

Let F_i(z) be one fixed function of the entire row-i endpoint, such as the
canonical weighted floor deficit. Including the final static entering
rewrite, the SAME labeled paths give exactly

    sum_flow delta F_i=E_(Q_i)F_i-E_p F_i(z_A).       (F-TELE)

No edge's positive part is taken. In a selected mean-floor-feasible domain,
E_Q F_i<=0, so this is paid by the original source canonical surplus. In
root's later uniform net-cap domain, F alone need not have nonpositive
selected mean; the correct potential is

    B_i(z)=d_i(z)+sum_(k>i)[M(z_<k)-u_k(z)].

For one global cap sum_i E_Q B_i<=W, let

    I_total=W-sum_i E_p d_i(z_A)>=0,
    S_total=sum_i E_p sum_(k>i)[u_k(z_A)-M(z_A,<k)]>=0.

Then the same full flow, summed over i, obeys

    sum_(all flows) delta B_i<=I_total+S_total.       (NET-TELE)

This uses the actual selected Q_i and one global cap, not a new bank or a
role-by-role reallocation. It also keeps the final static rewrite, whose
B_i difference need not vanish even though its deleted shadow work does.

For every original source tag A its total initial path mass is
sum_y p_A Q_i(y)=p_A. Thus its original reduced-cost/canonical bank is used
with exactly its original source probability, once. Every intermediate
potential appears with equal incoming/outgoing mass and cancels, including
an intermediate profile coinciding with some other source profile. Taking
edge positive parts would destroy this source-capacity statement. No such
statement is inferred for separate positive parts of the true IC slacks.

## 5. Exact replay edge amount and the remaining mismatch

For one future j-edge z->z', put delta=z'-z and
Sdesc(z)=sum_(k>j)[u_k(z)-M(z_<k)]. Both strict-descendant suffixes follow
original sigma, so Sdesc(z),Sdesc(z')>=0. Prefixes before j agree. Therefore

    delta B_i=delta d_i+Gamma_j
       +sum_(i<k<j)[u_k(z)-u_k(z')]
       +Sdesc(z)-Sdesc(z').                         (RESET)

With a uniform net-cap dual score
r_i(z)=eta_i+mu B_i(z)-w dot ell_i(z)>=0, exact shadow work is

    w dot delta ell_i=mu delta B_i+r_i(z)-r_i(z').

For the fixed entering action A, the reciprocal tangent error

    E_i^t(z)=sum_(x in A)(1-t_x c_x(z))^2/c_x(z)

satisfies -w_A dot delta ell_i=delta d_i-delta E_i^t. Combining gives the
exact adaptive edge expression

    -(w_A-w) dot delta ell_i
      =delta d_i-delta E_i^t+mu delta B_i+r_i(z)-r_i(z'). (EDGE)

All fixed B_i and r_i differences telescope under the proven flow. This is
why taking separate positive parts of ancestor losses and descendant
surpluses would discard useful cancellation. EDGE still contains entering
tangent-payoff work; it is not bounded by NET-TELE alone.

On the final static entering rewrite, deleted score is unchanged, so the
dual identity is exactly 0=mu delta B_i+r_i(zpre)-r_i(y). Adding this zero
term makes the B_i/reduced-cost telescope reach Q_i without claiming an IC
or a tangent-root identity on that last rewrite.

For a copy intervention y_j=A, same-leaf equality gives

    delta d_i+Gamma_j=u_j(z)-d_i(z).

For the actual arbitrary target y_j, the exact residual is instead

    delta d_i+Gamma_j
      =u_j(z)-d_i(z)+[d_i(z')-u_j(z')].             (PAIR-RESIDUAL)

The bracket compares DIFFERENT whole themes in one endpoint. The saddle
input-price law does not by itself give a usable sign for it. Replacing all
target actions by A would recover copy cancellation but would change the
selected Q_i endpoint law and invalidate F-TELE/NET-TELE's claimed bank.

This is the precise current gap: the real-replay coefficients and fixed
potential telescoping are now proved, but the accumulated adaptive tangent
work/same-leaf pair residual has not been bounded by D, IC, or the permitted
half-slot/statical slack. For m=5 the identical flow and RESET/EDGE formulas
apply; no unconditional OPT_5<=2W follows.

For a full-slot score w dot c rather than deleted score, the final entering
rewrite has common score change w dot(1_(y_i)-1_A). It must be retained
explicitly; the zero-work statement above concerns deleted-row-i work only.
The separate full-slot norm identity cannot be silently imported with that
term dropped.
