# Boss4 CJ 五原程序证据

唯一claim回执pushed/Boss4/synced，tip `3ab555d889a2fe96a0f1a40c09bcc9493c4b161e`。五primary owner均在本次完成前再核Boss4/in-progress。交付仅external staging，Root精确拷入并串行保存；无Git/claim/done/checkpoint操作。

本批原程序main新运行 **0**。旧冻结报告完整且内部SHA绑定当前五源码，参数/输出充分，复用历史事件，不补造exit code。新增独立有界数据helper仅一次exit0，结果/输入/日志完整保存；它没有导入原模块，没有重做旧全owner/匹配计数。

| 证据 | 内容 |
|---|---|
[primary-inventory.json](primary-inventory.json) | 五原件SHA/字节/完整行数 |
[comparison-inventory.json](comparison-inventory.json) | 12相关原件，current只§10–11复核，其余全读 |
[historical-run-reuse.json](historical-run-reuse.json) | 每主源旧运行SHA绑定与真实边界 |
[verify_frozen_inputs.py](verify_frozen_inputs.py) | 新独立数据检查源码 |
[new-data-check/result.json](new-data-check/result.json) | 32输入/两完整certificate/5源码绑定PASS |
[new-data-check/expanded-inputs.json](new-data-check/expanded-inputs.json) | 每件两端/全部S0,S1,x,bad,repair/slot邻边/root区间/编号映射/逆尾路径 |
[input-expansion-scope.json](input-expansion-scope.json) | role超出原main的映射只作数学展开，不冒原run |
[new-data-check/event.json](new-data-check/event.json) | 实际command/cwd/exit0/日志SHA，未捕获开始时间不虚填 |
[comparison-findings.json](comparison-findings.json) | 全仓检索、量词与版本范围 |
[unapplied-corrections/whitelist.json](unapplied-corrections/whitelist.json) | 三旧页4处最小未应用修订、精确快照SHA |

完整原件：

- [4b417f3b0c8858c5c2ba — tests/audits/unrelated_machines/optimal_hull_closed_cycle_independent.py](original/tests/audits/unrelated_machines/optimal_hull_closed_cycle_independent.py)，SHA `ac42e3dce6b3acf0fa6512de939b186e17ea0e1b2e01808f2e9c09cbe761eeaa`。
- [7c60cdc8dd34a338c6a6 — tests/audits/unrelated_machines/optimal_hull_closed_cycle_reviewer.py](original/tests/audits/unrelated_machines/optimal_hull_closed_cycle_reviewer.py)，SHA `aa6ad02c4c40ff976b7978332137793a4ca69906924e5160fc0f14521bb76021`。
- [9ab216969ac3b3ada7e0 — tests/audits/unrelated_machines/optimal_hull_long_chain_gap.py](original/tests/audits/unrelated_machines/optimal_hull_long_chain_gap.py)，SHA `98f52cbb67f2b5ee4994414c29b44eac80da0f92e4aa91710b3531249d1ded68`。
- [7a2d85c62c8b28b8cbdf — tests/audits/unrelated_machines/optimal_hull_long_chain_independent.py](original/tests/audits/unrelated_machines/optimal_hull_long_chain_independent.py)，SHA `e0a4d4f99396cdfa42a07dac191431fc8c439f76b033a1df555ab3a16f573149`。
- [cac5f52d0332f1acf59d — tests/audits/unrelated_machines/optimal_hull_long_chain_reviewer.py](original/tests/audits/unrelated_machines/optimal_hull_long_chain_reviewer.py)，SHA `5561827f8cfed3db564d84f36bff8aafa9402d0ae22b4cd202526c202d250f7f`。

完整比较原件（comparison-only，不抵primary done）：

