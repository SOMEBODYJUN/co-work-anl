# 不交单客户静态安全值：product 取等分类与 half/SPE 边界

## 任务与实读范围

本审读对应任务 `customer-attraction-3a-3a-61fdfdbdfd7b0fb1`，对象是
`M-64d638d96fb64c1fa45fd17638164363`（v2，registration pin
`c4b90c219b5d6a430913be673c32d668fbec8ca0bfd41a91eabfaa08d875550d`）。身份为
`SOLVER-M64-OBLIGATION-FRESH`。任务只声明这一数学对象，未声明可直接联结的
其它对象；没有把 deferred candidates 当作本轮证据，也没有改 registry、coverage、
integration 或 task state。

三个 declared refs 均从当前 clone 全文实读并核对 SHA：

* 定理正文 `archives/customer-attraction/state/定理/不交单客户安全值的独立背景取等分类--定理.md`
  （`1f6b837ea0f3b5ec05714d74bbaabecbdfffc1c27f2a2ecc689930fcf5196ef5`）；
* 审查正文 `archives/customer-attraction/state/审查/完整策略搜索与索引必要行的认证层级--审查.md`
  （`783584c6c1b6a6e827bca98791909934fe4210a0b5ac797b4c733f18834936cd`），全文包括
  “当前实际执行与关系”；
* 证据 JSON `archives/customer-attraction/tools/evidence/product-background-and-completion-primary/new-product-completion-and-2016.json`
  （`13254694ba282fcb76402fead3c4735d4718359a1e8e00caa41b022695bee71d`）。

## 对象模型、量词与精确结论

模型是共同有限标签目录中的静态安全问题。目录有 (K\geq1) 个两两不交的
单客户主题，(r=m-1\geq0) 个竞争槽；竞争者在查询抽取前预先固定一个不看
query 的联合分布，允许任意相关、重复主题和确定动作。查询 (j) 面对计数
(H_j) 的支付是 (g(H_j)=1/(1+H_j))。定义

\[
 v_m=\min_{Q\in\Delta([K]^r)}\max_j\mathbb E_Q g(H_j),\qquad
 v_m^{\rm prod}=\min_{p_1,\ldots,p_r\in\Delta([K])}
       \max_j\mathbb E_{p_1\otimes\cdots\otimes p_r}g(H_j).
\]

写 (r=qK+s)，其中 (q\geq0)、(0\leq s<K)。定理对所有 (K,r) 全称地给出

\[
 v_m=V_{K,r}=\frac{K-s}{K(q+1)}+\frac{s}{K(q+2)},
 \qquad
 v_m^{\rm prod}=v_m\iff s=0\text{ 或 }s\mid K.
\]

这里 product 是**不同边缘但跨槽独立**的产品；没有假定不同主题的负载相互独立。
任意相关 (Q) 的最优值总是 (V_{K,r})，而 product 在 (s\nmid K) 时只能取得严格
更大的 cap。连续的 product 参数空间是有限个单纯形的紧乘积，cap 连续，故
“没有 product 取等构造”在 (s\nmid K) 时确实升级为严格 gap；这一步不是有限
扫描外推。

## 证明承重步骤

对每个整数 (h\geq0)，有精确割线余项

\[
 \frac1{h+1}-\left[\frac1{q+1}-
 \frac{h-q}{(q+1)(q+2)}\right]
 =\frac{(h-q)(h-q-1)}{(h+1)(q+1)(q+2)}\geq0.
\]

余项只在 (h=q,q+1) 为零；对每个查询求和并使用
(sum_jH_j=r)，得到所有联合背景的均匀查询下界 (V_{K,r})。把 (s) 个负载
设为 (q+1)、其它负载设为 (q)，再对标签作均匀循环平移，得到查询无关的
相关背景，反向达到 (V_{K,r})。这给出 (v_m) 的精确值，不使用 SPE。

若 product 也达到 (V_{K,r})，均匀查询的平均值和每个查询 cap 都必须同时取等，
因而每个 (H_j) 几乎处处只落在 ({q,q+1})。在固定主题 (j) 上，跨槽独立使
(H_j) 是 Bernoulli 和；其非退化项数不能超过一，且唯一非退化命中概率必须为
(s/K)。于是每主题恰有 (q) 个确定命中槽，余下 (s) 槽的正概率支持必须两两
不交并覆盖全部 (K) 主题；每槽支持大小为 (K/s)，所以必有 (s\mid K)。反向
按 (s) 个大小 (K/s) 的块构造余槽边缘，得到充要性。这个必要性只使用槽间
独立，不是把不同主题误当作独立。

