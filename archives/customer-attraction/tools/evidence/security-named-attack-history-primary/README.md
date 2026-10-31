# 命名策略相邻钱包与历史边界的证据

正式正文为[静态消项与冻结行价格](../../../state/引理/全相邻退出钱包的静态消项与冻结行价格--引理.md)和[两份命名策略诊断](../../../state/计算/两份命名策略的相邻钱包诊断与历史范围--计算.md)。它们保留有效的静态恒等式、没有分离的两个旧输入、碰撞自由族强弱量词差，以及后来已反驳的相邻钱包候选。原half未被本批反驳；五人已有独立普遍结果，六人仍开放。

本批5主源的实际claim为 a00c34fe9498ab5bc9439b7a1c12d60bccf8805b（parent确认pushed/synced）。[source-manifest](source-manifest.json)逐项记录inventory大小、SHA和两个冻结定位的全字节核验。主源总19871B，三个真实运行输入共39475B。其他原件仅用于数学比较，不额外done。所有保存的原件都在original下保留repo相对路径，未改写源冻结JSON。

| 主源ID | 字节 | 原内容与处置 |
|---|---:|---|
| 2c2fdb99195aa0a9e3ad | 6666 | 命名攻击全文：静态cashout、g/h价格、两packet阴性、碰撞自由族强式锐等号及弱式重配；保其开头后修正与正文旧OPEN的时间差 |
| 1d305bb3f9999d836b5b | 4587 | 独立标准库审计，直接加载三JSON、全有序历史和全部比较元组 |
| c19b4a93560ff473adf5 | 4163 | 全部冻结矩阵/收益/行最大主题/钱包/最优指派/cashout最小值，逐字段保存 |
| 6aca9b93763f751a2cb7 | 2004 | security入口：相邻钱包、旧13算术、安全最优查询固定锥三条不同对象；纠正后续状态但保原文 |
| 6b81f6445e9914b0b550 | 2451 | 旧13同SHA源已在既有反例与计算正文完整吸收，本批duplicate复用并记录真实旧执行，不另造同一对象 |

## 仅一次新原入口

[runtime-input-manifest](runtime-input-manifest.json)包括原入口、两个实例与一个独立完整policy。原入口自己读取这些文件；没有import前代审计。其路径parents[6]依赖保留原research层级，所以新replay-tree放置完整相对路径，不给代码打补丁。

本批新运行仅有命名相邻钱包main；执行记录在[execution](replay/execution.json)，[stdout](replay/stdout.txt)、[stderr](replay/stderr.txt)、[新报告](replay/adjacent_wallet_named_packets.json)分别保留。原入口1次、exit0、用时0.9836061000823975秒；4163B新报告SHA e303ec93699c8ae3d89d87fb301385e2657a831c837e46780343c87d82d407a2，与原报告全字节相同。代码和输入SHA运行前后相同。未运行old13、碰撞自由族程序、一般族程序或最优查询LP。

完整有序决策历史为259+43=302，含自身IC1554+258=1812，非自身IC1295+215=1510；全部比较元组1296+216=1512。原程序不搜索新实例、策略、SPE集合或客户兴趣锥。两份固定策略的IC和静态查询均为精确有理数检查；普遍静态消项另有逐客户证明，不能由这1512个测试取代。

运行工具保存在cleanup工作室的run_original_once.py；它有一次性执行记录保护，不能把重跑包装成同一事件。check_package.py只核记录/字节/数学字段和链接，不运行任何数学原入口。

## 既有旧13执行的明确复用

[reused-old13-evidence](reused-old13-evidence.json)登记既有正式正文、原MD/程序/报告、压缩packet、全自动机执行与alpha-one标量执行的现有路径/SHA。旧13 MD的SHA与本批主源完全相同；现有正式反例已列其source_ref，计算页明确全自动机与标量程序各自承担什么。没有将过去真实执行时间或认证结果回填成本批新事件。

旧13实际 \(P^{10},A,A,B\)，36单位客户、13角色，W33/OPT36。全自动机27243节点（18675决策）、112050含self IC。标量 \(J_{\rm base}=359/66\)，两个指定银行缺口均37/66。基本税、全相邻钱包、真实安全值、完整extra-slot菜单量词分开；这一旧反例不击破half。

## 全仓比较与后修正

完整读当前模型、完整历史SPE终局算法、碰撞自由完整族、静态末对直接式、十客户钱包反例、唯一最优支持一般族及上述两旧13正式正文。原碰撞自由源与security安全最优查询三源完整读作比较；原件保留但本批不done。有限named检查没有被提升成普遍正证；碰撞自由族rowmax锐等号与最优重配Q=W−1分别推导；一般族m≥7严格反证而m6等号也明确保留。

安全查询固定锥原报告是一次浮点优化加恢复点精确可行性核验，未有精确最优对偶证书；本批未执行该脚本、也未声称完成其外部helper依赖审计。README中真实安全最优p的m−1背景总量，与完整m槽extra-slot Mpath相异。原代码比较、原报告阅读、定义级精确新运行、内部复核和外审身份分别记录。

过去另一批曾有无关的非MD广域grep在中断后报下列错误，exit130；那次没有观察到目标401/403、登录或凭据挑战。已停止该探测，未重试认证或换凭据。

    fatal: unable to access 'https://github.com/SOMEBODYJUN/co-work-anl.git/': Proxy CONNECT aborted

本批必要冻结blob读取均本地、设置GIT_NO_LAZY_FETCH=1，不依赖额外非MD远端扫描。该历史错误不是本批原审计失败。

[verification](verification.json)、工作室逐源receipt、数学自查、关系说明和候选清单一并交付。正文与必要证据先由Boss串行保存，完成登记由Boss处理；本stage不进行Git写入或done。
