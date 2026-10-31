---
id: "unrelated-machines/long-path-gap-small-instance-input-review"
kind: "review"
type_tag: "审查"
title: "长路径小实例配置证书输入的范围审查"
status: "source-read-ready-for-integration"
truth_status: "finite-configuration-feasibility-input-only"
review_level: "full-source-read-and-related-certificate-reconciliation"
scope: "UM-MODEL-v1 sparse two-eligible instance; k=3; path_length=3; 16 machines; 19 jobs"
summary: "冻结输入包含三层稀疏长路径和两端分支，共16台机器、19个二可选任务。对应的16份配置分布证书目标为4/3；源及既有证书明确这是可行性见证，不是最优性或普适配置-gap 证明。"
source_id: "35d2b666346494bfb6a2"
source_sha256: "4a96cfbb10e5c3d61bb4bf8dbe146d39e038078a8d0afbf704a4cc2253d3c3b5"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:examples/unrelated_machines/long_path_gap_small_instance.json"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:examples/unrelated_machines/long_path_gap_small_instance.json"
related_evidence:
  - "archives/unrelated-machines/tools/evidence/clean-batch-config-certificates/e4c3b8e6f1e404c0ec96.raw"
  - "archives/unrelated-machines/tools/evidence/clean-batch-config-certificates/manifest.json"
---

# 来源身份与输入结构

本源是 `examples/unrelated_machines/long_path_gap_small_instance.json` 的冻结输入夹具，源 ID 为 `35d2b666346494bfb6a2`，SHA-256 为 `4a96cfbb10e5c3d61bb4bf8dbe146d39e038078a8d0afbf704a4cc2253d3c3b5`，两个冻结提交的路径和字节一致。JSON 声明 `UM-MODEL-v1 sparse two-eligible instance; omitted entries forbidden`，参数为 (k=3)、`path_length=3`，机器数为 16，作业数为 19。

每个作业只在两个端点机器上可处理，处理时间为有理数 `1` 或 `1/3`。前半部分从机器 0 经过三个长度三的分支到机器 2：主链为 (0	o3	o4	o2)，另外两条链为 (0	o5	o6	o2) 和 (0	o7	o8	o2)。后半部分从机器 1 经过三条对应分支到机器 9：(1	o10	o11	o9)、(1	o12	o13	o9)、(1	o14	o15	o9)。每条链的首段作业在入口处具有 (1/3) 的快端点，内部和末端作业时间为 1；输入没有省略项，因而必须按完整端点列表解释资格关系。

# 与冻结配置证书的对应

既有证据 `e4c3b8e6f1e404c0ec96` 明确把该输入作为 `long_path_gap_small_instance.json` 的输入，并保存目标配置值 (4/3) 与 16 个 `configuration_distributions`。每份分布只使用当前输入中的 job 编号和有理权重（例如 (1/2,1/6,1/3,2/3)），权重和为一；因此它们是该具体输入上的配置可行性见证。证据 manifest 同时保存输入哈希与配置证书哈希，输入关系与本次 `clean show` 导出的哈希一致。

证据文本和既有审查明确区分两个命题：

1. 给定的 16 份配置分布达到目标 (4/3)，说明该目标在这个有限实例上可行；
2. 整数调度的真实最优值以及“配置值与整数最优之间存在某个 gap”的上界，需要另一个输入侧枚举或完整最优性证书。

本输入本身没有列出配置求解器、整数最优枚举或证明“(4/3) 是最小可行配置值”。因此不能仅凭此 JSON 把 (4/3) 称为全局最优，也不能把该数值推广到所有 (k)、所有路径长度或所有二可选稀疏实例。

# 量词、模型边界与接续

该对象属于 unrelated-machines 模型，必须和 customer-attraction 的共同目录/客户分摊模型保持独立。它不是顺序 SPE 实例，也不含提供者历史、客户福利或六人 half 覆盖量词。它的用途是作为长路径配置可行性输入和有限 gap 证据的原始 fixture，供既有“未归档配置证书批次与量词边界”审查引用。

建议将本源 `integrated` 到既有审查和 `clean-batch-config-certificates` 证据 manifest，保留输入哈希与配置证书的对应关系；不新建重复定理。若后续需要把它用于配置-gap 结论，必须同时给出整数最优值的来源、穷举范围、配置可行域定义和有理最优性/下界证明。当前应保留为有限可行性输入，不升级成一般近似界或主线六人结论。

复现边界：

```sh
python3 tools/cleanup.py --repo . show 35d2b666346494bfb6a2 --out cleanup/workspaces/Boss5/long_path_gap_small_instance.json
sha256sum cleanup/workspaces/Boss5/long_path_gap_small_instance.json
```

本次实际读取输入、相关证据和既有审查，未把配置证书当作已运行的优化器证明，也未改动正式 Git 文件。
