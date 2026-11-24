# RA07 来源与作者说明

## 原件

- 原文件：`input/pdf/实分析7.pdf`，13 个物理页，无旧稿。
- 原文件 SHA256：`c053b24757b997ab489d1c18371df9ba44137919d53596b7158856ac1e8746c8`。
- 认领工作区：`work/notes-fc2ba28a26cd495f/notes/RA07/project/`。
- 作者、实际会话：`/root/ra07_rebuild`。协调编辑 `/root` 对第 1 页全页及问题裁图作过局部复读，并提供无限维命题补证；这不计第二遍或最终复核。
- 只使用该 PDF 作字迹来源。下面的数学材料只能支持补充命题，不能支持“原稿写了这些字”的断言。

## 图像与逐区观察

`prepare_pdf.py` 以 300 dpi、重叠 0.12 渲染。13 张整页均为 2480×3509 像素；每页依次实际查看整页，再查看六个高清重叠区。原件末页与空白分区均实际打开，没有用自动空白检测代替视觉阅读。第 7 页有一批工具输出超长被截断，随后将六区分成两批重新查看，记录依据为重看的结果。

真实工具路径为 `functions.exec -> tools.view_image({path: ...}) -> image(image_url)`。各页、各区完整文件路径及 SHA256 见 `project/manifest.json`；逐页布局与逐区首末内容、符号、留白、接续见 `observations-first.json`。11 张补充裁图坐标见 `crops.json`，均已实际打开查看，不只是生成。

## 外部数学核验

1. `/root` 提供并在作者回图后采用的无限维命题材料：`project/evidence/ra07-q001-root.md`。协调编辑实际打开核验了 [USC 大学讲义 Wiener Measure](https://dornsife.usc.edu/sergey-lototsky/wp-content/uploads/sites/211/2023/06/Week8-ByDiogo.pdf) 的相关页。作者复核 Riesz 引理、R/2 中心与 R/8 小球的分离、包含及可分覆盖推导。正文把它写为适用范围明确的蓝色补证，没有把局部有限性、可分性等补充条件改成黑色原文。
2. Solovay 原论文：Robert M. Solovay, *A Model of Set-Theory in Which Every Set of Reals is Lebesgue Measurable*, Annals of Mathematics 92 (1970), 1–56，DOI 10.2307/1970696。[期刊原始页面](https://annals.math.princeton.edu/1970/92-1/p01) 与[原论文 PDF 镜像](https://www.liutianren.com/discrete/ref/Logic%20and%20Set%20Theory/Solovay-ModelSetTheoryEvery-1970.pdf)。本作者实际检索到原论文 Theorem 1 的文字并打开期刊原始书目页面，核对“ZFC 加不可达基数的传递模型”假设以及“ZF+DC、所有实数集 Lebesgue 可测”的结论。没有把 forcing 构造补称为原稿已有证明，也不声称自己逐页视觉读过该 57 页扫描论文。

其余蓝色证明为作者依源内容写出的数学补充；依赖顺序记录于 `study-order.json`。无旧稿，故没有迁移旧稿独有内容。

## 原色与新增内容

转写中的公式错误、重复、残缺、提纲词和原稿用语保留。学习稿用 Obsidian `> [!info]` 标出补充、补证、纠错；原明确提问或 Proof 待填处用红色文字说明。普通物理空白页、边缘留白不标红。两幅原集合图均保留原裁图，使用仓库分支的稳定 raw URL，便于正文原字节复制到 output 后继续显示。
