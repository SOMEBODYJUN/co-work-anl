# 随机等槽交换矩的父方独立重构

审查对象：signed_harmonic/optimal_exchange_moments.md，任意m>=1、实际m槽和达到OPT_m的比较m槽，两者可重复，按原模型客户计数c,d。仅为静态最优性的加权表示；没有使用SPE，也没有证明half或signed预算。内部独立重构通过，无外审/新颖性认证。

独立删去最优元组r个槽并从实际元组独立抽r个槽插入，得到合法m槽。一个O客户丢失，恰需它的全部d个最优覆盖槽被删且插入的槽均避开它；概率C(r,d)/C(m,d)乘C(m-r,c)/C(m,c)。O外客户新增概率为1-C(m-r,c)/C(m,c)。期望改进非正，直接得到作者R_r，全部重复槽视为不同抽样位置，因此不需要主题或策略位置可交换。

1/r加权的交集系数，独立使用C(r,d)/r=C(r-1,d-1)/d，Vandermonde给sum_r C(r-1,d-1)C(m-r,c)=C(m,c+d)。恰得到K_m(c,d)=C(m,c+d)/[d C(m,c)C(m,d)]；c+d>m时严格零，c=0时1/d。

对左侧L(c)=sum_(r=1)^m[1-Q_r(c)]/r，L(0)=0。由Q_r(c-1)-Q_r(c)=r Q_r(c-1)/(m-c+1)，再求和并用sum_(s=0)^(m-1) C(s,c-1)=C(m,c)，得到L(c)-L(c-1)=1/c。因此左侧精确H_c。这个证明量化所有m,c，不由有限点拟合。

逆向权1/(m-r)同理：交集分母由r变为m-r，将C(m-r,c)/(m-r)写成C(m-r-1,c-1)/c，得到K_m(d,c)。纯侧为H_m-1/c及H_m-H_d，边界r=0..m-1无除零。

[audit_exchange_moments_independent.py](audit_exchange_moments_independent.py)不导入作者代码，从comb和Fraction独立核对两向核及端点；输出见exchange_moments_independent_report.json。一般性来自上面推导。该行族可复用为signed预算静态输入，但只是已有所有合法OPT比较行的非负线性组合，不能声称引入新的真实SPE激励。缺口仍是早期真实续局与这些静态行之间的非负共同支付。
