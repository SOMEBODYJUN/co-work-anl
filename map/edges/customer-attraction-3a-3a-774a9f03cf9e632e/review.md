# 60 原子点的 2016 条必要行：有限投影与完整 SPE 边界

## 任务、对象与读取

本审读对应 `customer-attraction-3a-3a-774a9f03cf9e632e`，唯一核心对象为
`M-efbc6dcd98984d8087fec6a69c6179eb`，registration pin
`bc5414ff0a88a946b1d2e59c76690f0c020d112505b282bf9247631ab1fa2521`，内部词
`SOLVER-EFBC-FRESH`。没有改 registry、任务状态、coverage 或 Boss 文件。

任务声明的两个来源均完整读取并 SHA-256 核对：

* `archives/customer-attraction/state/审查/完整策略搜索与索引必要行的认证层级--审查.md`
  （声明节“60点的2016条额外必要行及本次完整核验”，SHA
  `783584c6c1b6a6e827bca98791909934fe4210a0b5ac797b4c733f18834936cd`）；
* `archives/customer-attraction/tools/evidence/product-background-and-completion-primary/new-product-completion-and-2016.json`
  （完整 JSON，SHA
  `13254694ba282fcb76402fead3c4735d4718359a1e8e00caa41b022695bee71d`）。

JSON 全部顶层区块均已解析；分段读取只是工程分块，不是截断证明。未将 deferred
`M-83073a4d06954c9cb02d2101b1627f7d` 或 `M-bb7d149596394020804ac192335b8678`
当作本轮已读端点，也没有 read-add。

## 模型、量词和核心有限证书

共同模型是有限单位客户、有限共同标签目录中的按序一次行动均分博弈；纯策略在
**所有有序历史**上定义。对象本身不是一般 SPE 定理：它固定同一输入 SHA
`11a26c56faca5a3331a4f2ab002455aa6ca115f999ddde2eced6f1edd39c0825` 的 60 个正有理
原子。原先 557 条必要行、`W=1` 和 `O>2` 的点由既有证据承担；本轮不重算旧 557
或 220 条跨族行。

21 个菜单为十个固定主题长度 1、长度 5 的 `T` 索引、三个旧末回复 `L` 菜单、
`AB`/`AE` 两尾 `R/S` 菜单和 `second` 的三后继 `H/I/J`。对真实两人 source，
每客户的末位精确量使用 `a_i=1/(p_i+1)`、`b_i=1/((p_i+1)(p_i+2))`；早期查询使用
真实改选后继的安全分母。source 在客户外整行选定，不能逐客户挑有利 source。

新定义完整重建三类行：

1. `Cartesian`：所有菜单索引的可重复无序二元组合共 231 种，乘 6 个 source，
   共 1386 行。逐原子系数是
   `n_M n_N Σ_i H_ix − (n_N M+n_M N)Σ_i a_i + M N Σ_i b_i`。
2. `ownindex_diag_offdiag`：三索引族固定一个位置 `z_j`、另一查询扫 21 个菜单，
   分 `i=j` 和 `i≠j` 两行；位置数 `3+3+4=10`，共 `10×21×2=420` 行。其系数
   使用审查中的 `D`、`O` 两式，保留同索引与异索引量词。
3. `direct`：`AB/AE` 各两个优化者、`second` 三个优化者及三个旧 `L` 族，共
   `10×21=210` 行。当前收益用 `n_NΣv_ix−NΣ(p_ix+r)^{-1}`；`L` 族的固定前三主题后
   强制 `T_i` 仍按精确末位/安全早期分母处理。

证据 JSON 给出 2016 行、120960 个逐原子系数；所有总 slack 非负，恰 10 行为零：
`direct:AB:2:AB.2`、`direct:AE:2:AE.2`、`direct:SB:1:Y`、
`direct:SB:1:AB.2`、`direct:SB:1:SB.2`、`direct:SB:3:SB.3`、
`direct:L.actual:L.actual`、`direct:L.second:D`、`direct:L.second:L.second`、
`direct:L.third:AE.1`。`old557_orGO220_recomputed=false`，故这不是旧记录的重跑。

量词严格是“同一 SHA 的 60 点、全部指定 2016 行和安全分母定义”。这只认证有限
投影中的非负性与零 slack，不能改写成任意可实现完整 SPE 的全称声明。2016 行中
有与旧必要行重复者，不能声称 2016 个独立新信息；2016 过行也不恢复两外族同索引
交叠。该点同时违反既有跨族 `query_equal`，但完整 Cartesian 的异型盈余可以掩盖
亏缺，因此不与该跨族失败矛盾。

## 同一 evidence JSON 的其它区块及边界

`product` 区块是伴随的静态/构造性校准，不是把当前 60 点变成动态 product 定理：
`K=1..5,r=0..5` 共 30 个参数、461 个 count vectors、24 个构造 product、44 个
有序结果；记录标记 `general_iff_by_analytic_proof_not_finite_scan=true`。`K=3,r=2`
给三组 `Q_t` 值 `['1','-1/2']`，根的隔离区间 `[63/100,16/25]`、最小多项式
`2t^2+5t-4`；`product_optimum_not_claimed=true`，所以不能把该可行值写成 product
全局最优。

`two_player` 区块是 13 单位客户的有限补全核验：目录 `A=[0,1,2,3]`、
`B=[8,9,10,11,12]`、`T=[2,3,4,5,6,7]`，阈值 6；9 个根行动对有精确 slack，
72 个字面节点比较、6 个形式回复政策对、2 份完整纯 SPE。仅有有序路径 `T,B` 可
完成，`not_half_counterexample=true`。它验证有限两人记录的范围，不能把广告路径或
2016 行静态投影提升为一般 SPE/half 证书。

## overlap、开放义务与交付关系

对象范围明确写明与主 owner `M-830...` 共享上述 60 原子输入。这个 overlap 是字节
/输入身份的复用提示，不是本轮已付的跨对象数学前提；M-830 及另一 deferred 候选均
未 read-add，因此本包不生成跨对象逻辑边，也不把共同定义当 hub 边。可复用的实际
信息是：固定 60 点上的三类必要行公式、行计数、精确零行和“跨族同索引尚未保存”的
边界。

尚欠义务是完整路径补全、所有有序历史 IC、真实 continuation 后的福利比较，以及
把任何 product/两人静态量映射到动态 `W`、`OPT` 的合法支付桥。没有普遍 SPE、half、
全策略 LP 或 2016 个独立证书；61 点两负和 9/5 策略属于其它原件/对象，不在本轮
重认证。故只交付一个 self-context `checks` 关系，固定有限证据与上述语义边界。
