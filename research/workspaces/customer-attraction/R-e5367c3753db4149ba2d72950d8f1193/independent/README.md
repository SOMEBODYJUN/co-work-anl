# Independent general-proof attack and audit checkpoint

2026-10-24. General Q-CAG-HALF remains open. No git commit or board message
was made by this subagent.

## Independent attack

I first attempted a background-state induction charging old-provider rent.
The natural threshold step fails: even if every later provider at every
tail history has final payoff greater than t, the root can remain below t.
The existing 34-customer full-history individual-security certificate gives
this failure for 29/3<t<2411/246. Thus future utility floors alone do not
pay for adaptive movement across branches.

A stronger general candidate is

    every current SPE payoff >= theta_(r+1)(b)
      := min_(r static competitor topics) max_T sum_(x in T)1/(b_x+1+c_x).

At arbitrary backgrounds this would imply each actual player gets at least
OPT_m/(2m), by the standard common-catalogue static budget, and hence half.
No proof or counterexample was obtained. On the old 34-customer certificate,
theta_4(0)=23/3<29/3, so that certificate does not refute it.

`test_extra_pure_threshold.py` tests only this explicit all-input candidate:
it fixes the full 43-node strategy from that certificate, varies all 63
nonempty customer interest types, and uses a MILP query selector for all 56
three-slot static backgrounds. The normalized maximal diagnostic gap was
numerically zero. This is only a finite fixed-strategy failure to find a
counterexample. The floating MILP output in the accompanying JSON is not
an exact general proof or an exact infeasibility certificate. No broader
negative scan was performed. The optimization is a labelled-action cone
relaxation: its zero-gap optimizer identifies old labels 0 and 3 as the same
customer set. It is not presented as a new distinct-set catalogue instance.

## Independent reservation-lift audit

`reservation_lift_independent_audit.md` reconstructs and proves the root's
conditional closure before reading the proposed proof. It covers every
query support, alpha=0 and alpha=1, actual insertion-cap preservation,
empty old topics, the full off-path credible construction, and the n=1
root exception. It also records the zero-J action-identity caveat.

The conditional closure is sound. It is not a proof of the old universal
menu inequality, path-menu conjecture, or general half coverage.
