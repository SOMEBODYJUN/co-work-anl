# 均匀定基数单/双边际的显式稀疏证书：Exact

2026-10-18，boss11。辅助Claim UM-UNIFORM-CARDINALITY-PAIR-SPARSE-SUPPORT-v1。

对每个显式正整数d和整数0<=h<=d，存在固定确定性算法，在poly(d)总位时间内输出至多1+d+binom(d,2)个[d]的h-subsets A_t及非负二进制有理权α_t，Σα_t=1，使每个r的Σ_(r∈A_t)α_t=h/d，每个r≠s的Σ_(r,s∈A_t)α_t=h(h−1)/(d(d−1))。d=1时没有pair条件。输出全部实际subsets与权值；不是只给存在性/压缩抽样oracle，输入规模包含d个显式标签，不承诺关于log d的poly。

可用标准有理LP/线性代数，不用枚举所有h-subsets或任意二次定基数优化oracle。Scope仅定基数first/pair：不保证三阶以上矩同uniform slice，不把此sparse law替换用于globalq/M3的原uniform law。它可给七态局部星各rowCFG显式有限支持证书。Proof另冻，审者先只看本Exact。
