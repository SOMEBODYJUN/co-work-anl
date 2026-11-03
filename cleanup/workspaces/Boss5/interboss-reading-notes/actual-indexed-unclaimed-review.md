# 未认领来源的实读交接：actual13、匹配索引及最大根审计

## 当前状态与可用边界

这是Boss5内部代理的**阅读交接笔记**，供实际source owner判断与复用；不是已发布数学正文、完成回执、独立新审计或done依据。父方首次显式claim37因为 `c761424f19bf719d1d65` 已被Boss3认领而整笔未成功；随后父方报告maxroot prefix及整个research/workspaces原子claim均为空。本代理没有取得下列任何来源的清洗所有权，也未替其他Boss提交done。

按父方最终协调，本批在此冻结。没有正式state对象、没有 `receipts-actual-indexed.json`、没有数学程序执行、没有新LP/逆向归纳/定价/搜索或新checker。后续不再扩读未领来源。所有Git/start/claim/done/checkpoint/公屏操作由父方协调；本代理未读取凭据、未改clone内文件。工具只用于冻结文本读取、全仓本地文字比较及clone外笔记写入；不把取得文本当作数学运行。

原先拟写的 `state/审查/五人匹配分支索引铰链与双状态证书--审查.md`，以及后来拟拆的两个state对象均**未生成**。本笔记中建议的对象划分只供实际owner决定，不构成正式路径占用。

## 冻结版本绑定及实际阅读范围

以下表中原件共同前缀为 `research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/round8_five/`。所有条目在inventory里均绑定两个冻结提交：

- legacy-cleanup：`68fad804ec5946cb296f77dc5b336308a66abf12`；
- main：`aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c`。

每个表项的两个提交在inventory中同path、同blob和同SHA；本次直接读取冻结 `clean show ID` 输出，没有将当前工作树搜索命中冒充原件。下表前8件是父方原拟分派但未领成功的主源，接着5件是本代理只读的maxroot相关源，再后7件是全文比较来源，最后1件只检查actual乘子及诊断作用域，不声明读尽其长数据。

