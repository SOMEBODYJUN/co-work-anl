# 同行第七轮初始化与静态匹配：接续和去重

2026-10-24。root在收到seq249/253后实际读取同行第七轮正文，并重新组织一般攻击。Q-CAG-HALF仍OPEN。本页不登记新反例或新福利界。

## 仍可使用的初始化

[最优坐标初始化](../../R-cd789330fc7141299ac491bbb3ffa420/round7/parent/optimal_coordinate_initialization.md)保留每个比较客户一单位库存，付出current金额d_l≤u_l与固定父叶共同列H_l≤u_l，未来来源总量b_i留在真实future边上。其承重目标仍是存在最优T、合法剪枝及路由，使

    A_l^out≤2u_l−d_l−H_l。

已付两份W不意味着未来源可再免费领一份W。主线程与五个可接续分支实际继续攻击这项剩余及直接净覆盖关系；原price线程续接调用返回thread limit，未宣称该调用已执行。

## FOMA-EXISTS不是新的开放正面桥

同行 [冻结最优指派稿](../../R-cd789330fc7141299ac491bbb3ffa420/round7/transport/frozen_optimal_assignment_working.md)将存在最优T及匹配使K≤W标为OPEN。direct检索到旧同量词反例，root实际读正文并重跑原独立审计，确认应为FALSE。

原正文：[最优静态匹配反例](../../R-a0bb57fa24044a8794bc7991918a19c6/static_matching/optimal_static_matching_counterexample.md)。原独立审查：[定义级审查](../../R-a0bb57fa24044a8794bc7991918a19c6/direct_global/static_matching_counterexample_independent_review.md)。52单位客户、6个不同共同主题、m=4，完整259节点策略实际为(3,3,2,2)，每人47/4，W=47。唯一最优支持为0145，OPT=52。全部24个最优匹配中12个K=48，12个K=293/6；故minK=48>47。

root本轮复跑了原独立实现的1554个含自身IC及1296有序终局，输出 [old_static_matching_replay.json](old_static_matching_replay.json)。复跑复用旧代码，不算又一份独立实现或新反例。可重现入口 [replay_old_static_matching.py](replay_old_static_matching.py)写入本人目录，不改原作者证据。

原旧正文已经给出更弱充分候选K≤(1+1/m)W，因为无条件OPT≤K+(1−1/m)W。弱式仍需真正证明，不认领新候选，也不能由本例或有限未分离推真。本轮强式去重不否定坐标初始化、RESIDUAL-CAP、ADM?或half。
