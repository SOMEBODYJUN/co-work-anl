---
id: "unrelated-machines/whole-row-config-finite-difference-four-case-code-replay"
kind: "computation"
type_tag: "计算"
title: "整行CONFIG有限差分交易的四例原程序复跑"
status: "four-explicit-row-laws-replayed-no-global-localizer-enumeration"
summary: "4880B standalone程序一次真实复跑，以整数共分母比对四组全部低阶row单项式与完整pure-home边际；保下一mixed阶自然法则见证与一般d/全局PSD的范围。"
source_refs:
  - "clean:6b6d5e129a802a6d3922"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:tests/audits/unrelated_machines/diluted_shared_terminal_row_degree_trade_audit.py"
legacy_ids:
  - "UM-DILUTED-SHARED-TERMINAL-ROW-DEGREE-GAP-v1"
---

# 1. 一个B行上的两个真正有限测度

完整读原4880B程序，SHA `acee8c713dc7886dd03405031f8dd1d71c7ac67c7274a1fadc5fa715e36f8cc8`。它不import旧k2 Gram程序；本轮原CLI一次`--output`写新文件、exit0。它处理2k个原row Boolean变量：k个home Y和k个incoming R，至多一个R为1，不构造整个UM输入/M2。

对所选四组d≤k，s=d−1，low是全部|S|≤s的具体home子集，Z=Σ_(u≤s)binom(k,u)，Amax=binom(k−1,s)，L=2k²，M=1+120Lk⁴+4kZAmax、a=1/M。这里M是新行度合同参数，不能用旧rawK2的1+60Lk⁴代替。

Q行法则的质量：all-home/no-unit为1−3/(4L)；各unit/no-home和各no-unit/缺一home各1/(8Lk)；每low subset无unit为1/(4LZ)，每unit label+该subset为1/(4LkZ)，重复状态合并。raw=(1−a)Q加foreground H：all-home/no-unit质量a(1−k/L)，各unit+all-home质量a/L。raw状态可超目标T=1+s/k。

legal从(1−a)Q加a个all-home/no-unit起，以每S系数

`b_S=(-1)^(s−|S|) binom(k−|S|−1,s−|S|)`

给各unit+S加a b_S/L，给no-unit+S减ak b_S/L。它不是在raw H之外再多加一份foreground。程序核系数对每low probe有Σ_(S⊇probe)b_S=1、|b_S|≤Amax，两个法则总质量一、合并后legal全部非负，且每legal状态至多一unit、k·#unit+#homes≤k+s。Rfill的背景质量支付负系数，得到真正合法CONFIG而非有符号伪分布。

# 2. 为何这些row矩应当相等

对次数≤s的multilinear f，有限差分给f(1)=Σ_low b_S f(1_S)。在至多一unit行空间，任次数≤d的p可写p0(Y)+Σ_j R_j p_j(Y)，其中deg p_j≤s。将含unit/all-home项按上式换成低home配置，并用no-unit差补，pure-home p0项完全相消，所以raw与legal全部row degree≤d矩相同。忽略R后每个完整Y状态的边际其实全等，不只低阶相同。

程序把两法则所有Fraction分母取lcm，转整数质量；逐枚举2k变量的全部squarefree单项式|A|≤d，以Σ_(state⊇A)质量比对。Boolean重复因子由平方自由化简涵盖。另把每个完整home mask汇总核相同，并核下一个mixed单项式R_0·Y_0···Y_(d−1)在raw为a/L而legal零。

# 3. 四组实际输出

| d,k | L,M,Z,Amax | row变量 | 枚举单项式数 | 最大配置负载 | 最小配置质量 | 自然下一mixed阶raw值 |
|---|---|---:|---:|---|---|---|
| 2,2 | 8,15385,3,1 | 4 | 11 | 3/2 | 321/61540 | 1/123080 |
| 3,3 | 18,175045,7,1 | 6 | 42 | 5/3 | 162/245063 | 1/3150810 |
| 4,4 | 32,983281,15,1 | 8 | 163 | 7/4 | 128/983281 | 1/31464992 |
| 4,7 | 98,28271601,64,20 | 14 | 1471 | 10/7 | 252361/44329870368 | 1/2770616898 |

四例总1687个单项式，所有matched/pure-home equality为true、legal质量1、上述见证legal值均0。完整payload全字节等历史bdcc JSON，SHA `416d764ad20172efde6e845efab8c33f176bd45f34ba50d29acb88dfb0bf9841`；与532449旧root replay的stdout/代码/输出SHA一致，但旧重放次数不算本轮新运行。

# 4. 一般合同与下一阶量词

本轮完整读当前rawK2正文全部440行，尤其新增§13的一般固定d证明与旧§1–12保留关系；[解析审查](../审查/稀释共享终端rawK2与终端探针共同间隙双源审查--审查.md)已有共同法则、CONFIG trade、全局affine localizer支配及真实OPT证明，不以本四例重签一般证明。

自然degree-(d+1)法则的正见证说明给定自然延伸不匹配该高阶CONFIG矩；当d+1> D=max(4,d)时，不能由此断言已给degree-D restriction不存在任何其它延伸。这里也没有更高次q的localizer、跨行二事件容量或共同Boolean配置变量全次数links。全局M2/affine矩阵未被本程序枚举，d作为输入时的统一多项式不由固定d理论获得。

[证据](../../tools/evidence/um-following-actual-code-primary/README.md)保存原件/新payload/原stdout/stderr及精确命令。完整行度策略早有共同讨论，先Exact/作者读后/软件审查身份在原记录各自保留；本轮知情读取复跑，无新blind、通用求解器或hardness结论。
