---
id: "unrelated-machines/gated-normalized-fslp-four-source-cleaning"
kind: "review"
type_tag: "审查"
title: "门控归一化菜单与正支撑FSLP四源清洗"
status: "integrated-with-scoped-claims"
summary: "合并四份门控归一化菜单来源的精确对象、独立重构、作者证明与Exact攻击：正支撑FSLP给确定性福利舍入与高质量组计数；完整门控普通UM矩阵满足OPT=2-beta*；并修正robust源中高质量组阈值与低质量比例的互补量词。结论只适用于显式归一化菜单和门控矩阵，不外推一般不相关机或六人SPE。"
legacy_ids:
  - "3e856a22c23d93795e61"
  - "50fb6c57837e0e00329b"
  - "9a15b8d9af2b4192ccea"
  - "32384b81f59dd655a55b"
source_refs:
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/notes/unrelated_machines/gated_menu_fslp_author_proof_v1.md#1-8"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/notes/unrelated_machines/gated_menu_fslp_exact_read_attack.md#1-5"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/notes/unrelated_machines/gated_menu_fslp_exact_v1.md#E1-E5"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/notes/unrelated_machines/gated_menu_fslp_independent_reconstruction.md#1-7"
---

# 门控归一化菜单与正支撑FSLP四源清洗

## 来源身份和比较范围

本对象完整读取并比较四个冻结版本。它们是同一研究簇中的不同证据层，而不是四个相互独立的定理。

|稳定来源ID|来源路径|在本对象中的作用|
|---|---|---|
|9a15b8d9af2b4192ccea|gated_menu_fslp_exact_v1.md|E1--E5 的冻结精确陈述|
|32384b81f59dd655a55b|gated_menu_fslp_independent_reconstruction.md|独立重构|
|3e856a22c23d93795e61|gated_menu_fslp_author_proof_v1.md|作者证明|
|50fb6c57837e0e00329b|gated_menu_fslp_exact_read_attack.md|先读 Exact 的攻击/核对|

四源均有 legacy-cleanup 提交 `68fad804ec5946cb296f77dc5b336308a66abf12` 与 main 提交 `aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c` 的冻结定位。3e 的作者证明晚于 9a 的 Exact；50 明确先读独立重构再读 Exact。四源未提供外部同行评审或全球新颖性认证；作者证明、独立重构和攻击报告不能互称外审。

## 一、显式归一化菜单与正支撑 FSLP

输入有有限非空组集 (G)，(n=|G|ge1)，有限资源集 (U)。每组 (g) 有非空有限 indexed state 集 (A_g)。state (s) 给出显式二进制有理数 (p_{g,s,u}ge0)，并满足
\[
\sum_{u\in U}p_{g,s,u}=1.
\]
允许显式零系数、未使用资源、重复 indexed states；未列出的系数按零用于效用，但不凭空生成物理作业。显式 incidence 总数记为 (I)，state 总数为 (S=\sum_g|A_g|)。

对 bundle (B\subseteq U)，原菜单价值为
\[
v_g(B)=\max_{s\in A_g}\sum_{u\in B\cap U_{g,s}}p_{g,s,u}.
\]
allocation 要求各 (B_g) 两两不交，资源可闲置。正支撑
\[
P_{g,s}=\{u:p_{g,s,u}>0\}
\]
只记录真正消耗资源容量的 incidence；零系数不进入列约束。

给定显式有理 \(\lambda_{g,s}\) 的 unit-FSLP 是
\[
\lambda_{g,s}\ge0,\qquad
\sum_s\lambda_{g,s}=1\ (g\in G),\qquad
\sum_{g,s:u\in P_{g,s}}\lambda_{g,s}\le1\ (u\in U).
\tag{FSLP}
\]
这是有限 0/1 矩阵的有理 LP，按正支撑计数而不是用 (p\lambda) 加权。把零 incidence 误计入会破坏后续 (z_u(t)\le1)；把 weighted-load LP 当作 FSLP 也不能直接代入本对象。

## 二、福利舍入和高质量组计数

独立按 \(\lambda_{g,s}\) 为每组抽 state。固定资源 (u) 和阈值 (t>0)，令
\[
a_g(t)=\Pr[p_{g,s_g,u}\ge t],\qquad z_u(t)=\sum_ga_g(t).
\]
正支撑约束给 (0\le z_u(t)\le1)。组间独立，因此
\[
\Pr[\max_gp_{g,s_g,u}\ge t]
=1-\prod_g(1-a_g(t))
\ge1-e^{-z_u(t)}
\ge(1-1/e)z_u(t).
\]
对所有有限正 level 做尾和/积分，得到
\[
\mathbb E[\sum_u\max_gp_{g,s_g,u}]\ge(1-1/e)n.
\tag{1}
\]
每个资源交给其最高系数的固定编号赢家，故抽态已经产生两两不交的资源束；同一组的资源总质量不超过1。

