---
id: "customer-attraction/f6-count-credible-generators-and-static-security-search-contracts"
kind: "program"
type_tag: "程序"
title: "R-f6两种完整策略生成与静态安全探索的原始合同"
status: "full-source-and-all-saved-data-reviewed;fixed-rational-audit-separate;no-original-search-replay"
summary: "完整重构9583B双策略发现器和6236B静态安全交替LP；五份JSON逐字段保全，四分数策略资格与两个全兴趣单客户等号分别证明；参数/停止/归一/精确门和历史元数据不混用。"
source_refs: ["source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-f6e401683adb4a76a4bd4d8022713582/credible_badpoint/count_policy_attack.py", "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-f6e401683adb4a76a4bd4d8022713582/credible_badpoint/count_policy_attack.py", "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-f6e401683adb4a76a4bd4d8022713582/security_aggregate/search.py", "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-f6e401683adb4a76a4bd4d8022713582/security_aggregate/search.py", "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-f6e401683adb4a76a4bd4d8022713582/security_aggregate/arbitrary_4_4.json", "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-f6e401683adb4a76a4bd4d8022713582/security_aggregate/arbitrary_4_4.json", "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-f6e401683adb4a76a4bd4d8022713582/security_aggregate/generated_6_4.json", "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-f6e401683adb4a76a4bd4d8022713582/security_aggregate/generated_6_4.json"]
---

# R-f6两种完整策略生成与静态安全探索的原始合同

## 模型与完整锥

有限单位客户、有限非空共同标签目录、m≥1位单位提供者、每个完整有序历史可依赖地选题，客户在终局覆盖者间均分；保空覆盖、同覆盖异标签、重复、零客户和所有平局。这就是当前任务模型。若另研究要求不同标签覆盖不同集合的受限目录，迁移须重构策略，见[完整商](../等价/覆盖等价标签的完整策略商--等价.md)；此附加限制不用于排除当前原标签。

给定形式策略σ，对每个决策h及标签b，由原策略分别重放规定终局z_h与强制b后的终局z_{hb}。客户型B的IC行是规定份额减偏离份额，记Γ_{h,b;B}。质量w≥0满足Γw≥0当且仅当这份σ完整纯SPE。份额在行动不属B时为0；属B时该终局包含该行动，分母必正。以下两个发现器都意在保持这样的固定真实σ，而不是冻结其他人在轨题作静态替换。

## 9583B双策略发现器：共同数据与count分支

原模块导入即寻找含customer_attraction/__init__.py的祖先根，再用绝对冻结相对路径动态导入R-d28.../experiments/cex_exact_sweep.py。继承的IntegerSetSolver完整源码已实读，按原同SHA保在[成熟原件](../../tools/evidence/rd28-exact-outcomes-and-static-backgrounds-primary/original/experiments/cex_exact_sweep.py)，不重复拷贝/运行。它以非递减标签元组枚举每层count与终局，L=lcm(1,…,m)清分母，rows为终局×标签×兴趣型的整数份额，coverage为终局覆盖0/1。maxfreq非零时按popcount≤maxfreq删列，表示限制客户兴趣频率，**没有**删目录行动或历史。

count分支从末层向前，对每个count只接每个孩子已选的一个终局，按浮点收益最大者选行动；容差|v−high|<10^−7。welfare模式再在这些近似平局中挑低福利，最后随机破平局。这生成一份count形式完整策略，不等于全集合值BI，也不是“任一count表自动是SPE”。最终是否为SPE取决于固定表的全部Γ是否对所保存新质量非负。

cone()枚举所有count状态的真实非自身IC，按整数行逐字去重并删零。对一个预选J，在w≥0、Γw≥0、实际根福利=1下最大化比较并集覆盖；HiGHS接收浮点矩阵。J来自全部恰min(p,m)不同标签支持，它在新质量求出前固定。换质量后没有重选原策略，也没有保证原根仍为该新输入的最坏SPE。

## credible分支：集合值菜单与完整有序展开

