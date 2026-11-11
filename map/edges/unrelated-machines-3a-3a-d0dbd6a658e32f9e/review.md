# 原 InfDegreeTwo 存在性间隙的 3A 主覆盖复核

本包覆盖 G=`M-b126c4b3ff29400589f7f38abdca4d85` v4。结论为 linked：既有 canonical 关系 `boss6-explicit-intersection-family-back-to-infdegree-two-gap` 已完整支持 G 当前整条陈述，本轮按原 SHA 共享，不重复新增边。共同前提保持 ALL{A,B}，其中 A=`M-16209762a32e42e48ec20b76381b5e9d` v1，B=`M-7bc9eab74ecd475db7df33c3f4b75e61` v1。A/B 是本任务当前 read endpoints，不在本包另作核心覆盖。

任务是 `unrelated-machines-3a-3a-d0dbd6a658e32f9e`，当前 owner Boss6、state claimed；本轮沿父 Boss6 身份工作，只写本任务 staging。完整对象记录与当前 read-add 后任务均已实读。当前三 pins、任务字节及复用资产的精确 SHA 在 reading-ledger.json 和收据中列明。

## 1. 完整目标、模型与来源范围

G 只断言存在参数化有限家族，按玩家数 n 计，InfDegreeTwo 上的 M-LP/整数与原始 CONFIG/整数间隙分别为 Ω(n^(1/4))。它不要求两 LP 在一般输入或全部阈值上同值，不断言每个实例均有该 gap。物品不可分、单归属、估值非负加性；InfDegreeTwo 约束每件物品的无限值玩家端数≤2。

原始 CONFIG(s) 对每位玩家所有达有限正阈值 s 的配置分配质量一，每件物品总边际≤1。M-LP 依 M/λ 逐玩家端重估大端为 M，并要求：物品列容量≤1；big 质量+z≥1；small 效用≥Mz；每个 small x≤z；变量非负。没有每行 x 总和一的额外约束。

G v4 的来源范围已准确修正：本轮直接从原 PDF 导出实读 p4、p6–8、p12–13，并将 p7 渲染视觉核对式(4)–(8)。p13 脚注2仅声明 InfDegreeTwo 的 Ω(n^(1/4)) 存在性；正文 Lemma4.1 展开的是 InfDegreeOne。完整 I_T 构造和证明由 A/B 共同正文§8–9，以及 M-LP 正文§5.3 承担。本轮没有将脚注写成含完整构造的原证明。

## 2. A/B 如何恢复原人数下的明确家族

A 的同一输出 D∞(I) 对每个有限 s>0 双向保持整数与原始 CONFIG 可行性，两个合同分开证明。每条高正度物品链用 d 份专属副本、d−1 名相邻∞helper。整数反向中 helpers 至少占 d−1 个不同副本，至多一份可给旧玩家；CONFIG 反向中每名 helper 配置边际至少一，d 份总容量扣去 d−1，旧玩家总边际≤1。删零后每名原玩家对旧物品仅有一份正值副本，合回不会在配置中制造重复物品，值和行质量保持。正向 hole/prefix 令 w_r≥q_r、Σw=1，helper 在左右 singleton 的质量为 1−W_k 与 W_k，各副本负载 q_r+1−w_r≤1。这些论证使用符号∞，因此输出本身不依赖 s；有限 helper 的受限阈值合同不能代替它。

B 提供的不是任选交域实例，而是明确的 J_T=D∞(I_T) 以及精确值 ConfigOPT(J_T)=T、IntOPT(J_T)=q=floor√T。源 I_T 对整数 T≥4 有 T 个 block。每个 block 有 root a_r、T 位 b_{r,k}、T 件 u_{r,k}、T 件 w_{r,ℓ}；root 对本 block 全 u 值1，b_k 对自己 u 值∞、对全 w 值1。另 T−1 件 B_r 仅对相邻 roots 值∞，其余值零。故原 n=T²+T、m=2T²+T−1；u/w/B 的物品∞度分别为1/0/2，I_T 属原 InfDegreeTwo 类。A 反向把 B 的两种 raw 目标恢复到这份 I_T。

本轮还直接核了源值，不只接受反向符号。CONFIG(T)：root 的全 u 质量1/T；B_r 给左/右 root 的 singleton 质量分别为(T−r)/T与r/T；每位 root 外部总质量(T−1)/T。每位 b 的自己 u singleton 质量1−1/T、全 w 质量1/T。各行质量一，各 u、w、B 列负载均一。若 s>T，每位 root 的每个合法配置都必须含 B，T 行至少耗 T 单位 B，而只有 T−1 容量，矛盾，故 ConfigOPT(I_T)=T。

整数上界：至少一位 root 无 B，设其得到 s 件 u、全体最低值为 V>0，则 s≥V；失去这些 u 的 s 位 b 仅能共享 T 件单位 w，故 sV≤T，得 V²≤T。最低值有限且为整数。令 q=floor√T，每个 root 取 q 件 u，相应 q 位 b 各取 q 件互异 w，因 q²≤T 可行；其余 b 取自己的∞u，故 IntOPT(I_T)=q≥2。

