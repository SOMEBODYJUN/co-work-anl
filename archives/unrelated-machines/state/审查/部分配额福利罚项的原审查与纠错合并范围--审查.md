---
id: "unrelated-machines/partial-quota-welfare-original-review-merged-scope"
kind: review
type_tag: 审查
title: "部分配额福利罚项的原审查与纠错合并范围"
status: complete-primary-read-and-mathematical-reconstruction
summary: "给定部分正support见证的W−δA精确确定化与高组计数，原Exact-first/15定向与完整冻结audit分开，保gamma后纠错和软件q>0。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/reviews/unrelated_machines/normalized_menu_partial_quota_welfare_review.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/reviews/unrelated_machines/normalized_menu_partial_quota_welfare_review.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/current/unrelated_machines/explicit_xos_fractional_nsw_and_normalized_robust_gap_boundary.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/current/unrelated_machines/explicit_xos_fractional_nsw_and_normalized_robust_gap_boundary.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:evidence/runs/unrelated_machines/normalized_menu_partial_quota_welfare.json"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:evidence/runs/unrelated_machines/normalized_menu_partial_quota_welfare.json"
evidence_manifest: ../../../../tools/evidence/um-following-review-primary/source-manifest.json
---

# 独立身份、实际读序与合并更正

主源a0ffc0bf14eee80c5fce全文9313B/80行已读；current e7736babc411473bec2a全765行在前批实际读并核SHA9ef11b3f…a33c后复用原字节，本批另核F2/相邻语境。仅处理UM-NORMALIZED-MENU-PARTIAL-QUOTA-WELFARE-FLOOR-v1，不重审A–E NSW或调用其常数。

logic_audit先仅full-row陈述独立福利/CDF，再仅subprobability陈述独立发现W−δA必要，发出两次重构后才读作者F2。最初全页89cbe7…、状态修句后bc077ba1…；审者只读F2、原E/F相邻和首尾状态，不签旧NSW。原审查一度说旧F不排γ≤δ；2026-10-19 root append已明确撤回高/低γ混用，旧段只能按γ_lo与高组β分别理解，不给γ_hi=γ_lo背书。

append将合并全页绑定9ef11b3f…a33c，报告F2历史section hash8972edd5…。本轮全页hash确实相同；按明确字节“## F2.”起到“## 来源分工”前的切片117行，hash为a6be77b334b34e17ac2e7a8bf9895849f297892a6b875bfc73204d9bac8f779f。未取得历史切片规则，不冒称复现8972，也不据该不明边界断言数学有差异；原作者/root合并记录与本轮验证边界分别保留。

# 给定部分LP与自足福利计数

n≥1显式groups，每组非空indexed states，p≥0二进制有理、每state全U和1。原quality f_g(B)=max_sΣ_Bp∈[0,1]，bundles跨组不交。给有理0<q≤n及λ≥0，a_g=Σ_sλ_gs≤1、Σa=q、每资源Σ_(p>0)λ≤1。列按正support而非p加权；允许零λ/整行inactive、零项、重复states、unused资源。

每group按λ选state、剩余1−a选inactive，组间独立；active对item出原p的bid。W=Σitem maxbid、A=active数。阈值t>0的总请求z(t)≤1，故Pr(maxbid≥t)=1−Π(1−r_g)≥1−e^(−z)≥(1−1/e)z。有限层求和、norm1给EW≥(1−1/e)q和EA=q。

实际A可能>q，不能只去随机化W再把A当q。对给定有理δ取Φ=W−δA，逐group枚举正概率state/inactive并取最大精确条件期望，最终Φ≥(1−1/e−δ)q。每item有限bid levels用Σ_ℓ(t_ℓ−t_(ℓ−1))[1−Π_gPr(bid<t_ℓ)]，固定group CDF为0/1，未定含inactive及state概率。没有计算e或Bayes除tiny prefix，概率分母乘积bits多项式。

每positive bid item给一最高active bidder，ties固定，零bid闲置。chosen-state质量w_g≤1，inactive空bundle；再遍历原表取真attaining state，f_g(B_g)≥w_g（该state无需λ>0）。低于δ的真实质量组贡献w_g−δ≤0，其余active贡献≤1−δ，故
\[
H_\delta=\#\{f_g(B_g)\ge\delta\}\ge
\frac{1-1/e-\delta}{1-\delta}q
\quad(0<\delta<1-1/e).
\]
δ3/8时e>65/24>8/3给Φ>q/4、H>2q/5。strict号需q>0，不需q整数。理论q0可返回空但不套strict；规范软件只收q>0。

YES有r≥q个unit groups时，norm1 attaining state全部positive support必须在bundle内，给各这些states λ=q/r即得LP。固定0<β≤3/8，NO若每allocation的H_(3/8)<βq，则LP可行将矛盾H>2q/5≥βq。因此给定显式promise可只用LP可行性分离；一般δ,β充分域δ+(1−δ)β<1−1/e是证明常数域，程序不执行超越数比较。LP不可行仅否定该源YES，不是一般UM可靠FAIL。高组比例β、组数q和旧γ_lo不混；不保所有组常数质量或全部mandatory selectors次二。

# 原review实际核验与完整audit报告分开

历史审者独立inline Fraction枚举full-row1440、subprobability27648例，固定两组/三资源、每组singleton或等权pair；full-row概率1/4、1/2、3/4及其补，subprobability的λ坐标0、1/2、1；另q=1/10^200，分母665bits。它不是规范源码完整audit，也不是本轮执行。

审者实际全文读源码ee41f5fd…e53，导入精确文件对五类输入各δ1/10、3/8、3/5，共15次定向：共享singleton、独立资源且实际A>q、整行零激活、q1/10^200且权1/7与6/7、重复states。独立重算attaining值/CDF oracle；δ3/8核strict。他没有跑规范完整audit或读冻结JSON。validate拒float/bool/负/非norm1/无效列/零q，inactive输出state0在空bundle上真attaining；这些是原review实际范围，本轮未重跑或冒全文读源码。

本轮另全文读5b8edefb22e5a2e189ac的266行冻结报告：3536 feasible（3528枚举接受加8边界fixture）、5696枚举candidates、2168 over-capacity、86912 joint-action visits、42418 prefixes、19非法拒绝、8边界。完整有限域n1/2、m1..3、每组两个ordered states（duplicates保留）、权0、1/2、1，θ∈{1,1/3,1/2,5/6}，每态概率θ/2/inactive1−θ，δ3/8；没有随机采样。报告tiny_q=1/(2^257+1)不同于review的1/10^200，不混样例。该报告不是审者亲执行范围，也不替代全称证明、LP后端或一般排程器。

Feige公开原刊摘要支持标准XOS福利1−1/e背景，历史审者未读全文证明；原B已有最高出价CDF，F2是直接计数推论，新颖性未认证。本轮无外部PDF/新程序运行。软件状态修句只把“未实现”限原A–F，另列F2实现，不改变旧数学。高低γ互补纠错按后append生效；原review旧句不继续流通为无条件边界。
