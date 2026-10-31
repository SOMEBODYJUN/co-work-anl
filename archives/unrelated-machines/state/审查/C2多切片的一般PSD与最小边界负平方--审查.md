---
id: unrelated-machines/c2-multislice-general-psd-minimal-boundary-square-and-review
kind: review
type_tag: 审查
title: C2多切片的一般PSD与最小边界负平方
status: proved-m-ge3-C2-load-gap-and-m2-negative-square; global-dominance-not-claimed
summary: 一般四阶PSD由完整分解不以实验代替；m2三单项式负平方最小，CONFIG不蕴含方向修句及不同m5运行身份分开。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/reviews/unrelated_machines/c2_unit_multislice_gap_review.md
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/reviews/unrelated_machines/c2_unit_multislice_gap_review.md
---

# C2多切片的一般PSD与最小边界负平方

## 合同、版本与实际范围

8268B/114行主review全文读，另全文读211行最终canonical96863e90ce3893505bbb910c74ea896286b5893be4f487f9efe00d329d9f4b85。UM-C2-LOAD-UNIT-GAP-v1只含全局Boolean one-hot四阶矩、M2 PSD、次数一逐机负载localizer及端剪枝；**不含三阶逐项非负、完整CONFIG或prefix-count localizer**。这是实际调度易解实例上的松弛间隙，不是计算hardness。

已全文比较[当前C2/cyclic双源页](C2单位多切片与循环批量修复双源审查--审查.md)、[有限多切片/前缀页](C2前缀满载与单位多切片有限审计--审查.md)。cyclic调度修复及source-specific prefix信息是另身份，不并入本review。下面补完整分解、m2最小负平方和唯一范围修句，不称新发现。

## 显式矩、radical先于PSD

每m≥3，n=m+1件unit任务在m相同机器上全可用，t=n/m。令x_(j,a)为任务j选机a。重复literal按Boolean并，同任务不同机乘积0。含k≤4不同任务的相容端集S，c_a(S)为机a次数，定义

$$y_S=\frac{\prod_a(t)_{c_a(S)}}{(n)_k},\qquad Lx_S=y_S.$$

n≥4使所有所需分母非零。对未出现j且|S|=k≤3，增加(j,a)的递推比为(t−c_a)/(n−k)。求a和得one-hot守恒；求全部j得N_a=Σ_j x_(j,a)满足

$$L[(N_a-t)x_S]=0\quad(|S|\le3).$$

所以全部线性测试负载localizer为零，且(N_a−t)ℓ（degℓ≤1）与任意degq≤2的Gram乘积为零。此radical来自四次**线性恒等式**，不能循环借尚未证明PSD的Cauchy。

## 完整二次空间与正交Gram

同job二次项先降阶；不同job对的机器核分对称/反对称。对称job数组唯一分u_jk=c_j+c_k+h_jk，$\sum_{k\ne j}h_{jk}=0$，行和映射为(n−2)c+(Σc)1而可逆；反对称分c_j−c_k+h_jk，$\sum_jc_j=0$时行和nc。非harmonic部分用count-null降为一次；机器核additive/gradient在harmonic job系数下本就零，故可取B=B^T,B1=0或C=−C^T,C1=0。

模radical后由常数、双居中一次U、对称job-harmonic×B、反对称job-harmonic×C张成。一次Gram为t/(n−1)倍Frobenius。harmonic与常数/一次交叉因job行和零消去；对称/反对称在same/shared/disjoint任务对的混合分别由交换变号、对称与skew的Frobenius/对角内积零而消去。不是只核纯张量平方便略去任意线性组合。

对称零行和B,C，F=Σ_ab B_ab C_ab，H=Σ_a B_aa C_aa，d=trB trC。相同/共享一端/不交两job对的矩分别

$$D=(t^2F-tH)/(n)_2,\quad O=(-t^2F+2tH)/(n)_3,$$
$$Z=[t^2(d+2F)-6tH]/(n)_4.$$

job harmonic有序系数和分别S、−2S、S，故Gram为S(D−2O+Z)，机器因子

$$K_S=\frac{t^2}{n(n-3)}\left[F-\frac m{n-2}H+\frac d{(n-1)(n-2)}\right].$$

代n=m+1，对角型括号为||B||²_F−m||diagB||²/(m−1)+(trB)²/[m(m−1)]。逐行Cauchy给m||diagB||²≤(m−1)||B||²_F；等号时每行非对角同值、对称性使全体非对角同值，$\operatorname{tr}B=0$再迫$B=0$，故K_S正定。

skew核D0=t²F/(n)_2、O0=−t²F/(n)_3、disjoint0，考虑任务方向后共享系数仍−2S，化为K_A=t²F/[(n−1)(n−2)]正定。job harmonic取正交基便是正定机器Gram的直和。与上述完整张成/正交性结合，给所有二次q的Lq²≥0。

