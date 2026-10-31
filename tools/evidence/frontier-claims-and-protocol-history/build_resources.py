"""New frontier historical resources; no legacy program import or execution."""
from pathlib import Path
import hashlib, json, re

E=Path(__file__).resolve().parent
S=E.parents[2]
F=S/'archives/weighted-congestion/state/资料'
F.mkdir(parents=True,exist_ok=True)
sources=json.loads((E/'source-manifest.json').read_text())
by_id={x['id']:x for x in sources}
claim_id='2f4a0833cc651ca428c8'
claims=(S/by_id[claim_id]['saved_path']).read_text()
lines=claims.splitlines(keepends=True)
formal=[]
segments=[]

def dump(p,obj):
    p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')

def write(name,ident,summary,ids,body):
    meta={'id':ident,'kind':'resource','type_tag':'资料','title':name,
          'status':'historical-primary-fully-read-with-explicit-version-and-mathematical-scope',
          'summary':summary}
    refs=['source:'+z['commit']+':'+z['path'] for i in ids for z in by_id[i]['sources']]
    refs=list(dict.fromkeys(refs))
    text='---\n'+''.join(k+': '+json.dumps(v,ensure_ascii=False)+'\n' for k,v in meta.items())
    text+='source_refs:\n'+''.join('  - '+json.dumps(x,ensure_ascii=False)+'\n' for x in refs)+'---\n\n# '+name+'\n\n'+body.rstrip()+'\n'
    assert not any(ord(c)<32 and c not in '\n\r\t' for c in text)
    p=F/(name+'--资料.md');p.write_text(text);rel=str(p.relative_to(S));formal.append(rel);return rel

base=r'''以下完整保留冻结 `research/weighted_congestion_frontier/CLAIMS.md` 的原陈述。它是精确数学身份、域、量词、依赖、证据、异议和状态的账本，不是本批重新证明全部被链论文。原作者的“完整证明”“内部审查”按其历史版本和实际覆盖理解；Paper Fact、候选、条件成立及有限证书不自动同级。原文中的相对链接只在原目录解释，故用完整原文块保留，原路径/标签不误绑到新资料目录。当前纠正及相关实际比较见[总合同](拥塞命题账本与协作协议的版本合同--资料.md)。

统一MODEL只作已经明示的共同背景：有限玩家与资源、每玩家正实权、有限非空资源子集动作族（可有空动作）、非负系数次数至多d的资源费用；普通成本为所用资源费用之和，偏离后重算包含自身的真实负载。α-PNE采用所有真实单方偏离的弱不等式，不算0/0。各条附加条件仍按原文逐条保留，不因这一背景删除。step依赖模型和正占用核是另外对象，须另证迁移。
'''

