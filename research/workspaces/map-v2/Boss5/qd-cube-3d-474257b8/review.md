# Boss5 / 474257b8：QD-decoder 与 cube 当前3D数学审读

结论：保留两条现行 accepted/unconditional、premises_mode=all 边及其 linked 收据。逐式核对没有发现需要更改这两条边的数学缺口。本报告是实读证明后的判断，SHA和semantic pin核对仅负责冻结身份，不充当数学证明。

本次严格只读repo；没有Git命令、网络调用、队列操作、repo写入或spawn。输出仅在repo外。采用当前正式正文及其已展开的必要证明；没有冒称读过历史scratch原稿、外部PDF或重新证明Haxell。

冻结时刻：`2026-11-09T19:23:06.639643+00:00`。当前registry semantic pin `dda1f9bb63c04da3850f6c9712533ed68a74a3d32a84a92ce88fe460766caf1c` 与integration.registry_pin完全一致。registry.edge_files是**相对路径字符串数组**，两条support路径均已列入。

## 两包精确交付与整合

| 包 | 当前队列 | 独立receipt = done内receipt | 当前semantic receipt pin | integration精确一致 |
|---|---|---|---|---|
| `boss5-474257b8-qd-decoder-3a-69d5a688c474b34c` | done / Boss5 | 是 | `6e8fe21e72869090b23c09fc78496e30166574fc0c295bfacefb7e899e78cb42` | 是 |
| `boss5-474257b8-cube-3a-0a0c1be8c9ee5558` | done / Boss5 | 是 | `42827b81d7faf0940f8e8ee808ce1bfb873a6568fb3ae06b8930011ac274cec9` | 是 |

初次读取发生在父Boss同步前，当时canonical边路径尚未出现；最终判定已重读同步后的当前registry/integration。两条edge semantic pin、所有六端点的task/edge/integration/current object pin均逐项一致，独立receipt.asset中的原始边SHA也等于实际文件字节。具体值保存在review.json；没有以初次瞬时未集成状态作为最终结论。

## QD-decoder：ALL如何支付整目标

边 `b5-qd-and-private-tree-config-force-decoder-parameter-growth` 的两个联合前提是Q_D精确整数值/CONFIG证书和v3私有树完整实际存在界，终点是 `M-4bfb99ccca4f4f77a6aaee6882ef1170` 的必要条件定理。

对每个显式整数D≥2，Q_D的main选在某行并领取至少两个g时，对应helpers为了正值只能共同领取唯一A_a，违反资源不交。因此任何正partial分配的main至多领取一个g，其值≤1/D。领取一个g、对应helper取A_a、其余helper各取home，给V=1/D。完整norm1 flat桥把领取的原incidences外送、其余所有state原jobs留private，给峰≤2−V；反向任意完整C<2调度从selector所在state读取至少2−C的外送质量，每资源至多一个unit，给原不交partial分配。所以OPT(P_D)=2−1/D，包含高峰分支的排除，没有删除未选state任务。

共同λ为main每state 1/D、每helper home/parking为(1−1/D,1/D)。每g与每A_a的资源容量恰为1。每state private以λ放selector singleton、以1−λ放全部该state incidences，资源端按λ放unit singleton；Q_D没有零权项，所有配置负载≤1，每selector及每原incidence恰覆盖1。这是真正的全原任务CONFIG1证书。

对目标，v3要求所有内部机在不同states间也完全私有，全局d同时是满树分叉数并规定父端时间1/d；每root只有一个selector，leaf只有唯一unit外端。μ是每完整state对单外机的实际叶逆像最大重数，不是所有states总共享数。CONFIG1给T=1、a=d；取r=ceil(d/(μ+2))。由于d≥(μ+2)(r−1)+1，b=d−μ(r−1)≥2r−1≥1，且(2r−1)^h≥2r^h−1。该数值条件恰支付rainbow blocker/Haxell存在性输入。

v3证明先用occurrence分桶与raw q次可加性把“命中所有rainbow子树”化为逆像叶数下界，再以同一λ的multiplicity容量得到|X|≥b^h|I|。rainbow子树资源数为r^h，加root后的总边大小为r^h+1，严格Haxell阈值是(2r^h−1)(|I|−1)，不存在额外除μ。最终仍在原d树回填：活跃内部机一枚incoming unit加d−r枚small，负载2−r/d；所有未选、零λ、非活跃分支的jobs全部父置，负载≤1；外机至多一unit。因此完整目标有实际C′≤2−r/d<2。