四块维数1、(n−1)(m−1)、[n(n−3)/2][m(m−1)/2]、[(n−1)(n−2)/2][(m−1)(m−2)/2]，故rankM1=1+m(m−1)，rankM2=1+m(m−1)+m²(m−1)(m−2)/2；不是从m3/4数值外推。

## 精确阈值、sup2和正确的CONFIG关系

unit任务n=m+1迫整数OPT2且两件同机达到；常数localizer与总守恒迫任意可行C2阈值T'≥n/m，故本构造的T_C2=t精确。比2m/(m+1)→2。对一般含端剪枝C2，M2对角非负给x≥0、任务和1、常数localizer给分数负载≤T；支撑时间≤T使经典ST给实际≤2T。取可行阈值下确界即可得OPT≤2T_C2，不需下确界达到或精确SDP finder。正OPT时T_C2>0，零OPT逐任务零端另处理，sup2未声称有限例取到2。

同机三不同job矩(t)_3/(n)_3=−1/m^4，所以不是概率分布；三阶逐项非负即排**此证书**。T<2时CONFIG每机至多一件、总m<n，故其阈值2。本族证明C2-load不蕴含CONFIG可行，不证明CONFIG对所有输入能扩成共同M2，因而不能称已证两个松弛的全局支配，也不判C2+CONFIG合取gap。

端数mn=O(m²)，四阶compatible矩最多O((mn)^4)，每项O(logm)位，显式生成按原输入多项式；没有通用精确SDP求解器。

## m2最小三项负平方

m2、n3、t3/2取jobs1,2,3、colors1,2，

$$p_1=x_{1,1}x_{2,1},\quad p_2=x_{1,1}x_{3,2},\quad p_3=x_{2,2}x_{3,2},$$
$$G=\begin{pmatrix}1/8&3/16&0\\3/16&3/8&3/16\\0&3/16&1/8\end{pmatrix},\qquad L[(p_1-p_2+p_3)^2]=-1/8.$$

在常数/一次/compatible二次monomial基，所有对角为1、1/2、1/8、3/8。两基项union≤2为nested/相同或不同job一次项，2×2主块PSD；union3的cross只可能−1/16全同色或3/16的2+1型。一一次一二次时对角乘积≥1/16；两二次全同色各1/8，混色时不能两者都同色各1/8，对角乘积≥3/64>9/256。incompatible cross0。这穷尽所有两项主块，故一/二基项支撑无负平方，三项最小。

n3缺给全部degree3乘子的count-null，不能套n≥4分解；此边界不反驳m≥3一般证明。

## 先验、唯一修句与历史软件

审者multislice_review在读作者前另得到一般n≥4、t_a≥1、Σt_a=n的PSD重构，报告机制为权t_a(t_b−δ_ab) edge内积的additive投影及权t_at_b的gradient投影，冻58272c171faa6d0dd061df210cd073363449584250d2818bef9f6a4bf53f6de9。**本批未取该更一般手稿全文**，不把它升级成本页新定理；已展开的是canonical等容量域。

原审查全文hash5fe91d05aa2d9e05023c14fa26c7b0490a9ad85623a57690e365510ea9506a7f。唯一异议是“严格弱于完整配置”会冒称全局支配；主线程改§1一范围句，审者实际读修稿并逆替换回原句精确复原旧hash，最终96863…接受。该逆核为原review报告；本批核最终SHA，未伪称自己已恢复未知原句原件。两程序hashb3c79a…和b12850…未变。

| 独立完整矩 | dim | 整数缩放 | 结论/rank |
|---|---:|---:|---|
| m2,n3 | 19 | 16 | 零diagonal tail非零offdiag，非PSD；不报失败矩的PSD rank |
| m3,n4 | 67 | 243 | 正pivot、零tail，rank16 |
| m4,n5 | 181 | 6144 | 正pivot、零tail，rank61 |

旧有限页的m2失败输出字段rank4不在本页升级为完整矩的代数rank断言。独立程序先Fraction生全矩再整数Bareiss、每次精确整除，不import规范核心；规范程序走Fraction Schur/LDL。审者还复跑规范默认full m3/4、公式m3..8，去elapsed_seconds后字段同冻结；**没有独立跑m5**。主线程后来m5全矩dim406/rank171属另一实际运行，不能倒填审者。原review还记其只核arXiv1811.08539v3摘要/定理1页3（CONFIG上Ω(n)轮仍≥1.0009 gap）与AppendixB页33–34背景，未下载原字节或重构全文/优先权；本批无新PDF读取。

本批不重跑已处理程序，历史范围不当新run。一般共同配置/计数强化、actual原任务解码、主目标正反及外审/新颖性均未由此关闭。[原件与实际读域](../../../../tools/evidence/um-bounded-bundle-cactus-reviews/README.md)。
