---
id: "customer-attraction/Ra0-background-near-saturation-audit"
kind: "review"
type_tag: "审查"
title: "Ra0 背景近饱和审计脚本"
status: "finite-examples-replayed-with-external-case-missing"
truth_status: "finite-arithmetic-audit; no-universal-BNS-or-half-theorem"
summary: "冻结脚本对指定完整纯 SPE 证书的所有有序节点，用 Fraction 审计 BNS 候选不等式、任意主题查询和实际后继分支；7 个内置有限实例完成，随后因引用的外部 nonpne_best.json 不在当前可读来源而停止。"
source_refs:
  - "clean:b2193e7b539b0b40ef69:research/workspaces/customer-attraction/R-a0bb57fa24044a8794bc7991918a19c6/credible_counterexample/background_near_saturation_audit.py"
  - "local:archives/customer-attraction/tools/evidence/Ra0-py1-agent/manifest.json"
  - "local:archives/customer-attraction/tools/evidence/Ra0-py1-agent/partial_rows.json"
evidence_paths:
  - "archives/customer-attraction/tools/evidence/Ra0-py1-agent/background_near_saturation_audit.py"
  - "archives/customer-attraction/tools/evidence/Ra0-py1-agent/customer_attraction/"
  - "archives/customer-attraction/tools/evidence/Ra0-py1-agent/replay.stdout"
  - "archives/customer-attraction/tools/evidence/Ra0-py1-agent/replay.stderr"
  - "archives/customer-attraction/tools/evidence/Ra0-py1-agent/partial_rows.json"
  - "archives/customer-attraction/tools/evidence/Ra0-py1-agent/manifest.json"
---

主源是 6,370 字节的 Python 审计脚本，SHA-256 为 `ddf71f2c3696123ec177dee97246b0158e9539769bb4f2eeb944d2a2e285b972`。脚本导入 ExactSPESolver 与 `verify_certificate`，不把策略限制为按计数状态的 Markov 策略；客户重数作为独立单位克隆处理。

对给定实例和完整策略证书，脚本先验证每个有序历史和偏离动作的纯 SPE 证书，然后对剩余人数 `k≥2` 的节点计算实际路径、客户背景负载、`M=k+max(b)`、`w_j=1/(b_j+k)`、最坏背景值 `K` 和当前动作收益 `u`。它用精确 Fraction 检查候选 BNS 不等式、任意主题查询对、实际最大化客户的后继分支、最后一位偏离以及饱和时的支持一致性；同时记录最小松弛、非 Markov 计数类和比较对数量。

在隔离证据目录运行原脚本并接入冻结 ExactSPESolver 依赖，先完整通过 7 个内置实例：空客户、共同重复客户、大私有客户、稀疏 `(m,p)=(3,4),(4,5),(5,7),(6,4)`。每个实例的 `definition_verified_histories` 与 `definition_verified_deviations`、候选 BNS 检查和任意查询检查均完成；记录的 `minimum_BNS_slack` 均为 0，说明存在等号节点，并不说明严格不等式。随后脚本尝试读取外部 `R-84ce8a8709e34ea6af94f99991d3c2e3/counterexample_search/nonpne_best.json`，该文件不在当前证据范围，程序以 `FileNotFoundError` 停止；因此不能把最后一个案例或全批运行宣称完成。

该对象是有限算术审计和实现边界记录。它没有证明 BNS 对所有客户模型、所有完整纯 SPE 或所有六人历史成立，也没有推出 Q-CAG-HALF-6 的半覆盖结论。后续需要取得缺失的 `nonpne_best.json` 后重跑，或单独构造完整证书；同时保持 `minimum_BNS_slack=0` 的等号节点和非 Markov 分支信息，不把有限通过升级为普遍定理。

## 所引用非PNE输入的当前保全位置

原外部R84 `counterexample_search/nonpne_best.json`现已按冻结源完整取得，见[五人七主题固定整数见证](../计算/五人七主题非静态均衡完整策略的整数见证--计算.md)及其原件闭包。该保存点包含1992009名不同单位客户、2801个完整有序历史动作；一次新定义级整数审计确认其SPE和静态4→0正偏离，W1250000、OPT1992009。

这只补足当时缺少输入的当前来源链。本页旧FileNotFoundError/未执行generate的历史记录继续成立；本次没有重跑本页原程序、随机生成流程或BNS/AP公式检查，因此不能把输入到位写作本页全批复现成功或普遍引理证明。
