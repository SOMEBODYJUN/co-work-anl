# 异权直接共居查询—返回接口：typed_edge_gap 作者Proof read-after v1

审查ID：UM-WEIGHTED-DIRECT-COHABITING-QUERY-RETURN-ALL-FORMULA-FAILURE-v1。
审查者 typed_edge_gap，2026-10-18。仅scratch，无repo/Work/Git写入。

## 实际读取与独立性顺序

本次实际全文读作者Proof：
/workspace/scratch/038d9dcc4cac/weighted_direct_cohabiting_query_return_all_formula_failure_proof_v1.md
实核 SHA256 82783900de69ccb3e14aa187c7aa8a2e2146934d404686f2d67d0dcedbc1b571。

对应Exact此前实际全文读取且实核SHA256 076561e78796927d6792f6dfb3c581c11afd263752b9098abd9f35d58df2ddfb。独立Exact-only完整重构已先冻结：
/workspace/scratch/038d9dcc4cac/weighted_direct_cohabiting_query_return_all_formula_failure_exact_only_review_typed_edge_gap_v1.md
SHA256 6d853646c525a26a0776c4dc393650f95d2c3ae6de882ab64a001a8ed5a40c00。

时间顺序明确：先完成上述独立记录并取得SHA；此后才收到作者rainbow包含matching策略的简短摘要；再经root明确授权，才实际全文读取本作者Proof。作者摘要不是先行证据，不倒填为Exact-only推导来源。原独立记录字节未改。本轮未读取general的新sharp Claim、其Exact/Proof或推导，正式认证范围只限本v1严格SAT域与全公式上界。

## 作者Proof与独立重构逐义务核对

1. **原P严格同域。** q_i三个原端M_i:ρ、M_i+:1、C_i:x_i；b_i两个原端pin:ρ/C_i:1；u_c仅本clause真实C_i:y_i。真实x/y正且和≤1、dummy x1、ρ>1/2。无D/h/真实公共R，作者V_c始终只分析、最终消去。未把旧medium原输入或machine-uniform交换定理免费套来。

2. **strict身份确由物理约束推出。** 作者E⊆R来自C_i上x_i>0与unit b_i不能共居；内部M容量至多一件给N−|E|+|R|≤N，所以E=R、每M恰一件。与独立记录的q/b全槽饱和是相同结论的两种计数。y_i>0排斥u与b，故每clause的u读到同编号q；cycle方程(1−z_i)+z_i−=1保证同变量单方向。没有把同编号作为外加关系。

3. **SAT正向全jobs无漏。** 每clause仅选真实真文字，q与u在其C真实共居x+y≤1，b按满足方向返回替代q内部槽；其它q（含dummy）走同向环、b留C。每M恰一件，每原job一次。重复literal/变量只复用源变量，物理occurrence与jobs仍不同。空公式一idle机零jobs、空赋值，与strict iff兼容。

4. **active共同matching覆盖baseline。** 作者将所有q/b及active u都留在图中，baseline/dummy C只有其b一个邻居，故整数perfect matching强制它们b留C、q内部。我的独立记录先固定这些b并删除相应左右节点，是该图的等价简化；两者都没有偷偷借用baseline返回容量。每active i的θ=1/k_c≤1/2；q两个环端half再在pin扣θ，由同编号b的θ逐项补回；C列b(1−θ)+uθ，virtual列Σθ=1，所有行列和1。合法非负fractional perfect matching给一个共同整数matching，不是各clause分别找可能冲突的局部见证。

5. **恢复全部原任务并核真实异权。** q→V只选择export索引，实际改回同编号C_i、耗时原x_i；active u按原y_i，b按1/ρ；全部baseline u在最后逐件加回。active所有y>1/2逼x<1/2，故query/return错配时q+b的1+x<3/2；同编号时q+u≤1。baseline机b+u≤1+1/2，dummy C仅b，所有M一件≤1。每occ唯一所属clause确保不同u不叠到同一C。无job分数执行，无virtual真实目的地。

6. **算法与位域。** 精确finite数5N+L、dense项2N(2N+m)正确。最少padding为N≤L+2v，额外显式dummy按实际N计；active空时图退化为q/b环matching仍成立。ρ/x/y只做有理比较及常数项负载和，θ位长O(logL)，匹配只扫描显式图，不按参数倒数/分母数值循环。最终输出全部2N+m原jobs的真实端；无软件执行或有限枚举承担一般证明。

## 最终认证与边界

作者Proof与先行独立重构相合，无新增fatal或未闭合义务。正式PASS：所述完整异权direct-cohabitation P的strict≤1 iff SAT及其精确同编号decoder；所有输入公式、任意合法逐occurrence异权/环排序/dummy polarity，均可确定性总位多项式输出全部原jobs实际≤3/2。

这里只认证上界≤3/2，不认证该上界sharp、不认证某个固定NO阈值的NP-hard gap，也不认证一般medium/多尺度复制不可能。作者Proof未宣称这些外推；本轮未读取另一个sharp Claim。主normalized tiny-gap源与UM-TARGET仍OPEN。
