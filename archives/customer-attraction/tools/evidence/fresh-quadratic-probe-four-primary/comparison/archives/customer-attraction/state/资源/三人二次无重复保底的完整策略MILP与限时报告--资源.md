---
id: customer-attraction/three-player-quadratic-fresh-full-policy-MILP-and-time-limit-report
kind: resource
type_tag: 资源
title: 三人二次无重复保底的完整策略MILP与限时报告
status: full-source-and-frozen-report-reviewed; bounded-root-attack-only; no-new-MILP-entry
summary: 3738B无guard源保所有fresh有序孩子策略和根0真实BI、每静态H存在query超过根1的MILP；原p5/B20是45秒无primal返回，不是不可行。0重跑旧搜索，相关gluing独审首次primary精确去重。
source_refs:
  - source:e4733ad4f22da750e6ec
  - source:4f72f94bc08205e91a0d
  - source:3e4e3534aa71467c11df
  - source:f1b1d787c8170500c3f4
---

## 四个主源与两种数学对象

817B探索README、3738B fresh_m3_milp.py、380B fresh_m3_p5_milp.json、3842B local_gluing_review.md总8777B均全文读。前三项归[独立对称二次fresh候选](../候选/对称二次无重复辅助博弈的逐人静态保底--候选.md)和本程序资源。第四是另一signed客户局部粘合审查，早先NT批只related、未done；现在首次primary，全部独有数学和审查先验已完整保存到[局部粘合障碍](../障碍/一致局部客户边际与全树激励的整数二次粘合缺口--障碍.md)、[固定人数整数行接口](../方法/整数二次客户行的固定人数收益接口--方法.md)及[原审计资源](整数二次粘合原审计与工作区元资料--资源.md)，因此精确duplicate，不再造第二障碍或重跑其旧原审计。

gluing审查先只读构造消息，后同日明确补读最终正文/原脚本/clock。它保proper总m与投影一致、全目录Q−1、全史常锚SPE/真同图和截断稀释；既不把整篇冒盲审，也不将signed half正余量称half分离。本批没有继承其旧actor/“不提交git”或探索偏好。

## CLI、模型域与变量

原3738B仅固定m3，参数p默认6、bound默认20、seconds默认60、output为必需路径。它**无main guard**，import即解析CLI并建矩阵求MILP；没有冻结点verify选项。数学有效使用需p≥3、B=bound≥0；代码未显式检查这些条件，不能将p<3导致空fresh孩子的不可行或负B非法bounds当候选失败。

连续系数x=(α,β)各在[−B,B]，无单调或β≤0假设，β按无序标签对共享。M=20B+20；对实际B20时每终局利润在[−60,60]，M420足以释放未选择大M约束，不把未激活行误作额外数学限制。

对全部a≠b有连续X_ab/Y_ab，表示首/次玩家在第三位指定真实回复后的收益。对全部互异(a,b,c)有binary z_abc，在每个有序二步历史(a,b)恰选一个第三题；对每a有binary b_ab，在该首题后恰选一个第二行动。R_a是首位强制a后沿这些真实子策略完成的利润，L是规定根收益；另对每无序二元H和e∉H有binary t_He，选一个静态query。

变量域没有对原CAG给fresh限制；它就是独立辅助游戏的全部有序合法策略编码。不同(a,b)/(b,a)可有不同z和不同真实尾，未强制计数Markov。

## 大M约束的完整含义

令v_a(S)=α_a+Σ_(b∈S\a)β_ab。