| 源ID | 前缀后路径 | 字节 | SHA-256 |
|---|---|---:|---|
| `c761424f19bf719d1d65` | `certificate/actual13_projection.py` | 5212 | `04c4496011670c79ab2c4c01d0e6c0a1d3aeed947d6c3fcd1a84298c4afb3926` |
| `5bee16e8128666067aa2` | `certificate/actual13_two_state_certificate.json` | 5532 | `27abaed9a9c6f203b620ae21856c29e0b18409037893eaf9f0d9acc37145cbb4` |
| `cfddac5e392ab8d6f0ed` | `certificate/actual13_two_state_certificate.py` | 3825 | `8cd25c9b9282540a3ad29aea643efcfa7716d73759c1ba1475a814abb42e98d3` |
| `7d205a6494aec795baf2` | `certificate/audit_matched_indexed_hinges.json` | 2102 | `34a719b65e9f468beeb7d79b10b42f3594ebffae8e28773289c92b14ed0c13df` |
| `d66b0459e38b41b23ea5` | `certificate/audit_matched_indexed_hinges.py` | 4220 | `4767ab503941f18cf3c57b31771154c783fc2ffe14d241a0c4ab42f21140bacc` |
| `a8715da48314f1084995` | `certificate/audit_max_indexed.json` | 2590 | `45fdcbe6f9c5af35e39bb1647b7865eb3ac67b2d1f20893d6efc2dde9fe7513c` |
| `72b49f59e51a44e0804d` | `certificate/audit_max_indexed.py` | 6007 | `7f57bd49b25150e0abe8c2f2a08e63379ef28187e4b46cc5b4368f5d0a1e643b` |
| `f5a35689f03675cf229d` | `certificate/matched_source_review.md` | 2857 | `d50b6b8edf9480dbbef1ac31369a5573ed387b1de452052626235bbd77e526f5` |
| `229ddd23a41de996995d` | `maxroot/actual13_decomposition_audit.json` | 199 | `7e481a0bc1f53d37a637ecd2256a1d1667aba49cdfe37ec03eaf071800d78dba` |
| `2c041730362346cdefbf` | `maxroot/actual13_payment_pricing.py` | 6741 | `45a3dfc411778ca98779058e6fa07d9bd00eb0256bfb3c3b020ef6996a27ceb7` |
| `598d6bbd0dcb98249a8a` | `maxroot/actual13_pricing_contract.md` | 3303 | `4bb70c19347cf59bc37c662d90e0df510c3812a86cd8468969429e699846cc44` |
| `4e2de0ae1f4a6004bba0` | `maxroot/actual_payment.md` | 3053 | `2960857fbdedbb911d02c342c3ebf02e682e6d43b5807084c0af135b4dbfaf7d` |
| `c6f4a50af01a355f86aa` | `maxroot/price_actual13_payment.py` | 317 | `eabb533941b60f6b738a8fe3d534b716bf4b63019233f6f33340e85d2eff657b` |
| `6b67dd8f3846535b08c2` | `certificate/max_indexed_coupling.md` | 6043 | `48a230e3038b402bd5b8e08b3554390f4bee796484591ae01b06e5915d1b127c` |
| `891a9e91438dc2380ff1` | `certificate/max_indexed_coupling.py` | 11829 | `32704775277544852e3c3b69bac4bc6c9303643ea880183b416c250322a29e81` |
| `2f4bb7016d749eb818a2` | `maxroot/indexed_hinge_pricing.py` | 4251 | `27b9fdc7c3971bfd48a0cd8f2c4ba1a99bb1f5b3921bc499d6b56ce8079bfdf0` |
| `36564ce6b130325083d5` | `maxroot/trueH_payment_pricing.py` | 4469 | `adf09af85278d5c1b90dd5f534ad4464c82249ad84b5f886aa5e40fc3280c507` |
| `f804f00da032eb7f28b1` | `certificate/two_real_weighted_branches.py` | 7501 | `cc28b48c3f8c49df4f0f135784974479a90f28922545f2d55f68880c97f83c83` |
| `d8d084b1bcf43d1406b5` | `maxroot/weighted_hinge_independent_review.md` | 5651 | `810a983cfce9a9ef2dc44ec35c69d26cf1f4ab9938d56b5a6b58875b893d5f2c` |
| `4417e3718ddadf36e491` | `certificate/trueH_seven_rows.md` | 4835 | `6bd7a6ad74d6dc42ffd1d14c78a0d3aa2c78a5840988a9a87759111321dfb1f1` |
| `1c198f1a0750989b7d43` | `certificate/two_real_branches_exact_current_source_own_index_v1.json` | 12026 | `baee2c969b1284df1d42cfb1bf502e49dc5fa02a160f930001fff7597770a3bb` |

前8件源码、审查和JSON均全文实读。`actual13_two_state_certificate.json` 的36项Theta及144项逐状态余数全部读到；两份四例报告的全部主题、路径、计数、空/零字段及hash均读到。`two_real_branches_exact_current_source_own_index_v1.json` 作为相关源，其actual的13个原有理乘子、输入身份与单历史优先诊断已读，max的长系数向量未读尽，不能写成该相关源完整处置。

## 一、十三行实际第三位投影及其双状态化

### 1. 同一完整策略与行的来源

原模型是有限单位客户、有限非空共同带标签目录、恰五名单位提供者；固定每份在全部有序历史上定义的纯SPE。空主题、重复选择、同覆盖异标签、零客户和任意离轨平局全部保留。实际路径ABCDE，第三位精确前缀(A,B)的旧负载p=A+B、原当前收益u=C/(A+B+C+D+E)。在该节点选择背景权1/(p+3)最大的合法H，强制选H后同一策略给真实Q,R。强制H不是被另假定为最优动作；其真实后继才各自有末两人最优性。

