---
id: "customer-attraction/arbitrary-child-spe-row-contract-finite-attack-review"
kind: "review"
type_tag: "审查"
title: "任意孩子 SPE 整数 ROW 合同与有限攻击审查"
status: "finite-negative-search-classified"
summary: "完整读取任意独立孩子 SPE 的整数 ROW 加强合同及三份独立攻击脚本；合同仍未证明，也没有找到致命反例。有限阴性搜索只说明所测权重、主题数、余数和线性锥范围，不能替代跨孩子共同付款证明或一般反例。"
truth_status: "unproved-contract-with-finite-falsification-only"
review_level: "full-source-read-legacy-main-byte-equality-and-customer-attraction-cross-check"
scope: "arbitrary independent complete (r-1)-player child SPE choices, integer ROW comparison contract, and finite exact/numeric attacks"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-a4671b9ccb664300b43d3216ce45c934/independent/arbitrary_children_contract_status.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-a4671b9ccb664300b43d3216ce45c934/independent/arbitrary_children_contract_status.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-a4671b9ccb664300b43d3216ce45c934/independent/attack_child_menu_contract.py"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-a4671b9ccb664300b43d3216ce45c934/independent/attack_child_menu_contract.py"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-a4671b9ccb664300b43d3216ce45c934/independent/attack_child_menu_general.py"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-a4671b9ccb664300b43d3216ce45c934/independent/attack_child_menu_general.py"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-a4671b9ccb664300b43d3216ce45c934/independent/cone_attack_child_menu.py"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-a4671b9ccb664300b43d3216ce45c934/independent/cone_attack_child_menu.py"
evidence:
  source_sha256:
    arbitrary_children_contract_status: "fa8795898d995cfadd1ae5d978efcdb2e8c51d5418d3e78b37a094a483b0b1eb"
    attack_child_menu_contract: "d58609b5a8199494d313ce13ae93688fed808e68f3328ad4c6d928753190c34f"
    attack_child_menu_general: "611a8e23f2e0cad478abbea7935050979273a20ad6c644d353102ee8b6b17f5f"
    cone_attack_child_menu: "9df0c10f73f24ce6189f0f148e8cbdd59876c0d60148688c5262d1e093fe6973"
  legacy_main_byte_equal: true
---

# 1. 实读与模型边界

本批逐字读取四个冻结源在 `legacy-cleanup`（68fad804…）与 `main`（aefc58ea…）的同路径版本；逐对 SHA-256 相同。又回读 customer-attraction 的完整共同目录模型、固定完整策略的覆盖矩表示、固定策略锥的非负价格合同、有界联合策略/客户重数表示，以及已经证明的非零背景总税反例与六人条件 half 证书。四个源属于 customer-attraction 的研究工作区，不是六个 Boss 当前 unrelated-machines 数学对象；不能跨模型合并。

待检合同固定：有限客户、有限非空共同主题目录、单位提供者、某个合法背景 `b`，剩余人数 `r≥1`。对每个当前合法主题 `A`，允许独立选择一个完整的 `(r−1)` 人孩子纯 SPE；完整叶记为 `z_A`，当前 `A` 的最终利润记 `d(A)`，全部旧玩家最终覆盖数记 `W(A)`。对任意有限比较元组 `T_1,…,T_q` 和任意 `A_0`，候选 ROW 不等式是

`Σ_j d(T_j) ≥ |⋃_j T_j| − W(A_0)`.

若某 `T_j=A_0`，同一个 `z_{A_0}` 必须同时用于 `d(A_0)` 与 `W(A_0)`；不同孩子的离轨选择可以不同；`A_0` 不要求最大化 `d`。这是一个跨孩子共同预算合同，而非单个固定策略锥中的普通 IC 行。

# 2. 合同若成立时能推出什么

若该合同在每个真实位置、每个当前主题和每个比较元组都成立，取 `q=m` 个达到 `OPT_m` 的比较主题。真实当前 IC 对每个位置给 `m u_i ≥ OPT_m−W`；把合同给出的比较和沿这 `m` 个位置求和，则候选桥直接得到 `mW ≥ m(OPT_m−W)`，即 `2W≥OPT_m`。这只是“合同 ⇒ half”的条件推论，不能反向证明合同，也没有把支付项拆成已经存在的 SPE 行。

合同的预算语义与已有对象不同：固定完整策略锥的矩表示和价格合同都要求**同一份完整有序历史策略**在所有节点、所有离轨动作下共同延续；本合同允许每个当前主题独立任选孩子 SPE，但又要求 `A_0` 的收益和覆盖同叶耦合。正是这种“孩子之间可独立、基准孩子必须共享”的混合量词，使既有单策略锥证书不能直接覆盖它。

# 3. 定义级边界与已知不承重处

源状态正文明确记录：目前没有证明，也没有发现致命反例。此前逐人安全值、自由分数 floor、根菜单去相关和实际缩放背景的失败，均不直接否定这个整数 ROW 合同，因为该合同下界是实际遗漏净差，而不是 `OPT/(2m)` 或静态 minimax 值。

