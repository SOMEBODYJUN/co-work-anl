# Wave18：21份固定完整策略锥的共同静态安全对偶——独立数学准备

本文件是Boss2 fresh独立准备备忘录，只供Root在gate后决定正式任务的read-add与构图；不是claim、正式coverage、native验证、队列交付或done。此次只写本scratch文件；没有仓库文件、source、registry、canonical、Git、native、queue或全局状态写入，没有重跑成熟LP、完整SPE或证书矩阵审计。仓库路径为 /workspace/scratch/e8cf4ce833a5/co-work-anl-boss2。以下状态是所见本地字节快照，不声称已独立确认远端归属。

## 1. 结论与身份

核心是当前已登记的 customer-attraction/fractional-and-cone-auditor-contracts v2，标题“21份固定完整策略锥的共同静态安全对偶证书”，kind=certificate-theorem，truth_status=proved。其证明含义准确：21份完整形式策略分别固定后，对每份策略的全部非负客户质量IC锥，一份不观察query的合法静态竞争分布同时封顶所有query，得到 W_sigma(w) >= n v_n(w)。这既超过“21个客户点PASS”，又严格小于“任意完整策略的聚合安全定理”。

对应原任务 customer-attraction-3a-3a-2c3bfa8c793694f1 的完整JSON已读；本地state=available、owner=null；object_ids只有该核心，read_object_ids为空，没有overlap_comparisons或具名follow-up。task input_pin与当前record pin相同：c11bad6a52fd8dbb38e5a0cb845f9631008b7afe3026360fd709327e69f2debd。没有据此执行claim，也不把本地available视为远端可领取授权。

主要实读比较端点是 CA-SECURITY-CONE-DUAL（固定查询的精确锥对偶）、CA-OBLIVIOUS-MIXED-SECURITY-2N1（真正静态安全值的锐目录计数界）及六人原题 customer-attraction/six-providers/exact-six-full-history-half-cover。它们确实有承重关系；无须为同目录或共享模型补hub。

## 2. 精确数学对象与全部有序偏离

记标签目录为[k]、人数为n；本包只有19份(n,k)=(5,7)、1份(5,8)、1份(6,8)。每份sigma在所有 h in [k]^{<n} 定义行动，而不是只在实际路径、计数状态或指定惩罚菜单定义行动。

每个非空兴趣类型 T subset [k] 的质量为 w_T>=0。整数w_T表示该类不同单位客户数；有理w清共同分母还原不同单位客户；它不是玩家权重，也不是单个不可分重客户。类型T=empty对所有收益和覆盖为零，可以另加任意质量而不改结论。

在有序历史h处，z_h表示沿sigma真实完成的终局，z_ha表示先强制a、再沿同一sigma在改变后的有序历史完成的终局。当前行动者的类型份额是

    rho_T(a,z) = 1_{a in T} / #{j : z_j in T}.
    Gamma_{h,a;T} = rho_T(sigma(h),z_h) - rho_T(a,z_ha).
    K_sigma = {w>=0 : Gamma_sigma w>=0}.

零分子时份额定义为0；非零分子时终局含当前行动，所以分母正。全部h、a都保留，含自身比较与离轨节点。每人仅在自己的层行动一次，故这些全部真实一处偏离比较恰刻画该完整策略在每个子局的最佳回应；K_sigma恰为sigma成为完整纯SPE的客户质量锥。不能把相同计数的两个历史合并成同一续局。

根覆盖行 c_T = 1_{T与z_empty相交}，于是 W_sigma(w)=c dot w。n为提供者数，不是标签数；审计源码将topics临时记m，不能与其它正文的m人数约定混写。

L=lcm(1,...,n)，本包n=5、6均L=60。源码从所有真实有序h、a重建L Gamma，再去重完全相等的行；重复约束去重不丢条件，零行也无额外约束。存储lambda中的row是完整的L Gamma整数向量；使用时必须除以L，不能将raw整数行当作未缩放收益差。每项row须属于本sigma从全树重建的行集，非负系数不能乘一个没有真实历史来源的任意向量。 如需对齐未去重的完整Gamma索引，为每个存储行任选一个实际(h,a)代表并将该行全部系数合并到代表上；其余完整行乘子取0，即得到原全矩阵上的合法非负乘子。因此去重不改变这里的证书合法性。