`actual13_projection.context` 的固定标签顺序为 `ABCDEUVWXY`。m=`max_bits[0]`是全目录裸最大主题会员，z=`max_bits[4]`是原最大根真实路径的末主题；它们不等于actual第三位H。d由AB_hist前坐标为1的五索引计数给出，必须与AE和Sbranch共用同一个比较元组计数。AB末菜单计数ab，AE末菜单ae，Sbranch三个后继菜单su/sv/sw。X/Y是旧固定合法主题。以上菜单只作H分支的合法比较，不被冒充为H的后继。

十三权顺序准确为8251、4703、5446、165、307、92、66、2、925、15、7、17、4，分别支持source IC、同H支配Q/R、真R五比较末位行、裸M大小cap、两固定税、AB末菜单×比较菜单税、AE末菜单cap及Sbranch四种税。各原行仅在对全部客户求和后非负；逐客户可能负。零分子份额定义为零。

对背景b=p+h，真两尾的税预算是Htax=Vq+Vr+q/[(b+1)(b+2)]。长度na/nb菜单会员数a/b的笛卡尔比较税为

    na*nb*Htax − (nb*a+na*b−2*a*b)/(p+h+1) − 2*a*b/(p+h+2).

对角、重复和同主题比较仍合法，不删相同索引。该预算由真实三条IC及非负交叠余项得到，不假设终局静态NE。每客户G是13行的正整数权和，phi=max_(h,q,r)G。真实共同HQR的一组会员值给ΣG(true)≥0，因此逐客户向上取最大给Σphi≥0。独立最大状态未必拼成真实主题，不提供逆实现性。取min会丢掉这个必要方向。

### 2. 双状态证书的完整公式

七税对及权重为(X,Y;1,1;92)、(Y,z;1,1;66)、(ab,d;5,5;2)、(su,X;5,1;15)、(su,sv;5,5;7)、(su,sw;5,5;17)、(sv,d;5,5;4)。据此

    C1=Σ weight*(nb*a+na*b−2*a*b),
    C2=Σ weight*2*a*b.

所有Htax常数系数合计983，q/r所有依赖移入

    core(p,h,d,q,r)
      =(-8251h+983q+1808r)/(p+h+q+r)
       +983q/[(p+h+1)(p+h+2)]
       −4703q/(p+3)−5446r/(p+3)−165d/(p+h+q+1)
       +14774h/(p+3)−307h.

第一项按零分子取零。14774=4703+5446+5*925；不要只复制现有资源中的Fqr而遗漏这两个q/r无关h项。Theta(p,h,d)=max_(q,r)core，完整表为：

| p,h \ d | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---:|---:|---:|---:|---:|---:|
| 0,0 | 0 | −165 | −1549/6 | −1022/3 | −2539/6 | −1517/3 |
| 0,1 | −2515/6 | −2851/6 | −3181/6 | −3511/6 | −3841/6 | −4171/6 |
| 1,0 | 0 | −165/2 | −165 | −495/2 | −330 | −825/2 |
| 1,1 | −368/3 | −685/4 | −425/2 | −1015/4 | −295 | −1345/4 |
| 2,0 | 0 | −55 | −110 | −165 | −220 | −275 |
| 2,1 | −1043/20 | −467/5 | −2533/20 | −3193/20 | −3853/20 | −4513/20 |

置

    V(h)=8251u+307m−925ae/(p+3)
          −C1/(p+h+1)−C2/(p+h+2)+Theta(p,h,d).

则phi=max(V(0),V(1))，也精确等于

    V(0)+[Theta(p,1,d)−Theta(p,0,d)
           +C1/((p+1)(p+2))+C2/((p+2)(p+3))]_+.

这给相同当前13权的双状态铰链，不是任意未来支持都免费双状态。新增R对非固定族菜单查询可能使q与hist交互，需要重核。不同分别投影cut的正权和一般需要各自hidden状态，不能强行共用h。

原 `actual13_two_state_certificate.py` 标准库Fraction构36个Theta及完整144个差Theta−core，并断言全部非负；再导入作者projection，在63指定原子上逐h比较，共126次条件比较，完整max2还与max8及hinge同值。144系数域检查与126指定点比较是不同责任，后者不能反说全部直方图组合已被代码枚举。普遍恒等式来自税成本分解及36核表，指定点比对补实现证据。

