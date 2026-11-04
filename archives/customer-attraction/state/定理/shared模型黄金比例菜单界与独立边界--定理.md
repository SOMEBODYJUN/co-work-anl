---
id: "shared-model/golden-ratio-menu-boundary"
kind: "theorem"
type_tag: "定理"
title: "shared模型黄金比例菜单界与独立边界"
status: "finite-certificates-paired-with-mature-facility-proofs"
truth_status: "exact-attainment; five-site-optimality-by-global-guards; no-CAG-transfer"
review_level: "full-frozen-json-and-existing-proof-comparison"
scope: "共同目录双设施、正权原子客户、独立混合精确NE和完整布局续局"
summary: "把四份shared证书接回设施模型、完整输入和既有证明；两五地点YES实例的真最优为3/2与809/500，两个菜单实例实际达到1。区分这些有限值、统一phi保证和CAG半覆盖问题。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:evidence/certificates/shared/five_site_a3_2_yes.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:evidence/certificates/shared/five_site_a809_500_yes.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:evidence/certificates/shared/on_path_chord.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:evidence/certificates/shared/tiny_phi.json"
---

# shared模型黄金比例菜单界与独立边界

这里的 shared 是 [facility-games 的共同目录双设施模型](../../../facility-games/subarchives/common-two/问题--问题.md)。本页保留在原来源位置，补足四份冻结证书的模型、真实输入、全部实际偏离和成熟证明入口。它们不采用六名顺序提供者、客户均分收益及完整历史纯 SPE 的 Q-CAG-HALF-6 模型，倍率不能移作 CAG 的支付或福利结论。

## 客户成本、完整续局与三个不同倍率

两家带标签设施同时从同一有限非空目录 $S$ 选址，允许同址。客户有正原子权重和显式覆盖关系，被覆盖时必须选择一个可达设施，各自独立随机化，并最小化包含自身完整重量的条件负载期望；设施收益是期望服务总重。

固定布局的私有负载为 $A,B$，共同客户权重为 $w_i$、选择第一设施的概率为 $p_i$。令

\[
X=A+\sum_iw_ip_i,\qquad Y=B+\sum_iw_i(1-p_i),\qquad \Delta=X-Y.
\]

客户精确 NE 等价于

\[
p_i=1\Rightarrow\Delta\le w_i,\quad
p_i=0\Rightarrow\Delta\ge-w_i,\quad
0<p_i<1\Rightarrow\Delta=w_i(2p_i-1).
\tag{NE}
\]

完整规则 $\sigma$ 在每个有序布局取一个这样的精确 NE。给定在轨 $(s,t)$ 及正收益 $(X,Y)$，该规则的实际设施倍率为

\[
\alpha(\sigma;s,t)=
\max\left\{1,\ \max_{z\ne s}\frac{L_1(\sigma(z,t))}{X},
\ \max_{z\ne t}\frac{L_2(\sigma(s,z))}{Y}\right\}.
\tag{A}
\]

一般零收益情形按 $L^{dev}\le\alpha L^{on}$ 处理，正数除零不可行。实例最优 $\alpha^*(I)$ 还要在所有在轨布局和完整规则上最小化。一个达到证书只先给 $\alpha^*(I)\le\alpha$；匹配下界需要排除所有其他布局及全部客户 NE 选择。

有限菜单 $F(s,t)\subseteq\mathrm{NE}(s,t)$ 的最低收益 $u_F(s,t)$ 与全部客户 NE 的最低收益 $m(s,t)$ 满足 $m\le u_F$，不能默认相等。P/E/T/C 固定菜单及全目录威胁的充分证明见[菜单算法](../../../facility-games/subarchives/common-two/state/算法/黄金比有限菜单与完整续局证书--算法.md)。JSON 的 guarantee=phi 是算法统一保证的标记；本实例的实际倍率须按 (A) 计算。普遍上界与新版主稿的定向复审状态见[共同目录问题入口](../../../facility-games/subarchives/common-two/问题--问题.md)，不由下面四个样本认证。

## 两份五地点证书：同一覆盖结构的两个精确端点

