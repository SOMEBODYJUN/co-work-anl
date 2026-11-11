# v6 冻结摘要

Boss1；RUN `six-boss1-20261111`。保留全部546旧原始行，加320 P25和一条ROOT30_B2容量反馈；867 raw / 798 unique / 全256客户型+K共257列。仅一次已授权LP，准确恢复与独立Fraction检查全部通过，旧163冻结文件不变。

普遍下界与该指定必要系统的准确最优值为

\[
\frac W{\operatorname{OPT}_6}\ge
\frac{297031626302473255982375236165519763056}
{674971380794216193950126045384710917501}
=0.440065512041364\ldots.
\]

12正客户型、12正预算；867原行全部可行、257列对偶余项全部非负，互补且原对偶gap0。243列余项正，14列零，K余项0。四个正P25为源2的T4Q7、T5Q6、T6Q5、T8Q8；后者使用真实30个异索引对。新根反馈正付款，旧ROOT30和BG付款0。

完整整数付款、原子表与证明见 [proof.md](proof.md)。精确输入和证书为：

| 文件 | SHA256 |
|---|---|
| exact_input.json | `49532be5fae2913f2ab56ae641452510d7b0f8f14ff7049de0dd62fa7b9a8936` |
| exact_certificate.json | `98fa318efae0c6fef36e87b1861d559ede340ab4aaf7ed390c426854e5711f1d` |

0优化器的精确线性代数给整个必要系统最优面 z=z*+s e0，s≥0；14零列上的正行加norm秩13。整面 K约.19390807694515017、O=1，故O−K>0。

同一真实C根分支的新根线取等，却强制支撑仅在0,2,9,125四型，且同支CAP(B2)、CAP(B4)同时紧。这些型满足o−p=y4−y2，遂强制O−K=|B4|−|B2|=0，与整面矛盾。因此**整个v6最优面不能实现为SPE**。这不是half证明或SPE反例，也没有隐含一个未经量化的更好全域常数。

可复核：

```bash
python research/workspaces/six-boss1-20261111/universal_union_wallet_v6/check_source_and_certificate.py
python research/workspaces/six-boss1-20261111/universal_union_wallet_v6/check_face_and_root_equality.py
```

两者均无优化器。全部残差索引见`residual_index.json`；整面全257 signed identities及根全128 signed identity另存。Main将另行量化剩余根尾容量缺口；本包到此冻结并停止。
