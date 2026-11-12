# 第二源 τ4→τ5 完整条件重配族

实际 agentID：`/root/source2_conditional_redistribution`。RUN：`six-boss1-20261111`。只做精确符号/Fraction；0 优化，0 LP 或全局候选读取。

## 已完成

- 全域 δ∈[0,5977/6912]，τ3=0、τ4=5977/6912−δ、τ5=43/48+δ；s∈{0,61273/6912,9}。
- q0=1/6 的三个纯族分别有 5 个完整公共断点；每点保留 A1,…,A6,X,C 八个合法目标原行与 C-only 自由等式形式。
- q0=1/5 的 ordered 三族分别有 16、15、14 个完整条件断点；先逐态取 m，再全六重数 f_d，最后 G。全域 d=1 唯一最弱，全部 f_d 两两交点为空；大 q 条件最小尾变化没有删除。
- 全部 1536 个真实仿射态；180 条端点原行、3 条额外 ordered ε 行、150 条完整 513 列仿射段；全部弱态及来源行保留。
- 独立检查 PASS：38016 次逐态检查、2376 张全弱态最小表、93879 个点行列、153900 个段行仿射系数、7695 个 C 自由等式列、1026 个 ε 身份列。

## 关键局部结论

q6、s=0、c=o=1 首个锚变化点为 δ*=1/144（p=1）；该点尾1101、1110、1111全并列，δ>δ*才严格低于锚。p=0 的同类直到29/48才变化。

设 Mpo 为 c=1 且 p=A1、o=O 会员位分别为 p,o 的客户数，则全区间

\[
R_\delta=R_0-\delta(N_5-N_4)
+\frac{4\delta}{5}M_{10}
+\left[\frac{4\delta}{5}-\frac1{180}\right]_+M_{11}
+\left[\frac{3\delta}{4}-\frac{427}{960}\right]_+M_{00}
+\left[\frac{3\delta}{4}-\frac{29}{64}\right]_+M_{01}.
\]

故左端闭段0≤δ≤1/144准确为 `Rδ=R0−δ(N5−N4)+(4δ/5)M10`。ε=1/144 时，s=0 的修正为 M10/180；s*=61273/6912 另有 101M00/27648。两条指定猜想逐列成立，没有反例。

## 工件入口

- [完整证明](source2_conditional_redistribution/proof.md)
- [全部断点及条件事件](source2_conditional_redistribution/breakpoint_table.md)
- [全部条件分段式与端点弱态](source2_conditional_redistribution/conditional_piecewise_table.md)
- [全部1536真态及精确包络](source2_conditional_redistribution/exact_envelopes.json)
- [180条513列原行](source2_conditional_redistribution/exact_family.json)
- [150条513列仿射段](source2_conditional_redistribution/affine_family.json)
- [独立检查结果](source2_conditional_redistribution/literal_checker_output.json)
- [失败/执行记录](source2_conditional_redistribution/failure_log.json)
- [冻结manifest](source2_conditional_redistribution/freeze_manifest.json)

schema：`rows` 为列表，每条 `a` 是长度513的有理数字符串列表，按完整九位 `(a1,…,a6,x,o,c)` 字典序512列后加独立K列。原尺度不等式 `a·x≥0`，正数值除数25。没有修改任何旧包、Git、registry、map、RUN或全局输入；冻结完成后停止写入。
