---
id: customer-attraction/true-source-menu-ap-seventy-six-atom-exact-primal
kind: computation
type_tag: 计算
title: 真实源双菜单AP必要系统的七十六原子精确可行点
status: exact-feasible-for-current-frozen-scalar-2621-rows;not-game-or-optimum
truth_status: rational-countermodel-to-factor-two-from-stated-linear-rows
review_level: original-data-completely-read;one-source-function-Fraction-qualification;not-independent-implementation
scope: 五名单位提供者的共同有限非空目录与单位客户完整历史模型所导出的明定压缩必要行；全部允许的直方图原子域
summary: 七十六个正有理质量满足2621条保存必要行、W=1且O约2.02730894678；固定点资格由当前冻结标量函数逐项绑定，不声称历史生成同版、全域最优、真实OPT或SPE。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round13/certificate/exact_menu_ap_primal.json
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round13/certificate/menu_ap_discovery.json
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round13/certificate/freeze_menu_ap_primal.py
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round13/certificate/menu_ap_pricing.py
---

# 真实源双菜单AP必要系统的七十六原子精确可行点

这是一份精确线性系统障碍：所写2621条必要行不足以推出比较覆盖O≤2W。它保留五人HALF探索中的真实数学，和已由[另一完整证书证明的五人半覆盖](../定理/五人半覆盖--定理.md)相容。原README中HALF(5) OPEN是当时状态，不是本页当前问题状态；本点不能迁移成六人反例。

## 类型、质量与所否定的命题

原模型为五名单位权提供者、有限单位客户、有限非空共同带标签目录；每名提供者观察全部有序历史，终局客户在覆盖者之间均分。空主题、重复选择、同覆盖异标签、零客户及所有离轨平局均保留。下面的类型域是从同一完整纯SPE抽取记录后得到的放大域，不能反向假定每份记录都实现一份共同策略。

旧十主题会员位顺序为`ABCDEUVWXY`；三叶为actual `ABCDE`、在A后强制第二位E再沿原σ的 `AEUVW`、在AB后强制第三位E再沿原σ的 `ABEXY`。首真优化位置（零起）分别0、2、3。固定五个合法比较索引T_i，可重复。AB与AE两族记录强制T_i后的两回复，其8格直方图按字典序(t,r,s)；Sbranch在A后强制T_i，记录三回复，其16格直方图按(t,u,v,w)。每图总数5，三个首位t总数共同为d∈{0,…,5}。三份旧末回复菜单边缘`menus_lh`各为(ℓ,h)，满足0≤h≤d、0≤ℓ−h≤5−d。这些是旧末回复的会员计数，不是原子质量。

对类型a令w(a)=1_{actual前五位至少一位为1}，o(a)=1_{d>0}。非负有理质量μ_a定义

\[
W=\sum_a\mu_aw(a),\qquad O=\sum_a\mu_ao(a),\qquad
S_r=\sum_a\mu_a r(a).
\]

本页命题只涉及μ≥0、W=1和全部指定S_r≥0。T_i真正取某个最优五元组时O才是原OPT；保存必要点没有给出共同原目录/全部历史σ或这个最优性。因此正文始终称O“比较覆盖”。

## 明定2621行

|层|数量|确切含义|
|---|---:|---|
|原旧系统|557|完整直方图索引必要行、保留交集版本的同族末两人五种相等模式、末位离对角查询|
|跨族成对查询|160|源只AB/AE、目标为另一AB/AE/Sbranch，保共同T会员与五种三索引相等模式，overlap=1|
|fixed AP|707|七个非末真优化源，每源10×10固定位对及一个五槽opt×opt|
|同族菜单AP|1197|AB/AE每族每源48，Sbranch每源75；仅同族双菜单、菜单×固定位、菜单×opt两方向|
|总计|2621|不含跨两个自由直方图的双菜单AP|

底层557=旧437+10末位离对角+110同族五等号型强PAIR；旧437的逐行定义与必要性在[五人索引福利界](../定理/五人索引最优偏离福利界--定理.md)，10/110的完整域与五型见[增强索引系统](../审查/增强索引系统的全型定价与可行点分离--审查.md)。160跨族行的真节点共同锚点依据在[跨族末两人菜单引理](../引理/跨族末两人菜单的共同锚点与运输界--引理.md)；[717原父审](../程序/最终七百一十七行点与共同匹配的原父审--程序.md)给其字面三索引形式：每源真末两人的H_i=(a_i+b_i)/(p_i+a_i+b_i)+a_i/[(p_i+1)(p_i+2)]减两个查询份额再加**一份**交叠，依i=j=k、j=k≠i、i=j≠k、i=k≠j、全异分组求和。源背景在共同t组内常值，故这里保特殊跨族可加性，非任意跨族查询免费可分。该父审的另一个61/717点与本76/2621点不是同一输入；本页只沿用行定义，不借它的运行认证。

