# 任意异权 query/return 三半交换：作者 Proof 实际 read-after

审查者：general_query_response_review。2026-10-18。

## 实际顺序与输入

先仅据新Exact及获准的既存查询分离v2，独立构证并冻结c3f424...记录；root实际全文读该记录后，本轮才首次实际全文读：

/workspace/scratch/038d9dcc4cac/general_weighted_query_return_three_halves_exchange_proof_v1.md

作者Proof SHA-256：da8edbfcaaa481e7842947147ea4aa136a775aa1b5a0624ecff5297a57ddbedf。

对应Exact SHA-256：bda34c6f0abcbbb3fafad8fbadbec8c2e89f940ddef8e3a8f6d9ab92b04cbd41。
先行独立记录SHA-256：c3f42455499c407f3d959c0a0d94965c925829fff62a0d5adf31b0e90304492e。

**明确结论：作者Proof有效，无fatal；其删q_i再建P*路线与先行保全部jobs的P0路线均满足同一Exact完整实际合同。**

未读隔离的global private-clause新候选或其它agent输出；未改repo/Work/Git及任何旧冻结字节，仅scratch新增。

## 作者路线逐项实际核对

1. A'=A∪(R\{b_i,b_j})正确；sigma_i内部恰A',b_j,q_i，sigma_j内部恰A',b_i,q_j。分析中删sigma_i的q_i因内部时间非负只减负载，不要求其时间为正。此处不是最终删除原job。
2. P*含A'及三枚b_i,b_j,q_j，对A'仅保留两见证实际内部端，对三特殊jobs保留其各自已用内部端；另加三个不同analysis-only outside0端。资格可在分析实例删减、不能在最终原P新增，作者区分明确。两份rho_0/rho_1都是P*全部jobs的完整actual，峰≤T。
3. Q*={b_i,q_j}在rho_0均outside0、rho_1内部，因此是changed jobs且每枚delta=0。调用既存分离v2时，零时间域、两份完整见证及owner变动条件全部满足；所得single-query actual峰≤3T/2。
4. 所用关键依赖为nonquery支持不交，不是仅费用平均。b_j是nonquery且从内部到analysis outside，最多被一个支持移出，所以至少一份输出仍留b_j原内部端。A'全部端均内部，选中输出于是内部jobs精确为A∪R或A∪(R\{b_i})∪{q_j}，准确是inactive或指定mismatch(j,i)。
5. 恢复阶段保所有这些内部原端；对其它全部原boundary jobs放其自身O_z、真实时间T，包括P*未列的q_i、其它Q及未内部化query。全部A已在内部，原N件jobs各恰一次，没有仍在analysis Z执行的原任务、遗漏的q_i或复制的job。每原O_z只可接自己一件，恢复outside同时≤T；内部≤3T/2，故原P完整峰≤3T/2。
6. 内部目的机均为两原见证实际用过的有限端，符合Exact更强endpoint合同。P*中新增0端/新Z只服务证明，最终不输出，亦没有利用原见证外的内部有限资格。
7. 这与我先行P0构造的关系准确：我先将完整原P的所有私有outside成本置0，分离后保护b_j并把q_i外移；作者在建P*前已删去q_i，选中后再统一恢复原outside。二者都仅减少分析内部负载，并依私有outside恢复完整原jobs，没有数学冲突。

## 推论、边界与复杂度

8. Inactive≤3T/2不可行时，实际二选一不能给inactive，故必须给指定错配；不需算法判定不可行性。交换i,j可得反向。全部k份见证已知时逐有序对输出，多项式；仅知存在时只给存在量词，没有计算隐藏strict witness。
9. B≥3T/2的inactive弱禁止推出同阈值内指定错配，足以反驳同一明确接口的弱同编号合同。不从源NO自动得到两份输入strict见证，也不推出源hardness或一般UM算法。
10. 非均匀内部cost、0、A空、unused机器及输入额外有限端>T均不造成例外。只使用原见证实际有限端，不对∞运算。H空时合法aligned输入在k≥2下不可能，此为前件不满足，不是漏例；T0不在当前ID域。
11. P*有|A|+k+1≤N jobs、|H|+3机器，原时间逐项复制或写0；既存分离及支持检查、全部原任务恢复按显式总位长多项式，dense原矩阵全部(|H|+2k)N成本已计。没有按分母或T倒数展开。
12. 私有outside只保证自身一件T；若改成真实共享变量/clause机器，恢复可能累积负载，不能局部错配免费拼成全公式。A可跨网络外送、多个query/return bundle或额外共同外部锁的改域均未自动覆盖。作者没有把此直接结构推论包装新分离定理、新全局近似、全球新颖性或near2源。

所用既存依赖为UM-TWO-WITNESS-QUERY-SEPARATION-v2，其当前读取文件SHA fa93beb7acbe8cbc96ce8da05c30e69584bd6c5828bb6e1ab164497150b45b1c，正式使用§1–2及§4，不用sharpness、费用或§5筛选。本轮没有软件或有限枚举认证。

**最终作者读后：Exact/Proof一致，完整actual、zero、bitpoly和外部边界通过，无standing fatal；等待final canonical后另冻实际范围审查。**
