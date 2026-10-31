# Dynamic-credit coverage one-step LP probe comparison

- source ID: `469334e1729f6e2a0365`
- source path: `research/workspaces/customer-attraction/R-12bf6a96d24c48eca828620d6642e203/dynamic_credit/coverage_one_step_probe.py`
- source SHA-256: `71410303ae040502d47b226ec3124e7d089619871f9647d54e236379202e350c`
- source size: 1498 B

The probe was read and executed once. It fixes r=3,k=4, samples 3000 random response maps, constructs exact Fraction utility/profit values and a floating LP with coverage equality and one-step rows, then reports a witness at trial 9 with `gap=1/5`, support weights `{2:3/5,3:1/5,4:3/5,8:3/5,9:1/5}`, and `minrow=0`. This is a finite floating LP witness for the sampled one-step projection, not a complete strategy/SPE certificate and not a universal theorem.

Compared with `背景新增覆盖余额与首步分解--引理` and `两步安全归纳与策略锥精确边界--审查`, the probe illustrates a local sufficient-condition failure while the global telescoping/half question remains separate. It is not migrated to unrelated-machines.
