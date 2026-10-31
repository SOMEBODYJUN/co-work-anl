# Harmonic insertion checkpoint; no new paid bridge

2026-10-24. Paused at parent request for an independent repair review.
General Q-CAG-HALF remains OPEN. This checkpoint records an exact route
identification, not a new theorem or a negative search campaign.

For Phi(z)=sum_x H_(c_x(z)), the individual utility is
u_i(z)=Phi(z)-Phi(z^{-i}). At an arbitrary nonroot history the true welfare
relay remains DeltaW=DeltaV+DeltaP_old-Gamma, with signed old-player refund;
none of the following permits deleting DeltaP_old.

Fix an actual history of current player i. Let z_A denote its true complete
leaf after forcing A, including fixed past, current A, and the original full
SPE continuation. An extra independent query T has insertion payoff

  K(T,A)=Phi(z_A+T)-Phi(z_A)=sum_(x in T) 1/(1+c_x(z_A)).

Hence the full-menu root condition is exactly a potential insertion minimax:
for every query distribution p, find a column mixture (equivalently for this
fixed p, one column A) satisfying

  E_(T~p) K(T,A) <= u_i.

The passage from this insertion derivative to current utility is not implied
by current IC: current IC compares root-deletion marginals, while the
insertion query adds a separate player. If a proof transports Φ differences
across same-count histories, those histories' complete continuations can
still differ; they cannot be identified without a new true-successor IC
relation. This remains the exact missing transport.

A useful exact bookkeeping relation, already present in the established WP
and insertion-tax literature in the repository, is the following. Let
q_x=Pr_(T~p)[x in T], a_x=1_(x in A), and c_x=c_x(z_A). The query payoff
against the leaf with current i removed is

  h_p(A)=sum_x q_x/(1+c_x-a_x),

and

  E_T K(T,A)=h_p(A)-tau_p(A),
  tau_p(A)=sum_(x in A) q_x/[c_x(c_x+1)] >=0.

Averaging forced A~p gives insertion average C_i(p)-E_A tau_p(A), whereas
average actual deviator utility is D_i(p). Thus the stronger diagonal-push
condition would require its insertion tax to pay the negative
D_i(p)-C_i(p), together with actual IC slack u_i-D_i(p). This is WP, not
an independently established payment. The repository's earlier
R-cd789330fc7141299ac491bbb3ffa420/round2/mixed work already identifies
this relation and the unresolved successor-IC deletion transport; no novelty
or proof is claimed here.

At m=5 the unproved full-menu relation would imply the original bound after
summing all five actual positions, but no unconditional factor-two bound
has been derived. Known endpoint-potential monotonicity and optimal-prefix
relay-budget failures are not repeated as new results.
