# R-171 reservoir 三源清洗独立草稿

## 来源身份与读取方式

本草稿只处理三份通过 `clean show` 读取的冻结版本，不把当前工作树中同名临时目录当作来源。

| 稳定 ID | 冻结路径 | 字节数 | SHA-256 | 作用 |
|---|---|---:|---|---|
| `e1f1b683928e2e2cae42` | `research/workspaces/customer-attraction/R-171cd7d518434f36a48cd50df29c9303/credible/reservoir_m7.json` | 8,889 | `40007056b608343a591c3c36b466626c6d0c4c48ff948496dabb2a2f40da3d38` | reservoir 有限探针输出 |
| `ad0cf87b18bf7f1afd33` | `research/workspaces/customer-attraction/R-171cd7d518434f36a48cd50df29c9303/credible/reservoir_search.py` | 1,933 | `8dcab36e0fb94bdb4f24892b38fdc05920153656571177bceabd51d7be9b8625` | reservoir 探针源码 |
| `3258071a267ea42b55b3` | `research/workspaces/customer-attraction/R-171cd7d518434f36a48cd50df29c9303/parent/full_terminal_packet_probe.py` | 4,918 | `088ee78780ce8399b6d2ac778dda64c4fef51ee5aa4431c05c3693ed48d8efa8` | 固定完整自动机的 FTA 浮点探针源码 |

三个版本在冻结清单中均有 `68fad804ec5946cb296f77dc5b336308a66abf12` 与 `aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c` 两个来源定位，内容哈希相同。实际读取命令是：

```sh
python tools/cleanup.py show e1f1b683928e2e2cae42 --out <reservoir_m7.json>
python tools/cleanup.py show ad0cf87b18bf7f1afd33 --out <reservoir_search.py>
python tools/cleanup.py show 3258071a267ea42b55b3 --out <full_terminal_packet_probe.py>
```

`clean show` 会校验冻结清单中的路径和 SHA-256；因此下面的程序解释针对实际冻结字节。第三份源码的关联输入不是同一目录下的 reservoir JSON，而是已有证据包中的 13 人完整策略自动机；不要按文件名把两条路线合并。

## 定义域与对象

### 对称私有主题加双 reservoir 的有限族

`reservoir_search.py` 的 `make(m,a,b,x)` 令 `k=m-1`，建立 `m+2` 个共同主题 `P0,...,P{k-1},R,B,C` 和 `m` 个依次行动的单位提供者。客户类型为：

- `x` 个喜欢 `{R,B}` 的单位客户，`x` 个喜欢 `{R,C}` 的单位客户；
- 对每个 `j<k`，`a` 个喜欢私有单例 `{Pj}` 的客户，以及 `b` 个喜欢 `{Pj,B,C}` 的客户。

源码固定 `b=1`，在源输出的运行中使用 `m=7`，所以是 7 名提供者、9 个主题、6 个私有主题。客户总数是 `6a+6+2x`。选择 `P0,...,P5,R` 可覆盖所有客户，因此这组参数的精确整数最优值是 `OPT=6a+6+2x`；程序仍通过规范 `Instance.optimal_welfare()` 逐实例计算它，没有把这个观察当成替代实现。

`ExactSPESolver` 求的是同一共同目录模型下、允许所有有序历史依赖平局的全部纯 SPE 终局计数集合。每条输出记录的 `W` 是该集合中的最小福利，`worst_outcomes` 是达到该最小值的计数向量数，`SPE_outcomes` 是全部不同终局计数向量数，`ratio=OPT/W`。`one_worst` 只在该记录刷新当前最高比率时保存一个最坏计数向量；它不是完整策略证书。

这与 R-171 可信低根旧种子（五人、七主题、目标根计数 `(1,1,1,0,0,1,1)`）是不同对象。旧种子属于低根 continuation 路线；reservoir 源是新的 7 人、9 主题参数族，不能因同属 R-171 而共用量词或稳定身份。

### 固定 13 人自动机的策略锥浮点探针

`full_terminal_packet_probe.py` 读取一个 gzip 或 JSON packet，要求其具有 `instance`、`root` 和完整 `nodes`。本次实际输入是已有 `R-c50fecc37aa44fb4a69a2122bb70e5fe/security/refined_tax_k10_packet.json.gz`：6 个主题、13 名提供者、27,243 个节点，其中 18,675 个决策节点和 8,568 个终端节点。根的指定路径是 `[5,5,5,5,5,5,5,5,5,5,0,0,1]`，指定终局计数为 `[2,1,0,0,0,10]`；packet 的客户重数合计 36。

