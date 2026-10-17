# 残余通过量格结构与占位图表示的独立审查

`UM-TARGET-v1`仍OPEN。本审查覆盖 `UM-RESIDUAL-THROUGHPUT-LATTICE-v1` 与 `UM-OCCUPATION-INDUCED-EDGE-DEFICIT-v1` 的完整声明范围；未发现仍成立的fatal objection。证明、有限计算、实现及新颖性分别判断，不是外部同行评审。

## 实际独立过程与冻结范围

基准main为`3b5575a94d905a35d12c7bd12df29895d57fa85e`。一个内部研究者先推导任意异端固定R的对偶格封闭，另一个先构造严格次二占位的任意独立集投影。独立攻击者在读最终证明前收到两个精确statement，自行以dual max函数格性质重构第一项、以padding容量重构第二项，并提出更精确的D=e(I)恒等式。图构造者随后独立攻击这项公式，明确上界必须允许牺牲padding，并从实际P加整数最大流验证；主研究者统一重写并亲自核对。

之后独立攻击者完整读取最终正文及两份代码、复跑正式审计。审查不宣称从未读过旧共同容量背景，也未把同一研究者重复执行计为多组独立评审。来源原PDF定位由构造者与主研究者执行，独立攻击者本轮未重新读原文，不在其审查覆盖内。

| 路径 | SHA256 |
| --- | --- |
| research/current/unrelated_machines/residual_throughput_and_occupation_projection.md | 2c0c8001e0c2313bdcad7ca434e8a16688f10488aa050ff9390ab642fa9a295e |
| tests/audits/unrelated_machines/residual_throughput_lattice.py | 66677a73831484233020020b89df6e21c18e71e9e1b3bd37d7d5e74d3830f12a |
| tests/audits/unrelated_machines/occupation_induced_edge_deficit.py | 5d2b822bf18e0ea081a2627b755d248f855d2a003b169cb0818e80509bc6f966 |
| evidence/runs/unrelated_machines/residual_throughput_lattice_release.json | faf7ac1bd3e95e2e4345466f31a128483d6023532c52046c4e7d884d51f3bff6 |
| evidence/runs/unrelated_machines/occupation_induced_edge_deficit_release.json | 2070d39d86c82673779a6505ef0df6d0b92713af8bcb4d940822eca399df4d94 |

## 承重攻击及已处理问题

- **格不等式方向。** 对偶可行集在(u∧v,a∨b)、(u∨v,a∧b)混合下封闭；配对c∨d与较小u才能得到正确重排方向。允许异端p、零时间/容量、孤立任务；没有偷偷改为共同job size。取最优有理dual及强对偶的条件满足。
- **零边解释。** F_R=|Z|+F_{R\Z}只在原机集保留、剩余容量改变时给免费任务预处理；物理删机另有资格语义。容量0不能排零时间边。空R/无资格均覆盖。
- **固定R不可省。** 2×2原P的F明确只用固定交叉light资格；否则剩余任务仍走另一big端，四值会改变。四个H都合法，原OPT1/2；精确V=2,1,1,2只否定继承推理，不否定promise算法。F(I)次模、D(I)超模，不能错用次模最小化。
- **图公式上界。** 合计I内专属tiny与内部edge任务，所有这些任务仅能用I的r|I|件容量；故至少少内部edge数。这允许牺牲专属任务，不假定LP先安排padding。下界保留全部padding、只弃内部edge，其余edge向未占位端；负载逐台≤1或α−1。由此F缺口精确等于诱导边数。
- **完整原任务。** N个宏始终全部安排，I占用后余宏去不同辅助机；α<2确保每机至多一宏。宏身份和辅助机位置对所有时间相同，故审计canonical布置未漏掉可行性。OPT1由实际σ上界和任一单位宏下界共同证明；不是只报估计值。
- **总规模。** q是2B倍数，r=q(α−1)为整数；q≥1/δ、q≥Δ/(2−α)。只有固定α、δ时q=O(Δ+1)，按二进制动态参数不作统一poly断言。无顶点图N0与N≥1无边图区分。星图只否定固定p-extendibility，不是路径能垒。
- **非hardness。** 每个原实例都直接OPT1，投影任意独立集不能变成一般R||Cmax困难性。必须把“可验证某占位状态”与“所有promise输入能选出有用占位”分开。

代码审查修补了两个nonfatal：Generic Gaussian初始化显式转Fraction，避免整数系数除法产生float；occupation脚本头部使用正式仓库根命令。这些在发布前修复，正式冻结输出源hash与现码一致。未削弱测试或数学结论。

## 实际运行与未覆盖部分

复现命令（stdout写新scratch文件）：

- `python3 tests/audits/unrelated_machines/residual_throughput_lattice.py`
- `python3 tests/audits/unrelated_machines/occupation_induced_edge_deficit.py`

第一份只对少量极小LP独立枚举primal/dual顶点，检查证书相等、混合dual、重排、格不等式、零边、空R、缺资格、大分母，以及真实2×2原矩阵全部调度和四份light残余LP。第二份只用预先固定的K1、K2、P3、K3、K1,4和α=1、3/2、199/100、δ=1/17；显式生成实际P、回算完整OPT1调度，对全部占位子集交叉核对原edge方向与普通整数最大流，并以残余可达割反算流值。c/h全部整数被明确核验，所以流的整数最优等于本族fractional F。输入hash、精确参数、源hash及实际结果在两冻结JSON中。

这些有限核验不承担一般证明，不扩大图/参数范围；小LP枚举不是一般位多项式solver。两命题的全球新颖性、独立论文价值和外部评审均未认证。

**仍未闭合的义务：** 一般H同时改变R(H)及h(H)的共同可求恢复，并在实际联合舍入中留固定余量。若只固定R、用总通过量近似或免费识别成拟阵，本页说明精确会缺哪一步；不以更多有限样本代替该义务。
