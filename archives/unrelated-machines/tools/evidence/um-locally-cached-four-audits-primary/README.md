# CN 四份本地冻结原程序的实质整理

实际claim pushed/synced650271925f9e1dc7d0a722967b07597c4f479a58，四owner逐项Boss4/in-progress核验。Root提供纯本地blob，本站只读/复制本地文件，独立核size/SHA256/Git blob SHA1；未调用clean show/Git/network。CM五源输入缺失记录仍是未完成，不由CN替done。

原CLI各一次、全exit0、Python3.12.14，标准Fraction/整数。4 source CLI=4审计体（tree一份顶层、其它三份guarded）；额外CLI0、supplemental数学0、helper main0、imported unguarded审计体0。unique加载helper/baseline函数定义并在块内用height，不执行它们main。四份完整stdout/stderr/argv/cwd/时长和execution manifest保全；无子进程隐藏计数。

## 自足对象

- [两条小资格整数流的原容量表与逐阈值审计--计算.md](../../../state/计算/两条小资格整数流的原容量表与逐阈值审计--计算.md)
- [五机树Markov主原程序的顶层枚举与完整边际--计算.md](../../../state/计算/五机树Markov主原程序的顶层枚举与完整边际--计算.md)
- [唯一小端三维匹配的源程序与条件块切面--计算.md](../../../state/计算/唯一小端三维匹配的源程序与条件块切面--计算.md)
- [对称固定推前独立原程序的计数轨道与同边际修复--计算.md](../../../state/计算/对称固定推前独立原程序的计数轨道与同边际修复--计算.md)

## 原件、依赖与比较

- [source-manifest.json](source-manifest.json)
- [root-local-input-manifest.json](root-local-input-manifest.json)
- [actual-owner-verification.json](actual-owner-verification.json)
- [claim-confirmation.json](claim-confirmation.json)
- [dependency-manifest.json](dependency-manifest.json)
- [comparison-manifest.json](comparison-manifest.json)
- [historical-comparison-and-version-scope.json](historical-comparison-and-version-scope.json)
- [mathematical-execution-scope.json](mathematical-execution-scope.json)
- [relation-review.json](relation-review.json)
- [artifact-manifest.json](artifact-manifest.json)
- [delivery-self-check.json](delivery-self-check.json)
- [verify_delivery.py](verify_delivery.py)
- [00d731603b0001b80486 tests/audits/unrelated_machines/symmetric_reset_independent.py](original/tests/audits/unrelated_machines/symmetric_reset_independent.py)
- [2171ba148bfb1f9ac193 tests/audits/unrelated_machines/tree_markov_completion.py](original/tests/audits/unrelated_machines/tree_markov_completion.py)
- [4e687930a16eef8a9594 tests/audits/unrelated_machines/two_small_incidence_flow_audit.py](original/tests/audits/unrelated_machines/two_small_incidence_flow_audit.py)
- [c5d61da8d28020d9e9b5 tests/audits/unrelated_machines/unique_small_matching_audit.py](original/tests/audits/unrelated_machines/unique_small_matching_audit.py)
- [30bcde3e1f48ab5c0e63 tests/audits/unrelated_machines/joint_matching_completion.py](original/tests/audits/unrelated_machines/joint_matching_completion.py)
- [e57947bc795251d373c3 tests/audits/unrelated_machines/rounding_and_gap.py](original/tests/audits/unrelated_machines/rounding_and_gap.py)
- [2dd3413231d9b1499f4c tests/audits/unrelated_machines/heavy_matching_residual.py](original/tests/audits/unrelated_machines/heavy_matching_residual.py)
- [afd52ee890bac94b4bf8 research/current/unrelated_machines/symmetric_moment_reset_and_single_machine_threshold.md](comparison/research/current/unrelated_machines/symmetric_moment_reset_and_single_machine_threshold.md)
- [78feb63e463faf4700e7 research/reviews/unrelated_machines/symmetric_moment_reset_review.md](comparison/research/reviews/unrelated_machines/symmetric_moment_reset_review.md)
- [310a8c401a6f5bff9a69 evidence/runs/unrelated_machines/symmetric_moment_reset_audit.json](comparison/evidence/runs/unrelated_machines/symmetric_moment_reset_audit.json)
- [41a27cbaee8b545450e6 evidence/runs/unrelated_machines/symmetric_reset_independent_formatting_rerun.json](comparison/evidence/runs/unrelated_machines/symmetric_reset_independent_formatting_rerun.json)
- [9e66cf0e6411197f7a23 research/current/unrelated_machines/tree_markov_completion.md](comparison/research/current/unrelated_machines/tree_markov_completion.md)
- [4975658e3ef8ba0c8506 research/reviews/unrelated_machines/tree_markov_completion_review.md](comparison/research/reviews/unrelated_machines/tree_markov_completion_review.md)
- [72369fac674ccdc4c862 evidence/runs/unrelated_machines/tree_markov_completion_audit.json](comparison/evidence/runs/unrelated_machines/tree_markov_completion_audit.json)
- [4793fd8514c206c37797 evidence/runs/unrelated_machines/independent_tree_markov_completion_audit.json](comparison/evidence/runs/unrelated_machines/independent_tree_markov_completion_audit.json)
- [8880cf5284ef95a424b1 research/current/unrelated_machines/joint_slot_prefix_rounding.md](comparison/research/current/unrelated_machines/joint_slot_prefix_rounding.md)
- [427a196bda944014458f evidence/runs/unrelated_machines/two_small_incidence_flow_audit.json](comparison/evidence/runs/unrelated_machines/two_small_incidence_flow_audit.json)
- [8416c0f705c62b5a68e5 history/source/notes/unrelated_machines/two_small_incidence_sharp_v2_exact_statement_source.md](comparison/history/source/notes/unrelated_machines/two_small_incidence_sharp_v2_exact_statement_source.md)
- [1d8914155d1a253adfa9 research/current/unrelated_machines/joint_matching_completion_and_block_cuts.md](comparison/research/current/unrelated_machines/joint_matching_completion_and_block_cuts.md)
- [bc969f57611eec4af74d evidence/runs/unrelated_machines/joint_matching_completion_audit.json](comparison/evidence/runs/unrelated_machines/joint_matching_completion_audit.json)

