# Kun 两份定向修复的 fresh 3D 数学审查

结论：可在下列精确资产 SHA 和四个 v2 registration pin 上采用两份 done 包，均保留 accepted / unconditional / whole_result。没有发现新的数学错误、未付数学前提或本包输入的过时 pin。审查只读；没有改动仓库、队列、登记或边。交付提交以父 Boss 给出的 378f8d9198c219dc3379dffe3d40b7459dc86280 为起点；本轮末次只读 HEAD 是 83953cde20c637944dc395bd8a7f1b9aaa91ed7a，所审资产和来源字节保持下列 SHA。

| 当前任务 | 采用资产 | SHA-256 |
|---|---|---|
| map-repair-7491db9b84448830 | map/edges/map-repair-7491db9b84448830/fixed-seed-double-padding.json | 5d85de7dbcf86c79d9aa96b8557b6e42dc78aa0e7543686db33afaadb584df9d |
| map-repair-a78e71b42e9bd669 | map/edges/map-repair-a78e71b42e9bd669/sparse-and-modern-dichotomy-complete-fixed-signature.json | 2add47337243ac22dc5da9d8c69537472820802e03606ed6ffacdcf632a0573a |

两个任务的 definition、当前独立及嵌入 receipt、旧任务和旧 receipt、唯一旧资产均实读。receipt 与嵌入 receipt 相同，输入 pin 与 research show 一致，两个 edge-check 均返回 whole；这些结构检查只作绑定核验，数学意见来自下述原文和承重论证。

## 当前精确目标及固定参数合同

精确阶数包的目标 M-cdd66f04eebf4c44b73d62aece017919 v2 登记原句是“所有 n 足够大时可多项式时间构造 n 点、围长至少 k、度有界的 ε-expander 关系结构”。冻结 Kun PDF p.3 Theorem 3 的完整量词要求 M=M(τ,ε) 不依赖 k，阈值可依赖 τ,ε,k，且针对每一个充分大整数 n。Definition 5 还要求每个至少二元关系非空并分别扩展。新 whole_result 完整保留这些要求，算法只对固定 τ,k,ε 主张关于 n 的确定性多项式时间。种子大小和搜索成本可依赖 k；D_A、p 及最终 M=D_A D_B 不依赖 k。

同签名包的目标 M-e37dfe8f79184d5ba961c1e78cf3a558 v2 登记原句是“每个 MMSNP 语言 L 与某有限结构集 T 的 CSP(T) 多项式时间互归约”。冻结 PDF p.2 Theorem 2 进一步明写 L⊆Rel(τ)、T⊂Rel(τ)。新 whole_result 恢复相同输入签名 τ 上的有限模板族，并保留 CSP(族) 的有限析取语义。保证是固定 L、τ 的双向确定性多项式 many-one 判定归约，不是统一高效地产生模板/分支/归约的元算法，不保实例形状、围长或同态见证。仅一元/零元签名的独立剖面分支给出更强的语言字面相等。

四个 current v2 pin：

| 对象 | pin |
|---|---|
| M-2cade1d7f2d24941acd7fb06b938c73e | 2731a90af12bcb31c023bfe0342f847e6bc3128f60ec2d4be6101e8f472df37c |
| M-cdd66f04eebf4c44b73d62aece017919 | a4e4c065b40291de0d2f4684419381102f90eebf0cf979bbb71f8434a2e25db9 |
| M-dcddc9883c494fea8a4b270fdc4b10c7 | d7d4efe1412c23438b3c478da7574fadf9d36fbf4edbff31177248a421331e4a |
| M-e37dfe8f79184d5ba961c1e78cf3a558 | 0b180510308df6f911e049d3940293ba946379e5693bea94c500ee8109bb2d87 |

## 外部承重定理的实读合同