只对这一份目标低峰见证调用必要条件定理的假设解码，就得

\[
2-1/D=OPT(P_D)\le C'\le2-r/d,
\qquad Dr\le d.
\]

r≥1给d≥D，r≥d/(μ+2)给μ≥D−2。固定d0不能覆盖D>d0；以整数松上界μ0≥μ代入同一定理，得到D ceil(d/(μ0+2))≤d。当D>μ0+2时矛盾；D=μ0+2时等价于D整除d，仍然只是必要条件。D=2时μ≥0这一投影界较松，实际模型μ≥1保留，无退化矛盾。

目标CONFIG1经v3使OPT′<2，两边有限非空实例的合法assignments集合有限且最优值达到。解码作用于目标最优调度给OPT(P_D)≤OPT′；反过来若该标量序成立，对每个目标低峰调度采用同一份源最优调度即可。所以存在性解码与该标量序等价。没有算法性、统一可计算选择、前向调度映射、高峰解码或复杂性前件。

accepted/unconditional的对象是“若CONFIG1且有低峰解码，则参数必须增长”的完整已证定理。它没有把满足合同的编译存在性当作已证前提。两源均实质承重，保ALL；不拆为单源足够边。

## cube：D后接C的全部任务与计数

边 `b5-real-path-and-zero-cell-cube-give-unrestricted-degree-transfer` 的终点是 `M-4aa4bcc7358b4ab8bf1bc53f57d3f1d1`。先D后C的顺序不可省：C单独只接受资源跨组度≤3输入，D实际支付该前件。

D将资源u的d_u个incident groups分别接到d_u个ports，零权membership仍按组并集计数。相邻ports间建立d_u−1个二态helper，每个helper真实具有两private、一selector、两incidences；每state恰一件private1/port1 incidence。d_u=0保unused，d_u=1无helper。源C<2时每原资源至多一unit外送，按实际外送位置留孔并匹配全部helpers。selector留所选private、所选incidence送port、未选incidence留另一private，全部helper机器负载≤1，原全部任务决定不动。

反向给任意目标C<2完整调度，每个选中helper incidence若不外送就与selector形成2，故被迫占一个port。d_u−1个helpers占不同ports，未选helper额外外送只会进一步挤占容量，原旧任务最多一件外送。删除helpers并合回原资源合法且峰不增；没有假设目标采用正向matching，也没有遗漏未选原state外送或零权原job。

C为D的每个资源保独立tag的完整27格cube。对接触变量的至多三组赋互异index，所有states使用含z*=(1,2,3)的完整九格切片。原job精确映到active格，原零权job也按身份保留；缺state-variable位置和非active格添private0辅助任务。原selector全部资格不变。空组资源并集另加独立dummy cube，unused原资源也保完整cube。

C的扩展将辅助任务放private0，保每个原job执行端，故峰完全相同；任意目标调度按身份删除辅助后逐原job投影，峰不增。C这一步甚至不需要C<2。组合的正向依次D、C，反向依次C、D，保全部低峰完整调度。

所有模型均有全private峰≤2且selector使OPT≥1，最优值在有限assignments中达到。一侧OPT<2时低峰映射给双向比较；一侧OPT=2而另一侧<2则反向产生矛盾。因此OPT精确相等含2。给定峰≥2的调度可输出另一侧全private基线，但不保给定外送决定。归一化原W=1时，D所有新helper也W=1；C只添零权。因此每个v∈(0,1]的partial阈值双向保留，有限非负allocation最大值使V=0一并保持。一般W≤1只沿边使用调度/OPT合同，不套OPT=2−V_raw。

令原组数n、state/private数a、incidences L、组资源并集大小q_g，并定义p=Σ_ud_u、h=Σ_u(d_u−1)_+、u0为unused资源数、e为原q_g=0的组数、T0=Σ_gK_g max(1,q_g)。这里h是helper数，与另一包树高度符号没有模型对应。