## 原入口和完整输出

- `symmetric-reset`：exit0，0.723945s；[stdout](runs/symmetric-reset.stdout)、[stderr](runs/symmetric-reset.stderr)、[execution](runs/symmetric-reset.execution.json)。
- `tree-markov`：exit0，0.034095s；[stdout](runs/tree-markov.stdout)、[stderr](runs/tree-markov.stderr)、[execution](runs/tree-markov.execution.json)。
- `two-small-flow`：exit0，16.727434s；[stdout](runs/two-small-flow.stdout)、[stderr](runs/two-small-flow.stderr)、[execution](runs/two-small-flow.execution.json)。
- `unique-small`：exit0，16.478604s；[stdout](runs/unique-small.stdout)、[stderr](runs/unique-small.stderr)、[execution](runs/unique-small.execution.json)。

[execution-manifest](runs/execution-manifest.json)。历史比较五条全部结构比较：当前reset格式重跑、tree、two-small和unique全字段同；旧reset仅codeSHA字段不同，源码一空格逆核准确。仅tree与旧主输出逐字节同；小资格回执格式不同，JSON全同，不用字节同替代实际新运行。

## 说明修正建议与范围

[errata说明](errata/README.md)、[before/proposed/patch manifest](errata/manifest.json)、[proposed](errata/two-small-page-proposed.md)、[patch](errata/two-small-page.patch)。只是供Root维护旧有限页的两处说明，不覆盖共享目标、不改旧done或源码。

reset一般阈值和同Rx修复、tree固定每态反例、common-b容量表/候选流、unique1/3归约和末块各保模型；当前half-unit/随机reset后加节不冒成本轮程序执行。finite counts不替一般证明，实际历史读序不倒填blind，所有其它sourceIDs仅依赖/比较。

## 冻结正式比较快照

- [强配置矩与对称重置阈值有限审查--审查.md](formal-comparison/强配置矩与对称重置阈值有限审查--审查.md)
- [对称重置与双见证查询双源审查--审查.md](formal-comparison/对称重置与双见证查询双源审查--审查.md)
- [五机树Markov再耦合补全反例最终审查--审查.md](formal-comparison/五机树Markov再耦合补全反例最终审查--审查.md)
- [五机树Markov独立原程序的逐态最优补全--计算.md](formal-comparison/五机树Markov独立原程序的逐态最优补全--计算.md)
- [每机至多两条小资格的三半审计--计算.md](formal-comparison/每机至多两条小资格的三半审计--计算.md)
- [共同大边补全双原程序与三分之一版本边界--计算.md](formal-comparison/共同大边补全双原程序与三分之一版本边界--计算.md)

[四条语义receipt](../../../../../cleanup/workspaces/Boss4/r3-um-locally-cached-four-audits-primary/semantic-receipts.json)、[精确copy白名单](../../../../../cleanup/workspaces/Boss4/r3-um-locally-cached-four-audits-primary/copy-files.json)、[下一本地元数据候选](../../../../../cleanup/workspaces/Boss4/r3-um-locally-cached-four-audits-primary/next-candidates.json)。验证器只读保存字节/完整JSON/链接，执行数学程序0；stage exact tree，repo只查列明文件存在。
