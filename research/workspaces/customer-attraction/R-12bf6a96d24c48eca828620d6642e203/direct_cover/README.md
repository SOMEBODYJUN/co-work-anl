# 直接覆盖分支：弱匹配、真实入场者值及其跨前缀障碍

状态：一般 Q-CAG-HALF 仍 OPEN；本分支没有给出新的半覆盖承重引理。

主资产是 [actual_prefix_relay_obstruction.md](actual_prefix_relay_obstruction.md)：复用61客户输入，构造实际路径 BAAF 的完整 SPE，同时否定真实偏离值、可信入场者最小值及节点最大值的比例前缀中继。root 已独立按单位客户重构259历史、1295个非自身真实偏离，并独立证明 f4=9、f3=13；父审计保存于相邻 parent 目录。五客户全背景族是任意额外固定动作版本的更简短对照。

## 当前精确义务

固定完整纯 SPE 的实际路径及达到 OPT 的 m 元组 T，令 V(i,T) 为实际位置 i 首次偏离到 T 后、沿同一策略的真实收益。以下三个义务必须区分：

1. **弱匹配**（充分推出 half）：存在某个最优元组及一个排列 pi，使 `sum_i V(i,T_pi(i)) >= OPT-W`。
2. **弱平均**（更强，充分推出 half）：`m OPT <= m W + sum_ij V(i,T_j)`。
3. **旧强平均**（更强，充分推出 `2-1/m`）：`m OPT <= (m-1)W + sum_ij V(i,T_j)`。已有两人任意背景证明在 `research/current/customer_attraction/global_new_uniform_portfolio_two.md`；任意人数未证。

原 portfolio_matching 反例只否定支付 `|O\C|`，没有否定弱匹配的 `OPT-W = |O\C|-|C\O|`。全分布安全预算反例比较独立查询 C_i，不直接否定这里的真实偏离 D_i。没有将有限计算当作这些义务的证明。

## 一个精确压缩

固定一条 SPE 可实现的实际有序路径。所有首次偏离实际行动的分支互不相交。可分别以任意完整 SPE 续局替换每个这样的子树，而不改变实际路径。令 `f_r(b,T)` 为固定前缀负载 b、首位已经选择 T 后，余下 r-1 位所有合法完整纯 SPE 续局中该 T 入场者的最小收益；有限性保证最小值存在。把每个首次偏离子树替换为达到该最小值的子树，仍为 SPE，因为实际节点的偏离选项收益只会下降，替换子树内部则仍满足 SPE。

所以弱匹配/平均的普遍命题可等价地只针对同时最小化所有实际路径首次偏离选项的策略：非实际行动处 V(i,T)=f_r(b_i,T)，实际行动处 V(i,S_i)=u_i 保持不变。规范 solver 的 certificate 默认使用同一 min-continuation 原理；这里没有宣称新的均衡压缩定理。

## 已失败的较早交换桥

尝试用统一的人数比例将这些可信入场者值沿实际前缀传递：

`f_r(b,T) >= (r-1)/r * f_{r-1}(b+A,T)`。

此桥为假。它在 5 客户、3 主题、任意正背景重数的统一族中失败；该族的附加固定 A 不一定是实际行动，故另检查了 actual 限定。完整解析证明见 [incumbent_lipschitz_obstruction.md](incumbent_lipschitz_obstruction.md)；定义级 Fraction 核验见 [verify_incumbent_obstruction.py](verify_incumbent_obstruction.py)。该反例把后续跟随者收益从 P 转移到 B，说明不能只保留某一入场主题标量值，再把固定一个未来行动的影响按人数比例结算。

[actual_prefix_relay_obstruction.md](actual_prefix_relay_obstruction.md) 进一步复用61客户输入，给同一完整SPE的实际路径 `(B,A,A,F)`：真实偏离 `V1,A=9 < (3/4)V2,A=39/4`。故把额外行动限制为实际当前行动也不能修补单主题比例递推。完整259历史证书和不导入规范代码的核验器都在本目录；核验PASS。该文也给可信入场者最小值版本的直接六行证明。

这不否定弱匹配、弱平均、旧强平均、真正聚合安全值或主目标。下一个有判别意义的机制须保留至少 B 的替代信用，或使用真实跨分支中继；再调单个入场者比例没有依据。

## 诊断代码及边界

- `check_weak_matching.py`：规范现成证书的精确匹配诊断，输出 `weak_matching_existing.json`。忽略了嵌套 schema 的若干文件；不能声称扫描了全部证书。
- `lp_weak_matching.py`：对固定完整策略锥的 LP 诊断。少量 m=4,k=6 与 m=5,k=7 策略锥没有分离强平均；没有一般结论，已停止扩展同类随机扫描。
- `check_incumbent_lipschitz.py`：先在既有 `dynamic_iid_local.json` 中找到该比例桥的失败，保存原诊断 `incumbent_lipschitz_failure.json`；随后压缩得到上述独立 5 客户族。

不运行 git/work.py；由 root 统一 checkpoint 和通信。
