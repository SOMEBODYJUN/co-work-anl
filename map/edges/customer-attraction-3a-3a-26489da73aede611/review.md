# Solver report — customer-attraction-3a-3a-26489da73aede611

## 任务和阅读核对

核心对象是 `customer-attraction/maximal-root-true-tail-income-strengthening`（registration pin `997098f7fc23e8073978f1d5b917a8084682b084ebf5e8347decae795e7042b2`）。任务声明没有 `read_object_ids`；其 overlap 指定 `customer-attraction/all-m-nearly-saturated-root-rigidity`（pin `fc9ad23fad83f04e23c4107d85f10995212c12864bead15c364e70ddec390469`）为 3B follow-up。为核对该 overlap，本轮也完整读取了该一般人数引理和共同模型定义。

任务声明的 31 个 reading passes 均已实读，且逐字节 SHA256 全部与 task JSON 相符（31/31 OK）。范围包括：核心引理；共同目录完整历史模型；任意人数近饱和根刚性；Main 的根加强、容量回流和三份诊断；near-equality 独立审计及其 Fraction checker、结果和冻结清单；maximal-root-tail wallet 的摘要、proof、derivation、129 列 71 行 exact input/certificate、字面 checker、129 列表和冻结清单；maximal-root-tail 独立审计、checker、结果、冻结清单；两个 Main checker 结果。没有改动这些冻结源，也没有运行 optimizer、Main、builder 或重新求解。

## 核心命题、量词和模型边界

模型是有限单位客户、有限非空共同标签目录（覆盖映射可别名、可为空），恰六名单位提供者依固定顺序行动；完整纯策略在全部有序历史上量化，保留空覆盖、重复行动、同覆盖异标签、任意弱平局和零客户。`u` 是实际根玩家收益。取目录中真正达到最大裸覆盖大小 `K` 的合法标签 `C`，强制根选 `C` 后必须沿**同一份原策略的真实有序续局**得到 `(C,B2,B3,B4,B5,B6)`；不把相同覆盖标签或相同计数的历史合并。任取六个合法查询标签，记覆盖并大小 `O`；`O` 是六标签查询的并，不是合成的新行动。取 `O=OPT6` 得目标形式；TAIL 的正预算实际上不使用分支并集帽，因此同一根线对任意六合法查询并都成立。

核心正文完整给出三条普遍必要根线：

* `NEW`: `10980u - 1658K - 87O >= 0`；
* `SIZE`: `67140u - 9878K - 627O >= 0`；
* `TAIL`: `112944305160u - 11595684007K - 2178783435O >= 0`。

旧根行 `H=150u-(139/6)K-O>=0` 取等且 `O>0` 时还推出 `K >= 23O/63`。这三条根线都只是必要条件，不是 `2W>=OPT6` 的证明、SPE 锐界或反例。12/5、65/84 是各自逐型比较的最佳系数，只在声明的 Boolean 域和对应预算内使用，不能外推为整体锥的锐性。

## 独立证明的实际承重

沿真实 C 分支，对每客户保留位型
`(p,y2,y3,y4,y5,z,o) in {0,1}^7`，其中前六位是 `C,B2,...,B6` 的会员，`o` 是查询并会员。`n=y2+y3+y4+y5`、`c=p+n+z`，根、第五、末位的分支份额分别是 `p/c,y5/c,z/c`（零分子零分母按零定义）。由真实根 IC、五个尾标签的最大裸大小、末位 BR 和第五位在准确有序前缀 `(C,B2,B3,B4)` 的真实偏离后继，得到

`I=u-v>=0`, `D_j=K-|Bj|>=0 (j=2,...,5)`, `D_Z=K-|B6|>=0`,

`B=w-sum o/[6(1+p+n)]>=0`,

`G=s-sum o/[6(p+n-y5+2)]>=0`。

`G` 是新关键来源：第五位改选每个合法查询后沿自己真实末回复，查询客户的后继覆盖数最多为 `6-j=1`；不能冻结原分支的末两位。对每个 Boolean 型，根刚性转移余项 `tau` 非负。设

`T=u-O/12+K/18`,
实际逐客户式为 `delta=(p-y5)/c + o/[6(p+n-y5+2)] - o/12 + p/18`；这里末项使用逐客户并会员 `o`，不能把整体并集大小 `O` 代入。

由 `T=I+G+sum delta` 和完整 128 型检查
`rho=delta+(12/5)tau>=0`，结合 H 的逐项分解

`H=150I+3 sum(D2..D5)+6 DZ+6B+6 sum tau +(5/6)|C\O|`,

得到非负付款

`T+(2/5)H = 61I+G+(6/5)sum(D2..D5)+(12/5)DZ+(12/5)B +(1/3)|C\O|+sum rho >=0`,

等价于 NEW。`rho` 的唯一单余项尖点为 `(p,y2,y3,y4,y5,z,o)=(0,0,0,0,1,0,1)`，恰给 `delta=-1,tau=5/12`，故 12/5 只是在该指定逐型控制下锐。

SIZE 的独立承重不能由 `J=13L-504H` 与两个已知非负式直接相减。令 `eta=(65/84)rho-tau-(5/12)(p-y5)`；完整 128 型核对 `eta>=0`，并以 `sum(p-y5)=D5` 回流同一 B5 的大小缺额，得到

`J=67140I+2340G+1296(D2+D3+D4)+2556D5+2592DZ+2592B+360|C\O|+3024 sum eta >=0`。

