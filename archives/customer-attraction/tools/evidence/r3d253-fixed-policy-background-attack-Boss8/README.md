# R-3d253 fixed-policy background attack probe

The packet preserves the fixed `p=6,r=3` policy program, its 61-byte frozen output, and 100/200-trial replay logs. The program enumerates all 43 ordered histories and 258 action rows for one policy, then solves floating LPs over 63 nonempty masks and 21 two-slot backgrounds.

`python3 fixed_policy_background_attack.py 100` reproduces the frozen `{"status": "no negative numerical candidate", "trials": 100}` byte-for-byte; a 200-trial pressure run has the same status. The prefix is an integer background, continuous mask weights are not unit customers, and no Fraction or complete SPE certificate is present. This packet is a finite auxiliary audit only and does not prove universal security, a counterexample, or the six-provider half target.