报告保存完全相同负分数

    −372081335141417451740722684895465152621574175134577343908604041024433
    /218406283421045387636446698134713715269092649270874886827970243628332.

这是排除指定6750旧必要系统点；不是游戏、完整SPE、真实OPT、half或6750行的本程序完整重审。原点SHA `29e0b3e0c07884ad2565999c373db36ff32ea4b77c79a61ef52e12cdc8e3286e`；two-state报告中的 `source_certificate_sha256=5220d2dbd21a23cd8c0e5d2ce342e3ca036783c3a7bcc47ab616c6c05ebd56f0` 绑定actual13_projection.json字节，而不是点文件或自身源码。源码hash与表中cfdd一致。

### 3. 发现、相互依赖与尚未处置

`actual13_projection.recover()` 从two_real_branches报告的actual有理乘子读取发现权；D逐1000/2000/5000/10000/20000/50000/100000/1000000尝试，遇首次负即break，冻结报告实际只到20000。最终非负整数自身证明行合法；浮点来源和取整只属发现。它还导入 `two_real_weighted_branches.rows` 做63*8*13=6552项公式比较，因此这部分是作者两实现一致性，不能冒称无作者依赖的新独立原始推导。recover有main guard；two_state.certify也有guard，但导入其模块会构造THETA。两者运行会覆写相邻同名JSON，本代理未运行。

现有正式 `五人根独立审计的输入身份与投影范围--资源.md` 已完整保13原行、指定63点、分离值、单cut max方向及原tree审查；本批候选独有增量是actual13作者源码自身合同、完整Theta/144余数和max2/hinge实现，不应重复授既有父审一次新成功。实际owner可决定补入已有资源还是建立双状态引理；本笔记不替其作最终处置。

## 二、161条匹配索引铰链及四例原节点回放

AB/AE五索引枝分别是(A,B,T_i,R_i,S_i)、(A,E,T_i,R'_i,S'_i)，type=(t,r,s)。pos0强制T_i不作优化源；pos1是真第四位，自己的旧负载p=旧背景+t、余k=2、当前真实收益r/(旧背景+t+r+s)。Sbranch为(A,T_i,U_i,V_i,W_i)，type=(t,u,v,w)；pos1真第三位p=A+t,k3，pos2真第四位p=A+t+u,k2，收益各按本索引真实终局自己的分子/总负载。不能从别索引搬收益或仅保菜单总数而丢源关联。

每个真源节点应用背景加权最大主题H的BNS，再与同一个H对五查询菜单的cap相加。L=4(k−1)，查询会员数c、五比较数d，参数t≥0的逐客户式为

    5L*u_x − t*c/(p+k) − d/(p+1)
    +[(k−1)d−5(L−1−t)(p+1)]_+/[(p+1)(p+k)].

真正非负的是对全部客户求和。五源分别取自己的H并逐源消去，再对五个索引求和；c/d是本family共同固定的五主题菜单重数，不随源i重选查询菜单。完整参数断点来自整数p,d域；相关 `max_indexed_coupling.md` 及 `weighted_hinge_independent_review.md` 已解析说明断点间全系数仿射、终端射线不更强，有限断点不是任意目录/SPE抽样。

`indexed_hinge_pricing.py` 的row_value按完整直方图类型重数n乘上述本源式。coefficient_array对同一完整hist数组求和，条件缓存保tag,bg,pos,menu,t；固定旧十位、共同d及完整32最大根状态之后，新行仍只依一个family。其整数模式显式拒绝，不把浮点array当Fraction证书。run只做受限LP，不能凭受限二以下值宣称全域；相关原独审已经说1.9940166655771112候选被完整oracle找到负类型。

`audit_matched_indexed_hinges.py` 使用规范Instance/ExactSPESolver构完整有序策略，history依赖action_selector保平局，再直接枚举全部有序历史的每种行动比较。直接侧**不调用target.scalar**，但读取target.SPECS和target.rows作被比较实现；独立性限支付展开，不等于无目标数据/规范求解器依赖。它从原客户集合、原主题标签、finish后的真实路径和Fraction支付独立展开每条源节点式，再核与压缩求和相等且≥0。

