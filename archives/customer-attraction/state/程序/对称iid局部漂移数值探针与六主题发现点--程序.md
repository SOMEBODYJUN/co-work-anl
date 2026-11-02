---
id: customer-attraction/symmetric-iid-local-drift-numerical-probe-and-six-label-discovery-point
kind: program
type_tag: 程序
title: 对称iid局部漂移数值探针与六主题发现点
status: native-program-and-all-saved-fields-read;numeric-discovery-preserved-with-exact-small-replacement
summary: 原2633B探针将精确全终局SPE可实现性与浮点残余iid势最大化分开；保存trial5的五人六题98客户数据，不将近似q/Z或未附策略当完整证书。原入口0次，一次新固定算术只核已给数据。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-8e45018cd1354e279ca636fdb82cf0f1/global_proof/iid_drift_probe.py
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-8e45018cd1354e279ca636fdb82cf0f1/global_proof/iid_drift_probe.py
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-8e45018cd1354e279ca636fdb82cf0f1/global_proof/iid_drift_candidate.json
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-8e45018cd1354e279ca636fdb82cf0f1/global_proof/iid_drift_candidate.json
---

# 对称iid局部漂移数值探针与六主题发现点

## 原程序究竟优化什么

2633B原码、2446B保存JSON及说明README全部读完。原程序的benchmark(ins,r,prefix)固定合法主题计数prefix。对每类客户T，背景b_T为prefix中覆盖该客户的行动数，t_T=q(T)为独立查询分布命中概率。原代码最大化

\[
 F_{r,b}(q)=\sum_Tw_T\sum_{j=0}^r\binom rj t_T^j(1-t_T)^{r-j}
                 \sum_{\ell=1}^j\frac1{b_T+\ell}.
\]

它实现的梯度是r倍纯查询收益向量：

\[
 \partial_aF=r\sum_{T\ni a}w_T\sum_{j=0}^{r-1}
 \binom{r-1}j\frac{t_T^j(1-t_T)^{r-1-j}}{b_T+1+j}.
\]

由[残余静态凹势定理](../定理/合法前缀残余独立同分布价值与租金--定理.md)，**精确**最大者是残余静态对称混合Nash；程序随后返回该数值分布的剩余总支付

\[
 Z(q)=\sum_Tw_T\sum_{j=1}^r\binom rj
 t_T^j(1-t_T)^{r-j}\frac{j}{b_T+j}.
\]

这不是势值F，也不是直接最大化剩余利润Z；非零背景时更不是完整覆盖。r=0分支直接回0及均匀分布，当前main只用根m和首步后m−1，m∈{3,4,5}，不会在主入口走r=0。

优化器是SciPy SLSQP，从均匀q开始，显式梯度、坐标[0,1]、概率和1，ftol=10⁻¹⁰、maxiter=300。result.success为假时抛RuntimeError；成功时直接使用result.x，没有精确KKT、有理区间夹逼、精确和1检查或支持逐行动等收益证书。凹势的数学性质不把一次浮点success自动变成精确均衡认证。

## 精确SPE可实现计数的部分与数值基准的部分

原码使用规范ExactSPESolver。对每个随机输入先算roots=solver.outcomes()，该局部变量之后未被消费，但计算已完成根集合缓存；再取根门槛floor=solver.threshold(0)。对每个可能根行动a，枚举child outcomes并保留

\[
 u_a(c)\ge\text{floor}.
\]

在这些候选中选使当前根收益最小的c。集合BI门槛是各行动孩子中最坏根收益的最大值；因此这个精确判据允许为其它行动各选一个相容子博弈续局，拼成以a为根且实现c的完整纯SPE。它并未要求不同有序历史共享计数策略，亦不只沿一条根路径检查。完整量词见[全历史终局全集](../算法/完整历史纯SPE终局全集--算法.md)。有并列最小c时未另设规范化平局键；不能保证跨实现得到相同保存counts。

随后算根v、首步后z，检查float(u)+z−v。只有u、可实现性筛选和模型收益用精确有理；两个benchmark及最后drift是浮点。保存JSON没有提取或写出完整策略表、全部子博弈证书或根门槛。正确描述是“使用精确SPE可实现性oracle的数值发现程序”，不能把该JSON直接称为已独立验证的完整SPE反例。

## 发现循环和输出合同

