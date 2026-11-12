# 21份完整策略锥：一般对偶实例与六人局部福利贡献

本说明由Boss2正式任务customer-attraction-3a-3a-2c3bfa8c793694f1的fresh数学worker编写。仅写本任务边目录与收据；没有修改source、registry、其它任务、Git或原生队列。Root负责后续edge-bind/check、checkpoint与done。本说明是本包support资产，可按准确SHA列入本包收据，不作为其它包可借用的独立canonical边。

## 当前合同与所回答的问题

任务定义pin为9eeed0a4ea7c636789feae17cfb5cbdb1105b93c34de7697e6ac62f060ece935，当前本地owner=Boss2、state=claimed，已追加三个真实只读端点。读取时registry原字节SHA为df18a812d37f7957bc41e04692b2223cba6e84bdb942f3afec673626dd9bdd14；其中edge_files为2296项。完整实读以下四个当前登记合同的model、statement、quantifiers、assumptions、scope、objections、body/evidence：

| 对象 | v / 状态 | 当前pin |
|---|---|---|
| customer-attraction/fractional-and-cone-auditor-contracts | 2 / proved | c11bad6a52fd8dbb38e5a0cb845f9631008b7afe3026360fd709327e69f2debd |
| CA-SECURITY-CONE-DUAL | 3 / proved | e31e80e9d89c7fad56eadbcbfd46a50af3857d6119eea8060c3a41a0cb987899 |
| CA-OBLIVIOUS-MIXED-SECURITY-2N1 | 3 / proved | 565f6bdb541c09f8229f27ca4d47409f946a555f141378e72fb91c5a55082ea4 |
| customer-attraction/six-providers/exact-six-full-history-half-cover | 1 / open | 2d5b191271cb052c435121a41935eb3958540d5a53cb05013f13dd45a70f6e31 |

本核心v2的实际Claim是21份固定完整策略的共同Q全客户锥证书。正文还说明弱实际负载桥与分数覆盖的其它审计合同；它们各有外owner，不因资料标题而进入本21锥数学结论。这里完整读正文和全部核心异议，保留这些外边界，没有声称本轮新运行或重读其它两个审计的每份原码。

本轮回答两个问题：逐query共同Q证书在一般固定查询对偶中到底承担什么证明角色；唯一六人锥能否与同实例静态锐界联合，支付六人原题的一个明确子域。优先采用wave19-static-dual-edge-adjudication.md的显式更正，撤回wave18原建议A的implies/contribution分类；其正确算式仍使用，但按当前target独立判断为checks/context。

## 全历史客户锥与成熟证书的数学含义

记人数n、标签数k，兴趣类型为非空T⊆[k]，质量w_T≥0。n、k不混用。固定σ在所有有序h∈[k]^{<n}上定义行动；z_h为沿同一σ真实完成的终局，z_ha为强制a后沿改变后的有序历史真实续行。定义

    ρ_T(a,z)=1_(a∈T)/#{j:z_j∈T}，零分子项为0；
    Γ_(h,a);T=ρ_T(σ(h),z_h)−ρ_T(a,z_ha)；
    Kσ={w≥0:Γσw≥0}，c_T=1_(T与根叶相交)，Wσ(w)=c·w。

非零分子时该行动已在终局，分母正。每位提供者只在自己的层行动一次，全部历史、全部a的弱收益比较恰给完整纯SPE；同计数不同历史仍可有不同后继。Γ不能被在轨行、冻结惩罚或actual菜单替换。整数w是不同单位客户克隆，有理w可清分母；不是加权玩家或不可分有权客户。空兴趣类型无贡献，可任意补入。

