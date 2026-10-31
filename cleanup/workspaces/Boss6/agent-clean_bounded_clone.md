---
source_id: "f657f78b9f1052a321b4"
source_sha256: "1ba6d22df8f4643dc41b5dc3e8567dc1c80214a7c1acef0146ebe06ac7601779"
source_path: "history/source/notes/unrelated_machines/bounded_multiplicity_clone_author_draft.md"
kind: "cleaning-draft"
role: "Boss6/clean_bounded_clone"
read_status: "full-read-and-compared"
recommended_disposition: "integrated"
recommended_targets:
  - "archives/unrelated-machines/state/定理/有界重数克隆接线与共同循环坍缩--定理.md"
  - "archives/unrelated-machines/state/计算/有界接线的证书实现与有限穷举--计算.md"
---

# f657f78b9f1052a321b4：有界重数克隆作者草稿处置

## 读取和来源核对

使用绑定的 Boss6 clone 和 `clean show f657f78b9f1052a321b4 --out` 导出后全文读取 13,641 字节源。程序返回的冻结元数据为：

- blob `75faab56d65f00c027d44d97adeeec65a88fa547`，mode `100644`
- SHA-256 `1ba6d22df8f4643dc41b5dc3e8567dc1c80214a7c1acef0146ebe06ac7601779`
- 两个来源版本：`68fad804ec5946cb296f77dc5b336308a66abf12:legacy-cleanup` 与 `aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:main`
- 原文题名为“有界重数克隆接线的配置包络与共同循环复制反例”。

源文分成四个数学负载和一个有限审计说明：

1. 定义每个原有限 incidence 由至多 (c) 个（允许重复）置换组成的 (c)-wiring；以 (A_i^c(T)) 和 (MC_c(T)) 表示每行至多 (c) 个同型任务的配置域。
2. 给出 actual schedule 到 (MC_c) 的投影；反向从有理 (MC_c) 证书、共同分母 (q) 构造带全部任务标签的 schedule 和每条 incidence 的 (c) 个置换。关键是使用边的任务副本端度数至多 1、机器副本端度数至多 (c)，按颜色分成 (c) 个部分匹配，再逐色补成全置换；允许不同颜色补出同一条未用边。
3. 给出严格层级族：删去零端类型后，(t_c=t_+) 对所有 (c\ge\lfloor U/p_{\min}\rfloor)；并以 (c+1) 台机、(c) 个全局单位任务和每台 (1/(c+1)) 私有任务证明 (t_c=1+1/(c+1))、(t_{c+1}=1)。
4. 给出共同循环二接线族 (P_m)：一件全局单位任务、每机 (m-1) 件 (1/m) 私有任务；原 (OPT=t_1=2-1/m)，每条 incidence 共用 identity 和循环 shift、(q=m) 时实际展开实例的每台负载恰为 1，故 (t_2=1)。该构造对同一 incidence 图是连通 (2m)-环、平移不变，且不是任意 wiring 都坍缩的结论。
5. 明确这些结果不是一般 (MC_c) 优化器、近二困难性、UM-TARGET-v1 反例或一般 unrelated-machines 算法；显式 (q) 可能指数大，不能由 (log q) 直接宣称输出规模多项式。

## 仓库比较和已有去向

当前结果分支中已存在完整对象：

- [定理对象](archives/unrelated-machines/state/定理/有界重数克隆接线与共同循环坍缩--定理.md)，frontmatter ID 为 `unrelated-machines/bounded-multiplicity-clone-wiring-envelope`，保留 legacy IDs `UM-BOUNDED-MULTIPLICITY-CLONE-ENVELOPE-v1` 与 `UM-COMMON-CYCLIC-TWO-WIRING-NEAR-TWO-COLLAPSE-v1`。该对象逐节保存了源的定义、投影/反向构造、严格层级、共同循环 witness、复杂度边界和开放的 reduction 义务。
- [计算对象](archives/unrelated-machines/state/计算/有界接线的证书实现与有限穷举--计算.md)，frontmatter ID 为 `unrelated-machines/bounded-clone-wiring-certificate-enumeration-audit`，单独保存实现接口、81 图/2448 指派、22 配置阵列/8 分布、严格层级小范围和 zero/empty/unavailable 边界。它明确代码不是一般 MC_c 求解器，也没有把冻结 JSON 当成逐项证书。
- 代码 `tools/evidence/private-tree/bounded-wiring/bounded_multiplicity_clone_audit.py` SHA-256 `0e671a934710df3c542a1e863d339a8eae5a68a5c07807316c1583c7e86a12d9`。
- 独立结构核验脚本和 JSON 为 `tools/evidence/private-tree/structural_witness_check.py` 与 `structural_witness_check.json`；它们只重建共同循环族（及另一个固定 witness），不证明一般定理。