credible_cone先对旧质量按浮点后limit_denominator(10^6)恢复，清分母/公因子成整数。显式拒绝sum(nums)·L≥2^62，以保护该非负整数数据的int64收益乘法；此门不替代任意恶意参数/负质量输入验证。该分支不是只对count选一个共同续局，而是缓存每个count的全部可实现终局集合R(q)：对每个行动a取孩子集合R(q+e_a)，阈值是max_a min_{t∈R(q+e_a)}U_a(t)，将各孩子中当前收益不低于阈值的终局合并。

再在最小福利根终局中随机取target。expand(h,q,target)对每个**有序**h独立选能实现target的当前行动；偏离b后，从该孩子集合中挑一个使偏离者收益不超过规定收益的dest，并递归到h b。uniform/min/max/lowW只决定这个合格菜单内的选择法，不删除完整树。保存记录[h,selected,target,destinations]以及完整真实Γ。由有限树归纳，给定终局选择器构成一份真实σ；保存后质量改变了，仍须对该固定σ重新检查Γ。

本批2801动作保存图的所有target/dest索引与真实重放逐项一致，见[四点资格页](<../../../../tools/evidence/phase25-material-attachments/20261103-boss6-triage/396e014803a5c7d749d2.md>)。这份源scope沿用“count-policy”字样，不得据此把有序图降成count表。集合值缓存也不承诺原策略匿名净化；[该一般净化已假](../问题/完整历史计数策略净化--问题.md)。

## 共同迭代、精确门和三份历史报告

默认p7/m5/100轮/seed63/maxfreq0，需--output，credible默认false。每12轮或无champion时重启，第0轮赋mask1质量m、其他singleton1；否则沿champion，每3轮可能加小噪声。目标J先按旧质量覆盖最大挑，逢it%4=0改随机支持；count动作签名重复时只扰动一次再生成，不是循环直至新策略。credible的四菜单mode按it%4轮换。

LP成功即更新champion；只有value>best+10^−8才记录。每坐标limit_denominator(10^7)后：count路径逐count核包括自身IC及W，credible路径只算去重非零Γ行和W。源码**无论精确松弛是否负或W是否为1都会保存该改善记录**；scope给读者资格条件，不是程序自动拒收门，也无独立非负/单位客户展开检查。此次四保存点恰全满足非负、精确W1、完整IC与目标绑定，由本次新固定核承担，不把旧字符串当资格证明。原 float ratio 并非有理LP最优证书。

|原JSON|配置轮数/seed|实际保存改善记录|原elapsed秒|输入坐标/动作|
|---|---|---|---:|---|
|m5p7_all|100/63|iteration0、3|8.939444158000015|127型；各330 count动作|
|m5p7_credible|160/97，credible=true|iteration0|52.97128274299996|127型；2801有序动作|
|m6p8_freq2|100/63，maxfreq2|iteration0|12.901645943000005|36型；1287 count动作|

原件未存每轮LP成功/失败、全部随机输入、stdout或可认证的完成计数。configured iterations和最终elapsed不能倒填为100/160/100次成功精确证书。每5轮checkpoint及最终写的源码合同保留；两份count报告args缺当前源码必输出的credible=false字段，表明不能声称当前main与历史报告逐字节同源执行。三份记录各完整保留在[原件清单](../../tools/evidence/f6-fixed-count-and-credible-policies-primary/source-manifest.json)。

## 6236B静态安全探针的真实值和归一

此程序独立prepare全部p标签有序历史，含Σ_{d=0}^{m−1}p^d个决策；cone从末层按给定动作重放终局，形成全树IC后**先round到12位再去重**。因此其实际浮点G不是未经舍入的精确Γ，阳性必须另恢复真IC。

对静态查询分布p∈Δ(标签)与一个m−1竞争标签多重集b，
\[
 \beta_b(p)_B=\frac{\sum_{a\in B}p_a}{1+b(B)},\qquad
 v_m(w)=\max_{p\in\Delta}\min_{|b|=m-1}\sum_B\beta_b(p)_Bw_B.
\tag{3}
\]
竞争者不观察实际抽中的查询，背景枚举全部重复允许的多重集，非原σ菜单。重复背景的排列对(3)相同，所以用combinations_with_replacement合并不损失静态值；这不匿名化σ。