## 3. 共同证书的合法性、量词顺序和证明

合法静态竞争元组 B in [k]^{n-1} 长度恰n-1，允许重复标签；其收益系数为

    f_B(a)_T = 1_{a in T}/(1+#{j : B_j in T}).

Q是这些元组上的概率分布，Q_B>=0、sum Q_B=1。它可以相关，也不必来自sigma的任何actual菜单；但不能观察本次query抽出的a再选背景。每份策略存一份Q_sigma，且每个query a存非负乘子lambda_sigma,a和逐类型非负余项r_sigma,a，使

    c/n - E_{B~Q_sigma} f_B(a) = Gamma_sigma^T lambda_sigma,a + r_sigma,a,
    lambda_sigma,a>=0, r_sigma,a>=0.

正确的量词顺序是：

    对每份 sigma in 该固定21份集合，
    存在 Q_sigma 及整组 (lambda_sigma,a,r_sigma,a)_{a in[k]}，
    对每个query a、对每个w in K_sigma，以上同一份证书均适用。

Q_sigma不依w、不依a或查询分布p；lambda/r可以依a但同样不随w变化。“共同”是每份sigma内部跨全部query和整个客户锥共同，不是21份策略之间共用一个Q。原件中既有delta_(0,...,0)，也有三项、四项、七项Q，已直接读取全部21份Q。

与任意w in K_sigma内积，得到

    W_sigma(w)/n - E_Q f_B(a) dot w
      = lambda_sigma,a^T Gamma_sigma w + r_sigma,a dot w >=0.

对任意（可为实数概率）查询混合p加权，因同一Q可跨a使用，

    min_B E_{a~p} f_B(a) dot w
      <= E_{B~Q_sigma} E_{a~p} f_B(a) dot w
      <= W_sigma(w)/n.

再max_p得到 W_sigma(w)>=n v_n(w)。这里不需要证明Q为最优对手、不需要假设它是顺序混合SPE，也不需要先知道哪个查询是安全最优。该内积证明直接对任意非负实质量成立；有理质量的单位客户还原另由清分母给出。

与 CA-SECURITY-CONE-DUAL 的精确对应也可显式给出。对任意固定有理p，取同一Q_sigma，令

    lambda(p)=n sum_a p_a lambda_sigma,a,
    r(p)=n sum_a p_a r_sigma,a.

则 c-n E_Q beta_B(p)=Gamma^T lambda(p)+r(p)，正是该定理(T)。因此本包对21份sigma逐份给出全部有理p的显式(T)实例，而且Q甚至不依p。一般定理只要求固定sigma、p后有Q_(sigma,p)，允许其依p；本包的同一Q接口更强。没有证明“每个固定锥上W>=nv”必等价于“存在一份跨所有p的共同Q”，也不能从共同Q搜索失败推出固定p证书失败或aggregate反例。

## 4. 归一化、有理克隆、别名与边界

本证书齐次，无sum w=1、W=1或正福利归一化前提。W=0及w=0都在范围内，直接得到v=0，不作0/0。一般对偶定理证明反向时采用sum w=1，是为了在紧凸多面体上minimax；全兴趣类型质量1使该切片对任何形式sigma均非空。这不把本有限证书结论限制到总质量1，也不等于其它发现程序的W=1切片。

若w为非负有理向量，取正整数D清全部分母，Dw为非负整数，所有真实IC和福利/静态支付同比例缩放，sigma不变；由同一完整动作表获得单位客户完整SPE。不得为了“归一化”删掉全兴趣类型或要求正余量。全兴趣类型的每条Gamma为0、c/n=E_Q f=1/n，所以该坐标残差必为0。本报告中的min_residual=0不表示严格正余量，更不意味着数值最小值初始化0即可独立证明所有残差非负。

允许空覆盖、不同标签同覆盖、重复动作、零客户与所有离轨弱平局。w的某些坐标为0时，标签可变成空覆盖或别名；sigma仍定义在原带标签有序历史上。不能自动合并别名历史或删除空标签后沿用原策略身份。非严格Gamma w>=0保所有平局，不强加生成器的root_min/root_max/seed选择规则为一般策略限制。

本包是零过去背景根福利结论。非零合法前缀下，剩余利润通常不等于覆盖；不能直接将c/n和W搬成残余玩家总利润的证书。

## 5. 实际福利用途：只给定策略锥，不升级六人原题

CA-OBLIVIOUS-MIXED-SECURITY-2N1已经证明同一单位客户实例、同一目录的真正静态值满足 v_n>=OPT_n/(2n-1)。与本核心联合，在本21份策略各自的整数客户锥上得到

    W_sigma >= n v_n >= n OPT_n/(2n-1).

因此20份五人策略锥给 W>=5OPT5/9；唯一六人case b352b7fb49fe 给 W>=6OPT6/11，从而2W>=OPT6。有理质量先清分母成单位客户，应用静态定理，再同比例除回即可。这些福利推论在本备忘录只主张单位客户及有理克隆输入；不免费扩大静态单位客户定理为任意实质量版。若Root另要写全real-cone OPT比，应另明确使用有限有理多面体的有理点稠密性及有限静态博弈价值/OPT的连续性，或独立写加权Jensen同线性证明；本次没有把该延拓当免费已登记前提。

该唯一六人case有k=8，root=(0,1,3,5,6,7)，37449有序决策历史，299592含自身行动比较，18613去重Gamma行，2040客户坐标恒等式，Q=delta_(0,0,0,0,0)，lambda列表项合计470。它的整个K_sigma支持上述单位/有理客户福利保证；不是只一个seed的n6点。也不是全部六人八标签策略，更不涵盖任意标签数的所有六人完整SPE。

不得从此得到每位u_i>=v_n、任意两位成对付款、任意残余背景安全值、弱/强全局债务界、某指定GB推送规则、iid或自由分数安全付款。它只支付根总福利W。聚合安全桥即使有真正反例也不自动是half反例；仍需另算OPT>2W。

## 6. 成熟证据的实际复用与本次读取界限

核心完整body、66行独立Fraction审计源码、412行新报告、完整增量审查，以及五源接续审查的精确第5节已实读。552002B gzip已从原路径读入并解压为6153467B JSON：检查根结构、21个case的全部source元数据、players/topics、policy长度、第一/末项动作、certificate键、全部21份Q、每query lambda长度及全部row向量宽度；精确数字原件未修改。解析遍历不是人工逐字读6MB数字，也不是本次重新建立全部Gamma/复核20971余项。没有导入或执行audit certify_cones，没有重跑生成器、LP、SPE或完整证书矩阵。

成熟报告绑定的审计代码SHA52e8...与输入SHAa4e8...已逐字节核同；run_metadata是普通未优化解释器（optimize0、无-O）的既有一次真实运行，returncode0、7.257秒。源码assert负责合法policy的全部有序历史键、action精确int/范围、Q概率非负归一/合法n-1槽、每query lambda长度、row真实行集成员、lambda非负和全部逐类型Fraction residual>=0。stored exact_certified/Gamma_scale标签本身不足以代替这些检查。旧新报告除source绝对路径外全字段相等；不能回填旧报告为当时已有代码SHA绑定。

既有成熟总计为21case、95349有序历史、709573含自身比较、20971恒等式、5662个lambda列表项。这里复用其数学与运行证据，不把列表项计数当去重正支持，也不说本次重算了这些矩阵。

仅为核一个真实归一化疑点，本次做一项短Fraction算术：e41f608f31b4的七项Q混用分母513432893与1026865786。前五项分子和464175520，后两项合计49257373/513432893，故总和(464175520+49257373)/513432893=1；脚本精确输出1。这不充当其余lambda/IC审计。

辅助实读的共同背景报告说明另一个n4/k6锥的Q=(3/4,1/4)有理恢复成立，但其n5报告的保存十进制未精确归一/有负余项，仍为候选。它不能作为本21份证书的证据替身。旧security-cone-contracts程序合同的21锥一句与当前有限锥结论一致，但其86客户逐人反例/浮点诊断属于其它对象；本核心不检查那些结论。

## 7. Canonical去重结果及可复用边

只枚举当前data['edge_files']中的2285个canonical文件来查端点；没有把磁盘上的任意JSON或旧receipt视作canonical。runtime.load按(data,objects_dict)解包，用verify=False读取当前登记合同，随后对本次所需原件直接核SHA；没有声称完成全仓验证。

当前canonical没有以本核心为source或target的incident边，因此没有可直接共享复用来记该核心linked的既有逻辑边。以下三条已完整读JSON，并核仍在canonical清单：

1. boss6-six-universal-fixed-query-cone-security-and-static-price11-imply-half：{CA-SECURITY-CONE-DUAL, CA-OBLIVIOUS-MIXED-SECURITY-2N1} ALL -> 六人原题，accepted/conditional。它保额外开放C6：所有目录大小、所有六人形式sigma、所有有理p均存在全锥证书。可复用其同实例11v6与强付款推导及量词边界，不能用本包一个n6 sigma当作C6已付，也不能把此边列作本core自身coverage证据。
2. boss6-384393-constant-policy-explicit-security-dual-certificate：恒A策略对象 -> CA-SECURITY-CONE-DUAL，accepted/unconditional且contribution，给任意人数恒A子族的显式Q/乘子。它是正确的局部实例交付形式先例；本21份非恒定策略不由该恒A子族定理推出，不能把两个对象同化。
3. cag-009e-fractional-static-bound-to-conditional-full-cover：分数覆盖静态下界 -> M-5c61b8e33f844e8498ea4d5865b1f7bd，accepted/conditional。完整源已读；可复用整数W取整与严格阈值的条件推论。本21锥可支付其强桥的有限策略输入，但本次不推荐为此再造一条高重复、低新增量边；普通分数覆盖预算/弱实际负载反例仍沿外owner。

三条精确路径与SHA在下方ledger。未读的其它canonical文件仅作端点ID扫描，不冒称逐边数学复审。

## 8. Gate后精确read-add建议与待比较问题

正式接续若采用下面两条关系，至少read-add这三个稳定ID；本次没有执行read-add：

- CA-SECURITY-CONE-DUAL（v3）：比较固定p的(T)与本每query共同Q恒等式，核lambda(p)=n sum p_a lambda_a、r(p)=n sum p_a r_a，确定只给21份全p实例，不声称证明一般等价或普遍证书存在。
- CA-OBLIVIOUS-MIXED-SECURITY-2N1（v3）：同一单位客户目录、同一n-1整数槽安全值，核W>=nv与OPT<=(2n-1)v联合；不替换为自由分数、iid、真实菜单或额外一槽值。
- customer-attraction/six-providers/exact-six-full-history-half-cover（v1）：只将b352b7fb49fe、k8、n6固定完整策略客户锥的单位/有理克隆结果接作局部贡献；remaining保全部其它六人策略及任意目录大小。

CAG-MODEL是必要定义，已经作为body/evidence完整实读；若工具要求共享读取登记可read-add其稳定ID CAG-MODEL，但不为定义本身制造逻辑hub。frontmatter中的customer-attraction/full-strategy-cone-security-duality与customer-attraction/common-catalog-full-history-model不是本快照的现役object_id；应分别使用CA-SECURITY-CONE-DUAL与CAG-MODEL，不补重复身份。

建议关系A：本核心 -> CA-SECURITY-CONE-DUAL，kind=implies、premises_mode=all、relation_mode=unconditional、accepted、明确contribution。result为“21份指定sigma，对每个有理p存在上述全有理(T)，同一Q_sigma甚至独立于p、w”。remaining为“一般任意sigma固定p双向等价仍由目标原minimax/Farkas证明承担；普遍所有sigma,p都有证书仍open”。这不是把21个例子说成一般定理的whole_result。

建议关系B：{本核心, CA-OBLIVIOUS-MIXED-SECURITY-2N1} ALL -> 六人原题，kind=implies、relation_mode=unconditional、accepted、明确contribution。result为“b352b7fb49fe的完整K_sigma内所有单位客户点及有理克隆点，W>=6v6>=6OPT6/11，故2W>=OPT6”。remaining为“六人原题其它所有完整形式策略、其它标签数未被本有限证书覆盖”。限制给定case是已明示适用域，不是假装已付普遍C6；不可whole_result指向整个六人原题。

implementation/checks语境只有在Root认为对研究者有明确复用价值时才新增：独立审计源码实现了本精确有限证书的定义级验证，生成器/旧浮点数值页不是数学前提。现有核心evidence已经保存该实现入口，通常无需再造程序hub或将每个目录相邻对象连边。

## 9. 不能成边、未付义务与Root后续边界

一个n4共同Q锥、三旧selected锥、恒A策略族、21份有限锥之间，没有已给出的策略包含/变量映射可互相推出；人数、标签域、Gamma、实际叶及Q不同。只有证书形式相同，不足以造implies/equivalent_to。security-cone-contracts的杂合合同也不由本21锥完整推出。

核心给定21锥的数学soundness无新缺口；本次仍依赖现有明确source+input绑定的成熟审计，不自称独立重验全部数值证书。后续正式worker应保准确复用范围。任何正文或registry变更都须重新对受影响pin/SHA判断，不能把本准备快照当永久当前版本。

普遍强聚合证书存在仍未付；一般共同Q的必要性未证；六人half仍open；一般逐人安全桥已失败且与这里的总福利证书不同。Root gate后仍须核最新任务归属和版本、正式claim/read-add、制作独立边/收据、native绑定与检查、checkpoint确认pushed，再按正式队列交付。此次没有执行其中任何状态变更，不能据本备忘录称原3A任务done。

## 10. 读取与字节ledger

下面的“全文”指本轮实际文本实读；registry全文件仅JSON解析和指定对象合同/metadata检索，未声称全文读全部对象。gzip为原字节读取、JSON解析与上述精确结构/21全部Q范围；未新重建Gamma或复算完整矩阵。证据README是成熟证据合同复用，不冒称其链接的每份原码/矩阵均于本轮重读。

### 当前完整登记合同与pins

| object_id | v / truth_status | registration_pin |
|---|---|---|
| customer-attraction/fractional-and-cone-auditor-contracts | 2 / proved | c11bad6a52fd8dbb38e5a0cb845f9631008b7afe3026360fd709327e69f2debd |
| CA-SECURITY-CONE-DUAL | 3 / proved | e31e80e9d89c7fad56eadbcbfd46a50af3857d6119eea8060c3a41a0cb987899 |
| CA-OBLIVIOUS-MIXED-SECURITY-2N1 | 3 / proved | 565f6bdb541c09f8229f27ca4d47409f946a555f141378e72fb91c5a55082ea4 |
| customer-attraction/six-providers/exact-six-full-history-half-cover | 1 / open | 2d5b191271cb052c435121a41935eb3958540d5a53cb05013f13dd45a70f6e31 |
| CAG-MODEL | 1 / definition | 3216d1db43ff83e0e0c9cf2479e79611277c9d9291a68e7f9b85ec4bb299dc5c |
| customer-attraction/fractional-set-cover-static-security-lower-bound | 1 / proved | 5df2fb84ed38e70c0cbdb6bce118370fc9d681c98c5dba89a8dca1be6f78f230 |
| M-5c61b8e33f844e8498ea4d5865b1f7bd | 1 / conditional | 69e60e6cabe910150355acaecb7eae23f079577f976ad90d36a9a096eb5dc05a |
| customer-attraction/common-background-security-cone-reports-and-version-boundaries | 1 / proved | 1916894cf2d930adf2b0173f6c3ea962b85c648ad48cf5222cb50b5c14b595eb |
| customer-attraction/security-cone-contracts | 2 / unassessed | 4b4891e8fcd1763af31233f0487a46fc274def46da1acc0db7eca848da1b4f17 |
| customer-attraction/designated-policy-security-cone-and-seven-maxima-boundary | 1 / unassessed | c4262a44867bd336dd5d5487a34689e15391381208ba7dffcfdc7b998f2cb5af |

### 实际读取/比较的文件与当前完整字节SHA

| path（相对clone） | bytes | SHA-256 | 本轮范围 |
|---|---:|---|---|
| AGENTS.md | 5518 | 20293db840f907c32f774b0d7f72450c56e6c0ad937720699d14f7c02e693cc9 | 全文 |
| research/IMPLEMENTATION.md | 31889 | fb6613cd0c429f28b8bcfb1064076a629540cfbee8f7e3d670b0b39e78ff0d4b | 完整阶段接口；登记/构图/ALL与contribution/成熟证据复用规则 |
| prompts/03-map-worker.md | 2559 | 6629f71923c54d994297d54c3737b285227b72c463641d318c3f61c9342d07b2 | 全文 |
| research/operations/map-v2/tasks/customer-attraction-3a-3a-2c3bfa8c793694f1.json | 5288 | 4e82f43dc1c4ba8f32c31106946f2603c15bfb3d2b375c7714c99b1ac60159f6 | 完整task定义与本地状态 |
| research/registry.json | 16592455 | 9f98c4681c75fdc25f9a38f2a13b2dc3ac950b4c0b14c21d6525d763801ebc77 | JSON解析；上述完整对象合同；其余仅ID/title检索与canonical清单 |
| archives/customer-attraction/state/资料/客户分数负载覆盖与固定策略锥的审计合同--资料.md | 17780 | 0013a2a0986eb81e11735bc2a794e47e5f650cad43c173817a02a14f01ddb3aa | 全文 |
| tools/evidence/collaboration-model-and-cag-audit-primary/related-cones/760834c0f64c80b5ccc1 | 552002 | a4e84d0478ba0ededabe547870ad0a4916cd05a78e686183ed6ef1b660583045 | gzip全部字节读取/完整JSON解析；全部21 source/Q；policy首末行/长度；lambda分块长度/行宽；无新Gamma/全矩阵复算 |
| tools/evidence/collaboration-model-and-cag-audit-primary/original/3e153d43f71d6ebd66e6/tests/audits/customer_attraction_new_security_cones.py | 3795 | 52e8f2a93db13ed523014119c52d7d82333092eb1d084668481b26c0a38693c9 | 66行全文，只读未执行 |
| tools/evidence/collaboration-model-and-cag-audit-primary/runs/new-cones-report.json | 8686 | cfaf3ac6bda723bccca5ff0da40d1778b3be1a67b5ba9fc88f6741154ed4ea7d | 412行全部21case全文 |
| archives/customer-attraction/state/审查/五人半覆盖上传证书与个体安全运输尾部五源接续审查--审查.md | 18825 | 21243ef4cd7288e4e305dae1d3868a77da9ea67e73333619d03b438b246f020a | 精确section：5. common_q_generator.py：固定策略锥的候选算法，运行边界明确（175-203行；含5.1/5.2） |
| archives/customer-attraction/state/审查/新策略安全锥与半顶点候选增量审计--审查.md | 9556 | f1ead3c45e5ee9e75cbe097a334ca7dfd7aa9f94e2cea76414d515572f0b604f | 全文 |
| tools/evidence/collaboration-model-and-cag-audit-primary/README.md | 714 | 64971051539b436f63b59e996f499e0eda30bdc69131c11b2c4588fd762ff12f | 全文 |
| tools/evidence/collaboration-model-and-cag-audit-primary/cone-input-structure.json | 21172 | 9ae8d0ebd5aca837f386c4b88b43e88176648c339788aab2df3d5744c33a20ed | 成熟输入结构合同；本轮独立原gzip结构解析与21全部Q，不冒称逐字读全结构文件 |
| tools/evidence/collaboration-model-and-cag-audit-primary/runs/new-cones-run.json | 1841 | 0f80fd4788d7a4eb4e4b1f4d8b677b5dd3f1f4ee4db1b7931b693e0f9cd8ac88 | 全文 |
| tools/evidence/collaboration-model-and-cag-audit-primary/new-old-cones-comparison.json | 624 | d6a1dcb2a4340fa9ef584f174b1f47a73dc383de3f28ea934ccb83528556d634 | 全文 |
| archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md | 7598 | cc4a9dadb09e08b072cb63214d2e084db38db219e4100efbccf9b7f497520e88 | 全文 |
| archives/customer-attraction/state/定理/完整策略锥的静态安全值对偶--定理.md | 8723 | b279e1f63f08b961365a2cbc0173530de7090fd1c7beefc1a42c585ef6e58cf5 | 全文 |
| archives/customer-attraction/state/定理/静态混合安全值的锐目录计数界--定理.md | 6354 | 034c940129b4ef2e1b5a2902f9256f9dbfed5fbc8bf6750c4403217db3a6b15f | 全文 |
| archives/customer-attraction/state/审查/指定完整策略锥安全证书与预算边界--审查.md | 8627 | ba40e499dce1198cf24fde610f358bdd3b42988493064e769bd9cbe938f153f3 | 全文，承重全锥证书节重点比较 |
| archives/customer-attraction/state/审查/共同背景安全锥报告与版本边界--审查.md | 23128 | f26af391adb454cfb27bad1f62e37ab0e7a894f7a133f621eec80a1c5379c5f5 | 全文；首90行另补读 |
| archives/customer-attraction/tools/evidence/Boss7-resume-common-reports/README.md | 3210 | 8e9dae3af518c9f53c86b7224a81e87132d7be2d4f0d96dba0cbc5531f145601 | 全文，证据合同，未重跑 |
| archives/customer-attraction/state/程序/R-f6两种完整策略生成与静态安全探索的原始合同--程序.md | 12282 | 247938c0f2bfd4d1d5fdf80d8d8b7c2542e394a21530a4400f00d3e8b0ce8d9f | 精确section：6236B静态安全探针的真实值和归一 |
| archives/customer-attraction/state/审查/逐人安全与全树流增量审查--审查.md | 12465 | d764ea3fca542496ae66c7c5a4af66ef113e22d6871fc8785016e397be8879da | 全文 |
| archives/customer-attraction/state/计算/静态安全值与聚合保底的精确核验--计算.md | 8460 | 9ca3c8ce9e23da06f04168123bbbef57e70998a16a11b22f90c79c4c07da35f9 | 全文，成熟运行证据合同 |
| archives/customer-attraction/tools/evidence/aggregate-security/README.md | 3975 | ea2b4a3ea87d3ef451642b9d1f555e71f43e78063fd3f8fcfbb18705ec4731f9 | 全文，未执行所列命令 |
| archives/customer-attraction/state/程序/安全锥合同与共同Q认证边界--程序.md | 2375 | bfd39640ed6206aeb08db2f5a370c0ca184ca4ec51d38381e991d98ad6b7b975 | 全文 |
| archives/customer-attraction/state/计算/指定策略安全锥与七极大来源边界--计算.md | 1308 | ae3113480ec327071179eb43933185e7d72b8b9548f5da4ba5a32571b6832a1e | 全文 |
| archives/customer-attraction/state/引理/分数集合覆盖数的静态安全值下界--引理.md | 15414 | 364c4716daa32bf6c677c777ae89eaf73515a1ed931569c8a84f2fc588c193a6 | 全文；也承载M-5c61...必要证明 |
| archives/customer-attraction/subarchives/six-providers/state/问题/六人完整历史半覆盖目标--问题.md | 4995 | 0626668e7a825108fc0b3699e42394b75b1c2e2a526df220a90d91a02afc8a0c | 全文 |
| archives/customer-attraction/subarchives/six-providers/问题--问题.md | 2140 | 21391fbaaa2893fef7b228a345fcf1d7f5c5d1dc8a42cc642d6bfbbeccc7c065 | 全文 |
| map/edges/boss6-six-security-bridge-3b-37e2f44d17517898/universal-fixed-query-security-to-six-half.json | 5898 | 3d26fb6b6167a692827a5b5a881ccc3c079474fc73d6db5000dc90074799d4d4 | 全文，canonical=True |
| map/edges/boss6-six-security-bridge-3b-37e2f44d17517898/review.md | 11602 | b3ba68bb8713e48e3622d231eb015258aae17f87462fd90f6b82841d93924f1e | 全文，成熟关系证明范围 |
| map/edges/customer-attraction-3a-3a-384393b28422e037/constant-policy-explicit-security-dual-certificate.json | 3224 | 30bab87a7740aeda8b1cc593534e8f60af8b4474e2217fe96505308050124db0 | 全文，canonical=True；未据此声称恒A源对象已完整新读 |
| map/edges/customer-attraction-3a-3a-009ebb79ddec6207/fractional-static-bound-to-conditional-full-cover.json | 2514 | 644a3e5340543cbc8ed6ff5a6101076013c2723d04575db335835b1a82f669bb | 全文，canonical=True |
| tools/research_runtime.py | 119092 | 414713215bc28a062a2ef0330b150f81298987e893278fe90b44b38c7f4d4023 | 只读pin定义、load合同、相关对象view定位段；-B导入load verify=False，无native命令 |

解压JSON：6153467B，SHA-256=4272c141c110c130a391d5ba68b9085f29486bddd1351007dfe14a654d14665c。没有把解压文件另写入仓库或scratch。

canonical端点扫描之外，没有把其余2285文件的数学论证称作已实读。初次尝试按frontmatter名查询对偶/模型时明确得到不存在，随后按现役稳定ID读取；没有为此新增或改写身份。
