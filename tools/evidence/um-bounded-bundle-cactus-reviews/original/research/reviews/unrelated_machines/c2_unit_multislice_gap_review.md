# UM-C2-LOAD-UNIT-GAP-v1 独立攻击审查

日期：2026-10-17。审查者：multislice_review。未修改仓库、未导入规范审计核心。

## 审查对象及三 SHA256

| 冻结对象 | SHA256 |
|---|---|
| research/current/unrelated_machines/c2_unit_multislice_gap.md | 5fe91d05aa2d9e05023c14fa26c7b0490a9ad85623a57690e365510ea9506a7f |
| tests/audits/unrelated_machines/c2_unit_multislice_gap.py | b3c79afee6c44e1d4d1df3a1e7f110ac57f17b9e7432055c857c55beebde0395 |
| tests/audits/unrelated_machines/c2_unit_multislice_independent.py | b12850596bb79361d58803866e5ba29c9366dcf57e98929d561d86fca005b262 |

## 结论与唯一范围修正

**主体证明通过独立重构与攻击；未发现数学 fatal。** 对全部 m≥3，完整 degree≤2 矩阵 PSD、全部 onehot/count 关系及零负载 localizer 成立；精确 C2 阈值 n/m、整数 OPT=2 和趋二比值均成立。
§9 的一般 supremum gap=2 也成立，明确依赖端剪枝与 UM-ST-ROUND-v1。该上界不是由本族有限实验推出。

须收窄 §1 的“该 C2 合同严格弱于完整配置”措辞：此例只证明同一实例同一阈值上 C2 可行而 CONFIG 不可行，即 C2 不蕴含 CONFIG。
若“严格弱于”意指对全部实例成立的松弛支配关系，则还需要 CONFIG 可行解向共同 M2 的普遍扩展，正文没有证明这一步。
建议直接改成“本族在 C2-load(t) 可行而 CONFIG(t) 不可行；不主张两个一般松弛的全局支配关系”。此措辞修正不影响任何已证间隙结论。

## 初等分解、null 降阶与交叉项攻击

1. n≥4 是 count-null 的必要范围条件。对每个 |S|≤3 仍有未占用 job，下降阶乘直接给 L[(N_a−t)x_S]=0。
   所以 (N_a−t)ell（deg ell≤1）与任何 deg q≤2 的 Gram 交叉乘积，乘子次数最多3，全部已在四阶信息内。
   此处先由线性恒等式证明 radical，没有循环借用 PSD。
2. onehot 把同-job二次项降一次；每个不同-job color 核分对称/反对称后，取 color 矩阵基即覆盖所有 job 对系数数组。
   对称 rowpair 映射 c↦(n−2)c+(Σc)1 可逆；反对称在 Σc=0 上为 nc。
   因此 rowpair+row-zero 分解完整，不漏 S_n multiplicity 空间。
3. 反对称的 c_j−c_k 与核变号抵消，降阶仍是 Σ_jc_jΣ_{k≠j}B(X_j,X_k)，符号正确。
   color additive/gradient 在 job harmonic 下本身为零；其行和映射可逆，确能取 B1=0 或 C1=0。
4. 一次双居中后 Gram=t/(n−1)倍 Frobenius。harmonic 与一次/常数的交叉项由 row sums 为0消去。
   对称/反对称的 mixed shared-edge 公式只剩 Frobenius 与 diagonal 内积，二者均为0；same-edge、disjoint-edge 也为0。
5. 独立逐项反算作者 D/O/Z 及 alpha 化简，均正确。
   对称 shared-edge 有序系数和为 −2S、disjoint 为 S；反对称考虑方向后仍为 −2S。
   例如反对称 circulation H12=H23=H31=1 给 3(D−2O)，与作者公式吻合。
6. 对称块逐行 Cauchy 与 trace 项确给正定；等号时对称性迫所有非对角同值，trace=0再迫全零。
   反对称 color 块为正标量倍 Frobenius。
   job 正交基使 bilinear factor S*K_color 成为直和，因此覆盖任意纯张量和，而非只检查分离型平方。
7. 四块均正定且正交，结合完整张成性，作者 M1/M2 秩公式成立。

在读作者稿前，审查者还独立得到一般 n≥4、t_a≥1、Σ_at_a=n 的 PSD 证明。
其 symmetric color 正性来自权 t_a(t_b−δ_ab) 的 edge 内积中 additive 投影；skew 来自权 t_at_b 的 gradient 投影。
故此重构与作者等容量 Cauchy 推导相互独立。scratch 完整证明 multislice_independent_proof.md 的 SHA256 为
58272c171faa6d0dd061df210cd073363449584250d2818bef9f6a4bf53f6de9。

## §9 上确界、端剪枝与零值

