# partial-support 与福利 LP：零 job 源差分复核

本任务 `boss2-wave10-repair-094b299464e358ff` 定向替代已完成的 `boss5-localfix-repair-25d12f7253028f37`。17 核心、9 共享只读对象的 26 个 input pins 均与当前登记一致；定义 pin 为 `4457d5645c0777f8feee342e41bf2ab2b485c16b99a6a94084e2c5a08f152944`。本轮只有 robust 核心从登记 version 5/pin `4dfe055bb9bcc7ce75cee4da19f61871b56a22c8b4f0f6e5df32c69d234fc642` 改为 version 6/pin `3a0dc3aefc137b6c09a0d1af24714d66d7a6a899f385442caa2098c834e1517d`；其数学陈述、量词、条件和主正文不变。

## 1. 源句修正的精确作用

共享审查《归一化菜单福利与配置证书双源审查》§二.1 将“以 1−λ 权重放所有 positive incidence；”改为“以 1−λ 权重放全部 incidence jobs（含零 jobs）；”。当前全文 SHA 为 `33bd31b883b26f49508808dd7175cd104f391b86642bff90ea2bce7f1142097b`。把唯一新句反向换回旧句恰重建旧全文 SHA `63629abaa5cd2bcc0e42ff051936b91882ea63c711dfdac231f238763b682255`，没有另一处字节变化。

未改的主定理《规范化平菜单的 CONFIG(1) 与正支撑 FSLP 双向保持》§1 本来就给完整配置：private 以 λ 选 selector 加全部零 job，以 1−λ 选全部 incidence。两配置负载均为 1；零 job 的覆盖为 λ+(1−λ)=1，正 job 的 private/resource 覆盖为 (1−λ)+λ=1，selector 按组 Σλ=1。零私有时间不消耗正支撑 FSLP 列容量。这次修正补全摘要的全任务覆盖，没有产生新的数学结论。

该 flat CONFIG 证书配置不进入 F2 的激活罚项，也不进入 robust 的福利 LP。P_gate 的 root/gate/private 完整前向回填已由前任成熟审读支付；共享源§一未变，本轮继承该历史审读。

## 2. 替代子域判别与目标仍是不同合同

F2 使用正支撑部分 LP：λ≥0、每组和≤1、总质量 q>0、每资源正支撑列和≤1。独立抽态允许 inactive；对 W−τA 做精确有理条件期望，不能把实际激活数 A 换成 q。norm1 与不交 bundle 使 YES 的至少 q 个 unit 组提供完整正支撑 λ。

在 0≤η≤1/40、0<γ≤δ≤3/8 中取 q=(1−η)n、τ=19/50。由 1−1/e>5/8，

\[
H_\tau>\frac{5/8-19/50}{1-19/50}q
=\frac{49}{124}q\ge\frac{1911}{4960}n
=\left(\frac38+\frac{51}{4960}\right)n>\gamma n.
\]

τ>3/8≥δ，所以这些组同时属于 r≥δ 与 r>δ，分别排除两版 NO，包括非整 q 和三重等号端点。这是检查正支撑 λ 可行性的替代子域算法。

目标 robust 指定另一总可行福利 LP：Σz=1、0≤x≤z、每资源 Σx≤1、L=maxΣpx，并在一般 (E)：(5/8)(1−η)≥γ+(1−γ)δ 域检查 L≥(1−η)n。F2 的上述子域算法没有支付这一指定 L 判别或一般 (E) 合同。

精确分离例仍成立：两组各唯一 state，在各自私有 a/b 权 19/20、共享 u 权 1/20。福利最优 L=39/20，而正支撑共享列迫 λ₁+λ₂≤1。η=1/40、n=2 给 q=39/20，因而没有从任意 L≥q 到同质量整 support λ 的免费转换。该例不在 near-perfect YES 或 robust NO 中，只否定这条转换桥，不反驳任一 promise 判别定理。

因此替换边保原 edge_id、accepted / motivates / context / ALL，robust 在本包仍为 isolated-after-review。全局其他包的 incoming whole 关系不改变这条 F2 比较的数学理由。F2 因既有 uniform-quota 条件 step 保持 linked：必须额外有 |R_(x,a)|=K_(x,a)>0 及给定同一质量 q=q_r 的 λ；只构造 δ=3/8 的 orientation 右侧见证。一般 K、任意 δ 的完整 iff、方向搜索、无 λ 可行性与全方向 FAIL 仍由原 contribution.remaining 限定。

## 3. 资产处置与实际阅读

11 份前任边逐项保原数学范围：6 whole、2 step、3 context，全部保 ALL。唯一替换是 `partial-support-versus-welfare-lp.json`，写到本任务目录并保旧路径历史；其余 10 份在完整收据中逐项 retained 原路径/原始 SHA。旧 11 边的 43 条 direct evidence 引用全部仍为当前字节，没有一条直接引用本次共享审查；只有 partial-support 的 robust 目标 pin 过时。新边保全部旧 direct evidence，不扩大已有 whole_result 或缩短任一 contribution.remaining。

本轮实读：当前任务与前任务结构、前任收据全部 17 核 coverage；26 个当前对象的模型、陈述、量词、条件、范围、异议和正文定位；全部 11 旧边的端点、条件、实际解释、whole_result/contribution/scope，受影响边与相邻 uniform-quota 边全文；F2 定理、robust 四源正文、共享双源审查和前任 mathematical-review 全文；主 CONFIG 定理§1及其输入合同。另读 source-correction 记录、partial-welfare 预核，以及 impact-3d 中本前任 head 与受影响 partial-support 条目。

本轮元数据核验：26 current pins；任务 108 阅读引用、68 不同文件的原始 SHA 与所列标题唯一性；11 旧资产原始 SHA、全部端点和 43 direct evidence SHA。元数据核验不等于对 68 文件的正文重读。未变材料的完整证明、原 PDF、外部科学审读、CE 程序/有限枚举及历史运行，明确继承前任成熟正式交付；本轮没有重跑数学程序或新增有限实验。

本任务及直接前任均未声明 follow-up 对象对；closed_overlaps 和 follow_up_tasks 均为空，未产生需要发布的新比较任务。17 核覆盖保持 8 linked、9 isolated-after-review，没有新增节点或强迫逻辑边。

正式 edge-bind/edge-check、收据最终边 SHA 刷新、checkpoint、推送、done 及集成由 Boss 串行完成；本说明不声称这些动作已经执行。
