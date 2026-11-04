---
id: unrelated-machines/explicit-uniform-bundle-robust-welfare-boundary
kind: lemma
type_tag: 引理
title: 显式均匀束robust源的福利排除域
status: proved-by-reuse-of-welfare-rounding
source_refs:
  - ../审查/三维匹配与高维配额部分障碍双源审查--审查.md
  - ../审查/近完美归一化robust源四源审查--审查.md
---

本页把KDM全层需求树的条件源合同接到已经自足证明的福利LP界，保留直接四层菜单源后来被排除的参数域。它不是一般UM困难性，也不要求重新证明成熟的福利舍入。

有 \(q\ge1\) 个变量；每变量有显式非空 indexed 标签菜单，每标签对应原资源的一个 \(K\)-元素集 \(S_e\)，\(K\ge1\)。不同变量可复用同一原资源，但实际领取的资源集必须全局不交；允许空领取及闲置资源。没有额外标签相容、coherence或共享内部任务约束。定义
\[
 r_x(B_x)=\max_{e\text{ 属于 }x}|B_x\cap S_e|/K\in[0,1].
\]
完整YES指每变量可选一个完整标签束，且这些束两两不交。robust NO指：任意至少 \(\gamma q\) 个变量、任意逐变量标签及其大小至少 \(\delta K\) 的子束，都不能全局不交。

若 \(0<\gamma\le\delta\le3/8\)，上述YES/NO promise有确定性总位多项式判别器。更广地，YES只要求至少 \((1-\eta)q\) 个变量获质量1，且NO要求每个allocation的高组数严格小于 \(\gamma q\)，在
\[
 0\le\eta<1,\quad 0\le\delta<1,\quad0<\gamma\le1,
 \qquad \frac58(1-\eta)\ge\gamma+(1-\gamma)\delta
\]
时同样可判。高组可分别按 \(r_x\ge\delta\) 或 \(r_x>\delta\) 定义，不能混用两版NO；统一子域包含 \(0<\gamma\le\delta\le3/8,\ 0\le\eta\le1/40\)，包括三重等号角点。

证明将每标签在 \(S_e\) 上赋权 \(1/K\)，恰为显式norm1菜单。取变量 \(z_{xe}\ge0\)、仅正incidence的 \(y_{xeu}\ge0\)，约束
\[
 \sum_ez_{xe}=1,\qquad y_{xeu}\le z_{xe},\qquad
 \sum_{x,e}y_{xeu}\le1,
 \qquad L=\max\sum_{x,e,u}y_{xeu}/K.
\]
该LP总可行，\(L\le q\)，任意实际allocation都可嵌入；完整YES给 \(L=q\)。[成熟福利证明](../审查/近完美归一化robust源四源审查--审查.md)按组选态、条件提议、逐资源最高系数赢家及有理条件期望，给 \(L>0\) 时一个实际不交allocation满足 \(W=\sum_xr_x>5L/8\)。最终重新取attaining标签只会增加福利。

完整YES时令 \(H=\#\{x:r_x\ge3/8\}\)，则
\[
 \frac58q<W\le H+(q-H)\frac38
 \quad\Longrightarrow\quad H>\frac25q.
\]
这些变量的实际已领子束质量至少 \(\delta\)，数量严格超过 \(\gamma q\)，故违反所列robust NO。于是精确LP按 \(L=q\) 判YES、否则判NO即足够，无需实际运行福利finder。近完美情形按 \(L\ge(1-\eta)q\) 判；NO的福利严格小于 \([\gamma+(1-\gamma)\delta]q\)，与 \(W>5L/8\) 矛盾。这里的严格号允许参数等号，组数和束数均不需额外整除。

需求树的根→变量→标签→资源编译在 \(\gamma\le\delta\) 下确有条件结论：YES为 \(b^*=1\)，NO为 \(b^*<\delta\)，再于准确token桥域翻译为OPT=2−b*。但上面的直接显式均匀束promise已可判，不能仅把它称为“robust源待构造”并假定它NP难；若NP完全语言确定性Karp归约到此完整promise，则P=NP。任意矩阵的共享内部容量、隐式菜单、不归一化或跨层一致性不在此排除域，须另给真实YES、全部低调度decoder及规模证明。空菜单先判非完整YES；不能把它送入非空菜单定理。
