---
id: customer-attraction/R105-deletion-blind-suffix-regret-boundary-review-20261031
kind: review
type_tag: 审查
title: R105 删除盲性、尾部预算与全历史 regret 边界审查
status: complete-source-read-integrated-with-open-half-boundaries
truth_status: auxiliary analytical inequalities and explicit boundaries; Q-CAG-HALF remains open
review_level: full-source-read-cross-comparison
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-105f776c3e6d4a22bb7c380c5df8edc7/independent_general/background_deletion_blind.md
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-105f776c3e6d4a22bb7c380c5df8edc7/independent_general/background_deletion_blind.md
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-105f776c3e6d4a22bb7c380c5df8edc7/independent_general/suffix_deletion_corollary_blind.md
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-105f776c3e6d4a22bb7c380c5df8edc7/independent_general/suffix_deletion_corollary_blind.md
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-105f776c3e6d4a22bb7c380c5df8edc7/new_induction_repair/all_history_regret_and_reset.md
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-105f776c3e6d4a22bb7c380c5df8edc7/new_induction_repair/all_history_regret_and_reset.md
evidence_paths:
  - archives/customer-attraction/tools/evidence/R105-deletion-blind-reset-20261031/manifest.json
  - archives/customer-attraction/tools/evidence/R105-deletion-blind-reset-20261031/background_deletion_blind.md
  - archives/customer-attraction/tools/evidence/R105-deletion-blind-reset-20261031/suffix_deletion_corollary_blind.md
  - archives/customer-attraction/tools/evidence/R105-deletion-blind-reset-20261031/all_history_regret_and_reset.md
related_objects:
  - ../审查/R105交叉分支与regret修复障碍接续审查--审查.md
  - ../问题--问题.md

# R105 删除盲性、尾部预算与全历史 regret 边界审查

## 1. 三份来源的精确数学身份

background_deletion_blind.md 证明固定背景删除后的实际节点 regret 包络；
suffix_deletion_corollary_blind.md 把它沿实际路径求和得到 D/2 的重叠退款；
all_history_regret_and_reset.md 则说明仅有全历史 regret 范数也不能给 dimension-free half contract。
三者都是辅助分析，不关闭 Q-CAG-HALF。

## 2. 背景删除 lemma

固定完整计划 sigma，在背景 b+d 下为原 SPE，实际尾叶 q；删除 d 后仍沿 sigma。对真实节点 j 和强制主题 T，删除后的偏离收益差被分解为 deletion gain minus original IC slack。令

K_j=max_T sum_{x in T} d_x / [(b_x+p_j(x)+1)(b_x+p_j(x)+d_x+1)]

以及实际叶退款

E_d(q)=sum_{x:c_x>0} d_x c_x / [(b_x+c_x)(b_x+d_x+c_x)].

逐节点严格推导给出

sum_j R_j <= sum_j K_j - E_d(q).

关键点是实际离轨叶的后继允许改变；只使用当前主题覆盖至少 p_j(x)+1，不冻结 follower。每个 removal gain 对负载单调递减，因此 K_j 是有效上界。有限单位客户、空主题、重复主题和零客户都保留。

## 3. 尾部 corollary

删去实际提供者 i 后，固定实际前缀并保留其真实 suffix；对 j>i 得 R_ij。因为 S_i 是合法主题，K_ij 取精确的共同主题和。对每个客户 x 的 c_x 次实际覆盖，所有 i<j 覆盖对共给 1/[c_x(c_x-1)]，故总退款正好 D/2，其中 D 是最终被至少两次覆盖的客户数。

由单位背景整数性和 1/(b+1)<=1/2，得到

sum_{i<j} R_ij <= [(m-1)W-D]/2.

该不等式可用作尾部 regret 预算，但它只针对冻结前缀后的 suffix。对 i>1 的删除若要形成 m-1 人根游戏，早期提供者偏离时被删除角色的动作会重新响应，d 不再固定；这部分 recourse 没有被三角和消掉。即使 i=1，也要控制每个离轨历史的 credible suffix reset，实际路径预算不能自动替代全树预算。

## 4. 全历史 regret 家族与乘积 bound

对任意完整计划 tau，定义每层所有有序历史的最大 regret e_i，B=sum e_i。来源构造共同核心加花瓣主题族：实际 W=q+2、OPT=q+m，最后玩家在每个历史都是最佳回应，但中间玩家 regret 形成

e_i=1/(m-i)-1/(m-1),  B=H_{m-1}-1.

取 q=0 时 (OPT-2W)/B 趋于无穷，说明仅以全历史 regret 范数 B 付费的 dimension-free 常数 C 不存在。该族不是 SPE，也没有声明是 deletion replay；它只排除过强稳定 contract。

来源同时给出合法的 regret-weighted prefix product relation：

OPT_m <= [W+B]/F_m(m),

其中 F_m(m)=1-product_{r=1}^m(1-1/(rm))。该 factor 约为 m/H_m，不能满足 half。它是完整计划的无修复 transfer，不是一般 half 证明。

## 5. 结论边界

三源的共同结论是：删除实际路径的 regret 有精确退款恒等式，但缺少早期 recourse 和可信 suffix reset；全历史 regret 虽更强，也不足以产生固定半覆盖常数。可继续研究的正面方向是把删除后的真实离轨菜单、被删玩家利润和 reset 费用纳入共同支付；不能把实际路径 regret、冻结策略或 product bound 写成 Q-CAG-HALF 定理。

本批原件和 manifest 已保全；哈希、字节、控制字符和 git diff --check 通过。未执行 Git commit、push 或 clean done。
