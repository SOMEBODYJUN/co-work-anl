# Dynamic-credit one-step closure probe comparison

- source ID: `ac321ae4ebb5862e0dc9`
- source path: `research/workspaces/customer-attraction/R-12bf6a96d24c48eca828620d6642e203/dynamic_credit/one_step_closure_probe.py`
- source SHA-256: `8975d63c1fde7d51abfa8690b08ff2a119be44d4492ad5ea12c1242af2e32ba9`
- source size: 1447 B

The probe was read and run once. It fixes r=3,k=4, samples 3000 random response maps and solves a floating LP over mask weights. The run found a finite witness at trial 2 with `gap=1/16`, support weights `{2:17/40,4:1/40,5:33/40,8:51/80,9:3/20}`, and `minrow=0`. The output is a finite exploratory separation of the scalar one-step closure rows, not a strategy certificate, SPE, exact proof, or universal impossibility result.

Compared with the exact JSON/note pair, this script is a random floating search rather than the final exact 30-customer record. It is distinct from `coverage_one_step_probe.py` and from the archived direct-cover LP probe. No witness is migrated to unrelated-machines.
