---
id: "customer-attraction/r105-direct-cover-prefix-and-reachability-review"
kind: "review"
type_tag: "审查"
title: "R-105 直接覆盖前缀可达性与中继比例障碍"
status: "integrated-with-finite-replay-boundaries"
truth_status: "general incidence lemma proved; explicit six-theme relay obstruction and exact certificate replay; no Q-CAG-HALF conclusion"
review_level: "full-source-read-and-exact-replay"
summary: "五个 R-105 direct_cover 来源共同给出一个实际 SPE 前缀的 incidence-budget 必要条件、六十一客户完整 SPE 的 prefix-relay 反例、嵌套根证书的 259 历史/1295 偏离精确核验，以及弱 matching 诊断和 Lipschitz 候选的有限边界。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-105f776c3e6d4a22bb7c380c5df8edc7/credible_attack/root_reachability_incidence_budget.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-105f776c3e6d4a22bb7c380c5df8edc7/credible_attack/root_reachability_incidence_budget.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-12bf6a96d24c48eca828620d6642e203/direct_cover/actual_prefix_relay_obstruction.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-12bf6a96d24c48eca828620d6642e203/direct_cover/actual_prefix_relay_obstruction.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-12bf6a96d24c48eca828620d6642e203/direct_cover/actual_root_B_certificate.json"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-12bf6a96d24c48eca828620d6642e203/direct_cover/actual_root_B_certificate.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-12bf6a96d24c48eca828620d6642e203/direct_cover/check_incumbent_lipschitz.py"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-12bf6a96d24c48eca828620d6642e203/direct_cover/check_incumbent_lipschitz.py"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-12bf6a96d24c48eca828620d6642e203/direct_cover/check_weak_matching.py"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-12bf6a96d24c48eca828620d6642e203/direct_cover/check_weak_matching.py"
evidence_manifest: "../../tools/evidence/r105-direct-cover-20261031/manifest.json"
---

## 来源身份与复现范围

五个来源均通过 `clean show` 逐字读取。R-105 的 `root_reachability_incidence_budget.md` 是一般必要条件草稿；另一个 workspace 的 `actual_prefix_relay_obstruction.md`、嵌套根证书 JSON、`check_incumbent_lipschitz.py` 和 `check_weak_matching.py` 是同一类客户吸引模型中的具体障碍与程序诊断。`legacy-cleanup` 和 `main` 的同路径字节按一个冻结版本处理。大小、blob、SHA-256、处置和复现输出见证据清单。

复现使用仓库已保留的 `customer_attraction` 精确模型副本与 `Fraction` 算术。证书 JSON 的外层不是标准 `StrategyCertificate` 形状，实际核验时取其中的 `certificate` 子对象；这一步和源文本中的“嵌套证书”边界一致，未把解析失败误报为数学失败。

## 实际 SPE 前缀的 incidence-budget 必要条件

设客户分解为非空的 (N=R\mathbin{\dot\cup}D)，其中 D-singleton 是只覆盖一个 (D) 客户的主题。假设每个主题要么是 D-singleton，要么至少包含 (alpha) 个 R 客户；触及 D 且不是 D-singleton 的主题至少包含 (a) 个 R 客户；并存在一个含至少 (q) 个 R 客户的合法主题。对某个合法有序前缀 (h)，记其负载向量为 (b)，剩余玩家数为 (r)，并设

[
I=\sum_{x\in R}b_x,\qquad \beta=\max_{x\in R}b_x,\qquad B=\min_{x\in D}b_x.
]

若

[
B>I/a,\qquad qB>\beta+\lfloor I/\alpha\rfloor+r+1, \tag{RB}
]

则 h 不可能是任何完整有序历史纯 SPE 的实际前缀。证明只用一次实际节点的 deviation：若前缀没有 D-singleton，则每个 D 客户的负载至多 (I/a)，矛盾。因此取最后一个 D-singleton ({x})。其后至多 (lfloor I/\alpha\rfloor) 个动作。该玩家遵循策略的最终收益至多 (1/B)；改选含 q 个 R 客户的主题后，无论后继如何，相关客户的负载至多 (eta+lfloor I/\alpha\rfloor+r+1)，故收益严格大于 (1/B)。这个上界与后继策略无关，所以任意 off-path 威胁或平局都不能修复偏离。

