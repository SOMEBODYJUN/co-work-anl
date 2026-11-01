---
id: customer-attraction/symmetric-singleton-topic-block-price-direct-mask-finite-audit-contract
kind: resource
type_tag: 资源
title: 对称单占主题块价格的直接mask有限审计合同
status: complete-two-primary-read;full-eight-settings-and-all-report-fields-preserved;general-coupling-compared;zero-new-math-run
summary: 3280B标准库Fraction程序以wreath-product每个非空兴趣轨道各mask一客户，固定玩家块总负载1、其它块任意重复有限计数，直接核遗漏/独占/实际收益及B(u)<=W−u；原8组4820profile-orbit/34198均匀价格检查与任意参数耦合定理、原独审先验分开。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-5c4f6385eec046eb9a20052facacba11/early_price/audit_symmetric_singleton.py
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-5c4f6385eec046eb9a20052facacba11/early_price/symmetric_singleton_audit.json
---

# 对称单占主题块价格的直接mask有限审计合同

3280B代码与1911B报告共5191B全部实读，含八行所有字段/分数字符串/等号数；原size/SHA256/blob、实际2YB claim3a6c91d6…pushed/synced、本2Boss4 owner/normal-show齐。没有执行main/audit/compositions、生成客户mask、重演Fraction收益或价格检查。下述数学归纳/计数解释与原有限报告、当前静态自查分开。

## 这里的singleton是单占主题块，不是单客户主题

给c个主题块、每块k个共同可区分标签，p=ck。群允许块内任意置换以及任意块置换（wreath product）。客户兴趣mask M的轨道键是其各块度数的排序多重集

\[
\operatorname{key}(M)=\operatorname{sort}(|M\cap block_0|,\ldots,|M\cap block_{c-1}|).
\]

相同键确为一个完整轨道：先把块度数配到相应块，再在每块内将所选主题置换过去。代码逐mask1…2^p−1直接造出每个轨道，**每个mask是一名单位客户**，无0mask/无玩家随机策略/无浮点客户。一个轨道客户数n、共同关联度d=popcount固定；每个主题在轨道中大小相同，源码还直接assert该大小唯一及p·size=d·n。

实际终局固定

\[
q=(1,\underbrace{0,\ldots,0}_{k-1},q_{outside}),
\]

第一块总共恰选择一次，选标签0的玩家是被审计者。其它(c−1)k个标签计数任意非负，合计r=0…max_others，由compositions完整枚举，所以总玩家数是1+r；其它块可重复选同一主题或同块多主题。不是“第一块只有一个不同已用主题但多人重复”，也不是q个不交单客户主题/m=q+1的[近半floor族](../定理/单例满配的真实终局与近半地板损失--定理.md)。程序没有有序策略、子博弈、离轨节点、HI、BI或均衡假设，检查的是任意满足单占条件的终局。

轨道单独作为一份标签实例时，若干主题覆盖可以完全相同（例如全mask轨道仅一名喜欢所有主题的客户）。代码不检查“原集合目录中每主题是互异实际集合”的额外条件；这些是逐轨道代数单元，不把每行宣为原严格集合目录的独立完整游戏或反例。用于原集合目录须在完整输入另核覆盖互异；任意非负整数轨道重数组合亦须保相同群对称和实际单占条件。

## 每条profile-orbit实际核了什么

对轨道每个客户mask，代码按给定q求load=Σ_(a∈M)q_a；w为load>0客户数，missing=n−w。被审计玩家的实际均分收益和独占客户数分别为

\[
u=\sum_{M\ni0}\frac1{load(M)},\qquad
e=\#\{M:0\in M,load(M)=1\}.
\]

因q₀1，喜欢0的客户分母正，不会计算1/0；其它未覆盖客户只算missing。所有收益用Fraction精确累加。源码assert完整链

\[
\boxed{d\,missing\le(p-d)e\le(p-d)u.}\tag{1}
\]

对这个单一关联度轨道，算

\[
price=\max\{0,n-(p/d)u\},\quad slack=price-(w-u),
\]

