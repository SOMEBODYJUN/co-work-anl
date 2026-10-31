---
id: "unrelated-machines/learning-augmented-makespan-prediction-guided-search"
kind: "resource"
type_tag: "文献"
title: "学习增强的非相关机最大完工时间：预测引导的重作业搜索"
status: "retained-with-scope"
summary: "Baba–Bampis–Mitropoulos 的 arXiv:2606.13133v1 论文。对 R||Cmax 输入一个部分机器分配预测，只固定 εT 重作业投影，再枚举至多 K 个遗漏重作业、解残余 LP 并用 Shmoys–Tardos/LST 舍入；给出随假阳性超载和第 K+1 个遗漏重作业平滑变化、始终不超过 2OPT 的近似保证。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/literature/unrelated_machines/baba_bampis_mitropoulos_2026_learning_augmented_v1.pdf"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/literature/unrelated_machines/baba_bampis_mitropoulos_2026_learning_augmented_v1.pdf"
---

# 学习增强的非相关机最大完工时间：预测引导的重作业搜索

## 来源身份与处置

本页逐页读取冻结 PDF `baba_bampis_mitropoulos_2026_learning_augmented_v1.pdf`（arXiv:2606.13133v1，2026-06-11，Baba、Bampis、Mitropoulos），冻结源 blob 为 `187bb9ed491a47fcc26af24580e99abfdb4df286`，文件 SHA-256 为 `611d6650d65255e9515cc126a9a5f64a0d4d5292411abadc455614148bd1c09f`，大小 898138 字节。`legacy-cleanup` 与 `main` 两个冻结提交的同路径内容由清单合并为同一文献对象；没有把论文正文复制进仓库，也没有把引用文献的结论当作本页已核验事实。

这是外部文献/资源对象，独立于本档的近二问题。当前 `archives/unrelated-machines/问题--问题.md` 讨论无预测的非负二进制有理输入上是否存在统一 (2-\varepsilon) 算法；本论文研究有额外预测、允许误差项的学习增强算法，不能直接回答或否定该问题。它也不属于六人共同目录的 SPE 覆盖模型。

## 模型与预测对象

有 (m) 台非相关机器、(n) 个作业，机器 (i) 上作业 (j) 的处理时间为正数 (p_{ij})，调度是函数 \(\sigma:[n]\to[m]\)，
\[
 C_{\max}(\sigma)=\max_i\sum_{j:\sigma(j)=i}p_{ij},\qquad OPT=\min_\sigma C_{\max}(\sigma).
\]
论文将处理时间视为输入的二进制数，令 (P=\max_{i,j}p_{ij})。预测是部分分配
\(\hat\phi:[n]\to[m]\cup\{\bot\}\)：\(\hat\phi(j)=i\) 表示预测把作业 (j) 放到机器 (i)，\(\bot\) 表示弃权。完整分配预测只是特殊情形；允许弃权是为了不错误地固定不确定的重作业。

给定目标阈值 (T>0) 与 \(\varepsilon\in(0,1)\)，只保留预测中满足 \(p_{\hat\phi(j),j}>\varepsilon T\) 的条目，得到重作业投影 \(\hat\phi_T\)。其余作业交给残余 LP。阈值严格大于 \(\varepsilon T\) 是算法的承重条件，不能把“重”换成仅按作业大小或按最优调度中的负载判断。

## 内层算法：局部补回遗漏重作业

对 \(\hat\phi_T\) 枚举增量 \(A:[n]\to[m]\cup\{\bot\}\)，满足
\[
 \operatorname{dom}(A)\cap\operatorname{dom}(\hat\phi_T)=\varnothing,\quad
 |\operatorname{dom}(A)|\le K,\quad p_{A(j),j}>\varepsilon T
\]
（最后条件只对 \(j\in\operatorname{dom}(A)\) 要求）。令 \(\psi_A=\hat\phi_T\cup A\)。对每个候选 \(\psi_A\)，构造离散阈值集
\[
 \Lambda(T)=\{\varepsilon T\}\cup\{p_{ij}:p_{ij}\ge\varepsilon T\}.
\]
对每个 \(\tau\in\Lambda(T)\)，固定 \(\psi_A\) 的机器负载 \(\ell_i^{\rm fix}(\psi_A)\)，在未固定作业上解 LP：每个作业分配总量为 1；机器 \(i\) 的残余负载不超过 \(L-\ell_i^{\rm fix}\)；禁止所有 \(p_{ij}>\tau\) 的残余边；其余 \(x_{ij}\ge0\)。若 LP 可行，用 Shmoys–Tardos 舍入（论文注记 LST 舍入给出同一保证），舍入后每台机器至多增加 \(\tau\)，候选完工时间至多 \(L_{\psi_A}+\tau\)。输出所有候选中完工时间最小者。