完整正整数权重与覆盖分别保存在 [3/2 原输入](../../../../tools/evidence/small-catalog-hardness-assets/original/examples/shared/five_site_a3_2_yes.json) 和 [809/500 原输入](../../../../tools/evidence/small-catalog-hardness-assets/original/examples/shared/five_site_a809_500_yes.json)。双方目录均为 $\{0,1,2,3,4\}$，设施数始终为2；客户数分别为11和15。两输入的覆盖结构是

\[
C_0=\{0,1\},\quad C_1=\{0,2\},\quad C_2=\{0,3\},\quad
C_3=\{0,4\}\cup J,\quad C_4=\{2,3,4,5\}\cup J,
\]

其中 $J=\{6,\ldots,10\}$ 或 $\{6,\ldots,14\}$。原权重列表全部保留在上述输入中；统一整数缩放不改变客户概率、NE 或设施收益比。

两份[3/2 完整证书](../../tools/evidence/shared-certificates/original/five_site_a3_2_yes.json)、[809/500 完整证书](../../tools/evidence/shared-certificates/original/five_site_a809_500_yes.json)各指定 **25个有序布局**上的客户 NE。25不是25个连续支持分支。在轨均为 $(0,3)$，唯一共同客户0选择较低 reach 的地点3，所以第一设施收益 $X=w_1$，第二设施收益 $Y=R_3$。

| 因子 $a$ | 在轨 $X$ | 在轨 $Y$ | 第一家去4的收益 $T=aX$ |
| --- | ---: | ---: | ---: |
| $3/2$ | $2464309$ | $3912336$ | $7392927/2$ |
| $809/500$ | $1359855527379937500000$ | $2330283365518030852941$ | $2200246243300738875000$ |

令 $R_j=w(C_j)$。原完整规则中，全部八个实际偏离的收益如下；这同时给出每个比值的分母。

| 偏离者 | 目的地顺序 | 所选续局的偏离收益 | 在轨分母 |
| --- | --- | --- | --- |
| 第一设施 | $1,2,3,4$ | $w_2,w_3,R_3/2,T$ | $X=w_1$ |
| 第二设施 | $0,1,2,4$ | $R_0/2,R_1,R_2,R_4$ | $Y=R_3$ |

单共同客户偏离严格选低 reach 端；同址偏离取全体独立半分；硬布局 $(4,3)$ 的概率向量和全部客户索引在完整证书中逐项给出。其第一坐标分别是表中的 $T$。证书无需对任意客户 NE 都稳定，而是为每个真实偏离选定这一份 NE。

第一家最大偏离比在两例中恰为 $a$。第二家最大偏离比来自目的地1，分别为

\[
\frac{5694192}{3912336}=\frac{147}{101}<\frac32,\qquad
\frac{3560071161461661000000}{2330283365518030852941}
=\frac{2209151000000}{1446023855631}<\frac{809}{500}.
\]

因此这两份完整规则的实际倍率分别是 $3/2$ 和 $809/500$。其原25布局证书与[现行构造器复核](../../../facility-games/state/计算/小目录硬度构造器与五地点样本的精确合同--计算.md)中已经验证的完整证书逐字段相同；客户 NE 和覆盖完整性不由 factor 字段自行证明。

这两个数还是各自实例的**真正最优**，依据是已成熟的[五地点全布局守卫](../../../facility-games/state/归约/共同目录三五地点固定倍率的全布局守卫--归约.md)：“五地点YES完整续局与NO全部十五类”。两原源为 SUBSET SUM 的 YES 输入 $([2],2)$、$([2,3],2)$。十四种非门控无序布局均有对任意续局成立的严格守卫；门控 $(0,3)$ 的在轨 NE 唯一，而第一家去4后在所有 NE 中的最低收益 $\mu=T$，故任何完整规则在该路径也有偏离比至少 $T/X=a$。结合上面的达到，得到 $\alpha^*=a$。

$809/500$ 是严格亚黄金比的有理数，因为

\[
(809/500)^2-809/500-1=-19/250000<0.
\]

它不是 $\phi$ 端点本身。固定 $1<a<\phi$ 的一般弱 NP 完全性由所链接归约证明承担；两份 YES JSON 只提供具体实例与完整达到，既不证明该全称归约，也不表示它们是 NO 障碍。

