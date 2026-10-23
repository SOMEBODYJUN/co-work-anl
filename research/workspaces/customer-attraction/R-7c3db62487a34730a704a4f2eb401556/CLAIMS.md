# 精确个人研究账本

本页登记本工作区资产，不自动提升共享 canonical 状态。主目标 Q-CAG-HALF
的对象、量词不变，仍 OPEN；外审和新颖性均未认证。

## CA-ANCHOR-PRIVATE-SEAT-SPECTRUM-v1

- **Exact Statement / Objects / Domain：** CAG-MODEL 的每个有限实例、任意 m≥1、
  每个全部有序历史依赖纯 SPE。取实际覆盖 C，所有包含极大主题 B_j，
  P_j=B_j\∪_(l≠j)B_l，Q_j=P_j\C，a_j=|Q_j|。
  在每个实际位置 i 取 r=m−i+1、前缀负载 b_i，令
  β_ij=Σ_(x∈B_j\Q_j)1/(b_i(x)+r)，λ_i 为所有
  a_j/k+β_ij（j全体、1≤k≤m）的第 r 大值。
  则对每个 i 有 u_i≥λ_i，故 W≥Σ_iλ_i。
- **Quantifiers / Assumptions / Definitions：** 对全部实例、人数、完整纯 SPE
  和实际位置全称；保留任意平局、空主题、重复和零客户。比较块从实际终局
  固定后，在离轨树中不更换；β 在每个 anchor 子树中固定。
- **Scope / Conclusion：** 联合私有席位与共享遗漏/已覆盖客户的前缀基线；
  是后验必要预算，不是一般 half，也不是输入端均衡选择算法。
- **Dependencies：** 旧 superset 残余席位归纳、全局私有块、同终局子主题支配、
  单位客户份额与全部历史的真实偏离最优性。
- **Evidence：** 自足任意人数解析归纳；主代理先见公式独立重构；有限精确回归
  30 实例、174 可实现有序路径、548 位置行、30 完整策略证书，仅检查实现。
- **Counterevidence / Objections：** 无已成立的本命题致命异议；下一条明确否定
  仅用此谱加全部分数覆盖行即可闭合一般 half 的接口。
- **Status：** 已有解析证明及内部独立重构；个人资产，未作共享正式整理。
- **Related Files：** [正文](omission/joint_omission_prefix_spectrum.md)、
  [作者复现](omission/audit_joint_omission_spectrum.py)、
  [冻结输出](omission/joint_omission_spectrum_audit.json)、
  [独立审查](parent/joint_spectrum_independent_review.md)。

## CA-JOINT-SPECTRUM-FRACTIONAL-NOSUFF-v1

- **Exact Statement / Domain / Quantifiers：** 对每个整数 m≥13，存在有限单位客户
  共同目录和一条确定有序路径，该路径满足上一条联合谱全部位置行以及
  对每个可覆盖客户集 E、每个分数覆盖总重 τ 的全部真实形式前缀行
  |E|≤P_(i−1)+(m−i+1)τu_i，但有 OPT_m>2W。
- **Objects / Definitions / Assumptions：** L=lcm(1,...,m)，K=(m−1)L。
  m 个 B_j 的每对共享 L 名独有客户，另有 m 个不交银行 A_r，大小 K/r；
  路径 A_m,...,A_1。这里明确不假定该路径为 SPE。
- **Conclusion / Scope：** 必要预算接口不充分；不是主目标反例。
- **Dependencies / Evidence：** λ_i=u_i=K/r，W=KH_m，OPT≥mK/2；
  m>4H_m 对全部 m≥13 的有理基础值与差分证明。
  所有主题大小≤K，直接推出对全部 E、全部覆盖的前缀行。
- **Counterevidence / Objections：** 原路径在倒二节点存在严格盈利偏离，
  且偏离后末位唯一选 A_1；因此已证明不能由任何 SPE 实现。
- **Status：** 解析方法障碍与定义级不可实现性，内部独立重构；不改变 Q-CAG-HALF。
- **Related Files：** 同上正文第 4—5 节及独立审查。
