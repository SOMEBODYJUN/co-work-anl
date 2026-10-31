# Direct covering surplus absorbs the terminal frozen wallet

2026-10-24, exchange10. Arbitrary finite common catalogs, arbitrary m>=2,
unit customers/providers, every full-history pure SPE. **HALF and the early
frozen-debt payment remain OPEN.** This is a static refinement of the residual
interface, not new actual income or a terminal-wallet constant improvement.

## Static surplus and absorption

Fix any full legal leaf Z=(S_1,...,S_m) and any m legal comparison themes
(T_1,...,T_m), assigned to the actual roles. Repetitions/empty themes are
allowed. Set B_Z=union_i S_i, O=union_i T_i, W=|B_Z|, and

    c_x=#i with x in S_i,
    k_x=#i with x in T_i,
    t_x=#i with x in S_i intersect T_i,
    Q=sum_i u_i(T_i,Z_-i),
    S=Q+(1-1/m)W-|O|.

S is static, not a true SPE deviation payoff. Its exact customer coefficients
are k-1 for c=0,k>0; 1-1/m for c>0,k=0; and

    s_x=k/(c+1)+t/[c(c+1)]-1/m

for c,k>0. The remaining coefficient is zero. Every s_x>=0: for c<m use
k/(c+1)>=1/m; at c=m retain t=k, so s_x=(k-1)/m>=0.

Write A=S_(m-1), B=S_m, X=A minus B, and define the existing unreduced
terminal wallet C=sum_(x in X)1/[c_x(c_x+1)]. Then

    Z_sur:=S+|X|/m-C >=0.                              (ABSORB)

Off X retain s_x>=0. On X, c>=1 and the exact coefficients are

    k=0:  1-1/[c(c+1)] >=0;
    k>0:  (c k+t-1)/[c(c+1)] >=0.

The last numerator is nonnegative because c,k>=1. This proof needs neither
SPE nor optimality. It pays C from the explicitly retained static surplus
and the indicated |X|/m part of the usual W/m direct-covering allowance.

## Original terminal IC and the direct early gap

Now Z is the actual leaf of one fixed full-history pure SPE. At actual
prefix i force T_i and follow the original strategy, obtaining Y^i. Put

    D_i=u_i(Y^i), e_i=u_i(Z)-D_i>=0,
    E_i=u_i(T_i,Z_-i)-D_i,
    EARLY=sum_(i<=m-2)(E_i-e_i).

Use the exact existing [terminal identity](../../round9/exchange/harmonic_terminal_wallet.md)
with a=u_(m-1), v=u_m, Delta=(a-v)_+, C'=C-Delta and h_T>=0:

    Q-W=C'+EARLY-e_m-h_(T_(m-1)).                     (QTAIL)

Consequently the following are exact:

    W/m+S-C'=(W-|X|)/m+Delta+Z_sur,

    |O|-2W=EARLY-e_m-h_(T_(m-1))
                 -(W-|X|)/m-Delta-Z_sur.             (DIRECT-EARLY)

Equivalently, in the existing unreduced notation G_T=e_T+g_T+ell_T,
the row anchor gives G_T=Delta+h_T, and

    |O|-2W=EARLY-e_m-G_(T_(m-1))
                 -(W-|X|)/m-Z_sur.                   (DIRECT-G)

All displayed direct credits are nonnegative. Thus the direct interface
does not need the stronger assignment demand Q<=(1+1/m)W or a separate
use of the harmonic C' funding. It still needs an EARLY upper bound; no
such all-history payment is proved here.

After choosing an optimal comparator, direct substitution m=5 gives

    OPT_5-2W=EARLY-e_5-G_(T_4)-(W-|X|)/5-Z_sur.

The three early rows remain uncontrolled. This does not establish half
coverage for arbitrary five-player catalogs; no five-player optimization or
finite no-counterexample scan was run.

Root and tree10 independently reconstructed ABSORB and the rearrangement
from definitions, with no fatal issue. Their sign review is in
[tree10's note](../tree/exchange_terminal_refinement_review.md). The static
sign proof and the terminal SPE identity are distinct inputs. No external
review or novelty claim is made.

The attempted full-suffix harmonic-potential extension was not promoted:
its unpaid deletion-potential terms already occur in
[round2](../../round2/mixed/two_query_cross_child_boundary.md) and
[round3](../../round3/mixed/self_consistent_query.md). Further work must obtain
a real early all-history bound, not merely restate that coalition regret.
