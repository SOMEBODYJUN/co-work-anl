from pathlib import Path
import json
root=Path('.'); state=root/'archives/customer-attraction/subarchives/six-providers/state'
commit='68fad804ec5946cb296f77dc5b336308a66abf12';pre='research/workspaces/customer-attraction/R-486bb9adb8cd4d9a940dbf3b1ab0b1de/'
def save(rel,i,kind,tag,title,status,summary,paths,body):
 p=state/rel;assert not p.exists();p.parent.mkdir(parents=True,exist_ok=True)
 meta=dict(id='customer-attraction/six-providers/'+i,kind=kind,type_tag=tag,title=title,status=status,truth_status='as-stated-local-proofs-and-finite-records-separated',review_level='source-proof-and-read-after-source-parent-review-reconciled;no-external-review',scope='有限单位客户、有限非空共同目录、任意m≥1；固定同一完整有序历史纯SPE；有限程序/失败模板分别标域',summary=summary,source_refs=['source:'+commit+':'+pre+x for x in paths])
 lines=['---']
 for k,v in meta.items():
  if isinstance(v,list):lines.append(k+':');lines.extend('  - '+json.dumps(x,ensure_ascii=False) for x in v)
  else:lines.append(k+': '+json.dumps(v,ensure_ascii=False))
 p.write_text('\n'.join(lines+['---','',body.strip(),'']))
save('引理/共同终局交换与负载匹配的条件福利证书--引理.md','same-terminal-exchange-load-distortion-conditional-matching','lemma','引理','共同终局交换与负载匹配的条件福利证书','proved-local-exchange-and-conditional-matching;universal-witness-existence-unproved','同策略真实早偏离和真实末位BR经同主题同终局计数转移；负载失真匹配给条件(2−alpha)界，不证明任意SPE有匹配。',['credible/common_terminal_exchange.md','parent/common_terminal_exchange_review.md'],r'''
# 共同终局交换与负载匹配的条件福利证书

采用[共同目录完整历史模型](../../../../state/定义/共同目录完整历史模型--定义.md)：有限单位客户，有限非空共同主题目录，m≥1单位提供者顺序行动，终局客户价值在覆盖者间均分。固定一份在**全部有序历史**定义的纯SPEσ；空主题、重复、零客户及任意离轨平局均保留。这里没有加权提供者，整数类型重数是不同单位客户。

## 两个真实节点的共同终局交换

对任何合法决策历史h，记其当前玩家沿σ得到的最终收益u(h)。在h改选合法主题b后仍沿**同一σ**完成，所得终局计数为q。假设确有长度m−1的合法末位历史g，使σ(g)=b，且(g,b)的终局计数也是q。对每个合法主题T都有
\[
\boxed{u(h)\ge U_b(q)=u_m(g,b)
\ge\sum_{x\in T}\frac1{1+c_x(g)}.}\tag{EXCHANGE}
\]
第一步是h上对b的一条真实偏离IC。单位玩家在同一主题b、同一最终负载q的收益均为U_b(q)，给中间等号。末步是**具体有序历史g**处的末位BR。两节点可以来自不同分支，也可让g在h,b真实后继上且末位再选b；不要求两个历史可比、同深或回复对称。

承重的是**给定σ同时存在这些真实节点和相同q**。仅某个叶可以置换、同福利、另一个SPE可实现相同计数，或任选一份有利续局，都不够；同终局计数也从不识别两节点策略/平局。所有分母只对T客户加查询自身，至少1。m1、空T、零客户仍成立。

若T=X∪Y、X/Y不交，g在X上负载≤1、Y上负载0，直接得u(h)≥|X|/2+|Y|。不需要把后继冻结成原实际路径。

## 任意实际拥挤的负载匹配证书

固定根实际叶(S₁,…,Sₘ)、实际覆盖C、最终负载c*、实际收益uᵢ及W=Σuᵢ。取I⊆[m]，每个h∈I给E_h⊆N\C，使T_h=S_h∪E_h是共同合法主题。E_h彼此可重叠。固定α∈[0,1]，左右各放一份I。

若在i的**根实际前缀**存在上节共同终局见证b,g，且
\[
\alpha(1+c_x(g))\le c_x^*\quad(x\in S_h),\qquad
c_y(g)=0\quad(y\in E_h),\tag{LOAD}
\]
则给i→h画边。c*≥1在S_h上成立；不除以α，故α0/空S_h也在域内。EXCHANGE逐客户相加得每条边的真实比较
\[
\boxed{u_i\ge\alpha u_h+|E_h|.}\tag{EDGE}
\]
因为1/(1+c_g)≥α/c*于S_h，E_h每客户给1。边可各自用不同b,g，不合并它们的历史。

若该二部图有I到I的完美匹配π，只对匹配边求和：
\[
\sum_{h\in I}|E_h|\le(1-\alpha)\sum_{i\in I}u_i
\le(1-\alpha)W.\tag{MATCH}
\]
若某个达到OPT_m的合法m主题元组覆盖O，且其实际遗漏集O\C⊆∪_{h∈I}E_h，则
\[
\operatorname{OPT}_m-W=|O\setminus C|-|C\setminus O|
\le |O\setminus C|\le\left|\bigcup_hE_h\right|
\le\sum_h|E_h|,
\]
\[
\boxed{\operatorname{OPT}_m\le(2-\alpha)W.}\tag{CONDITIONAL}
\]
不要求E_h全在O内。I空时需遗漏集空，推论仍真；W0时不作比率除法。

α1/2时LOAD等价于c_g(x)≤2c*_x−1，给条件3/2界。若实际碰撞自由，则所有x∈S_h的c*=1、u_h=|S_h|，退化为c_g≤1与u_i≥|S_h|/2+|E_h|，是原碰撞自由形式。α0只给**条件half**，不能令见证、匹配或遗漏覆盖自动存在。

## 证明身份与接续范围

原研究员稿§1给短交换证明，父审**先读作者稿后**从定义重构，并独立提出上述拥挤负载推广；作者再吸收入§2。不是盲审、新外审或本次独立发现。匹配和LOAD都是承重假设，未证明任意完整SPE均有；本页也不授一般碰撞自由3/2上界。

[同终局近包含追随下界](../../../../state/引理/同终局近包含差集罚金的全深度追随下界--引理.md)同样利用单位份额在同一终局相同，但比较当前与后继不同主题并扣U\T罚金；本页要求两个真实分支的同主题同计数，才能把收益转到末位BR。[共同末位报价](../../../../state/引理/共同末位报价与隐藏回复投影--引理.md)则以整行乘子合并源IC/末位查询，不自动提供此匹配。关系是不同真实节点接口的比较，不是互授未证明的福利结论。

本引理用于[多惩罚共享终局障碍](../障碍/共享终局多惩罚扩张的外组末位门槛--障碍.md)，其一般匹配存在性和当前[六人半覆盖](../问题/六人完整历史半覆盖目标--问题.md)仍未闭合。原件/程序/有限报告范围见[资源](../资源/共同终局局部审计与碰撞自由联合锥的有限记录--资源.md)。
''')