并assert slack≤0。worst是全部profile-orbit的**最大**slack，报告max_price_minus_W_plus_u即B(u)−W+u；equalities只计slack恰0的profile-orbit，未计每个h的相等次数。

随后每h1…p直接取均匀实权z_T=1/h，逐客户累加min(1,d/h)再减(p/h)u，assert每个obj≤w−u；uniform_price_checks仅数这些额外p个检查，不包含(1)或前面的单次exact price检查。它不是输入游戏数、LP数、完整策略数或有序IC比较数。

## 为什么这个price是完整连续价格，而非只抽一个菜单

定义全部客户的连续分数价格

\[
B(v)=\max_{z_T\ge0}\left[\sum_M\min(1,\sum_{T\in M}z_T)-v\sum_Tz_T\right].
\]

本对象容许总质量τ0，不是仅τ≥1的固定菜单子族。单轨道各主题大小d n/p，给定任意z及τ=Σz，对客户求和的凹性/Jensen得覆盖≤n min(1,dτ/p)。均匀z_T=τ/p每客户同时达等。因此B(v)精确为max_(τ≥0)[n min(1,dτ/p)−vτ]，其最优在τ0或p/d，恰max{0,n−(p/d)v}。h=d就是后一转折点，源码其它h是直接有限交叉检查，未调用LP或母稿概率公式。

(1)又给d(n−w)≤(p−d)u，即n−(p/d)u≤w−u；零候选也≤w−u，因为单玩家收益不超过总覆盖。故B(u)≤w−u。多轨道各按同样单占计数：对任意同一个z，逐轨道目标≤各自B(u_orbit)≤w_orbit−u_orbit，求和再取max得全客户B(u)≤W−u。该解析拼接处理任意非负整数轨道重数；程序只直接枚举一份每mask重数1的轨道和有限q，不把解析外推冒额外运行case。

## 任意参数的承重证明来自完整耦合

[结构价格定理](../定理/关联度正则分数价格与对称单占主题块预算--定理.md)与本次全文实读8410B原母稿给所有c,k及其它块任意重复的证明。为使(1)的量词自足，简述其完整机制。

固定轨道块度数多重集(a₀,…,a_(c−1))、d=Σa_g。均匀客户等价于先把这些度数均匀分给各块，再在块内均匀选a_g标签。其它块g用了t_g个不同标签，令q_t(a)=C(k−t,a)/C(k,a)（不合法分子为0）、G=Π_(g>0)q_(t_g)(a_g)。q_t随a非增。遗漏比例为E[(1−a₀/k)G]，独占比例为E[(a₀/k)G]，两者和EG；块0没有第二个选择者是这两式的必要结构前提。

f(b)=E[G|a₀=b]随b非减：对可能值a<b，从总多重集各删a、b得公共剩余；条件a₀=a的其它块为公共剩余加b，条件a₀=b的其它块为公共剩余加a。把新增值放在同一个均匀随机其它块，其余度数同排列；即使度数重复，每最终排列可作为新增位置的数目固定，故边缘分布正确。只一个其它块度数降低，q_t非增使后一G不小。c1时G1直接成立。

独立复制a₀′，Cov(a₀,f(a₀))=½E[(a₀−a₀′)(f(a₀)−f(a₀′))]≥0。于是E[a₀G]≥E[a₀]EG=(d/c)EG，换算为计数正得d·missing≤(p−d)e；e≤u给(1)。这是真正所有参数/人数的论证，不由4820项的有限阴性承担。当前是知情重构母稿，不新增盲审、外审或原作者时点“已独审”身份。

## 八组完整原记录与范围计数

main无CLI/输入/seed，固定以下八个(c,k,max_others)。报告顶层恰status、scope、results、total_profiles_and_orbits、total_uniform_price_checks五字段；status="passed"，scope="Finite direct-mask audit, not a general proof"。每行恰blocks/topics_per_block/orbits/profiles_and_orbits/uniform_price_checks/max_price_minus_W_plus_u/price_equalities七字段，全数如下：

