# M-76622f3817514ca5800fcbc0bd9f91c0 数学复核报告

- **对象**：`customer-attraction-3a-3a-aa23d428c3205649`，对象 `M-76622f3817514ca5800fcbc0bd9f91c0`，registry pin `81a8f0fd6f4f80783433acc487ff4cc2b85e38e809ddc65ebb9a72064e11ab6c`。
- **复核范围**：task JSON 声明的 10 个 reading pass 全部读取；两个 Markdown、源 Python、两个 596/815 kB 级 exact JSON、独立 audit Python、432 kB replay audit、runtime manifest 均做了完整解析/字段检查。未读、未引用 deferred candidates。
- **复核结论**：对象的 324 行普遍必要性和两次原入口的有限 Fraction 回代成立；精确点是固定 1905 维必要行松弛点，不是完整目录/SPE 证书。`early_reply_exact` 还缺 36 floor 中 5 条，不能升级成反例；`early_reply_floors_exact` 的 5287 行点通过 36 floor，也不能升级成 SPE 或 half 定理。

## 1. 模型、量词和真正承重的数学式

共同模型是：有限单位客户；有限非空**标签**目录 `S` 及任意覆盖映射（可空、可重复覆盖、同覆盖异标签）；六位单位权提供者按固定顺序、观察完整有序历史、各选一次；客户终局价值在全部覆盖者之间均分；完整纯策略在全部合法历史给动作，SPE 在每个历史和每个单步标签偏离后沿同一策略真实续局满足弱 IC。允许空主题、重复动作、同覆盖异标签、零客户和弱平局。这里的 `hist` 重数是单位客户类型重数，不是加权玩家，也不允许把策略无证明地商成计数函数。

对象只取实际第四位/第五位源。固定实际 `A_1,...,A_6`，强制 `T` 为同一原策略生成的合法 `R_e`/`Z_e`，实际源位置 `s=4,5`（源码零基 `i=3,4`），隐藏真实后继数分别 `r=2,1`。有序边族为 `R` 非对角、`Z` 非对角、`Z` 对角（代码统一三轨道 `(0,0),(1,0),(1,1)`，边重数 `30,30,6`）；索引/标签可重复，重数按有序边累加。

单客户令 `p=sum_{a<s}1_{A_a}`、`ell=sum_{a<=5}1_{A_a}`、`t=1_T`、`q=1_Q`，隐藏位 `f∈{0,1}^r`、末位 `g=f_r`、`z=p+t+sum f_j`。在 `beta=0`、非负 `alpha_j,mu` 下，源码/引理的逐客户函数是

```
H(f)= t/z + Σ_j alpha_j f_j/(ell+1) − mu*g/z
     + mu*q/(p+t+Σ_{j<r} f_j+1),
psi = min_{f∈{0,1}^r} H(f),
```

零分子份额按零约定。源节点 IC、实际末位对每个真实后继的报价、分支末位对 `Q` 的最佳回应给出

```
u_s + (Σ_j alpha_j)u_6 − Σ_x psi_x >= 0.
```

等价分解为源真实 IC 损失、每个真实后继的实际末价预算、分支末位对 `Q` 的 IC 损失和 `Σ_x(H−psi)≥0`。因此这里必须取 `min`，不能把分支包络方向写成 `max`；不能冻结离轨后继、不能把分支末位利润替换成 `u_6`，也不能把强制节点当新节点最佳回应。`Q=T` 时 `q=t` 仍是合法自查询，完整分母保留当前查询者。

价格参数数目逐项核对：实际第四位 `2×3×3×2×3×2=216`（subject `R/Z`、三轨道、`Q∈{A5,A6,self}`、`all/last`、`aa∈{0,1/4,1/2}`、`mu∈{0,1}`）；实际第五位只有一名后继，代码只留 `last`，得 `108`；总计 `324`。这 324 不是 324 个线性独立方向，也不是新福利常数；没有 K 项或 overlap 项系数。

## 2. JSON 布局与程序核对

两份新 exact JSON 均有 1905 列，列型为 `K=1`、`hist=16`、`joint-reply=582`、`overlap=1306`；所有 hist 的六位 actual、八词重数和 `d=sum t` 逐项成立；194 个 joint 组的隐含 00 质量非负，2612 个 overlap 上界逐项成立；所有列描述符在四个保存点之间按序相同。`O=1` 是必要行系统的归一化，不是固定客户实例规模。

