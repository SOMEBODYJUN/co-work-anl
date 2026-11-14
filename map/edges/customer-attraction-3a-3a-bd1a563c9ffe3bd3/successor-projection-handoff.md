# 5112 与两个扩展主图的定向比较

承接任务 **boss5-terminal-5112-projection-3b-3fd0485284c9f819**。端点分别为原 5112 点 `M-f741bf740e11475da1c2938cdad9c288`、5277 点 `M-7b187928aed64027bd7b4dee58308400` 及 5692 点 `M-96807ccbb51d4a04a699093e9211323e`。

## 继承行与投影

三份冻结点的前 1905 个非 weight 描述符逐项相同。5112 使用 5043 基础行、后期 continuous 32、portfolio 8、capacity 29。原 `combined_branch_master.py` 在同四个基础开关下调用同一个 `floors.build()`，再加早期 continuous 64、第四位 B 的一条旧投影行，`--latest` 加与 5112 字节相同的 32、8、29 参数及三条早 B 投影。于是 5180 含全部 5112 行及另外 68 条。按矩阵逐行识别而非假设 5112 行是最前面的连续切片。

5277 固定入口强制 `--latest --local-v2`，另加 18 条旧坐标切面及 79 条显式 B 行。旧 1905 坐标不动，在其后加 128 个 Bstate 坐标，继承行、目标和归一化系数在这些列都补零。5692 的主入口只强制 `--latest`，由 5180 加 314 条 B-family、170 条 Mroot、28 条四菜单行，在旧前缀后加 896 Bstate 与 2048 Mrootstate，继承行同样补零。因此向下投影均保 \(O,W,K\)。两扩展共享祖系统，5277 的 18 条局部行没有自动继承到 5692。

## 严格性与冻结交叉试算

分别保留并求和全部 16 个 hist，即使若干 hist 的 \((a,d)\) 相同也不能覆盖。冻结 5112 点的 64 条额外早期 continuous 行全部正，第四源旧尾部 B 投影也正，三条额外早 B 投影源 2/3 严格负、源 4 正。前两精确余量为

\[
-\frac{96627384659132786611213858155393356035451671}{92506895642307409887983828615724072241775},
\qquad
-\frac{2903074722056357887410271810639861408124129}{333024824312306675596741783016606660070390}.
\]

它们是两个扩展都继承的旧坐标行，任何新增列赋值都无法补偿。因此是两个严格的向下投影包含的简短证据。

5277 的 18 条 local-v2 还给出不同的固定统计分离。使用原三个行函数的纯 AST 定义，以有理数对原输入逐行点乘，结果如下。

| 冻结点 | nested 5 | requery 5 | portfolio 8 |
| --- | --- | --- | --- |
| 5112 | 第 1、2 负 | 第 1–4 负 | 全正 |
| 5277 | 全正 | 两零、三正 | 一零、七正 |
| 5692 的前缀 | 第 1、2、5 负 | 第 1–3 负 | 第 1 负 |

5112 的第一条 nested 为 \(-51894544608554995280563630063793761374981/78697466260823759739905602679968782737522828\)。5692 的七条是对 5277 实际 `--local-v2` 的分离，与已登记五条 pending 的比较不同。这给出 5692 前缀不落在 5277 的投影域。

## 不用早 B 投影的独立证书

两个显式扩展的实际第四源强制实际末主题分支中，取 \(12\,\mathrm{IC}+2\,\mathrm{cross}[4]+2\,\mathrm{cross}[8]+3\,\mathrm{cross}[9]\)，下标从零开始。设 \(p=a_1+a_2+a_3\)，\(b=a_6\)，\(x=p+b\)，新中间及末位会员为 \(q,r\)。设 \(B_*=6^{-1}\sum_w H_w w_B\)，\(C_*=6^{-1}\sum_w H_w\,\mathrm{sh}(w_C,p+|w|)\)，\(D_*=6^{-1}\sum_w H_w/(p+w_T+w_B+1)\)，其中 \(\mathrm{sh}\) 是零分子为零的份额。逐块组合系数为

\[
12\mathrm{sh}(a_4,|a|)+5C_*+\mathrm{sh}(-12b+2r,x+q+r)
-\frac{2B_*}{x+q+1}-(2q+3r)D_* .
\]

源 IC 的真实被强制主题会员是 \(b=a_6\)。cross[4] 用真末回复查询六个旧 \(B_j\) 的平均，cross[8/9] 用旧 \(C_j\) 对新中间及真末主题的安全比较。四行不使用 \(\ell\) 或 \(K\)。两份显式源码逐块核同式。固定 5112 的每块质量，取四个 \((q,r)\) 的逐块最大并加权，仍严格负

