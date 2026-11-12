# Wave19：21固定锥到一般对偶的边类型更正与六人局部贡献裁定

这是Wave18原准备的批内定向反馈，只更正边类型与后续最小read-add；不是新的扫描、正式claim、coverage或done。本轮只写本scratch文件，不修改已发表W/wave18-static-dual-3d-review.md、原scratch报告、仓库、Git、native、queue、source或其它全局状态，没有运行LP/SPE/成熟证书矩阵审计。

## 1. 明确更正：撤回原建议A的逻辑边类型，保留其算式

原报告第8节“建议关系A”原建议：

    customer-attraction/fractional-and-cone-auditor-contracts
        -> CA-SECURITY-CONE-DUAL
    kind=implies, relation_mode=unconditional, accepted, contribution。

此分类不准确，应撤回，改为：

    source_ids=[customer-attraction/fractional-and-cone-auditor-contracts]
    target_ids=[CA-SECURITY-CONE-DUAL]
    kind=checks
    status=accepted
    premises_mode=all
    relation_mode=context

语义是“21份固定完整策略的共同Q证书给一般固定查询锥对偶接口的具体输入实例”；不是一般等价定理的逻辑支持，不写contribution来掩盖一般定理证明仍由target自己的正文承担，也不写whole_result声称得到整条对偶定理。

原从逐query证书构造固定p的(T)解的算式仍正确。更正的是将应用实例当成一般证明的contribution这一关系建议，而非撤回21锥证书或其全锥安全不等式。原报告第3节的证书量词、内积soundness、第5节的单位/有理福利用途不受此更正影响。

原建议B——ALL{21cones, staticsharp}到六人原题的固定b352六人6/11局部结论——仍可作为accepted逻辑contribution，详见第5节。两条不能沿用同一种边类型。

## 2. 先按当前target判断，而非以同行决定替代数学判断

已重新完整实读CA-SECURITY-CONE-DUAL v3的完整当前登记合同及自足正文。target statement的实际内容是：任意有限目录大小m、任意n、固定完整有序形式sigma及有理p，下面(A)与(T)等价；证书可取有理；(T)不存在时能以精确有理LP得到严格正见证并清分母，形成单位客户完整SPE的aggregate反例。

    (A) 对全部w in K_sigma：c dot w >= n min_B beta_B(p) dot w。
    (T) 存在合法Q、lambda,r>=0，使
        c-n E_Q beta_B(p)=Gamma_sigma^T lambda+r。

其中K_sigma={w>=0:Gamma_sigma w>=0}保全部真实有序历史IC；B是全部合法n-1静态槽，不能限成actual回复菜单；Q可依sigma,p，不能依w或本次query抽样变化。

该target证明有三项承重内容：

1. 一般(T)推出(A)：与锥中w内积，使用lambda,r非负。
2. 一般(A)推出(T)：sum w=1切片含全兴趣客户点，非空紧凸；双线性minimax交换，再用有限多面体锥Farkas及有理可行系统。
3. 严格失败提取：没有(T)时得到严格违反(A)的有理质量与完整Gamma可行点，清分母保sigma所有真实IC；还须另算OPT>2W才是half反例。

21份显式成功(T)输入没有承担第2项的minimax/Farkas证明，也没有给第3项的无证书分离/严格失败提取。对第1项，它们是已经符合非负恒等式条件的具体应用；其内积检查可以展示该接口如何使用，但不是一般任意sigma,p命题的新增承重前提。

可以准确说这些指定输入同时满足A、T，或验证一般接口在这些输入上的实现；不能把“找到有限个T解”说成“一般A当且仅当T及严格失败提取的证明贡献”。若把它改写成仅21个输入上的真值等价，仍只是成功实例，未给一般必要性/失败机制增加证明内容。数学上可复用的实际作用是checks/context。

原报告引用一条恒A实例contribution作为形式先例，不足以支持本条分类。边必须按当前target statement与这次实际承重作用判断，已有其它边的格式不替代这个判断。本次不扩展为重审或修改恒A边。

## 3. 原21证书到(T)的映射仍严格成立