独立 `audit_added_price_rows.py` 在不构建旧完整图、不跑 LP/优化器、不执行原 main 的前提下：

- AST 摘出原 `build`，与字面枚举二元隐藏状态逐系数比较，`324×1905=617220` 个系数全部相等；
- 36 floor 函数与独立有序边实现全部相等，比较 `36×1905=68580`；总新增系数 `685800` 全部相等；
- 536 个不同隐藏投影键、1772 个字面二元状态（排序候选也为 1772），全部通过；
- 四个保存点的全部顶层字段、1905 描述符、质量非负性、194 joint/2612 overlap 约束、O/W/gap 和逐列差异全部重核。

原入口分别在 clone 外独立 runtime 用 `--verify` 和 `--floors --verify` 跑一次，均 exit 0、stderr 为空；只做 Fraction 回代，没有重新优化：

- `5251` 行、1905 列、`minimum_slack=0`，W 精确匹配；
- `5287` 行、1905 列、`minimum_slack=0`，W 精确匹配。

Runtime manifest 表明复用 47 个冻结依赖，覆盖本批 4 个 overlay；根 `work.py` 仅用于路径标记，未执行控制器或网络。

## 3. 精确结果和可证贡献

### 324 条普遍必要行

对任意共同目录模型中的六人完整纯 SPE、任意实际第四/第五位节点、任意正文列出的 `R/Z` 主题/轨道/参数，以上 IC 组合给出 324 条有效必要行。实际源真实后继取自同一 `σ`，所有偏离沿真实续局；有限系数计算保留 ordered-edge 身份和 R/Z 相关质量，不用独立边缘乘积。

### 5251 点（`early_reply_exact.json`）

- 继承旧 4927 行，增加 324 行；`O=1`。
- `W = 57770848877002761745569033003977 / 120785977474956965853696208259979 ≈ 0.4782910242 < 1/2`。
- `strict_half_gap` 存的是 `O−2W`，严格为正；171 个正质量列；全部 5251 行 Fraction 非负，最小余量 0。
- 新 324 行全部严格正，最小余量
  `3068136569007345979888391178557 / 402619924916523219512320694199930`。
- 另加的 36 条全实际前缀 floor 中恰 5 条负、5 条零；负键（`i` 从 0 计）为
  `(1,0,1,0)`, `(1,1,1,1)`, `(2,0,0,0)`, `(2,0,1,0)`, `(2,1,1,1)`；最负
  `-37918341723853123058170585072309 / 1073653133110728585366188517866480`。

因此 5251 点只证明固定 1905 维必要系统可行，且不满足另一个已知 36-floor 族；负 floor 只排除保留该固定质量向量坐标的完整行完成，不给出目录、完整历史 IC、真实偏离终局或 SPE 反例。

### 5287 点（`early_reply_floors_exact.json`）

- 在相应 floor 版本上为 `4927+324+36=5287` 行；`O=1`。
- `W = 348849746216199535907980629211183 / 729080852958937593380920238282304 ≈ 0.4784788200 < 1/2`；169 个正质量；全部 5287 行非负，最小余量 0。
- 新 324 行全部严格正，最小余量
  `379923480164036730819855690374081 / 32403593464841670816929788368102400`。
- 36 floor 全非负，恰 7 条为零；因此该点是更强的**有限必要行松弛**点，不是完整 SPE/反例。它不能反向修复 5251 点，因为 5251→5287 改了 `K=1`、`hist=10`、`joint=106`、`overlap=90` 共 207 个质量，且 W 也变。

### 旧点身份和差异边界

- `4927→5251`：所有列描述符、K、16 hist 质量和 W 相同；仅 57 个 joint、61 个 overlap 质量改变。324 新行在旧 4927 点已全部严格正，不能说“加行切掉旧点后修复”。
- `4963→5287`：列描述符、K、16 hist 质量和 W 相同；51 个 joint、44 个 overlap 改变。两点各自 36 floor 都通过，仍是不同质量向量。
- `5251→5287`：除新增 36 行外还改了上述 207 个质量，故不能把 W 的变化或 floor 通过仅归因于新增 324/36 行。

## 4. 建议的 map 边方向（不在本次修改）

建议只建立一个**上下文/实现型**边，而不是全局蕴含边：

