# coupling：共同客户正性与根支付

Q-CAG-HALF 仍 OPEN。本个人目录不改共享数学状态；父研究者统一 checkpoint。

- `interval_ancestor_floor_prices.md`：当前根承重接口。任意非负节点动作价格
  λ给合法根界B_I(λ)，λ1恰G_I、λ0恰最小HI终局W；最优价格等价终局相关
  HI路径混合LP并有有限有理最优价格。一般half支付仍OPEN。
- `interval_floor_prices.py` / `interval_floor_prices.json`：有限路径LP生成及
  Fraction原始/对偶核验；小回归只作为接口诊断。
- `interval_price_strict_candidate.json` / `verify_interval_prices.py` /
  `interval_price_strict_audit.json`：合法29单位客户m4p5例，四个价格把
  G_I=80/3、minHI W25共同提高到29；独立无优化器重建57路径及真BI。

- `fractional_slice_obstruction.md`：任意 m>=2 的分数基数伪客户；全部≤m局部
  真投影、全部 degree预算≤m 条件平方、同一全历史 all-anchor 激励均成立，
  一个始终二阶的整数客户行却为−1/4。不是合法客户或half反例；根W=OPT=1。
- `audit_fractional_slice.py` / `fractional_slice_audit.json`：字面signed数组、完整
  有序历史、分数slice矩阵特征向量与条件平方参数的Fraction审计。
- `monotone_complementarity_root_boundary.md`：普通互补性在共同单调Shapley放松
  中的精确根half分离：完整all-anchor弱占优、W1、OPT=3m/2。非客户模型；
  二阶次模性已经排除它，因此不当作主目标新增障碍。

当前剩余任务是给祖先门槛价格的一般选择及终局相关混合债支付，或另建真实Γ
直接根2W−OPT证书；不继续单独增加正性层次。正文尚待父研究者独立数学攻击；
无外审或新颖性声明。