该引理是一般的实际可达性障碍，未给出任意背景的充分条件，也不涉及福利。R-105 的一个 round-5 精确背景取 (d=20,Q=2063,q_{block}=12,H=100000,M=10^9,r=2475)，计算得到
(I=495120000041260)、(eta=1000000001)、(B=10^{14})。取 (a=q=240) 时，(aB>I) 且 (qB>\beta+I+r+1)，因此该精确背景的任何合法前缀都不是实际根 SPE 前缀。它仍可作为任意背景的 off-path 证书；本结论不能把该背景当作 root-SPE 路径。

源还给出单一终局的福利记账：若前缀已覆盖支持 (H_b)，后继首次覆盖集合为 J，则 (W=|H_b|+|J|)，且前缀与尾部的客户价值按 (b_x/(b_x+d_x)) 和 (d_x/(b_x+d_x)) 分拆。对比较覆盖集合 C，(|C|-2W=|C\setminus H_b|-|H_b|-2|J|-|H_b\setminus C|)。这些恒等式只用于防止重复计费；它们没有推出一般 Q-CAG-HALF。

## 真实 SPE 路径上的 prefix-relay 比例候选被击穿

六主题、六十一单位客户的冻结输入顺序为 A,B,C,D,E,F，类型及数量完整保存在源和证据中。嵌套根证书的实际路径为
((B,A,A,F))，收益 ((9,13,13,11))。在同一完整策略中，根偏离到 A 的真实路径为 ((A,A,A,F))，偏离者收益为 9；而在实际前缀 B 后，A 作为第二位入场的可信最小值为 13。因此

[
V_{(1,A)}=9<\frac34 V_{(2,A)}=\frac{39}{4}.
]

这排除了把剩余 (r) 位玩家的真实偏离值沿实际 SPE 节点传递时只损失 ((r-1)/r) 的标量候选，即使首动作 B 本身确实是完整 SPE 的实际动作。源还记录了四个实际前缀的完整真实偏离矩阵：空前缀各主题值均为 9；前缀 B 与 BA 的行是 (13,5,11,10,11,11)；前缀 BAA 的行是 (10,5,11,10,11,11)。A 列增加与 B 列减少的转移说明一个标量无法表达跨主题信用。

可信入场者的最小值版本也被击穿：固定首位 A 后，对所有 36 个二、三位前缀逐一取末位最佳回复，最小首位 A 收益为 9；固定前缀 BA 时，第三位必须选 A，末位选 E/F 可使固定 A 收益为 13。因此 (f_4(\varnothing,A)=9) 而 (f_3(B,A)=13)，同样有 (f_4<\tfrac34 f_3)。这不是对弱 matching 或平均桥的反例；后两者仍要求一个最优元组的排列支付和全局的 (V_{i,j}) 预算。

## 精确证书核验与两个程序诊断

从 `actual_root_B_certificate.json` 的 `certificate` 子对象和归档的 `root_tax_failure.json` 实例重新调用标准验证器，结果为 `valid=true`，检查 259 个历史、1295 个偏离、0 个 violation，终局历史 ((1,0,0,5))，终局计数 ((2,1,0,0,0,1))。该结果证明给定证书确为完整纯 SPE；它不证明该输入的所有 SPE，也不把单个证书升级为策略存在性以外的全局福利结论。

`check_incumbent_lipschitz.py` 的实跑在小实例筛选中首先返回 `root_tax_failure.json` 的记录：前缀为空、目标 T=A、候选实际动作 A、(r=4)，左值 9，右值 (3/4\cdot13=39/4)。这与上述手工计算一致。脚本是有限枚举诊断，并非输入位长多项式算法。

`check_weak_matching.py` 的归档复跑输出为 `portfolio_matching_failure.json 40 40`；`root_tax_failure.json` 因该嵌套证书不是标准证书 schema 而跳过。这个结果只说明 portfolio 证书在该程序 scope 下的 best/worst matching slack 均为 40；它没有否定弱 matching 桥，也没有把 schema skip 当作根证书无效。标准根证书的有效性由上面的独立 `verify_certificate` 复现负责。

## 处置与开放边界

五个来源均已全文读取、相关对象核对和唯一内容归档。一般 incidence-budget 引理保存为实际根可达性的必要条件；prefix-relay 源保存为真实 SPE 节点上的比例中继反例；嵌套证书和两个脚本保存为有限精确证据及程序边界。它们共同否定若干标量/直接修补路线，但没有证明六人半覆盖主命题失败，也没有给出一般 Q-CAG-HALF 上界或下界。后续若使用该障碍，必须保留完整历史、平局、跨主题菜单信用和实际前缀量词。
