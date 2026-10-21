# 连续静态安全接口的本轮检查

主目标 Q-CAG-HALF 仍 OPEN。本分支没有一般证明，也没有真正福利反例。

- `continuous_security_log_boundary.md`：给出 v_cont 的精确定义、与真正静态安全值
  的 Jensen 比较、OPT/(2m−1) 下界，并用每个 m≥2 的整数客户族严格分离最大
  对数势与连续 minimax。自足候选，尚未独立审查，不认证新颖性。
- `audit_continuous_log_boundary.py`：不调用浮点优化或 SPE solver 的 Fraction
  审计，重算查询值与全部通分步骤；不把有限计算作为全称证明。
- `cartesian_catalog_coupling.md`：笛卡尔积目录下 OPT、真正静态安全值和连续安全值
  的可加性，以及联合完整 SPE 的分量投影可以不是 SPE 的八客户例。提示跨分量
  可信惩罚的真实构造机制；实际例 W=OPT，不是主目标反例。
- `audit_cartesian_coupling.py`：独立逐客户核对该策略的全部有序节点和严格投影改善。

下一步应攻击真正的全局义务 W≥(m−1/2)v_cont，或直接原半覆盖；不能把
对数势 KKT 条件误作 v_cont 的最优性条件。任意给定 q 仍提供 v_cont 上界。
旧实际终局删除支持、真实根菜单支持和逐人安全保证已有反例，未在此重做。
