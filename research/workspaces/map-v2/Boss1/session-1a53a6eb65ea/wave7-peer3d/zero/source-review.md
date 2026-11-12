# 六源 zero-incidence 定向 source review（冻结）

本报告是 Boss1 身份下的独立只读 3D 窄核，可采用为此次 source delta 的数学审读；不是 primary claim、native done 收据、repair 完成或 canonical 整合证明。没有修改仓库正文、登记、边或队列，没有运行旧科学程序。冻结读取仓库 `/workspace/scratch/1a53a6eb65ea/co-work-anl-boss1`，最终 HEAD `90e4ff1723256c59b1e87706b172c13fd67a2f6a`。读取期间 Root 从 `2ed7ad475c5b5b0596e9f8aa763acc0d0231ff5a` 同步到该 HEAD；最后又核六条当前登记的 native `research_runtime.pin`，均与 Boss2 勘误列出的 new pins 一致。精确文件 SHA、对象记录、任务状态及观察时刻在同目录 `snapshot.json`。

结论：此次修正必要且充分。旧审查摘要把补配置写成只有 positive incidences，会使零私有时间 job 仅获 selector 配置的 λ 覆盖，一般小于一；λ=0 时甚至覆盖零。当前改为补配置包含全部 listed incidences 后，与从未改动的主证明完全一致。六对象的 title、kind、truth_status、model、statement、quantifiers、assumptions、scope、body、sources 均逐字段与 `9454c751c^` 比较相同；只有 version、evidence 的共享源 SHA 和 objections 的勘误追溯变化。没有发现由此产生的数学新缺口，但受影响旧边和回执仍需要正式 successor，不能以本报告清 pending。

## 1. 实读范围和精确 source delta

完整实读现行共享审查《归一化菜单福利与配置证书双源审查》、共同主证明《规范化平菜单的CONFIG与正支撑LP双向保持》、三份其余主 body《近完美归一化robust源四源审查》《归一化门控菜单v2三源精读与13-8算法版本审查》《门控归一化FSLP四源清洗》，以及六个完整 registry records。共享审查 current SHA 为 `33bd31b883b26f49508808dd7175cd104f391b86642bff90ea2bce7f1142097b`；共同主证明 SHA 仍为 `8bfbaa80b98546b6d1320e9760bb9491165e26a6cef1b6cd35eb86116c822f66`。

读 Boss2 的 `zero-incidence-source-correction.json` 全部；对 `zero-incidence-impact-3d.json` 实读结论、数学核、六对象、8个有效head/7个被替代历史done、active任务、9条edge审查、wave9建议与阅读边界。另完整实读该报告定位的9条现有 edge JSON，独立比较它们实际使用的 mathematical clause、whole/contribution/context 和当前端点。其它历史阅读附件、DNS/BCG/Haxell原文、旧科学代码和有限证书运行按成熟历史继承，未冒称本次重新全文核验。

旧句“以 1−λ 权重放所有 positive incidence”与新句“以 1−λ 权重放全部 incidence jobs（含零 jobs）”只改变共享审查 §二.1 的正向配置摘要。旧 SHA `63629abaa5cd2bcc0e42ff051936b91882ea63c711dfdac231f238763b682255` 不再绑定当前文件。引用 §一 的 evidence 也绑定 whole-file SHA，因此仍须更新，不因所用章节数学未变而保旧 SHA。

## 2. 双配置逐 job 核对

固定 state，记正关联集合 I+、零私有时间关联集合 I0。私有机两个配置为 A={selector}∪I0，权重 λ；B=I+∪I0，权重 1−λ。norm1 使 A 的负载为1，B的负载为全部正私有时间之和1。它们是配置概率，不是同时执行这两份任务的完整实际调度。

* 每个零 job 在 A、B 均存在，且只在该 private 端安排，覆盖 λ+(1−λ)=1，负载为0。
* 每个正 job 在 B 获私有覆盖1−λ，在其资源机 singleton 获覆盖λ，合为1；资源端用时为1。
* group selector 在各 state 的 A 中获得总覆盖 Σ_s λ_gs=1。
* 每个资源上只为正 incidences 放 singleton，权重总和 Σ_{g,s:u∈P_gs}λ_gs≤1；剩余给 empty。不为零私有时间 incidence 再收费，zero/unused resource 可全为空。

λ=0、λ=1 两端同样成立；indexed duplicate states 仍按各自 job 身份覆盖。零 job 有合法 private endpoint 且耗时零，不能因为未进入 FSLP 列而删除该物理 job。修正恰好恢复完整原任务覆盖，没有改处理时间、资源容量或阈值。

反向设 α_gs 为 private 配置包含 selector 的边际，A_g=Σ_sα_gs≥1。每个正 job 的 private 边际至多1−α_gs，所以其资源端边际至少α_gs；unit resource 的合法阈值1配置至多含一个关联 job，故每资源的正支撑 α 和≤1。取 λ_gs=α_gs/A_g 只减少列使用。零 job 可以与 selector 共存，因此它不满足这个排斥论证，不能把它计入正support列。该段未因新句改变，也没有把 weighted Σpλ 容量冒充0/1 support容量。

## 3. 阈值、福利和实际调度分别支付

state-dummy SC 的阈值1桥仍使用每state实资源总值1、每group K−1枚unit dummy。FSLP 给有限 CONFIG(1)；若 t>1，每名state-agent每个合法配置都须含本组dummy，K名agents各至少一单位dummy边际而只有K−1容量，故最高有限阈值恰1。先付此上界，才能在 Q_D 复合链中调用 SC path 的旧最高阈值≤1前件。一般SC path正向只给0<t≤1的证书迁移，反向任意t>0仍允许helper配置含两端copy，不能强剪singleton。actual分配的0<v≤1正向及任意正值反向是另一合同，精确actualOPT相等须旧actualOPT≤1。现行主证明及9条相关边保留这些区别。

