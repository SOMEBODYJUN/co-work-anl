# Vontobel–Koetter 2005 v1：原文、阅读证据及有限重放

对应正式对象：[图覆盖译码与基本多面体](../../../state/文献/图覆盖译码与基本多面体--文献.md)。源ID `e367617bfd1e98dfb971`，冻结来源路径 `history/source/literature/unrelated_machines/vontobel_koetter_2005_graph_cover_decoding_v1.pdf`；两个冻结提交内容相同：`68fad804ec5946cb296f77dc5b336308a66abf12` 与 `aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c`。封面为arXiv cs/0512078v1，2005-12-20；67页、660122字节，SHA-256 `d6b6f7868f5a80220586b0394a55c244f6732b787e4aa9945baf0369167366cf`。

## 文件

- [原PDF](vontobel-koetter-2005-v1.pdf)：经 `python tools/cleanup.py --repo . show e367617bfd1e98dfb971 --out <path>` 直接恢复；没有通过work.py读取认证。
- [全文布局提取](fulltext-layout.txt)：`/usr/bin/pdftotext -layout`，共4225行；公式符号可能失真，不能替代PDF视觉核验。
- `rendered/page-*.png`：28页渲染。第27页110dpi，其余85dpi。`contact-1.png` 至 `contact-5.png` 为阅读用接触表；第27/28/45/51页另直接打开单页检查等式、锥约束、指数常数及有理构造。
- [精确重放程序](replay.py)及[实际输出](replay-output.json)：仅标准库 `Fraction`/整数，无浮点容差。
- [文件清单及哈希](manifest.json)：保存源身份、阅读范围、渲染页码和上述文件的SHA-256。

## 复现

在仓库根运行：

```bash
/usr/bin/pdfinfo archives/unrelated-machines/tools/evidence/Boss7-vontobel-restored/vontobel-koetter-2005-v1.pdf
/usr/bin/pdftotext -layout archives/unrelated-machines/tools/evidence/Boss7-vontobel-restored/vontobel-koetter-2005-v1.pdf archives/unrelated-machines/tools/evidence/Boss7-vontobel-restored/fulltext-layout.txt
python archives/unrelated-machines/tools/evidence/Boss7-vontobel-restored/replay.py
```

需要重建某页图像时，以第27页为例：

```bash
/usr/bin/pdftoppm -f 27 -l 27 -r 110 -png -singlefile archives/unrelated-machines/tools/evidence/Boss7-vontobel-restored/vontobel-koetter-2005-v1.pdf archives/unrelated-machines/tools/evidence/Boss7-vontobel-restored/rendered/page-27
```

本环境PATH中的runtime Poppler缺动态库；使用现成 `/usr/bin` 的Poppler后成功，不涉及安装、提权或外部认证。原PDF的Type3字形有bounding-box警告，渲染仍可读；数学读取采用全文与原图交叉，不靠提取中的丢失符号判断等式。

## 重放做了什么

1. 为Example4/7/57的两行校验矩阵和 `(2/3,2/3,2/3,0)`，从给定局部有理分布构造3-覆盖。程序检查每条边是真置换、所有提升校验为偶数、类型平均恰为目标有理向量。
2. 穷举引言长度3码的全部8个二元向量，确认唯一真实码字为000，并保留基本多面体端点2/3的局部总和界。
3. 明确核对v1第27页Lemma24误印等式的反例：`H=(1,1,1)`、`z=(1,1,1)` 满足所有基本锥不等式，而总计数为奇数。对任何覆盖阶数，全部提升偶校验求和都迫使计数总和为偶数，所以它不可能是未缩放覆盖伪码字。该奇偶理由是对任意M的解析反证，脚本只核对反例数值。

程序不是通用LP求解器、一般解码器、SPA/MSA仿真或调度工具；没有运行文中仿真的60/30/100迭代实验，也没有运行仓内调度cover审计。Prop.10/22和其他一般结论来自原稿证明的实读；不能用这一有限重放冒充一般验证。源错误和必要条件均在正式对象的【数学审查】中明示。

## 阅读及关系记录

逐页语义阅读记录和仓内比较位于 `cleanup/workspaces/Boss7/resume-20261031-current/vontobel/reading-notes.md`；逐源处置草案为同目录 `receipt.json`。两份相关调度原稿也只为比较恢复在该工作目录，不新认领、不作额外完成登记。

本轮为Boss7现有认领的本地整理。没有执行Git add/commit/push、start、doctor、claim、done、checkpoint、send或handoff；是否推送由父Boss串行处理。源文献的“有理局部一致点可在某覆盖实现”与调度专门结果仅为来源/机制关系，不能跨到一般LP整数化、R||Cmax统一近似或六人SPE。