证明中真正使用的增量是最优比较调度 \(\sigma\) 中至多 (K) 个遗漏重作业；选择它们作为 \(A^\star\) 后，剩余遗漏重作业的最大处理时间就是第 (K+1) 大遗漏重作业。因此该算法只局部搜索预测邻域，未声称消除了所有重作业枚举的指数因素。

## 外层算法：临界阈值同步

先运行 Lenstra–Shmoys–Tardos (LST) 经典 2-近似，得基线调度 (S_0) 和 (B=C_{\max}(S_0)\le2OPT)，故 \(OPT\in[B/2,B]\)。外层临界集合为
\[
 \mathcal T=\{B/2\}\cup\{p_{ij}/\varepsilon:B/2\le p_{ij}/\varepsilon\le B\}\cup\{B\}.
\]
对每个 (T\in\mathcal T) 运行内层算法并把 (S_0) 一起比较。选择这个集合的理由是：在最大的 (T^\star\le OPT) 与 (OPT) 之间没有新的 (p_{ij}/\varepsilon)，因此重/轻分类、预测投影和错误量在两阈值上一致；固定阈值上不能直接二分，因为内层失败也可能来自错误预测而非真实不可行。

## 误差量与主保证

对任意比较调度 \(\sigma\)，定义遗漏重作业集合
\[
 \operatorname{Miss}_T(\hat\phi,\sigma)=\{j:p_{\sigma(j),j}>\varepsilon T,\ \hat\phi_T(j)=\bot\}.
\]
遗漏阈值
\[
 R_T^-(\hat\phi,\sigma)=\max_{j\in\operatorname{Miss}_T}p_{\sigma(j),j}
\]
（空集时为 0），以及预测错误机器造成的假阳性超载
\[
 R_T^+(\hat\phi,\sigma)=\max_i\sum_{j:\hat\phi_T(j)=i,\ \hat\phi_T(j)\ne\sigma(j)}p_{ij}.
\]
预算 (K) 后的遗漏阈值
\[
 R_{T,K}^-(\hat\phi,\sigma)=min_{U\subseteq\operatorname{Miss}_T,\ |U|\le K}
 \max_{j\in\operatorname{Miss}_T\setminus U}p_{\sigma(j),j},
\]
即遗漏重作业处理时间的第 (K+1) 大值，空集约定为 0。

**内层定理（论文 Theorem 5.1）。** 对任意 (T,\varepsilon,K,\hat\phi) 与任意比较调度 \(\sigma)，内层输出可行 (S) 且
\[
 C_{\max}(S)\le C_{\max}(\sigma)+
 \max\{\varepsilon T,R_{T,K}^-(\hat\phi,\sigma)\}+R_T^+(\hat\phi,\sigma).
\]
运行时间为
\[
 O\big((mn)^K\,\operatorname{poly}(m,n,\log P,1/\varepsilon)\big).
\]
证明先选掉至多 (K) 个最大的遗漏重作业作为 (A^\star)，令 \(\tau^\star=\max\{\varepsilon T,R_{T,K}^-\}\)，用 \(\sigma) 给残余 LP 一个可行分配；错误预测只会给固定负载增加 (R_T^+)，舍入再增加 \(\tau^\star\)。枚举增量数不超过 \((K+1)(mn)^K\)，阈值数不超过 (mn+1)。

**外层定理（论文 Theorem 5.2）。** 令 \(\sigma^\star\) 为最优调度，(OPT=C_{\max}(\sigma^\star))。外层输出满足
\[
 C_{\max}(S)\le
 \min\left\{OPT+\max\{\varepsilon OPT,R_{OPT,K}^-(\hat\phi,\sigma^\star)\}+R_{OPT}^+(\hat\phi,\sigma^\star),\ 2OPT\right\},
\]
并且进一步
\[
 C_{\max}(S)\le
 \min\left\{(1+\varepsilon)OPT+R_{OPT,K}^-(\hat\phi,\sigma^\star)+R_{OPT}^+(\hat\phi,\sigma^\star),\ 2OPT\right\}.
\]
运行时间与内层相同。因而准确预测（两误差均为 0）给多项式时间的 ((1+\varepsilon)OPT)；任意坏预测仍有 LST 的 (2OPT) 兜底；(K) 增大只降低遗漏项并增加 \((mn)^K\) 时间，假阳性项与 (K) 无关。

两篇附录结论也属于该对象的范围：(K\ge|\operatorname{Miss}_{OPT}|\) 时遗漏项消失，只剩 \(\varepsilon OPT+R^+\)；(K=0) 时无局部搜索，误差项为最大遗漏重作业与假阳性超载之和，运行时间退化为普通位多项式。论文给出完整证明而非仅数值猜测。

## 可编辑预测变体（附录 D）

