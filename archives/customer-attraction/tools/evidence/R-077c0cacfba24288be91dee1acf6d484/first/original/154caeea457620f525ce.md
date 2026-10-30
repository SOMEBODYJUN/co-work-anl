# 正项回路与共同客户耦合

一般 Q-CAG-HALF 仍 OPEN。本目录是 Boss4 本轮内部研究备份，不是可靠结果提升。

* `reciprocal_reply_telescoping.md`：任意固定有序前缀 H、任意 r 的对称末位收益核；
  r>=2 的正项对回路沿互惠真实回复链精确消去内部误差。r=2 时任意长链只留
  固定前缀客户的端点债，上界 n_1/6+4n_2/15，并可由同一实际前缀cohort的
  最终总收益一次支付。尚无他人独立审核。
* `verify_reciprocal_reply.py`：独立 Fraction 系数与真实末位图复核器。
* `reply_staircase.md`：一类跨前缀扩展：真实最后回复、核对称，再把一份枢轴
  移入前缀并减少复制数。所有步的损耗精确望远镜成调和租金差；末端前缀
  通常离轨，仍未支付实际根福利。
* `parity_moment_gluing.md`：任意m>=3、2m标签的全局signed奇偶构造。全部<=m
  标签边际非负、所有<m阶全局矩与真uniform客户相同，却违反一个明确m阶
  全目录逐客户非负行。signed形式完整BI图与true-uniform同图SPE来源分开
  证明；不是合法客户或half反例。
* `verify_parity_moment_gluing.py`：显式有限类型、覆盖基行与完整BI图独立审计。
* `reciprocal_reply_audit.json`：首版运行输出；
  `reciprocal_reply_audit_v2.json` 为另加实际前缀cohort收益支付检验后的完整输出。

范围：完整原策略的真实末位历史；任意目录、单位客户、任意历史平局。局部
运输可跨任意长回复链，但有序 H 和 r 必须不变。r>2 仍可端点化，却会对原
前缀未覆盖客户收费。没有把回复环的终点支付给实际根路径。

下一步：找出从实际早期行动到回复环/阶梯终点的共同支付；确定一组阶梯
是否能覆盖最优并集而不重复收费。不能把已闭合的一类跨前缀代数粘合
外推成实际根福利预算或一般half证明。
