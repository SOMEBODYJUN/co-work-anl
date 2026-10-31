# BCG STOC’09 degree-path primary：实际 target 阅读来源账

审查者：`/root/sol_nsw_independent_attack`。本账只记录实际读到的 primary 与它对 D_+ 路径 topology 的作用，不是全文文献 review，不是 K2 新颖性认证。

## 精确来源与实际范围

MohammadHossein Bateni、Moses Charikar、Venkatesan Guruswami，*MaxMin Allocation via Degree Lower-bounded Arborescences*，STOC’09 extended abstract，作者站 PDF：

<https://people.eecs.berkeley.edu/~venkatg/pubs/papers/maxmin-stoc09.pdf>

本次用 web reader 实际打开并阅读其 PDF text extraction，没有下载为本地 PDF，因而**没有本地原 PDF SHA 可报**；不得把 web excerpt hash 当成 PDF hash，也不声称读了全部 10 页。

按 web reader 对该 PDF 的 1,459 行编号，真正返回并读到的连续 excerpts 为：

- 首次 open：`turn703view0`，lines **0–407**，含作者身份、摘要、介绍、§2 和 Theorem 3。
- 随后按 §4 位置 open：`turn705view0`，lines **367–783**，含相关 allocation/gap 与 arborescence 部分；这不是当前 K2 承重来源。
- 本次 canonical 审查后重新定位 Theorem 3：`turn718view0`，lines **188–609**；再次实际读到 Figure 1 caption **290–295**、Theorem 3 及 proof **323–335**、caveat **336–337**、MinMax footnote **338–340**。
- 期间 find 返回过 selected snippets；本账不把 find snippets 计作额外全文范围。

这些 excerpts 的并集覆盖 text-extraction 0–783，但我不据此宣称 PDF 图片、排版或后续页面均已审。Line numbers 只标当前 web reader 的该次抽取结果，不当作论文正式行号。

## 已核到的来源角色

Theorem 3 已给出 degree reduction：将旧 item 按邻居拆成 d 份，以 d−1 个相邻 dummy players 连成路径，迫使至多一份供旧 taker。Footnote 同时提到 MinMax 情形与 better-than-two 阈值。故 D_+ 的底层 copies/path/helper topology 有直接先例，应明确引用 BCG，而不称为本次的新拓扑。

本次 K2 的新增义务是完整 ordinary flat jobs、zero/inactive routing、给定 degree-four rational functional、全局 M2、每机 CONFIG first/pair、global-affine physical load localizers 和全旧 moments 的双向保持。BCG 上述 target theorem/proof 未给这份合同；本审查靠页内独立数学推导核对它，**不把“未在这些已读段落给出”升格成全球不存在先例**。

## 时间与审查限制

BCG primary 的首次实际阅读发生在我的 K2 Exact-first 重构记录和 Author-Proof read-after 都已冻结之后，早于本次 canonical append 审查；定位 Theorem 3 的再次实际阅读发生在 canonical 340–536 全读后。因而不会把这份后得 primary knowledge 追写成 Exact-first 时已读来源。

我没有在本次打开 BCG 的 full-version technical report，没有审其全部引用文献，也没有认证 authors/root 之前读过哪些 source。其他相关来源各自只能按其真实读取范围登记。全球新颖性未认证；本账没有软件或 SDP 算法结论。