\[
-\frac{245604769923895081791133830617787185909}{74005516513845927910387062892579257793420}.
\]

故两个显式扩展中，即使只保持 5112 的 hist 而允许另选全部 R/Z 边缘、RR 辅助量和 K，也无法付这组第四源必要行。此为原已保存行的非负组合，结论不依赖探索乘子的浮点过程。用于 5692 的 `b-family-menu-prices-boss3/replay/research_2/coupled_B_families_master.py` SHA 为 `7f91a363a1eca0fdcb90fbae589130b03f4b74b716d3836652093166d093a7e1`。

可运行 [精确回代](replay_successor_projection.py)，逐项核 68 条共用增量、18 条 local-v2、实际第四源的四态上包络、第三源的八态上包络和 5277 已存的全部 18 余量。见 [实际输出](successor-projection-audit.txt)。

## 5277 前缀也无法升到 5692

实际第三源强制实际末主题的显式 B-family 行中，依次对 \(\mathrm{IC},M,Z,\mathrm{CAP:hidden:3},\mathrm{cross}[8],\mathrm{cross}[12],\mathrm{cross}[13],\mathrm{cross}[14]\) 赋非负权 \((670,9,1,4,76,32,100,105)\)。逐 hist 对八个隐藏会员模式和末位过去负载 \(\ell=0,6\) 求最大。其中只有原 `menus` 的 M/Z 系数依赖 \(\ell\)，并且在固定会员位和 \(d\) 后都对 \(\ell\) 仿射。端点最大值控制所有中间整数。按冻结 5277 hist 加权再加 \(4K\)，所得严格负

\[
-\frac{1505595416077174278327675259267902161027078757}{735576345002473658294053882445594433882234368}.
\]

相同证书在原 5692 前缀的上界严格正。冻结 5277 点据此没有 5692 扩展，即使更改任何新增显式列。结合反方向的七条 local-v2 违例，两者投影域不可比。代码中逐项保留源 3 的原索引、权重及真实行读取，交接给定向任务独立复核。

## 可核输入

以下路径以 `archives/customer-attraction/tools/evidence/` 为根。

| 用途 | 路径 | SHA-256 |
| --- | --- | --- |
| 5180/5198 装配 | `combined-branch-master-program/original/combined_branch_master.py` | `b29b0615415747d39a2af80f3b370b1dfd13afdf3e7ee1256576ca85e26c9dd5` |
| 三条早 B 旧投影 | `early-b-projection-and-old702-boss3/original/519adddb8a5e5058acc5/early_B_projection_certificate.json` | `b68b72b030fac2922f745adaabd34b627ae2c8ff70ec3e645f276a942f5a7959` |
| 5277 固定点 | `coupled-latest-menu-check-boss3/original/coupled_latest_exact.json` | `303291e7ec19437d226bb8d33d3e689beaf54f52103fde53a12e28f1058f806a` |
| 5277 显式 B | `coupled-b-fixed-points-boss3/original/coupled_B_branch_master.py` | `d533de28427a0690d28ec9bd2017920e01221930f5c37aa9ec294f08c0546aa2` |
| 5692 固定点 | `b-family-menu-prices-boss3/original/research_2/all_menu_prices_exact.json` | `46e52c1cec4a5cac3e6d7fe3bbe8d227cd663e428ca7f4e955182343eedb418e` |
| local-v2 原参数 | `local-reply-portfolio-joint-cuts/original/joint_local_v2_cuts.json` | `49aaf81f49aac3b544cf38ed97efdb6fa1849e1c810ff1705b7dd313052017a1` |
| nested 行 | `nested-reply-projection-program/original/nested_reply_projection.py` | `19ef4b99b8a315d0f4a4f064eece25dd240601d28729f935d5960ce17d124b96` |
| requery 行 | `early-reply-requery-program/original/early_reply_requery_cuts.py` | `b458f25360e3e35416f571b31af6dcc0418e6b1eb30894a8bde3965b03e0434a` |
| portfolio 行 | `terminal-capacity-refinement-boss3/related/terminal_portfolio_cuts.py` | `46815b59bb97fad17d2aab75ab9a698fe3a3884bc41caac4196bf8e0251d5389` |

组字典依 `(family,diag,word_i,word_j)`，保持所有 hist 块索引及三个联合态。用原同序 1905 个 weight 对每个有限行点乘。后续的全部独有行、两个新系统各自的完整精确可行性及新图的比较，由定向任务绑定证据。