- `source_ids: [M-76622f3817514ca5800fcbc0bd9f91c0]`
- `target_ids: [M-94fb0280f8af4175b3ec6801a8843744]`
- 建议 `kind: "implements"`（或若 schema 只允许审计关系则 `kind: "checks"`, `relation_mode: "context"`）。
- 边义：对象给出目标 5251 点中“实际四/五位 R/Z 价格投影”这一 324 行族的普遍必要性，并逐系数/逐点验证其在该固定点的全部严格正余量；目标点同时承载 36-floor 的五条负值。该边只能说明有限行族与点态审计的对应关系，不能声称 324 行蕴含点的存在、LP 最优性、共同目录实现、完整 SPE 或 half。
- 目标对象当前 registry pin 为 `8de84cff3acd09a1320f867b301a2d4a9add9a5586bf3badb0062c7c6ef90a36`；若只保留已有 endpoint pin 体系，边应携带该 pin 与本对象 pin。
- 不建议把它连到 deferred `CA-PRICED-HIDDEN-REPLY-v1`、`CAG-MODEL`、`M-5d2fee3a1f8a4dc6a76eea98204ba228`、`M-96807ccbb51d4a04a699093e9211323e`、`M-f9361826fd0f4923b924933366813431`；它们本轮未作为 paid/read evidence。共同定义只作模型背景，不构成 hub edge。

## 5. Evidence 路径与 SHA-256

以下是 task JSON 声明的全部 primary reading refs（均已完整读取）：

| path | sha256 |
|---|---|
| `archives/customer-attraction/state/计算/显式新回复的实际四五位补价与精确点--计算.md` | `0d1817e1c6481c592b24b09ae7d8cd5b0914f75267592a76d43e59e6bc0f9853` |
| `archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md` | `cc4a9dadb09e08b072cb63214d2e084db38db219e4100efbccf9b7f497520e88` |
| `archives/customer-attraction/tools/evidence/early-reply-price-points-boss3/original/early_reply_prices.py` | `2e5d169cff6f4ec26a18e2b06894de79ba7892737523e36d2ad0439e6b862be1` |
| `archives/customer-attraction/tools/evidence/early-reply-price-points-boss3/original/early_reply_exact.json` | `4c5903b72783e55b1afe0f43606cff191c69b844bd64428ce0293dc4d4f3ece5` |
| `archives/customer-attraction/tools/evidence/early-reply-price-points-boss3/original/early_reply_floors_exact.json` | `78e3a89cf01a62ea2a4d2768043e09027e0b3dd920984d3f9591b0c0a1e0fe2e` |
| `archives/customer-attraction/tools/evidence/early-reply-price-points-boss3/audit_added_price_rows.py` | `3035a76b447036402555d02f998d8451e99c19eff3623e48ce5793b299fde967` |
| `archives/customer-attraction/tools/evidence/early-reply-price-points-boss3/replay/added-row-and-point-audit.json` | `fb008c5e7fe4421f4ce601e1d9990d519ee4523b969b16c0984000cfadcade3e` |
| `archives/customer-attraction/tools/evidence/early-reply-price-points-boss3/runtime-dependency-manifest.json` | `e24f7a16ce37bf607fb26a575dbbb78daa18b72cb902f3875d181a26aedbf6a3` |

执行/封装旁证：

| path | sha256 |
|---|---|
| `archives/customer-attraction/tools/evidence/early-reply-price-points-boss3/replay/base-execution.json` | `4f21b685b0f2bf5fb35d356b3feb9727b79e5ab4046f2aa39a0d9e060ea19984` |
| `archives/customer-attraction/tools/evidence/early-reply-price-points-boss3/replay/floors-execution.json` | `b0d4fbf1ecb498b4cbd40d05ecc549f7fe1b2b0bd81a56f8ab5791d4edad3d62` |
| `archives/customer-attraction/tools/evidence/early-reply-price-points-boss3/replay/base-stdout.txt` | `1754fd8f85b876e8230d184ce53475f5b6f037e3e831689b83e44c8d5662f97f` |
| `archives/customer-attraction/tools/evidence/early-reply-price-points-boss3/replay/floors-stdout.txt` | `f1a1dac6da3990ddaf66eb51981ed1d20d16e2422a0693ede2797058d4997318` |
| `archives/customer-attraction/tools/evidence/early-reply-price-points-boss3/package-check.json` | `b00642398398dd6e7cb4ebffcf6f3f2cbdc6fba1aefe56a634d7a1cee41a1921` |

## 6. Remaining / open obligations