四例全部冻结为：

| 例 | 共同目录主题（每组为客户集合） | actual五标签 | 含自身IC | 行数 | 源使用次数 | 最小余量 |
|---|---|---|---:|---:|---:|---:|
| 1 | ∅ | 0,0,0,0,0 | 5 | 161 | 805 | 0 |
| 2 | ∅;{0};{0,1};{1,2} | 2,2,3,3,3 | 1364 | 161 | 805 | 377/30 |
| 3 | {0,1,2,3,4};{5};{6};{7};{8} | 0,0,0,0,0 | 3905 | 161 | 805 | 121/12 |
| 4 | {0,1};{1,2};{0,2,3};{3,4};{0,2,4} | 1,4,4,2,2 | 3905 | 161 | 805 | 177/20 |

总9179个含自身行动IC、3220个源历史**使用事件**。805=161*5，不能说805互异有序节点；相同行可能反复使用同源。四个指定实例仅核实现，普遍性来自真实节点及BNS证明。JSON target_code_sha256与表中indexed_hinge_pricing的27b9…相符。原audit有main guard，执行会写相邻JSON；本代理未执行。

## 三、1414条最大根—旧索引菜单耦合审计

`max_indexed_coupling.py` 保留最大裸主题根强制后的完整真实五主题路径z0…z4，共32会员状态。根强制主题本身没有新分支优化性；所有i≥1的真后继才是源。旧十位主题、共同d和完整五位max状态固定后，K/AP/Tax/Tuple每条只含一个旧family菜单计数及本族二次乘积，因而原三族最大化仍能分开。只保max末背景负载会丢AP查询的个别主题会员信息，不能替换完整32位状态条件。

1414行包括：真尾节点i=1..3的AP菜单笛卡尔比较、i=1..4的K保底比较、真末两人的税比较，以及rem3/4时同一个合法菜单主题重复n次加max路径固定主题索引的tuple比较。三人用beta5/3；四人用1499/750且每个菜单槽扣同一RHOMIN，聚合后是5RHOMIN。query菜单保5索引，固定旧/max主题保1项。税是全部合法对，Tuple包括重复主题；不能把行名字当某单节点IC。

`audit_max_indexed.py` 对相同四实例、同种确定history依赖selector，从实际客户/主题/完整策略展开pair与tuple，在每个被展开比较上核真实不等式，再核全部1414个压缩和相等；其直接侧会使用cm的row specs、AP常数函数及RHOMIN表，不应称完全无作者公式依赖。它自己的支付求值和菜单对/元组展开独立写出。

四例actual与上一表相同。maximum_true_path依次为(0,0,0,0,0)、(2,2,3,3,3)、(0,0,0,0,0)、(2,1,2,4,4)。各例1414行、6615对展开、2695元组展开，最小精确余量均0；IC依次5/1364/3905/3905。总9179 IC、26460 pair及10780 tuple。两份原audit的9179对应同四输入，不能把它们相加称18358互异输入检查或8种不同实例。JSON audited_code_sha256与表中cm源码327047…绑定。

本程序输出路径是cm.HERE/audit_max_indexed.json，而matched audit输出自身HERE报告；原目录同为certificate时常相同，但移植时不能省略这一行为差别。两个audit导入规范solver，完整依赖仍须恢复原相对目录及规范包。当前未完整取得依赖闭包，不授予任意目录下可独立运行的承诺。

## 四、24条真H七行投影的源节点审查

`matched_source_review.md` 后半另审 `trueH_payment_pricing.py` 的24行，不能因为标题同时含161就只保存第一半。24=三个固定真实第三位(max、actual、second)*七个旧索引菜单，加Sbranch五索引真第三位对本族三个菜单。

固定第三位用自己的p/u，七行投影是17040u+1085M−2679*c/(p+3)−F(p,d)，M仅全目录裸最大主题。H每次在精确源历史最大化背景加权大小；强制H后Q/R仍沿同一原策略。indexed只对Sbranch的真U_i逐索引保p=A+t_i、收益U_i/(A+t_i+U_i+V_i+W_i)，所以1085M在五索引和中出现5次。强制T_i、H均不被冒充优化者。