本核心v2的21份固定sigma分别为19份n5/k7、一份n5/k8、一份n6/k8；每份固定全部有序history policy，再在所有w>=0且完整Gamma w>=0的锥上变化客户质量。合法Q是n-1整数静态槽的概率分布，可重复/相关且不观察本次query。

对每份sigma，证书保存同一个Q_sigma及每query a的lambda_sigma,a、r_sigma,a>=0，使逐非空类型成立：

    c/n-E_{B~Q_sigma} f_B(a)
       =Gamma_sigma^T lambda_sigma,a+r_sigma,a。

量词是：

    对每份sigma in 固定21集合，存在Q_sigma及整组(lambda_sigma,a,r_sigma,a)_a，
    对所有query a和所有w in K_sigma，同一份证书有效。

Q_sigma既不依w，也不依a/p；不是21份之间共用同一Q。lambda/r可依a而仍不依w。L Gamma存储行用L=lcm(1,...,n)=60恢复真实Gamma；去重行可选真实有序(h,a)代表、合并乘子并把其余行系数设0，从而合法提升回完整Gamma。

对任意固定有理p，beta_B(p)=sum_a p_a f_B(a)。因此

    c-n E_Q beta_B(p)
      =Gamma_sigma^T [n sum_a p_a lambda_sigma,a]
         +[n sum_a p_a r_sigma,a]。

所以可取lambda(p)=n sum_a p_a lambda_sigma,a、r(p)=n sum_a p_a r_sigma,a。它们全有理且非负，同一Q_sigma甚至不依p。这个精确映射就是新checks边应保存的解释。

与任意w内积再对query加权、用min_B不大于Q平均、最后max_p，仍得到该固定锥全部非负实质量的W_sigma(w)>=n v_n(w)。这条core自身结论没有被更正。空兴趣类型无贡献；别名、空覆盖、重复动作、零客户和弱平局仍保留。没有将一般安全定理的存在量词扩大为21以外。

## 4. 同行c385边的核对与21锥/selected三锥区别

已完整读当前c385的selected-common-q-checks-duality.json及review全文。其现有kind=checks、relation_mode=context，解释从aggregate逐query恒等式平均得到固定p的(T)解，并明确“不证明通用(A)⇔(T)或普遍证书存在”。这与上面独立按target证明角色所得裁定一致；不是因为peer如此标注才接受该分类。

CA-SELECTED-SECURITY-CONES v3是三张另有身份的策略：原三人六标签034、四人六标签root-tax 0005与global-decorrelation 2500，十三份逐人/aggregate证书合计4914坐标。当前21cones是五/六人、七/八标签的指定完整策略，20971坐标。二者不是同一输入，也不是把三张拆成21张；不同人数/标签域/Gamma/根叶下，没有已给的策略嵌入或客户映射可互相包含或推出。不能将selected原JSON、逐人结论或c385的绑定替换成21证书证明。

本次只把c385用作明确已读的同接口比较材料。其当前是否在data['edge_files']，依第7节同一快照结果报告；磁盘有accepted/bound JSON或Root说明已发表，都不自动等于本地canonical清单已整合。即使它已canonical，也只覆盖selected三个输入，不覆盖本21核心，不能直接作为本核心coverage的既有逻辑边。

## 5. 建议B为何仍是真实ALL推导，而非仅语境检查

建议B的target是六人原题customer-attraction/six-providers/exact-six-full-history-half-cover：对所有单位客户、任意非空共同标签目录、每份六人完整SPE，是否2W>=OPT6。这里确实有一个可由两个已登记结果联合推出的目标域内子结论，而非将一般证明方法的几个成功输入当方法本身的证明。

从21cones中只选唯一n6/k8 case b352b7fb49fe，保其冻结完整sigma。root=(0,1,3,5,6,7)，37449有序决策history，Q=delta_(0,0,0,0,0)，lambda分块长度(0,73,52,81,57,79,68,60)，L=60。该case已由原成熟证书给整个K_sigma上的W>=6v6。