1. **全目录/完整 SPE 可实现性**：为 5251 或 5287 的质量向量构造真实共同标签目录、完整六人 `σ` 和全部历史 IC；当前有限松弛不提供反向实现。
2. **全局 324 行族的使用边界**：行族本身对声明的完整 SPE/实际节点量词成立，但有限参数集合不穷尽所有非负价格、所有源位置、全部目录主题或所有新 PAIR/闭包。
3. **最优性/全局半覆盖**：没有精确 LP 对偶，也没有把 `W<1/2` 的归一化点值提升为 `OPT_6>2W` 的游戏结论；不证明 324 行全局冗余或必要。
4. **36-floor 与新点**：5251 点的 5 个负键需要保留为“固定点排除”；5287 点通过且 7 零，不等于存在 SPE。若要形成反例，必须补齐真实目录、全历史策略并核 `OPT_6`。
5. **更强 R/Z 联合实现**：各 ordered edge 的 4-state 联合质量被保留；不能以独立边缘或“同 W”合并 4927/5251/4963/5287 点。任何跨边共同实现仍需额外证明。
6. **复现合同**：如需重跑，应在隔离 runtime 先核 47 份 frozen dependencies 与 4 overlays，再显式执行两个原 `--verify` 入口；默认优化模式会改写 exact/status，本次没有运行，不应以旧文件存在代称新优化。

## 7. follow_up_tasks

- 对 `M-94fb0280f8af4175b3ec6801a8843744` 建立 context/implements 边，明确 324 行与 5251 点的行族对应；保留负 floor 键和最负精确余量。
- 单独核查 5287 对端 `M-c213464ff5db45bcb0625547ae7f20a1` 的点态身份差异；沿用现有 pointwise-contrast/finite-audit-boundary 语义，禁止从 5287 反推 5251。
- 若目标是全局结论，先补“有限必要系统 → 真实目录/完整历史 SPE”的反向构造，随后再检查 `OPT_6`；不要先把 `W<1/2` 当反例。
- 若继续扩展价格族，必须明确新的源位置/后继数、`Q=T` 分母和 ordered-edge 相关性，并对每个新参数做 exact hidden-state audit；不能把排序压缩只因本轮 `r≤2` 成立而宣称一般余尾认证。
- deferred IDs 仅作为独立检索候选，待其各自声明/证据完整读取后再决定是否建边。

## 8. closed_overlaps

- **已关闭：324 行计数身份**：`216(actual4)+108(actual5)=324`，无重复参数去重假设；实际 4 位 `all/last`，实际 5 位仅 `last`。
- **已关闭：程序与字面数学实现一致**：617220 个价格系数、68580 个 floor 系数、685800 个新增系数比较全部 exact 相等；原入口两次 verify 均 exit 0。
- **已关闭：point 字段合同**：四点的 1905 描述符一致；每点 joint 194、overlap 2612 上界、O=1、W/gap、positive counts 与原值一致。
- **已关闭：同 W 误拼**：4927→5251 与 4963→5287 虽同 K/hist/W，各自辅助质量不同；5251→5287 还改 K/hist/W，不能拼成同一点或把差异归因于单一新增行族。
- **已关闭：floor/price 命名混淆**：`additional_early_reply_rows=324` 只指价格行；`--floors` 的 `360=324+36`，另 36 是普通实际前缀 floor，不是第二套 360 价格投影。
- **已关闭：min/max 方向和后继冻结误读**：本族使用 `psi=min_f H`，`H−psi≥0`；真实后继沿同一 `σ`，强制节点不添加最佳回应要求；`Q=T` 仍完整计分母。
- **已关闭：O/W/half 误读**：`strict_half_gap` 是 `O−2W`；`O=1` 仅归一化有限系统，W<1/2 不等于目录实例的 SPE/OPT6 反例。
- **已关闭：deferred candidate 越权**：`CA-PRICED-HIDDEN-REPLY-v1`、`CAG-MODEL`、`M-5d2fee3a1f8a4dc6a76eea98204ba228`、`M-96807ccbb51d4a04a699093e9211323e`、`M-f9361826fd0f4923b924933366813431` 均未作为本报告已证前提或 paid evidence。

**审计命令**：

```text
python -B archives/customer-attraction/tools/evidence/early-reply-price-points-boss3/audit_added_price_rows.py /workspace/scratch/0719eb21fa32/co-work-anl
```

结果为 exit 0，输出与上文 `617220/68580/685800`、四点 exact summaries 一致。未修改共享 `map` 文件，未提交 Git。