save('障碍/共享终局多惩罚扩张的外组末位门槛--障碍.md','shared-terminal-many-punisher-lift-outside-group-last-node-obstruction','obstruction','障碍','共享终局多惩罚扩张的外组末位门槛','proved-all-k-at-least-two-all-q-template-obstruction;not-general-collisionfree-bound','早选惩罚与末选惩罚共享完整终局，强迫每个外组扩张由半组收益支付；任意q/奖励重叠仍有sum a≤sum x/2，literal t>2已末位失败。',['credible/common_terminal_exchange.md','parent/common_terminal_exchange_review.md','credible/common_terminal_audit.py','credible/common_terminal_audit.json'],r'''
# 共享终局多惩罚扩张的外组末位门槛

在[单位客户共同目录模型](../../../../state/定义/共同目录完整历史模型--定义.md)研究一类拟议构造，给的是**排除该模板参数的必要条件**，不是一份低福利完整SPE，也不是所有碰撞自由SPE的上界。

## 一般多惩罚模板及两条必须指定的分支

取k≥2，两两不交早期客户组Xᵢ,Yᵢ，xᵢ=|Xᵢ|、aᵢ=|Yᵢ|，Cᵢ=Xᵢ、Aᵢ=Xᵢ∪Yᵢ。储备Z与全部早组不交。给任意q≥1，惩罚主题Bᵢ,ₗ⊆Xᵢ∪Yᵢ∪Z（l1…q），内部及储备奖励任意、可重叠；实际尾主题Dₗ⊆Z，不要求彼此不交。人数m=k+q，拟议实际路径
\[
C_1,\ldots,C_k,D_1,\ldots,D_q
\]
早玩家i收益xᵢ。若各D不交则整路径碰撞自由，但下面必要条件不依赖此附加条件。

要求在实际早期i节点的两类真实偏离后，后续早人仍选剩余C_h：

1. 改Aᵢ后，q个尾人将所有Bᵢ,ₗ各选一次，顺序任意；记最后所选为Bᵢ,ₗᵢ。
2. 改Bᵢ,ₗᵢ后，q个尾人选Aᵢ和其余q−1个Bᵢ,ₗ，各一次，顺序任意。

两枝完整终局多重集相同：
\[
Q_i=\{C_h:h\ne i\}\uplus\{A_i,B_{i,1},\ldots,B_{i,q}\}.\tag{SAME}
\]
若存在一份完整SPE实现这些要求，[共同终局交换](../引理/共同终局交换与负载匹配的条件福利证书--引理.md)把早Bᵢ,ₗᵢ的偏离收益等同到Aᵢ分支末位Bᵢ,ₗᵢ的规定收益。在该末位前缀gᵢ，任何外组h≠i只有C_h：X_h负载1、Y_h负载0，因为全部i惩罚主题不触外组。合法末位查询A_h给
\[
\boxed{x_i\ge x_h/2+a_h\quad(h\ne i).}\tag{OUTSIDE}
\]
只需早节点IC与该具体末节点BR两条必要比较；未指定的子树如何补全都不能挽救违反此式的参数。

k≥2时取任一无不动点置换π（如循环），按h=π(i)相加即得
\[
\boxed{\sum_i a_i\le\tfrac12\sum_i x_i.}\tag{BUDGET}
\]
不依赖q、惩罚奖励、奖励储备内交叠、异质组大小或尾顺序。等组时a≤x/2。k1无外组，不能套该证明或声称所有单组扩张都受同界。

若额外假设合法m主题组合A₁,…,A_k,D₁,…,D_q覆盖全部客户，则它确为OPT，实际与比较差恰Σaᵢ（Y与Z不交），因此OPT−W≤Σxᵢ/2≤W/2，模板比率≤3/2。**全覆盖附加条件不能删除**：任意Z中的其它可覆盖客户不能免费计入该比较。也没有由此得到普遍匹配或一般碰撞自由3/2定理。

## literal整数扩张为什么在末位已失败

取整数t≥2、q=t−1，所有|Xᵢ|=t、|Yᵢ|=t−1。Z内两两不交bₗ（t−1客户）和dₗ（1客户），目录
\[
C_i=X_i,\quad A_i=X_i\cup Y_i,\quad
B_{i,l}=X_i\cup b_l,\quad D_l=b_l\cup d_l.
\]
拟议actual路径如上，
\[
W=t(k+t-1),\quad\operatorname{OPT}_{k+t-1}=W+k(t-1).
\]
最优值是这个**固定实例的静态事实**：A_i全部加D_l恰m题覆盖全体单位客户，非均衡断言。其比率若误认为路径SPE、令k远大t会趋2−1/t。

实际最后D的收益t，而其合法偏离Aᵢ收益t/2+t−1=3t/2−1。t>2严格改善(t−2)/2，故拟议实际路径已经不是SPE。在Aᵢ惩罚枝，最后Bᵢ,ₗ收益也是t，外组A_h同样给3t/2−1，末节点再失败一次。两个分支Counter相同只说明收益相等，不使这份候选策略理性。t2两条局部比较取等；这不由局部审计单独认证完整策略。

增大储备奖励或可修具体末位差额，但只要保SAME和外组不受影响，OUTSIDE/BUDGET仍成立。逃逸须打破共享多重集、让惩罚改变外组负载，或换掉产生匹配的分支几何；仅加更多共享X惩罚者无效。

原[单惩罚碰撞自由无限族](../../../../state/反例/三人碰撞自由族福利障碍--反例.md)对每k≥1确有**存在型完整SPE**，x2/a1/q1给W2k+2、OPT3k+2趋3/2；其Q/B加强状态归纳处理所有真实离轨与多旧A。它不是本t>2失败路径；本障碍只说明此共享终局扩张不能改进该族比率。原完整策略存在性、所有SPE上界、六人half是三个不同量词。

14个局部实例及56条共同终局比较是有限公式审计，不承担BUDGET的全q/k证明，不生成t>2完整SPE。原程序及冻结数据的全部字段见[证据资源](../资源/共同终局局部审计与碰撞自由联合锥的有限记录--资源.md)。
''')
save('资源/共同终局局部审计与碰撞自由联合锥的有限记录--资源.md','common-terminal-local-audit-and-collisionfree-joint-cone-records','resource','资源','共同终局局部审计与碰撞自由联合锥的有限记录','six-primary-whole-read;frozen-output-preserved;no-new-original-run-or-search','352标量/14实例/56本地比较是公式审计；碰撞自由MILP只提完整策略候选，m3p6端点比1、m4p7无候选且metadata失败；保算法/所有字段/依赖。',['credible/common_terminal_audit.py','credible/common_terminal_audit.json','credible/collisionfree_joint.py','credible/cf_m4p7_failed.json','credible/common_terminal_exchange.md','parent/common_terminal_exchange_review.md'],r'''
# 共同终局局部审计与碰撞自由联合锥的有限记录

六主源共34957B全部正常`clean show --out`全文读并保原字节/SHA256/Git blob。六源实际新clone进度owner=Boss4、in-progress；Root正式claim提交8a85c0dc0392c613b5a1f744f3ef715f5a325389报告pushed/synced，原progress保于证据。不作Git、claim/done/checkpoint或共享图变更。

主数学见[交换/条件匹配](../引理/共同终局交换与负载匹配的条件福利证书--引理.md)与[多惩罚模板障碍](../障碍/共享终局多惩罚扩张的外组末位门槛--障碍.md)。[证据](../../tools/evidence/common-terminal-exchange-primary/README.md)保存所有原件、四份正常show related和七份runtime依赖（joint/LP两源重叠）及现formal比较；此处算法与冻结报告不替解析证明。

## 2950B局部审计的真正输入与执行范围

`common_terminal_audit.py`只用Fraction、Counter、Path、json，有main guard、无CLI。run(t,k)显式展开不同单位客户，t2…8、k∈{2,3}，q=t−1、m=k+q。客户用带组标签的tuple区分，构造X/Y/b/d、C/A/B/D合法目录。

它按固定拟议终局和一个合法比较m元组求union大小，不调用solver求SPE。比较元组A_i加D_l恰m题覆盖全体实例客户，所以保存的`intended_OPT`也是该实例真实静态OPT；标签“intended”不表示路径已是均衡。

payoff(action,terminal)按action客户的最终覆盖数精确分份额；join把action追加prefix。代码核actual末D收益t、改A0收益3t/2−1；对每个i及h≠i核两枝Counter相同、早B/末B收益同为t、末位改外组A_h收益3t/2−1。这里没有定义完整σ，更没有枚举任何有序策略树或全部IC。

main另对α∈{0,1/4,1/2,1}、actual_load1…8、branch_load0…16，**仅在**α(1+branch_load)≤actual_load时核倒数比较。544个网格点中满足前件的352个计入；按α分组数量为136、108、72、36，均由有限整数范围可直接数出。该有限网格不替一般[LOAD解析证明](../引理/共同终局交换与负载匹配的条件福利证书--引理.md)。

main会**覆盖写**邻接`common_terminal_audit.json`，再stdout打印cases14、all_t_above_two_fail_last及其计算的邻接output路径。冻结JSON没有保stdout、Python/时长/argv、源码SHA或本轮运行绑定；本批不运行它或覆盖原报告。

## 14679B报告全部字段与全部case

根3字段为scope=`exact local obstruction arithmetic; no complete SPE claim`、load_distortion_scalar_checks=352、cases。每个case共11字段：t/q/k/m、unit_customers、actual_W、intended_OPT、actual_last、actual_last_A_deviation、is_intended_last_BestReply、common_terminal_comparisons。保留此逐名清单以免把“BestReply”当完整认证。

|t/q|k2：(m,客户数,W,OPT)|k3：(m,客户数,W,OPT)|actual_last|A偏离|全部外组slack|
|---|---|---|---:|---:|---:|
|2/1|(3,8,6,8)|(4,11,8,11)|2|2|0|
|3/2|(4,16,12,16)|(5,21,15,21)|3|7/2|−1/2|
|4/3|(5,26,20,26)|(6,33,24,33)|4|5|−1|
|5/4|(6,38,30,38)|(7,47,35,47)|5|13/2|−3/2|
|6/5|(7,52,42,52)|(8,63,48,63)|6|8|−2|
|7/6|(8,68,56,68)|(9,81,63,81)|7|19/2|−5/2|
|8/7|(9,86,72,86)|(10,101,80,101)|8|11|−3|

bool在t2两case为true，其余12为false；程序此字段只比较actual_last≥A0偏离，不穷尽所有末动作。common_terminal_comparisons对每case列出**全部有序对**i,h∈{0,…,k−1}、i≠h：k2各2条、k3各6条，总56条。每条6字段为i、h、last_B=t、early_B_same_terminal=t、last_deviation_A_h=3t/2−1、slack=1−t/2，全部Fraction值按原字符串保存。完整原JSON逐行保留，表格不替换原字段/类型。

t>2的false是明确盈利偏离，足以排除拟议路径；t2的true仅通过此比较，不自动给完整SPE。旧[单惩罚族](../../../../state/反例/三人碰撞自由族福利障碍--反例.md)另有完整Q/B归纳证明，不能借该有限报告认证它所有k，亦不能借完整族修补t>2。

## 3094B碰撞自由联合候选程序：不是局部审计

`collisionfree_joint.py`导入NumPy/SciPy、canonical joint MILP与固定策略锥模块、规范Instance/StrategyCertificate/verify_certificate。原路径由parents[5]定位项目根，sys.path加根和tests/audits。顶层取joint_candidate函数源码，再用字符串替换和exec重定义：

- 在`hi[:n]=m`之后，对rootmask同时含两个实际路径标签的客户类型设重数上界0；
- 将metadata的`float(result.mip_gap)`改成还需`mip_gap is not None`才转换。已全文读canonical joint/LP原件，两个目标文本均实际存在；未导入或执行此monkey patch。

CLI为--players默认3、--topics默认6、--seconds默认60、必填--out。内部m玩家/p主题，强制actual有序路径(0,…,m−1)、比较portfolio=(p−m,…,p−1)。其有效预期域p≥m≥1，CLI本身没有完整参数校验；只搜这一根路径和一个固定portfolio，不穷尽有限规模全部SPE或所有collisionfree路径。

所有非空兴趣mask是客户变量，共2^p−1项。类型不得同时喜欢两个actual路径主题保证该指定终局碰撞自由；允许没有实际coverer的类型，不把它们当零客户。继承联合MILP的big-M=m来自归一化W=1及根偏离保底：每主题总客户≤m u_root≤m，故类型/效用都有此有效界。完整有序节点各有one-hot动作、conditional效用一致/IC，根路径固定，浮点MILP仅提一张完整动作图，任何浮点upper bound/timeout均不是数学证书。

若提到cone，再在该**固定完整策略**的真实IC矩阵上用linprog优化portfolio覆盖，保同样零类型限制、W1。浮点点转分母≤10⁷的Fraction；未精确可行/归一时用原cone.recover_vertex恢复活动行。只有精确非负/全IC/被禁类型为零才进整数clone。LCM缩放再GCD约简得不同单位客户，`independently_verify`按全部有序历史直接收益比较，另用规范verify_certificate核完整证书；该后者不调用全集SPE solver。Instance.optimal_welfare枚举至多m个主题支持给静态OPT。程序没有恢复全局MILP最优对偶，也没有给此碰撞自由固定锥的最优对偶；exact endpoint是**一个可行点**。

输出报告4根字段scope、parameters、milp_proposal、exact_endpoint。endpoint若有，含W/OPT/ratio/instance/strategy/all_history_verified/objective；objective是指定portfolio归一值，ratio是实际OPT/W，不可一般混同。--out会直接覆盖目标文件，stdout仅milp及endpoint四标量。原码/依赖中项目Git调用只在其它main分支；本批从未运行任何main、solver或Git。

## 两个有限尝试分别保真

552B `cf_m4p7_failed.json`全部5根字段：scope=`failed finite candidate generation only; no SPE result or numerical upper bound`；parameters为players4/topics7/seconds70/actual_path[0,1,2,3]/portfolio[3,4,5,6]；outcome说继承metadata在MILP后float(None)，未保存report或action graph；corrective_change说mip_gap guard已修且未重跑；mathematical_conclusion=null。

这是失败经过的历史文字记录，不是候选、精确证书、数值上界或任何策略不存在性。**当前冻结3094B源码已含guard替换**，不能说其未经修订的当前字节又发生同一失败；报告也未绑定发生失败的前版源码SHA/argv/日志。

相关而非本批primary的6202B `cf_m3p6.json`全文旁读保全。parameters m3/p6/seconds50/out原相对路径；milp status1、HiGHS timeout、variables579、binary_actions258、constraints4438、seconds50.04504197900002、floating_objective1.0000000000000182、floating_mip_gap1.2126563649742048、floating_bound_not_a_certificate=true。endpoint W3/OPT3/ratio"1"/objective"1"/all_history_verified=true；六名各只喜欢一个不同主题的单位客户，actual root计数(1,1,1,0,0,0)。完整策略有43条有序history行动表，原样保存，不将相同计数历史合并。

该单例输入的每个规定行动都是尚未使用标签；完整表的根/次位规定后终局都选三个不同标签，当前收益1达到一客户主题上界，末位在任意重复历史仍选未用标签取得1，给这个有限策略的直接解析核对。它不验证其它客户重数/策略，更不将timeout排成ratio≤1的区域结论。本次不重跑曾经低信息的两个搜索或原定义级SPE检查；历史报告未绑定代码SHA，保持其原记录身份。

## 依赖、原审查与未付义务

必要canonical joint/LP两模块本次正常show全文读；它们的已清洗[固定策略锥资源](../../../../state/计算/固定策略锥精确证书与重放--计算.md)已分开固定锥精确证书和浮点联合搜索。运行树另从该已发布证据同SHA复用credible_variants及customer_attraction四模块，所有原字节和来源指纹保全。当前全文读__init__/model/certificate；exact.py与credible_variants只作既有清洗依赖保全，不冒本次重新全文审查或额外done，wrapper也不调用其其它求解main。

34957B六主源、相关README/m3报告/两canonical模块、原审查先验、所有输出字段与状态均已有归宿；完整claim/manifest/relations/静态自查见证据。没有新数学入口或实验。一般共同终局见证/匹配覆盖遗漏集仍未证，失败模板也未给六人half反例或一般collisionfree上界。
''')