条件期望去随机化不需要计算 (e)。在已固定一部分组的前缀下，对资源 (u) 列出所有不同正系数
\[
0=t_{u,0}<t_{u,1}<\cdots<t_{u,L_u}.
\]
若 (F_{g,u}(t)) 是当前分布下 (p_{g,s_g,u}<t) 的有理概率，则
\[
\mathbb E[\max_gp_{g,s_g,u}\mid\text{prefix}]
=\sum_{\ell=1}^{L_u}(t_{u,\ell}-t_{u,\ell-1})
  (1-\prod_gF_{g,u}(t_{u,\ell})).
\tag{2}
\]
固定下一组时，父期望是正概率候选子期望的加权平均，选最大候选即可保证不下降。完成全部组后，资源赢家给出有理、确定、总位多项式的 allocation；再在每组原菜单中重选 attaining state，只会增加 (v_g(B_g))。候选个数、level 个数和乘法次数均由显式 (S,I,n) 控制，分母位长只作加法式增长；没有对最小正系数或最小 \(\lambda\) 做迭代。

由于 (1-1/e>5/8)，输出质量 (r_g=v_g(B_g)) 满足
\[
\sum_gr_g>\frac58n.
\tag{3}
\]
更一般地，对有理 (0\le\delta<5/8)，
\[
|\{g:r_g\ge\delta\}|>
\frac{(5/8)-\delta}{1-\delta}\,n.
\tag{4}
\]
严格阈值 (>\delta) 版本必须同步改变其余组的弱不等式。特别 \(\delta=3/8\) 时高质量组数 (>2n/5)，从而至少有 \(\lceil3n/8\rceil\) 个组达到 (3/8)。严格号可由 (e>1+1+1/2+1/6=8/3) 自足推出，不依赖整除。该推导只保证部分高质量组数，不是全组 max-min，也不等价于一般 Santa Claus 或一般 (R\|C_{\max})。

## 三、完整门控普通 UM 矩阵和精确值桥

构造 (P_{\mathrm{gate}})：机器为根 (R)、每组 gate (X_g)、每个 indexed state 的 private 机 (M_{g,s})、每个资源机 (Q_u)。作业为根 pin (J_0)（仅 (R) 用时1）；connector (C_g)（(R) 用时 (1/n)，(X_g) 用时1）；selector (T_g)（(X_g) 与全部本组 (M_{g,s}) 用时1）；每个显式 incidence 作业 (I_{g,s,u})（(M_{g,s}) 用时 (p_{g,s,u})，(Q_u) 用时1）。未选 state、零 incidence 和未使用资源的显式身份全部保留，其他端为不可用。

定义 balanced value
\[
\beta^*=\max\left(\{0\}\cup\left\{\min\left(\frac{|H|}{n},\min_{g\in H}\sum_{u\in B_g\cap U_{g,s_g}}p_{g,s_g,u}\right):\begin{array}{l}\emptyset\ne H\subseteq G,\\B_g\text{ 两两不交},\ s_g\in A_g\end{array}\right\}\right).
\tag{5}
\]
这是有限集合上的定义，不提供免费 oracle。

**前向构造。** 给 (\beta>0) 的 (H,B_g,s_g) 见证，选中 connector 去 gate，其余留根；选中 selector 去对应 private，其余 selector 去 gate；选中 state 对 (B_g) 的正 incidence 导出资源机，其余 incidence 留各自 private。根负载为 (2-|H|/n\le2-\beta)，选中 private 负载为 (2-v_g(B_g)\le2-\beta)，资源机至多一件 unit incidence，其他 private 和 gate 负载至多1。\(\beta=0\) 时用 connector 全留根、selector 去 gate、incidence 留 private 的峰值2基线。

**反向解码。** 对任意完整调度峰值 (C<2)，令 (H=\{g:C_g\text{ 在 }X_g\}\)。根负载精确为 (2-|H|/n)，故 (|H|/n\ge2-C>0)。若 (g\in H)，则 (T_g) 不可能也留在 (X_g)，否则该机负载至少2；它必须去某个 (M_{g,s_g})。由该 private 的负载 \(\le C\)，被导出的正 incidence 质量至少 (2-C)。每个 (Q_u) 在 (C<2) 时至多接一件 unit incidence，因此这些 (B_g) 全局不交。于是 \(\beta^*\ge2-C\)。