`q=1` 不能承重一般合同。末位之后的每个孩子叶都是最佳回复；若末位之前客户负载为 `c_x`，令 `R=Σ_x c_x/(c_x+1)`，则任意主题 `T` 的末位改选利润至少 `|T|−R`，而实际末位利润至多 `W(A_0)−R`。末位最佳回复给 `W(A_0)≥|T|`，所以只有一个比较项时右侧非正。这个观察只解释简单攻击为何失败，不是一般 `q≥2` 的证明。

已有 customer-attraction 结果必须保持独立：非零背景总税的具体四人子局反例否定了另一条全称税式，但其根福利仍满足 half；固定策略锥的有限价格不等式是对固定 `σ` 的锥上证书；有界联合策略 MILP 是指定路径、全部节点动作和客户重数的精确表示，但规模随完整树和 `2^p−1` 类型增长。它们都没有自动提供本合同所需的跨孩子共同付款。

# 4. 三份攻击程序实际做了什么

## 4.1 `attack_child_menu_contract.py`

该脚本固定随机种子，遍历 `k=3,…,8`，每个 `k` 做 3000 个随机有限权重实例；权重是非负整数主题子集重数，随机生成一个有限前缀。对每个首位主题枚举两层孩子选择，先用末位最佳回复构造叶集合，再按孩子 SPE 的最小收益和候选联合成本检查所有非空比较子集。它把一个潜在正缺口写成整数尺度 `gap_scaled`，若发现便保存 `child_menu_contract_counterexample.json`；冻结源的运行口径是 `NO COUNTEREXAMPLE; finite only`。

程序保留了 `A_0` 叶与其覆盖的耦合：构造比较时用同一个 `(b,c,u,W)` 元组，而不是把 `d(A_0)` 和 `W(A_0)` 分别取两个极值。这一点是本合同的关键语义。没有输出反例只表示这些随机权重、主题数、前缀和三层子局都未找到正 gap。

## 4.2 `attack_child_menu_general.py`

该脚本对 `r=3,…,6`、`k=3,…,7` 的有限组合进行 500 次随机搜索。`outcomes(q,left)` 递归恢复所有可由完整孩子 SPE 产生的终局计数；每一步以每个动作的最坏收益构造完整子局安全门槛，并保留达到门槛的所有终局。随后对每个 `A_0`、它的一份完整叶、每个非空主题子集计算

`|union| − W(A_0) − Σ d(T_j)`.

若正则保存完整子局计数、实际利润和 `gap_scaled`。这比 4.1 的三层菜单更接近“任意完整孩子”，但仍只覆盖随机权重和小 `r,k`，不证明全称合同。

## 4.3 `cone_attack_child_menu.py`

该脚本在 `k=5`（前 60 次）和 `k=6`（后 40 次）、`r=4` 或 `5` 的有限随机权重上，先递归恢复所有完整孩子 SPE 终局，再在线性 SPE 锥内用 `scipy.optimize.linprog` 搜索使合同缺口最大的有理近似方向。它显式构造策略锥的动作约束：任何给定孩子终局必须达到对应节点的最坏收益门槛；然后以覆盖并集减去 `A_0` 的覆盖和逐主题利润作为目标。输出 `FOUND` 只会保存一个候选 `child_menu_cone_discovery.json`，否则输出 `NO COUNTEREXAMPLE: finite cones only`。

这里的浮点 `linprog` 只负责发现方向，不是数学证书。即便某次发现正 gap，也还需要从策略锥恢复完整有序历史、客户重数和全部 IC，并用精确有理算术核验；当前冻结源没有这样的正 gap 输出。反之，有限运行没有发现正 gap，也不是对锥上所有实权的证明。

# 5. 结论、失败机制与接续

**当前可采纳结论**是：任意独立孩子 SPE 的整数 ROW 合同仍为未证明命题；三份攻击在各自有限范围内没有生成反例；`q=1` 的定义级边界不承重。候选证明路线必须同时处理每个 `A_0` 的共享叶覆盖与各比较主题的可独立孩子选择，建立跨孩子的共同付款或找到精确反例。

**不能写入的结论**包括：不能把“NO COUNTEREXAMPLE”写成合同成立；不能把浮点锥优化写成精确负证书；不能把已有非零背景总税反例、固定策略锥证书、静态 CCE/Nash 结果或六人 `τ_C≤9/2` 条件 half 直接套到本合同；不能把该合同推出六人目标已经完成。阶段三若继续，应先固定 `q≥2` 的最小难例，保留同一 `z_{A_0}` 耦合，再逐分支核验真实续局和支付来源。

# 6. 处置

四个来源均 `integrated` 到本审查。状态正文、三个攻击程序及其有限输出/未输出情况一并保留；没有删除未成熟想法，也没有把有限阴性升级为定理。该审查对象与 unrelated-machines 的任务桥、weighted-congestion 的时钟证书和六人 SPE 覆盖目标保持独立身份。
