---
id: "unrelated-machines/coordinate-slice-private-output-padding-v3-source-review"
kind: "review"
type_tag: "审查"
title: "坐标切片私有输出 padding v3 来源去向审查"
status: "retained-duplicate-provenance"
summary: "逐字阅读 v3 私有输出 padding 陈述，与 v4 坐标切片反例正文逐项对照；E--G 已由 v4 对象吸收，v3 不含证明或新的模型。"
truth_status: "source statement retained; mathematical status inherited only from the separately reviewed v4 object"
review_level: "full-source-read-and-current-object-comparison"
scope: "UM-Q-COORDINATE-SLICE-PARTIAL-MINREP-COUNTEREXAMPLE-v3, private-output padding Claims E--G"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/coordinate_slice_private_output_padding_exact_source.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/notes/unrelated_machines/coordinate_slice_private_output_padding_exact_source.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:archives/unrelated-machines/state/反例/坐标切片投影源编译--反例.md"
---

# 阅读范围与来源身份

本次实际读取冻结源 ID `0944f1eb99dd9e353daa`，路径为 `history/source/notes/unrelated_machines/coordinate_slice_private_output_padding_exact_source.md`，大小 2946 字节，SHA-256 为 `8abe3bf7eb704ad41acfffae69ed0f0fd1eb1a824fb9b0216698815c455331d7`。同一内容在冻结提交 `68fad804ec5946cb296f77dc5b336308a66abf12` 与 `aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c` 中出现；不把两个提交计成两个数学结果。

源标题是“坐标切片的私有输出padding：v3精确陈述增补”，稳定身份为 `UM-Q-COORDINATE-SLICE-PARTIAL-MINREP-COUNTEREXAMPLE-v3`。文本明确说明只给陈述、不含证明，并把 v1/v2 的哈希作为历史前置版本保存。其新增内容是 v3 的私有输出 padding，而非重新定义坐标树、列表覆盖或实际调度。

# v3 的精确陈述

输入是显式、非空、simple、平衡的 \(D\)-regular 二部全投影游戏，\(D\ge3\)，左右各 \(n\) 点，旧字母表 \(\Sigma_0\) 大小 \(Q_0\ge2\)，\(N=2n\)、\(M=DN/2\)。参数为二进制整数 \(g\ge2\) 与有理数 \(0<\rho_0<\rho\le1\)，并要求
\[
  \rho_0+2g/D\le\rho .
\]
左侧冲突图把共享右邻居的两个左点相连；最大度不超过 \(D(D-1)\)，按给定顺序贪心着色得到 \(\chi:A\to[s]\)，其中 \(s\le D(D-1)+1\)。增加互异的新符号 \(\alpha^*,p_1,\ldots,p_s\)，令
\[
  \Sigma'=\Sigma_0\cup\{\alpha^*,p_1,\ldots,p_s\},\qquad
  \pi'_{ab}(\alpha)=
  \begin{cases}
    \pi_{ab}(\alpha),&\alpha\in\Sigma_0,\\
    p_{\chi(a)},&\alpha\notin\Sigma_0 .
  \end{cases}
\]
因此 \(Q'\le Q_0+D(D-1)+2\)，图、正则度、平衡性和全投影保持；新 padding 的颜色是坐标名，边上的右邻居编号仍是坐标值。

源 Claim E：这是统一确定性位多项式变换；perfect YES 保持；若旧源在成本至多 \(gN\) 下任意列表覆盖严格少于 \(\rho_0M\)，则新源在同成本下覆盖严格少于 \(\rho M\)。证明义务是：删去新符号后得到旧列表，旧部分贡献严格少于 \(\rho_0M\)；每个新投影 token \((b,p_{\chi(a)})\) 至多充一条边，因为同一右点的相邻左点颜色两两不同且图 simple；新部分总贡献至多 \(gN=2gM/D\)。

源 Claim F：无论旧源 value 如何，把 \(\Pi' \) 编译成同一坐标切片树/实际任务后，所有玩家都可选同一新状态 \(\alpha^*\)。在任一测试 \(b\)，若邻居 \(a\) 的编号为 \(i_b(a)\)，就固定坐标 \(p_{\chi(a)}=i_b(a)\)，并在每个其他自由颜色坐标删除相应的一个值；保留 \(D-1\) 个根测试，形成满 \((D-1)\)-叉深 \(Q'\) 子树。因同一右点相邻左点颜色不同，一方固定的颜色坐标值被另一方删去，所以所有叶资源两两不交，得到实际 \(C\le1+1/D\)。

源 Claim G：若旧源满足 Claim E 的 NO，则 \(\Pi'\) 无 perfect 赋值（\(g\ge2,\rho\le1\)），而 v2 的精确单位阈值给出编译后 \(\operatorname{OPT}=1+1/D\)；若旧源 perfect YES，则 \(\operatorname{OPT}=1\)。源同时提醒：padding 本身统一多项式，但后续树展开含 \(D^{|\Sigma'|}\) 叶；只有固定 \(D,Q_0,g,\rho\) 后，对图大小的展开才是多项式，不能把变参数 binary \(D,Q_0\) 的展开误称统一输入多项式。源不引入未核的 simple hard 源族，也不宣称一般 UM-TARGET 反面。

# 与现有正文的逐项比较与去向

当前正式对象 [坐标切片投影源编译的精确阈值与反例](../反例/坐标切片投影源编译--反例.md) 的稳定 ID 是 `unrelated-machines/coordinate-slice-projection-source-compilation-counterexample`，legacy ID 为 v4。该正文已逐项包含 v3 的四个承重点：

1. 相同的冲突图与贪心 proper coloring 上界 \(s\le D(D-1)+1\)；
2. 相同的 \(\alpha^*,p_1,\ldots,p_s\) 新字母表与所有新符号统一走第二行投影；
3. 相同的 \(\rho_0+2g/D\le\rho\) 覆盖预算、每个新 token 至多充一条边的严格覆盖推导；
4. 相同的 \(\alpha^*\) 状态、颜色坐标删值、满 \((D-1)\)-叉子树、实际 \(1+1/D\) 上界、perfect/NO 两分支以及 \(D^{Q'}\) 规模边界。

v4 正文随后加入 v4 的双射/均匀纤维概率 NO 与 \(T_{CONFIG}=1\) 证书等扩展；这些不是 v3 源的内容，不能反向写成 v3 已证明。现有 v4 审查范围也明确区分 v3 padding 与后来追加对象，因此本文件不把历史审查或有限程序运行升级成 v3 的独立证明。

# 状态、限制与用途

- **处置：** `duplicate`，保留为独立来源审查与版本时序记录；数学承重正文唯一去向是 v4 对象，避免产生第二个相同反例节点。
- **证明状态：** v3 源自身仅陈述，无证明、代码或有限审计；Claim E 的 token 计数、Claim F 的树叶不交和 Claim G 的单位阈值需要引用 v4 正文中相应证明，不能把本源单独标为完整证明。
- **范围限制：** 结果只涉及该二部全投影坐标切片编译和给定 \(g,\rho_0,\rho,D,Q_0\) 条件；不推出一般 q-allocation、一般 UM-TARGET 的 hardness 或近二间隙。padding 的统一多项式性不消除后续 \(D^{Q'}\) 展开。
- **接续：** 第三阶段可把本审查作为 v3→v4 的 provenance/版本边，与 v4 反例对象相连；若以后要使用 padding 作为硬度保持变换，必须另给满足固定参数域的 hard 源族和完整编译复杂度证明。
