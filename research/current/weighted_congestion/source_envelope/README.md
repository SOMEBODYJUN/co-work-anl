# R3 sharp source-parameter review

`proof.md` contains a complete independent reconstruction of

\[
\sup_{n,k,w,\beta}\min(A,B)
\sim\frac2{\sqrt e}\frac{\sqrt{d\ln\ln d}}{\ln d},
\]

with the exact positive-weight integer parameter domain of source
Theorem 1, equation (3). Its lower proof retains both integer roundings;
its upper proof covers every legal parameter sequence. This is an
optimization result inside the existing source construction, and gives
no existence upper bound for the universal game class.

Review state: independently reconstructed proof, pending parent-agent
independent attack. No priority/novelty certification.

`verify_logs.py` uses only Python's standard-library `decimal`. From the
repository root, the actual successful command was:

```bash
python tests/audits/weighted_congestion/source_envelope/verify_logs.py --output evidence/runs/weighted_congestion/source_envelope/verification.json
```

Run date: 2026-10-14 UTC. Six integer degrees `10^32` through `10^1024`
were checked at two different arbitrary precisions. The floor/ceil choices
agree, displayed normalized ratios agree, and exact inequalities (U3)
and (L5) pass their numerical checks. `verification.json` also contains
explicitly separated continuous proxies at symbolic integer degrees
`10^10000`, `10^1000000`, `10^(10^10)`, and `10^(10^20)`; in those proxies
`n` is replaced by its unrounded precursor `N`.

The exhibited candidate converges extremely slowly: the normalized first
ratio rises from approximately `0.4464` at `10^32` to `0.7043` at
`10^1024`, and the largest continuous proxy has approximately `1.0897`,
against the limiting `2/sqrt(e)=1.2130613194...`. This reflects
`H/(H-ln(2H))->1`; it is consistent with the proof and should not be
presented as finite-range near optimality.

No finite calculation supplies the global upper proof. These computations
are reproducible diagnostics, not rigorously rounded intervals or exact
certificates. No git write or shared ledger edit was performed by this
reviewer.


---
整理来源与当前文件用途见[逐文件登记](../../../weighted_congestion_frontier/FILES.md)。程序统一通过 `python3 tests/audits/weighted_congestion/replay.py --list` 选择；历史命令、输出摘要与源码哈希属于原冻结版本。