M2 对角非负给每端 y_e≥0；onehot 给逐任务和1；常数 localizer 给逐机分数负载≤T。
端剪枝保证每条正支撑处理时间≤T，故已重构的 UM-ST-ROUND-v1 输出真实负载≤fractional load+support max≤2T。
这对每个可行 T 都成立。取可行阈值下确界即可得 OPT≤2T_C2，不需要下确界达到，也不需要精确 SDP 求解算法。
本族给比率趋2，因此 supremum 恰2；未声称某个有限实例达到2。
正 OPT 下上式保证 T_C2>0。零 OPT 的逐任务零端处理与仓库模型一致。
没有把松弛间隙改称相对 OPT 的一般算法困难性。

## 实际独立运行范围

审查者独立实现先 Fraction 生成全矩，再乘共同正分母，做整数对称 Bareiss 消元；每次除法精确整除，零 diagonal tail 要求整个 tail 为0。
这与规范程序的 Fraction Schur/LDL 路径不同；没有导入其 core。

| m | n | 完整 M2 维数 | 整数缩放 | 结论 | rank |
|---|---|---|---|---|---|
| 2 | 3 | 19 | 16 | 非PSD：零 diagonal tail 存非零 off-diagonal | — |
| 3 | 4 | 67 | 243 | 全部非零 pivot 为正，余 tail 全零 | 16 |
| 4 | 5 | 181 | 6144 | 全部非零 pivot 为正，余 tail 全零 | 61 |

独立实现/规范拷贝的 SHA256 均为上表第三项；scratch 输出 multislice_independent_audit.json。
另实际重跑规范作者程序默认范围，结果保存 multislice_review_author_rerun.json；去除 elapsed_seconds 后与作者冻结输出逐字段一致。
该规范默认 full-matrix/全部线性约束范围是 m=3,4，指定 color kernel 公式范围是 m=3,...,8。
本审查没有声称独立跑过 m=5 全矩；主线程后续运行须另据实际输出记载。
以上有限运行互证实现，不替代所有 m≥3 的代数证明。

## m=2 边界：明确 job,color 坐标与最小支撑

本节固定 x_{j,a}：第一个下标是 job，第二个下标是 color。取 jobs j=1,2,3、colors a=1,2。
令

\[
p_1=x_{1,1}x_{2,1},\qquad
p_2=x_{1,1}x_{3,2},\qquad
p_3=x_{2,2}x_{3,2}.
\]

m=2,n=3,t=3/2 的直接 moment 计算给

\[
G=\begin{pmatrix}1/8&3/16&0\\3/16&3/8&3/16\\0&3/16&1/8\end{pmatrix},
\qquad L[(p_1-p_2+p_3)^2]=-1/8.
\]

三单项式支撑在此 monomial 基中最小：所有 diagonal 属于 {1,1/2,1/8,3/8}。
union≤2 时，compatible pair 或为 nested/相同（直接有 cross²≤diagonal乘积），或为两个不同-job单项式，此时 diagonal 均1/2、|cross|≤3/8。
union=3 的 cross 只可能 −1/16（全同色）或3/16（2+1色型）。
若是一单项式与一二次单项式，其 diagonal 乘积至少1/16，大于等于 cross²。
若是两个二次单项式，全同色时 diagonal 均1/8；2+1色型不能同时有两个 compatible 同色pair各 diagonal=1/8，所以 diagonal 乘积至少3/64，大于 cross²=9/256。
incompatible cross=0。以上类型穷尽每个二阶主块。
所以一或二支撑不能给负平方。
该边界没有被扩展成 m≥3 的反证；n=3 恰缺 degree3 count-null，是不能套用规范分解的原因。

## §10 原始文献范围

实际独立浏览了作者所给 [arXiv v3 摘要页](https://arxiv.org/abs/1811.08539v3) 及 [PDF](https://arxiv.org/pdf/1811.08539v3)。
v3 日期2020-05-16；Theorem1 在PDF/印页3给 CONFIG 上 Ω(n)轮仍有至少1.0009间隙；AppendixB 在页33–34讨论向 assignment LP 的转移。
这符合规范稿的窄比较，不能替代本稿特定四阶合同的正性证明，也不认证本稿优先权。
审查只核这几处表述与公式背景，没有下载原始PDF字节、核全文证明或进行全球优先权检索。

## 最终修正复核与接受

在上述原始审查哈希之后，主线程只修改了 §1 的一处范围句子，明确 C2-load 不蕴含 CONFIG 可行性，且不主张两个一般松弛的全局支配关系。
审查者读取修正版，将该新句精确替换回原句后重算 SHA256，恰得到原审查哈希 5fe91d05aa2d9e05023c14fa26c7b0490a9ad85623a57690e365510ea9506a7f。
因此已确认除此句外正文无任何字节变更。
修正版正文 SHA256 为 **96863e90ce3893505bbb910c74ea896286b5893be4f487f9efe00d329d9f4b85**；两审计脚本 SHA256 未变。
唯一范围异议已解决，**最终接受修正版规范稿的 stated-scope 数学结论**。
主线程随后实际完成的 m=5 全矩 dim406、rank171 不被冒称为本审查者的独立运行；本审查者 full-matrix 实际范围仍为 m=2,3,4。