specs=[
('拥塞全类目标与早期源包络账本的全部陈述',1,248,r'''本段区分全类a_*(d)、文献Paper Fact、奇环增长族、既有源公式、三载荷基础工具、二列端点和稀疏权谱。开头已经登记线性全状态族否定全类Cd/ln d；“长期精确阈值尚未刻画”与原判定义务已否定可以同时成立。文献d上界、人数n界和旧Ω(√d/log d)族的团队未重构事实不能由后来的局部审查倒填。

源F_d是特定四参数两攻击的sup，参数游戏可随α变化；没有sup取得假设，也不等于每个源游戏的真实最优均衡倍率。LF-SHARP的旧candidate与R3的后续完整锐渐近分开保留。三点非负多项式的相邻单项式包络只优化三个载荷，不是均衡阈值。DAG阶跃在原辅助费用模型成立，其多项式端点或平台模拟还需新条件。'''),
('拥塞有限分离与奇环证书账本的全部陈述',249,450,r'''固定32次14资源全状态反例、把同一权/幅度直接升幂的失败、缩权重调幅的序列与其选定偏离锥是四个不同命题。度40出现9/5-PNE并不反驳重调权族；一个有限分离不能承担增长量词。Shapley字典的坏最小点可以与精确PNE并存，潜在用户填充可改变密度参数而保持原均衡。

奇环的两严格局部测试 iff 是正系数证书可行性，测试失败不自动给实际PNE。多项式混合保同动作副本/群内同费时仍是同一个T_d证书包络；单light的实际min{2,T_d}上界是另一个结构定理。后续一般cohort实际T_d上界在下一段后的新身份闭合，不删除早期证书/单成员的精确限制。'''),
('拥塞结构势与规范形账本的全部陈述',451,672,r'''要求全部改善边下降的序势、仅让某个全局最小点稳定、资源边际夹逼与存在PNE是不同量词。全动作2^E允许全空精确PNE，仍可有严格改善环，故方法障碍不等于全状态无均衡。资源签名与degree局部维数是固定模板的表示界，不提供无界玩家/动作族的统一规模截止。全状态selector的dual须保其支持/真实边，不可用任意局部一致矩替换。

整数单位单项式规范形依有限严格余量，其反例存在等价不保证保持原实例β、资源数或一般算法效率；全类端点闭性不表示有单游戏取得sup。密度/份额、尾部、两权/有限权类的势各带不同参数。A_(d,k)<d对每个有限k成立，固定d时k增大趋d，不能把固定k的o(d)推广全类；不过逐有限游戏取其实际k可以给d-PNE存在，这一准确推论在总合同解释。'''),
('拥塞时钟与局部矩账本的全部陈述',673,844,r'''严格双扫环可以经锚定时钟编译成全状态无α-PNE，但时钟次数要支付完整成本B、真实余量η和全部非法态；没有统一跨实例的次数效率。三次保次数失败、统一低泄漏预算非必要、43次稀疏证书和80次完整uniform证书是不同对象，均不宣称最优次数。保front的相位商和端点差不自动保证全部front有出口。

身份子集的局部成本压缩保所有状态/偏离成本，不保原资源或算法效率；暂态dual可行不表示暂态必要。异权全成本刚性是有限非负表示锥的射线/支持结论，既不排改变玩家/权/标签的均衡lift，也不排≤D资源数量压缩。奇环dual的无界mover支撑是特定selector合同，不是无PNE族。'''),
('拥塞共享侧资源与正占用核账本的全部陈述',845,1053,r'''共享侧资源的v1/v2/v3依次改变强迫/目标倍率条件：(τ−1)(α−1)≥d、α(τ−1)≥d、ατ≥d；UFτ、同权hub、唯一source、同费副本等共同域仍保留，旧版本不覆写。τ=d是保证精确PNE的限定子类锐边界；不能由α=1反例把一般α>1乘积条件称必要。异权hub再需要局部R/K，原降序势的坏全局最小点并不否定别的选态或PNE存在。

PK交互秩暴露面、锐坏项质量、Euclidean闭锥是正质量/非负有限占用核的独立代数工具，闭包新增对象不能冒充有限表示，也没有免费均衡桥。潜在使用森林给存在但不保证FIP；一条圈秩1固定反例不刻画所有单环。条件front编译须全部front出口，后续健康族另供增长输入。一般cohort奇环T_d实际阈值闭合早期“只有证书上界”的缺口，但仍是指定奇环拓扑。'''),
('拥塞全状态与决策重建账本的全部陈述',1054,1325,r'''健康双扫环、全部front出口、非法态修复及同次数预算共同证明每p≥2^20全状态严格p/10改善，进而否定任何固定C的全类Cd/log d存在保证。早期单环或有限代码不是这一推导的前提替代。后续近一次数和加性平方对数缺口使用独立版本：固定n阈值不能代入n(d)，局部收缩不能代替全状态构造。

决策器的YES、精确接口NO、UNKNOWN与原游戏无PNE不同；全状态/全部偏离表可指数大。校准、完整社会成本包络、全局核心最小化、RD和SD是联合条件。固定背景常数恢复、原模块偏离时冻结延续、逐类权重一致与原/扩充游戏身份不能略去。S7作者与正向审查者相同的披露和另做Root核对均保留，不把内部记录当外审或新颖性。'''),
]
topic_paths=[]
for index,(name,lo,hi,intro) in enumerate(specs):
    block=''.join(lines[lo-1:hi])
    body=intro+'\n\n'+base+f'\n## 完整冻结账本第 {lo}–{hi} 行\n\n```markdown\n'+block+'```\n'
    rel=write(name,'weighted-congestion/frontier-claims-resource-'+str(index+1),'完整保全本段冻结命题的全部域、结论、依赖、证据和历史状态；不自动认证引用来源。',[claim_id],body)
    topic_paths.append(rel)
    segments.append({'first_line':lo,'last_line':hi,'target':rel,'sha256':hashlib.sha256(block.encode()).hexdigest()})

