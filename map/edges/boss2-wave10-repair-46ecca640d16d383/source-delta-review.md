# F v5 零 job 源更正：有限阈值与同一 ∞ 输出的定向继承

本任务 `boss2-wave10-repair-46ecca640d16d383` 继承前任 `boss6-mlp-g-scope-repair-b2229510e88b478a` 及其祖先已经完成的成熟数学、原 PDF 指定页实读和比较。本次 fresh worker 新做的是当前合同、源差分、两条受影响关系完整证明和字节追溯的定向复核，不把继承的 PDF 或旧程序实读记成本次新实读。三个核心 A、B、D 继续 linked；F→A、F→D 保 accepted whole 并各生成一份当前替换文件；A→B 与其余六件旧说明资产保原路径和原 SHA。

## 1. 精确输入与唯一源差分

简写沿用旧包：F=M-080d9b22ae87408f9a673a898c7a6dc3 v5；A=M-16209762a32e42e48ec20b76381b5e9d v1；B=M-7bc9eab74ecd475db7df33c3f4b75e61 v1；D=M-a9534c70ffa74fca9a91cd270468de3f v3；G=M-b126c4b3ff29400589f7f38abdca4d85 v4。另两项当前只读合同是 DegreeTwo 四近似 M-e52574ff126d4b128f222053c97bf596 v3 与 VW 后端 UM-VW2010-THEOREM12-BACKEND-PRECHECK-v1 v1。

本次完整读取七个当前登记合同。按规范 JSON SHA 独立计算的七个 pin 全部等于本任务 input_pins；definition pin 为 `e660f352d9b33e9f7b13fcf3b0f78b2e49e9af3f42427ea33f835186b2b22bc3`。本地任务为 claimed/Boss2，request `e72d8c2d0b02445894f91ae2fa94b77b`；认领已 pushed 及 remote `d02fbad671bac9421247d224e64ff39d36ba9bd9` 由 Boss 通知，本 worker 没有查询远端、执行 Git 或原生命令。

唯一正文版本变化在共享审查“归一化菜单福利与配置证书双源审查--审查.md”§二.1：补配置从“以 1−λ 权重放所有 positive incidence”更正为“以 1−λ 权重放全部 incidence jobs（含零 jobs）”。当前全文 SHA 是 `33bd31b883b26f49508808dd7175cd104f391b86642bff90ea2bce7f1142097b`；将这唯一片段原样反换后，字节 SHA 恰为旧 `63629abaa5cd2bcc0e42ff051936b91882ea63c711dfdac231f238763b682255`。这核实是单处源更正，未把旧全文仍为 current 作断言。

数学原因逐 job 可见。private 的 selector 配置以质量 λ 同时含零私有时间 incidence；补配置以质量 1−λ 含全部 incidence。因此每个零 job 覆盖为 λ+(1−λ)=1，私有负载仍为零；positive incidence 私有覆盖 1−λ、资源 singleton 覆盖 λ，总覆盖同样为一。selector 按组覆盖一；资源使用只计 positive support。F 的主正文 §1 已明确给出 selector 加零项与全部 incidence 两份配置，本次新实读确认其原字节 `8bfbaa80b98546b6d1320e9760bb9491165e26a6cef1b6cd35eb86116c822f66` 未改。更正不改变 F 的 statement/model/quantifiers/assumptions 或本包 unit-helper §4。

## 2. F→D：完整固定正阈值整数合同

固定任意有限实 t>0。对旧物品 j 的 d>3 个不同正 owner i_1,…,i_d 建 d 份专属 copy c_r，只让 i_r 在自己的 copy 保原值；添 d−1 位相邻 helper h_k，每位仅在 c_k、c_(k+1) 取值 t。低度物品不变。正向旧 j 给 i_r 时，把 c_r 留给它，k<r 的 helper 取 c_k，k≥r 的 helper 取 c_(k+1)；旧 j 未用时任选一 hole。全部 helper 得 t，原玩家逐物品效用保持。

反向任一新 t 分配中，每位 helper 至少占一份正 copy，单归属使 d−1 位 helper 占互异 copy，故旧玩家合计至多有一份正值 copy。删零值使用后把它合回 j；不同链彼此独立，不发生旧物品冲突，旧玩家效用保持。仅对 d>3 的局部应用来自源证明逐物品独立，未删除任何输出中仍存在的 helper。