save('审查/共同终局交换的读后重构与负载推广范围--审查.md','same-terminal-exchange-read-after-source-review-and-extension-scope','review','审查','共同终局交换的读后重构与负载推广范围','historical-informed-internal-review-reconciled;local-results-proved;no-external-review','保存父方先读作者后重构、独立提出实际拥挤推广的真实时序；相同终局不是任意置换，条件匹配和模板障碍不升级为一般福利界。',['parent/common_terminal_exchange_review.md','credible/common_terminal_exchange.md'],r'''
# 共同终局交换的读后重构与负载推广范围

3454B父审明确记载：root**阅读作者common_terminal_exchange.md后**从定义重构，原稿不是盲审；负载推广由root独立提出。10228B作者稿则记root先核§1和多惩罚论证、建议§2，另审正在准备。本批读到的父审补足这个历史文件身份，不把它重命名为外审、盲题发现、新颖性或程序独立运行。

审查真正确认[交换引理](../引理/共同终局交换与负载匹配的条件福利证书--引理.md)的三步：原h真偏离IC、单位玩家同b同q利润相等、给定有序末节点g的真BR。只同福利不够；任意终局置换或另一SPE可达也不够。同计数不识别策略，g必须属于同一完整σ，所有平局仍保留。

父方提出的推广把无拥挤S_h大小换成实际u_h：1/(1+c_g)≥α/c*于S_h，E_h完全actual-fresh且在g负载0。匹配相加使Σ|E_h|≤(1−α)Σu_i，若覆盖最优遗漏才得OPT≤(2−α)W。α1/2、c*=1恢复旧特殊形式，是**假设推广**而非换成加权模型；α0没有让见证、匹配或遗漏覆盖自动存在，I空/零W亦无比率除法。

[多惩罚外组门槛](../障碍/共享终局多惩罚扩张的外组末位门槛--障碍.md)依同终局两枝与外组保持单C，k≥2用无不动点置换给半组预算；k1没有此结论。违反参数被两条必要比较排除，不要求假装未指定子树已是SPE。与既有[单惩罚完整归纳族](../../../../state/反例/三人碰撞自由族福利障碍--反例.md)全文比较后，原存在型趋3/2构造保真，但其多惩罚literal t>2不是另一份有效SPE。

本次从原定义知情重构、比对全部源和后续正式对象，未发现上述局部解析证明缺口。局部审计14cases/352标量与无结果MILP各自保存为[资源](../资源/共同终局局部审计与碰撞自由联合锥的有限记录--资源.md)，不把有限pass、metadata失败或ratio1点当一般上界。可接续方向仍是找足够多真实共同终局转移及负载匹配，或打破模板共享多重集/外组不变结构；这是一项未证明适用性义务，不是新的六人福利关系。
''')
print('wrote four formal objects')
