# 一般顺序半覆盖：Boss2 的可接续工作区

目标为 Q-CAG-HALF，精确模型以 `research/current/customer_attraction/model.md` 为准。一般命题仍 OPEN。
发布身份 `R-64201cd12083425899e2d643ec9bc087`；本轮独立 clone 绑定 customer-attraction / boss。凭据留在仓库外。

## 当前研究

六名内部研究员使用 gpt-6.1-sol、ultra 分别研究：一般偏离树/背景利润归纳、真实反例构造、聚合静态安全值、积分与结构表示、完整分支运输、独立问题重构和审查。子目录按研究机制保存，不代表相应结论成立。

| 路径 | 研究作用与读取条件 |
| --- | --- |
| global_proof/ | 一般背景利润与偏离树，查看新归纳义务及真实失败点 |
| counterexample/ | 五人起的多主题真实 SPE 构造、锥优化；须核对完整策略验证范围 |
| security_aggregate/ | 聚合安全值与静态对手背景，区分候选桥及支持限制反例 |
| new_representation/ | 不限人数/目录的新表示与结构类；实验观察不视为定理 |
| branch_transport/ | 保留逐节点偏离行的分支复杂度、对偶与反例模板 |
| independent_attack/ | 独立重构及均匀最优主题偏离接口的攻击 |
| root_payoff/scan.json | 根玩家最小 SPE 收益不控制每个 SPE 的平均收益；小例仅用作立即淘汰该替代指标，非主猜想反例 |

## 状态与下一步

本轮恢复基点 ee77c45ccb7ab5e0d78146eb269664af89ba7129。未提交的非本题文件保持原样；不进入本轮 checkpoint。
优先继续一般证明或真实反例；允许局部债务并共同选择离轨分支乘子。各目录中的候选、实验、完整证明和审查分别标级。形成成熟资产后请独立清洗，并按实际范围更新共享账本；个人备份不自动成为 canonical。