该七行原证明不依赖AP/BNS，与161行的BNS来源不同；原父144态审计已在现有正式真实第三位包络及根审计资源保留。本审查只保代码源节点、缓存与求和的匹配，不把24行或四例审计说成half证书。

## 五、maxroot新增五件的精确定价合同

### 1. 三族差值和65664条原报告

`actual13_payment_pricing.py` 将一个名为Actual13TrueHQRProjection的max8行接到旧6750行，形成6751行。固定p,h,x,d，设a=1/(p+h+1)、b=1/(p+h+2)、delta=a−b。AB差值为

    2*ab*(−5a+2d*delta),

AE差值为−925ae/(p+3)，Sbranch差值为

    15su*(−a+2x*delta)
    +7[−5(su+sv)a+2su*sv*delta]
    +17[−5(su+sw)a+2su*sw*delta]
    +4sv*(−5a+2d*delta).

将ab/ae/su/sv/sw同时置0、保留原d所得不是一个要求可实现的直方图；只是系数多项式常数项。C_h是在此常数上对四个q/r完整取max。三个差值均不含q/r，所以phi=max_h[C_h+ΔAB+ΔAE+ΔS]。Sbranch的二次乘积仍留在同一族内部，不可再拆成独立su/sv/sw最大化。

`audit_decomposition()` 按p∈0..2、h/x∈0..1、d∈0..5、四q/r及AB6值、AE6值、Sbranch6^3全部计数差检查，共3*2*2*6*4*(6+6+216)=65664。它每次调用作者raw_blocks对比family_delta，故是同项目分解恒等式检查，不是又一份独立原始SPE证明。`actual13_decomposition_audit.json` 只有status/checks/meaning三字段，未绑定code_sha256或输入hash；不能凭报告自身单独认定它来自另一源码版本。当前源码与文本合同逐式相符，但本代理未重跑。

### 2. LP与oracle状态恢复不能混用

对新行非负乘子μ，有

    max_hist[old+μ*max_h(C_h+ΣΔ)]
      =max_h max_hist[old+μ(C_h+ΣΔ)].

只有固定h后才可在共同旧bits/maxbits/d条件下独立最大化三个**完整**family直方图。μ非负是方向所需；不同cut不可免费共用h。max路径保32状态、外层h保2状态，共64个条件模式，但这是完整放大系数域的条件化表示，不是枚举64个SPE，也不是已运行并通过了64模式的执行证书。

Universe.proj_h初值None：LP添加列必须用full max8；oracle内部固定h时atom_rows才返回fixed-h max4以匹配条件direct residual。fixed-h行本身不保证原模型必要性。generic driver在两个模式后必须恢复None再加列，这是承重调用合同；本批只读五件未取得generic driver全部实现，不能断言当前driver已被本批独立核对。若固定h产生负目标余项，full max8因μ≥0只令余项更小，故仍给真负类型；反之浮点无负类型须另有精确证书。

源码constant_block用1024*6*2*2表，m/z只取max路径首末位，cache保(h,p,u,x,y,d,m,z)；family差保持自己的完整直方图。源码array、threshold与LP均浮点：proj_weight按绝对值1e−11判断零，family_score拒绝integer；不把数学恒等式的精确性授给全部浮点oracle运行。

### 3. 五件的结果与未取得部分

`actual13_pricing_contract.md` 报告6751行在旧849列上受限重求O/W≈2.00063351925>2，所以当时未启动beta2全域oracle；63正支持新点经单history诊断仍actual747行不可lift、max单可lift，不允许把失败归因成新跨history共同兼容障碍。当前强接口是显式保留actual同一HQR及747原行；此处只是原稿接续建议，不限制后续solver方法。

本代理未读 `actual13_payment_discovery.json` 的完整大数据，也未取得/执行actual13_payment_fullpricing报告，故上述849列、比值、新63点诊断只作为**原合同所报历史状态**，不冒称本批逐列核验。它与既有actual13切掉旧点的精确负值是不同点、不同阶段；不能合并为“新投影已经half”。

