# 完整矩阵平方的闭式初态与十五件交换：新增结构全文独立审查

这是独立Exact-first重构、旧作者全文读后审查之后的**新增读取事件**。不把旧 `kronecker_author_read_after_review_v1.md` 当作已经审过本结构证明。

## 本次实际全文读取与版本

- `hardness_amplification/STRUCTURAL_PROOF.md`，SHA256 `794d71f3776b3a3736387ea68ea476d4e4f43966c32ed84ea63ab6dae9cc6512`。
- `hardness_amplification/verify_structural_schedule.py`，SHA256 `fdac347bda65808e552b51ee017154c35c22ced1ceaee143c3e23f5adab1d187`。
- `hardness_amplification/structural_verification.json` 全部100项actual assignment和13行balance，SHA256 `65b2356d337c0d24bdc4ba7269257f23b7d8a67e2ed4d4f7bcfc43aa3511a85e`。

完整矩阵/资格/机器和任务索引沿用已独立核过的作者原Exact。审查者没有执行会原位重写作者 `structural_verification.json` 的脚本；在自己的目录另写 `verify_structural_read_after.py`，不导入作者checker/search，直接按原资格与数学初态重构，并比对作者现有json。结果另存 `kronecker_structural_independent_audit.json`。

## 闭式初态的逐类推导

四种job types的数量是4、16、16、64，恰为全部100件。

(A_g,A_h)→(S_gh,S_hg)为原资格；不同(g,h)给不同selected SS机器，共4台。任一SS机器(S_gl,S_hk)，若l=h且k=g，就是selected，其四枚incidence×incidence全部导出RR；否则四枚都留SS，各1/4，合计1。故全部16台SS初载1。

(A_g,B_hkc)→(S_gh,R_{c,k+hc})。给定一台SR机器(S_ga,R_cd)，必须h=a，而k=d+hc恰唯一，因此此映射是16枚原任务与16台SR机器之间的真实双射，各负载1。RS完全类似：给定(R_ab,S_hg)，l=b+ga唯一。未忽略任何mixed jobs。

RR层固定(a,c)后，实际映射是(g,h)→(b,d)=(ag+h,g+ch)。F₂上的线性矩阵为[[a,1],[1,c]]，行列式ac+1；除a=c=1外都可逆，每台对应RR收到一枚unit。a=c=1时b=d=g+h，两个对角像各有2原像，两个非对角像无原像。所以完整64机初载只有(R10,R10)、(R11,R11)为2和(R10,R11)、(R11,R10)为0，其他60台为1。公式和满映射分析通过，不靠MILP。

## 十五件替换的完整攻击

独立脚本按原机器顺序S00,S01,S10,S11,R00,R01,R10,R11与原job顺序A0,A1,B000,…,B111读取每一个明示job pair，确认15个pair两两不同；逐项确认表中old确是闭式初态给出的端，而不是任取的另一个端；逐项确认new的两个坐标都是原资格，再用Fraction乘积重算old/new真实处理时间。

全部100件最终job恰执行一次。全部13台受影响机器的“移出量/移入量”精确重算与证明表完全一致：4台各1/2↔1/2，5台各1↔1，两台对角各移出1，两台非对角各移入1。其余51台毫无变化。因此最终64机均恰1，且作者json的全部100项最终assignment与独立重构完全相同。

这是一组**同时替换**的完整实际调度证明；不应增加“每个顺序中间调度都≤1”之类本段未证明也不需要的动态合同。原初态本来有峰2，不影响最终上界。

## 其他攻击与边界

“相关机带资格限制”解释正确：原job size为selector2/incidence1，原machine speed为state2/resource1，所以每条原有限p=size/speed。平方size、speed对应乘积；总size与总speed均144。其正权总容量恒等迫使任何≤1实际调度全部行饱和，与本结构的精确结果相符。

这组显式有限公式/交换足以写成canonical自足反例；可以把原优化器证书作为独立第二份证书保留，而不让数学有效性依赖优化器状态。

“旧裸菜单t=2为5/4”的跨文件对照不是本新证明的必要前提；当前仓库 `cartesian_menu_recoupling_and_coordinate_consistency.md` 表确把旧裸菜单实际OPT列为5/4，但应写清是旧不同矩阵的Cmax，不与本完整tensor混用。

## 结论与真实范围

本次闭式初态、2×2缺陷、15原任务同时替换、所有原资格与最终64行负载都通过独立代数和精确回算；新增结构版本无standing fatal。

完整张量平方的OPT=1与seedOPT=3/2、所有偶次幂OPT=1均可保留。一般未剪枝LP乘法另见v1读后审查，不把本有限结构当作该泛化的证明。

它只关闭全域完整Kronecker产品的自动NO放大，不排hard-image限定的产品或新真实一致性gadget；没有NP-hard源、没有主目标正反解答、新颖性或外审认证。全部作者原文件和共享仓库均未被本审查修改。
