# R-18 next-security 四源比较记录

## 逐源身份和处置

| ID | 文件 | 原件字节 / SHA-256 | 主要观察 | 处置 |
|---|---|---:|---|---|
| `294d323a2f01440fe2bc` | `background_search_best6.json` | 823 / `b76c9232008d9739467ea5780de7fa80a70656817feaf554110ffd125e6feee8` | `topics=6, remaining=3, P=171.25, v=57.08333333333334, ratio≈1, iteration=4163, all_root_outcomes=2` | `retained` |
| `0f9f80cbc75446bd5b78` | `background_search_best6_r4.json` | 848 / `43592e90fd7e41b8db5cc1108118c544611ac541cacea886a5fb3e52d3c41128` | `topics=6, remaining=4, P=70.0, v=17.500000000000004, ratio≈1, iteration=16126, all_root_outcomes=2` | `retained` |
| `deadef6bc35b00f54164` | `binary_potential_menu.py` | 2211 / `b11a4596339c80bd7c619a19bc0df7786d8730c995078483128a7838a153e78a` | n=4, pA=.5; policy code 顺序在 `code=17427` 首次找到 `gap=.25`，累计测试 17428/32768 | `integrated` |
| `b5ac195f8c2ea25aa0af` | `binary_potential_menu_n4.json` | 388 / `f96f7fefd9671fdd72a7f2b97282f11765931102d91397dafb3335caf283fd2b` | 冻结输出记录 `path=[1,0,0,0]`、`menu_countsA=[0,2,3]`、`gap=.25`，与脚本重放结构字段一致 | `retained` |

四个 raw 导出分别与 evidence `original/` 副本逐字 `cmp` 通过。JSON 原件不是可执行源；脚本原件按 n=4、pA=.5、limit=32768 实际运行，命令退出码为 0。运行 stdout 在 `replay/binary_potential_menu_n4.stdout.txt`，stderr 在 `replay/binary_potential_menu_n4.stderr.txt`（空文件，长度 0），输出 JSON 在 `replay/binary_potential_menu_n4_replay.json`。重放与冻结 n=4 JSON 的 `players,pA,full_policies,tested,found` 五个结构字段全部相等；只有计时字段 `seconds` 随机器运行时间变化（冻结 19.925655364990234 s，本次 20.87387990951538 s）。

## 数学对象和全仓比较

两个 background JSON 来自次安全值有限搜索，字段 `weights` 是有限主题客户重数，`background` 是背景主题计数，`outcome` 是剩余玩家终局计数，`P` 是该有限递归中选出的根结果利润，`v` 是静态安全值 LP 的值，`ratio` 实际为 `P/(remaining·v)` 的浮点比值。它们没有 CAG `Instance`、完整策略表、所有历史的偏离证书、客户级 `W/OPT` 或 exact rational witness；因此只登记为有限 security/potential 记录。

它们与既有 `R-18-next-security-finite-20261031` 的 k=5、r=3 background search 结果（冻结比率约 1、复跑比率 1）属于同一背景聚合探针的不同 k/r 参数；也与 `R-18次安全值有限搜索与根缺口--候选` 中的高背景半利润条件和根背景缺口相接。新增 k=6、r=3/4 输出没有关闭根背景缺口，也不能把 `ratio≈1` 外推为一般 `P≥r v` 或 Q-CAG-HALF。

`binary_potential_menu.py` 则枚举有序二元匿名策略表。它把匿名两动作 payoff 向量 `(a_1,…,a_n,b_0,…,b_{n-1})` 作为可正可负的自由变量，先写完整历史单步偏离行，再写固定 `pA` 的 menu 行，用带 `[-1,1]` payoff box 的 LP 最大化 signed-potential gap。n=4 的运行在策略代码 `17427` 处首次得到 `gap=1/4`，对应 `path=(1,0,0,0)`、菜单计数 `{0,2,3}` 和 payoff `(-1,1,0,1,1,1,0,-1)`；这是抽象匿名两动作游戏的有限分离。

该脚本与既有 `R-18-POTENTIAL-MENU-PROBE-20261031` 的任意整数势函数探针互补：后者在 m=3,p=3 的有限抽样中未找到严格菜单反例，而本源在更窄的二动作自由 payoff 抽象中找到一个 LP gap；两者都没有共同目录客户覆盖语义。`匿名计数势的客户相容性与非负反演条件--障碍` 进一步说明任意匿名势表不能自由编译为非负客户重数。故 `gap=.25` 不能迁移为 CAG SPE 反例、静态 CCE 反例或 Q-CAG-HALF 结论。

## 结论边界

四源的独有信息已经分别归档，但没有完整 CAG 证明、完整 CAG 反例、exact rational certificate 或新颖性认证。两份 background 记录保留（`retained`）其有限数值；脚本和 n=4 输出分别以 `integrated`/`retained` 保存匿名实验及冻结 witness。Q-CAG-HALF 保持 OPEN。