源内容与上述定理对象在数学实体上一致；没有发现尚未入档、且应新建为第三个数学对象的独有命题。建议把这个源标为 `integrated`，以既有定理对象为主目标；源中有限审计叙述的可复现接口已在计算对象中有独立目标，但不要把作者草稿本身当成代码证据。

## 独立复核

本次全文读取现有定理对象、计算对象和审计程序；随后运行：

```bash
python3 tools/evidence/private-tree/bounded-wiring/bounded_multiplicity_clone_audit.py \
  --output <临时新路径>/bounded_clone_replay_child.json
```

运行成功，Python 3.12.14，输出 SHA-256 为 `9681729724c2a5c45f414b13be1be1f79d710c548b82159e2e577342eea4a927`，与仓库计算对象所记录的规范冻结/重放报告哈希相同。实际核验范围和结果：

- (m=2,ldots,17) 的共同循环族：总计 1,784 台机器、21,776 件任务、46,816 条有限边；每台实际负载恰为 1。
- (m=2,q=2) 的 81 个至多二置换接线图完整枚举 2,448 个带标签实际指派；72 图的精确最优值为 (3/2)，9 图为 1；16 个单置换图全为 (3/2)。
- 共同循环 (m=2) 图另行完整枚举 256 个指派，精确最优值为 1；这 256 是重复复查，不应加到 2,448 的去重计数。
- 有理证书到实际接线的转换、(c=1,ldots,4) 严格层级小范围、空任务、零处理时间和不可用端显式零坐标边界均通过。审计明确未实现一般 (MC_c) 优化、未运行大实例完整最优值、未建立 NP-hard source reduction 或 near-two hardness。

这次运行只验证有限代码和固定输入；一般投影/反向构造、最小值取得、严格层级公式以及共同循环族的全称结论仍由定理正文承担。外部同行审查和全局新颖性未认证。

## 处置和回执建议

建议 receipt：

- `disposition`: `integrated`
- `target_objects`: 上述定理对象和（若接收多目标）计算对象
- `read_note`: “完整读取 13,641 字节 frozen author draft；核对 c-wiring、MC_c 投影/反向着色补置换、严格层级、共同 identity/shift 环族与所有复杂度/开放边界。”
- `comparison_note`: “与现有 `unrelated-machines/bounded-multiplicity-clone-wiring-envelope` 及 `bounded-clone-wiring-certificate-enumeration-audit` 逐节比较；源无新增数学对象。源的共同循环族、q<c 允许、重复置换合同和显式 q 规模边界均已在定理/计算对象保留。”
- `evidence_note`: “实际重放 bounded_multiplicity_clone_audit.py；报告 hash `9681729724c2a5c45f414b13be1be1f79d710c548b82159e2e577342eea4a927`；有限结果与计算对象一致。”
- `decision_note`: “标 integrated；不重复新建对象，不宣称一般 MC_c solver、一般 hardness、near-two theorem 或全局 UM 结论。保留源作为历史版本并以其 SHA/commit 绑定。”
- `source_refs`:
  - `source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/bounded_multiplicity_clone_author_draft.md`
  - `source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/notes/unrelated_machines/bounded_multiplicity_clone_author_draft.md`

## 尚未完成的数学义务

该源本身明确留下的开放工作应在接续记录中保留：若要形成困难性结果，必须选择源相关且显式规模多项式的 wiring，保持 YES，并把每一个低负载实际调度解码成源见证；有界度、连通环、平移不变或“存在某个坍缩 wiring”都不提供该解码器。不得把共同循环 (t_2=1) 族升级为任意 wiring、任意随机 wiring 或一般 UM-TARGET-v1 反例。
