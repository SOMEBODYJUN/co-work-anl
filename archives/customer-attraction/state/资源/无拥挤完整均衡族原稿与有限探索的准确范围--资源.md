---
id: customer-attraction/collision-free-complete-equilibrium-family-source-and-finite-search-scope
kind: resource
type_tag: 资源
title: 无拥挤完整均衡族原稿与有限探索的准确范围
status: 四主源全文实读；完整构造复用现行证明，有限探索与后续纠错分开
source_refs:
- source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/global_proof/README.md
- source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/global_proof/collision_free_occupancy_obstruction.md
- source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/global_proof/collision_free_three_halves_family.md
- source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/global_proof/promoted_punishment_family_failure.md
---

# 无拥挤完整均衡族原稿与有限探索的准确范围

四原件共18599B：全局README4467、五客户4468、任意k族6678、多围堵失败2986。模型均有限单位客户/共同目录/单位提供者/全有序历史纯SPE，不将六个主题误读为六位玩家。所有原实验/原内部独核均保历史身份，本批0原/新数学入口，不重复旧成功。

## 五客户与任意k的数学去向

[五客户完整证明](../反例/五客户无拥挤SPE负载桥障碍--反例.md)与原S0…3按A/B/C/D映射相同：S0={x0,x1,a}、S1={x0,x1,b}、S2={x0,x1}、S3={b,d}，根2、末回复1/0/3/0。原5节点20含自身/15真正比较的全表及16终局最优值均在该自足对象。实际23两主题不交、u=(2,2)、W4、OPT5；负载函数f0=0/f1=1无论高负载系数如何都只有4，不能支配OPT。逐客户复制k次成W4k/OPT5k仍完整SPE；不规范f1时只给必要f1≥5/4。实际首主题严格小于另两个主题，扩大动作会触发真实离轨回复、用共享亏损抵消新增客户，故实际无拥挤不等于离轨可忽略。

[任意k族完整归纳](../反例/三人碰撞自由族福利障碍--反例.md)的文件名沿旧稳定对象；定理实际适用于每k≥1、m=k+1、p=3k+1、3k+2客户，并不只三玩家。目录A_i=X_i+a_i、B_i=X_i+b、C_i=X_i、D=b+d，|X_i|2，其余每块1。存在完整SPE路径所有C_i后D，收益全2、W2k+2；所有A_i加D覆盖全部，OPT3k+2，比例趋3/2。对统一纯负载付款只迫必要f1≥3/2，不证明此系数充分或3/2一般上界。

原构造的承重证明已与完整正文逐项对照：Q域允许任意多个旧A/C，每组恰触一次，无B/D，g未触组/余g+1人。指定旧A组t或空，依次freshC后选B_t或D。freshA偏离更新指定组、**保留全部旧A历史**；freshB进入B域，不能粗称即时利润≤2。B域恰一个B_i，其余旧A/C，指定续局freshA后A_i；freshA独享3达到全目录主题大小上限，故任意兜底SPE不破最优。g0末位均分给指定回复2且其它≤2。每次递归人数减一，分支有序历史不相交，兜底全树BI和特殊域可以独立粘合；没有同计数策略必须相同的限制。空根属于Q域。这些是全参数存在证明，不由有限k的结果集枚举外推。

源称audit_collision_free_family对k1/2/3分别5/57/1111节点、20/399/11110含自身比较，特殊Q/B外用普通BI补树；Root当年另有结构审计和独立研究员符号重构。当前本批不据源声明冒称新独立代码重演或外审。五客户原审计、九客户发现中间点、十一客户早版均按不同输入保留，不删除旧版来伪造单一路线。

## 多围堵直接推广及其它复制失败分列

本批新自足[末位障碍](../障碍/多个围堵块的目标终局末位障碍--障碍.md)证明t>2的所有k、所有目标排列均失败；t2只保末位D的有效顺序。原三点oracle是发现背景而非普遍结论的前提。不能从本目标失败推出一切无拥挤趋2构造失败，更不能称原half已解。

## README有限扫描的完整边界及旧OPEN纠错

* background_regret_probe固定完整Markov策略，以LP攻击任意合法背景r人SPE的P+新增覆盖Δ≥freshOPT_r。q6/r3完成100棵，每棵最多12比较主题；q7/r5主动停止，最后输出确认至少600棵、每棵最多12比较。都是源有限浮点无负点，非所有策略或精确证明，无后台仍在运行。
* collision_free_ratio_probe：q6/m3、500随机完整Markov策略，加实际load≤1，最高浮点候选约1.116279，没改善已证5/4，更不构成比例上界。
* joint_collision_free_probe：m3/q6完整有序历史联合MILP，按比较主题与实际交集k=0/1/2各15秒，均只提比1；超时/浮点优化状态不是不存在更好SPE的证据。joint_collision_free_m3p6.json和k1版本只保原指针，没有本批读取或新复跑；未继续扩大m4。
* truncated_potential_probe第86棵78客户点与同策略MILP压至11，由[11客户自足证书](../反例/三人均衡调和势低于最优覆盖的十一客户证书--反例.md)保完整真实客户/策略，不靠发现优化器作有效性证明；更强五客户/任意k负载障碍不原位覆盖它。

原README两次说背景P+Δ整体仍OPEN，这是当时扫描后的状态。后来[实际52客户根前缀完整SPE](../反例/实际前缀的剩余利润与新增覆盖--反例.md)在实际前缀有P17、Δ0、freshOPT₂18，已反驳P+λΔ的所有固定λ整体式；因此今天不能照录OPEN。早期23/488首步失败确实只反逐步，不反整体，与52例不同。该52例原模型half仍成立，背景加强失败不能转成六人半覆盖反例。

## 保全与接续用途

原4冻结主稿完整字节在[证据原件](../../tools/evidence/collision-free-family-and-terminal-obstruction-primary/original/)，逐源ID/哈希/size和真实claim在manifest；数学已在现行定理/反例或本新障碍自足展开。既有独审与源当时Root/研究员交叉核对分别保时间及先验，不倒称本次盲审、原运行或外部评审。

关系供第三阶段：五客户是任意k族k1端点；任意k给f1必要下界3/2；多围堵是同结构t推广但目标末位IC失败；固定实际占用付款不能处理离轨共享损失，背景整体又有独立原模型反例。后续要用所有真实分支的合法信用或另造不同构造，不能堆有限无反例样本补未付普遍预算。