- [cab1dc997d607b2168c5 — evidence/certificates/unrelated_machines/optimal_hull_closed_cycle_k3d1.json](comparison/evidence/certificates/unrelated_machines/optimal_hull_closed_cycle_k3d1.json)，SHA `767b3419d1b9bc6aad4f75eff9c9a6eb5ad3148a40327c0d8abe6bed95e42c74`；full source。
- [93bcdf4e09e6338aab8f — evidence/certificates/unrelated_machines/optimal_hull_long_chain_k3d1.json](comparison/evidence/certificates/unrelated_machines/optimal_hull_long_chain_k3d1.json)，SHA `e640f1180f6b34596033d86d5c8c370a61451d176559d212789970ad1d42b077`；full source。
- [86039e74710aa9d97bf7 — evidence/runs/unrelated_machines/optimal_hull_closed_cycle_audit.json](comparison/evidence/runs/unrelated_machines/optimal_hull_closed_cycle_audit.json)，SHA `5cd6127e5038ea25f2b19c2cb0b2b5d281dde127a91fad5e5ab2d5c3a77ec4eb`；full source。
- [736d43957f29e74cecc4 — evidence/runs/unrelated_machines/optimal_hull_long_chain_audit.json](comparison/evidence/runs/unrelated_machines/optimal_hull_long_chain_audit.json)，SHA `e4b15778a93f79c026fe7c94b69e95d8ecd993ebf4257da8d9c2d38668826a04`；full source。
- [fafe3d3d44e5dbc74bab — evidence/runs/unrelated_machines/optimal_hull_long_chain_independent.json](comparison/evidence/runs/unrelated_machines/optimal_hull_long_chain_independent.json)，SHA `f6c885a6262ba3974a5918ac1c1f11e5528cb0ca5a42736d4aeedc68388f35d9`；full source。
- [bfd5450b740d8c5a2744 — evidence/runs/unrelated_machines/optimal_hull_long_chain_reviewer.json](comparison/evidence/runs/unrelated_machines/optimal_hull_long_chain_reviewer.json)，SHA `2984227db80d29eddf108208f61add3b2e690bf4be67d61a249756cce51ec283`；full source。
- [ec929868bd8d7c9ca425 — examples/unrelated_machines/optimal_hull_closed_cycle_k3d1.json](comparison/examples/unrelated_machines/optimal_hull_closed_cycle_k3d1.json)，SHA `d531ad742ed8b37b4ddd98da8ef187b10d80ddbdd164f5209c3747d1f73cab0a`；full source。
- [b34ae3ca7a190e180641 — examples/unrelated_machines/optimal_hull_long_chain_k3d1.json](comparison/examples/unrelated_machines/optimal_hull_long_chain_k3d1.json)，SHA `dd25ee4743dd9ea2d1dff4af880d0c03a464c4661f79ae56c1702ede17be921b`；full source。
- [d01be51934200f21ded1 — research/current/unrelated_machines/cyclic_batch_repair_and_fork_obstruction.md](comparison/research/current/unrelated_machines/cyclic_batch_repair_and_fork_obstruction.md)，SHA `ba5d9763aca26d9b8fee7b49f353c3588291fbd94d89f111e77a23808fe41fc5`；§10–11 full relevant proof; §1–9 not re-reviewed as primary。
- [288001c1e251d3af65d7 — research/reviews/unrelated_machines/optimal_hull_closed_cycle_review.md](comparison/research/reviews/unrelated_machines/optimal_hull_closed_cycle_review.md)，SHA `6b836d16a7650b5f99cb412e6622ebe9fab9b7ef2ebc320ea0bf647168ea5499`；full source。
- [704e41e5911efe317744 — research/reviews/unrelated_machines/optimal_hull_long_chain_review.md](comparison/research/reviews/unrelated_machines/optimal_hull_long_chain_review.md)，SHA `62bbfd90f4accc6693e19fac024e2031baf530b7dd00a3305aa5b4988d000393`；full source。
- [555810a28cb65428aed4 — tests/audits/unrelated_machines/optimal_hull_closed_cycle_gap.py](comparison/tests/audits/unrelated_machines/optimal_hull_closed_cycle_gap.py)，SHA `325094ac60f993ac38e5a408891e51a01a104de44000ea8e4f49aeaba7df858b`；full source。

复现数据检查时须用另一个新空目录，以绝对路径调用本helper；其输出是expanded-inputs.json/result.json，避免覆盖本目录已有证据。五原入口若以后确需重跑，同样在空目录直接执行冻结脚本并捕获stdout；不能import顶层执行的long independent来取函数。所有原入口无仓库导入、无网络、无随机输入；k/d参数由各main字面域指定。

正文新增两页自足对象：closed整数/BFS与Fraction全最优owner DP；long单最优流、全owner匹配和全cover matching计数。两族一般证明来自已入canonical，原句/版本与新resource不互相授新定理或新审查先验。