令w为该K_sigma中的非负整数客户重数。它是原单位客户实例，完整Gamma保证同一sigma为完整纯SPE。CA-OBLIVIOUS-MIXED-SECURITY-2N1在同一客户总体、同一八标签目录及同一五整数静态槽安全值上给

    OPT6<=11v6。

联合得到

    W_sigma>=6v6>=6OPT6/11，因而2W_sigma>=12OPT6/11>=OPT6。

对有理w取正整数D清分母，先对单位客户Dw用该结论，再利用W、OPT和有限安全博弈价值的同倍缩放除回；不需要将单位客户静态定理免费推广到任意实质量。此反馈页只为B主张单位/有理输入，不主张全real-cone的OPT比。OPT6=0及零客户直接成立，不作0/0。

ALL必须同时保留：21cones付该固定sigma的动态总收益，staticsharp付同一实例的静态OPT比较。只用前者没有OPT数额，只用后者没有真实SPE总收益。二者对齐后产生本次实际可复用的新福利子结论，所以它是目标half命题在给定完整策略子域上的accepted逻辑contribution。

建议字段：

    kind=implies；status=accepted；premises_mode=all；relation_mode=unconditional。
    source_ids=[customer-attraction/fractional-and-cone-auditor-contracts,
                CA-OBLIVIOUS-MIXED-SECURITY-2N1]。
    target_ids=[customer-attraction/six-providers/exact-six-full-history-half-cover]。
    contribution.result：仅b352b7fb49fe的n6/k8完整客户锥，全部单位客户点及有理克隆点，
                         W>=6OPT6/11，故2W>=OPT6。
    contribution.remaining：全部其它六人完整sigma、其它目录大小仍需证明；
                            原六人全称目标仍open，不能由此支付普遍C6。

这里的域限制应写在conditions/scope/result中；它是所证结论的适用范围，不是尚未支付的开放数学前提。故可unconditional并使用contribution，不能用whole_result指向整条六人原题。若正式writer另采用conditional措辞，也必须明确条件只是哪一固定已认证策略域，不能令读者误以为还有未核的lambda或普遍C6。

原21中的二十份五人策略与staticsharp同理有5/9局部福利界，但不往六人target硬接；本次无需为它们新增无关端点。也不需要CA-SECURITY-CONE-DUAL成为B的第三个数学前提：core证书的内积结论已经直接给W>=6v6，一般等价定理可作解释背景而非重复ALL前提。

## 6. 正式最小read-add与coverage边界

原task当前仍只声明21cones核心、read_object_ids=[]。正式worker如同时采用A与B，最小新增共享读取端点仍是三项：

1. CA-SECURITY-CONE-DUAL：A的checks/context目标，核固定p的(A)⇔(T)及实际应用角色。
2. CA-OBLIVIOUS-MIXED-SECURITY-2N1：B的联合逻辑前提，核同实例OPT6<=11v6。
3. customer-attraction/six-providers/exact-six-full-history-half-cover：B的局部贡献目标，核限制与remaining。

只做A时新增dual即可；只做B时新增staticsharp与six-target即可。CAG-MODEL必要定义已在core/dual证据中，正式worker须实读，但不必为它造hub；若接口要求可作为额外共享read。CA-SELECTED不是A/B逻辑前提或新边端点，不在最小read-add中。c385只是解释比较，不因为目录邻近再开selected与21互推任务。

仅有A时，不应凭checks/context把core记linked；可在实读比较后用isolated-after-review并单列context边。若B正式完成、绑定并验证，其真实accepted contribution可支持core的相应linked记录，仍须明确范围及六人原题open。本页本身不做任何coverage结论或原生状态变更。

## 7. 当前快照、字节与复核范围

本次定向重新读当前五对象完整合同（core、dual、staticsharp、six-target、selected），完整重读dual、core body、staticsharp和六人目标正文，以及c385边/review。原21输入仍按Wave18原读范围复用成熟证据；本次只再次解压原gzip定位b352的完整元数据、Q与lambda分块长度，没有重建Gamma、重算余项或启动大审计。原task完整当前定义/本地状态也已再读。