论文还定义可编辑邻域
\[
 E_{T,K}(\hat\phi)=\{\psi:d_T(\psi,\hat\phi_T)\le K,\ \psi(j)\ne\bot\Rightarrow p_{\psi(j),j}>\varepsilon T\},
\]
其中一次编辑可插入、删除或改派一个重作业。对同一个 \(\psi\) 同时计算遗漏与假阳性，定义
\[
 \Delta_{T,K}^{\rm edit}(\hat\phi,\sigma)=
 \min_{\psi\in E_{T,K}(\hat\phi)}
 \left(\max\{\varepsilon T,R_T^-(\psi,\sigma)\}+R_T^+(\psi,\sigma)\right).
\]
附录定理 D.1 给出内层 (C_{\max}(S)\le C_{\max}(\sigma)+\Delta_{T,K}^{\rm edit})，定理 D.2 给出外层
\[
 C_{\max}(S)\le\min\{OPT+\Delta_{OPT,K}^{\rm edit}(\hat\phi,\sigma^\star),2OPT\}
\]
及相应 ((1+\varepsilon)OPT) 形式，运行时间仍为 ((mn)^K) 乘位多项式。附录还证明：若预测的 (OPT)-重作业投影与最优重作业投影的编辑距离不超过 (K)，则可编辑版本达到 ((1+\varepsilon)OPT)。编辑误差总量随 (K) 单调不增，但其中单独的遗漏/假阳性分量不必单调，因为删除一个假阳性可能制造遗漏。

## 证据、实验与限制

论文第 6 节及附录 F 的实验均为作者新生成的有限合成实验，不是一般性证明。主实验取 (p_{ij}\sim U[1,100])，(m=10,n=100,\varepsilon=0.01,K\in\{0,1,2\})，从最优调度重作业投影随机制造假阴性或把可改派重作业随机改到另一台重机器；五个随机种子报告均值和标准误。附录另测 (m=10,n=50)、(m=5,n=100) 和机器相关模型 (p_{ij}=\alpha_i+\eta_{ij})，其中 \(\alpha_i\sim U\{1,\ldots,100\}\)、\(\eta_{ij}\sim U\{1,\ldots,20\}\)，以及固定 (m=5) 变化 (n\in\{5,\ldots,15\})。实验趋势与定理一致：误差增大时平滑退化，(K) 对假阴性有效而对假阳性几乎无影响，始终低于所测的 LST 2-近似；这不等于对所有随机实例或学习模型的外部验证。

实现使用 Python 3.13.11、OR-Tools CP-SAT 9.15.6755 求最优调度，SciPy 1.17.1/HiGHS 解 LP，单机 Intel Core Ultra 7 155H、22 逻辑核、16 GB、Arch Linux。论文没有在本仓库提交这些代码或可复现实验数据，本页不把实现版本当作本仓库证据文件。

作者明确的适用范围是 R||Cmax 与“预测重作业部分分配”。不能把保证自动迁移到相关机、同机、在线调度、其它目标（总完工时间、加权和等），也不能把实验中“低于基线”写成严格最坏情况比 2 更强的无条件比率。经典背景引用 Lenstra–Shmoys–Tardos 1990 的 2-近似与固定机数 ((1+\varepsilon)) 方案，以及 Shmoys–Tardos 1993 舍入；这些引用仅作论文来源，不是本轮逐一重新取得的外部文献对象。

## 与本档已有材料的关系与接续

- 与 `archives/unrelated-machines/问题--问题.md`：共享 R||Cmax 的调度定义和 LST/重轻分解背景；本页额外引入预测、错误量和局部重作业搜索，不能据此把一般无预测 (2-\varepsilon) 问题视为已解。
- 与 `archives/unrelated-machines/state/资源/文献源目录登记检查点--资源.md`：后者只证明文献源目录 checkpoint 的工程范围测试，本页提供实际 PDF 数学内容；两者不能互相替代。
- 与本档现有配置/菜单、单位读出和 Santa 资源对象：目标函数、输入结构和量词不同；没有从这些对象推导任何边，也不把学习增强论文当作其近二障碍的证明。
- 可能的第三阶段关系：可建立“来源”边到问题页和 R||Cmax 经典基线对象；若要建立“方法/推广”边，必须另行解释预测局部化如何对应本档某个具体重作业搜索对象，不能只凭相同关键词造边。

## 处置结论

- **对象类型**：文献/资源，保留完整论文身份与数学结论。
- **真值与完成度**：论文内 Theorem 5.1、5.2、D.1、D.2 及其证明在该论文给定模型内作为“论文声称且正文含证明”的条件结论保存；数值实验作为有限实验保存，不升级为定理。
- **独有内容去向**：预测为部分机器分配、(T)-重投影、至多 (K) 增量、离散阈值外层搜索、假阴性/假阳性分解和可编辑预测变体均只在本页整理；原始 PDF 仍由 source 清单保全。
- **未覆盖缺口**：没有独立复现代码、没有外部同行评审状态核验、没有把该算法接入本仓库的非相关机问题实例，也没有把其保证推广到本档其它模型。
