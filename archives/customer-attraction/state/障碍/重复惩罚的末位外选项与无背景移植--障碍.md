---
id: "customer-attraction/repeated-punisher-last-outside-option-and-no-background-transplant"
kind: "obstruction"
type_tag: "障碍"
title: "重复惩罚的末位外选项与无背景移植"
status: "proved-specific-obstructions; shared-omission-path-not-yet-SPE"
summary: "完整保重复H末位D严格偏离、去PB背景两个充分IC冲突、Beta重复损失及共享遗漏全k目录与δ≥7/成本≥21；不升级一般不可能性或half反例。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-3bc48d936f044f12b0fa743482ff5eb0/FAILED_ROUTES.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-3bc48d936f044f12b0fa743482ff5eb0/FAILED_ROUTES.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-3bc48d936f044f12b0fa743482ff5eb0/credible/target_attack_checkpoint.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-3bc48d936f044f12b0fa743482ff5eb0/credible/target_attack_checkpoint.md"
---

# 重复惩罚的末位外选项与无背景移植

## 两个精确移植障碍，不是一般不可能性

共同目录单位客户、单位提供者、每个有序历史纯SPE，保空/重复/平局。下面只排指定经济机制的直接版本。异质修复会将合法路径的旧差额g=OPT−2W减少2R+D；这些尝试尚未给g>2R+D的输入，不构成half反例。先定义各自目录和后继，不把一种toy中的主题默认加入另一完整目录。

## 重复同一punisher的真实末位外选项

碰撞自由目标C₁,…,C_k,D中，C_i两两不交、各p，D独立、大小t，遗漏Q_i各q且在actual并集外。若合法A_i=C_i∪Q_i，actual末位D成为BR至少要求p/2+q≤t。只在C_i上共享一次而不覆盖Q_i的惩罚不能把偏离者压到p，除非q≤p/2；这是这套构造渐近3/2天花板的来源，非所有SPE的比值上界。

改用H_i=A_i∪E_i，E_i⊆D且|E_i|=b，actual末位BR更要求
\[
p/2+q+b\le t.\tag{L}
\]
假设偏离A_i后有r≥1人重复H_i，末位做最后一次，且其他该枝动作避开A_i及D\E_i。末位留H_i得
\[
(p+q)/(r+1)+b/r,
\]
改D得(t−b)+b/r。q>0且r≥1时
\[
(p+q)/(r+1)\le(p+q)/2<p/2+q\le t-b,
\]
故规定的最后H_i严格不是BR。所有k/r均成立，不是有限扫描。修复方向必须用其他真实枝动作先覆盖D\E_i，或用不同punisher；它们仍须付actual末位外选项和完整离轨IC，不能任意分配continuation payoffs。

## 把原PB背景直接删去的两个充分IC冲突

原PB的regular动作每段选至多k≥2个real块并用dummy块补齐。原两类充分IC写为
\[
g(r)>2f(1)-f(2),\qquad
k f(k)>f(t)+(k-1)g(1).
\]
只删背景、real/dummy块大小a,b时f(c)=a/c、g(c)=b/c。因此Greedy迫b>(3/2)ar，Fill/Copy迫a>a/t+(k−1)b，进而b<a/(k−1)。对r≥1,k≥2不相容；t1第二式已不可能。仅排这套充分IC的literal无背景移植，不排其他构造或证明。

[Beta静态克隆](../引理/Beta克隆的单次增益与复用上尾债务--引理.md)亦不能白保旧Copy：其单位有限有理实现中，原客户背景M≥1的潜在包含率P密度M(1−p)^(M−1)，相关fresh标签条件独立。k个fresh标签按对称分享每人精确份额1/(M+k)；k人重复一个exact标签时，含该标签概率E P=1/(M+1)，于是每人只1/[k(M+1)]，大M约少k倍。所有有理型共同整数清分母后是确定单位客户，非真实博弈临时随机客户。沿拟定路径用不同fresh标签避开损失，仍须补全部重复标签历史的真SPE。另原PB大背景曲线f(c),g(c)=q/M+O(M⁻²)，r名实际总利润与r动作fresh-clone覆盖共同主项rdkq/M；局部前两人安全值分离本身不提供宏观正g，更不提供g>2R+D。这里是源解析尺度边界，不新验原PB程序或新全族反例。

[原PB实际前缀障碍](PB大背景的最后单例偏离--障碍.md)另在原参数证明最后D-singleton真获利，排特定背景在轨实现。这与这里去背景的互斥充分IC是两条不同障碍；合法背景子SPE本身仍有效。

## 合法共享遗漏路径：明确给目录，但威胁未构造

对每个k≥4，m=k+1；互不交X_i大小2、Q_i大小3及E₀,E₁各4。A_i=X_i∪Q_i，D=E₀⊔E₁。**完整共同目录恰为**
\[
C_i=X_i,\quad H_i^e=A_i\cup E_e\ (e=0,1),\quad
P_{ij}=A_i\cup A_j\ (i<j),\quad D.
\]
没有额外独立A_i动作。目标路径C₁,…,C_k,D的末位是真BR：D8，H_i^e为1+3+4=8，P_ij为2(1+3)=8，C_i为1。故它是j=m−1合法**真尾输入**，前面C_i尚未声称可信。

目标W=2k+8。以至多⌈k/2⌉个pair主题覆盖全部组，再D，槽数≤m，达到全部5k+8客户，所以OPT_m=5k+8、g=k−8，k≥9为正。拟定distinct威胁要覆盖残余reservoir并分享偏离Ai，但尚没有完整SPE；有fresh pair外选项时不能硬给低punisher收益。

事实上已有必须付的真倒二缺陷。在过去C₁,…,C_(k−1)强制P_(k,j)，j<k。当前从fresh组k得5，从旧组j得1+3=4；末位若碰这两组，任何合法主题收益至多13/2<8，而D总给8。因此**每个末位BR**都避开两组选中组（可选D），强制者最终恰9，无论平局如何。
\[
\ell_k(P_{kj})=9,\quad \delta_k\ge9-2=7,\quad 2R+D\ge21.
\]
所以k≤29时g=k−8≤21不能严格超过修复成本；k≥30只超过这个下界，更早的真实floor/成本仍未控，不构成反例。R可能线性增长，不能把k调大当完成。

## 精确去向与证据

2250B FAILED原文已全文读；8648B target checkpoint四节完整旁读，原字节与两冻结SHA见[清单](../../../../tools/evidence/origin-retraction-and-credible-entry-resources/related-source-manifest.json)。以上均解析复建，0新数学程序/LP/BI/扫描，未认证外审或新颖性；共享目录有用候选继续保留，不把失败直接退休或扩为一般不可能性。异质修复完整树和费用见[现定理](../定理/真实退出缺陷的统一与异质前缀修复--定理.md)。
