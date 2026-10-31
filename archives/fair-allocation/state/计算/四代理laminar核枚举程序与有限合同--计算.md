---
id: "fair-allocation/four-agent-laminar-key-enumeration-program"
kind: calculation
type_tag: 计算
title: "四代理 laminar 核枚举程序与有限合同"
status: "finite-exact-program-retained; universal-existence-open"
truth_status: "finite-evidence"
source_refs:
  - "clean:2c5467ccde544c41791a:history/retired_topic_selection/multi_lane/research/topic_selection/probes/boss0_laminar_keys.py"
  - "workspace:cleanup/workspaces/Boss3/root/boss0_laminar_keys.py"
evidence_paths:
  - "archives/fair-allocation/tools/evidence/retired-topic-selection-20261031/boss0_laminar_keys.py"
related_objects:
  - "../审查/四代理laminar核有限枚举与顺序独裁障碍--审查.md"
---

# 程序身份和合同

本对象保存完整读取的 boss0_laminar_keys.py。程序自称 finite exact-integer oracles for ordered EF1 on the two published key matroids；它明确只评价有限 valuation profiles，不回答 universal existence。输入合同是四代理、正整数类别大小不超过四、完整分配、每人容量与总物品数相匹配；估值必须是 [0,10^6] 内整数，不接受负值、浮点或过大数。

allocations() 通过每类向四代理的全单射积枚举，再筛掉每人容量不符的行；run() 另以逐件 4^8 归属枚举八物品核验证分组枚举。check_profile() 逐个分配计算每位评价者对各包的效用、EF1 和指定顺序 ordered no-envy，并逐代理最大化自身效用得到 serial dictatorship 的并列集合。direct_check() 独立按包逐项删除一个物品重算 EF1。

## 有限域和断言

程序固定 seed=20261020；八物品核 (3,3,2) 产生
\[
4\cdot3\cdot(3!)^2\cdot2!=864
\]
个可行分配，十二物品核 (3,3,3,3) 产生
\[
4!\cdot(3!)^4=31104.
\]
八物品测试包含全零、单位、稀疏共同 profile、模3 profile 和 80 组随机整数，合计 84 个；十二物品为 4 个固定加 12 个随机，合计 16 个。程序检查八物品 labelled enumeration 与分组枚举集合相等，断言上述计数，并拒绝四类非法 key 与五类非法估值输入。

对于列出的所有 profile，程序要求至少一个 ordered_ef1 witness；八物品前八个 profile 还用 direct_check 对全部枚举逐项交叉。输出含 source_sha256、Python/NumPy 版本、无效输入计数和 serial_failure。原始脚本已复制到 evidence 目录，未改写冻结源码。

## 证据边界

这些断言是精确整数域内的有限程序合同：它们证明指定核、指定估值集合和指定顺序上的枚举结果，不能推广到任意连续或无界估值，也不能代替 Cookson–Shah 从一般 laminar 实例到两个核的完整约化。serial_failure 只说明顺序独裁模板在某个有限 profile 上失败，不否定共同分配存在，也不证明复杂度下界。任何后续重跑都应在临时副本输出新 JSON，不能覆盖冻结证据。

该程序与审查对象共同保留“有限证据、失败机制、未闭全域义务”三层；第三阶段如建立关系，应把程序输出和数学证明分开引用。
