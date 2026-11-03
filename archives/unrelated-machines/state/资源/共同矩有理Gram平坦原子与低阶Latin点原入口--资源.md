---
id: "unrelated-machines/global-flat-moment-original-gram-and-atom-extractor"
kind: "resource"
type_tag: "资源"
title: "共同矩有理Gram平坦原子与低阶Latin点原入口"
status: "complete-primary-read-and-one-original-main-run"
truth_status: "explicit-rational-moment-audit-with-stronger-test-validator"
summary: "保312行helper的强验证合同、共同缺陷Gram、flat原子分裂及四个真实分布/Latin4低阶点；新目录原main一次完成，不把它混作弱C2-load或一般SDP。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:tests/audits/unrelated_machines/global_assignment_flat_moment_audit.py#全文"
evidence_manifest: "archives/unrelated-machines/tools/evidence/um-ghmr-flat-moment-and-hall-primary/README.md"
---

主源e3f0fcf717accc012b76全文312行、16133B，SHA1dfcaee91aaa6886dae201f5b796decbab9e2b667bb96ff24285a6a00c118666。此前作为near-flat独立代码的有理helper已有来源登记，但没有找到本文件独立main的完整输出；本次只对它在新空目录执行一次，Python3.12.14、退出0，完整JSON、stdout/stderr、真实命令/耗时/代码与输出SHA见[证据包](../../tools/evidence/um-ghmr-flat-moment-and-hall-primary/README.md)。其他四主源原main未重跑。

已有[全局矩审查](../审查/全局指派矩轮廓冻结审查增量--审查.md)保存near-flat条件定理及HS二倍反例；本helper不是那个主算法，不重新授定理，也不将它的强测试条件加入较弱的C2-load数学合同。

## 共同有理矩与本文件的实际验证域

原job由有限机器→非负有理时间的显式字典给出。变量e=(machine,job)，幂按Boolean合并；同job两个不同端相乘为0。build_moments从明确列出的正有理权真实调度生成兼容次数≤2r矩表。演示全部r2；实际提取函数只读jobs、T、r、variables、y，不读造矩原子。

validate要求空矩1、所有存储条目在[0,1]、次数≤2r−1的逐job one-hot守恒，以及\(M_{r-1}\)、\(M_r\)的PSD。它还对每机器检查负载localizer和**每个正时间阈值的计数localizer**：

\[
L((T-\sum_{e\text{在i}}p_ex_e)q^2)\ge0,\qquad
L((\lfloor T/a\rfloor-\sum_{p_e\ge a}x_e)q^2)\ge0.
\]

这比现行near-flat定理仅需的四阶共同PSD/one-hot/负载localizer更强；定理不要求逐个四阶条目非负或prefix-count localizer。此helper拒绝某证书不能据此反驳定理或断言普通OPT>T。它没有SDP或矩生成器，不是全面验证任意外部输入格式的求解器。

psd_exact用对称Fraction Schur消元，负对角拒绝；剩余对角全0但有非零块也拒绝，不能把“没有正pivot”误作PSD。返回正pivot数量及独立单项式索引。无浮点谱分解、容差或数值特征值。

## 共同压缩、缺陷与真正flat提取

从低阶Gram选独立基b，\(G=L(bb^\top)\)，\(H_e=L(bb^\top x_e)\)，\(A_e=G^{-1}H_e\)，内积是G。代码检查\(0\preceq H_e\preceq G\)、\(G(A_e-A_e^2)\succeq0\)、每job的A和I，以及共同残差块

\[
J_{ef}-H_eG^{-1}H_f,\qquad J_{ef}=L(bb^\top x_ex_f).
\]

联合残差Gram的秩恰为高低矩秩差。共同矩使
\[
[A_e,A_f]=B_f^*B_e-B_e^*B_f.
\]

程序逐对验证此式；所有合法例在常数state \(v_0\) 上的缺陷/交换子均为0，却可有正全空间迹缺陷Δ。机器真实平均负载饱和T时，再检查整个压缩负载算子恰为TI，不只检查常数向量。

