# Boss6 independent literal finite audit

This evidence belongs to `archives/unrelated-machines/state/审查/三叉palette张量v2独立字面清洗增量--审查.md`.

`audit.py` is a standard-library finite check only. It verifies the exact rational formula and strict decrease of
\[
G_k=(2-3^{-k})/(2-(2/3)^k)
\]
for `1<=k<=30`, the local product bound for all ternary palettes of size at most two for `k<=4`, and by exhaustive enumeration of all `2^9` edge assignments checks `OPT=2-q/d` on two explicit `d=3`, height-two ordinary tree-machine instances. `audit.json` is the saved run output.

The finite run does not certify the all-height proof, NP-hardness, any output-size claim, or operations outside aligned tuple tensor and pure layer contraction.