| 账本 | D(P) | E(P)=C(D(P)) |
|---|---:|---:|
| groups / selectors | n+h | n+h |
| states / private machines | a+2h | a+2h |
| resource machines | p+u0 | 27(p+u0+e) |
| incidence jobs | L+2h | 9(T0+4h) |
| all jobs | n+L+3h | n+h+9(T0+4h) |
| finite processing entries | a+2L+6h | a+2h+18(T0+4h) |

每helper两states各含一port，但组并集有两个ports，C会对每state补齐两个变量，所以ΣKq增加4，确为4h而不是2h。每selector有限端数等于其组菜单大小，所以最后selector entries是a+2h；每incidence恰两个有限端，包括private0与unit资源端。总机器为a+2h+27(p+u0+e)。p,h≤L、e≤n、T0≤a max(1,|U|)，时间仅复制旧二进制有理数或0/1，稠密矩阵乘积也按总显式位长多项式。K_gq_g不能误作原incidence数或线性规模。

C保持的是D(P)的完整组交互图。两旧组各一state共享r≥2个资源、权均1/r时，原M=κ=1；D为每资源添一个helper，每旧组邻接r个helpers，故M=r，port上的正权同时为1/r和1，κ=r。C只添零权且保D图，最后M=κ=r。固定三坐标/三标签不能恢复原M或正权比。

## 已知措辞、精确处分与模型边界

D登记v4的objections已经明确隔离read-after §2的旧合写：“每个 helper 的 selector、选中 incidence 和未选状态 incidence 都在其 private machine 上形成实际负载一。”按字面理解会把selector与selected incidence叠在一起达到2，确实不能当作证明。本次采用并直接核验的是D主正文§3的正确三任务安排：selector留所选private，selected incidence去匹配port，unselected incidence留另一private。主证明、现edge解释、receipt及v4 objections完全一致。无需因此改动两条现行边或宣称新repair任务；如以后改历史审查正文，应保留provenance并按影响刷新冻结引用，不能无痕换字节。

三态N的binary-selector tree每顶点对应一组并有自己的unit selector、own singleton，原selector资格改变；再接真实port路径。v3则要求全局d、父端1/d及每root唯一selector、内部机全state私有。图形二叉不能把N认作d=2的v3结构；两条结论没有冲突。cube边也没有采用N压态，Kmax仅为max(Kmax(P),2)。

精确处分：两条边和两receipt均retained，无replaced/retired资产，无新数学修复请求。外部Haxell为已登记v3的既有有限存在性依赖，本次不重证；没有宣称变参位多项式输出、外审或新颖性。

## 可追加的实际integration文字

### archives/unrelated-machines

**comparison_scope**：本次3D实读Q_D与CONFIG保真解码参数目标、私有树v3完整证明，并实读真实路径D、零格C、三态N及其范围审查，分别比较两条已done包的全部联合前提、完整目标、全原任务调度、有限端点及计数。独立重算当前两receipt semantic pin、六endpoint pin、两edge semantic pin及canonical路径，均与integration精确一致；这项绑定核对与数学判断分开。

**outcome**：Q_D的V=1/D由同行helper对唯一A_a的整数鸽巢给出，完整flat桥保全部未选state原jobs并得OPT=2−1/D及CONFIG1。私有均匀树v3在T=1、r=ceil(d/(μ+2))下给完整实际峰≤2−r/d；目标向源的C<2存在性解码于是迫Dr≤d、d≥D、μ≥D−2。松上界μ0仍可代入，D=μ0+2时整除仅必要；有限最优达到给解码合同⇔OPT(Q_D)≤OPT(P′)，没有算法性或hardness结论。另一条ALL由D先支付资源组度≤3，再由C保全部原job身份及完整九格切片；任意低峰调度两向峰不增，OPT=2端点用全private基线闭合。原W=1时才沿边调用全部正partial阈值及V含零。设p=Σd_u、h=Σ(d_u−1)_+、u0为unused数、e为原空组并集数、T0=ΣK_g max(1,q_g)，则E资源27(p+u0+e)、private a+2h、selectors n+h、incidences9(T0+4h)、有限entries a+2h+18(T0+4h)；每helper两state对C各补两变量给4h。C保持D(P)的图；两旧组共享r≥2个权1/r资源显示原M=κ=1而E后M=κ=r。两条边均保留现accepted/unconditional与完整ALL。

