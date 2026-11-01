# 数学与实现自查

1. 合法seed是非负整数类型客户、m/p正、q在完整SPE终局R(0)且W(q)>0；归一化每主题≤W、bigM1来自原SPE实际角色保证，不是float residual证明。
2. y集合除root仅q外全R(k)，终局自身；z为每desired选择合格行动，x为每行动最小利润孩子，t=M(k)/W。索引逐states y/t后再z/x，完全配旧DAG。非Markov目标不被删。
3. restrict只冻结seed0的y上界；radius行恰二元Hamming≤R，连续客户/t不受半径。float残差在加radius前，adapter本身无独立整性核；cold仍构造并检查seed，显式floor高于seed超过容差会在优化前拒绝。
4. fixed root/portfolio客户重数自由，不是固定seed；显式portfolio不验范围/重复/≤m且helper bit求和会进位，默认合法，小点合法。参数floor null不表示无默认seed下界。
5. 私有HiGHS passModel/setSolution和float kOptimal/gap0只生成见证；expand≥0.9后仍需精确policy核。
6. fixedpolicy精确恢复先limitdenominator再active-row精确消元、严格verify、清分母/gcd、全有序直接Fraction比较。βw−Γᵀμ≥objective及μ≥0才给固定policy上界，certified primal不保证dual optimal，更不保证MIP全局。
7. 小点allA三历史真实偏离松弛0/0/3/2，W2OPT3；去重Γ0=(1/2,−1,0)、Γ1=(1,−1/2,0)，原始(1,1/2,0)，β3/2和μ0=1余项(0,0,1/2)。全部解析重构，无新数学代码执行。
8. warm报告hash20a37…≠当前6e419…；旧DAGc7d550…相同，不绑定未记录hash的helper/model旧版本。未知旧warm代码未取得，不猜差异，不借新run认证旧run。
9. 150B workspace四字段仅旧路由身份，无数学输入，不切换Boss4。3源12485B与8related/依赖全SHA保，related不额外done。
10. 0原CLI/import/MIP/LP/oracle/策略复跑；旧成功有限实验不重复，大报告/42输出未读不冒已认证。一般五人后续别证与六人OPEN保持各自范围。
