---
id: customer-attraction/off-support-hub-repairs-static-query-average-gap
kind: counterexample
type_tag: 反例
title: 支持外枢轴修复与静态查询平均的两人分离族
status: proved-full-history-unit-customer-family;only-specific-query-average-bridge-refuted
summary: 偶数个周边主题的子集设计使静态三人对称Nash查询的平均真实根偏离低于其共同收益，但支持外枢轴给更高真实根收益。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-75bfd8f0f91740408bf08f0c9f5e2aa1/iid_extra_slot/child/hub_family.md
---

# 支持外枢轴修复与静态查询平均的两人分离族

这里真实顺序游戏始终**两名**单位提供者；n是周边主题数，不是提供者人数。客户单位、共同有限目录为H及P₁…P_n，全部历史/重复和平局保留。反驳的是从一个给定静态对称Nash查询q直接平均真实偏离支付其λ的强桥；不由该例反驳真实根extra-slot、全路径聚合或half。

## 一般设计及完整历史比较

取n≥2，1≤s<n，每个s元周边标签子集各有a≥1名核心客户，喜欢H和该子集；每P_i另有整数P≥0名私有客户。记
\[
M=a\binom ns,\ d=a\binom{n-1}{s-1},\ e=a\binom{n-2}{s-2},\ t=s/n,
\]
s1时e0。g₃(z)=1−z+z²/3是面对两个独立查询者时 \(\mathbb E[1/(1+\mathrm{Bin}(2,z))]\)。取q_H0、q_Pi1/n，G=g₃(1/n)，静态三人对称混合收益为
\[
\alpha_H=Mg_3(t),\quad\alpha_{P_i}=dg_3(t)+PG=\lambda.
\]
目录恰这n+1题，故q为对称混合Nash当且仅当 \(P\ge(M-d)g_3(t)/G\)。这里λ指该指定q的共同支持收益，不偷加跨任意静态均衡的唯一值。

顺序完整σ规定根H、H后P₁、任意P_i后H。末位全部比较：

| 首动作 | 末位查H | 末位查同P_i | 末位查其它P_j |
|---|---:|---:|---:|
| H | M/2 | P+d/2（任意i） | 同前 |
| P_i | M−d/2 | (d+P)/2 | P+d−e/2 |

根H获L_H=M−d/2；根偏任意P_i得D=P+d/2。由表直接得该指定完整策略为SPE的准确参数区间
\[
(M-d)/2\le P\le U_B=M-3d/2+e/2.
\]
下界保证H后P最优；上界保证P_i后H优于其它P_j，也保证优于重复P_i，因为U_B≤2(M−d)；还因U_B≤M−d保证根H≥D。等号仍按所给合法平局执行。

查询q平均真实偏离恰D，D<λ等价
\[
P<\frac{d[g_3(t)-1/2]}{1-G}.
\]
所以与上述Nash和SPE区间联合，得到可判定的整数设计域，不把任意参数自动称SPE。

## 偶数周边主题的无限单位族

取偶n≥8、s=n/2、a3，C=binom(n,n/2)、M3C、P=C=M/3、d=M/2、e=M(n−2)/(4(n−1))。所有重数确为整数（源子集设计产生e，不另给任意有理客户）。总单位客户(n+3)C。
\[
\alpha_H=D=7M/12,\quad\lambda=7M/24+MG/3,
\quad\lambda-D=\frac{M(3n^2-24n+8)}{72n^2}>0.
\]
n≥8时分子3n(n−8)+8>0，所以q是静态Nash且H是严格支持外较劣静态回应。

H后P收益7M/12>M/2。P_i后H收益3M/4，别P_j收益5M/6−e/2，两者差M(n−4)/(24(n−1))>0；重复P_i仅5M/12。因此每个P_i后的唯一末回复H，根H严格优于偏P_i的7M/12。这覆盖1+(n+1)个全部决策历史，给完整两人SPE。

然而 \(\lambda\le7M/24+M/3=5M/8<3M/4=u_1\)。所以给定q平均失败，同时支持外H真正修复当前收益；不能把静态未用题的α_H<λ当真实分支无用。一般更强extra-slot接口后来在其它人数已被银行族否定，见[准确版本资源](../资源/DIRECT与前缀门槛的历史量词和后来反驳--资源.md)；该后续反例不倒归本hub族。

## 单个更小实例与证据范围

n8/s4/a1/P24给M70,d35,e15、262名不同单位客户。
\[
\alpha_H=245/6,\quad\lambda=997/24,\quad D=83/2,\quad\lambda-D=1/24,
\quad u_1=105/2.
\]
P_i后H得105/2、别P_j得103/2；H后P得83/2，故完整σ同样成立。原稿另写D=θ₂。按[末位最坏背景值](../引理/末位最坏背景值与目录计数界--引理.md)的通常定义，θ₂=min单个阻挡主题 max查询收益：背景H时最大查询为83/2，背景任P_i时最大为105/2，故θ₂=83/2准确。它**不是全完整SPE根最小可达门槛M₂**。本输入H后任何最佳回复都是周边题，根选H必得105/2；因此真正M₂也为105/2（所给σ达到）。原θ₂等式正确，只须保两种门槛不混。

原check_hub.py及check_family.py在来源仅记录旧有限核验，本文未新读/执行它们；一般族靠上面所有历史代数证明，不由有限参数采样推出。与[三人八客户同分布额外查询例](同分布额外查询高于平均强制收益--反例.md)的区别是：该例用任意给定p的独立额外查询K超过p·D，这里q还是静态三人对称Nash，且真实玩家仅两名、客户定义完全不同。原内部读序/后续审查在相应资源保，未新增外审或新颖性认证。

原件、逐项指纹、真实读取范围和本批运行事件见[本批证据](../../../../tools/evidence/cag-maxroot-terminal-share-and-direction-primary/README.md)。