| c | k | max_others（代码） | orbits | profile-orbit | uniform price checks | 最大slack字符串 | price_equalities |
|---:|---:|---:|---:|---:|---:|---|---:|
|1|1|0|1|1|1|0|1|
|1|3|0|3|3|9|0|3|
|2|1|6|2|14|28|0|8|
|2|2|6|5|140|560|0|32|
|2|3|5|9|504|3024|0|64|
|3|1|6|3|84|252|0|30|
|3|2|5|9|1134|6804|0|134|
|4|2|4|14|2940|23520|0|223|

原总数4820/34198，所有最大slack为字符串"0"。原price_equalities逐行保留，没有用其总和或某一等号点替全部profile断言。范围最大p8、其它玩家上限6，但不同setting上限不同；绝不是8主题/7玩家所有终局或所有兴趣客户重数。

计数可解析解释：非空轨道数C(c+k,c)−1；outside坐标q=(c−1)k、总数≤R的弱组成数C(R+q,q)，q0也只空组成一份。因此profile-orbit为二者乘积、uniform checks再乘p，与表中口径相符，不重演原枚举。每个轨道都含r0的profile，此时u=w=dn/p、price0、slack0，故结合全称不等式其最大slack确可取0；等号profile的其余具体数目仍是原有限报告，不伪新增逐项复核。

报告没有逐orbit键/客户mask列表/逐profile loads、等号见证、每个h目标、argv/Python flags、源码hash/耗时/退出日志。代码是确定性配方，当前不为补这些数据再跑生成器/收益。原计数True/"passed"均不冒当前0run。

## 独立性、停止和真实运行闭包

程序只用标准库itertools/json/defaultdict/Fraction/Path，无项目helper、SPE engine、数值优化器、轨道LP导入或母稿概率公式导入。独立之处是它直接枚举兴趣mask和负载，从定义算均分收益/独占/遗漏，而非调用耦合q_t公式；它仍在代码里使用已述单关联度price的代数表达，不是另一份一般定理证明或盲读数学审稿。

main有保护；全部八次audit返回后才write_text覆写旁侧symmetric_singleton_audit.json，再print全部pretty JSON。没有时间/参数budget、超界提前截断或正点早停；遇assert失败会在写新总报告前中断，旧JSON可能仍留。所有数学验证均用Python assert，优化启动可移除它们；原启动flag/退出日志未提供，不能从现存status字符串重造原实际过程。正常启用assert的源码路径与报告完整数字相容，当前不重复运行来取得新PASS。

8410B母稿是**相关数学比较资产，不是runtime依赖**，经本次正常clean show成功取得（exit0/stderr空）并核inventory size/SHA/blob、全文与已出版定理对照，不额外done。旧定理页的“当时尚未读此code/JSON”属于其原清洗范围；本2补足实际有限字段，不倒填成那一历史批已经执行或原作者独审已完。

## 全仓比较与当前状态

关联度REG的一维价格式及单占主题块条件不需要SPE；不能据此证明一般实际玩家B(u_i)≤W或六人half。删单占后的不交单客户/两人同题可使B(1/2)=p/2>W1，但那终局可改fresh独得1、非SPE，亦非本审计的“单占”输入。

与[强菜单固定查询锥](实际玩家强菜单价格的固定查询客户锥合同--资源.md)相比，本audit无Gx≥0/重选任意非空客户质量/LP；与[29客户根价格](二十九客户根价格的父方Fraction重构合同--资源.md)相比，它无共同endpoint祖先λ/流约束/HI允许路径；与单例满配floor族相比，它不算L/G/完整均衡。准备时的三篇全读及后续结构定理/实际母稿全读各有SHA记录，不按same singleton名字借有限成功。

原代码和所有报告字段、逐源语义收据、相关母稿/normal原捕获见[证据](../../tools/evidence/symmetric-singleton-price-audit-two-primary/README.md)。本次0main/import/audit/compositions/mask-orbit生成/Fraction收益检查/LP/SPE/旧成功重放，仅JSON/YAML/AST/字节hash/元字段/链接静态自查；解析耦合与组合数解释不称程序执行，阶段三不建图。