七源为actual位置0…3、second位置2/3、third位置3；被强制E的槽和末位不作AP源。其当前客户份额u、前缀负载p、余人数k给a_k=8(k−1)+k²。两合法菜单长度n_C,n_D、该客户计数c,d'的行系数为

\[
n_Cn_Da_ku-\frac{(a_k-2)n_Dc+2cd'}{p+k}
-\frac{2(n_Cd'-cd')}{p+1}.
\tag{AP}
\]

单主题长度1、索引菜单与opt长度5；相同菜单也扫全部有序笛卡尔对，包括对角与重复。根Sbranch末回复J_i对T_j求和再乘5是7125u₁−275ΣJ_x−50Σd_x+8ΣJ_xd_x≥0。[成熟AP审查](../审查/真实源AP菜单的笛卡尔求和与定价闭包--审查.md)已给任意合法主题AP的完整证明、压缩恒等式、源合法性及条件可分定价，本页沿用，不把原子检查充作一般证明。557/160行权威标量式和2621个有序行名均保于[证据包](../../tools/evidence/Boss7-resume-rcd-ap-tuple/README.md)的原文件与依赖副本，不只保存活动行名。

## 精确点与结果

原件`exact_menu_ap_primal.json`，555420B，SHA-256 `59e4393c8781a864ac5b898a5faec2fe1e25ceaef2c128746edcf1f92b9bed2b`。76个原子全部有正有理`exact_mass`，W=1，且

\[
O=\frac{301096005584531931518151878370617731245854978526707777317258703718564906124049}
{148520039859838019388353751817515100196948145475874390394861284859859633706762},
\]

\[
O-2=\frac{4055925864855892741444374735587530851958687574958996527536133998845638710525}
{148520039859838019388353751817515100196948145475874390394861284859859633706762}>0.
\]

因此O≈2.027308946783771。全部2621个S_r非负，最小0，恰88个为0。每个原子可有正负行系数，只有按全部客户质量求和的S_r承担必要性；没有假定逐客户所有行非负。

全部76结构/质量、2621有理余量、scope/source_sha/code_sha/原作者seconds均完整保存。对应发现池有1080列，只有76个正浮点质量；其另34列带来的旧`exact_mass`是前代数据，本点恢复时以新质量覆盖，不能拿它们当当前1080列质量。`source_sha256`精确指向796382B、SHA `02ab432555bd8d1a16b70d12dbf2f55ff15228c1426fe152cd15fa40089d6a4e`的发现报告；去掉继承质量字段后，发现质量>10⁻⁸的按序结构与本76原子逐项一致。所有零列和发现过程另见[程序与轨迹](<../../../../tools/evidence/phase25-material-attachments/20261103-boss6-triage/e735c5e2c1bdd71754bb.md>)。

## 当前资格与历史生成身份分开

接续的同一次标准库Fraction资格检查抽取冻结原源码白名单scalar函数，未import原模块，未运行原Universe初始化、QR、LP、BI、CG或全域price。对本76×2621=199196个有理系数求和，逐一核2621个保存余量完全相等；μ>0、共同d/菜单域、W/O/差值及88零行均相符。此检查是**复用原函数的抽取核**，不是第二套独立系数实现或原CLI重放。一次两点联合检查的进程与完整逐行输出见证据说明，本页不重复运行。

原发现、精确点与四例回放记录的menu代码SHA均为`dae5573ff8b5577e12e7ece42b621697de17ed599af214ea8894d9d7ea2daa10`；当前冻结9062B `menu_ap_pricing.py`为`1bf8fac75ae4a5f65c13ad66c8c3ae4463b642572623baf3a3f1321b054e2f19`。本次等值核定的是**当前冻结scalar式上的这个保存点**，没有证明旧生成运行与当前全部程序同版，不能改写原code_sha来消去差异。

## 障碍如何复用

这个μ是明定线性系统的反模型。若仅用这些S_r≥0、μ≥0与W归一导出O≤2W，代入本点便矛盾；尤其不存在把这些行以非负乘子合成全允许类型有效系数二上界的证书。它不确定该系统全域最优值，也不否定加上真实共同策略一致性/新菜单关系后的系统。保存具体点可用于在同一μ上精确测试新行、寻找缺失共同历史关系；新行值和输入SHA需另存，不能把分离另一个旧点的负值借来。当前五人half证明与本必要系统的不充分性应保为两个对象。