## on_path_chord：三人混合在轨，实际倍率为1

[完整原输入](../../../../tools/evidence/shared-certificates-runtime/original/examples/shared/on_path_chord.json)的权重为 $(20,20,20,40,39,7)$，覆盖为
$C_0=\{0,1,2,3\}$、$C_1=\{0,1,2,4\}$、$C_2=\{2,3,4,5\}$。在轨 $(0,1)$ 的私有负载为 $40,39$，三名共同客户各重20。

[冻结证书](../../tools/evidence/shared-certificates/original/on_path_chord.json)令三人各以 $39/80$ 选择第一设施，负载为 $(277/4,279/4)$。差 $\Delta=-1/2$ 恰等于每人的 $20(2p_i-1)$，所以三名客户均满足 (NE)。该布局的强交叉配额确需三名实际混合者，完整分型见[三混合必要例](../../../facility-games/state/反例/两设施强配额的三名混合必要例--反例.md)。

全部四个真实设施偏离都指定 guarded pure 续局：

| 偏离者 | 目的地 | 偏离布局 | 偏离者收益 / 在轨收益 |
| --- | ---: | --- | --- |
| 第一设施 | 1 | $(1,1)$ | $40/(277/4)=160/277$ |
| 第一设施 | 2 | $(2,1)$ | $67/(277/4)=268/277$ |
| 第二设施 | 0 | $(0,0)$ | $40/(279/4)=160/279$ |
| 第二设施 | 2 | $(0,2)$ | $66/(279/4)=88/93$ |

它们全部小于1，故 (A) 恰为1。其余布局由证书规定的全第一种子 guarded repair 补齐。原 response_cycle=(0,1,2)、9个有序对和33个菜单条目是这个固定菜单的记录，不改变实际稳定倍率，也不宣称遍历全部 NE。

## tiny_phi：纯在轨、两个同址 T 惩罚

[tiny 原输入](../../../../tools/evidence/shared-certificates-runtime/original/examples/shared/tiny.json)为八名权 $(2,3,5,7,11,13,17,19)$ 客户，覆盖依次为
$0123;124;035;246;357$；例如 $0123$ 表示客户集合 $\{0,1,2,3\}$。双方可选全部五地点。

[冻结菜单证书](../../tools/evidence/shared-certificates/original/tiny_phi.json)在轨 $(4,3)$ 无共同客户，负载 $(39,33)$。全部实际偏离为：

| 偏离者 | 目的地顺序 | 偏离者收益顺序 | 最大偏离比 |
| --- | --- | --- | --- |
| 第一设施 | $0,1,2,3$ | $17,19,22,14$ | $22/39$ |
| 第二设施 | $0,1,2,4$ | $17,19,22,16$ | $22/33=2/3$ |

末列同址惩罚是 T 成员：$(3,3)$ 的共同客户 $(2,4,6)$ 概率为 $(1,3/11,6/17)$，两负载 $(14,19)$；$(4,4)$ 的共同客户 $(3,5,7)$ 概率为 $(0,10/13,13/19)$，两负载 $(23,16)$。其余六个偏离使用证书中的 guarded pure 成员。故实际倍率也是1，且因定义要求 $\alpha\ge1$，这个实例的真正最优即为1。

其 response_cycle=(4,3)、25个有序对和49个菜单条目仅描述有限算法。菜单威胁、完整 NE 极小值以及 lazy 环输出之间的准确关系见[配套计算页](../计算/shared模型环与有限菜单精确核验--计算.md)；其中 tiny 的完整 NE 最优解只是同一稳定布局的标签反射。

## 保存与使用边界

四份冻结 JSON、全部概率及大整数均原样保留，身份见[来源 manifest](../../tools/evidence/shared-certificates/source-manifest.json)。完整输入、已验证完整证书和一般证明各承担不同义务：输入定义游戏；证书支持给定完整规则的达到；十四守卫与门控最低负载才支持两五地点实例的匹配下界。一般 $\phi$ 上界、任意环覆盖、位复杂度和外部审查均沿用各自现行对象的准确状态，本页没有重新认证这些命题，也未向 CAG 转移结论。