原scratch报告保持原SHA；Root已发表副本的状态由Root提供，本轮未修改也未重新查找其副本。读取期间registry因Root并发整合从57f40e...2271推进到其它快照；下面表格及pins均取同一次read_bytes解析的最终可见快照，不将多次读取混成同一个版本。正式worker应重新核当时实际task pins，而非将本页快照假装永久当前。

最终登记快照SHA-256：df18a812d37f7957bc41e04692b2223cba6e84bdb942f3afec673626dd9bdd14；data[edge_files]文件数：2296。

c385指定路径在本快照canonical清单中：True。本页未使用它宣称21核心已有canonical覆盖。

原scratch报告SHA-256（未改）：c3ad54acdc9ec3ca779ebfb281795fe8ab0bfbbca2f9aecd2c724099c2f3e054。

| object_id | version / status | 当前pin |
|---|---|---|
| customer-attraction/fractional-and-cone-auditor-contracts | 2 / proved | c11bad6a52fd8dbb38e5a0cb845f9631008b7afe3026360fd709327e69f2debd |
| CA-SECURITY-CONE-DUAL | 3 / proved | e31e80e9d89c7fad56eadbcbfd46a50af3857d6119eea8060c3a41a0cb987899 |
| CA-OBLIVIOUS-MIXED-SECURITY-2N1 | 3 / proved | 565f6bdb541c09f8229f27ca4d47409f946a555f141378e72fb91c5a55082ea4 |
| customer-attraction/six-providers/exact-six-full-history-half-cover | 1 / open | 2d5b191271cb052c435121a41935eb3958540d5a53cb05013f13dd45a70f6e31 |
| CA-SELECTED-SECURITY-CONES | 3 / proved | cbd09a113694b6c6373fd55496413e4575d304f71705e9f380ce134ce282b3b0 |

| 实读文件（相对clone） | SHA-256 | 本次范围 |
|---|---|---|
| research/operations/map-v2/tasks/customer-attraction-3a-3a-2c3bfa8c793694f1.json | 4e82f43dc1c4ba8f32c31106946f2603c15bfb3d2b375c7714c99b1ac60159f6 | 完整定义/状态 |
| archives/customer-attraction/state/定理/完整策略锥的静态安全值对偶--定理.md | b279e1f63f08b961365a2cbc0173530de7090fd1c7beefc1a42c585ef6e58cf5 | 全文重新读 |
| archives/customer-attraction/state/资料/客户分数负载覆盖与固定策略锥的审计合同--资料.md | 0013a2a0986eb81e11735bc2a794e47e5f650cad43c173817a02a14f01ddb3aa | 全文重新读；承重21锥节重点 |
| archives/customer-attraction/state/定理/静态混合安全值的锐目录计数界--定理.md | 034c940129b4ef2e1b5a2902f9256f9dbfed5fbc8bf6750c4403217db3a6b15f | 全文重新读 |
| archives/customer-attraction/subarchives/six-providers/state/问题/六人完整历史半覆盖目标--问题.md | 0626668e7a825108fc0b3699e42394b75b1c2e2a526df220a90d91a02afc8a0c | 全文重新读 |
| map/edges/customer-attraction-3a-3a-c385b158f346250d/selected-common-q-checks-duality.json | fa9554fb3760152f55036d3042ea125b1bf8eff13f6f82f16fa7276bdc85fd57 | 完整JSON；只比较，不当canonical权威 |
| map/edges/customer-attraction-3a-3a-c385b158f346250d/review.md | 92802998810cad2d490e9dd68e0e4dcc165f1d49bccb3a84bd503e63c13ba23c | 全文；重点指定策略证书与通用对偶的实际关系 |
| tools/evidence/collaboration-model-and-cag-audit-primary/related-cones/760834c0f64c80b5ccc1 | a4e84d0478ba0ededabe547870ad0a4916cd05a78e686183ed6ef1b660583045 | 原字节/JSON解析；仅b352元数据/Q/lambda分块，本次无完整Gamma/余项复算 |

此次未执行正式read-add、edge-bind/check、checkpoint或done。已发表Wave18报告中关系A的implies/contribution建议以本页更正为checks/context；其证书算式及B的固定六人局部推导保留。