只有 T² 件 w 需要降度，每件加 T−1 名 helper，所以 J_T 人数 N=T³+T、物品数 T³+T²+T−1。B 的交域 CONFIG gap 是 Θ(N^(1/6))。这与 G 按原人数 n 的四分之一次幂并不冲突，也不能交换 n、N。

## 3. 固定 λ=2 的完整 M-LP 证书

固定 λ=2，取目标 M=T。因 T≥4，有1<T/2，所有单位正端仍 small，所有原∞端重估为 big；没有新增 big 端，因此物品 InfDegreeTwo 语义保持。对所有 roots 与 b 设 z=1/T。root 对每件 u 设 x=1/T；b 对自己 big u 设 x=1−1/T，对每件 w 设 x=1/T；B_r 的左右 root x 仍取(T−r)/T与r/T，未列 x=0。

逐类约束如下：

- 每件 u 的 root/b 总负载为1/T+1−1/T=1；每件 w 的 T 位 b 各用1/T，负载1；每件 B 的左右质量和1。
- 每位 root 的 big B 总质量为1−1/T，每位 b 的 big u 质量也是1−1/T，故 big+z=1。
- 每位 root 的 T 个单位 u、每位 b 的 T 个单位 w，small 效用均为1=Tz。
- 每个正 small x=1/T=z；零端 x=0≤z；所有变量非负。

因此 M-LP(T) 可行。也可从上述 CONFIG(T) 证书剪为 big singleton 或全 small 配置，再取 small 配置质量为 z，得到相同正向证书。这个步骤不需要任何 M-LP→CONFIG 逆接口。

事实上固定 λ=2 时最高 M-LP 参数也恰为 T：若 M>T，单位端仍 small，root 的 small 效用由 x≤z 至多 Tz，而效用约束至少 Mz，迫 z=0；每位 root 于是要至少一单位 big B。T 位 root 对 T−1 件 B 再次容量矛盾。这是本明确族的直接计算，并非两种 LP 的一般同值定理。

两 LP 的最高参数各至少 T，除同一整数 OPT=q 得 T/q≥√T。因 n=T²+T≤2T²，有 √T≥2^(−1/4)n^(1/4)。T 遍历全部≥4整数得到无限参数家族，完整支付 G 的 M-LP 与 CONFIG 各自存在性间隙。

## 4. canonical 复用、比较处置与边界

共享边是 accepted、unconditional、premises_mode=all，source_ids 恰为 A/B，target_ids 恰为 G，whole_result 完整，未含未付 contribution.remaining。本轮逐一对照其全文、三端当前记录及全部 evidence：A/B 正文§8、§9和 M-LP 正文§5.3 的文件 SHA 均匹配，标题各唯一；endpoint_pins 恰等于本任务当前三个 input_pins。路径实际在当前 registry.edge_files 中。边字节 SHA 保持 a92a2135159c895e90b66f6f257b8a22cdb1f6bc17092ce00c315445157a02df，不另复制或重绑。

A 提供反向恢复的全正阈值 raw 合同，B 提供明确可反投影的 J_T 与完整族数据；固定 λ2 证书在关系内部已付清。M-LP 的 D∞ 全阈值桥 H 不是这里的额外必要前提，本包只读其正文中本证书所需的定义、正向 CONFIG 接口和具体族§5，没有把 H 加进 ALL。

当前任务没有 overlap_comparisons、comparison_groups 或 deferred_candidate_ids 中的待比较对象。本轮实际比较了 G 与 A/B 的明确族迁移、原/新人数及 raw/M-LP 层次；已由同一 canonical whole 关系闭合。收据 closed_overlaps=[]、follow_up_tasks=[]，不造尚未发布的后续任务。cap λ1 的非前缀一般反族不参与本证明，也不能据它推断当前 λ2 明确族失败；本轮不重审该反族或其他未分配对象。

## 5. 本轮实读与历史继承

本轮新实读：三个完整对象记录；当前任务全文；G 文献汇编全文（实际使用 MaxMin §2）；A/B 共同正文全文155行、独立复核全文274行；有限 unit-helper 正文§4；M-LP 正文的导言/§1、§3.1、§5.1–5.3；原 PDF p4、p6–8、p12–13及 p7 视觉；共享边全文；先前3B review全文、reading-ledger全文与receipt全文。精确读取范围和 SHA 在本轮 ledger。

历史继承仅指该成熟3B审读和已发表 canonical 关系的来历。先前 review 为155b10384f2e801fe362002ee4ee8780ca44f0e462e863f04da35ea3424faf16，ledger 为def4e77f892d08c8fe6e03578a567699ee05a56a16a9af50d0389441cb75e4a6，receipt 为9359190309ca10493ff61c4e8d4832c711435b09d9d88d4e94dddc17da5931c0；本轮实际读了它们，但不把其所列全部外部原稿、旧程序、其他对象或 p9 读取记成本轮实读。旧 review/ledger 只作历史引用，不列成本包共享资产；本包交独立 review/ledger。

本轮仅运行只读 research show、PDF 导出/渲染，以及路径、字节 SHA、JSON pins 和唯一标题的元数据核对。没有运行科学程序、LP 求解、枚举、历史证书或测试；没有写 clone、Git、registry、队列或 native binding。没有新边，故不需为共享边重绑。发布和 done 由 Root 在实际核对后串行执行，不在本报告预写为已完成。
