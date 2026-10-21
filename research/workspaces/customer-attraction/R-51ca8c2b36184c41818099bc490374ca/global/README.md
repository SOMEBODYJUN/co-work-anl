# Global gap research checkpoint

2026-10-21. Personal exploratory backup for Boss7. Q-CAG-HALF remains OPEN.
No new general theorem or counterexample to half coverage was obtained here.
All files are confined to this personal directory; root handles shared changes.

## Current mathematical question

For the prescribed complete strategy, let V_ij be player i's utility after
choosing comparison topic T_j at the **actual** prefix, followed by the original
strategy's actual off-path continuation. The existing, unproved interface from
`research/current/customer_attraction/global_new_uniform_portfolio_two.md` is

    m O <= (m-1) W + sum_(i,j) V_ij.                 (UP)

This would prove the stronger ratio 2-1/m. The two-player version is already
proved in that existing asset. This directory does not claim UP for m>=3.
The next useful step is either a genuinely new full-tree comparison proving UP
or an exact complete-policy counterexample to UP. A negative floating LP or
an infeasible multiplier template would not itself be a half-coverage example.

`uniform_portfolio_induction_boundary.md` explains why a natural background
extension does not automatically give a backward induction: even the all-big
sharp family requires retaining a positive tail surplus.

## Discovery tools and actual runs

* `portfolio_probe.py` uses the canonical exact all-SPE solver. It minimizes
  actual-prefix query utilities over independently selectable off-path SPE
  continuations for each chosen actual path. A seed-734170 run of 300 random
  3-player/5-topic inputs found no negative UP slack; this is only finite
  diagnostic work. Existing root-tax and residual examples also gave positive
  UP slack. The tool considers all optimal supports and cheapest padding.
* `cone_probe.py` builds every ordered-history SPE row for a fixed complete
  policy and then minimizes the UP functional over the full nonnegative
  interest-type cone, normalized to actual W=1. Runs were 200 random sources
  at (m,k)=(3,5), seed 90230; 100 at (4,6), seed 90231; and 25 at (5,7), seed
  90232. Up to three low-welfare policy certificates were taken per source.
  No negative numerical optimum appeared. The 3- and 4-player runs attained
  numerical zero. These are neither exhaustive policy enumeration nor proof.
  The cone probe currently tests distinct m-topic comparison supports only.
* `portfolio_full_tree.py` reuses the existing full ordered-history MILP
  formulation from R-18e.../next_boss. It fixes an actual action pattern and
  optimizes the true UP expression, including all off-path policies. Outputs
  `full_tree_*.json` preserve the actual timed runs (45 seconds each).
  AAA/BCD at (3,4) numerically closed at zero. ABC/CDE at (3,5), ABB/BCD and
  ABC/BCD at (3,4), and AABB/BCDE at (4,5) timed out with no negative incumbent
  and negative lower bounds. No numerical optimum is promoted to exact proof.

The complete-tree program is a discovery tool, not a polynomial algorithm.
Its normalization u_1=1 excludes zero-u_1 policies. Any meaningful negative
proposal must be rationally recovered and independently checked at every
ordered history before use.

## Important boundaries already checked elsewhere

The stronger demand that all omitted comparison clients be paid directly by W
is false. R-d51.../independent_attack/residual_cover_family.md gives a two-player
family with external residual optimum 4q+6 > W=4q+5. The payment object must
retain the **net** gap OPT-W, including actual-only clients.

R-2fc.../background_induction explores P+new_coverage >= fresh_OPT in arbitrary
backgrounds. Its 23-customer example refutes a local first-step strengthening,
not its global candidate. It should not be rediscovered as a new bridge here.

Root reports a separate static minimum-matching candidate under examination
by the cone researcher. No computations for that candidate were duplicated.
Its exact per-customer cost formula was sent to root: common base
sum_(c=0)d + sum_(c>0)d/(c+1), plus the minimum assignment cost of matrix
C_ij=sum_(x in S_i cap T_j)1/[c_x(c_x+1)].
