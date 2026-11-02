# Equilibrium trees and punishment thresholds

Assigned branch of boss4; Q-CAG-HALF remains open. No git operations here.

* `weak_theta_replication.md`: new candidate full-SPE block replication
  proving the auxiliary bound W >= (m-1/2) theta_m false for m=3k, k>=4.
  theta_m is the worst static last-player best reply, not the oblivious
  mixed security value v_m. Independent attack is pending.
* `weak_theta_replication_audit.py`: exact expanded-client audit of every
  local arithmetic class used by the preceding induction.
* `theta_attack.py`: exploratory fixed-policy cone LP for the weaker theta
  bridge; floats only, no mathematical certification. The replication
  proof supersedes its immediate purpose.

Next: seek a threshold envelope that survives independent disjoint blocks,
or use a truly distributional security benchmark. The failed scalar theta
bridge cannot be repaired by a fixed additive half-player allowance.
