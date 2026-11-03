---
id: "fair-allocation/four-agent-laminar-key-frozen-result-20261020"
kind: calculation
type_tag: "计算"
title: "四代理 laminar 核冻结结果与程序一致性"
status: "finite-exact-result-retained; universal-claim-open"
truth_status: "finite-evidence"
source_refs:
  - "clean:e7b9b839ffb859124b0a:history/retired_topic_selection/multi_lane/research/topic_selection/probes/results/boss0_laminar_keys_20261020.json"
  - "clean:2c5467ccde544c41791a:history/retired_topic_selection/multi_lane/research/topic_selection/probes/boss0_laminar_keys.py"
evidence_paths:
  - "archives/fair-allocation/tools/evidence/retired-topic-selection-20261031/boss0_laminar_keys_20261020.json"
  - "archives/fair-allocation/tools/evidence/retired-topic-selection-20261031/boss0_laminar_keys.py"
related_objects:
  - "四代理laminar核枚举程序与有限合同--计算.md"
  - "../审查/四代理laminar核有限枚举与顺序独裁障碍--审查.md"
---

# 冻结结果身份

本对象完整读取冻结结果 `boss0_laminar_keys_20261020.json`，源大小 1672 bytes，SHA-256 为 `039c54a3112104a7d83f8bcfb4875dc305806c79c053d968f1e75246522f3ddc`。结果引用程序 `boss0_laminar_keys.py`，其源 SHA-256 为 `a73529953764a83b89f12a2f5327b93ab79381c3be495f221c4b54c01baa47ad`。两者均按原字节复制到 evidence；结果中的 Python 3.12.14、NumPy 2.3.5、精确 int64 输入上限、seed 20261020 和 source_sha256 字段与程序登记相符。

JSON 声明的是有限观察，不是普遍定理：`status` 为 finite observation only，算术为 exact int64，输入值至多 `10**6`，bundle size 至多 3，且没有连续/无界估值、浮点 LP 或一般 laminar 约化。

# 可复核的有限计数

四代理八物品核的类别大小为 `(3,3,2)`。程序枚举的可行分配数是 864，profile 数是 84，最小 good count 是 16，zero_good 为 0。十二物品核的类别大小为 `(3,3,3,3)`，可行分配数是 31104，profile 数是 16，最小 good count 是 651，zero_good 为 0。结果还记录 `invalid_inputs_rejected=9`，与程序的非法输入检查合同一致。

“good”只表示在该 profile 的有限完整分配枚举中找到满足指定 ordered-EF1 检查的 witness。该标签没有把所有 profile 归入一个连续估值域，也没有证明 witness 可由统一算法生成。

# 顺序独裁失败观察

结果中的 `serial_failure` 对应八物品核中的一组固定顺序独裁轨迹：其记录的序列为 `[1,2,3,1,2,3,1,2]`，可行分配数仍为 864，ordered-EF1 计数为 92，但 serial_good_count 为 0；程序保留一份 serial_witness `[2,1,0,3,1,0,3,2]` 作为失败机制的具体标号。

这只说明该有限 profile 上的朴素全局顺序独裁模板没有命中 ordered-EF1 witness。它不否定共同分配存在，不否定其他顺序/交换/随机算法，也不构成复杂度下界。

# 与相邻对象的关系和边界

本结果把程序对象中的有限枚举数字、serial_failure 和输入/版本字段落到可独立引用的冻结输出；程序对象保留枚举实现与断言，审查对象保留模型解释和与一般 laminar 约化的缺口。三者不能合并为“所有 laminar 估值都有共同 EF1”或“顺序独裁必败”的一般命题。

后续重跑必须复制脚本和 JSON 到临时目录，记录新的 source SHA 与 profile 范围，并生成增量对象；不能覆盖本冻结证据。第三阶段若建关系，应使用“有限输出支持审查”关系，不把有限观察直接升级为定理、hardness 或新颖性证明。