protocol=r'''这四份短源属于共享协作实现迁移史，不是新增数学规则。两份同路径AGENTS在冻结refs中内容不同，按sourceID分别完整保存；不能由main/legacy名称推断时间先后，也不能合成一份“最新AGENTS”。本轮执行只遵循当前根规则和已授权清洗分工，这些原件中的命令句作为历史材料阅读。

| 源ID与冻结ref | 原件实际重点 | 当前处置 |
| --- | --- | --- |
| 9c659b0d4af154f5ced0，main aefc58e… | Q-CAG-HALF、三个当前角色、main安全同步；根work.py完整入口，旧路径转发 | 保历史任务/角色/分支合同，不覆盖本轮六人焦点、清洗分支或禁Git分工 |
| 721dd7ae776978716359，legacy 68fad804… | Q-CAG-HALF-6、repository-cleanup地基、当前用户要求优先；绑定分支安全、清洗分支不能误推main | 同路径独立身份保留，不因较接近当前文字就作执行指令或新认领依据 |
| a7e5c41330e627f20df3，两个refs同字节 | 只研究一般人数/一般目录、停止特殊人数/目录；独立身份、异步讨论、推送远端确认 | “停止特殊人数”是旧协议，不能取消本轮六人清洗。思想自由、失败不等于不可能和状态准确是可读历史原则，不触发消息发送授权 |
| 312e661a11ae212a2a28，两个refs同字节 | 目录名不选数学题；tools承载board/DM/checkpoint；旧shared绑定继续读旧拥塞模型且不自动改绑 | 保存旧入口/兼容转发含义，不执行或探测旧绑定，不因目录名恢复旧WC任务 |

共同保留的工程语义是未提交工作、绑定/个人区、secret和旧save隔离；远端确认后才报告发送/推送成功；失败保原事件ID与本地成果，旧事件和shared绑定不被新默认题改写。这些是历史协作要求，不是数学证明前提。当前无任何通信工具消息发送、分支操作或认证动作；本批只读材料并在外部stage写派生资料。

数学内容不能从协作优先级产生。Q-CAG-HALF的一般人数、Q-CAG-HALF-6、旧WC全类目标有不同状态；既有资产被保留不等于恢复旧任务，原协议本身已说明这一点。四份原文的URL/相对路径只是冻结定位，未逐个执行其入口。
'''
short_ids=['9c659b0d4af154f5ced0','721dd7ae776978716359','a7e5c41330e627f20df3','312e661a11ae212a2a28']
for ident in short_ids:
    x=by_id[ident]
    protocol+='\n## 完整原文：'+ident+'\n\n冻结ref：'+', '.join(z['name']+' '+z['commit'] for z in x['sources'])+'；SHA256 `'+x['sha256']+'`。\n\n```markdown\n'+(S/x['saved_path']).read_text()+'```\n'
protocol_path=write('共享工具协作协议的双版本与任务迁移','weighted-congestion/frontier-protocol-two-agent-versions','四份旧协议全原文及两个AGENTS独立版本；旧任务/角色/命令不覆盖当前清洗。',short_ids,protocol)

contract=r'''本批五源已经完整实读：CLAIMS全部230169字节/1325行，另有四份短源（含同路径两个AGENTS）。本对象保存账本的精确数学/状态合同和协议迁移史；它们不是新数学证明，也不是新执行规则。没有Git、claim/done、旧套件、网络、PDF/浏览器或mapper操作。全原文按下列六段无损进入资料，所有候选、条件、文献、证书与独有反例边界都保留。

## 版本、原件和去向

CLAIMS、PROTOCOL、README在legacy-cleanup 68fad804ec5946cb296f77dc5b336308a66abf12与main aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c字节相同；两AGENTS各只属于其列出的冻结ref。原件以sourceID分目录，避免同路径覆盖；source-manifest完整保存commit/path/blob/SHA。
'''
contract+='\n| 源ID | 路径 | 字节 | SHA-256 |\n| --- | --- | ---: | --- |\n'
for x in sources:
    contract+='| `'+x['id']+'` | `'+x['path']+'` | '+str(x['size'])+' | `'+x['sha256']+'` |\n'
contract+='\n'
for path in topic_paths+[protocol_path]:
    contract+='- ['+Path(path).name[:-3]+']('+Path(path).name+')。\n'
