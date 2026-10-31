# 共享外端四任务 query/return 环：候选 Exact v1

提出者：rank_deficiency_fee，2026-10-18。仅冻结完整实际矩阵与精确陈述，供 root 决定是否安排新的 Exact-first 审查；本文件没有一般证明。对象是标准交替 matching 环的带权版本，不申请新 matching 理论或困难性结论。仅写 clone 外 scratch。

## 1. 完整实际矩阵、参数与边界

给任意二进制有理 ε，0<ε<1。全部原任务恰为四件不同jobs q₁,q₂,b₁,b₂，A=∅。内部机器H,I；外部机器E₁,E₂。完整矩阵如下，所有∞均不可执行：

| 原job | H（internal） | I（internal） | E₁（outside） | E₂（outside） |
| --- | --- | --- | --- | --- |
| q₁ | 1 | ∞ | 1 | ∞ |
| q₂ | 1 | ∞ | ∞ | 1 |
| b₁ | ∞ | 1 | 1 | ∞ |
| b₂ | ∞ | 1−ε | ∞ | 1 |

没有预载、守卫、其它任务、任务副本或资格。每个原job只整件执行一次。E₁真实共享q₁与b₁，E₂真实共享q₂与b₂；这两机的实际负载计入全局makespan。I上不同原job的处理时间不同，均为正。

内部模式按H∪I的实际目的地集合定义：

* aligned₁：内部{q₁,b₂}、外部{q₂,b₁}；
* aligned₂：内部{q₂,b₁}、外部{q₁,b₂}；
* inactive：内部{b₁,b₂}、外部{q₁,q₂}；
* cross(2,1)：内部{q₂,b₂}、外部{q₁,b₁}；
* cross(1,2)：内部{q₁,b₁}、外部{q₂,b₂}。

对其它任意内部子集，也按这同一完整矩阵执行全部四件原jobs；外部端没有被私有化。

## 2. 待审精确结论

1. 两aligned模式都有完整实际峰恰1的调度：

   * aligned₁：q₁→H，b₂→I，q₂→E₂，b₁→E₁；
   * aligned₂：q₂→H，b₁→I，q₁→E₁，b₂→E₂。

2. inactive模式的完整实际最小makespan精确为2−ε。两个cross模式的完整实际最小makespan均精确为2。

3. 对**每份全部四件原jobs的完整实际调度σ**，若C(σ)<2−ε，则σ必恰为上面两份aligned调度之一。不只有排除列出的三种bad模式；零query内部、两个queries内部及其它任意边界子集也没有遗漏。

4. 因而对任何1≤B<2−ε，全部≤B实际调度恰为两个aligned见证。每个实际低负载解可通过原q₁/q₂的目的地直接解码其唯一索引，不需已有optimum witness或hidden source解。该完整矩阵OPT恰1。

5. 对每个有理δ∈(0,1)，显式取ε=δ/3、B=2−δ，就给两aligned strict1、全部非aligned完整调度峰>B的near2局部接口。规模固定四机四任务，有理编码位长O(bitlen(δ))，无参数数值展开。

## 3. 准确范围与未完成义务

这满足实际共享outside负载下的局部身份合同，outside机器恰两台、无free forced preload，全部aux要求因A空而为空。它不反驳machine-uniform localA交换，后者不承诺此种共享outside的全局扩展。I上的异权不是本例承重，ε=0的unit环也有同类关系，故不把它包装成异权medium一致性的新机制。

两个strict见证的四台机器均被占用；原job身份不同但机器presence相同。没有实现可供任意其它query读取的空闲slot，也没有证明可把E₁/E₂随意识别为已有变量环/锁定机器后仍保YES。任意共享、级联、clause读取或source嵌入必须重新给完整矩阵、全部原jobs的YES及全NO decoder。

本候选只是边界对照：真实外部共享可以阻断内部matching交换的全局扩展。未给NP-hard源、任意规模一致性放大、费用摊销或near2 hardness；不是对一般UM的算法或反面。若该标准交替环没有后续接口价值，不宜单独登记新研究ID。