TAIL 则完全独立重建 71 条真实必要行（根 IC 1、五 CAP 5、并集帽 1、根 K/6 地板 1、source 2–6 的 35 条 SAFE、末两位七查询描述子的 28 条 PAIR）和 129 列（128 Boolean 质量列加 `u`），保留两个自由质量等式 `sum p_h w_h=K`、`sum o_h w_h=O`。SAFE 的分母按准确有序前缀，PAIR 的 `Omean/Omean` 必须平均六个真实查询的完整 36 个有序索引对；不是六个对角对，也不是把 O 当行动。正整数预算是根 IC、五个尾大小帽、source 3/4/6 的 Omean SAFE 和完整 36 配对 PAIR。全 9159 矩阵系数、两个 K/O 参数列、全部 129 对偶余项均由独立 Fraction checker 重建；115 列余项正、13 列为零，`u` 列余项为零。并集帽和 K/6 地板权为零，故 TAIL 对任意六合法查询并适用。

## 有限证书和边界

指定 `K0=24376964954228547006/142891298915142483961`, `O=1` 时，71 行必要锥的精确匹配值是

`u*=197998925913631121419767306359/5379586156460209884457196512920 ≈ 0.03680560551592973`。

该原始点只有十个正质量原子，未给出六个最优标签逐标签会员或完整策略，所以不是完整 SPE，也不是反例。Main 的 NEW 在该点低 `≈0.0031215046388437047`；TAIL 的交点条件是 `K/O < 8701782449/37000646641 ≈ 0.2351791992564166`。全系统的独立审计状态为 `PASS_ALL_SOURCE_ROWS_PRIMAL_DUAL_AND_UNIVERSAL_HOMOGENEOUS_IDENTITY`，没有 outstanding errors；没有声称任意 K 上的根界最优、SPE 可实现性或 half。

## 与一般人数刚性对象的比较

一般对象对任意 `m>=2`、每份完整纯 SPE、任意合法 `T,Q` 给

`Delta_T=mu-|T|>=0`,
`F_T(Q)=|Q\T|+|Q∩T|/m <= u +(3m-4)Delta_T/2`。

在 `m=6`，逐客户转移式和求和消元正是核心 NEW/SIZE 所复用的 `tau`/`H` 部件；核心再加入真正最大裸大小 `C`、同一真实第五源 SAFE `G`、同一 B5 大小缺额、source 3/4/6 SAFE 及 full36 PAIR，才得到三条加强根线。因此“一般人数刚性”单独不足以推出核心三式；本比较是“通用 m=6 转移 + 六人真实尾部钱包”的条件性专化/加强，不能把它写成一般对象独立蕴含 TAIL。旧 edge 已准确编码了这一点（见下）。

## canonical 边复用和建议 JSON

已存在并已登记的现役边：

`map/edges/six-boss1-20261111/complete-history-rigidity-to-root-tail.json`

SHA256 `3f4cbe1410120e0d0bc1857da6adcd737e766551e45fc566672ca04d725dd059`（本地完整值可由 sha256sum 复核），edge id `ca-six-boss1-rigidity-and-true-tail-pay-root-income`，status `accepted`，kind `implies`，premises_mode `all`，relation_mode `unconditional`。其 source 是 `CAG-MODEL` 与 `customer-attraction/all-m-nearly-saturated-root-rigidity`，target 是核心对象；条件写清“恰六人、C 真实达到 K、O 任意六合法标签并、所有钱包沿同一完整 σ 真实历史”，roles 明确一般引理只支付 `tau/H`，CAG-MODEL 支付真实 IC/SAFE/CAP/PAIR，核心支付 NEW/SIZE/TAIL。该边已绑定 endpoint pins：

* CAG-MODEL `3216d1db43ff83e0e0c9cf2479e79611277c9d9291a68e7f9b85ec4bb299dc5c`
* all-m peer `fc9ad23fad83f04e23c4107d85f10995212c12864bead15c364e70ddec390469`
* core `997098f7fc23e8073978f1d5b917a8084682b084ebf5e8347decae795e7042b2`

建议继续复用该 canonical edge，不重复写同端点新 edge；本任务只交一份复用说明和 receipt。canonical edge 的数学说明正好与本轮实读一致：`H` 分解、`delta+(12/5)tau`、`65delta+72tau-35(p-y5)`、TAIL 十预算和全 128 型整数余项；范围明确不支付六人 half。

## coverage 处置建议

核心 coverage 应标 `linked`，`object_pin=997098f7...`，`edge_ids=["ca-six-boss1-rigidity-and-true-tail-pay-root-income"]`。comparison_scope 应包含核心引理、peer 一般刚性、共同定义、三套独立 audit、71×129 证书以及 31/31 SHA 当前核对；reason 应说明该边已完整承重三条根线和 H=0 障碍，但不推出 half/SPE 锐性。`assets` 可列现役 canonical edge（SHA `3f4cbe1410120e0d0bc1857da6adcd737e766551e45fc566672ca04d725dd059`）和本报告。

指定 overlap `core ↔ all-m-nearly-saturated-root-rigidity` 可写入 `closed_overlaps`：一般 m=6 转移已由现役 canonical edge 与本轮 full read 解决；剩余差异是 3A 六人真实第五/末两位付款，已在核心和 canonical edge 中完整给出，未发现需另发 3B 数学任务的缺步。`follow_up_tasks=[]`。若队列策略仍要求 3B 独立复核，则应新发一个只审“一般 m=6 RIG 如何被 G/full36 PAIR 加强”的定向任务，不能把本核心或现役边复制成第二条同端点边。

## 结论

本次没有新增逻辑边；已完整核对并复用 canonical `ca-six-boss1-rigidity-and-true-tail-pay-root-income`。核心对象可按 `linked` 完成，保留其三条全类型必要根线、有限锥证书和明确开放义务（half、SPE 锐性、全局最优性）。
