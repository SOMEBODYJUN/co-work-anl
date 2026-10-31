---
id: customer-attraction/actual-prefix-incidence-budget-and-pb-reachability-review
kind: review
type_tag: 审查
title: 实际前缀的关联预算与PB背景可达性复核
status: complete-conditional-prefix-obstruction-and-internal-review
truth_status: exact-catalogue-and-background-reachability-obstruction; no-general-half-conclusion
review_level: full-parent-review-and-proposer-source-read; exact-integer-comparison
scope: 单位客户完整历史纯SPE，目录满足所列R/D关联假设；固定前缀负载及剩余人数；PB仅原目录/原背景
summary: 最后D单例角色的规定收益被1/B封顶，而合法R主题有跨全部真后继的统一分母下界；两严格不等式排除精确背景成为实际均衡前缀。合法离轨/任意背景子游戏仍不受此否定。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-105f776c3e6d4a22bb7c380c5df8edc7/parent/root_reachability_review.md
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-105f776c3e6d4a22bb7c380c5df8edc7/parent/root_reachability_review.md
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-105f776c3e6d4a22bb7c380c5df8edc7/credible_attack/root_reachability_incidence_budget.md
---

本对象完整读取1722B父方解析复核，并实际读取其6852B提出者原稿。复核是在读作者证明后核对，不称盲审、外审或新颖性认证；提出者稿只作此批必要比较，不额外记其source done。这里排除的是精确背景在精确目录中成为实际SPE前缀，不否定它作为合法离轨历史或固定背景子游戏。

## 一般条件引理与证明

客户宇宙有限且分为非空R、D。D-singleton指目录中恰{ x }、x∈D的主题。给正整数α,a,q，要求每个主题或者是D-singleton，或者至少含α个R客户；任何触及D而非D-singleton的主题至少含a个R客户；至少有一合法主题T含q个R客户。模型仍允许其他目录，但本条件引理不覆盖违反这些假设的新增主题（例如空主题）。

固定任意合法有序前缀h，负载b，后面还剩r位。定义
\[
I=\sum_{x\in R}b_x,\qquad \beta=\max_{x\in R}b_x,\qquad B=\min_{x\in D}b_x.
\]
若
\[
B>I/a,\qquad qB>\beta+\lfloor I/\alpha\rfloor+r+1,\tag{RB}
\]
则h不能是任何完整纯SPE的实际前缀。该结论同时量化所有实现同一负载b的有序历史，允许全部历史依赖平局。

若h没有D单例，则固定任一D客户的每次覆盖至少消耗a个R关联；它的覆盖次数≤I/a，与bₓ≥B矛盾。取h最后一个D单例角色i，其主题{x}，之后h内有L个非D单例行动，各贡献至少α个R关联，故L≤⌊I/α⌋。该角色原规定终局收益≤1/bₓ≤1/B。

在i之前的实际R负载逐客户≤β。令i改选合法T，然后允许所有后继任意改变行动：从i起还有L+r+1位，每个所选R客户最终分母至多β+L+r+1。因此该偏离的真实收益至少q/[β+⌊I/α⌋+r+1]>1/B，严格盈利。它不需要冻结follower、平均平局或可信威胁假设；任何真后继都不能挽回该节点IC。B>0由第一严格式保证，不除零。

## PB参数的准确应用

采用原round5 PB的同一目录、同一背景b和r=2475，分真实块客户R与dummy块客户D。原目录只含regular主题及真实/dummy单例；每个非D单例至少含一个R客户，故α=1；触D的regular主题在d=20段每段含一个12客户真实块，故可取a=q=240。这里只核该原目录合同和原数值，不认证添加其他主题或背景修改后的新构造。

| 参数 | 精确值 |
|---|---:|
| 段数d、块数Q、块重数M | 20，2063，10⁹ |
| dummy倍数H、剩余人数r | 100000，2475 |
| I=dQ(12M+1) | 495120000041260 |
| β=M+1 | 1000000001 |
| B=HM | 100000000000000 |
| aB=qB | 24000000000000000 |
| β+I+r+1 | 495121000043737 |

aB>I、qB>β+I+r+1都严格成立。因此原目录中任何实现该精确b的合法有序前缀都不能是还剩2475位的实际SPE前缀；不仅排除了字面“全部单例”的某一个实现。原任意背景SPE仍可在该合法离轨历史后成立，与本结论相容。更换目录、b或剩余人数，须重新检查(RB)。

## 同一实际叶的福利账与剩余缺口

另固定某实际前缀，H_b为已覆盖客户，J为续局首次覆盖客户，d为其续局负载。对同一实际完整叶，
\[
W=|H_b|+|J|,\quad
\sum_{\rm prefix}u_i=\sum_{x\in H_b}\frac{b_x}{b_x+d_x},\quad
\sum_{\rm tail}u_i=|J|+\sum_{x\in H_b}\frac{d_x}{b_x+d_x}.
\]
已覆盖支持是一份福利池，由前缀利润和尾部租金分配，不能删掉或记两次。对比较并集C，纯集合恒等式为
\[
|C|-2W=|C\setminus H_b|-|H_b|-2|J|-|H_b\setminus C|.
\]
原PB背景覆盖全客户宇宙，原实例因而本就没有正的根half亏损；(RB)又给独立的战略可达性障碍。这些不是任意可达背景的一般福利不等式。未满足(RB)的背景并未被排除，六人half仍需真实最优m主题约束、已覆盖福利及跨枝共同付款。

本批新程序执行0；参数核对为明确整数代数，完整证明为上述关联数与收益分母估计。原稿的“主目标OPEN”按一般/当前六人范围保留，不覆盖后续已证五人对象。原文、精确指纹及阅读/比较范围见[证据入口](../../tools/evidence/parent-review-and-frozen-audits/README.md)。
