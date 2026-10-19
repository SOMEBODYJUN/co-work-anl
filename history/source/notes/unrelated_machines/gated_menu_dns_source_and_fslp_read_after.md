# DNS 福利舍入原件定位与 v1 作者证明读后记录

日期：2026-10-18。全部原字节和笔记在 clone 外，不改共同来源账本，不作 git 写入。

## A. DNS 原始作者稿

- Authors：Shahar Dobzinski, Noam Nisan, Michael Schapira。
- Title：Approximation Algorithms for Combinatorial Auctions with Complement-Free Bidders。
- 原始直链：https://www.cs.yale.edu/homes/schapira/cfjournal.pdf
- 本地原字节：`dobzinski_nisan_schapira_cfjournal_author.pdf`。
- 实际下载：urllib HTTPS，成功写入 278444 bytes；SHA256 `d0700d7674db45b4330d558c731c0200567f2c7a999f5eef7952029cab26dd15`。
- PDF 共 15 页。PDF metadata 为 TeX output `2009.10.30:2227`，CreationDate `D:20091030222754-05'00'`；首页及页眉有 journal 卷期、日期、DOI placeholder，因此只称 2009-10-30 内部生成的未注明正式版次作者稿，不能冒作 2010 MOR 正式排版或 2005 STOC 稿。
- 官方正式元数据：https://pubsonline.informs.org/doi/10.1287/moor.1090.0436 。官方页面实际检索/打开摘要给 MOR 35(1), 2010, pp.1–13，online date 2010-01-27；这与本地 15 页稿的页码不混用。
- 原始 web refs，可 root 直接 open：`turn14view0`（作者 PDF），`turn15view0`（§3.2 定位），`turn15view1`（Theorem3.2/Lemma3.3 原 proof 文本），`turn13search0`（官方元数据）。

实际阅读并渲染检查的范围：

1. PDF1/印1：首页标题、三位作者、placeholder；图像 `dns_page_01.png`。
2. PDF5/印5：Proposition2.1 的显式 XOS expression 可多项式模拟 demand 与 attaining-clause 查询；同页配置 LP。图像 `dns_page_05.png`。
3. PDF8/印8 §3.2：独立预分配后取相应 XOS clause，再按各物品最大 clause 系数分配；Theorem3.2 与 Lemma3.3 给有限 n 因子 `1−(1−1/n)^n`。图像 `dns_page_08.png`。
4. PDF9/印9：Lemma3.3 用 conditional item value、按平均 value 排序与 AM–GM 完成单物品最大值估计；图像 `dns_page_09.png`。

上述四页已本地提取文本并实际逐张查看渲染图。系统 pdftoppm 因缺 libpoppler.so.160 失败，随后 PyMuPDF 成功渲染；没有下载失败或绕过权限。只核对承重段，不声称全文内化。

数学归属：原单位 FSLP 的每 state 正 support 是质量一的可行配置，原 p_gsu 是它的一个 attaining clause。故新的独立 state→每资源最大系数福利论证是 DNS §3.2 机制的明确特化；精确有限 CDF 去随机化可自足给位复杂度。不能将福利比例或该机制本身称作新算法贡献。门控全作业值恒等、原 γ 互补纠错和特定 promise 的 LP 判别在本轮另行给自足推导，仍无全球新颖性认证。

## B. v1 作者完整证明实际读后

实际顺序如下，不能倒填：

1. 本人独立重构先冻 SHA `a7245326951f8c4e251552307c003fbbcc1d08efbe761c19f770843af5f2a5e3`。
2. 随后实际全文读 v1 正式 Exact SHA `591237d47b0330ebe6eb8d8daf509f467bc6fa663986905da13ce08ae40716e5`，冻读后攻击 `formal_exact_read_attack.md` SHA `d88c59cc9cc5eb023e6df6a4dfc3b5af96875db12cfaff6c5b7f26f581c4557a`。
3. 接 root 通知后，实际全文读 `../near_two_reduction/gated_normalized_menu_fslp_author_proof.md`，原字节 SHA `afdb45b8426145f1fc96029d68bd1aa568ce3fd4fc3a92028e22cc655d46e292`。

完整 Proof §1–7 与本人独立证明一致，未发现新 fatal。§2 公共分母 D_p*D_lambda 的位长支付正确；(4) 的严格 CDF `< level` 与有限 tail sum相符。§4–5 全原作业、零 incidence、未选 states、C≥2 分支与 β*=0 边界均已实际核对。§8 明确未来有限实验未运行，没有把拟验证内容假记为完成。

唯一建议：Proof 来源段可补 DNS §3.2 的直接机制归属，强于仅引用 Feige 官方摘要或泛称标准；Exact E4 ‘等价 promise’建议明确参数特例或称‘特别 gap promise’，如本人前一稿解释。该意见不反驳 v1 数学内容。

v2 whole-class 13/8 尚未审查，本记录不将 v1 通过转移到 v2。
