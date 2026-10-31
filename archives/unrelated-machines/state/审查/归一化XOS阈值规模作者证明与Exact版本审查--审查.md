---
id: "unrelated-machines/normalized-xos-threshold-menu-size-v2-source-review"
kind: "review"
type_tag: "审查"
title: "归一化 XOS 阈值规模作者证明与 Exact 版本审查"
status: "integrated-version-review"
truth_status: "reconciled-with-existing-obstruction"
review_level: "full-exact-and-author-proof-read"
summary: "逐源核对 v2 Exact 与作者 Proof；确认同宇宙归一化 clause 的支持下界、覆盖等价、两个锐端点和固定 eta 输出界，补足版本边界，不扩展为一般 Santa/UM hardness。"
source_refs:
  - "clean:a4946858cc8b88c116a5"
  - "clean:6624c132790212150bac"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/normalized_xos_menu_threshold_size_exact_v2.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/normalized_xos_menu_threshold_size_proof_v2.md"
evidence_manifest: "../../tools/evidence/normalized-xos-threshold-20261031/manifest.json"
---

# 模型和范围

两源均完整读取。固定有理 (0<eta<1)、(tge1)、同一资源宇宙 (|U|=2t)，(d=lflooreta tfloor)，(k=max(1,lceil d/etaceil))。菜单由有限个 indexed、非负、有理、逐 clause 总质量恰为一的加性 clause 组成，允许零系数与重复 indexed clause。要求所有 (|T|=t) 满足 (f(T)=1)，所有 (|B|le d) 满足 (f(B)leeta)。

## 作者证明与 Exact 的共同结论

任一 clause 的正支撑大小至少 (k)：若支撑不超过 (d)，自身 tiny 值已为一；否则取最大 (d) 个正项，其质量至少 (d/h)，由 tiny 量词得 (hgelceil d/etaceil)。从每个支撑任选 k-subset 并均匀化，保持所有 unit/tiny 合同；反向地，任何“每个 t-subset 含某个 k-subset”的 family 用均匀 clause 实现同一合同。因此

[
K_{min}=Theta(2t,t,k),
]

其中 (Theta) 的方向是每个 t 集包含一个指定 k 集，不是相反的 covering-design 约定。固定 k 集被 (inom{2t-k}{t-k}) 个 t 集包含，故有计数下界
[
Kge inom{2t}{t}/inom{2t-k}{t-k}.
]

Exact v2 的独有范围是精确组合等价、(d=0) 的 (K_{min}=t+1)、(eta t) 正整数时 (K_{min}=inom{2t}{t}) 以及固定 (eta) 的 (4^t/mathrm{poly}(t)) 输出界。作者 Proof v2 展开了支持大于 t 的 clause 可删除、原权重不需 uniform、显式可行菜单构造和“等价不是求解覆盖族的算法”边界。

## 版本与限制

两源与现有《归一化 XOS 菜单阈值规模下界--障碍》是同一数学对象，故本页是版本审查而非新定理。证明没有软件、枚举、外审或一般 hardness 证据。输出障碍按显式资源参数比较，不能写成 (2^{Omega(	ext{源总位长})})；(eta) 随输入变化时，固定 (eta) 的多项式指数常数不保持。

范围只排除同一资源宇宙、逐玩家、非负 norm-1、保全部 unit/tiny 子集的显式菜单 shortcut。辅助资源/玩家、全局耦合、只保可达集合、unit 有损、未归一化 clause 或另一种已证明的隐式表示均未被排除。该对象不推出一般 Santa Claus/UM NP-hardness、近二 gap、六人 SPE 或 Q-CAG-HALF。

# 处置

Exact 与 Proof 的原字节、SHA 和角色见 evidence manifest；数学内容并入现有障碍对象，新增的双向覆盖等价和版本边界在本页保留。第三阶段可将本页作为“来源审查→现行障碍”的 provenance 边，但不能把作者 Proof 与 Exact 误计为两个不同 theorem。
