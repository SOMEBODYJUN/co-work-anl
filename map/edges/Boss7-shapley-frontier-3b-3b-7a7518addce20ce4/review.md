# 五阶截断 Shapley frontier 与正根旧点：完整比较

任务：`Boss7-shapley-frontier-3b-3b-7a7518addce20ce4`。本 review 覆盖两个核心对象及任务列出的十个 reading refs；两个大 JSON 均按原字节完整读取并解析，未以截断的终端显示冒充实读。比较边是 `frontier-specializes-old-positive-root.json`，方向为

`CA-FIXED-00001-SHAPLEY-UP-FLOOR-FRONTIER-v1` → `CA-TRUNCATED-SHAPLEY-POSITIVE-ROOT-UP-NO-v1`。

## 1. 模型、符号与已核验证书

两份对象用的是同一张五人七标签完整有序动作表 `σ`，实际路径 `s=00001`，外部标签 `J={2,3,4,5,6}` 在集合值中交换对称，Shapley 收益按五个有标识副本的均匀排列计算。冻结表有 2801 个有序历史；每个历史有六个自身以外的动作，故有 16806 条偏离不等式。`verify_witness.py` 对目标 JSON 重放：399 条截断单调行、546 条截断递减边际行、2801 历史/16806 偏离，1193 个平局，最小严格正 slack 为 `1/60`，实际收益为 `19/100,19/100,19/100,19/100,6/25`，总福利 `W=1`。

目标正根点的共同值由 19 个 `(root-mask,外部不同标签数)` 矩确定。根删除边际是

`W-C(0)=1/5`，`W-C(1)=1/10`，

唯一最优五槽支持是 `J`，`C(J)=OPT_5=9/8`。实际路径上每个外部标签的五位置查询和相同，五个外部标签的查询总和为

`Q_J=53/40`。

所以目标反例使用

`D_J=4W+Q_J-5C(J)=-3/10`，

而 frontier 采用相反号

`L_J=5C(J)-4W-Q_J=3/10`。

两份独立标准库 verifier 均成功，并且输出与登记的两个 verification JSON 字节摘要一致。

R275 genuine JSON 也已全量解析：它是 broader common monotone-submodular Shapley 类的 five-player/seven-topic full-history candidate，root floor `0.1`，检查 `1470` 个 coefficient rows；MILP status 为 time limit（`floating_bound_not_a_certificate=true`），但 exact candidate 自带 `88/57` 的有理值/dual，independent uniform-order audit 为 2801 histories、16806 deviations、`W=1, OPT=88/57`。R275 review 明确 `customer_attraction_half_status=OPEN`，故只作外部压力测试和边界语境。

## 2. Frontier 的精确数值与旧点特化

固定 frontier 的归一可行域是 `0≤δ≤1/3`。对固定 `J`，在同一冻结策略、同一强制分支查询定义下，精确最大违反量是

\[
\max L_J=\begin{cases}
1-7\delta,&0\le\delta\le1/9,\\
8/3-22\delta,&1/9\le\delta\le1/3.
\end{cases}
\]

切换点由两条仿射式相等给出：`δ=1/9`，此时最大值为 `2/9`。根 IC 与域内次模性给 `C(0)≥2W/3`，因此归一地板的端点 `δ=1/3` 是可行域上界，而不是付款阈值。

frontier 的仿射取等族第一段在 `δ=1/10` 给

- `C(kJ)=k(1-δ)/4`（`k=1,…,5`），故 `C(J)=5·(9/10)/4=9/8`；
- `C(0+kJ)=9/10`、`C(1)=4/5`、`C(1+kJ)=C(01+kJ)=1`；
- 根删除边际 `(1/5,1/10)`；
- `L_J=1-7/10=3/10`，即目标反例的 `D_J=-3/10`。

这正是旧 `positive-tenth-witness.json` 的数值点和同一完整 σ，不是一个相似但不同策略的候选。因而 frontier 对旧点是严格的参数化特化：旧对象给出 `δ=1/10` 的单点存在性反例，frontier 额外支付了整段可行域、两段精确上包络和全比较元组阈值。frontier 不应被倒读为旧对象已经证明了所有 δ；同样，旧对象的一个失败点不能推出 `4/33` 的锐阈值。

## 3. 失败阈值、最优支持与量词

在取等族中，`J` 在 `δ<1/6` 时唯一最优，`δ=1/6` 时与最大其它支持并列，`δ>1/6` 时不再最优。这个 `1/6` 是支持最优性边界，不是均匀付款边界。

