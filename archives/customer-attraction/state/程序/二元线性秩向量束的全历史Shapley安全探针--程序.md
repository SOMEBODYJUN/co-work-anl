---
id: customer-attraction/binary-linear-rank-bundle-full-history-shapley-security-probe
kind: program
type_tag: 程序
title: 二元线性秩向量束的全历史Shapley安全探针
status: 原程序与三报告全文实读；三个固定best精确复核；不重放随机批次
truth_status: exact-finite-BI-for-submodular-Shapley-model-with-floating-safety-proposals
scope: GF2向量束秩福利、共同单主题行动、全部有序历史纯SPE；客户coverage为其子类，三记录逐点分类
summary: signed展开是Shapley收益的精确计算设备，不等于合法客户；集合BI精确，静态LP只提案，负点才恢复query和动作。原三best分别一份非coverage与两份9客户coverage。
source_refs:
- source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-64201cd12083425899e2d643ec9bc087/next_independent/matroid_bundle_probe.py
- source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-64201cd12083425899e2d643ec9bc087/next_independent/matroid_bundle_probe.py
---

# 二元线性秩向量束的全历史Shapley安全探针

## 扩大模型：主题仍一个，福利改为线性秩

有限标签集 $P=\{0,\ldots,k-1\}$。每标签a有一个GF(2)向量束 $V_a$；整数编码向量的二进制位是坐标，不是客户会员位。玩家按完整有序历史各选一个共同主题，允许重复选择；覆盖型福利在这里被替换为

\[
 C(S)=\operatorname{rank}_{\mathbf F_2}\left(\bigcup_{a\in S}V_a\right),\qquad C(\varnothing)=0.
\]

它是归零单调次模集合函数：添加向量不减秩，较大的已有线性空间只会减少再加向量束的秩增量。这里向量不是单位客户，rank也不当然是被覆盖客户人数。

对终局所选标签向量，玩家联盟I的价值为 $C(\{a_i:i\in I\})$，每位的收益定义为这个联盟游戏的Shapley边际：在所有玩家排列中，取本人加入前后联盟价值差的平均。均分客户模型恰是C为非负coverage时的特例；一般rank函数不必有共同非负客户实现。

这种模型在[全域共同删除势定理](../定理/共同删除势的全域效率与单调次模提升--定理.md)已经解析构造：同一 $C$ 的Shapley积分势定义全整数格收益，具有单调DR、自拥挤、全部人口层效率与harmonic纯态。本程序只是其中一种有限输入探索，不证明该一般定理或任何普遍聚合／half。原5197B稿也已作同一身份说明，本批完整比较，不因三个有限输出重授一般结果。

## GF2秩、采样与共同signed计算

原4708B[程序](../../tools/evidence/matroid-bundle-four-boss3/original/matroid_bundle_probe.py)只有标准库加NumPy/SciPy依赖，没有规范CAG solver导入。`rank`以最高非零位为pivot，用异或消元维护线性独立基；重复向量、束内相关不会重复加秩。`sample`对每标签先均匀取1至4次，再从1至 $2^d-1$ 抽非零向量、去重排序，因此实际束大小1至4，未保证束内或不同束互不相关。

`coverage`生成整个 $2^k$ 项C数组。随后 `signed_weights` 对全部非空类型 $B\subseteq P$ 作反演

\[
 w_B=\sum_{D\subseteq B}(-1)^{|B|-|D|}
       [C(P)-C(P\setminus D)].
\tag{1}
\]

因为 $C(P)-C(P\setminus D)=\sum_{B\subseteq D}w_B$，Möbius反演保证对任何C均有
$C(S)=\sum_{B:B\cap S\ne\varnothing}w_B$。全体非空类型的这份signed表示唯一；w可负，负数仅用于线性计算。若所有w非负整数，反而确有不同单位客户的共同实现，不能因函数来自matroid就一概标非coverage。

以终局标签计数q、已占行动a表示，其Shapley收益可写成

\[
 U_a(q)=\sum_{B\ni a}\frac{w_B}{\sum_{b\in B}q_b}.
\tag{2}
\]

理由是每个coverage原子在联盟游戏中由最早出现的喜欢者取得边际1，每位喜欢者以均等概率最早；Shapley值线性使同一公式对signed组合仍真。原`pay`用 $L=\operatorname{lcm}(1,\ldots,m)$ 整数缩放计算(2)，分母始终在1至m，整除无误，Python整数无固定溢出。未被选行动的数组槽填0，**不是**该未加入行动的查询利润；静态查询时原码先加 $e_a$ 再读取。

`Solver`不自行校验任意外部C是否归零、单调次模；main的向量束rank保证它们。负w也不意味着这里出现负收益：对单调C，Shapley的每次边际非负，虽用signed和计算仍有 $U_a\ge0$、$\sum_aq_aU_a=C(\operatorname{supp}q)$。

## 精确全部SPE终局与完整策略展开

