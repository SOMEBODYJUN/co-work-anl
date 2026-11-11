# 第二源嵌套重查询：751 行 P25+C30 符号模板

Boss1；RUN `six-boss1-20261111`。

**已准备 751 条真实必要预算的无点模板，优化器调用为 0。** 新包保留原 243 行，追加内部真实 sources3–5 的 507 条更强 P25 行，再追加一条同分支 C30。原 243 包与 v4 整面排除包均保持冻结。这里没有绑定已排除的 v5 点，也未建立任何固定点或8192列矩阵。

完整来源见 [derivation.md](actual_source2_nested_requery/derivation.md) 和 [source_review.md](actual_source2_nested_requery/source_review.md)。

## 行目录及真实收益归属

仍在实际历史 (A1) 分别强制六个合法比较菜单标签 Q_k，保留它们自己的真实四尾 R3_k,...,R6_k。变量为

\[
\nu_{v,q,r_3,r_4,r_5,r_6}\ge0,
\qquad v=(a_1,\ldots,a_6,x,o).
\]

nu 已含外层六分支平均，质量与查询矩界仍为

\[
\sum_{q,r}\nu_{v,q,r}=z_v,
\qquad \frac{o_vz_v}{6}\le\sum_r\nu_{v,1,r}\le o_vz_v.
\]

| 原始预算块 | 行数 |
|---|---:|
| 冻结原243行 | 243 |
| 真 source3，13×13 有序 P25 查询 | 169 |
| 真 source4，13×13 有序 P25 查询 | 169 |
| 真 source5，13×13 有序 P25 查询 | 169 |
| 真历史 (A1,Q_k) 后的 C30 | 1 |
| **总数** | **751** |

十三个描述子为 A1,...,A6,X,Q,R3,...,R6,Omean。前十二个都是纯合法角色；Q 的会员位是产生该外层分支的 q，不能当作 Omean。新的507行按 T 与末位查询的**有序**角色计数，两种单均值方向分别保留。

强制 Q_k 之后的 sources3–5 是同一完整 SPE 在相应合法历史上的真实行动，故可使用新来源定理。强制 source2 本身没有被赋予新的最优性条件。新行中的 v_i 都是强制分支自身的收益；继承行中的 actual MAX/MX/RC 仍使用原实际 P 及同一个 X。新增行只需要 X 合法，不迁移它的最大性。

## 507 条 P25 的准确付款

在新增来源 i 上，令

\[
n=6-i,\quad c=\frac{n+1}{2},\quad
p=\text{该真实分支在来源 i 前的负载}.
\]

Main 已释放的 P25 定理给出

\[
25v_i+cK\ge\sum m_{25}(p,t,q'),
\qquad
m_{25}=ct+\frac{24t}{p+n+1}+\frac{q'}{p+1+nt}.
\]

付款是25份真实源IC、每个中间真尾的大小帽各1/2、最后真尾的大小帽1份，以及该内层偏离分支自己的真末BR。K 系数在 sources3、4、5 上分别为 **2、3/2、1**。采用 Aν<=b 方向时，新增系数为 m25−25v_i，右侧为 cK。

内层强制 T 后用到的后继属于该偏离自己的真实续局，不能冻结为外层 R 标签。全尾覆盖是闭式最小值的一个达到态，但存在并列达到态；本模板没有由此推断尾标签唯一或同覆盖。

此前 P31 是较弱父族，准确关系为

\[
R_{31}(T,Q')=R_{25}(T,Q')+6\,SAFE_i(T)
+\frac{n-1}{2}\bigl(K-|T|\bigr).
\]

P25 的合法性有自身的非负付款；该身份用于比较强度。此次507行已经替换为 P25，没有重复追加 P31。

## 菜单平均与 C30

置 D=p+n+1，A=c+24/D、B=1/(p+1)、C=n/[(p+1)D]。四种查询成本为：

| 强制 T | 末位查询 | 使用的成本 |
|---|---|---|
| 纯 t | 纯 q′ | At+Bq′−Ctq′ |
| 纯 t | Omean | At+(o/6)(B−Ct) |
| Omean | 纯 q′ | Bq′+(o/6)(A−Cq′) |
| Omean | Omean | (o/6)(A+B) |

双均值成本来自同一六标签菜单的30个有序异索引对。不同索引允许同标签；纯 Q/Q 保持纯查询身份。外层1/6、单均值的内层六查询平均以及双均值的内层30平均各有自己的来源。

唯一新增 C30 行使用七位

\[
h=(a_1,q,r_3,r_4,r_5,r_6,o),
\]

其收益为同一强制分支的 v3、v4、v6。Main 冻结表的 cut 字段为

\[
126000v_3+65719v_4+4962v_6-m_{30}(h).
\]

因此本包 Aν<=b 的系数取 **−cut**，右侧和 K 系数均为零。没有把旧 a2 填入第二位，也没有使用实际路径 u3/u4/u6。

## 精确接口、来源哈希与检查

[单状态内核](actual_source2_nested_requery/symbolic_coefficients.py) 仅提供精确 Fraction 系数；[751 行目录](actual_source2_nested_requery/row_catalogue.json) 固定顺序并保留零行、重复行；[审计接口](actual_source2_nested_requery/audit_interface.json) 明确平均方式、K 系数和未来全域投影要求。

主来源固定为：

| 冻结来源 | SHA256 |
|---|---|
| P25 proof | `abe4e15a1d07b97ff230514f82415106267ad317bd94ef34ff0f0a3131f46bd0` |
| P25 exact family | `8965ab6534776f0cc9570979128df1e99835e0cc0bf60ce9d4a87b5354d4bec0` |
| 原243 kernel | `3b8a00fa72b2b15678656f7f2f21f18610ab2f1586d850b080a1d61235e4a205` |
| 原243 catalogue | `724a117332bdfed603990210daf83b5637828bf0a24cb8fc30b55c1344bd3ee0` |
| C30 全128包络 | `14ef732b35d0f859113daf92c8dda1f08330413682b057c69a57543a41a360bc` |

[来源绑定表](actual_source2_nested_requery/source_bindings.json) 及冻结来源清单保存所有169个引用或保护文件的哈希。原243目录及12个样本的前243条记录逐字段不变。

标准库独立检查器不导入生成器或新内核。它从真实份额重算200个内层隐藏状态和48个最小值，显式核768个双均值30对平均、3072个单均值平均、128个C30收益符号，以及12个边界状态上的6096条新增行；另匹配2916条继承记录。共核27036个 A/b_atom/b_K 有理数条目。[检查结果](actual_source2_nested_requery/literal_symbolic_check.json) 为 `PASS_SYMBOLIC751_UNBOUND_TRUE_INTERNAL_P25_AND_C30`。这不是全8192状态或任何固定点的证书。

## 下一精确点的接入边界

若未来 Main 释放的精确点有 s 个正旧型，物理变量为 **32s**，质量式为 **s**，原始不等式为 **751+2s**；phase-I 辅助变量另计。当前 [点释放模板](actual_source2_nested_requery/main_point_release_template.json) 的路径、点哈希、质量、K/O、支撑和优化授权均为 null。

若之后取得投影权，仍须在全部256旧型和8192新状态上精确计算两种 q 的四尾最小值，并在查询矩区间 [o/6,o] 上取端点包络。旧零支撑型、o0型和全零型均不可从普遍切面中删去。

当前包只完成有来源的符号必要层，不给出某点的可行补全、Farkas、完整SPE或半覆盖结论。后续点与唯一 phase-I 由 Main 独立释放；已排除的 v5 点未被绑定。