**范围及未付义务**：参数充分性/锐利性、存在性编译的实现、变参Haxell输出、一般UM困难性、全正格/label唯一定价及一般UM到flat不由本次结论支付。它们是范围外一般命题，非这两个已交付包的pending任务。保留全档其它真实未决项，不凭本次局部审读清空全档pending标签。

### cross_archive_review

**comparison_scope**：本次QD-decoder与D后接C两条关系均在archives/unrelated-machines内；比较了flat菜单、完全私有均匀树与binary-selector/port正规形的实际处理端、selector和job身份。

**outcome**：本次没有新增跨档逻辑边。N为每树顶点各自unit selector的正规化，不能由其二叉图形认作全局父端1/2、内部完全私有的v3模型；因此不与d≥D障碍冲突。三坐标切片仅表示显式flat输入，固定几何三不控制原M、正权比或未知source gap。Q_D是CONFIG/整数值分离，Santa/SC的最大化值与UM的最小化峰须经norm1全任务桥区分，不能据目录相近迁为一般UM hardness、近二不可能或其它存档的保证。

本次实际读及端点scope仅为`archives/unrelated-machines`；不要新增虚假的跨档逻辑边或附会其它archive_reviews。两包局部`unresolved_for_reviewed_scope=[]`，不能据此清空尚未在本次实读的全档未决项。现integration中的全档通用`cross-batch review pending`标签也不能被重新解释为这两个任务尚未done。

## 一般未付命题与实际pending分开

未付的一般命题有：参数必要条件是否充分/锐、满足解码合同的编译是否存在、变参Haxell实际调度输出、真正近二flat源与一般UM困难性、全正格/label唯一定价/任意UM到flat。原M/κ保持已被所列族否定，不能当作待证正面性质。

**这两个审读包的实际pending任务为空**：两当前task为done、两独立receipt与done嵌入receipt相同，全部当前semantic pins已exact-integrated，没有follow_up_tasks。cube的in-packet overlap已由这条ALL边处置。没有用数学上开放的一般问题虚构队列待办；没有审断其它available/claimed任务。

## 实读文件manifest

下列SHA都是冻结时完整原字节SHA；section-only只表示实读区间，SHA仍绑定整文件。registry、integration、coverage只读取指定记录/字段，其余数学未宣称读完。JSON保存全部六端点完整记录、逐项SHA/pin结果及实读范围。