程序逆计数序处理自动机，保留每个有序历史节点的真实子节点；同计数的不同历史仍可进入不同节点。它枚举 6 个主题的所有非空兴趣掩码，构造每个决策节点的真实比较差 `gamma`，并以 `gamma @ weights >= 0` 表示固定策略对非负客户重数锥的局部 IC 条件。随后只沿根在轨路径收集分支，构造一个依赖两个独立查询分布 `p` 的浮点二次目标；`linprog` 在该固定锥上选客户类型权重，`SLSQP` 更新 `p`。这是 FTA（固定策略锥）数值发现，不是全部 SPE 的搜索。

## 证据链与可复现实验

### reservoir 重放

为了满足源码中的 `ROOT=Path(__file__).resolve().parents[5]`，需保持源树等价层级，并在根目录放入规范 `customer_attraction` 包（仓库已保全于 `archives/customer-attraction/tools/evidence/exact-spe/`）。等价命令为：

```sh
python research/workspaces/customer-attraction/R-171cd7d518434f36a48cd50df29c9303/credible/reservoir_search.py \
  --m 7 --trials 45 --out reservoir_m7_replay.json
```

重放得到 45 条记录。除每条记录的运行秒数（机器/调度相关）外，`m,a,b,x,W,OPT,ratio,worst_outcomes,SPE_outcomes,one_worst` 逐条与冻结 `reservoir_m7.json` 一致。冻结记录中的最大观察比率是 `7/4`（首次出现在 `a=2,x=5`，后有 `a=4,x=13` 的同值记录）；没有 `ratio>=2`，因此源码也没有触发 `ratio>2` 分支去写 `*_counterexample.json`。输出是规范 Fraction 求解器的有限精确实例结果，重放验证的是程序和输入的可复现性。

### full-terminal packet 重放

把冻结源码置于等价 `parent/` 路径，使用上面 packet 运行：

```sh
python research/workspaces/customer-attraction/R-171cd7d518434f36a48cd50df29c9303/parent/full_terminal_packet_probe.py \
  research/workspaces/customer-attraction/R-c50fecc37aa44fb4a69a2122bb70e5fe/security/refined_tax_k10_packet.json.gz
```

程序打印一次当前最优记录并在搜索结束时打印：

```text
done; finite negative results have no general truth implication
```

写出的 461 B JSON 与已整合的 `archives/customer-attraction/tools/evidence/full-terminal-packet-probe-20261031/original/full_terminal_packet_probe.json`（稳定 ID `16232bdf99550baf9857`，SHA-256 `b6c18c7d2b89f8d6961ad656a7c9c505db0c3a7a5d2715209e23106311ad0832`）逐字段一致：

- `status`: `finite floating discovery only`；
- `gamma_rows`: 31,454；`seed`: 1,712,026；
- 归一化 `W=1.0`，`gap=-0.07142857142787729`（约 `-1/14`）；
- 浮点 `p=[0,0,0.2213133017,0.0138778368,1.1e-16,0.7648088614]`；
- 归一化 LP 权重只保留掩码 `63`（六主题全兴趣类型）质量 1。

已有 Boss1 工作区草稿中的 `pool_packet_report.json` 也在同一 packet 上报告 `ratio=1.0`、31,454 gamma 行、27,243 节点、在轨路径 `5` 重复十次后 `0,0,1`；`two_player_pool_report.json` 是另一个 81 个策略的有限扫描，最高比率同为 1。它们是邻接的池化数值材料，不改变本三源的来源身份。

## 数学结论与不应外推处

