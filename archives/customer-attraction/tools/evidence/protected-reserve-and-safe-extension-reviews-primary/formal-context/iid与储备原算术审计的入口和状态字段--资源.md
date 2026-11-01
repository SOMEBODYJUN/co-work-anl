---
id: customer-attraction/iid-and-reserve-original-arithmetic-entry-and-status-fields
kind: resource
type_tag: 资源
title: iid与储备原算术审计的入口和状态字段
status: 两代码/一冻结iid报告的全功能与有限域保存；原旧OPEN字节不代表当前真值
summary: iid顶层写520B/打印486B与储备guard写890B的合同分别明确；有理插值身份、36客户静态查询及69完整策略/n16标尺不同，已有LW充分同SHA成功不重复。
source_refs:
- source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-6cf1f30515fe44eeba28d5390d6940e7/coordination_2026_10_23_followup/audit_extra_iid.py
- source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-6cf1f30515fe44eeba28d5390d6940e7/coordination_2026_10_23_followup/extra_iid_audit.json
- source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-6cf1f30515fe44eeba28d5390d6940e7/coordination_2026_10_23_followup/audit_reserve_states.py
---

# iid与储备原算术审计的入口和状态字段

3285B iid原code、520B原JSON、4347B储备原code逐份全文/全部字段实读核size/SHA/blob。原890B储备输出在本批仅必要相关，未额外primarydone。两个程序此前LW各实际一次成功且全输入充分，当前主源处理0重复运行；不存在“以前related已读就已经primarydone”的倒填。MI5实际合批claim已pushed，本5 owner/in-progress/SHA已核；原needs-attention配独立保全证明，不改称synced。成功semantic receipt仅本5，当前正文未预称pushed/done。

## iid实现：有限身份检查不是全局EI真值认证

bernoulli_share(r,p,b)=Σ_(j0…r)C(r,j)p^j(1−p)^(r−j)/(1+b+j)，只用Fraction/comb；alpha8据8个明确单位客户、分布(0,t,(1−t)/2,(1−t)/2)、完整固定前缀兴趣负载求各纯查询期望。它不导任何SPE模型/solver，不读取外部实例或report。

root r3、prefix0 r2、prefix01 r1的α作为t多项式次数至多3/2/1。分别在4个点0,1/3,2/3,1；3个点0,1/2,1；2个点0,1核与显示g/差多项式相等，次数界使这些是精确恒等式核验，不是对未知非多项式函数少量采样就外推。随后核两个根区间端点符号、15/8与52/27严格低2及最后精确交点7/15的76/45。

36客户另独立构成：X/Y各3标签，9个跨对客户；每个X二元组和Y二元组的9种四会员模式各3名客户，共36。每纯题触3名二会员/18名四会员客户。对6查询各枚举216个静态三竞争者有序背景，均值305/36；它不重构原36块复制族SPE，不验证所有k背景，allk<10由[原积分证明](../证明/额外iid原压力家族的正确槽数解析判别--证明.md)承担。

代码**没有main guard**，顶层即完成上述检查，Path(__file__).with_name在源码相邻写pretty JSON520B，再print compact JSON486B。本次复用的LW原entry没有先import再运行。generated520与冻结字节同，stdout只字段同；两个字节数不同不是失败、不能写二者同一串。

520B字段完整是status、三八客户值（两个strict_upper15/8/52/27，一个exact76/45）、actual_payoffs三个2、replicated36_k1精确305/36、allk symbolic upper `12-3/e-9/e^2<10`、allk_scope注明解析证明。status原样含`EX-IID remains OPEN`，这是旧历史字段，不因程序exit0重新认证。全局EI已有m4银行反证，新的[七客户根静态精确比较](../反例/额外一人iid收益桥的七客户银行根反例--反例.md)更给m3 λ4=665/432>3/2；原两个家族未命中仍真，不能把全报告数学随旧状态一起弃掉或把旧字节改成新真值。

原程序没求root/prefix0的Nash精确代数根、没算所有SPE路径、没检查新七客户bank、没重演发现LP。当前它与新data-only bank核都出现1296查询，但前者36客户/后者7客户，不是一次或同schema客户输入。当前λ、真实菜单metaNash和整数静态v也不混。

## 储备实现：69完整策略和一个精确负信用标尺

4347B只有Fraction/itertools/pathlib/json。main有guard，客户9类型内嵌展开69名；choose对所有lenh<3取A，末位按A次数≤1取A、恰2且含F取E、其它取F。finish沿同策略在改动的有序历史继续；payoff调用占用行动，分母正，不借旧报告的PASS。

对所有6^d/depth0…3的259个有序节点，逐5个非自身动作1295比较，actualAAAF/利润10,10,10,18/W48。profit(portfolio,background)逐客户hits/(old+hits)，hits0跳过；optimum用可重多重集，4槽126个/3槽56个，得到F4root69/F3(1_A)41；robust_floor在合法六题max Σ1/(r+old)给两个15/2。126是四槽组合数，不是旧三人六题松弛的126收益顶点。

程序精确RHS=max(8hroot,2u+max(Fchild,6hchild))65、strictgap4；原真实child P38/half surplus35、floor surplus4、所需8；用既有三人5/3定理数值算41/5，这不是重新验证该定理的512类符号证书。

n16令h_n=min_(j1…n)(j+n/j)=8，只检查同f15(1,15)需≥−3/8又≤−77/120矛盾，并输出放开旧独占项需f15(1,0)≤−4/15。一般n≥16 no-go及无上界fresh>=H保护由[解析储备引理](../引理/新鲜储备的真实尾部保护与旧独占负信用门槛--引理.md)给，不是脚本扫全n/任意历史储备结构。它没有调用原构造作者的SPE验证器，是原协调者独立按数学陈述编码的实际实现。

main在源码相邻写reserve_states_independent_audit.json、再pretty print；890B生成文件和stdout在LW均与冻结逐字节同，当前主源不重跑。原890B所有字段必要相关原字节保，没有额外主done其source；原PASS只在上述69/标尺任务有效，不是一般half或信用充分性证书。

## 三种证据与当前版本

三个本批原code连同聚合3308共用标准库而不互导，既有LW三个原entry各一次的stdout/stderr/真实输入/源hash/新空目录都充分。当前新mathrun/原entry均0；代码/数据正式primary语义去向与旧related运行身份分开，不重写旧receipt/增加成功数量。

一般解析证明、原有限实现和当前候选真值分层：有限有理多项式身份可由次数闭合；全k、fresh归纳和结构no-go需解析proof；过期OPEN需要后续真实反例校正。原审查的内部独立/当前知情读后比较不等于新外审或全球新颖性。完整source/旧事件复用与关系自查由证据包保存，正文推送/done只依Root实际回执。
