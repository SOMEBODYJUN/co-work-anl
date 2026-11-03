---
id: customer-attraction/pair-crossed-reply-three-lp-probes-and-normalization-correction
kind: computation
type_tag: 计算
title: 双查询交叉回复的三份有限LP与归一化纠错
status: complete-source-replay
truth_status: floating-finite-necessary-relaxation-only
review_level: full-three-program-reading-and-local-replay
scope: 八标签255非空兴趣类型；每次固定统一背景b=0、1、2；34行或50行局部必要约束
summary: 三份探针保留局部curl负值及税系数1的数值边界，纠正branch_cov实际为两枝并集覆盖的一半；无完整SPE认证及有理最优对偶。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-c8ca54e5f2854c2c93bf83abc2f24f5c/n5/fresh_proof/pair_curl_probe.py
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-c8ca54e5f2854c2c93bf83abc2f24f5c/n5/fresh_proof/pair_curl_tax_probe.py
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-c8ca54e5f2854c2c93bf83abc2f24f5c/n5/fresh_proof/pair_curl_tax_full_worst_probe.py
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-c8ca54e5f2854c2c93bf83abc2f24f5c/n5/fresh_proof/audit_crossed_reply_tax.py
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-c8ca54e5f2854c2c93bf83abc2f24f5c/n5/fresh_proof/crossed_reply_tax_audit.json
---

# 双查询交叉回复的三份有限LP与归一化纠错

## 原程序的实际域

八个合法标签依次为a,b,r,s,p,q,k,l，四条指定局部枝为(a,r,s)、(b,p,q)、(a,p,k)、(b,r,l)。每个非空八位mask是客户兴趣类型，允许255个类型的任意非负连续质量。一次LP中每个客户的旧负载都是同一个固定整数b_g∈{0,1,2}；这些LP不枚举不同客户的异质背景。

令u(A;B,C)=Σ_x1_A(x)/(b_g+1+1_B(x)+1_C(x))。基础必要矩阵有两条首后继交叉偏离IC：u(r;a,s)≥u(p;a,k)、u(p;b,q)≥u(r;b,l)；另对四个列出末节点各比较全部八个合法标签，共32行，合计34行（含选定动作的恒等行）。它没有指定其他首后继偏离的真实末回复，没有根IC，也未补全所有有序历史。

目标curl为

\[
 C=u(a;r,s)+u(b;p,q)-u(a;p,q)-u(b;r,s).
\]

`pair_curl_probe.py`分别用平均查询大小、平均真实查询收益、名为branch_cov的量和全部质量归一化为1。均由SciPy/HiGHS浮点优化，再打印非零支撑及若干浮点对偶；无Fraction恢复或精确全行/最优性认证。

## branch_cov的实现纠正

原表达式把两个NumPy布尔数组直接相加，布尔加法仍是布尔OR。因此实际量为

\[
 \tfrac12\mathbf1_{x\in a\cup r\cup s\cup b\cup p\cup q},
\]

并非变量名暗示的“两条枝覆盖数之平均”。只有两个布尔数组先各转成数值再相加才会得到后者。原字节保持；本页按实际实现解释原输出，没有改程序后把结果冒称原程序。仅被k或l覆盖的类型也在255变量中，只是不进入这一归一化。

一次原字节重放的浮点最小curl如下（数值约列，不是有理最优证书）：

| b_g | 平均查询大小=1 | 平均真实query收益=1 | 实际branch_cov=1 | 总客户质量=1 |
|---:|---:|---:|---:|---:|
| 0 | −1.3333333333 | −4 | −0.5217391304 | −0.2608695652 |
| 1 | −0.5 | −2 | −0.1724137931 | −0.0862068966 |
| 2 | −0.2666666667 | −1.3333333333 | −0.0856269113 | −0.0428134557 |

## 私有税归一化及粗保底加强

另两程序用

\[
 T=\sum_x\left[{1_r(1-1_s)\over(b_g+1_a+1)(b_g+1_a+2)}
              +{1_p(1-1_q)\over(b_g+1_b+1)(b_g+1_b+2)}\right]
\]

归一化T=1，仍最小化C。`pair_curl_tax_probe.py`使用上面34行；`pair_curl_tax_full_worst_probe.py`另对两个原首后继、每个标签A加保底

\[
 u(r;a,s)\ge\sum_{x\in A}{1\over b_g+1_a(x)+2},\qquad
 u(p;b,q)\ge\sum_{x\in A}{1\over b_g+1_b(x)+2}.
\]

共有16条额外必要行，合计50行。该分母把末位视为最坏地覆盖当前查询的全部客户；真实末位可以更好，但不能凭它补齐完整续局。

| b_g | 34行、T=1时浮点min C | 50行、T=1时浮点min C |
|---:|---:|---:|
| 0 | −1.0000000000 | −1.0000000000 |
| 1 | −1.0000000000 | −0.8888888889 |
| 2 | −1.0000000000 | −0.8333333333 |

数值与[双后继交叉税引理](../引理/双后继交叉末回复的去相关税--引理.md)的两查询C+T≥0一致；引理的普遍证明由真实IC和势相消承担。本程序本身没有精确证成这些最小值，也不能把负C支撑称为完整SPE、合法根反例或六人half反例；其连续客户质量尚需有理化/整数克隆及全历史补全才可能成为游戏证书。

## 精确代数审计与证据

独立的`audit_crossed_reply_tax.py`不调用LP，以Fraction核b=0,1,2,3,4,10,100的全部64种相关会员模式，共448组两条恒等式及税/余项非负。它不声称逐客户三slack都非负；slack来自整体SPE。旧34单位fixture的36个交叉对另核三slack并得到冻结JSON完全相同的结果：Δ=−11/82、税5/2、和97/41、slack91/164、余项297/164。它只复用已知fixture，没有在该脚本内核整个策略。

[全部原字节、来源SHA](../../tools/evidence/crossed-reply-tax-and-exchange-primary/source-manifest.json)、[一次实际执行记录](../../tools/evidence/crossed-reply-tax-and-exchange-primary/replay/execution.json)及三个probe完整stdout保留支撑和打印乘子。当前对象的贡献是明确有限诊断域及原实现误标，不是把浮点线性松弛升级成定理或反例。