## 证据层级与有限检查

证据 JSON 的新数学入口一次成功、无失败数学入口、无外部 solver/原 CLI。其 product
部分在 (K=1,\ldots,5)、(r=0,\ldots,5) 的 30 参数上解析 461 个计数向量、
24 个构造 product 和 44 个有序结果；这些只作解析证明的有限校准。JSON 明确标记
`general_iff_by_analytic_proof_not_finite_scan=true`，所以定理的全称量词来自上述
证明，不来自 30 点穷举。

特殊 (K=3,r=2) 中，给出

\[
 t=(\sqrt{57}-5)/4,
 \quad 2t^2+5t-4=0,
 \quad p_1=(t,1-t,0),\quad p_2=(0,1-t,t),
\]

三查询相等并得到可行 product cap

\[
  v_3^{\rm prod}\le (13-\sqrt{57})/8,
 \qquad 2/3<v_3^{\rm prod}.
\]

这是一个可行上界，`product_optimum_not_claimed=true`；不能把根式值称作 product
全局最优。根 (t) 的有理隔离区间是 ((63/100,16/25))，只用于合法性和严格
大于 (2/3) 的检查。

同一 evidence JSON 的其它部分是不同问题的层级校准，不能反向补成 M64 的全称
结论：

* 13 单客户两人目录的小例有 72 个字面节点比较、2 份完整纯 SPE；9 条候选路径
  只有 `T,B` 满足阈值路径条件，JSON 明确 `not_half_counterexample=true`。
  这验证了“有限完整 SPE 记录”和“静态 product gap”可以并存，不能把 product
  gap 当作动态反例。
* 60 点的重建有 21 个菜单，2016 行（1386 Cartesian、420 own-index、210 direct），
  120960 个逐原子系数；所有总 slack 非负、恰 10 行为零。它是同一 60 点的静态
  必要行重建，且与旧必要行有重复；不是全策略 LP 上界，也不支付完整 SPE。
  61 点两条负行只按原记录合同保留，当前证据没有把它们重新认证，不能将其升级为
  本轮新的负证书。

## 与 half 和完整 SPE 的实际关系

M64 只回答“竞争背景在静态安全定义下能否把所有不交单客户的查询边际同时压到
何值”，并分类一个更窄的独立 product 可行域。它没有玩家顺序、完整有序历史、
真实偏离后的 continuation 或福利 (W,\mathrm{OPT}_m) 的连接，因此不能单独推出

* 任意完整纯 SPE 的 (W\geq m v_m) 或其它福利支付桥；
* 全模型的 `half`（例如 (mathrm{OPT}_m\leq2W)）；
* 存在或不存在某个目录的完整纯 SPE；
* (K=3,r=2) 的严格 product gap 是 half/SPE 反例。

尤其，(v_m) 的精确值允许任意相关背景通过循环平移取等，而 (v_m^{\rm prod}) 的
严格 gap 只说明“把背景额外限制为跨槽独立”会损失取等；不能把这一表示限制偷换成
原动态博弈的合法策略类。随附审查明确把静态表示障碍、完整 SPE 辅助桥、必要行松弛
和原 half 目标分开。

M64 对后续 half/SPE 研究的可用作用是一个**静态基准接口**：若另有独立证明把某一
完整 SPE 的真实偏离支付或银行/菜单分解化为本对象的静态 (K,r) 安全问题，则可以
代入 (V_{K,r})；此类额外映射必须保留完整客户模型、量词和 continuation 条件，
不能由 M64 自身补齐。已有其它批次的 bank 或 singleton-menu 边可以复用该接口，但
本任务没有重读那些端点，故本包不重复生成跨对象逻辑边。

## 开放义务

1. 对任意实际目录和完整纯 SPE，尚缺把真实历史 IC 推到静态背景安全值的合法支付
   桥；M64 不承担该桥。
2. 若目标只需 product 背景，还需说明动态对象确实限制为跨槽独立且给出对应的
   量词；否则只能使用任意相关的 (v_m)，不能使用 (v_m^{\rm prod}) 的 gap。
3. 需要 full-SPE 反例时，必须提供所有有序历史、全部合法偏离、真实 continuation
   和精确福利；本包的两人 2-SPE 记录和 60 点静态行都没有完成这项义务。
4. 不能从 30 个有限参数、2016 条有限行或 61 点原记录推断全模型最优性、普遍
   half 或严格反例。

本包因此只交付一条 self-context 边，明确对象内部证书与 half/SPE 语义边界；不将
“尚未建立动态桥”写成对象身份或来源问题。
