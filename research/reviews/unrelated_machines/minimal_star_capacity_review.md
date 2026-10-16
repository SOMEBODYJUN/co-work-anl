# 极小超载星、共享资源族及多任务压缩的独立冻结审查

UM-TARGET-v1仍OPEN。本审查分别记录一般证明、独立重构、实际有限计算和文献读取，未进行外部同行评审或新颖性认证。

## 冻结对象与审查顺序

基线main `974813e88ff9f80cdda9a1f817be990ce1d90816`。规范正文与代码：

| 路径 | SHA256 |
| --- | --- |
| `research/current/unrelated_machines/minimal_star_contraction_and_capacity_gap.md` | `be27a3e92dc1da3050cedb911798fb35b78a370afc011fbe5dde519f7cf31837` |
| `history/source/literature/unrelated_machines/bamas_et_al_2023_santa_claus_makespan_matroids_v1.pdf` | `fc907ac5159b3b20ae8498052c161f7aaf8d64114db84d7ef1947d6f1c6d4183` |
| `tests/audits/unrelated_machines/minimal_overload_star.py` | `062b2630aded0a125dc57ab9ad14069b712eec6ab8eb3baf6dec471a9c1bb98f` |
| `tests/audits/unrelated_machines/capacity_one_star_pair.py` | `f2a47ff47c9b03e5eaa2f5e747aa97908ebf35f031677251dbf8257cf489732f` |
| `tests/audits/unrelated_machines/independent_minimal_star.py` | `42809e43b35548d5302f4825fcfee7c491e9e81cab90433c8bdfc0ac949134a4` |
| `tests/audits/unrelated_machines/star_profile_compression.py` | `0f0fbc2dc8f3a1f302b3347f5a68076529419cfeae62cef6cf716f9324e19cc1` |

`coupling_hierarchy`在不阅读原路线时先收到第1节精确Claim，独立重构投影、argmin恢复、nested逆序与max(B,T)不累加；再读作者稿及代码。其后编写不导入规范核心的独立审计。`frontier_algorithms`独立验证主研究者提出的第4节显式pair公式，再逐项攻击规范稿第1、3、4、5节；首次规范hash为`d7595a3dc853784ea6c2a5aa768c8f111084a1dcfecc1f8954527603b800581f`。其指出gap比值须显式限OPT>0；最终补入该域、阈值取得及零实例约定，主研究者重新核对，未修改承重代数。下表hash是修补后的实际版本。

第5节来自boss4公屏消息`5f557aa15a544f7aa7d02e24549b6ca1`；主研究者与frontier_algorithms先独立检查其zero/∞分支及matching论证，再写入共同正文，不能冒称新作者独占。

## 承重重构与攻击

1. 极小星必须取剪枝后全部邻域。旧T调度外放至少一条，min≤其代价；任意新B调度取达到min的真实任务，其余放回v，负载≤max(B,T)。反向不需B≤T，正向却不能扩大到旧C>T。
2. 每替换任务代表不交原任务叶集；逆序时argmin机器已存在，children只展开一次。不发生重复任务/指数重建，负载界反复取max而不相加。F≥2、无零项，≤m轮及O(m²n)有理操作成立，p位长不增。
3. 紧凑族：X有全局容量k−1迫一中心接X，局部k个Y占k of k+1槽，最多撤一Z；θ上下界真实覆盖所有调度。配置边际由实际支持重算，没有把原SC结论直接移用。
4. GPC2对多eligible任务只要求pair支撑不相交；不错误要求每pair恰覆盖1。各类pair均有正确完整边际：G-G/R-R循环置换；V-R、V-G逐行逐列公式核验。其余pairs支持任务集合确实不交，乘积分解合法。没有假设所有pair可拼成全局分布。
5. 组合合同仅需对每个接受T用ST及逆恢复给≤2T，再取inf；无须猜测组合预处理对T单调。原族T<1时Y剪空域，T1两种规则均无起点且GPC2证书可行。
6. q-profile障碍：A调度如有零任务或正任务共机，则其正负载机器数≤q−1，原调度在对应B-profile仍可行，矛盾。故每个删一外机的A图有完整matching，单任务邻域至少2；两个邻域相交又可构造B可行分配。此证明覆盖所有非负/∞替代时间，只限q个普通任务及固定外机，不能排除带身份或辅助结构的算法。

在以上声明范围内没有仍成立的fatal objection。发现的比值域省略已修补。文献原始字节版本取得与证明全部内化仍是不同轴；AppendixB没有被宣称已重构。

## 实际有限核验

规范单步审计：seed837210，4000采样矩阵，956个适用星、3972个新调度提升，含776异长星与563含零矩阵。新增5000采样/2强制nested输入：122条多步链，123个nested步骤，83拒绝证书，89712个最终调度逆序恢复。k2紧凑星全部82944个分配独立整数放大求OPT3/2。

独立程序seed918273：1095个合法fixture，每fixture全部分配；92次收缩，369拒绝均真不可行；7486个最终分配逆提升，其中7个真正nested残余fixture和8个nested最终分配。未导入规范收缩或恢复核心。

全pair审计k=3,…,12：50179机器对，99363个显式联合项；45309个其余对以支持集合分离及精确乘积分解验证，不伪称每项展开。逐机不可消去、逐任务可用机数、全部配置覆盖与负载均独立重算。q-profile审计实际q=2,…,8，枚举A/B profiles与各自剪枝后的全部原星分配；它不枚举所有可能替代矩阵。

实际命令、版本、源hash和全部JSON在`evidence/runs/unrelated_machines/minimal_star_capacity_audit.json`。所有算术为Fraction/整数，没有容差；有限证据不替代一般证明。

## 同行更新合入复核

安全同步到`3655fb2`后，主研究者完整阅读GHMR/共享逃逸正文与冻结审查，以及五机tree-Markov正文与审查。它们没有反驳本稿声明；GHMR的精确单槽/大候选合同与下一资源池路线存在重叠，后续需去重或明确新版本。共享账本不同身份全部保留，生成稿由共同源重建；未修改同行数学正文或冻结证据。