完整 P_gate 的 β* 是允许选择部分组的 balanced value；flat 的 V 是所有组的 max-min value。两者不能互换。对 P_gate 的正向完整实际调度，root pin留root；H内connector去gate、selector去其选中state private；H外connector留root、selector去gate；只将选中state在其bundle上的正incidences导出，剩余全部incidences（含零、未选states）留原private。负载分别为 root 2−|H|/n、gate 1、选中private 2−v、其余private≤1、资源≤1。β=0时用完整峰二基线。反向只在 C<2 使用unit资源独占，得到 β*≥2−C；C≥2另用β*≥0。它没有调用 flat CONFIG 的两个随机配置，也没有把分数CONFIG当作实际调度。

福利总可行 LP 是 z/x 与 x≤z，不是 unit-FSLP。初始正tail容量Σq≤1只在初始分布用于舍入界；条件化后用精确有限level乘积重新算，不重复套容量界。13/8全类对象不要求unit-FSLP，其绝对13/8子保证才要求给定FSLP。近完美robust对象分别量化 NO_≥ 和 NO_> 的全部真实allocation，h<γn、δ<1给两者共同严格福利上界；(5/8)(1−η)≥γ+(1−γ)δ允许等号。共享源§二.1此次补零句没有改变这些论证。

Q_D 本身各 incidence 私有值为1/D或1，没有此次漏覆盖的zero job；它的共同λ证书和CONFIG(1)继续有效。完整flat UM actualOPT=2−1/D、SC actualOPT=1/D与最高CONFIG阈值1仍是不同模型的结论；本次只确认 source delta 不影响成熟整数/正规化论证，没有把它们重算为一条新的 primary proof。

## 4. 正式 repair 仍未完成的精确范围

最终本地已发布 task metadata 搜索所有 `supersedes`，8个有效done heads中只有 macro 的 `round20-um-macro-source-repair-repair-7adac135318f96e8` 有 successor：`boss2-wave9-macro-repair-3da3e018da6128bc`。但 wave9 当前 state=handoff、owner=null，仍绑旧三pin，未done；不能沿用 Boss2较早影响报告中的 claimed/Boss2 状态。它明确承接宏范围但尚未接住最终新pin的正式交付。

另外7个有效head在此快照中没有直接successor：

| 有效旧done head | 须处理的关系 | 数学差异与所需处理 |
|---|---|---|
| boss6-mlp-g-scope-repair-b2229510e88b478a | finite-unit-path-to-all-positive-infinity-chain；unit-helper-path-to-fixed-threshold-degree-three | 共同M080d endpoint改版；它们只用未改主证明§4，whole推导不变；新pin审读/重绑并处置旧资产。 |
| boss6-inf-chain-transfer-3b-ea6be0c00b1186cf | 同上两条共享资产 | 与b222共享相同两path，宜同一新path/SHA给两后继收据，不能只刷新一份receipt遗漏另一份。 |
| unrelated-machines-3a-3a-3f8b771c0276b1b2 | gated-value-bridge-to-full-unknown-opt-ratio；gated-general-welfare-proves-robust-two-threshold-decider | 门控/robust端点改版，前者还直接引旧共享审查SHA；whole算法及两种NO均不变，需正式刷新。 |
| unrelated-machines-3a-3a-cf566ee9cd0d2cf8 | xos-rounding-to-gated-menu-welfare | 13/8端点及§一evidence whole-file SHA改版；保局部contribution，不能升级整算法。 |
| boss5-localfix-repair-25d12f7253028f37 | partial-support-versus-welfare-lp | robust端点变；保context。两组19/20私有+1/20共享例仍分离福利L=39/20与support总质量≤1，不能升级指定福利LP的蕴含。 |
| boss2-6405-source-repair-b61b3ed236a4a90b | welfare-to-general-ratio-value-bridge | 两门控端点及§一evidence SHA改版；只付值桥/回填contribution，remaining继续保留。 |
| boss5-474257b8-qd-decoder-3a-69d5a688c474b34c | support.json / b5-qd-and-private-tree-config-force-decoder-parameter-growth | Q_D pin在此次前已过时，此次合并刷新到最终pin。Q_D无零 incidence；保持Q_D与v3的ALL、whole必要参数障碍，不冒称已有编译。 |

macro旧边 `map/edges/unrelated-machines-3a-3a-17669e4ba1771673/normalized-config-bridges-qd-degree-three.json` 此前也已过时；wave9接续须刷新最终三端点和共享源SHA。它只支付CONFIG/row/item度局部链，保ALL及contribution/remaining；不因修句升级为完整actual gap证明。

以上为9条unique相关edge，其中7条在Boss2旧快照为canonical，macro与decoder两条此前已非canonical；本次不把过时边恢复为canonical。7个已被成功done替代的历史done沿有效head处理，不重复发布repair。Boss3现有 `unrelated-machines-3a-3a-a56e5e8b03d8a1fd` 仍claimed/Boss3、仍旧三pin，须owner保稿刷新；它是独立主3A范围，不是这8个旧done的supersession，本报告未支付其primary coverage。

数学可复用与正式交付要分别记：此次所有9条关系未因zero补写需要新推导，但任务definition pins、coverage pins、endpoint/evidence pins、审读追溯和supersession资产处置仍须authorized owner正式完成bind/check/checkpoint/pushed/done并重新assemble。该报告没有执行这些动作。
