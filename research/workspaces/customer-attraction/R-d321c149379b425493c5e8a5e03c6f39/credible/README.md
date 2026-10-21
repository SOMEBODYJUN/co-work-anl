# 可信完整 SPE、结构极端与独立攻击

本目录保持 CAG-MODEL 与 Q-CAG-HALF 的全部量词：共同有限目录、单位客户/提供者、任意人数和每个完整有序历史纯 SPE。一般 half 仍 OPEN。

- `weak_iid_independent_review.md`：对 security 新的固定 102 主题弱 iid 桥反例作盲独立完整策略、Nash 支持唯一性、m≥41 与 m20 有理分离重构；读发现稿后再逐条核对。未见 fatal。
- `audit_weak_iid_independent.py/json`：零导入单位客户完整有序树核验 J=2,3，m=2,...,6，共 31668 个动作比较；独立有理阈值证书。
- `copy_floor_twin_review.md`：对 independent 的首次包含 DP 的孪生障碍作独立重构，得每个合法前缀精确 L=K/r+1、G=KH_m+m。另独立证明该等大孪生族的每个 SPE 都完全有效率。给出近包含有损比较与 myopic 上界剪枝接口（independent 已实现后者）。
- `audit_copy_floor_twins.py/json`：独立 DP 的 m≤4 全合法前缀 Fraction 核验及 m5,K12 的 G=162/5<OPT/2=65/2 证书。
- `two_pool_inverse.py/json`：两独立 bait 池的单 fresh 组、末三人完整策略联合 MILP 探索。浮点最优目标 a−x/2 为 0，仅保存数值定位；边界参数 x2,a1,b1=b2=2,d1=d2=1 的完整策略已从规范策略锥抽取并精确核验。没有对整族提升为一般不可能定理，也不是 half 反例。

下一步：myopic 剪枝 DP 仍把“即时收益够高但真实最终收益不足”的后继保留，需独立攻击或找共同支付；多后继跨 core 的完整报复仍未有新可信低福利族。
