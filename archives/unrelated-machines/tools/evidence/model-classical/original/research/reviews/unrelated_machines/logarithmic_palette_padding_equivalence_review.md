# 单一对数字母表与私有多项式填充的独立审查

日期：2026-10-19。仅审正文§8的 `UM-DENSE-LOGARITHMIC-ALPHABET-PADDED-EQUIVALENCE-v1`。§6–7原身份与证据保留；本审查不把旧全文hash改为新全文hash。

| 实际最终读取对象 | SHA-256 |
|---|---|
| `research/current/unrelated_machines/model_and_classical_barriers.md`，仅§8数学范围 | `1cbb777776fc4047a70e00396b7b12903ac890343ef6d3f0ee15c0d7bf10512b` |
| `tests/audits/unrelated_machines/logarithmic_palette_padding_equivalence.py` | `6f3b3c11815f82eb51f03ae63e529288898ddd4fab2022656f3af36b1e242391` |

## 独立重构与实际读取

`independent_frontier`先只获得A_N的公式、目标存在性等价和允许固定k指数的padding合同，自行重构独立尺度/阈值接口；冻结自己的重构后才通读作者证明。其后实际通读canonical§8和全部规范审计代码，并重跑。最后正文的式号引用由旧(1)..(9)改为(8.1)..(8.9)，该研究者又实际重读完整§8并核最终hash。root另行逐式核对。

## 承重义务与攻击

1. A_N只依实际job数N，既不依原n、阈值或k，也不把epsilon当未编码oracle。所有r=0重复值合为1，指数总和≤floor(H/2)，故确为O(logN)而不是对每个k另选字母表。
2. 取固定k后E=2^k·8k·ceil(log2(8kn))，N=2^E是原n的固定次数多项式；该次数可极大且依k。这是存在性等价，未声称可变二进制k下统一多项式。
3. 第k网格r终点确为8k·ell，二项式给b^(8k)≥2，范围覆盖8kn；非哨兵值≤N，N²严格独立。
4. 原n个active jobs每机累积至多n次加一误差，不能错误收费N。全部N−n dummy各有独占time1机器；跨dummy、dummy到原机、原job到dummy都是N²，故合格输出必须完整走私有边。
5. 正OPT时L≤OPT≤U≤nL；首个T≥OPT有T≤bOPT。逐机强界OPT(Q)≤b(8kn/T)OPT+n避免额外阈值乘损失，回译αb²=2−1/(2k)−7/(32k²)−1/(64k³)。N²大于所有合格负载，排除每个坏输出而不只某个YES调度。
6. n=0、全任务各有零端、部分零端、∞、单机单任务、大分母均有明确分支。所有输出先完整验证再按原P求和；舍弃某个候选不当作可靠FAIL。
7. 矩阵确须显式写全部padding行列；理论复杂度按实际输出规模收费。审计对天文padding只给精确完整负载分类，未假称真的物化矩阵或执行未知B。

## 有限证据及限度

规范命令：`python3 tests/audits/unrelated_machines/logarithmic_palette_padding_equivalence.py`。其[冻结JSON](../../../evidence/runs/unrelated_machines/logarithmic_palette_padding_equivalence.json)记录seed20261019、Python/代码/证明hash、1574份matrix/k输入、10890份active完整分配型、2993份合格输出型及1390个完整private分类。代码用Fraction核130个H值、2481个标量边界和999个固定k恒等式。独立研究者及root均实际重跑规范程序。

有限分类不是一般证明；未提供backend B、NP源gap或source decoder。**判定：最终§8限范围证明无尚成立fatal objection；外审与全球新颖性未认证，主目标正反面仍OPEN。** O(logN)结论允许增加job数，不能静默替换原§7的same-n合同，也不声称该大小最优。
