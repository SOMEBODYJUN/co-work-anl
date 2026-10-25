# Five-provider credible attack

The mathematical result and exact scope are in [feedback_cycle.md](feedback_cycle.md).
It gives a conditional general last-response cycle inequality and excludes one
universal-punisher lift of the old frozen 64-atom point. The main half problem
remains OPEN; no actual counterexample was found.

The optimizer-free exact certificate check is `verify_universal_punisher.py`,
with output `universal_punisher_exact.json`. Exploration scripts and proposal
outputs are not equilibrium certificates. The generated catalog is rejected
by the canonical all-SPE solver at prefix ABC.
