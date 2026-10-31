---
id: "unrelated-machines/c2-unit-gap-fraction-schur-finite-replay"
kind: "computation"
type_tag: "计算"
title: "C2单位伪矩的有限 Schur 消元与颜色公式复跑"
status: "one-original-CLI-full-m3-m4-formula-m3-through-m8-replayed"
summary: "原Fraction程序对m3/4完整M2、全部给定线性递推/localizer及秩做精确Schur，对m3..8指定对称/反对称颜色核做公式回归；本轮一次，历史m5/Bareiss/证书检查不倒填为新执行，任意m一般PSD由数学稿承担。"
source_refs:
  - "clean:8774f80cc59169768733"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:tests/audits/unrelated_machines/c2_unit_multislice_gap.py"
legacy_ids:
  - "UM-C2-LOAD-UNIT-GAP-v1"
---

# 1. 原代码与精确合同

原6513B、SHA `b3c79afee6c44e1d4d1df3a1e7f110ac57f17b9e7432055c857c55beebde0395`逐行完整读。它不导入solver或另一实现；Fraction算下降阶乘、有限矩阵与精确Schur。只接受m≥3，n=m+1，所有job在m机上耗时一，t=n/m。C2-load只含共同degree4 M2 PSD、Boolean/one-hot守恒与degree-one逐机load localizer，**没有**全局triple非负或完整单机CONFIG。

对相容端集S，k≤4个不同jobs、每机器a有c_a个端，原矩为

`y_S=Π_a(t)_(c_a)/(n)_k`。

同job不同机器的冲突monomial定义零，重复同变量按Boolean合并。分母(n)_k不为零，因为m≥3给n≥4。程序用compatible monomials枚举到degree3检查所有job one-hot等式和每row计数递推；不相容乘子原本全为零。再用degree≤1基S,U逐条核`(t−N_a)`localizer entry为零。

三不同jobs同机矩明确为`−1/m^4`。因此这些数不是概率分布，不满足triple非负；T<2时CONFIG每机至多一个unit job，m机不能覆盖m+1个jobs，故该证书不是C2+CONFIG证书。不能借同批真实parity分布的直观来把此处负矩解释成真实law。

# 2. 完整M2与零pivot规则

基为常数、所有single端及不同job的所有two-end monomials；同job冲突已代数约零，重复powers约Boolean，所以该基张成完整degree≤2商空间。M2[S,U]=moment(S∪U)。`exact_psd_ldl`复制矩阵后逐个Fraction Schur：每pivot必须≥0；pivot=0时余下该row必须全零，否则报错。正pivot才更新右下对称块并计秩，不把奇异矩阵强行除零。

原规范参数默认`--full-m 3 4 --max-formula-m 8`；本轮显式按这组参数实际CLI一次exit0，结果如下：

| m/n/t | onehot等式 | row递推 | 零localizer entries | M2维/秩 | 最小正pivot | 同机triple |
|---|---:|---:|---:|---|---|---|
| 3/4/(4/3) | 700 | 525 | 507 | 67/16 | 1/90 | −1/81 |
| 4/5/(5/4) | 4105 | 3284 | 1764 | 181/61 | 5/1536 | −1/256 |

代码核秩`1+m(m−1)+m²(m−1)(m−2)/2`、正pivot数等于rank。表中完整矩阵是有限两个m，不是所有m的一般SDP运行。程序输出integer_OPT=2和比值3/2、8/5；它**没有枚举求整数OPT**：真实值由m+1枚unit jobs的pigeonhole下界二和显式“某机两job、其它每机一job”上界证明。

# 3. 颜色公式实际检了哪些核

对每m=3..8，取零和v=(1,−1,0,…)及对称B=vv^T；另取前三颜色的有向3-cycle反对称C。它们是每m的一对指定非零测试核，不是枚举全部B/C或所有多项式。

程序逐颜色分配（degree2、3、4）计算D/O/Z，与

`D=(t²||B||²−t||diag B||²)/(n)_2`，

`O=(−t²||B||²+2t||diag B||²)/(n)_3`，

`Z=[t²((trB)²+2||B||²)−6t||diag B||²]/(n)_4`

比较；再核对称四点平方范数`4(D−2O+Z)=4K>0`，反对称cycle平方范数`3t²||C||²/((n−1)(n−2))>0`。全部六m都过，完整有理值在stdout。这个color regression支持公式实现，不以一对核的正值推一般矩PSD。

当前1a2d…原数学稿已自足证明任意m≥3：将二次空间模row/one-hot radical分成常数、一次块、对称及反对称harmonic块，证明张成与正交、机器Gram正定并算秩。[一般PSD与边界审查](../审查/C2多切片的一般PSD与最小边界负平方--审查.md)保这条一般证明；一般族的显式C2阈值恰t和supgap2由该解析证明及ST上界承担，本页不重复登记新定理或把finite elimination取代它。m=2的负平方亦由原审查另给，不属于当前m≥3 CLI的数值输出。

# 4. 旧冻结的更大范围与本轮必须分开

历史36d313…5008B联合记录有两个原命令：规范`--full-m 3 4 5`，以及另一个独立整数Bareiss脚本。其primary含m5维406/秩171、最小pivot1/700；独立数组含m2失败及m3/4通过；还记录m3显式256moments、81原schedule检查。这些数据本轮完整读作历史比较，**没有**再执行m5完整M2、Bareiss、m2或该certificate-check。

本轮只将新m3/4记录与历史primary相同m的所有数学字段比较（移除elapsed_seconds），颜色m3..8也逐值相同。代码SHA相同；历史正文SHA是早前版本，当前1a2d原稿有后续§9/10，不把sourcewhole hash不同抹成字节相同。时间字段只记运行环境观察，不作复杂度benchmark。

[既有C2满载/多切片审查](../审查/C2前缀满载与单位多切片有限审计--审查.md)保旧两路运行；[新证据](../../tools/evidence/um-following-five-audit-primary/README.md)保本轮明确参数、全stdout/stderr与比较规则。当前新增数学过程1次，supplemental0，外审/新blind0。没有generic SDP、C2+CONFIG可行证书、一般UM困难性或全参数数值穷举。