有限有理原值及有理 t 的算法合同可先除 t、在目标一用 F，再乘回；即使归一化旧 OPT>1，给定达一分配仍按上述 matching 转换，不需 F 关于 oldOPT≤1 的精确最优值附加结论。原端允许符号 ∞ 时，在本次固定 t 先封顶 min(v,t)：非负 bundle 达 t 当且仅当封顶后达 t；随后恢复旧玩家 copy 的原值，正向效用准确恢复，反向仍保 t。任意实 t 的数学 matching 与显式有理输入/t 的有限编码声明分别成立。

内部 copy 为一旧端加两 helper 端，总正度≤3；端点≤2。S=Σ_(d_j>3)(d_j−1) 给 n′=n+S、m′=m+S、E′=E+2S。n,m≥1 时规模 O(nm)，空物品的正阈值直接 NO；构造与有理缩放按总输入位长多项式，不按 t 数值枚举。t=0 不用 helper 占用论证。这支付 D 整条整数阈值、双向见证、规模和编码合同；没有声称 DegreeTwo、任意 OPT 全值保持或一般 CONFIG/M-LP 结论。源 §二.1 的 flat 零 job 配置没有进入这些步骤。

## 3. F→A：完整同一 ∞ 输出与 CONFIG 合同

先对固定输入 I 建同一 J∞：上述 helper 值改为符号 ∞，构造不含阈值。对每个有限实 s>0，整数正反 matching 仍成立。若借 F 有限证明，可选有理 H≥s，将原端截 min(v,H) 再除 H，在目标 s/H≤1 应用源，然后恢复原 copy 值和 helper ∞；非负性保证每次封顶都保持达 s 判定。H 只是复用证明的参数，最终实例仍是先建好的同一 J∞。

CONFIG 正向先删零，记旧 j 在各 owner 配置中的边际 q_r≥0、Σq_r≤1。选 w_r≥q_r 且 Σw_r=1，W_k=Σ_(r≤k)w_r。旧配置按 owner 重标 copy；给 h_k 两份 singleton {c_k}、{c_(k+1)}，质量分别为 1−W_k、W_k。两者非负、和一且值 ∞。端点或内部 copy 的 helper 边际均为 1−w_r，叠加旧 q_r 后 q_r+1−w_r≤1。不需要构造不同玩家配置的联合整数分布。

反向对任意 s>0，每位 helper 的每个合法正质量配置至少耗一份相邻 copy，故全部 helper 的边际消耗≥d−1；d 份 copy 总容量为 d，留给旧玩家的总边际≤1。每个旧玩家在这条链只有自己的 copy 有正值，所以删零后投影不会在同一配置生成重复旧 j，效用及配置质量保持，得到旧 CONFIG(s)。全部有限正阈值双向保持遂给整数与最高原始 CONFIG 阈值的扩展最优值相等，含零和 ∞ 端点。

若原物品 ∞ 度≤2，把这些旧 ∞ 端排链两端。内部旧端有限，加两位 ∞ helper 恰给 ∞ 度≤2；端点一 helper 加至多一旧 ∞ 端也≤2。一般旧玩家 ∞ 度不因此受限。{0,1,∞} 值域保留；精确 counts 同 §2。每 helper 至多两 singleton，有限有理输入见证 Q 项时新支持≤Q+2S；残量、部分和、复制及常长 ∞ 符号的编码按给定证书总位长多项式。此为证书转换，并非配置 LP 搜索算法。

有限 H 在 0<s≤H 可用；若存在被降度链且 s>H，每 helper 达标需两份 copy（s>2H 时无合法配置），2(d−1)>d 排除整数和 CONFIG。没有降度链时输出恒等，不能套此截断论证。有限逐阈值输出不等于同一 ∞ 输出的全正阈值量词。以上支付 A 全部目标，whole/ALL/unconditional 均保留，源零 job 更正不产生新前提或缺步。

## 4. B、G 与两个算法端点的继承范围

