# 末层多孩子金额归一：两倍列容量及一般未付接口

2026-10-24。个人工作稿。任意有限单位客户和共同目录、任意人数 m。
本页末层代数不使用 SPE；它尚未支付一般半覆盖。已完成父方自足证明、
[credible 独立重构](../credible/review_terminal_amount_cap.md)及
[independent 先重构后对稿](../independent/prefix_and_terminal_amount_review.md)。
无外审或新颖性认证。
前缀正价 q 的来源是既有
[同一孩子 prefix 回推](../../R-cd789330fc7141299ac491bbb3ffa420/round7/credible/joint_prefix_claim_pushback.md)。

## 1. 任意数量的真实末位孩子

固定任意完整叶 B=(B_1,...,B_m)。对每个分支 alpha，令
W^alpha=(B_1,...,B_(m-1),T_alpha)，T_alpha 是任意合法主题。
同一末位切点可以有多个不同的强制主题。记客户负载 c_B,c_alpha，
角色利润 p_j(B),p_j(W^alpha)。

对 j<m 取 lambda_(alpha,j)>=0，并假设每个 sender j 只有一份金额预算：

    sum_alpha lambda_(alpha,j) p_j(W^alpha) <= p_j(B).       (AMOUNT)

分支正价定义为

    q_(alpha,j,m)
      = sum_(x in B_j intersect (B_m\T_alpha)) 1/[c_B(x)c_alpha(x)].

所有求和客户均有 prefix coverer j，所以分母为正。则

    sum_(alpha,j<m) lambda_(alpha,j) q_(alpha,j,m)
      <= 2 sum_(x in B_m, c_B(x)>=2) 1/c_B(x)
      <= 2 p_m(B).                                          (TERMINAL-CAP2)

这是多个不同孩子共享同一个 B_m 钱包的关系，不是把单孩子 cap1 逐枝相加。

## 2. 自足证明与零利润端点

固定 j<m。对 x∈B_j，变更末位只可能使其负载增加一，故

    c_alpha(x) <= c_B(x)+1 <= 2 c_B(x).

逐客户相加有 p_j(W^alpha)>=p_j(B)/2。若 p_j(B)>0，由 AMOUNT 得
sum_alpha lambda_(alpha,j)<=2。若 p_j(B)=0，则 B_j 无正价值客户，
它的全部 q 为零，不需要除以 p_j(B)，也不限制没有意义的 lambda 总和。

现在固定 x∈B_m。若 c=c_B(x)=1，没有 sender 覆盖它，贡献为零。
若 c>=2，覆盖 x 的 prefix sender 恰有 c−1 个。在 q 中出现 x 的孩子
必定将末位从 x 移走，因此 c_alpha(x)=c−1。故 x 的全部贡献至多

    sum_(j<m:x in B_j) sum_alpha lambda_(alpha,j) / [c(c−1)]
      <= 2(c−1)/[c(c−1)] = 2/c.

对 x 相加即得 TERMINAL-CAP2。m=1 时 sender 集合为空；零客户、空主题
及相同主题标签去重均不影响证明。不存在从有限枚举推出一般性的步骤。

[coupling 的全人数完整 SPE 家族](../coupling/amount_cap1_family.md)使该
合同的列系数为 2−3/(n+1)，n>=3，因而这里的统一系数二不能减小。
它的实际福利等于最优福利，只检验本合同 sharpness；不是 half 反例。

## 3. 更深真实分支是不同候选

固定完整 SPE sigma 的实际叶 B。现在分支 alpha=(i_alpha,T_alpha) 可以
在任意位置 i_alpha 强制，然后沿同一 sigma 继续，得真实叶 W^alpha；
W^alpha 与 B 在 i_alpha 之前一致。对 j<i_alpha 保留同一 AMOUNT，定义

    q_(alpha,j,l)
      = sum_(x in B_j intersect (B_l\W_l^alpha))
          1/[c_B(x)c_alpha(x)] ,  l>=i_alpha.

待判别的全范围候选是：每个 l 是否总有

    sum_(alpha:i_alpha<=l) sum_(j<i_alpha)
        lambda_(alpha,j) q_(alpha,j,l) <= 2p_l(B).           (DEEP-CAP2?)

本页没有证明它；末层证明中“负载至多增加一”和“c_alpha=c_B−1”在深层
都可能失效。真正要用到全部真实后继 IC，不能把任意合法叶代替真实续局。
即使 DEEP-CAP2 成立，还必须证明一般覆盖债务能按 AMOUNT 输入且没有
既有 direct/suffix claim 的重复占款；不能据一个系数二就宣布 half。

另外，AMOUNT 已成立时，合计所有 recipient 的正价金额不超过同一份
sender 实际利润和，是既有 POSITIVE 的基线推论；见
[条件源池及保留项](../harmonic/positive_source_pool.md)。因此逐列 cap2
的用途若有，应是保留下一轮完整 IC 的密度合同，而不是创造额外总金额。
原覆盖债务的 AMOUNT 初始化仍须另证。

## 4. 本轮定义级有限攻击及限制

[check_amount_cap.py](check_amount_cap.py)读取既有完整策略证书，先从
全部有序历史按定义核验所有行动比较，再从实际前缀生成全部单次强制分支。
对给定 sender j 和 recipient l，AMOUNT 允许的最坏金额通过闭式

    p_j(B) max_(alpha:j<i_alpha<=l) q_(alpha,j,l)/p_j(W^alpha)

精确求得。利润为零时 q 为零，省去该项；不允许隐含除零。不同 j 的预算
独立，所以对 j 求和正是这些已固定分支的最大正价。该最大化只针对固定
输入实例和策略，不是求所有 SPE，也不是证明 DEEP-CAP2。

本轮输出在 [amount_cap_existing.json](amount_cap_existing.json)：仅核查仓库
已有且输入文件可对应的完整证书，未出现 cap2 反例。不以阴性提高真值，
不继续扩大这批旧锥。另实际运行零客户、单主题、重复覆盖及空主题偏离
四类边界，均通过；主目标仍 OPEN。
