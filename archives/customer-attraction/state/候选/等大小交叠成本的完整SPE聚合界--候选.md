---
id: "customer-attraction/equal-size-overlap-full-spe-aggregate-quadratic-bound"
kind: "conjecture"
type_tag: "候选"
title: "等大小交叠成本的完整SPE聚合界"
status: "unproved-and-no-certified-counterexample-in-reviewed-material"
summary: "准确保留负incidence-Gram辅助游戏的全目录全人数全完整SPE二次聚合候选，说明高背景用途、严格抬升条件及有限阴性不能支付的缺口。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-b6d636d360e14c11aeb4b76415ed422b/security_aggregate/uniform_background_quadratic_interface.md#4"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-b6d636d360e14c11aeb4b76415ed422b/security_aggregate/README.md"
---

# 等大小交叠成本的完整SPE聚合界

## 完整量词

取任意有限非空共同主题标签目录、有限单位客户，所有主题大小同为 $K\ge0$，允许同覆盖不同标签及重复。对任意 $m\ge1$，依次行动的m名单位玩家各最小化

$$L_i(S_1,\ldots,S_m)=\sum_{j\ne i}|S_i\cap S_j|.$$

玩家观察全部有序历史；完整纯SPE在每个历史均可信，离轨平局可依历史而异。记 $G_{ST}=|S\cap T|$、终局计数c及

$$H(G)=\min_{p\in\Delta(\mathcal S)}\max_{A\in\mathcal S}\sum_Tp_TG_{TA}.$$

原二次候选QG为：**每个上述实例、每个人数、每份完整纯SPE** 均满足

$$\boxed{\sum_iL_i=c^TGc-mK\le m(m-1)H(G).}\tag{QG}$$

$m=1$ 或 $K=0$ 两边直接为零；这些退化情形不解决一般量词。负Gram的“负”指收益为 $-L_i$，G本身仍为非负PSD的集合交叠矩阵。任意非负对称矩阵、一般PSD矩阵或抽象匿名势游戏不自动具有同一客户的0/1集合实现。

## 为什么这个候选出现

[显式二阶接口](../定理/均匀背景的真安全值二阶接口与策略极限--定理.md)对外生均匀旧负载B、$a=B+1$ 给

$$P_B-mv_m(B)=\frac{m(m-1)H-(c^TGc-mK)}{a^2}+E_B,
\quad |E_B|\le mK(m-1)^2/a^3.$$

固定有限实例的高背景SPE可抽出固定完整策略子列，其极限必是负Gram SPE。因此若QG普遍成立，就不存在固定正系数的 $B^{-2}$ 规模聚合安全亏损；仍可能留下更小规模失败。相反，负Gram坏策略若要变成真正有限B坏SPE，必须补全部比较的严格余量或精确高阶平局控制，不能把任意弱成本SPE直接提升。

H也不能替成 $\min_q q^TGq$；上引定理的六客户四三元主题例精确给H=2、最小范数5/3。较小二次值会成为另一个更强候选。

## 实际证据和准确未决点

[有限探针](../资源/等大小交叠与成对策略锥的有限探针--资源.md)报告六标签、十客户中大小四主题、m3…7各200输入，未见正gap；其集合值BI在给定整数矩阵内保留所有可实现终局，但只覆盖这些有限输入，H由浮点LP求得。任意对称矩阵扩域扫描也未见违反，不增强到原客户全域证明。另一成对锥程序优化的是**首人个体代价**与固定查询安全上界之差，不是QG聚合目标；没有精确锥对偶或全策略覆盖。

本批未提供QG的一般证明、精确反例或外审认证。原README及其后继方向评估均明确停止累计阴性Gram扫描，并把QG列为外生背景辅助义务；这是历史研究选择，不能把“暂停”改成命题已假或已真。

## 如何继续及与原目标的距离

可接续结果应是：一般的完整策略论证，或明确等大小集合目录、完整有序策略、全部真实偏离精确比较及严格QG负证书。抽象矩阵反例只能先反驳扩大模型；还需验证incidence实现。若谋求迁移回原CAG，另需控制有限B的余项、合法背景的原目录实现及背景玩家收益、不等大小的一阶项，最后才涉及B=0根福利。

即使QG为真，也没有自动得到真正空根强/弱安全聚合或六人half；已知五人half同样不能反推这个更强、不同模型的候选。阶段三关系仅为二阶接口提出的精确义务、有限程序的判别目标与原模型提升障碍，不补造已证依赖。