固定σ、p后，LP变量w,t≥0，约束G w≥0、**根福利c·w=1**、t≤β_b(p)·w全背景，最大化m t。源码gap=−fun−1。随后safety()固定新w，解另一个查询maximin LP更新p。不是对w,p的联合线性优化，不是最低CCE福利桥、逐人安全桥或适应查询的末位θ值。[精确完整锥对偶](../定理/完整策略锥的静态安全值对偶--定理.md)给正有理全IC见证的数学含义；本源没有执行其有理恢复/对偶证书。

默认p4/m4/300/seed81273。arbitrary每个历史独立随机动作，generated从稀疏随机整数质量通过浮点后推生成σ；两种均完整有序。对每新签名，先均匀查询、再Dirichlet查询，各至多3次固定σ交替；queue存在但源码从未加入元素。重复签名continue会跳过iterations_completed更新。LP失败只终止当前交替；全局best>10^−7才停止。所有约10^−8改善可更新best，但positive_found门是10^−7。原源码只存一个浮点best，不保存全部LP候选/真Γ/最优对偶；current finite best_gap0不证明普遍或固定锥精确上界0。

## 两份security保存点实际只有一个全兴趣客户

|原报告|m,p|原完成计数/不同策略|原best_iteration / best_gap /阳性|全部有序动作|实际路径/计数|原constraint_count/elapsed|
|---|---|---|---|---:|---|---|
|arbitrary_4_4|4,4|1000/1000|0 / 0.0 / false|85|1000；(3,1,0,0)|187 / 15.467538979999972|
|generated_6_4|4,6|500/499|0 / 0.0 / false|259|0241；(1,1,1,0,1,0)|370 / 33.57694404399996|

全部15/63个weights坐标（包括原-0.0）已读，只有全兴趣mask15/63质量1，其余均零。原各85/259动作的全部键域、合法动作与根路径已绑定；这些动作没有必要重算数值IC：无论怎样行动，唯一客户被四人全部覆盖，每个终局各得1/4，任意历史任意动作都平局。故**任意完整动作表**都是真SPE，W=OPT4=1；每个竞争背景都给任意合法查询1/4，所以真v4=1/4。这是这个单客户点的解析恒等式，不是当前轮验证187/370个舍入行或重放1500次探索。

第一点p=(1/4,…,1/4)字面即合法分布。第二点六个原小数0.16666666666666666若按JSON十进制有理数读，总和=24999999999999999/25000000000000000；若按Python二进制float精确读，总和=18014398509481983/18014398509481984。两者都小于1，**原数组不是精确概率分布**。不静默归一来宣称原p精确通过。

对这个常值收益点，非归一数组代入固定查询线性式时mβ−W恰为Σp−1，分别−1/25000000000000000和−1/18014398509481984。原报告best_gap0.0保为旧浮点输出。另行定义精确p_a=1/6，才是合法均匀查询，确使m v−W=0；该结论由单客户结构证明，未运行safety LP。这个修正版分布不是作者原字面数组，也不认证对应全σ客户锥的全域最优。

全兴趣点令全部标签同覆盖，集合商只一主题，仍合法且上述福利/安全值不变。若另外要求恰4/6个不同覆盖的固定目录，则此点并不是该附加合同的达到证据。旧tax审计中这两文件出现过的−1/4系数是另一个目标的有限记录，不能拿它代替本次完整原件实读或真安全值证明。

## 运行与接续

本轮唯一新固定核只处理四个分数策略点与security文件结构/字面查询；原两main/import、所有原LP/BI/RNG/safety调用均0。实际事件、原stdio及完整固定结果见[证据目录](../../tools/evidence/f6-fixed-count-and-credible-policies-primary/README.md)。后续若要认证某固定σ安全桥最优，须给原理性Γ、精确可行原始/对偶，而非重复旧近零扫描。主六人half、普遍安全桥均不由这两个四人常值点解决。