本次新读 A/B 当前完整正文及 A→B 完整边，也以旧三份 review 的直接数学和既有审读为继承来源。明确 I_T 在原人数 n=T²+T 下，root full-u 质量 1/T，B_r 两端 singleton 质量 (T−r)/T、r/T；每个 auxiliary 的私有 ∞ u 质量 1−1/T、full-w 质量 1/T。每行质量、每件 u/w/B 容量均为一。s>T 迫使 T 个 root 对 T−1 件 B 需求边际≥T，故 ConfigOPT=T。整数分配有无 B 的 root；它取 a≥V 件 u，使 a 位失去私有 ∞ 的 auxiliary 共享 T 件 w，aV≤T，故 V²≤T。有限最低效用为整数；q=floor√T 用 q²≤T 的块内分配达到，故 OPT=q。

只降度 T² 件 w，S=T²(T−1)，得到 N=T³+T、物品数 T³+T²+T−1。A 保全部正阈值，故输出仍 ConfigOPT=T、OPT=q；全部 helper 计入 N，比例 Θ(N^(1/6))，不是把原 n 的 1/4 指数照搬到 N。A→B 不含 F 端点，也无已变 source evidence；其原字节 SHA `02c845cd2426d6e1387552412d6f8a6fa4591423cf446cffcddadaf38b24ccbf` 与全部绑定均当前，原路径保留。

G v4 的原 n 存在性、固定 λ=2 M-LP 证书及 cap 边界的完整审读继承前任 review/ledger，当前 G 合同新读且相关正文 SHA 未变；本次没有另读整篇 H 或重导 PDF。旧 G v4 证书令 z=1/T、small x=1/T、big 质量 1−1/T；T≥4 时单位端仍 small，支付其原 n 的另一条存在性 gap。它不成为 F→D、F→A 或 A→B 的额外逻辑前提；不宣称一般 CONFIG/M-LP 同值，也不恢复无条件 cap 逆桥。前任对有限 H 的 cap-M-LP 可达 4H/3 及 raw CONFIG(M/2) 反例的范围判断按未改字节继承。

D 与 DegreeTwo 四近似、VW 后端的比较同样继承：内部 copy 可有三正端，没有 degree3→degree2 的映射；VW success 仅保证 T/2，failure 才证 OPT<T。当前两个完整合同与正文/证据 SHA 均核，未重审其算法证明。A/D、A/F、B/A、B/G、D/F、D/G 与两个后端的全部旧比较范围继续保留，不为来源相似或 identity refresh 另造逻辑边。

## 5. 历史审读时点、资产与后续路由

前任九件资产已逐一核原始 SHA。两条受影响旧边以相同 edge_id 在本任务目录生成唯一替换，原路径完全不改；其余七件以原路径、原 SHA retained。七件中包括 A→B 和六件 review/ledger。旧文件所写“当前 F v4”“所有绑定当前”“三边无需 rebind”等句子只描述当时审读快照，不能解释为 F v5 后仍当前；本 note 与新 ledger 明确补上当前差分。旧读者对 PDF 页、截图、外部临时路径和科学程序的实际阅读/未运行声明保原作者与原时点，不改写成新 worker 行为。

原后续任务 `boss6-inf-chain-transfer-3b-ea6be0c00b1186cf` 是真实历史路由，现虽 done，其 F 输入已因 v5 改版过时。Boss 已确认 source-only 正式 successor `boss2-wave11-inf-chain-transfer-repair-repair-f72bef2e3569ee84` plan pushed（request `3b4f24c492c845e59c12b434783bca35`，remote `a7f67767f0981cc2ab35a1dbb0cbde87bacd3c09`）；它 depends_on 本任务并仅写自身目录。本任务不声称旧 ea6be 是当前有效交付，也不把已证明的 H/C 数学记 open。后续包须引用本任务这唯一一对替换路径及最终 native bind 后的实际 SHA，不能再造第二套同 edge_id。本任务没有声明新的 follow-up 对象对，closed_overlaps 保空；active follow_up_tasks 只接这个已发布 successor，旧 ea6be 保在历史路由字段。

本次没有科学程序、证书或枚举重跑，没有新登记对象。新边的旧 binding 字段移除，最终 native edge-bind/check、receipt 最终 asset SHA、checkpoint、pushed、done 与整合由 Boss 串行完成；本 worker 只交已实读并数学 accepted 的当前内容。