contract+=r'''

## 原账本的作用和身份覆盖

账本有130个二/三级标题，其中125个以WC/WCF/OC/PK/R3身份命名。R2方法资产段另合列WC-R2-RESOURCE-POWER-BRIDGE、WC-R2-POWER-PATH-OBSTRUCTION、WC-R2-AFFINE-TWO-TYPE三个身份，没有各自标题，不能把125当全部命题ID总数。实际逐ID标题与同SHA旧graph和五轴review比较，有121个精确对应标题身份（其中4个graph kind=lemma，其余117个claim）；合列三身份也分别在图/五轴中，去向保在原段。旧WC-TARGET和三个WC-LIT条目不在该精确ID集合中。这里不造近名映射；四者的原身份、域与Paper Fact边界完整保存。五个非命题标题及开头/状态使用段同样保全，不以计数代替全文。

1. 账本开头WC-TARGET保留长期刻画a_*(d)的身份，并已登记全类Cd/ln d及所有o(d)保证被线性全状态族否定。逐条旧“Ambition全类OPEN”“没有缩小d/log d与d缺口”等，是早期时态，不能使已否定的原判定义务重新开放。精确有限d最优门槛仍不因此闭合。
2. 条件定理可以有完整证明，但其UF、全front出口、共同尺度、给定真实输入或全局最小点等假设仍是共同前提；current_proof=complete不等于该接口能免费应用全类。Methods/Value/Mechanism/Ambition、内部审查与外审也不是同一个数学轴。
3. 原账本要求缺失resource_cone/review.md、nonseparable_frontier/proof.md等只登记缺口。本批保留作者当时未取得事实；不借后来的独立证明宣称旧缺稿已找回，亦未为这些路径作新的可取得性断言。
4. WC-LIT-UPPER-D、WC-LIT-LOWER、WC-LIT-N保作者Paper Fact及未重构范围。没有新下载/阅读外部论文，不以书目/摘要的存在替代全文认证。文献sup、某固定参数实例、固定n和任意n的量词仍分别保留。

## 两个候选标签的实际后续比较

冻结五轴在本批121个精确对应ID中，119个current_proof=complete，另WC-R1-LF-SHARP和WC-R1-THREELOAD-ENVELOPE两条为candidate/internal_review=candidate。完整CLAIMS第120节标题自身也保LF-SHARP候选，而三载荷段称完整一般证明已完成；这两个标签不能只凭原账本自动升级。

本批实际全文读当前《两攻击源参数包络的锐渐近》，其自足证明明确把旧LF-SHARP与后续R3合在同一精确最终渐近之下保留不同推导来源：F_d∼(2/√e)√(d lnln d)/ln d。证明有整数floor/ceil合法下界、任意近sup序列定位与一维上界，以及另一候选的y坐标全域粗界/三域一致引理。参数sup未假设取得，真实源状态的两指定攻击只给保守证书，不等于每实例minimax。现正式证明/独审是后续实际数学，不是把旧candidate字节改成“当时已审”。

本批亦实际全文读《非负多项式三载荷精确包络》与《三载荷包络的独立审查范围》。给0<L<H<U、非零有限非负系数多项式和0<ε<1，归一化q_k=a_kH^k/p(H)、r=L/H、s=U/H。选择r^(n+1)≤ε≤r^n，θ=(ε−r^(n+1))/(r^n−r^(n+1))，负斜率相邻网格弦使p(U)/p(H)≥θs^n+(1−θ)s^(n+1)，等号恰为相邻两单项式的正倍数；最小次数ceil[ln(1/ε)/ln(H/L)]。此为完整现行数学与独审来源，不把冻结五轴candidate消去，也不声称博弈均衡门槛。源审查的11/(40δ)粗指数加强、m=2反边界和375例DAG旁证身份在已读正式页分别保存，未在本批重复旧成功运行。

两条的资源去向只保存精确版本差别，不回写他人正式页或冻结五轴表。当前比较快照和实际读范围以comparison-manifest为准；没有用“教材/当前标题”代替证明阅读。

## 从线性下界到近次数：共同前提与规模

先前批次已经全文读、且本批复用同SHA的《全状态线性次数无均衡族》给每整数p≥2²⁰，全部纯状态存在margin≥(2^p−p/10)/8>0的真实偏离。健康环、全部front覆盖、非法状态修复和同次数整数预算是联合前提；不能以有限fixture或单条环代替。任意固定C,d0取p≥d0且lnp>10C，则p/10>Cp/lnp，同一族否定原普遍存在保证。这是解析量词比较，无新数值游戏试验。

较后近次数定理是新身份，不覆写旧d/10。已全文读当前《平方对数加性缺口的全状态近次数下界》：每d≥2²⁰，ell=ceil(log2d)、n=ceil[d/(1200ell²)]，直接重证n≥2、d≥8n、T>16nd和d ln(3/2)>200n(ln d)²，不能把n(d)带入只对每固定n证明的d0(n)。alpha=(1−1/n)d≥d−1200ell²，通常不等号；d=2²⁰时n=3，alpha=2d/3而展示倍率568576。全状态构造仍需其真实资源、全front和非法态证明，不由ceil核验独立产生。

固定c时先固定n，权深O_c(ln d)；可变n(d)时g=O(d/ln d)、lnN=O(d)，整个显式游戏巨大。单个权分母或系数的O(d²)位长不等于整个游戏表多项式规模。原账本已经写不承诺高效构造，本资源不把“有理可表示”升级成总位多项式。

## 正向d上界的透明局部推论

本批全文读当前《有限权类别三角排序势》后可以作如下**直接归纳推论**，不是新外部论文认证：d≥2的每个给定有限MODEL游戏若有可动玩家，只有有限实际可动权值数k≥1，A_(d,k)∈[1,d)唯一满足A=Σ_(j<k)((d−1)/A)^j。跨全部资源同一玩家尺度h_i的势边际夹逼给势差≤h_i[A C_new−C_old]，有限状态最小点是A-PNE，于是也是d-PNE。无可动玩家时唯一状态精确，不定义A_(d,0)。逐游戏取各自k即可，不需要全类共同有限k上限；d=1的仿射精确势、d=0的常费用各自另证。

与近次数下界联合，在该内部证明接口下得到1−1200ceil(log2d)²/d≤a_*(d)/d≤1，因而极限1。此处只把已读正文的共同前提接起来解释账本中Paper Fact上界的作用；不宣称有限d阈值等于d、某有限游戏取得sup、算法能有效找全局最小点或全球新颖性。较弱自足资源幂矩上界d+1也足够给同一极限，二者不冲突。

## 确切可回收内容与不能越过的边界

六段账本保全部独有数值/公式/反例：三人二次286/267与源19/18的有限分离；32次14资源与升幂失败；全状态/actual-topology/sup端点的奇环区分；全空精确PNE与高倍率改善环并存；统一低泄漏(U)充分而不必要的80/91及稀疏43次证书；依真实余量的时钟次数；有限签名/局部矩/暂态概率dual的支持量词；UF多版本、α1精确强迫边界和异权R/K；PK有限锥与闭包；森林存在与圈秩1反例；校准NO和UNKNOWN；社会OPT与完整基线；RD/SD/全局最小化联合条件。完整陈述不由这些导读句替代。

S7披露作者与正向审查者相同，另有实际Root重构；内部自查和外部同行评审分开。论文/PDF导航不表示本批读过相应PDF。原代码/冻结运行的历史成功只作来源事实，本批不重新运行已有成功suite；也不声称列出的所有软件已在当前环境认证。当前三阶段要求不强制图连通，不沿用旧规则或创建mapper关系。

## 真实读取和自查范围

全部1325行依连续1–110、111–250、251–390、391–530、531–670、671–810、811–950、951–1090、1091–1210、1211–1325实际读取，无未读尾部或被截断主源段。只有已全文读过同SHA catalog中的精确路径用Cn缩写，所有名称、数学、状态及未命中路径原样完整输出。四短原件一次完整读完；两AGENTS未覆盖同名文件。

新检查仅限原件inventory SHA、全部行/标题无损去向、121精确身份对照、五receipt和正式页C0/行尾空白。计数不证明阅读或数学；人类实读范围与工具结构检查分别记录。没有旧程序执行、共享结果覆盖、Git/新network、PDF/视觉PASS、外文认证或额外done引用来源。
'''
contract_path=write('拥塞命题账本与协作协议的版本合同','weighted-congestion/frontier-ledger-protocol-contract','五源全文去向、两个AGENTS版本、候选/历史OPEN/后续证明与软件范围准确分离。',list(by_id),contract)

dump(E/'formal-manifest.json',[{'path':p,'bytes':(S/p).stat().st_size,'sha256':hashlib.sha256((S/p).read_bytes()).hexdigest()} for p in formal])
dump(E/'resource-targets.json',{'claim_topics':topic_paths,'protocol':protocol_path,'contract':contract_path})
dump(E/'line-dispositions.json',segments)
print(json.dumps({'formal_files':len(formal),'formal_bytes':sum((S/p).stat().st_size for p in formal),'claim_lines':sum(z['last_line']-z['first_line']+1 for z in segments)},ensure_ascii=False))
