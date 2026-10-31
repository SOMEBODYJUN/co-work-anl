# 数学逐项自查

以下20项是本次解析自查及旧输出有理算术，不是新游戏/激活/排列扫描；两次原入口另有完整状态。

1. DAG每边时间严格未来、每行后继按时间且无重复角色；不同query标签保留，不将3a/3b合成一个状态。
2. word权重为每具体word的$p^k(1-p)^{6-k}$，无需再乘组合数；9×64遍历含owner inactive，非零注入word每source32。
3. entered除p后是q，吸收除p后积分；不能把q当无条件arrival，p=0仅可去端点。
4. owner-conditional Markov第r后继概率$p(1-p)^r$，absorb$(1-p)^k$，和1；r按时间不是priority。
5. merge q可加，是因为同一word路线唯一、各前缀进入事件互斥；未来未暴露支持转移，adaptive全world不继承。
6. initial q1吸收积分1/c；nonowner q≤p给1/[c(c+1)]，不是另乘一次owner注入。
7. 报告9个source吸收总量1；33正格由9initial+24nonowner组成，48零格仍逐格比较。
8. 18个后续role入口检查仅17个正和、1个零和；同role多个query应合后用半界。
9. source0 q1b=p，q2a=p²，q3a=p−p²+p³，q3b=p²−p³；3a/3b entry合1/2，abs合1/12。
10. source0到1b c4吸收1/20恰Beta2；这是定义图非零传播，不包含收益分母或共同钱包。
11. priority中rank越大越高；source owner与future角色不同，代码>=与严格>等价，最早active仍按时间。
12. 条件Uowner=t后p=1−t，unit-world吸收等∫conditional-owner dp=∫unconditional dp/p；不同owner不共一个阈值。
13. 6!×9=6480路由、9×9=81边际；不校对joint moments、entry或role bound，均不认证真实SPE。
14. OFFIC三个叶A/B/W在同一原完整历史策略；g处规定a才给ell≥0，actual-prefix另给e≥0，owner-return不自动合格。
15. u−D=(u−vS)+(v−D)−ell；T_C符号可变，负ell保留，全部fresh域不缩到tracked。
16. cA=1+|U|、cB=b+1+|V|给signed FRESH；tracked真父保b≥1，故每recipient d=(1/cA)/cB≤u_j(A;x)/2。
17. θ为原整体非负常数，H/v≤θ/2只按同recipient聚合；完整IC方向是(H/v)d_query≤H，不能反向付已有H。
18. 同actual-query s的A相同，多父θ_g可相加；不同A/recipient不自动共一actual容量，0利润时H0且比值置0。
19. x吸收仅令F_s(x)低于owner_x阈值；whole-IC广播到y不保F_s(y)标签，即便b_y≥1。没有从半系数推出全tracked收缩。
20. R-only固定Gamma owner总下界/SOURCE预付与rankwise随机winner合同不同；定义图无这些资金字段。后来full-profit fresh/SAFE/M−H各自域不能拼为一般V≤W，五人已证与六人开放分开。
