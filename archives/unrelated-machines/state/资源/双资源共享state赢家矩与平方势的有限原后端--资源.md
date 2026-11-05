---
id: "unrelated-machines/two-resource-shared-state-winner-moment-original-backend"
kind: "resource"
type_tag: "资源"
title: "双资源共享state的矩计算与条件期望证书"
status: "exact-finite-certificate-with-explicit-scope"
truth_status: "finite-inputs-and-explicit-algorithm-interface"
summary: "同一helper共享状态下的单双资源事件公式、11次条件固定与两个精确概率输入。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:tests/audits/unrelated_machines/multi_outer_request_winner_pair_backend.py#全文"
evidence_manifest: "archives/unrelated-machines/tools/evidence/um-following-actual-checks-primary/README.md"
---

# 共享状态的双资源矩计算

## 同一个helper只抽一个state

helper h有state概率α_hs，剩余质量为empty；有group i(h)、权w_h、在资源u的state系数p_hsu。非empty给每资源一个独立Bernoulli请求，**此原程序只有统一request_rate**，不是规范算法任意r_hsu的完整实现。每资源独立均匀抽一个priority rule λ；候选按λ_i(h)w_hp_hsu降序、(h,s)字典序破平局，只收p>0。真实获胜贡献为未乘λ的w_hp_hsu，加到所属group。

给单/双资源及指定rule/winner events，event_probability对每helper先对其一个shared state求和：若它为winner须选指定s并请求；若同一helper在两资源获胜，两个s必须相同。若其当前state是更早竞争者而未赢，要求相应资源不请求。条件于此**同一state**，各资源请求位独立；再乘helper之间的factor。不能给每个state或每资源另抽一个独立helper state。

fixed_states后其条件state概率置1；fixed_requests用0/1替原rate；fixed_rules后该rule概率1。不同资源pair才用两rule概率乘积，同资源二阶只用单winner平方。下面两个输入的α、系数、groups、权与rules是明确有效的有理数。

## 一二阶矩与条件期望

写group i总值W_i=Σ_uY_iu。moments先枚举单资源rule/winner，累计E Y及E Y²；再枚举u<v、两rules和两winners，仅对同group乘积计2E(Y_iuY_iv)。所有事件概率按上一节同state因式分解，不枚举指数profiles。

brute另直接枚举每helper的(state,各请求bits)，再枚举各资源rule，从真实请求者中按rank取winner，重算全部W_i、均值、二阶和总概率。它不调用event_probability作oracle。两方法返回的均值/二阶必须精确相等。

CE先冻结原μ_i=E W_i，势为Σ_iE[(W_i−μ_i)²]。依次固定3个helper state/empty、6个请求位、2个资源rule，共11步；每一步试原条件下可行分支，调用moments算精确势，选最小者，核不增。empty helper的请求只选0。全固定后用**实际请求者**求W，不把未请求state重新加入候选；末态moments为W与W²，末势恰Σ(W−μ)²。源码只输出步数和端点势，不输出完整11步决定/势轨迹。

## 两个完整实际输入及结果

共有3helper、2group、2state/helper、2resource、2rule；groups=(0,0,1)，w=(1/2,1/2,1)，rules=(1/3,2/3)及(2/3,1/3)。三helper的两state系数依次为[(3/4,1/4),(1/4,3/4)]、[(1/2,1/2),(1,0)]、[(1/3,2/3),(2/3,1/3)]。

| α每state / 请求率 | 完整outcomes | μ | 二阶 | 初势→终势 | 最终实际值 |
|---|---:|---|---|---|---|
|1/2 / 1/3|2048|(137/576,371/1296)|(13565/124416,761/3888)|4467527/26873856→565057/26873856|(3/8,1/3)|
|1/4 / 1/2|2916|(799/4096,685/3072)|(5917/65536,1547/9216)|25725607/150994944→8248921/150994944|(1/8,0)|

第二例empty概率1/2，确有一个group终值0。两例均不满足tiny-domain/均值前提，不能据0值攻击规范定理，也不能把该后端PASS当整个调度算法实验。


[原程序、完整输入及端点证书](../../tools/evidence/um-following-actual-checks-primary/README.md)保留实际有理数据；[规范后端数学](../审查/多outer双资源后端与tiny-home算法边界有限审查--审查.md)说明另需的tiny-domain和均值前提。此程序不含LP、MW或全部原调度回填。
