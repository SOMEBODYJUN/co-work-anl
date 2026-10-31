---
id: "unrelated-machines/diluted-shared-terminal-k2-local-gram-original-code-replay"
kind: "computation"
type_tag: "计算"
title: "共享终端k2局部Gram的原程序重建"
status: "single-local-frame-original-CLI-replayed-not-full-global-M2"
summary: "原6727B代码一次复跑，121加权实际状态、10个B配置first/pair和50维slack加权Gram精确LDL；保selector regime、五类质量、均值间隙及旧双路径重放身份。"
source_refs:
  - "clean:b16528ece8c91d3df791"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:tests/audits/unrelated_machines/diluted_shared_terminal_raw_k2_finite_audit.py"
legacy_ids:
  - "UM-DILUTED-SHARED-TERMINAL-RAW-K2-GAP-v1"
---

# 1. 一个局部frame，不展开全部M个组件

原程序6727B、SHA `4da7af092c02ff53ff41b041d78099f23f23fea28f6021222f140e48911f362c`完整读，本轮`--output`指向新文件一次exit0，未改源。固定k2、L=2k²=8、M=1+60Lk⁴=7681、a=1/M、T=3/2；它不物化M个组件，而枚举一个组件和selector选中该组件的regime。

原机器类型为U、8台B和2台Z；组件内f_j有U小端1/k及各B大端1；e_(b,j)有B小端1/k及各Z大端1。selector的全局h身份在此用A∈{0,1}表示。50维feature是constant、A、kL=16个f nonhome heads、Lk²=32个e nonhome heads；home端由one-hot complement消去。

H以质量a均匀选[k]→[L] injection，所有f去不同B，全部e留home，A1；Q以质量1−a分三类：1/2全home；1/4均匀选f/B并把该B全部e按bijection送Z；1/4均匀单e export，A0。H状态56、Qzero1、Qunit32、Qnoise32，合121。全部状态权精确和一；它们是实际赋值，H允许B负载2，不能称实际T调度。

# 2. 同一行的10个合法配置

固定B0，R_j是其incoming f indicator、Y_ℓ为e home indicator。置p=ak/L、b0=c0=(1−a)/(4L)。程序从上述121态直接累加全部四个row变量的first和完整4×4 pair，另生成以下五类合法配置：

| 类 | 总质量 | k2逐项数 |
|---|---|---:|
| unit+一个home，labels独立均匀 | kp=1/15362 | 4 |
| unit无home | b0−(k−1)p=959/30724 | 2 |
| 无unit无home | p=1/30724 | 1 |
| 无unit恰缺一个home | c0−kp=479/15362 | 2 |
| 无unit全部home | 1−b0−c0+(k−2)p=7201/7681 | 1 |

逐项核非负、质量一、负载≤3/2，first/pair与真实态法则逐Fraction完全相同。它没有要求row triple匹配；H给R_jY_1Y_2正质量而合法T配置给零，这正是raw first/pair合同的边界。

# 3. 被精确分解的矩阵是什么

令φ为上述50维feature，g=T−load_(B0)。代码构造`G=Σ_states weight*g*φφᵀ`，是**affine负载localizer**的单组件/selector-regime矩阵，不是全输入以二次单项式索引的M2。H的g可以负，正定性不是逐态g≥0的结果。

程序用Fraction执行完整LDL，50个pivot全部严格正，再对每个矩阵条目重放`L diag(pivots) Lᵀ`核等。输出完整50 pivot，Gram紧凑JSON指纹`4ad7e5c7dd98316b7ea62897ccb9e07bf27e88a9a429c63a44770419ff7d985c`。按H/Q分别归一化的平均gap为1/4和33/64；不是全部条件q的最小特征值。

全部payload SHA为`0b2b750dbce6a49f2b027731b868eb2f709f93b1e573d3948edf07bf0eb392e6`，本轮实际输出与冻结bf7d文件**全字节同**；stdout也报告此输出SHA。矩阵本身未单独输出，但121态生成/逐项构造/精确重放代码完整可复核，不假称额外保存了未导出的2500项文件。

# 4. 复跑身份和一般证明去向

[证据包](../../tools/evidence/um-following-actual-code-primary/README.md)保本轮一次CLI命令、cwd、原码、stdout/stderr、完整payload及哈希。历史71c23是两条旧路径的同码同输出重放，已全文比较；那两次仍是历史，不与本轮相加成新独立票，历史独立数学审者未读/跑代码的范围也不改变。

本轮完整读33439B当前正文全部§1–12和新§13。一般rawK2结论另依共同全局有限法则、跨组件条件方差分解与维数无关支配；本代码不生成全局M2或所有跨组件affine contexts，也不验证任意k。k2本身真实OPT/T=1，不能把此有限表当趋二数值证据。[现有解析审查](../审查/稀释共享终端rawK2与终端探针共同间隙双源审查--审查.md)与[历史代码身份](../审查/稀释终端独立重放与探针缺口有限审计--审查.md)保一般量词及先验；本页新增原程序资源与一次真实复跑，不改raw系统为joint-CONFIG-M2、不升级到hardness或一般算法失败。