合法静态背景B∈[k]^{n−1}，允许重复及相关，不观察此次query；f_B(a)_T=1_(a∈T)/(1+#{j:B_j∈T})。每份σ保存一份Qσ和每个a的λσ,a≥0，使

    c/n−E_(B∼Qσ)f_B(a)=Γσᵀλσ,a+rσ,a，rσ,a≥0。

量词是对每份指定σ存在Qσ及整组(λa,ra)，对全部query a和全部w∈Kσ同时有效。Q不依w、a或p；λ/r可依a但不依w。21份之间无需相同Q。stored exact_certified不替代真实性与非负检查。

L=lcm(1,…,n)=60（本包n=5或6）。存储整数row为LΓ；读证书必须除60恢复收益差。原检查器先重建每个有序(h,a)的真实行，再按向量完全相等去重。把同一存储行的非负乘子合并到任一真实(h,a)代表，完整矩阵其它位置系数设0，即可把去重证书提升回原Γ；没有减少全历史量词。

与任意w∈Kσ内积得W/n≥E_Qf_B(a)·w。对任意查询分布p平均，min_B Σa p_a f_B(a)·w≤E_QΣa p_a f_B(a)·w≤W/n，再max_p，得到整个指定锥上的W≥n v_n。内积结论对非负实质量成立；有限数目的σ不是有限数目的客户点。

全兴趣类型每条Γ为0，且c/n=E_Qf=1/n，所以余项该坐标为0。报告的min_residual=0不能被说成严格正余量，也不能仅由minimum初始化0推断其它坐标非负。零客户与W=0直接保留，无需归一化或0/0。

## 21份证书的实际输入范围

原gzip共552002字节，解压6153467字节，解压JSON SHA为4272c141c110c130a391d5ba68b9085f29486bddd1351007dfe14a654d14665c。本轮完整解析JSON，实际查看全部21项source元数据、人数/标签、policy行数、沿policy查出的根路径、全部Q及每query λ块长度；下面的λ项数为列表项数，不冒称去重严格正支持。

| case | n/k | 根叶 | Q项 / λ项 |
|---|---|---|---|
| d837bffdf7e0 | 5/7 | 0,2,4,5,6 | 1 / 250 |
| 9715325c6b4e | 5/7 | 0,3,1,4,5 | 1 / 279 |
| 3c29e8f9160e | 5/7 | 0,3,4,1,2 | 1 / 293 |
| 793c98d89ec3 | 5/7 | 0,2,4,5,6 | 1 / 236 |
| 99d0aba203ee | 5/7 | 0,2,4,5,6 | 1 / 234 |
| 9fc41c69705a | 5/7 | 0,2,4,5,6 | 1 / 239 |
| a8decea1172b | 5/7 | 0,2,4,6,6 | 1 / 278 |
| a68fe3cc2c8a | 5/8 | 0,2,4,6,7 | 1 / 599 |
| b352b7fb49fe | 6/8 | 0,1,3,5,6,7 | 1 / 470 |
| 852bd8a5ce8f | 5/7 | 4,6,4,5,5 | 4 / 360 |
| e41f608f31b4 | 5/7 | 4,4,5,5,6 | 7 / 221 |
| 2c10d2a1c309 | 5/7 | 4,4,5,5,6 | 7 / 232 |
| 9c51225d1714 | 5/7 | 1,2,0,0,3 | 3 / 335 |
| 488dcf3496ee | 5/7 | 0,0,1,2,3 | 4 / 122 |
| 62dfde32fb79 | 5/7 | 0,0,1,2,3 | 3 / 231 |
| f29c1cd84101 | 5/7 | 0,1,6,4,5 | 1 / 269 |
| 46eeca17b38d | 5/7 | 0,1,4,5,6 | 1 / 130 |
| e122e07a6445 | 5/7 | 0,1,4,5,6 | 1 / 147 |
| 0d075a940a1a | 5/7 | 1,3,0,2,4 | 7 / 493 |
| 610da75b1409 | 5/7 | 0,1,2,3,4 | 1 / 124 |
| 48bf153929c4 | 5/7 | 0,1,2,3,4 | 1 / 120 |

b352独有n=6、k=8，policy为37449行，Q=δ_(0,0,0,0,0)，λ块长为(0,73,52,81,57,79,68,60)。其余20份为五人（19份k7、一份k8），不能直接支付六人target。

本轮实读原66行检查器：它用完整有序hist集合核policy键恰相等、无重复、动作精确int合法；按同一policy真实续行重建Γ并检查每条λ row的成员资格；Q概率非负归一且为合法n−1整数槽；逐query逐类型用Fraction检查残差非负。没有导入优化器、生成器或solver。既有new-cones-run.json明确绑定源码SHA52e8…与输入SHAa4e8…，普通解释器无-O且optimize0、returncode0、7.257秒；成熟report记录21case、95349历史、709573含自身比较、20971坐标、5662个λ列表项。新旧比较记录除source绝对路径外全字段相同。

这些全Γ成员资格、全部709573比较及20971残差算术沿用已登记原成熟成功审计。本轮没有执行certify_cones、重建全Γ、逐数人工阅读6MB数字、重算余项、跑LP/SPE或生成器。结构解析、根路径查表与证书形式检查不冒充新的科学重放。

## 一般对偶接口：实际是checks/context

CA-SECURITY-CONE-DUAL v3的整条target是任意m,n,完整σ、有理p的(A)⇔(T)、有理证书及无(T)时严格正有理见证提取。其自足正文使用归一切片中全兴趣点保非空紧性、双线性minimax、Farkas锥对偶；严格失败后清分母给完整SPE的aggregate反例，另算OPT>2W才是half反例。

本21锥证书对任意固定有理p满足β_B(p)=Σa p_a f_B(a)，取

    λ(p)=nΣa p_a λa≥0，r(p)=nΣa p_a ra≥0，
    c−nE_Qβ_B(p)=Γσᵀλ(p)+r(p)。

这是每个指定σ、每个p的一份全有理(T)成功实例，Q甚至不依p。它没有承担一般(A)⇒(T)或严格失败提取，也不构造所有σ的证书。故这条边是accepted checks/context，不写whole_result或contribution，不能用它给核心记linked。共同Q是更强充分接口；本轮未证明其必要性，更未从共同Q搜索失败推出固定p证书不存在。

## 同实例ALL联合：六人目标的局部贡献

只选b352b7fb49fe的冻结完整σ和八标签目录。任取Kσ中的非负整数w，将每类型展开为相应数量不同单位客户。完整Γ认证该σ为全部有序历史上的纯SPE，核心直接给Wσ(w)≥6v6(w)。

CA-OBLIVIOUS-MIXED-SECURITY-2N1使用同一客户总体、同一八标签目录、同一五个整数静态竞争槽，证明OPT6≤11v6。其Jensen/期望重数证明允许背景任意相关、标签重复与空覆盖；静态定理本身未支付动态总收益。联合得到

    Wσ(w)≥6v6(w)≥6OPT6(w)/11，
    2Wσ(w)≥12OPT6(w)/11≥OPT6(w)。

两个前提必须保ALL：core支付动态W≥6v，staticsharp支付同实例OPT≤11v。CA-SECURITY-CONE-DUAL不必成为第三个承重前提；core自己的内积证明已足够。

有理w取正整数D清分母，Dw仍在Kσ；W、OPT6、全部静态收益矩阵以及有限max-min值v6同比缩放。先对单位客户Dw用结论再除D；这条边只主张整数/有理点的福利比，不免费升级静态单位客户定理为任意实质量。零客户、OPT6=0直接成立。允许空覆盖、别名、重复行动与全部弱平局，不能合并带标签历史改变σ。

这是一条accepted implies、premises_mode=all、relation_mode=unconditional的局部contribution。固定已认证策略域是所证结果的适用范围，未留下未核乘子或开放C6作为前提。remaining必须保留其它全部六人σ及其它目录规模；原六人全称题仍open。更未证明逐人安全、残余背景利润、iid/自由分数付款或弱/强全局债务。

## 排重、相邻对象及覆盖处置

仅枚举当前registry.edge_files的2296个canonical路径并解析端点ID；没有扫描磁盘所有edge JSON。当前无以本核心为source或target的canonical边。因此两条本任务关系没有现役同core重复可借。

已实读canonical c385的selected-common-q-checks-duality.json全文及review全文，SHA分别为fa9554fb3760152f55036d3042ea125b1bf8eff13f6f82f16fa7276bdc85fd57、92802998810cad2d490e9dd68e0e4dcc165f1d49bccb3a84bd503e63c13ba23c。另读CA-SELECTED-SECURITY-CONES v3完整合同：三人/四人、六标签的三张指定策略有十三份证书、4914坐标；它们与当前五/六人、七/八标签的21张不是同输入或已给嵌入子集，不能互推。c385只覆盖selected三个实例，不能充当本核心canonical覆盖。其checks类型与本次按target证明角色独立所得结论一致。

已实读现役boss6-six-universal-fixed-query-cone-security-and-static-price11-imply-half完整JSON（路径universal-fixed-query-security-to-six-half.json，SHA3d26fb6b6167a692827a5b5a881ccc3c079474fc73d6db5000dc90074799d4d4）。它要求全部目录、全部六人σ、全部有理p的开放C6，属于accepted conditional整条half充分路线。本包支付b352局部域，未支付普遍C6；新边不复制其whole_result。其它canonical仅端点扫描，不称数学全文实读。

核心可记linked，唯一用于linked的逻辑edge_id为boss2-new21-b352-common-q-and-static-sharp-six-half；对偶context另列。task没有声明follow-up overlap，read-added三个端点的实际处置写comparison_dispositions，closed_overlaps与follow_up_tasks保持空。一般数学开放义务保留在remaining，不写needs-decision，不凭目录相近再派无必要任务。

## 实读与继承账本

下表“全文”为本worker实际文本阅读；registry仅四个端点与selected的完整合同、其余对象未冒称全文。外部只读子worker也独立核staticsharp、six target、共同模型及b352结构，结论一致；主worker已自行全文读同三份核心数学正文。wave18/19为先前准备的明确继承来源，不是本轮新证书审计记录。wave18旧建议A以wave19更正为准。

| 相对clone路径 | SHA-256 | 本轮实际范围 |
|---|---|---|
| AGENTS.md | 20293db840f907c32f774b0d7f72450c56e6c0ad937720699d14f7c02e693cc9 | 全文 |
| research/IMPLEMENTATION.md | fb6613cd0c429f28b8bcfb1064076a629540cfbee8f7e3d670b0b39e78ff0d4b | 全文分段；重点ALL、contribution、收据和共享canonical规则 |
| prompts/03-map-worker.md | 6629f71923c54d994297d54c3737b285227b72c463641d318c3f61c9342d07b2 | 全文 |
| research/operations/map-v2/tasks/customer-attraction-3a-3a-2c3bfa8c793694f1.json | 83cf1f7fef9625ff26645f61c8bc75c722594a9f9589e9cbc84ae8612314be80 | 完整定义、三个read-add端点及本地owner/state |
| research/registry.json | df18a812d37f7957bc41e04692b2223cba6e84bdb942f3afec673626dd9bdd14 | 指定完整合同；canonical列表内端点扫描 |
| archives/customer-attraction/state/资料/客户分数负载覆盖与固定策略锥的审计合同--资料.md | 0013a2a0986eb81e11735bc2a794e47e5f650cad43c173817a02a14f01ddb3aa | 全文，含21锥、其它审计及可扩大边界 |
| tools/evidence/collaboration-model-and-cag-audit-primary/related-cones/760834c0f64c80b5ccc1 | a4e84d0478ba0ededabe547870ad0a4916cd05a78e686183ed6ef1b660583045 | 原字节/完整JSON解析；21元数据、Q、λ块及根；b352示例row；无Γ/残差重放 |
| tools/evidence/collaboration-model-and-cag-audit-primary/original/3e153d43f71d6ebd66e6/tests/audits/customer_attraction_new_security_cones.py | 52e8f2a93db13ed523014119c52d7d82333092eb1d084668481b26c0a38693c9 | 全66行源码 |
| tools/evidence/collaboration-model-and-cag-audit-primary/runs/new-cones-report.json | cfaf3ac6bda723bccca5ff0da40d1778b3be1a67b5ba9fc88f6741154ed4ea7d | 全文21结果；继承成熟全矩阵审计 |
| tools/evidence/collaboration-model-and-cag-audit-primary/runs/new-cones-run.json | 0f80fd4788d7a4eb4e4b1f4d8b677b5dd3f1f4ee4db1b7931b693e0f9cd8ac88 | 全文原命令、returncode与source/input绑定 |
| tools/evidence/collaboration-model-and-cag-audit-primary/new-old-cones-comparison.json | d6a1dcb2a4340fa9ef584f174b1f47a73dc383de3f28ea934ccb83528556d634 | 全文 |
| archives/customer-attraction/state/审查/五人半覆盖上传证书与个体安全运输尾部五源接续审查--审查.md | 21243ef4cd7288e4e305dae1d3868a77da9ea67e73333619d03b438b246f020a | 精确第5节含5.1/5.2，至第6节前 |
| archives/customer-attraction/state/审查/新策略安全锥与半顶点候选增量审计--审查.md | f1ead3c45e5ee9e75cbe097a334ca7dfd7aa9f94e2cea76414d515572f0b604f | 全文，分清21精确锥与20浮点候选 |
| archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md | cc4a9dadb09e08b072cb63214d2e084db38db219e4100efbccf9b7f497520e88 | 全文 |
| archives/customer-attraction/state/定理/完整策略锥的静态安全值对偶--定理.md | b279e1f63f08b961365a2cbc0173530de7090fd1c7beefc1a42c585ef6e58cf5 | 全文，双向证明、严格失败提取与附加不同覆盖合同 |
| archives/customer-attraction/state/定理/静态混合安全值的锐目录计数界--定理.md | 034c940129b4ef2e1b5a2902f9256f9dbfed5fbc8bf6750c4403217db3a6b15f | 全文一般证明与相邻值边界 |
| archives/customer-attraction/subarchives/six-providers/state/问题/六人完整历史半覆盖目标--问题.md | 0626668e7a825108fc0b3699e42394b75b1c2e2a526df220a90d91a02afc8a0c | 全文 |
| archives/customer-attraction/subarchives/six-providers/问题--问题.md | 21391fbaaa2893fef7b228a345fcf1d7f5c5d1dc8a42cc642d6bfbbeccc7c065 | 全文同数学旧根页 |
| research/workspaces/map-v2/Boss2/recovery-20261112-e8cf4c/wave18-static-dual-3d-review.md | c3ad54acdc9ec3ca779ebfb281795fe8ab0bfbbca2f9aecd2c724099c2f3e054 | 数学第1–9节及读取账本定位；旧A已更正，不继承其错误类型 |
| research/workspaces/map-v2/Boss2/recovery-20261112-e8cf4c/wave19-static-dual-edge-adjudication.md | bbf4c96cc836fa7148e856a911fc66ca3d86569419dbd5e76a53473417b0e718 | 全文更正与B路线；重新按当前target实读复核 |

未声称新读wave18账本所列每份外source、原生成器412行或其它selected原数字矩阵。它们不承担本包新推导；本包承重证据以表列原21证书、66行审计、成熟绑定run、两自足定理正文及模型/target为准。没有发现需要改source的新勘误，也无新的身份、路由或缺附件阻碍。
