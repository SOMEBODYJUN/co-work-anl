---
id: "unrelated-machines/normalized-xos-k-cover-size-original-review-errata"
kind: review
type_tag: 审查
title: "XOS阈值规模k覆盖等价与r弱界勘误"
status: complete-primary-read-and-mathematical-reconstruction
summary: "同宇宙norm1显式max全部subset阈值的最小状态数等于k-cover，两个实际锐端点；r=d+1仅弱下界，反向uniform必须d/k≤η。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/reviews/unrelated_machines/normalized_xos_menu_threshold_size_review.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/reviews/unrelated_machines/normalized_xos_menu_threshold_size_review.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/current/unrelated_machines/normalized_weighted_menu_santa_value_and_size.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/current/unrelated_machines/normalized_weighted_menu_santa_value_and_size.md"
evidence_manifest: ../../../../tools/evidence/um-following-review-primary/source-manifest.json
---

# 对象、最小family方向与全部参数

主源f1a0fb3e7c413630cee8全文3184B/20行实读，current737121825175bccceb42全文109行/SHAce1c320e…13c5已比较；UM-NORMALIZED-XOS-THRESHOLD-MENU-SIZE-OBSTRUCTION-v2仅§4–6，§1–3实际SC桥由另一审者认证。

固定有理0<η<1、整数t≥1，原U有2t资源，d=floor(ηt)，k=max{1,ceil(d/η)}，0≤d<t、1≤k≤t。有限显式indexed clauses每个非负有理且全U总和1，允许零和重复。f(B)=max_sΣ_Bw_su，要求**每个**t-subset T有f(T)=1，每个|B|≤d有f(B)≤η。不是只保reachable或抽样bundles。

Θ(2t,t,k)是最小k-subset family，使每个t-set都**包含**其中某个k-set。则最小菜单数K_min=Θ，且
\[
K\ge\binom{2t}{t}/\binom{2t-k}{t-k}.
\]
Θ是有限组合量，不是可调用优化oracle；计数比值没有声称所有参数达到。

# Support计数、正确反向与旧r错误

每clause正support非空。d≥1时support h≤d将自身作为small B会值1>η，故h>d。其top-d项和≥d/h，而low≤η，得h≥ceil(d/η)=k；d0只需h≥1=k。某unit T上有限max由clause达到1，非负norm1迫该clause整个positive support在T内。

每clause任选support内k子集F_s，改为其上均匀1/k。原unit T仍包含对应F_s，且任意small B新值≤d/k≤η，所以两个阈值保住，去重不增K；不保所有中间B的逐点值或f_new≤f_old。反向任意Θ-family用这些均匀clauses满足两阈值，给准确K_min=Θ。每个k集只被binom(2t−k,t−k)个t集包含，全部t集必须覆盖，给上式。

v1仅由support>d给r=d+1的弱覆盖下界K≥binom(2t,t)/binom(2t−r,t−r)≥2^r。它正确但一般**不能**反向用r-family uniform满足tiny：η1/2、t4、d2、r3时，同r-support两项值2/3>1/2。旧《归一化XOS阈值规模独立Exact审查续页》§3附加的r-cover反向等价因此不成立；用v2 k=max(1,ceil(d/η))才有d/k≤η。[最小勘误包](../../../../tools/evidence/um-following-review-primary/errata/README.md)保原段/SHA与建议精确替换，不改冻结v1原件、原审读历史或进度。

# 两个真锐端点与固定η规模

d0/k1时，≤t个singletons会留下≥t个未选资源组成漏cover的T；t+1个singletons则任何T必命中，故K_min=t+1，含t1。ηt为正整数时k=t，每个t-set只能包含自己这个指定t-set，必须全部binom(2t,t)个；均匀1/t clauses在任意至多d项和≤d/t=η，取support内d项达到，故确实可行。外部零项不能写成每d项均等η。

固定η时设θ=ηt−d∈[0,1)、l=t−k=floor(θ/η)≤c=ceil(1/η)−1。d≥1时binom(2t−k,t−k)=binom(t+l,l)≤(2t)^c，中央二项式≥4^t/(2t+1)，因此
\[
K\ge4^t/[(2t+1)(2t)^c].
\]
η变时c也变；一个原additive玩家2t资源各值1/t的源只需O(t logt)bits，所以固定η下显式输出超多项式，但不是2^Ω(源位长)断言或poly求Θ结论。

仅排同U、逐玩家、非负norm1 explicit max、全部unit/tiny阈值的接口；允许辅助resources/players、全局耦合、reachable-only、unit completeness损失、未归一化或另证可处理的隐式表示均不在域。它不否定给定显式菜单的NSW算法，不提供sourcehardness或一般Santa/UM反面。

# 版本与真实审读范围

rank先冻v1 Exact/Proof，bicriteria只v1 Exact独立计数并发现更强support。root另冻v2 Exact，general仅此独立全证后才读root另冻v2 Proof，后通读canonical只签§4–6；root亲核top-d均值、有限max、family方向、d0/整数达到及总位长。v1旧弱下界与发现记录不倒写成v2完整证明。

初canonical把“任意d项和d/t=η”误写逐项等号；修为≤，support内达到，general实际读最终ce1c并逆替换恢复旧424506…，原Exact/Proof不改。另一值桥审者据此核§1–3未变，但没有一位审者独签全文件。八来源表保原v1/v2 Exact/Proof/独立/read-after/canonical身份，未冒本轮全部原件实读。无软件/有限枚举、外审或全球新颖性认证；新勘误只改mutable清洗概述，不追认原正确k稿有错。