1. **LPS，Ramanujan graphs (1988)**：本轮实打开作者论文 PDF 的 §2 构造、§3 Proposition 3.3 与连通性/非二分分支、§4 Theorem 4.1 及证明的 Case ii。p,q 是不同的 1 mod 4 素数；(p/q)=1 时使用 PSL(2,F_q)，阶数 q(q²−1)/2，连通且非二分，除常数谱外的特征值绝对值至多 2√p。q≡1 mod 4p 恰支付二次剩余条件。故边内 ||P−J||≤2√p/(p+1) 的两侧绝对谱用法成立；没有误用二分 PGL 分支，也没有把普通图围长当关系围长。p 固定，q 充分大时生成元不同且非单位元，walk 点序列无平行边重数问题。这里复用已证谱定理，没有重证其数论证明。

   原文：https://courses.grainger.illinois.edu/cs598sgt/sp2015/LPS.pdf 。本轮 web refs：turn0view0、turn2view3、turn2view4、turn3view4；保存摘录对应 turn7view0–turn7view2。

2. **Kedlaya，Notes on analytic number theory §5.4 Theorem 5.10**：实读固定互素剩余类的 π(x;N,a) 渐近及相邻证明。N=4p 是固定模数，足以保证每个固定相对区间 ((1−ρ)x,x] 最终含可用素数，因而 s(q)/m→1。此处无需变化模数的统一误差界、有效阈值或仅有无限多素数的弱结论。新边用该作者讲义替代旧边的 Montgomery–Vaughan 来源说明，数学输入相同且已付。

   原文：https://kskedlaya.org/ant/chapter-5.html 。本轮 web refs：turn1view2、turn2view5；保存摘录 turn7view3。

3. **Kun–Nešetřil，Forbidden lifts，arXiv:0706.1704**：本轮实读 §3 canonical SNP 语法和三项限制；§6 pp.19–21 Theorem 14 的完整陈述、β/Ψ/Θ 构造及高围长反向归约证明。原中间定理明确允许“possibly different type”，并要求 girth>k。新边在 β 型应用源算法，t=1+max|T| 固定，源输出 girth>k，逐模板保持后取存在析取再与反向归约复合，满足准确合同。不能由该引文本身认定模板已经在原 τ 上；新边没有这样认定。同 τ 是后续现代独立桥付清的。

   原文：https://arxiv.org/pdf/0706.1704 。本轮 web refs：turn3view0–turn3view3；保存摘录 turn7view4–turn7view5。三项限制支持标准 MMSNP 的无不等式、单调输入、一元证书合同；零元/空域由边内切片和剖面证明处理，没有外推原定理合同。

4. **Bulatov，FOCS2017 Theorem 1，§II.A**：实读原文 p.2 定理及 CSP 的变量、有限域、固定有限 constraint language、显式 tuple 输入与解定义。它支付每个固定单模板的确定性 P/NP 完全二分；有限模板族的二分还需新边自行证明的最大同态反链与输入 marker。新边确实单列并证明这一步，没有把有限析取直接当作单模板，也没有声称重证 Bulatov 的整个算法。

   原文：https://www.cs.sfu.ca/~abulatov/papers/focs17.pdf 。本轮 web refs：turn1view5、turn2view2；保存摘录 turn7view6–turn7view7。

5. **Garey–Johnson–Stockmeyer，STOC1974 Theorem 2.1**：沿用原 done 包已经成熟的图 3 染色 NP 完全性及原论文定位，不重新科研重跑 SAT gadget 证明。本轮打开同一 UC Davis 主源扫描 PDF，服务返回 16 页但无可读文本；未把 screenshot 占位返回当成实际逐页阅读。因此本轮不声称重新实读该扫描证明。新边关于 τ 型 Hτ 及任意输入 X 的并查集逆编码是其自给的数学，已独立核对。旧 Barsukov–Madelaine 外引只是语法/闭合旁证；新边的 Forbidden lifts 标准语法和证书拉回证明已承接它，无独有数学丢失。

   原引用：https://www.math.ucdavis.edu/~deloera/MISC/LA-BIBLIO/trunk/JohnsonDavid2.pdf ，§II Theorem 2.1，印页51–53/PDF页5–7。本轮打开 ref turn4view0。

## 全目标与复用范围判断

精确阶数新包继续使用旧包的成熟随机固定 seed、谱到 walk 估计、多关系总度求和、乘积度与扩展误差及孤点补齐。新增的清楚分解为：先把 LPS 可达阶数 s 补 h=m−s 个点到恰 m，h/m→0；再做高围长乘积到 N=am；最后仅补 d=n−am<a 个点。前一层每坐标 h/m，最后一层每坐标 d/n；统一误差 ≤δ+(δ+rh/m)+rd/n≤4δ≤ε。关系非空、元组集合、度与关系围长的保持范围准确，最后输出不再被说成完整 twisted product。旧的一次 near-N 补点证明本身有效，已被保留并重新组织，未被虚构为错误。

