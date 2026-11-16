# 共享 Cartesian 审计证据 v3 对正规形包的定向复核

作者：Boss7。任务 `boss7-tensor-notation-repair-b77a4277b54f13f4` 替代 `boss3-sourcefix-repair-8d806bdc7cc35ff1`。

## 变动与实际阅读范围

本轮唯一输入变化是共享对象 `UM-NORMALIZED-FLAT-CARTESIAN-TENSOR-REVERSE-AMPLIFICATION-v1` 从 v2 到 v3：独立有限审计的 §2 一般完整菜单支持改为

\[
b_i+g_i a_i=\ell_i\pmod2.
\]

冻结原文同处本来就是 `ell_i`；被清洗稿多写的 `(g_i)` 不能解释为对全部状态施加逐坐标选态限制。一般标签是任意完整向量，达界见证另取 $\ell_i(g)=g_{i+1}$。例如 $t=2$ 时，两个 $g_1=0$、$g_2$ 不同的组具有不同 $\ell_1$，该见证明确不是只依赖 $g_1$ 的选择。主反例、一般证明、有限导出、所有陈述和真值状态都未变。

本次实读新任务、前一有效任务与全部 coverage/asset 记录，当前 15 个核心和 3 个共享端点的登记陈述及 pin；完整阅读以下承重正文与关系：

- `archives/unrelated-machines/state/反例/裸笛卡尔菜单乘积的精确反向放大--反例.md`，尤其 §§1–6 的全部状态、实际任务和参数区别；
- `archives/unrelated-machines/state/审查/裸Cartesian张量反向放大独立实际稀疏审计--审查.md` 及其冻结 `original/tensor_reverse_actual_audit_review.md` 的准确支持方程；
- `archives/unrelated-machines/state/定理/归一化菜单的三态资源度三正规形--定理.md` 全文；
- `archives/unrelated-machines/state/定理/完整菜单的资源度三路径归约--定理.md` 全文；
- 原资产 `path-completes-three-state-normal-form.json` 的完整条件、全部任务正反映射、证据与作用范围。

前一批已交付的独立激活、NSW、局部势、畸变和标签源比较沿原有效审读与精确 SHA 继承。本轮不声称重新审完这些无字节或登记变化的证明。四个原资产都不以新 v3 对象为端点，也没有直接引用被改附件；其端点、证据和字节均仍匹配。它们全部 `retained`，没有复制、重绑或覆盖旧资产。

## 独立复核裸族与正规形的实际数学

令 $D=2^t$。对每个组 $g$ 和任意状态向量 $\ell$，支持大小是 $D$。补组 $g+\mathbf1$ 的两个任意状态恰交一个资源，因为两个坐标方程相减唯一确定 $a_i$，再确定 $b_i$。故不交领取不可能让每组都领满，$V_t\le(D-1)/D$。

对循环标签 $\ell_i(g)=g_{i+1}$，领取所有 $a\ne\mathbf1$ 的合法资源，每组恰 $D-1$ 个。若同资源属于 $g,h$，其差 $\delta$ 满足 $\delta_{i+1}=a_i\delta_i$。至少一个 $a_i=0$，沿环迫出全部 $\delta=0$，所以全组同时不交。于是 $V_t=1-1/D$。把每组 selector 放在所选 private、只外送这 $D-1$ 件任务、其余全部原 incidence 留 private，给全任务峰 $1+1/D$。任意峰 $C<2$ 的调度中补组所选状态的两件共同资源任务不能同时外送，至少一件与 selector 同 private，给相同下界。$C\ge2$ 的分支平凡，因此 $OPT(P_t)=1+1/D$。

正规形先作真实选择树 $T$，后作全部资源的路径 $D$，两阶段作用不同：

1. 每树顶点一 selector，非根顶点有 fresh own-resource。根的两个 child-singletons、内点的 own/两 child 三态、叶的 own/原 state 两态均是完整真实任务。对正 partial 阈值或完整峰 $C<2$，根选择迫出一条原叶；off-path 可以额外激活，逆向不假定唯一活动叶。$K_g=1$ 原位不动；$K_g>1$ 旧 selector 移 root，逆向再恢复。所有原 incidence 的实际端保留，所有新增任务也逐件安排。
2. 每原资源的 $d$ 个接触组分成 $d$ 个 ports，并加 $d-1$ 个二态 helper。每 helper 有一 selector、两件不同 incidence、两台 private。峰 $C<2$ 迫使所选 singleton 外送，故 $d-1$ 个互异 ports 被占，至多一件旧任务可外送；未选 helper 额外外送只会占去更多容量。正向为原实际 export 留孔，余 ports 用路径匹配填满；逆向合回原资源，全部原任务负载不增。每 port 接一旧组和至多两 helper，度至多三。

两阶段在 $0<v\le1$ 的 partial 合同上同样双向。每 state 质量一、selector 单位重使两边 $1\le OPT\le2$，并有全 private 峰二基线；因此若一边 $OPT=2$、另一边小于二，低峰逆向矛盾。正阈值双向与非负有限最优性同样闭合 $V=0$。在给定 $C\ge2$ 时用另一侧基线，不把严格低峰的强制外送论证延伸到等号。

故把一般裸族接入已证 $N=D\circ T$，仍得到 $V(P_t^*)=1-2^{-t}$、$OPT(P_t^*)=1+2^{-t}$，同时每组至多三态、每资源跨组度至多三。这是明确既有关系的复核，不新造一般困难源。压态/降度保值不能恢复裸乘积已经丢掉的 NO 间隙；归一化、显式菜单和全部原任务合同仍承重，原组数、交互度及固定角色不保持。

本包原 `um-real-path-reduction-completes-three-state-normal-form` 边的源是路径定理，选择树步骤完整写在边内，因此它本身不依赖新 v3 对象。共享裸族只用于说明既有正规形的后果和边界。修正该附属审计记号不会改变这条边的完整目标，也不会影响本包其他三条原边。

## 资产、覆盖和后续

全部 15 核心的原 registration pin 未变；仅共享 v3 对象 pin 从 `d81f97599f437f633889dd1bbb6df2f76d3f2c3e1e9de833eaf7f0a4f02832aa` 变为 `54a098141d2c72f69ed8b861f27d4f6602bffc7f1e3fcfe768ea0340b9c7e94c`。四个原资产的 SHA 均逐一核对相同；新收据逐项标明 retained，保原数学 coverage state 与 edge IDs，只在实际比较范围中记明本次定向审读和继承范围。

没有新的未处置对象对或数学缺口。原标签资源到实际低载调度的联合 decoder、给定目标与未知目标的区别、真实畸变参数和其他前批开放义务仍按原记录保留。本次有限审计的 $t=1$ 完整优化与 $t=2,3,4$ 见证核验也保持原范围，没有拿有限输出替代上述任意 $t$ 的证明。
