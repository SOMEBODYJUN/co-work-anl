# 研究问题与候选：先区分仍开放和已经闭合

当前主攻是[加权原子拥塞的普遍门槛](weighted_congestion/README.md)。本目录还保留设施选址与顺序客户吸引的独立问题。文件留在 questions 可以是候选、未解义务或原问题合同，不能只凭路径判定它仍未解决。

## 仍有明确缺口的问题

| 中文问题名 | 当前缺什么 | 对应结果入口 |
| --- | --- | --- |
| [加权原子拥塞：全类存在界与更强非存在机制](weighted_congestion/README.md) | 仍缺与奇环下界匹配量级的全类上界，或越过现有局部证书的新机制；势函数/端点/两列轨道稿按实际待审等级读取 | [当前数学资产](../current/weighted_congestion/README.md) |
| [顺序客户吸引：任意完整纯 SPE 的半覆盖](customer_attraction_half_coverage.md) | 小人数与目录结构结果没有覆盖一般情形；需一般全局支付或真实分支转移 | [已证子类、工具与失败桥](../current/customer_attraction/README.md)、[两条具体攻坚接口](customer_attraction_general_handoff.md) |
| [任意设施数：一般输入的位多项式盒内 NE 构造](greedy_box_polytime.md) | 完整盒存在和有限构造已内部闭合；一般输入多项式总时间或直接构造仍缺 | [多设施成果地图](../current/multi_facility/README.md) |
| [共同目录双设施：实例最优倍率 EPTAS](shared_alpha_eptas.md) | 近带补全已有工具，完整全局误差、精确续局与位复杂度合同尚未闭合 | [共同目录复杂度与算法](../current/shared/README.md) |
| [多设施：最优统一常数、恰三设施与特定布局形式](three_facilities.md) | 原有无统一常数问题已回答；锐值、多项式构造与特定布局形式须各自处理 | [因子二与完整盒](../current/multi_facility/README.md) |
| [立方期望客户成本：双设施普遍阈值](cubic_costs.md) | 需要真实立方均衡 oracle 与全局机制；线性混合均衡等价不能直接沿用 | [线性模型与费用扩展](../current/local_and_exact/README.md) |

## 原问题已获内部答案，仍保留边界与审查入口

| 原问题 | 现在已知什么 | 仍不能声称什么 |
| --- | --- | --- |
| [单交叠、任意长异构目录的尖锐阈值](sparse_catalogs.md) | 任意长目录的锐阈值已有内部一般证明；原探索路线用于追溯机制 | 不自动解决一般多交叠异构目录，也不代表外部评审或新颖性认证 |
| [共同目录双设施固定倍率判定](instance_complexity.md) | 三/五地点固定倍率的全局弱 NP 完全性、参数算法与小目录阶梯已有内部结果 | 不自动完成恰三/四地点高倍率细分类或新的输入倍率合同 |
| [任意设施数有无统一常数](three_facilities.md) | 因子二存在性与有限构造已内部闭合 | 有限终止不等于位多项式，布局规则障碍不等于全类锐性 |

新研究从[当前路线](../ROADMAP.md)选真正未闭合的义务；全部文件的[中文名字与用途](../CATALOG.md)可以反查。形成可复用候选后按[入库规范](../GROWTH.md)保存实际等级，不能把问题文件的探索计划当成已经存在的代码或证明。