`solve(q)`缓存所有可由完整纯SPE实现的终局计数集合E(q)。终端返回单元素；否则对各行动的孩子集合 $E_a$ 计算

\[
 \theta(q)=\max_a\min_{s\in E_a}U_a(s),\qquad
 E(q)=\bigcup_a\{s\in E_a:U_a(s)\ge\theta(q)\}.
\tag{3}
\]

比较用上段精确整数，不是浮点破平局。同计数前缀具有相同剩余博弈，所以可缓存**可实现终局集合**；实现子策略在不同有序历史仍可独立拼接，不强制一般SPE匿名。必要性由当前最佳回复必须高于每个孩子的最小可能收益；充分性在实际孩子实现目标终局，其他有序孩子选当前玩家最坏子SPE，逐子树拼接成立。这与[既有全集递推](../算法/完整历史纯SPE终局全集--算法.md)相同，证明只需有限行动、终局收益依计数和相同玩家，不要求先有非负客户。

`evaluate`在根集合中按 `(C(实际支持),q)` 取字典序最小的最差福利代表，得到W和target。`root_outcomes`若本轮记录，是终局计数数量，不是完整策略数。程序没有用最差单一路径代替全部可信终局。

`certificate(target)`在每个**有序历史**选第一个可实现目标且过门槛的行动；实际孩子继续该目标，其他孩子选使当前行动收益最小、再按终局字典序的子SPE目标，递归展开整树。返回所有长度小于m的历史动作，按深度与历史排序。虽然用计数集合决定候选，这份完整表没有被改成单一计数动作函数。原码没有另作定义级独立证书验证；本轮三个固定target才另生成新表并独立检查。

## 真正整数静态安全值与负候选闸门

static safety使用同一个抽象Shapley模型的 $m-1$ 名竞争者。背景为所有非负整数计数b、$\sum_ab_a=m-1$，查询a的收益为 $U_a(b+e_a)$。`solve`递归展开所有行动，所以 `self.th` 的深度m−1键恰覆盖这些背景，不只保根可实现SPE终局。程序求

\[
 v_m=\max_{p\in\Delta(P)}\min_b\sum_ap_aU_a(b+e_a)
\tag{4}
\]
的浮点LP提案；背景不观察查询，不是自由分数背景、真实根回复菜单或查询依赖对手。目标差为 $W-mv_m$，测试的是**强安全聚合**，代码没有计算OPT来直接测half。

只当float差小于 $-10^{-8}$ 时，才把query逐坐标限分母 $10^6$、归一化，用Fraction在**全部背景**上取最小保证g，再要求 $W<mg$。通过才加 `query,exact_safety_lower_bound,exact_gap,actions,coverage,signed_weights` 字段。这一g只需精确下界就足以反聚合，未验证它是精确最优；原源码也没有静态LP对偶恢复。

概率非负在发现LP中由bounds给出，但该分支没有再显式断言恢复后 $p_a\ge0$；精确候选仍应实际核概率合法、和1和全部背景，不能只看exact字样。另有具体复用前提：负分支写 `coverage=C` 使用**模块全局C**，不是`self.C`。原main每次先把同一函数赋给global C，CLI内匹配；独立导入后若未设置正确global C，负分支可能NameError或输出另一函数。三冻结best均未进入这个分支，本轮不改原码、不把未来类复用行为当已认证。

## 原三随机批次声明与输出范围

CLI默认seed37、topics6、players3、dimension6、games1000；输出名由`Path(__file__).with_name(out)`定位源码相邻文件，需要basename，非任意目录路径。main按完整C数组去重，不按原向量束字面量去重；同C、同m的完整收益和SPE相同，这种函数去重语义正确。

每次新C都运行精确BI和一次静态LP。best以float gap严格改善超过 $10^{-8}$ 才更新；发现带exact_gap的候选即break。最后JSON保存status、args、单个best、distinct_functions及elapsed_seconds，不是全部输入、函数、LP证书或改进轨迹；stdout只打印改善摘要。没有输入JSON读取，main有guard，安全导入仅定义类／函数与加载依赖，不开始随机采样。

三报告原声明分别2000、1000、400 games，distinct_functions恰同数；其保存best出现在trial35、645、253。它们未给原运行event／stdout／源码SHA／全部采样历史，本轮保历史字段，不将原6.083／12.074／11.407秒说成当前重放，也不从文件存在认证所有历史调用。三best都没有负候选字段；三人float gap约 $-8.88\times10^{-16}$ 没越闸门，绝非精确失败。

本轮只处理三个保存的bundle输入：原整数集合BI各一次，另用玩家联盟Shapley子集式独立核2184个占用收益、新完整策略22665次含自身比较，以及三个新的静态LP候选后恢复精确query下界／对偶上界。没有生成随机输入或运行原随机CLI。三点分别非coverage、真9客户、真9客户；精确差0、1/4、1/3。完整数值、原／新身份及可复用证明见[配套计算页](../计算/三份向量束秩记录的客户实现与精确安全值--计算.md)，不由有限阴性推普遍聚合或六人half。
