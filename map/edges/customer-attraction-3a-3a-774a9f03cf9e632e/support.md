# 数学支持：2016 条必要行的精确范围

## 1. 三类行的共同输入

固定原 60 原子、正有理质量和同一输入 SHA
`11a26c56faca5a3331a4f2ab002455aa6ca115f999ddde2eced6f1edd39c0825`。21 个菜单只
通过菜单长度 `n_M` 与会员总数 `M` 进入客户系数；source 在客户外一次选定。对真
末两人 source，令 `H_ix` 为强 PAIR 的客户量，
`a_i=1/(p_i+1)`、`b_i=1/((p_i+1)(p_i+2))`。

## 2. Cartesian 与 own-index 行

对菜单 `M,N` 的完整 Cartesian 行，单客户系数为

```text
n_M n_N Σ_i H_ix − (n_N M+n_M N)Σ_i a_i + M N Σ_i b_i .
```

21 个菜单的 231 个可重复无序二元组合乘 6 个 source，得到 1386 行。该笛卡尔积
保留所有查询组合，但将不同三索引等号型的盈亏合并。

在三索引族固定本族位置 `z_j`、让另一查询扫菜单 `N` 时，按 `i=j`/`i≠j` 分行；
令 `q=5`、`Z=Σz_i`、`Z_a=Σz_i a_i`、`Z_b=Σz_i b_i`，两类客户系数为

```text
D = n_N Σ_i H_ix − n_N Z_a − NΣ_i a_i + N Z_b,
O = (q−1)n_NΣ_i H_ix − n_N[ZΣ_i a_i−Z_a]
    − (q−1)NΣ_i a_i + N[ZΣ_i b_i−Z_b].
```

可取位置数为 `3+3+4=10`，故共 420 行。两式只给一个本族索引与另一菜单全扫，
并未给两个外族查询的同索引交叠。

## 3. direct 行、结果与零点

当前节点查询的单客户系数为

```text
n_N Σ_i v_ix − N Σ_i (p_ix+r)^{-1}.
```

末位 `r=1` 用精确分母；较早节点使用真实改选后的最坏后继下界。三个旧 `L` 族
位于固定前三主题后强制 `T_i`，故仍可由既有菜单重叠字段计算。`AB/AE/second` 七个
索引节点族加三个 `L` 族各扫 21 菜单，共 210 行。

完整重建给出 2016 行和 120960 原子系数；`all_nonnegative=true`，`minimum_total_slack=0`，
`zero_total_slacks=10`。零行正好是：

```text
 direct:AB:2:AB.2
 direct:AE:2:AE.2
 direct:SB:1:Y
 direct:SB:1:AB.2
 direct:SB:1:SB.2
 direct:SB:3:SB.3
 direct:L.actual:L.actual
 direct:L.second:D
 direct:L.second:L.second
 direct:L.third:AE.1
```

`old557_orGO220_recomputed=false`；旧 557/220 证据和本次 2016 重建分层保存。

## 4. 证据 JSON 的有限校准

* `product`：30 个 `(K,r)` 参数、461 个计数向量、24 个构造、44 个有序结果；
  全称 iff 标志来自解析证明而非该有限扫描。`K=3,r=2` 的隔离区间为
  `[63/100,16/25]`，最小多项式为 `2t^2+5t−4`，但记录明确没有声称 product
  optimum。
* `two_player`：13 客户，目录 `A/B/T`，阈值 6，72 个字面节点比较、6 个形式回复
  政策对、2 份完整 SPE；9 条候选路径只有 `T,B` 完成，`not_half_counterexample=true`。

这些数字只作为伴随 evidence 的审计层级，不能替代 60 点必要行的量词，也不能提供
全模型完整 SPE 或 half。

## 5. 数学边界

2016 行均非负只说明该固定点通过指定菜单投影；它不认证可实现性、策略存在性或
福利比。跨族 `query_equal` 失败与完整 Cartesian 过行可同时成立，因为异型行的
盈余可能掩盖同索引亏缺。要推进开放问题，需支付完整历史偏离和真实 continuation，
并明确把静态/product 查询量映射为同一动态福利 `W,OPT`；本支持片段不提供该桥。