1. Σ_(c∉{a,b})z_abc=1。被选c强制v_c({a,b,c})≥v_e({a,b,e})对全部fresh e，第三位真实最优；两向大M等式同时把X_ab=v_a({a,b,c})、Y_ab=v_b({a,b,c})。
2. 每a有Σ_(b≠a)b_ab=1。被选b要求Y_ab≥Y_ae对全部e≠a，并把R_a=X_ab。也就是第二位对各自真实第三位孩子最优；未冻结其偏离续局为原c。
3. L≥R_a对所有a，并设L=R_0，使root0成为最佳行动。标签可统一置换，固定0不损一般首人反例的搜索；它不把较晚角色的反例自动变成根反例。
4. 每个无序H有Σ_(e∉H)t_He=1，被选e要求v_e(H+e)−L≥1。等价每H至少一个query利润≥L+1，所以θ₃≥L+1。它不是让H看query后再选择，外层仍逐全部H。

由末层向上，这些选择若以精确有理数满足，确实拼出全部fresh有序历史的纯SPE，且首人严格低于θ₃。它没有提供一个真正原单位客户输入或处理原重复行动。浮点可行解必须有理化、独立重放全部约束后才可作该辅助候选反例，代码本身未做这一步。

一般p≥3时连续基本系数d=p+binom(p,2)，总变量

$$d+3p(p-1)+p(p-1)(p-2)+p+1+\binom p2(p-2).$$

约束数为

$$p(p-1)(p^2-3)+p^2(p-1)+2p+1+\binom p2(p-1).$$

这是源码循环的解析计数，不是本轮新建/求解矩阵。p5时171/591，吻合原报告；默认p6时298/1258，不能将默认p6冒报告的实际输入。只在给定B内搜差至少1；无论有限系统如何返回，都不证明无界系数/任意人数候选。

## 求解、保存与380B原结果

SciPy `milp` 用零目标、binary integrality、显示bounds/LinearConstraint、时间上限args.seconds和mip_rel_gap0；零目标只是寻找可行反例，gap0不认证精确不可行。若res.x非空，就保存所有α/β、L与>0.5的z/b/t，未保存X/Y/R、完整残差、分数恢复或第二实现证明。源码不在输出后assert策略/SPE/θ差。output路径由调用者给定、write_text覆盖且未自动创建父目录；stdout pretty打印同一个report，文件不额外补换行。直接对旧report路径运行会覆盖原证据。

380B冻结报告全部十一个字段为：object="full ordered-history quadratic fresh m=3 thetafloor MILP attack"；p5、m3、coefficient_bound20、gap_target1、variable_count171、constraint_count591、status1；message="Time limit reached. (HiGHS Status 13: model_status is Time limit reached; primal_status is None)"；seconds=45.004903078079224；success false。**没有solution字段。**

这表示旧限时运行未返回可行primal，不能称精确infeasible、最佳目标0或已验证不存在反例；也不认证求解器在完整45秒内穷尽哪些分支。报告45秒不同默认60，且无实际argv/源SHA/solver版本/独立stdout/退出码/种子，不从相邻文件补造这些字段。171/591与当前源p5规模一致，只是语义比较，不把它冒当前观察的一次运行绑定。

本次代码与JSON全文/字节核、所有选择器与真实BI语义/时间边界已自足整理，**原CLI/import/MILP/LP/新数学程序均0**。不重扫旧有界阴性，不把old time limit当本环境真实硬限制，继续处理仓库其它来源。

## 使用与接续

817B入口的早先随机/固定策略LP无反例只是未附输入的旧描述，不能算此MILP第二成功证据；一般对称二次候选仍须证明或真正精确反例。现有[完整fresh编译](../定理/无重复辅助博弈的完整历史编译--定理.md)和[偏置福利边界](../障碍/均匀客户偏置的福利与比较边界--障碍.md)用于区分辅助结构与原福利比，不让一次二次搜索替代六人目标。

四原件和初local缺→后normal实得、完整actual claim/owner、现有对象比较、逐源去向见[证据](../../tools/evidence/root-quadratic-fresh-MILP-and-gluing-review/README.md)。若未来确要新搜索，先在新输出目录明确参数并保完整解/时间/stdio，不覆冻结文件；该建议不是本次运行或任何通用最优性认证。本文只承担阶段二精确语义与证据归类。