random.Random(8913)固定生成流，最多200个trial。主题数从4、5、6选择，人数从3、4、5选择；每个非空兴趣mask以0.28概率入样，入样重数从1至10等概率取。没有客户则跳过；空主题仍可能出现，所有主题标签保留，不合并同覆盖标签。

每次更小drift向stdout打印best。遇drift<−10⁻⁵，就把当时best[1]覆盖写脚本旁iid_drift_candidate.json并return；否则最终打印DONE和best。原件没有完整stdout、依赖版本、运行时长或命令事件。保存trial=5不是“完成200输入”，也不单凭这个整数声称前五个trial每个都执行同样数量的优化或全部成功。

代码有main守卫；直接import不运行随机main，但顶层仍导入NumPy/SciPy及规范包。parents[5]依赖原research/workspaces/.../global_proof层次，拷平后无法按原约定解析根。重放必须在新目录恢复源相对路径及[四模块依赖](../../tools/evidence/r8e450-local-iid-and-root-primary/dependency-manifest.json)，并单独提供兼容NumPy/SciPy环境。本批没有新装环境或执行原入口。

## 保存的唯一六主题发现点：全部客户与字段

JSON顶层恰为trial、instance、counts、action、u、Z、Znext、q、qnext。instance为五人、标签字符串0至5、下列16类不同单位客户：

|兴趣标签|重数|兴趣标签|重数|
|---|---:|---|---:|
|1|8|0,1|5|
|1,2|6|0,1,2|5|
|0,4|3|0,1,4|2|
|1,2,4|8|0,3,4|3|
|1,3,4|7|0,1,3,4|9|
|1,5|4|0,2,5|8|
|0,4,5|7|0,1,2,4,5|8|
|0,3,4,5|6|0,1,2,3,4,5|9|

合98客户。保存trial5、counts=(2,3,0,0,0,0)、action0、u="211/10"。这些计数的算术可独立精确核：只含0不含1的客户27名，只含1不含0的33名，同时含两者的38名。于是占用主题0、1的每位玩家分别得

\[
 27/2+38/5=211/10,\qquad33/3+38/5=93/5.
\]

所有98客户都喜欢0或1，所以此计数覆盖W=98，合法比较包含0、1就达到OPT_5=98；这些结论不需要确认该计数是SPE可实现。

保存Z=95.96980062741156，Znext=73.25184068407242，原十进制所显示的差为−1.61795994333914。q与qnext为

\[
\begin{aligned}
q={}&(0.4401412066902629,\;0.5598587932960708,\;
7.232388657172918\cdot10^{-12},\;1.082031531656036\cdot10^{-11},\;0,\;1.4979398435312015\cdot10^{-12}),\\
q'={}&(0.2321411399616295,\;0.7678588600444581,\;
1.3154637588134772\cdot10^{-13},\;2.085609169841998\cdot10^{-13},\;
3.312638494685103\cdot10^{-12},\;3.732892285835806\cdot10^{-14}).
\end{aligned}
\]

按保存十进制求和约为1.00000000000588434和1.00000000000977767，说明它们是数值近似，不能原样当精确概率。没有擅自删小坐标、归一化后宣布仍是Nash，也没有把两浮点Z当经证明的上/下界。完整精确位串和所有字段仍原字节保留。

## 手算替代、现有成果与实际新执行

原README明确以[两客户三人完整SPE](../反例/两单客户三人完整均衡的静态iid逐步付款失败--反例.md)替代上述发现点承担局部反证。替代点有完整七历史策略、根及孩子静态Nash的解析唯一性、精确差−1/4，足以关闭原局部候选；六主题文件仍具有发现来源、程序合同和保存参数的价值。

本次新增固定标准库核只做两部分：两客户完整策略14项精确比较与静态值；六主题保存输入16类、98客户、两个占用题份额、W=OPT、原十进制差和概率和的读取算术。没有为六主题调用ExactSPESolver、重构完整策略、跑SLSQP或认证近似Nash；没有原200trial新搜索。

一次事件exit0、stderr0，Python3.12.14，输出6671B，完整事件及代码SHA见[证据README](../../tools/evidence/r8e450-local-iid-and-root-primary/README.md)。已有静态基准、五人实际前缀局部漂移及强弱全局反例已全文比较，不重复其充分成功审计。当前一般六人half与真正安全值聚合不由这些局部或iid基准失败判定。