1. reservoir 家族给出一批可精确重算的完整纯 SPE 终局。当前冻结批次只覆盖固定 `m=7,b=1`、`a∈{1,...,7}`、`x∈{1,...,14}` 的随机排列前 45 个配置；最大已见 `OPT/W=7/4` 是有限样本中的低福利见证，不是该族所有参数的上界，也不是任意目录/人数的下界或上界。
2. 该批次没有 `2W<OPT`。它没有证明 `2W>=OPT`，也没有直接回答恰六名提供者的 Q-CAG-HALF；运行人数为 7，且搜索只取有限配置。不能把无 `ratio>=2` 读成不存在反例。
3. `ExactSPESolver` 的每个实例输出在其定义域内是精确的，但 `SPE_outcomes` 是终局计数集合，不是完整策略枚举；`one_worst` 也不是证书。完整历史平局仍可在不同节点分别选择续局。
4. full-terminal 的负 `gap` 只表示该次浮点交替优化在一个固定策略 IC 锥上没有找到正的 pooled-query 目标差。它不是精确有理证书；不能推出固定锥下界，更不能推出一般 SPE 没有反例。即使未来出现正浮点 gap，也必须有有理重构、所有比较行、完整策略和真实 `OPT`/证书核验才可提升证据等级。
5. 13 人 packet 的实际客户输入、固定自动机和 FTA cone 与 reservoir 的参数族不同；不能把 `W=1` 归一化结果、掩码 63 权重或 gamma 行数解释成 reservoir 的客户实例。
6. 所有结论都留在共同目录单位客户、均分收益、完整有序历史纯 SPE 模型内；不迁移到设施/原子客户模型、混合 SPE、弱 CCE 或 unrelated-machines。

## 与现有 reservoir/terminal 对象的关系

- 共同上游是 `archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md` 和 `state/算法/完整历史纯SPE终局全集--算法.md`；reservoir 脚本调用保全的 exact SPE 包，复用了完整有序历史和历史依赖平局量词。
- R-171 低根/credible continuation 及 `state/审查/R-171可信低根接续与有限候选边界--审查.md` 只给五人七主题的低根候选路线，仍没有一般证明或目标反例；它与本文 7 人九主题 reservoir 族并行，不能合并成一个“低根 reservoir”对象。
- `state/反例/R-171完整SPE稀疏槽租金障碍--反例.md` 证明的是两名单位客户、`m=2q` 的稀疏槽租金调和发散，且 `W=OPT=2`；它击破连续窗口支付桥，不是效率反例。本文 reservoir 的 `7/4` 有限比率与该障碍没有共享客户族或推导边。
- `state/审查/R-171接续工作区主张边界与开放义务--审查.md`、`state/引理/R-171池化响应负载Jensen信用与条件接口--引理.md` 说明全局 POOL 预算和有符号中继缺陷预算仍开放。full-terminal probe 正是其中固定策略 FTA 数值压力测试；其负 gap 不能闭合这些条件义务。
- 已整合的 `full-terminal-packet-probe-20261031` 比较记录把 `16232bdf99550baf9857` 处置为历史有限浮点诊断；本草稿只补读其配套源码 `3258071a267ea42b55b3`，不重复注册 JSON 对象。当前 `archives/customer-attraction/state/` 没有 reservoir 命名的正式对象，`archives/customer-attraction/map/graph.json` 也没有对应节点或边。

## 缺口与处置建议

1. **reservoir 源。** 保留为“有限精确探针/候选生成”材料；若后续正式入库，建议新建一个 `state/计算/` 对象，明确 `m=7`、9 主题、45 配置、最大观察 `7/4` 和 exact solver 版本，并把 reservoir 源 JSON、源码、重放报告作为同一证据链。不要建定理或反例对象，也不要把 `7/4` 写成该族全参数最大值。
2. **参数覆盖。** 若要接近 Q-CAG-HALF，应直接运行 `m=6`，同时系统覆盖或明确记录 `a,b,x` 的范围；随机前缀扩大只能增加有限证据，不能替代全量参数或任意目录量词。每个新高比率实例都需要完整策略证书和独立 `verify_certificate` 重放。
3. **FTA packet。** 保留当前负 gap 诊断与固定自动机输入；若继续攻击，需固定 NumPy/SciPy 版本，保存 packet 哈希、所有 gamma 行/LP 状态，优先做有理化和定义级真实比较。没有正浮点 gap 也不能声明无反例；有正 gap 也不能跳过精确证书。
4. **关系图与重复。** 将来由正式对象负责人把本文与 exact SPE 算法、R-171 credible review、POOL/Jensen 条件接口建立“有限实现/数值诊断/未闭合条件”的解释边；不把 reservoir 与 terminal wallet、稀疏租金或旧低根 seed 自动连成推导边。清洗记录应继续引用三份稳定 ID，避免把 `full_terminal_packet_probe.py`（父目录源码）与 `full-terminal-packet-probe-20261031`（已整合 JSON 证据）混为一个文件。

当前建议处置：草稿保留在 `cleanup/workspaces/Boss1/drafts/`，不调用 `clean done`，不写 claim、checkpoint 或 git 状态。它是对三份冻结来源的语义清洗草稿，不是主目标结果。