固定 `δ=4/33`，`all-comparison-duals.json` 给 175 行（173 条不同非地板行加两条地板行）和 41 个五槽多重集类别的有理对偶；`J` 类的 bound 为 0，其余类别的最大 bound 为 `-35/33`。因此在固定 σ、外部对称、截断定义域的输入类中，`δ≥4/33` 时每个可行输入、每个合法五槽元组（包括重复槽）都有 `L_T≤0`。结合 `δ<4/33` 的取等族 `L_J>0`，`4/33` 是该作用域的精确失败阈值。

`δ=1/10<4/33` 位于第一段，故旧点严格失败；它不是第二段的切换或阈值端点。`δ=4/33` 时取等族仍有唯一最优 `J`，但 `L_J=0`，正好是付款等号。

需要分开的量词是：

1. frontier 的“`δ≥4/33` 每个可行输入、每个五槽元组付款”只对同一冻结 σ、外部交换对称、五阶截断集合值成立；
2. 旧正根对象的命题只有“存在一个明确输入和一份完整纯 SPE，使该 `σ` 的全部最优元组失败”；
3. R275 genuine 只是 broader moment 类的 exact candidate 和 necessary pressure test，既没有客户目录逆实现，也没有把结果写成当前客户吸引模型的全称结论。

## 4. 哪些可以迁移到旧正根对象

可以无损迁移的只有同一冻结策略/输入锥的内容：

- `δ=1/10` 取等族的共同值、`W=1`、根边际、`J`、`C(J)=9/8` 和 `Q_J=53/40`；
- `L_J=3/10` 与 `D_J=-3/10` 的符号转换；
- 同一 2801 历史和 16806 条真实偏离的定义级完整纯 SPE 验证；
- 由于 `1/10<4/33`，该旧输入的所有最优五槽元组均失败（目标的 `J` 唯一最优，故其原句的“至少有一个最优元组付款”也被否定）。

不能从旧单点反推的内容包括 `δ` 的整段仿射可行性、切换点 `1/9`、支持最优性边界 `1/6`、以及 `δ≥4/33` 的全输入全五槽付款保证。它们需要 frontier 的 12-row 对偶恒等式、173 条非地板行和 41 类比较对偶。

## 5. 不能迁移的模型边界

### 5.1 全域单调次模

目标 `C` 只定义在至多五个不同标签的截断域。其七标签全域延拓已被精确排除：令

`A={0}∪(J\{2})`，`A'={0}∪(J\{3})`。

目标值给 `C(A)=C(A')=C(A∩A')=9/10`，而 `C(J)=9/8`。若有全域单调次模延拓，次模性和单调性将要求

`9/8=C(J)≤C(A∪A')≤C(A)+C(A')−C(A∩A')=9/10`,

矛盾。故 frontier/old witness 没有全域次模解释，不能攻击或证明全域次模版本。

### 5.2 非负单位客户

若 `C` 来自非负单位客户覆盖，则对任意外部 `a∈J`，`C({0,a})=C({0})=9/10` 意味着任何被 `a` 覆盖的正客户质量都已被标签 0 覆盖。于是五个外部标签的联合质量至多 `9/10`，但 `C(J)=9/8`，矛盾。统一正倍数也不能修复这个质量矛盾。frontier 的输入是截断 moment/C 向量，不是已实现的客户目录，因此不能迁移为单位客户反例或客户吸引模型的单位客户全称否定。

### 5.3 五人 net-Q

已登记的五人 net-Q 定理使用另外两份冻结策略（实际路径 `00011` 与 `01010`）及非负单位客户类型，按

`Q(c,J)=Σ_x d_x(J)/(1+c_x)`

对客户负载逐类型结算，并要求恰五个不同标签的支持/排列；其证明依赖客户类型的逐型付款排列。这里 frontier 的 `Q_J` 是同一 00001 策略上五个位置、五个外部标签的 Shapley 真查询效用和，定义域允许重复槽，且输入本身没有非负客户实现。没有从 frontier C 向 net-Q 客户型配置或那两份动作表的策略映射，故不能把 `L_J` 或 `4/33` 说成 net-Q 结论，也不能用 net-Q 的付款判据替代 frontier 的 41 类对偶。

## 6. 复核与交付

完整执行：

```text
python archives/customer-attraction/tools/evidence/truncated-shapley-positive-root-uniform-payment/verify_witness.py
python archives/customer-attraction/tools/evidence/fixed-00001-shapley-up-floor/verify.py
```

两次均成功。读入的十个 ref 的当前 SHA、字节数和行数记录在 `reading-ledger.json`；边文件随后由 `edge-bind --write` 写入 endpoint/evidence pins 与 review digest，再用 `edge-check` 做本边结构核验。未运行 checkpoint、commit、push 或 map done；交付由根 Boss 串行完成。