| 文件 | 实读范围 | SHA-256 |
|---|---|---|
| `archives/unrelated-machines/state/定理/CONFIG保真低峰解码的私有树参数障碍--定理.md` | full | `e3e985e7d838474c692d633a77041dad85375b337ba704877376d73955f60f21` |
| `archives/unrelated-machines/state/定理/规范化平菜单的CONFIG与正支撑LP双向保持--定理.md` | full | `8bfbaa80b98546b6d1320e9760bb9491165e26a6cef1b6cd35eb86116c822f66` |
| `archives/unrelated-machines/state/定理/私有菜单树有界叶重数配置界--定理.md` | full | `5b810c65140f9581fb362f8ff739b09f019a7c435a1bc2eb3d7a34d42c3041d3` |
| `archives/unrelated-machines/state/资料/加权菜单Santa值桥与不相关机转换--资料.md` | full | `d01ac63a4da47c8cfaed8ed296efa00ea4b375ef8b567c0338c938d6d175aa8c` |
| `archives/unrelated-machines/state/定理/完整菜单的资源度三路径归约--定理.md` | full | `afb7a6751e65f5e968a2b8798b8ba284983d64694fde1a463dae991b0018bb34` |
| `archives/unrelated-machines/state/定理/三坐标零权切片的精确菜单嵌入--定理.md` | full | `986db069a11f89723aa3378bee60252d9a2e89bc807ecabe759973f8797861e9` |
| `archives/unrelated-machines/state/定理/归一化菜单的三态资源度三正规形--定理.md` | full | `31f1fb774f856f42255d1cd8b56c7a77d8396b2417b05e4d0b2f1d32e1195d1a` |
| `archives/unrelated-machines/state/审查/三坐标与三态路径正规形范围审查--审查.md` | full | `1239534319b20364efc91d34af78913b3dfe1b8898a1949c0c9d119c6dc025e0` |
| `archives/unrelated-machines/state/审查/规范化平菜单Exact与Proof版本核验--审查.md` | full | `acd5fa40598e0e880083405a713752569671abefc20ac63d32576c6bc717cc84` |
| `archives/unrelated-machines/state/审查/规范化平菜单row3degree9独立预Exact记录--审查.md` | full | `29f6c62f6fdbc4dfbc6ad99d832c9a25b5527f044c572bd14c322acd3689e6a8` |
| `archives/unrelated-machines/state/审查/规范化平菜单v1v3的独立与作者核验--审查.md` | full | `61835242b90509d0f831c95ebb38f1b002779716de335568a4fcf01cfd1321e6` |
| `archives/unrelated-machines/state/审查/归一化菜单福利与配置证书双源审查--审查.md` | full | `a5d9a684e8d8413457f5cf999e28b8a6aa93b140256be3031d6f3e2e02742195` |
| `archives/unrelated-machines/state/资源/单位读出树与实际调度地板的限定合同--资源.md` | full | `a65857c226db1209e4fd96add555e753ad0db130318adfc2d2f1a8f58473845e` |
| `archives/unrelated-machines/state/审查/私有树有界重数v3四源精读与证明边界--审查.md` | full | `fad498824aa96153a0ef0c0b4fdfd9cfac56bf0018abe8c48b2712a4cc1805f9` |
| `archives/unrelated-machines/state/审查/NSW比例勘误与flat菜单证明读后--审查.md` | section-only | `828aaf4fc65ad4b38350e639aceeccab5562ed0bae8e7d7f1d386f8923ba4024` |
| `AGENTS.md` | full | `a24b90db5ceabf26f4db3b831a4d63d121133ecc35b283ed5dd334c77cb38c92` |
| `research/IMPLEMENTATION.md` | full | `28bdc88dd144cad15c2081b2f00a3d1a7023792a0dde04c37831944d49e56632` |
| `prompts/03-map-worker.md` | full | `6629f71923c54d994297d54c3737b285227b72c463641d318c3f61c9342d07b2` |
| `research/registry.json` | six exact endpoint records plus edge_files structure/list; not whole registry mathematics | `63419139c13dddb237985359831c945135ef804f45453ef159c4872f874bf161` |
| `map/integration.json` | two task receipt pins, two edge pins, six object pins, registry pin, archive scope and cross_archive_review | `428ba4ba84a5f2b09b014af38542989d100d9f0974ad7cc720addb88c1358832` |
| `map/coverage.json` | two target coverage records | `37720700374da7e5f86f33b91e5a6605c104925220fe992f6dbec7cf6c3a81d7` |
| `map/edges/boss5-474257b8-qd-decoder-3a-69d5a688c474b34c/support.json` | full | `92611abbd9eaf8072df600f345908257e578c54a06d7d1817d7ed6c6864e27a2` |
| `map/receipts/boss5-474257b8-qd-decoder-3a-69d5a688c474b34c.json` | full | `80fe96ba3dc625ac9557c975885701db834743bd7071dd79509d259f102f84f2` |
| `research/operations/map-v2/tasks/boss5-474257b8-qd-decoder-3a-69d5a688c474b34c.json` | full | `5f8a8856a2f5fa5454d4bb12603fdb775f5450bf709445a2f97229fd6ab4e2ed` |
| `map/edges/boss5-474257b8-cube-3a-0a0c1be8c9ee5558/support.json` | full | `83bc692edbad998f872072305d6690f47a2e3f31f552f151abbcf1ede4d23459` |
| `map/receipts/boss5-474257b8-cube-3a-0a0c1be8c9ee5558.json` | full | `efc3e5903b46575da4cf01ebc4c5bab82d42fbd52b30fd4866c133b2528b7444` |
| `research/operations/map-v2/tasks/boss5-474257b8-cube-3a-0a0c1be8c9ee5558.json` | full | `b87f79bc5441f1f775405b7e80a97e7ae2b18367e89b18320e063929d16f218b` |

另外只读tools/research_runtime.py的pin、_map_registration_pin及final receipt核对段，和tools/map_tasks.py的receipt/assemble pin生成段，目的仅为解释原始SHA与canonical JSON semantic pin的区别；未调用会读Git/队列的CLI。
