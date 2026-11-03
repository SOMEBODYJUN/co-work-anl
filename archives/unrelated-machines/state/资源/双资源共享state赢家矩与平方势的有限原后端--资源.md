---
id: "unrelated-machines/two-resource-shared-state-winner-moment-original-backend"
kind: "resource"
type_tag: "资源"
title: "双资源共享state赢家矩与平方势的有限原后端"
status: "complete-primary-code-read-and-exact-old-run-reuse"
truth_status: "conditional-or-finite-backend-evidence-with-explicit-model-boundaries"
summary: "保两固定概率空间、共享helper state的单双资源事件乘积、11步CE及完整旧字节重放；无LP或全调度实现。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:tests/audits/unrelated_machines/multi_outer_request_winner_pair_backend.py#全文"
evidence_manifest: "archives/unrelated-machines/tools/evidence/um-following-actual-checks-primary/README.md"
---

主源1238fc8be70a78638988为9204B，SHA460679c82477934bcfdc3ad326f39dd0d0dd0baf7fa4fd75d02df015c7f6b2f0，全部Experiment方法、两个固定输入及输出实读。只导入itertools/json/Fraction，无研究程序依赖。[原件、两旧结果/真实root重放记录和完整新输入展开](../../tools/evidence/um-following-actual-checks-primary/README.md)保全。已有[后端有限审查](../审查/多outer双资源后端与tiny-home算法边界有限审查--审查.md)保存模型边界，本页具体说明数学事件和独有实现。

## 同一个helper只抽一个state

helper h有state概率α_hs，剩余质量为empty；有group i(h)、权w_h、在资源u的state系数p_hsu。非empty给每资源一个独立Bernoulli请求，**此原程序只有统一request_rate**，不是规范算法任意r_hsu的完整实现。每资源独立均匀抽一个priority rule λ；候选按λ_i(h)w_hp_hsu降序、(h,s)字典序破平局，只收p>0。真实获胜贡献为未乘λ的w_hp_hsu，加到所属group。

给单/双资源及指定rule/winner events，event_probability对每helper先对其一个shared state求和：若它为winner须选指定s并请求；若同一helper在两资源获胜，两个s必须相同。若其当前state是更早竞争者而未赢，要求相应资源不请求。条件于此**同一state**，各资源请求位独立；再乘helper之间的factor。不能给每个state或每资源另抽一个独立helper state。

fixed_states后其条件state概率置1；fixed_requests用0/1替原rate；fixed_rules后该rule概率1。不同资源pair才用两rule概率乘积，同资源二阶只用单winner平方。代码没有一般参数合法性验证产品；main的α、系数、groups、权与rules是明确有效的字面值。

## 一二阶矩与条件期望

写group i总值W_i=Σ_uY_iu。moments先枚举单资源rule/winner，累计E Y及E Y²；再枚举u<v、两rules和两winners，仅对同group乘积计2E(Y_iuY_iv)。所有事件概率按上一节同state因式分解，不枚举指数profiles。

brute另直接枚举每helper的(state,各请求bits)，再枚举各资源rule，从真实请求者中按rank取winner，重算全部W_i、均值、二阶和总概率。它不调用event_probability作oracle。两方法返回的均值/二阶必须精确相等。

CE先冻结原μ_i=E W_i，势为Σ_iE[(W_i−μ_i)²]。依次固定3个helper state/empty、6个请求位、2个资源rule，共11步；每一步试原条件下可行分支，调用moments算精确势，选最小者，核不增。empty helper的请求只选0。全固定后用**实际请求者**求W，不把未请求state重新加入候选；末态moments为W与W²，末势恰Σ(W−μ)²。源码只输出步数和端点势，不输出完整11步决定/势轨迹；新文档的兼容值见证不冒作旧CE transcript。

## 两个完整实际输入及结果

共有3helper、2group、2state/helper、2resource、2rule；groups=(0,0,1)，w=(1/2,1/2,1)，rules=(1/3,2/3)及(2/3,1/3)。三helper的两state系数依次为[(3/4,1/4),(1/4,3/4)]、[(1/2,1/2),(1,0)]、[(1/3,2/3),(2/3,1/3)]。

| α每state / 请求率 | 完整outcomes | μ | 二阶 | 初势→终势 | 最终实际值 |
|---|---:|---|---|---|---|
|1/2 / 1/3|2048|(137/576,371/1296)|(13565/124416,761/3888)|4467527/26873856→565057/26873856|(3/8,1/3)|
|1/4 / 1/2|2916|(799/4096,685/3072)|(5917/65536,1547/9216)|25725607/150994944→8248921/150994944|(1/8,0)|

第二例empty概率1/2，确有一个group终值0。两例均不满足tiny-domain/均值前提，不能据0值攻击规范定理，也不能把该后端PASS当整个调度算法实验。

## 真实运行与版本边界

19575…旧stdout SHAe7433…与3743…root记录双绑定本当前代码SHA，root新目录原CLI重放exit0且作者输出逐字相同。root参与denominator/request-coin caveat，不能称作者之外零信息盲审。本批原main新run0；新增独立数据从全部字面参数直接重算4964outcomes、同均值/二阶及端点势，并为两个旧final_values找兼容概率态，注明不是历史CE决定，也没有重做11步CE。

规范v1是Q-alone、single-state outer、互异homes、k⁴-tiny、共享fallback的数学19/10算法，包含必要SA1、MW、方差、CE和全原job回填。此程序没有生成/解LP、MW、tiny输入、一般方差证明或ordinary UM全assignment。当前canonical后来另附v4 k²/UD-leaf和v5 O(1/k)域；本资源只完整比较旧§1–11及各后续版本范围说明，不认证新算法证明，更不把旧后端软件倒填成它们的实现。一般UM、外审和新颖性保持原状态。
