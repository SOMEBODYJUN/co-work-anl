# Root rigidity: new missing full-history information for five-player half

The half objective remains OPEN in this branch. No finite necessary-row
primal is being called a full SPE or a counterexample.

- `root_rigidity.md`: arbitrary-m root-to-terminal lemma
  f_((m-1)T)(Q)<=u+(3m-4)(m u-|T|)/2, complete pointwise proof, explicit
  reason the frozen old 557 point cannot be SPE-completed. It needs root IC,
  common root topic-size bounds and the genuine final-node comparison only.
  The five-player coefficient is 11/2. A sibling independently reconstructed
  and accepted this lemma; no external review is claimed.
- `audit_root_rigidity.py/.json`: independent Fraction evaluation, all 100
  fixed-topic pairs on the old 557 point; 66 negative rows, most negative
  -0.355737858... at T=D,Q=E. The general proof uses factorization, not a
  finite-m extrapolation.
- `root_middle_rigidity.md`: five-player strengthening using a genuine
  penultimate comparison. With M=max catalog size,
  f_(4T)(Q)<=(311/21)u+(55/21)M-(113/21)|T|, and consequently coefficient
  113/21 rather than 11/2 in the root size deficit. Exact nonnegative
  64-type identity and the compressed 24-entry table are the proof.
- `audit_middle_rigidity.py/.json`: exact coefficients and all customer types;
  sibling independent mathematical review passed. Parent is using the common M row
  with its separate capacity and whole-universe pricing work.
- `root_copy_reply_rigidity.md`: retains the genuine last reply C after the
  penultimate player copies B5. Gives f_(4T)(Q)<=(44/3)u+(13/5)M-(16/3)|T|,
  exact 128-type proof and maximal-source row 15 OPT5+193M<=1100u.
  `audit_copy_reply_rigidity.py/.json` independently checks all coefficients;
  sibling independent review requested.
- `probe_middle_rigidity.py` and its JSON outputs are numerical discovery
  only. `probe_three_profit.py` tested one discarded use of the existing
  three-remaining 5/3 theorem; those Cartesian queries have large slack at
  the old point and supply no new positive conclusion.

All work stays in this personal subdirectory. No shared file, work.py, git
commit or push was performed by this subagent.
