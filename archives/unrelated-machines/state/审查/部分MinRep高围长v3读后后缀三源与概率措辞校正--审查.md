---
id: "unrelated-machines/partial-minrep-high-girth-v3-suffix-review-20261031"
kind: "review"
type_tag: "审查"
title: "部分 Min-Rep 高围长 v3 读后后缀三源与概率措辞校正"
status: "complete-source-read-read-after-corrections-integrated"
truth_status: "factorial-moment-proof-confirmed-sampling-count-corrected-no-new-bridge"
review_level: "clean-show-full-read-proof-read-after-and-complexity-scope-audit"
scope: "partial_minrep_regular_high_girth_v3 independent-row reconstruction、read-after-PCSP、read-after-row"
summary: "三份后缀来源对前一批 high-girth v3 Exact/Proof/PCSP 进行读后攻击与复杂度补充：factorial-moment 点态密度证明有效，fresh-image short-cycle 论证有效，repair 同时性保持；唯一文字校正是实际 permutations 数为 dN，Proof 使用 2dN 是保守多计。该后缀不增加新的 source bridge、软件或 PCP 结果。"
source_refs:
  - "source:1adf040842bbb51868e1:history/source/notes/unrelated_machines/partial_minrep_regular_high_girth_v3_independent_row_source.md"
  - "source:1c5ff76cfa939112e428:history/source/notes/unrelated_machines/partial_minrep_regular_high_girth_v3_read_after_pcsp_source.md"
  - "source:3b1b06c474aefb6a2360:history/source/notes/unrelated_machines/partial_minrep_regular_high_girth_v3_read_after_row_source.md"
related_objects:
  - "../审查/部分MinRep高围长v3三源精读与随机repair边界--审查.md"
  - "../审查/部分MinRep费用桥与pDM阈值双源审查--审查.md"
evidence_paths:
  - "archives/unrelated-machines/tools/evidence/partial-minrep-high-girth-v3-suffix-20261031/"
---

# 1. 来源身份与阅读顺序

三源均先 `clean claim` 后 `clean show` 全文读取；双冻结提交同字节。

| ID | 路径 | 字节 | SHA-256 |
|---|---|---:|---|
| `1adf040842bbb51868e1` | `partial_minrep_regular_high_girth_v3_independent_row_source.md` | 13,129 | `7493f719723990b2aa4416b151bef1c84e947eaa71392cd378c0195c9b26fc3d` |
| `1c5ff76cfa939112e428` | `partial_minrep_regular_high_girth_v3_read_after_pcsp_source.md` | 7,616 | `8db3a1405825c243a21c57b7e603b72bcbcba43c48c78732cda8424366474fc0` |
| `3b1b06c474aefb6a2360` | `partial_minrep_regular_high_girth_v3_read_after_row_source.md` | 5,372 | `a012d2d0b32b4691d76e839ac0e87a97b68fd722ff9583ee75c80a60c6613c3e` |

三份后缀都指向前一批 v3 Exact SHA `0e2b614a...` 和 frozen Proof SHA `f43e32fa...`；不是新的参数域。

# 2. Factorial-moment 上尾的确认

独立-row 来源和 PCSP read-after 都验证：对一份 uniform ([t]) permutation 的 (r) 个不同 slots，images 相对于独立均匀抽样的点态密度为 (t^r/(t)_r\le e^r)。每层 template 是 perfect matching，因此 (k) 条不同 `(layer,templateedge)` 只涉及 (2k) 个不同 slots；不同原点/layer permutations 独立，联合密度至多 (e^{2k})。with-replacement 参照模型中边覆盖事件独立，于是

\[
E\binom Zk\le(e^2\mu)^k/k!.
\]

MGF/Chernoff 给出

\[
\Pr[Z\ge\rho M'/2]\le(e^3\mu/a)^a\le\exp(-\rho M'\ln g),
\]

再与全部 copy-list 的生成函数计数并界，得到坏事件 (<0.001)。这一路线严格保留了 permutation 的无放回相关性；不需要把边指示变量假设为独立或负相关。

# 3. Short-cycle fresh-image 与 repair

PCSP read-after 逐项核对 simple cycle 的延迟揭示：相邻 layer 必须不同（包括首末），最后 fresh image 的目标 copy 仍未被揭，闭合概率至多 (1/(t-G))。因此

\[
EX_{\mathrm{cycle}}\le NtS/(t-G)\le2NS,
\]

Markov 给 short-cycle FAIL (le0.05)。长度2按不同 layer 的 parallel edges 计，单边往返不算。

同 type/layer bucket 仍是 matching，短环占至多 (GB)，端点 G-ball 至多 (4U)，(z\ge GB+4U+1) 保证 clean edge。双边交换不生新短环、保持 degree/projection/bucket；每次至少杀一条旧环，至多 B 次。每次覆盖数变化至多2，(2B/M'\le\rho/4)，所以初始所有-lists 同时事件经 repair 仍给最终覆盖 (<\rho M')。

# 4. 唯一措辞校正：dN permutations 是实际数，2dN 是保守多计

Proof v3 第6节写“有 (2dN) 份 permutations”；实际算法是每 layer、每原顶点一份，共 (dN) 份，Fisher–Yates draws 为 (dN(t-1))。把 (2dN) 当保守上界仍合法：sampling FAIL 仅被更松地估计为 (le0.001)。条件所有 draws 成功时，接受值仍独立 uniform，算法使用的目标分布不变。

该校正只影响精确计数/FAIL 常数措辞，不影响 Exact 的 `<0.1` FAIL、NO 侧 `>0.8` 成功、固定 G 位复杂度和 high-girth source bridge。其他位复杂度补充：若枚举长度≤G 的 cycles，复杂度可保守写 (O((N'+M')^G))；固定 G 时仍是显式输入的多项式。

# 5. 处置、关系和边界

这三源全部整合到前一批 v3 high-girth 对象：

| 源 | 独有内容 | 处置 |
|---|---|---|
| `1adf040842bbb51868e1` | 独立 row reconstruction 的 slot-cap witness 和复杂度补充 | integrated-independent-row-reconstruction |
| `1c5ff76cfa939112e428` | Proof 读后 factorial-moment、fresh-image、repair 攻击 | integrated-proof-read-after-pcsp |
| `3b1b06c474aefb6a2360` | row read-after 的采样份数校正、cycle 复杂度细化和旧稿自我勘误 | integrated-proof-read-after-row |

不增加软件运行、外部 PCP 阅读、一般 UM compiler、near-2 hardness 或 CAG 结论。父 Boss 在 checkpoint/pushed 后逐源 done；本批未执行 clean done、commit 或 push。
