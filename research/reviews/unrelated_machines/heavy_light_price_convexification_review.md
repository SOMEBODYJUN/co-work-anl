# 机器价格凸化的独立重构与冻结审查

目标 `UM-TARGET-v1` 仍 OPEN。本审查仅认可 `UM-HEAVY-LIGHT-PRICE-CONVEXIFICATION-v1` 的精确接口综合：网络流凸包/价格等价、剪枝后joint supgap2、未剪枝固定m锐界m和最优价格共同big面成功证书。它不是外部同行评审、全球新颖性或一般调度突破认证。

## 审查过程与准确归属

基准main：`ede1392dd5ea07457f188865a5f72fe8eb194409`。原min–max候选来自该提交，作者归属保留；boss3本阶段独立重构其精确凸包并整理新定理。内部构造者与另一独立攻击者均在阅读新证明前收到精确statement，自行重构网络流、ST首槽和两树唯一light端；后者曾读过原两机候选，因此不声称从未见相关背景。随后完整读取冻结新正文和代码，主研究者逐项回算。

第一个全文冻结版本正文hash为 `f430c444234be48eba10ef1cee8c225122cf34cd2e407aaeafca2c7a2370793e`，代码hash为 `1d4a7dc84f7d97976023348662e02eb490abd42f21f931969236e9d203390727`。审查未发现fatal，给出三个nonfatal：用任意小s写非最优价格扰动；非空全零配置走无anchor；正式代码补真正fractional-light共同面恢复、强制big反值检验及Q非空但容量失败例。以上均已修补，当前发布冻结hash见下表。旧临时输出留在clone外，不作为另一份长期资产重复入库。

## 当前冻结对象

| 路径 | SHA256 |
| --- | --- |
| research/current/unrelated_machines/heavy_light_price_convexification.md | b63dd00ddb4f202b21988ce1703b19f90d4f703815bdf1e5982a4e7f5045d0b9 |
| tests/audits/unrelated_machines/heavy_light_price_convexification.py | d5515cc282f2dd64d15e701678c2cf881990da2862444a92d5469be20fdb2ee7 |
| evidence/runs/unrelated_machines/heavy_light_price_convexification_release_audit.json | 82c5d76407d0f635f46b77671673b55f1d39b3cbc3984609b71f424d06fdc314 |

## 承重证明攻击

1. **角色必须在初始T固定。** 部分big匹配可选择有light端任务，但必须覆盖无light端任务。无可行H时min为+∞，不能在λ=0时伪通过；∞先排除，不出现0乘∞。β≥1/2与严格big号保证真实T调度每机至多一个big，故LP失败可靠推出OPT>T。
2. **价格到底凸化什么。** 去掉负载后是任务→big机器容量1/无限light出口的整数流多面体。它的全部整数顶点允许不同H；全部非负价格只分离其负载凸包。H固定时Farkas是准确的，交换量词才丢掉共同整数选择。
3. **上界必须同时保big和负载。** big时间严格在light之前且总质量≤1，所以只触第一单位槽；整个ST匹配每机至多一个big。剪枝才给maxp≤T。不允许先只舍light来代替这项证明。
4. **两树下界两向。** k>β/(1−β)使time1为big、1/k为light；每job唯一light端或无light端，故共同见证是整数调度。已知OPT=2−1/k<2又保证反向最优调度big部分为匹配，Γ确等于OPT。下界是经典gap直接推论，不是promise失败或UMhardness。
5. **无剪枝固定m。** 单任务m端时间mT达到m；λ全1与整数费用流给总工作量≤mT，从而上界m，m=1亦成立。
6. **最优面出口。** 任一primal最优点都在精确dual价的最小费用面；若面内所有整数顶点big相同，primal也big整数。每条big边反值费用测试恰能发现任一不同big向量。任意非最优价的唯一响应不够，检查失败不能判OPT>T。
7. **anchor与位长。** a>0没有统一正下界；空或全零配置不能强行取正anchor。一般局部凸化仍含CONFIG。全部有理LP/费用流与ST论证按显式输入位长；有限枚举未冒充一般solver。

## 实际核验与限制

正式命令：`python3 tests/audits/unrelated_machines/heavy_light_price_convexification.py > <new scratch output>`。Python版本、代码hash、精确结果沿冻结JSON读取；所有运算为Fraction，无随机seed。

有限核验包括：独立有理primal顶点枚举与二机dual全部折点比较；参数化量词例含接近1的大分母β；零/空任务、混合角色、单可用端、底层heavy冲突和Q非空的容量冲突；保H后仅舍light并独立回算τ+βT；逐big强制反值oracle；非最优价唯一响应负控制；两棵实际小树的原矩阵全分配与共同见证值；较大k只作门槛/代数恒等式，不展开大树。

独立攻击者另用自己scratch脚本核保H恢复，anchor4/5、三个2/5 light例的τ=1，实际负载(6/5,4/5)≤17/10；随后正式代码纳入同一行为。有限结果不证明一般命题。正式audit仍是指数小oracle/给定见证程序，未集成通用LP或价格费用流solver。

**结论：上述精确范围未发现仍成立的fatal objection。** 原问题仍缺可计算的非可加共同容量或实际联合舍入，以及全输入可靠FAIL/统一ε和总进展。正确性、复用价值与新颖性分别判断。