flat_extract首先完整validate。若高低秩不同，返回None及检查信息，**不宣告无可行调度**。若同秩，所有二次向量已在低阶空间，A为两两交换的自伴投影、逐job和I。把常数向量逐次分成 \(A_eu,(I-A_e)u\)，丢G范数0分支；正分支互相正交，最多R个。每分支恰为每job选一个真实端，权为G范数平方；代码逐件回算实际负载≤T、权和1，并重构全部输入矩条目。仅保存常数state缺陷0不够触发这条flat合同。

## 本次原main的全部内置点

| 点 | 输入/分布 | rank低/高 | 全空间缺陷/实际结果 |
|---|---|---:|---|
| 宏微共同flat | 5jobs/4机器；宏0或1端时间1；各home两微任务home1/2、专属sink1/4；原子(0,2,2,1,1)和(1,0,0,3,3)各1/2，T1 | 2/2 | Δ0，恢复同两原子，全部211四阶条目相同 |
| 独立全分布 | 4个unit job、2机器，全部16个分配均匀，T4 | 5/11 | Δ6，flat_extract返回None，但输入本就有真实可行原子 |
| 相同一阶的压缩law | 同4unit jobs，all0/all1各1/2，T4 | 2/2 | 可flat提取，和上一行单端边际相同，但二阶矩及整个M1不同 |
| balanced最优law | 同4unit jobs，恰两件到每机的6个分配均匀，T2 | 4/6 | Δ4，两机器负载算子均饱和，仍不flat |

第一例10个端，M1/M2行数11/51、守恒655次、饱和负载null检查102次、残差Gram20行秩0；恢复最大同时分支数2。独立四job例M1/M2行数9/33，联合残差Gram40行秩6；balanced残差32行秩2。这些是明确给定真实分布的有限证书，不是所有伪矩上的测试覆盖。

“Carathéodory保一阶不保整份M1”的区别在代码中具体体现：独立law的跨job同机器二阶值1/4，all0/all1压缩law为1/2。末尾general_same_state_confidence_bound字符串是一个附带数学指针，本main没有对所有偶n运行该界，也不能把字符串当一般证明。

## Latin4：低阶指示矩，不是完整调度局部化器

16个三元组为\((x,z,x+z\bmod4)\)。令每单点均值1/4，Q对角1/4，完全坐标不交对为1/8，其余0。原main检查增广一二阶矩PSD秩7、协方差秩6、Q每行和1，并穷举1820个四三元组子集确认无perfect3DM。

本批另作有限独立代数核对：将三元组按\(\mathbb Z_4^2\)索引，16倍协方差的平移核在(0,0)取3，三个坐标差均非零处取1，其余−1。16个精确字符和均为0或8，正值恰6个，故协方差PSD秩6、增广矩秩7；完整整数结果另存JSON。没有数值特征值。该点只是三元组指示变量的低阶共同PSD，未给degree4 assignment one-hot或逐机负载localizer，不能作为C2调度gap2证书。

## 输入输出、历史与边界

本main全部输入内置于代码。证据另冻四个分布的所有jobs/原子和Latin16三元组，注明这是内置输入的文档化展开，不是CLI读取的外部参数。CLI必须给--output，它会写该路径并打印摘要；本次保证目录和输出事前不存在，没有覆写任何旧结果。独立新数据自查重建211个矩条目和四组feature秩，检查26个原子共106次原job资格/负载；此数据核对不计作另一次原main运行。

旧freeze登记本helper精确SHA，但其canonical_path_reruns只列near-flat主程序、独立HS及full-HS，不能称早已运行本helper的独立main。现行数学正文c49e7…与旧5ec060…只差第13/16/18行两个尾空格，本批已反向恢复并核旧SHA；原review附节解释其ad9af3…旧前缀身份，未新增盲审。经典flat机制、给定证书算法、近平坦生成义务、指定HS反例和本helper有限运行保持不同身份；一般UM目标未解决。
