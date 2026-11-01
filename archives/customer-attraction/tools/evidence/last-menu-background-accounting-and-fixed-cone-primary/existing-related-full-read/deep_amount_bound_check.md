# DEEP-CAP2：一个粗界与未付处

2026-10-24。按父方 [精确定义](../parent/terminal_amount_cap.md)，B 是完整 SPE
实际叶，W^alpha 是真实单次强制分支，j<i_alpha<=l，且 sender 金额只花一次。
本页不证明 DEEP-CAP2，不提供其真实 SPE 反例，也不是新 half 结果。

定义

    q_(alpha,j,l)=sum_(x in B_j intersect (B_l\W_l^alpha))
                      1/[c_B(x)c_alpha(x)].

求和客户实际被不同角色 j,l 同时覆盖，所以 c_B(x)>=2。旧角色 j 在真实
分支中仍选 B_j，故其分支利润为 p_j(W^alpha)=sum_(x in B_j)1/c_alpha(x)。
直接逐客户得到

    q_(alpha,j,l)<=p_j(W^alpha)/2.

把它与每个 sender 的 AMOUNT

    sum_alpha lambda_(alpha,j) p_j(W^alpha)<=p_j(B)

相乘求和，便有任意深度的无条件粗界

    sum_(alpha:i_alpha<=l) sum_(j<i_alpha)
          lambda_(alpha,j) q_(alpha,j,l)
      <=(1/2)sum_(j<l)p_j(B).                       (COARSE)

利润零时 q 同样为零，不发生除零。这个粗界甚至不需要 SPE；真实策略
量词只是保证用到的 W^alpha 恰为父方指定分支。它被父方每个 sender 的
精确 max_alpha q/p_j(W^alpha) 公式包含，不是另一份新机制。

若 sum_(j<l)p_j(B)<=4p_l(B)，COARSE 足够给 DEEP-CAP2 的该列。
一般目录与人数没有已证的这类 prefix/recipient 利润比约束。尤其不能从
sum p_j(B)=W 推出逐列 cap2，也不能将不同 sender 的实际高利润重复支付给
一个低利润 recipient。因此本界没有补齐 DEEP-CAP2 的承重部分。

本轮没有进行新的有限 DEEP-CAP2 搜索；任意合法叶即使分离了代数加强，
也不能当作父方真实续局候选的反例。