同签名新包继续保留旧包已完整成立的 β 型归约、有限模板反链 marker、固定 τ 的高元三色模板、非平凡 P 的固定 yes/no 归约与仅一元/零元剖面。新增零元有限切片及空域有限例外，把外部定理的标准合同与退化模型接缝写清。有限模板集是析取；把全部模板不交并成单一目标会改变语言，这个错误用法已被明确排除。高元分支只需判定复杂度互归约；低元分支的逆同态闭合和 Q(X) 双向同态给语言相等。没有剩余的同签名数学缺步。

冻结 Kun §5 的原作者链经 Forbidden lifts 只显式提供可能异签名 β 的中间结果。2017年二分补全不得倒填成2013年作者证明；新 scope 已准确保持这一来源边界。目标是数学结论，现代独立证明完整成立，因此该来源边界不要求把本次 whole 降为 step。

## 逐资产 supersession

| 被替代任务的唯一资产 | 原 SHA | 处置和数学保持 |
|---|---|---|
| boss2-kun-fixed-seed-exact-n-3b-3b-a0d1b953a8e694c8/exact-order-by-dense-expander-sizes.json | 92b24c389967a66eab1d3c1ff9b6e6af22f4a1d88c1c2d08affc664a75af844b | replaced → 当前 fixed-seed-double-padding.json；全部有效数学保留，更新 v2 绑定并显式两段补点；旧 edge_id 退出，使用新 edge_id um-kun-fixed-seed-double-padding-all-exact-orders。 |
| boss2-kun-same-signature-3b-5d4dd1a8a16eca9d/sparse-and-modern-dichotomy-complete-fixed-signature.json | 7418da2ed6a0df46887531a1c7a41acf4f920ac2a37d9433e66d313fbd507360 | replaced → 当前同文件名新路径；保原 edge_id boss2-kun-modern-bridge-completes-fixed-signature 和 whole_result，更新 v2 绑定；旧03312e的β贡献直接写全后移除旧文件依赖。 |

两份收据各穷尽其原任务唯一资产；replacement_paths 均在新收据 assets 中，无有效旧证据被 retired。旧03312e v1/de08d9 文件本身仍是历史过时绑定，且其 contribution 正确只付 β 型结果；其旧 receipt 对 Lemma13 一元辅助关系须取满集的异议也实读。新边只调用已登记源算法，不以旧03312e文件作现行支持，故该历史 stale 不污染本次 whole。旧03312e并非这两份 supersedes 的额外资产，不冒称本轮把整个旧3A任务修复了。

## 剩余义务与采用文字

本范围无新的数学 open 或采用阻碍。无需补科学计算、重证外部成熟定理、重跑旧研究或另发同问题比较。可采用文字：

“在所列 current v2 endpoint pins 和资产 SHA 上，接受 Kun 两份定向修复的全目标支持。精确阶数构造完整保持每个充分大 n、M 与 k 无关及固定参数确定性多项式时间合同；同签名结论由异签名高围长归约与现代有限模板二分桥完整补全，有限模板析取、低元签名及零元/空域边界均已支付。逐资产 supersession 保留了全部有效旧数学；冻结作者的同签名来源边界继续保留。”

证据可复用性上的非阻塞建议：精确阶数边当前将 LPS/PNT 主源 URL 和位置写在 explanation 中，evidence_pins 只绑定本地 Kun 正文/PDF。旧同行也提出过把这两项外部主源进一步冻结为精确文件/页段证据的建议。本轮已实读核实相应定理，故不把文件加固当数学 open 或采用前置；此建议也不授权在本轮直接覆盖 done 资产。

完整本地实读 refs/SHA、current pin、任务及收据一致性、逐资产处置检查见 peer-review.json；本轮实际取得的外部正文摘录在 primary-web-excerpts.json。Kun 原 PDF 新提取文本与仓库保存文本逐字节一致（SHA 75fa6f933d8213316c0ad73660c9cc5f238b30f66ed44c7329f8b32b2fad4ac6）；本轮通过该文本实读原文，不声称视觉逐页审读 PDF。