`price_actual13_payment.py` 全文仅317B：main时调用generic p.run(100,a.Universe,'actual13_payment_discovery.json','actual13_payment_fullpricing.json',max_new_columns=400,per_state_batch=16,target_beta=2)。它是入口参数，不是成功日志；不能由文件名/fullpricing字样推执行。源码通过普通import取proj/oi/p，部分模块可能修改sys.path；本批没有恢复完整相对布局或验证此依赖链的独立可运行性。

### 4. actual_payment与既有实际并集钱包的关系

`actual_payment.md` 的精确强式为对每个合法C，4W−5r−4|C|+|A1|≥0；后四真源IC权为5/4、19/9、11/3、4。原文给全部64余项表，已逐格实读且均非负。C取裸最大且|A1|≤K推出4W−5r−3K≥0。它只需四个后继真节点最优性，不需要强制根自己最佳。不能把K裸大小与背景加权最大混同。

该强式及64余项已由现有 `五人实际并集钱包的真实前缀付款--引理.md` 与 `五人根独立审计的输入身份与投影范围--资源.md` 保留。本源的额外接口是与O≤Br−CK合并后，设E=5r−K、P=4W−5r−3K，得

    2W−O≥(2−B/5+C)K+(1/2−B/5)E+P/2.

P≥0本身不支付E；保|A1|版本另留K−|A1|信用。原行已由旧IC组合推出，加入含这些IC的线性模板不增强模板。当前五人half另有成熟精确证明；本源不是新的half或六人定理。

## 六、已比较的正式对象与接续建议

本代理本地比较了模型、以下正式对象及其中明确列出的原审查。模型、根审计资源、原tree审查、共享铰链、真实第三位包络、BNS/AP和两人税均全文读取；两斜率/保留余项/后续反例及五人half用于核相关接口、量词和当前状态，不将其中未返回的截断部分充作额外完整来源处置（下列路径均以customer-attraction为根）：

- `archives/customer-attraction/state/资源/五人根独立审计的输入身份与投影范围--资源.md`，及其保存的原tree/actual13_projection_review.md；
- `state/引理/共同加权最大主题的双菜单铰链消元--引理.md`；
- `state/引理/真实第三位投影的五人最大根包络--引理.md`；
- `state/引理/任意背景加权近饱和交换与统一锚主题上界--引理.md`；
- `state/引理/固定背景两人税界--引理.md`；
- `state/引理/两斜率四尾匹配与非匹配根提升--引理.md`、`二值四尾保留余项与对齐补余信用--引理.md`、`state/反例/两斜率根联合付款--反例.md`，用于区分匹配索引和跨根付款的不同含义；
- `state/定理/五人半覆盖--定理.md`，用于纠正旧源的HALF5 OPEN时态，保五人已证与六人独立未决。

“全文读取”的声明仅适用于上段明确标出的文件；其余只声明已读相关接口和状态。没有声称读完其中全部链接、所有source构造器或全仓所有后续材料。相关冻结6b67/d8d084/4417原文的HALF5 OPEN是历史停界，不能覆盖当前成熟定理。十三行、24七行、161铰链、1414耦合分别有不同原支持和源节点，不按相同“投影/最大”名称去重，也不把一个审计的成功外授给另一个系统。

实际owner若接续，可将双状态Theta证书与65664三族差合同合并到一个自足精确表示对象，将161/1414两审计保为资源/实现核验对象；actual_payment可根据已有完整钱包正文判同覆盖并保来源。所有候选都须由owner核自己的完整来源、未读大数据和真实处置，先checkpoint后done；本笔记不预设最终integrated/duplicate选择，不替他方勾选。阶段三图未创建，只有本文已解释的来源、推导、实现与有限核验角色可供后续mapper判断。

冻结交付范围：本笔记一件；没有数学结果入库、没有任何主源完成登记。父方可将此笔记作为跨Boss阅读交接，不能将其作为其他owner已实读的自动证明。