两向合成
\[
\operatorname{OPT}(P_{\mathrm{gate}})=2-\beta^*.
\tag{6}
\]
根 pin 保证 \(\operatorname{OPT}\ge1\)。该恒等式依赖完整门控矩阵和所有作业身份，不能删掉未选 state 作业、把 flat 矩阵 selector 强制激活的语义替换为 gate、或把任意隐式菜单当本对象。

把 (4) 的 \(3/8\) 高质量组带入 (5)，得到 FSLP 可行时完整调度峰值不超过 (13/8)；结合根 pin 可写成该显式门控子类的 (13/8) 比率上界。独立重构还给出 (b_0=1-e^{-1/2}) 的计数阈值及相应 (1+e^{-1/2}) 峰值口径；它与作者证明的保守 (13/8) 口径应分开记录，不能混称为两个普适算法。

## 四、robust 参数互补的正确量词

若 robust NO 写成
\[
h_{\ge\delta}=|\{g:r_g\ge\delta\}|<\gamma_{hi}n,
\]
互补的是
\[
|\{g:r_g<\delta\}|>(1-\gamma_{hi})n,
\]
而不是“至少 \(\gamma_{hi}n\) 个低质量组”。高端使用 (>\delta) 时，低端应改为 \(\le\delta)；严格/非严格边界不能自动互换。旧稿中把 \(\gamma_{bad}\) 与 \(\gamma_{hi}\) 当成同一个比例，错误发生在参数比较，不在各自不等式。

在本对象的 FSLP-feasible、显式 normalized 域内，福利地板 (4) 排除
\[
\gamma_{hi}\le\frac{(5/8)-\delta}{1-\delta},\qquad0\le\delta<5/8.
\tag{7}
\]
这是精确 promise 判别范围：YES 为存在全组质量1 allocation，NO 为所有 allocation 的高质量组数严格少于 \(\gamma_{hi}n\)。FSLP 可行判 YES、不可行判 NO；promise 外不作结论。将该合同编译到 (P_{\mathrm{gate}}) 可得到特定的 OPT=1 与 OPT>13/8 gap，但这不是一般 UM 的 gap 或 hardness 证明。若源改变归一化、使 state 菜单隐式指数、失去正支撑容量、只控制整束而非 all-allocation 高质量数，均不在 (7) 范围。

## 五、独有内容、审查状态和接续

- 9a 的独有承重内容是 E1--E5 的冻结对象身份、零/重复/unused 边界、P_gate 四层结构和 robust promise 的精确量词。
- 323 的独有承重内容是独立尾积分、条件期望去随机化、完整任务逐机负载与 (1+e^{-1/2}) 阈值口径。
- 3e 的独有承重内容是值反向解码的细节、位长界、LP promise 形式化和旧 \(\gamma\) 互补错误定位；作者证明仍非外审。
- 50 的独有承重内容是对正式 connector 资格、严格号、(n=1)、显式零、重复 state、大分母和“等价”措辞的逐项攻击；它把“E1--E5 无 fatal”限定在明示范围内。

与已有《部分激活菜单福利地板》和《归一化菜单福利与配置证书双源审查》的关系：前者处理允许总活跃质量 (q\le n) 的部分 FSLP 覆盖，后者还整理完整 machine CONFIG(1)、树形 normal form 和受限矩路径；本对象仅补入这四个具体冻结源的来源身份、P_gate 精确值桥与独立攻击层，不把不同对象合成一个菜单或配置模型。参见：
- [部分激活菜单福利地板](../定理/部分激活菜单福利地板--定理.md)
- [归一化菜单福利与配置证书双源审查](./归一化菜单福利与配置证书双源审查--审查.md)

仍未完成的义务：

1. 尚无把上述有限显式 FSLP/P_gate 结构编译到一般 (R\|C_{\max}) 近似困难性或一般 UM 算法的证明。
2. 尚无端到端生产实现的有理 LP、条件期望和全部 P_gate 作业回算；源中提出的 Fraction/枚举核验只能作为后续证据，不能冒充已完成通用实现。
3. flat、gated、多层私有树语义的跨模型映射仍需单独给出，不能凭对象名复用。
4. 该对象与 Q-CAG-HALF-6（六个提供者、完整历史纯 SPE）无直接量词联系；第三阶段若建图，应标记为独立 UM 工具/边界而非主命题证明。

处置：四源均有独有数学去向并合并为本自足审查对象；没有可安全删除的独立论证。50 对 9a 的攻击未发现明示范围内致命矛盾，但保留“未完成外审/实现”的限制。
