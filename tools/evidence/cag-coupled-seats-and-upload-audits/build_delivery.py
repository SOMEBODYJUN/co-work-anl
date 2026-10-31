"""Build semantic resources and receipts; never rerun original auditors."""
from pathlib import Path
from fractions import Fraction
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[3]
E = ROOT / 'tools/evidence/cag-coupled-seats-and-upload-audits'
W = ROOT / 'cleanup/workspaces/Boss4/r3-cag-coupled-seats-and-upload-audits-next'
W.mkdir(parents=True, exist_ok=True)
sources = json.loads((E / 'source-manifest.json').read_text())
deps = json.loads((E / 'dependency-manifest.json').read_text())
byid = {x['id']: x for x in sources + deps}

def dump(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')

def doc(path, ident, title, summary, ids, body):
    refs = [f"source:{s['commit']}:{s['path']}" for i in ids for s in byid[i]['sources']]
    head = ['---', 'id: ' + json.dumps(ident), 'kind: "resource"', 'type_tag: "资料"',
            'title: ' + json.dumps(title, ensure_ascii=False),
            'status: "full-primary-read-with-exact-domain-and-provenance"',
            'summary: ' + json.dumps(summary, ensure_ascii=False), 'source_refs:']
    head += ['  - ' + json.dumps(ref) for ref in refs]
    text = '\n'.join(head) + '\n---\n\n' + body.strip().replace('§', chr(92)) + '\n'
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text)
    return {'path': path, 'bytes': p.stat().st_size, 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}

seats = r'''
# 真实前缀席位与随机索引交换的两份审计

主源311146e332d3bac3e525（prefix_coupled_seats.py，6583B/124行，SHA1bde7f71…）和24f446797606924d0916（random_position_exchange.py，3691B/94行，SHAe4435ad0…）两冻结版本同字节，全部原代码实际读完。[原件/完整来源](../../../../tools/evidence/cag-coupled-seats-and-upload-audits/source-manifest.json)与真实输入、完整新旧报告分开保全。两程序均仅导入标准库Fraction，不导入作者脚本、模型或均衡验证器；有限数据不替代一般席位证明，也不产生六人half反例。

## 124客户原输入没有策略：如何补全而不偷换

prefix默认只读examples/customer_attraction/prefix_coupled_seats_strict.json（源6d08e55bce1a5336932c，1486B，SHA8fa88f66…）。其中只有实例、目标路径和数值声明，没有完整策略。三名单位提供者、五个共同主题标签0–4，十一种客户兴趣和单位重数为

| 兴趣主题 | 重数 | 兴趣主题 | 重数 | 兴趣主题 | 重数 |
| --- | ---: | --- | ---: | --- | ---: |
| {0} | 15 | {1} | 14 | {2} | 14 |
| {0,2} | 11 | {3} | 15 | {0,3} | 14 |
| {2,3} | 3 | {4} | 9 | {0,4} | 5 |
| {1,4} | 13 | {2,4} | 11 | | |

共124名不同单位客户，重数由range展开，不是有权客户或玩家。真实目录客户集由这些单位编号重建。source raw的目标是(0,4,2)，W95、new127/2、old_combined184/3、gap13/6；全部三条claimed rows实际读完。程序不是通用健壮schema验证器：例如负重数range会丢单位，rows比较使用zip且不独立断言任意输入的行数；本次真实合法输入的类型/全部三行另作明确检查。

对每个有序历史h递归保存所有可实现纯SPE终局M(h)。叶为自身；当前收益门槛是max_a min_(z∈M(ha))u_current(z)，保留达到该门槛的全部行动孩子终局。必要性来自每个偏离子树的最低可实现收益；充分性来自彼此不交的有序子树可独立选最低收益续局。因此本有限菜单未把等计数历史强绑同一平局。

先核目标属于根菜单，再递归build：在指定行动保留目标，其他行动孩子按“当前玩家收益、终局字典序”最小者选完整续局。得到根0；第一步0后第二人4，否则第二人0；全部第三人动作表为

| 首/第二行动 | 0 | 1 | 2 | 3 | 4 |
| --- | ---: | ---: | ---: | ---: | ---: |
| 0 | 4 | 2 | 4 | 4 | 2 |
| 1 | 2 | 0 | 0 | 0 | 0 |
| 2 | 4 | 0 | 0 | 0 | 0 |
| 3 | 4 | 0 | 0 | 4 | 0 |
| 4 | 2 | 0 | 0 | 0 | 0 |

直接沿这同一完整策略重算全部31有序历史/155含自身比较，124非自身偏离，最小slack0，121严格/34平局（其中31自身比较）；不是严格SPE。实际利润(37,30,28)，和为W95；穷举5³终局，OPT100由(0,1,2)达到。

## 新旧席位谱真正比较了什么

五主题覆盖两两不同且均极大。全局私有块大小(15,14,14,15,9)，实际根覆盖C遗漏的私有块D_a大小(0,14,0,15,0)。旧静态席位为|D_a|/s+|S_a−D_a|/m，s=1至m、m3；15个降序值为

62/3，55/3，15，15，15，79/6，13，13，13，38/3，38/3，38/3，34/3，32/3，9。

实际位置i（从1计）、余r=m−i+1、真实过去负载b_x时，程序重算

$$G_{i,a,s}=|D_a|/s+§sum_{x§in S_a§setminus D_a}1/(b_x+r),§quad 1§le s§le r.$$

全部主题和席位联合降序的第r项为λ_i；direct_i=max_a Σ_(x∈S_a)1/(b_x+r)，old_rank是旧谱第r项，old_max=max(old_rank,direct)。实际利润逐位核u_i≥λ_i≥old_max。

| i/r | 实际u | direct | λ | old_rank | old_max |
| --- | ---: | ---: | ---: | ---: | ---: |
| 1/3 | 37 | 15 | 15 | 15 | 15 |
| 2/2 | 30 | 109/6 | 41/2 | 55/3 | 55/3 |
| 3/1 | 28 | 28 | 28 | 62/3 | 28 |

因此Σλ=127/2、Σold_max=184/3、差13/6；全部每主题G数组、排序谱和31动作保完整报告。它是一个真实单位玩家SPE与谱定义的有限比较，不是从三个位置重新证明任意m的席位定理；source scope明确不重新审核arbitrary-m证明。

main可--output，创建父目录后write_text会覆盖该路径，和其他审计的x拒覆盖不同；本批只给新外部路径，未覆盖旧证据。stdout仅摘要，完整报告另存。本批在全输入先读后新增原CLI一次exit0/0.067秒，完整新报告与旧5758B JSON每个字段相同，补上本代码/真实输入SHA绑定；[命令与报告](../../../../tools/evidence/cag-coupled-seats-and-upload-audits/runs/new-run-summary.json)不伪称旧source已带策略。

## 五客户交换反例：全部13动作和六个真实前缀

random审计内嵌三名提供者、互不交主题A={0,1}、B={2,3}、C={4}。根A；首位A/B/C后第二位分别B/A/A，全部末位动作如下：

| 首/第二 | A | B | C |
| --- | --- | --- | --- |
| A | B | B | B |
| B | A | A | A |
| C | B | A | A |

末位是最佳回复，可选已覆盖主题；AB后选B、BA后选A都是并列合法回复，并非“全部选择未覆盖主题”。直接核全部13有序节点39比较，实际ABB，利润(2,1,1)，W4；全部3³终局给OPT3=5，唯一最优支持{A,B,C}。

随机排列这个最优元组的**索引**并强制前两位，在原策略上继续，六结果为

| 强制前缀 | 真终局 | 首位/最新位收益 |
| --- | --- | --- |
| AB | ABB | 2/1 |
| BA | BAA | 2/1 |
| AC | ACB | 2/1 |
| CA | CAB | 1/2 |
| BC | BCA | 2/1 |
| CB | CBA | 1/2 |

所以E最新=4/3，而全部前缀利润恒3，E前缀/2=3/2，差1/6。随机的是比较索引，真实策略仍区分位置和顺序；唯一最优支持/不交主题不产生交换性。

AB与BA的客户负载相同，末回复不同，末位收益都1、终局调和势都5。按位置看前两席在两叶恰同为(2,1)；按主题身份看A/B原持有者份额互换。合法一般结论只是同负载下末位最优值和最终势相同，不把末回复标签识别成同一个动作，更不能由此交换最新位与平均位。

源码还算真实uniform接口目标nOPT−(n−1)W−Σ_(i,j)V_ij=−4。原候选不等式为这个目标≤0，所以本例有正slack4，**不是uniform接口或half反例**。最大主题/安全值、随机前缀交换和全局覆盖是不同命题。

旧616B结果完整保存source_sha256恰等本e443…且没有项目代码依赖，本批准确复用，新增random原CLI0次；不把39比较和六排列重复计成新独立证据。两个现旧页“末位未覆盖主题”和AB/BA前两位置收益的措辞错误仅给[带旧SHA的修正建议](../../../../tools/evidence/cag-coupled-seats-and-upload-audits/suggested-existing-page-corrections.json)，不直接覆盖其所有权或旧source处置。
'''

priced = r'''
# 隐藏回复价格投影审计的真实行与有限域

主源b7956ea98f712cf7917f，tests/audits/customer_attraction_priced_hidden_reply.py，7053B/149行，SHA96b13737…，两冻结refs同字节；全文、实际参数、全部16目录和输出均已实读。直接依赖customer_attraction/priced_hidden_reply.py（a3926198d09da05d88b8，2908B，SHA3579b2ea…）也全文实际读完；包初始化所带model/exact/certificate四代码是此前完整阅读的相同SHA，已逐字节核复用。[全部原件与依赖](../../../../tools/evidence/cag-coupled-seats-and-upload-audits/dependency-manifest.json)保真实导入链，不隐去package初始化。

## 任意余尾的局部必要行及排序压缩

共同目录单位客户/单位提供者完整有序历史纯SPE。m人实际末位利润u_m、实际末前负载ℓ_x、目录最大客户数K。任一真实源h余k≥2人，源规定收益r；强制主题T后按同一策略的真实后继为F_1至F_(k−1)。令p_x为源过去负载，客户会员t=1_T、q=1_Q、隐藏位f_j=1_(F_j)，g=f_(k−1)、z=p+t+Σf。非负有理α、β、μ给逐客户函数

$$h(f)=§frac{t}{z}+§sum_j(§beta_j+§alpha_j/(§ell+1))f_j-§mu§frac{g}{z}+§mu§frac{q}{p+t+§sum_{j<k-1}f_j+1},§quad §psi=§min_f h(f).$$

零分子份额按0，非零分子保证其真实分母正。定义P_ℓ(F)=Σ_(x∈F)1/(ℓ_x+1)，强制分支的当前收益v_T、分支末位收益v_last，Q在分支末位背景上的查询值query。源IC、实际末位对每个合法F的查询IC、容量和分支末位IC给

$$r+(§sum§alpha_j)u_m+(§sum§beta_j)K-§sum_x§psi_x
=(r-v_T)+§sum_j§alpha_j(u_m-P_§ell(F_j))+§sum_j§beta_j(K-|F_j|)+§mu(v_{last}-query)+§sum_x(h(f_x)-§psi_x)§ge0.$$

源h可以离轨，r不是免费共用的实际根利润。每条u_m/K支出仍须由主证书共同计账；不同真实源的本行不能直接合成全局half。

核心实现令cost_j=β_j+α_j/(ℓ+1)，前k−2项排序，C_s为s最小成本和。固定末位位g和其他1位数s后，非线性只依赖s,g，最便宜线性和恰C_s，故

$$§psi=§min_{0§le s§le k-2,§ g§in§{0,1§}}[t/(p+t+s+g)-§mu g/(p+t+s+g)+C_s+cost_{k-1}g+§mu q/(p+t+s+1)].$$

2^(k−1)隐藏向量精确压成2(k−1)候选，包括k2无可排序早期后继。身份交叉项加入后须重证，不把按数量消元误作计数Markov策略。

核心_rational拒float价格，要求α/β同长度且非空、系数非负，所以本余尾语义至少k2。p/ℓ用isinstance(int)，会员位用0/1成员比较，并非处处type(...) is int；不要补称完全拒bool或所有浮点字段。实际审计全部传合法整数位和Fraction。projected是作者字面枚举，projected_by_count是排序；本独立审计自写literal_projection作字面枚举，仅调用后者比较，未把同作者两函数互相比当独立oracle。

## 3024参数槽与三组乘子

对k=2至10、三scheme、p=0至3、ℓ=0至6、t/q∈{0,1}，逐槽核自写字面最小值等于fast值，共3024。缓存可复用相同调用，计数是循环槽，不是不同完整SPE数。三scheme的j从0开始、n=k−1为

| scheme | α_j | β_j | μ |
| --- | --- | --- | --- |
| 0 | 前n−1项1/8，末项1/5 | 前n−1项0，末项1/20 | 1/4 |
| 1 | (j+1)/(j+3) | ((3j+1) mod5)/(j+11) | 2/3 |
| 2 | 全0 | 全0 | 0 |

这不是全有理乘子/无限horizon证明。旧计算页600组随机对照是另一条历史复核；原实现α必须非空，本页不把其中未保存参数释义的“k1”自动解释为支持余尾k1。

## 六人完整有序策略：每游戏一棵策略而非全部策略

solve_game按每个有序history递归比较所有行动的真实孩子终局收益，平局由SHA256(repr((seed,history)))前8字节mod平局数确定，故不同有序历史可独立选不同平局；只把终局支付按counts缓存。它生成一棵完整SPE，不枚举所有可实现完整策略或根菜单。

所有游戏四个具名单位客户，主题用四位覆盖mask。前十目录固定，后六由Random(6172026)按size2/3/4/4/4/4不放回抽样；每case tie_seed等其0–15索引。各目录标签覆盖不同，含空主题/全无兴趣有效覆盖0等边界；没有有限样本的重复覆盖标签案例。逐源节点仅history长度≤4（余尾≥2），末节点仍完整求解且用于真实末位IC，不能说所有六层都各有投影行。

@PRICE_TABLE@

合16棵完整策略、2664真实投影源、112794条(T,Q,scheme)必要不等式；所有最小gap0。每条按客户用真实followers计算h−ψ≥0，并精确核上述slack分解相等及非负。额外真实p可能达到4，参数网格p≤3不是游戏全部调用的截断；游戏检查仍对其真实负载调用字面oracle。

程序无argparse/output参数，main仅stdout完整JSON，不能把重定向惯例写成内置--output。此前6159B报告无该审计代码SHA绑定，本批在全部依赖实际读齐后新增原CLI一次，正常未优化-I/-B解释器，exit0/18.620秒，完整报告与旧JSON全部字段同。[新命令/报告](../../../../tools/evidence/cag-coupled-seats-and-upload-audits/runs/new-run-summary.json)明确代码及五实际代码依赖SHA；不从pass/16例推进为任意六人或任意目录half。

与21固定策略锥的全客户质量证书不同，本程序是具体四客户游戏上的局部行语义回归；与已证一般局部行的解析推导也不同。它不运行优化器、不发现共同K预算、不付款互斥子树、不引入阶段三边。
'''
price_result = json.loads((E / 'runs/priced-projection.stdout.txt').read_text())
table = ['| seed / 覆盖mask目录 | 完整决策节点 / 真源 | 投影行 | 实际六行动 |',
         '| --- | --- | ---: | --- |']
for game in price_result['games']:
    table.append('| ' + str(game['tie_seed']) + ' / ' + ','.join(map(str, game['catalog_bitmasks'])) +
                 ' | ' + str(game['complete_strategy_nodes']) + ' / ' + str(game['true_source_nodes_checked']) +
                 ' | ' + str(game['projected_inequalities']) + ' | ' + ','.join(map(str, game['actual_history'])) + ' |')
priced = priced.replace('@PRICE_TABLE@', '\n'.join(table))

nine = r'''
# 九人六极大算术审计的参数域和端点勘误

主源06319e5bab2a4043ed15，customer_attraction_six_maxima_nine_independent.py，2331B/52行，SHA7cfd7568…，两冻结refs同字节。全部代码/字面参数/输出实读，仅标准库Fraction，不读客户游戏、不构造SPE或优化器。NP21–NP25是来源标签，不是机器对任意人数证明的认证名。

## 全部有限域与可解析恒等式

n=2至500的499个δ比较令δ_n=2(n−1)/[n(n+2)(n+5)]，正通分母D=n(n+2)(n+5)(n+1)(n+3)(n+6)。源码逐项核

$$(§delta_n-§delta_{n+1})D=2(2n^3+7n^2-9n-18)=2(n-2)(2n^2+11n+13)+16>0.$$

右式解析上对全部n≥2正；有限扫描不是其全称理由。随后n=5至500、t=0至n−2共124744条私有系数检查，定义

$$A_t=§frac{n+t}{2(t+1)(3n-2t)},§quad A_{n-1}=1/(n+5).$$

核A_t≥1/(2n)的清分母差为

$$n(n+t)-(t+1)(3n-2t)=2(t-(n-1)/2)^2+(n^2-4n-1)/2§ge0.$$

末项n≥5也满足1/(n+5)≥1/(2n)。所以每个后缀最小值underline A_t=min_(q≥t)A_q仍≥1/(2n)，其n项和≥1/2；程序实际反向累积min并核该结论，不把后缀min误成逐项本来单调。

每个n另核共享系数

$$B_t=1/(3n-2t)§ (0§le t§le n-2),§quad B_{n-1}=(n+1)/[n(n+5)],§quad §sum_tB_t=H_n-§delta_n,§quad H_n=§sum_{r=1}^n1/(n+2r).$$

内部B递增，最后比较(n+1)(n+4)−n(n+5)=4>0，所以其后缀包络就是B。n5–500共496个恒等式；每n、s=1至6，仅t∈{0,n//2,n−2}取样核实际分母t+s(n−t)/2下的A/B≥统一六坐标系数，另核末项分母n+s−1≤n+5。不能把三个t取样说成全整数t扫描；一般分母支配由s≤6的代数直接给出。

## log3严格下界与两个不同half余量

变量log在代码里只是有限有理和1+1/12+1/80+1/448=7379/6720，没有数值调用log。解析上log3=2atanh(1/2)=Σ_(j≥0)1/[4^j(2j+1)]，余项严格正，故log3>7379/6720。凸函数g(x)=1/(3−2x)的复合梯形和给H_n≥(log3)/2−1/(3n)；这是已读数学证明，不是此脚本有限扫描或浮点算出来的断言。

δ_n随n下降，因此全部n≥9有

$$§mathcal B_n=H_n-§delta_n>7379/13440-1/27-16/(9§cdot11§cdot14)=665881/1330560=1/2+601/1330560.$$

代码另单独精确算B9=Σ_(r=2)^9 1/(9+2r)+10/(9·14)=229324183/456326325。因此

$$B_9-1/2=2322041/912652650,§qquad (665881/1330560)-1/2=601/1330560.$$

后者是统一解析下界的差，**不是精确B9的差**。现《极大关联前沿审查与七极大边界》§6混写了这两个标签；正确九人定理原正文已分清。新资源如上纠正，并给[最小替换与原页SHA](../../../../tools/evidence/cag-coupled-seats-and-upload-audits/suggested-existing-page-corrections.json)，没有直接覆盖Boss2页或重done旧来源。两数都大于1/2，定理本身不因标签勘误改变。

## 算术如何接入真正模型，哪些量词没有检查

现已实读[九人以上六极大定理快照](../../../../tools/evidence/cag-coupled-seats-and-upload-audits/context/archives/customer-attraction/state/定理/九人以上六极大强化覆盖界--定理.md)：n≥9提供者、不同极大覆盖数s≤6分别计数，有限共同目录/单位客户/单位玩家及全部有序历史纯SPE，允许空/重复/零客户/任意离轨平局。c是共同核心、P私有质量、V核心外共享质量、U全部极大并集。真实整极大偏离在无人同路由后继时给直接负载界；有同路由后继时由同终局子主题支配和后缀包络倒推给保底，最后才在实际路径求和得到

$$W§ge c+P§sum_t§underline A_t+V§sum_tB_t§ge c+(P+V)/2=(U+c)/2.$$

n≥9≥s使OPT_n=U，所以U≤2W−c。算术程序只核上文系数，不独立重演路由、全历史倒推或实例策略；其PASS不是单独完整数学证明。n9指玩家数而非九极大主题，不能扩到任意六人/任意极大数；n5–8的其他联合预算是不同对象。

顶层解析--output并立即执行检查，导入也有算术/参数副作用。输出可建父目录，x拒覆盖，stdout完整JSON。旧519B报告不绑定本审计代码SHA，本批必要新增原CLI一次exit0/1.348秒，124744/496/499及所有完整字段与旧报告相同；[新运行绑定](../../../../tools/evidence/cag-coupled-seats-and-upload-audits/runs/new-run-summary.json)明确普通未优化解释器，未把有限n2–500升级为全称证明或外审认证。
'''

uploaded = r'''
# 上传完整策略与四路微型比较的独立审计合同

主源9d31cb84f11929de63c3，tests/audits/customer_attraction_uploaded.py，18133B/348行，SHA b4f93f9ee4f6a05dd2139870e57b4034e1fdf1b26c69301a217adc5ed6dc17af，两冻结版本同字节，全部源码/实际输入/导入/元数据尾部实读。[主源与原件](../../../../tools/evidence/cag-coupled-seats-and-upload-audits/source-manifest.json)不改。

它有两部分：先从单位客户定义独立重放保存的四人全历史策略，再用微型完整策略oracle比较三种实现。前者不使用上传收益表/结果递推；后者故意导入比较对象。源码require主动抛ValueError，不受-O取消；但上传/规范/搜索依赖仍含assert，不能将一句require说明扩为整条导入链在-O下都同样验证。

## 全部真实依赖及输入身份

默认source-dir为history/source/notes/customer_attraction/uploaded_2026-10-10，需SHA256.json及其恰四项RESEARCH.md、exact_spe.py、auxiliary_counterexample.json、verification_report.json。逐文件读全字节并核manifest；状态文档/旧报告是hash依赖，不等于其历史“未同步/DNS失败”是本轮网络事实。四文件SHA分别ee53a931…、ab1ccf71…、be96cbb5…、e40dac2b…，清单自身c0ca4cf1…；[17依赖清单](../../../../tools/evidence/cag-coupled-seats-and-upload-audits/dependency-manifest.json)保完整SHA和原字节。

真实代码依赖包括上传exact_spe.py全300行、独立search.py全329行（只相关读取，不额外done）及customer_attraction包四源码，均完整实读或相同SHA的既有全文阅读逐字节复用。上传库依NumPy，搜索实现是Python整数LCM，不依NumPy。新环境仅只读查NumPy安装版本2.3.5，与旧报告相同；这不伪称新运行。

auxiliary JSON完整schema恰status/m/n/weights/target/policy；243955B包含4095非空兴趣类型、1885有序策略行。所有字段/参数/状态/目标和完整向量结构实际读取，全部整数保原件并检查合法；不冒称人工逐个数字读完，也不额外done该输入。mask键转int后再核不碰撞；n4、m12、正重数总26171145、最小1最大15091，目标计数在0、4、5、8各1。

DefinitionGame要求主题正整数、玩家非负整数、0<mask<2^m、重数非负整数，过滤零重数。它不接受mask0，无兴趣客户可在数学上忽略不等于这个API允许mask0；上传Game同样先查mask再去零重数，mask0即使重数0也拒绝。现旧《上传精确SPE脚本与个体安全压缩生成接续审查》把“空兴趣类型”写成允许输入，已给带旧SHA的建议纠正，未覆共享页。

DefinitionGame的终局计数API只核长度/总和，并不是所有直接调用计数的完整schema验证；本次counts均来自合法整数有序路径/组合生成器。每类型按分母分组累整数分子再造Fraction，等价于所有不同单位客户逐个均分。它仅给实际出现的主题计算该玩家收益；与上传表的比较也只检查occupied主题，不能冒称两个数组对所有未出现主题的“假想收益”逐格相同。

## 保存策略的定义级独立重放

策略每行恰history/action，历史和动作精确int且范围合法；要求全部长度0–3有序历史恰一行，无重复/遗漏，共1+12+144+1728=1885。terminal按完整有序prefix缓存，偏离后沿同一保存策略在改变历史继续。每节点规定收益与12行动比较，真实离轨也全部覆盖。

旧成功报告精确给22620含自身比较、20735非自身比较、6440零差（含1885自身）及最小正差1。仍有4555非自身平局，不是严格SPE。实际(8,4,5,0)，u=(6135345,6135380,6135380,6135371)，和为W24541476。

根行动0–3的真实续局(a,9,10,11)给6135344；4–7的(a,2,3,11)给6135342；8的(8,4,5,0)、9–11的(a,6,7,3)都给6135345。保存动作8最佳，但改动作后真实后继各自改变，未冻结在轨尾部。

独立穷举C(15,4)=1365终局计数求OPT24541532，唯一最优在0/1/2/3各1；穷举C(14,3)=364末位背景，逐12查询的最大值再取min，得θ=6135346，四个最小背景是从{8,9,10,11}任选三个不同标签。K=13088768；u1=θ−1，θ是min_纯背景 max_纯查询的末位最坏值，不能直接当真正max_混合查询 min_背景安全值v，故此审计只否定逐人θ桥。

实际W/OPT=6135369/6135383，2W−OPT=24541420>0。程序也主动require该half保持和两个静态θ下界θ≥OPT/(2n−1)、θ≥[2OPT−(n−1)K]/(2n)。这些是具体输入检查；RESEARCH另有静态覆盖代数和末两位势论证给原解析通界4(n−1)/[n(2n−1)]、n3时8/15，旧原程序27×128/100自测是另一组运行，不能加入本独立审计209例计数。

## 上传构造与有限实现边界

上传源把12标签分成三组各4，以每个子集在三组的计数定义desired势：子集大小3用SMALL，大小4用BIG，其他0。两个全部字面表如下（键为三组计数）：

SMALL={300:−17,210:−14,201:10,120:20,111:−15,102:−20,030:−16,021:−6,012:9,003:20}。

BIG={400:6,310:−13,301:−19,220:−19,211:−8,202:−1,130:9,121:5,112:4,103:4,040:−13,031:2,022:−16,013:−18,004:6}。

先对子集作Möbius差分得coeff，置sums_M=(−1)^(|M|+1)|M|coeff_M，再作超集Möbius反演得signed_M；offset=1−min_(M非空)signed_M=6391，weights_M=signed_M+offset。检查所有不同三/四标签子集的scaled harmonic势对应desired。最后真正整数客户Game求菜单和完整策略，不把有符号辅助势向量当合法客户输入。保存weights与这一确定构造重新生成的weights逐项相等，是旧同SHA审计的一项明确检查。

上传Game用Q=lcm(1,…,n)、NumPy int64稠密精确表；若总重数·max(n,1)·Q≥2^62或掩码数×终局数>20000000即拒绝。当前4人Q12、4095×1365=5589675，安全整数上界1256214960<2^62。实现内存/机器整数限制不是数学实例上限，也不是一般多项式算法声明。

outcomes(counts)保存全部可实现终局集合，阈值max_a min_孩子u_a，未强绑相同counts历史的平局。certificate按每个有序历史选支持target的最小合法动作，其他孩子用当前收益及计数字典序最低者；verify再走所有有序历史逐行动。上传main按此算法生成1885动作表；本独立审计只重新验证保存策略，不在本入口重生成后逐动作比较。因此不能拿“97根终局”代替完整策略。source audit还比较所有1365终局覆盖和所有occupied主题的Fraction收益，并核θ/OPT/target在根97菜单内。

## 209微型输入：哪些比较在根，哪些在前缀

direct_policy_outcomes真正展开单位客户，对每个完整有序历史策略映射自底向上核全部真实偏离，保接受映射数和根终局计数集合。输入为二主题三种非空兴趣重数各0/1/2（27个）分别n1/2/3，加三主题七兴趣重数0/1（128个）n2，总209。共14094完整策略映射、1350接受映射。

每个根把这个独立oracle与上传NumPy Game、规范Fraction ExactSPESolver、独立Python整数LCM search.exact_outcomes三者比较，故是四路根集合比较。另遍历所有前缀计数，**仅上传与规范**两者比较，共1793集合；没有把1793说成四路完整子局枚举。规范/搜索按counts缓存可能菜单仍保任意有序平局，其证明接口已读；这里只用搜索exact_outcomes，不执行其随机/穷举main或其Git metadata尾部。

旧有序输入与根集合digest为2d0e1942ec13c81c44515af0425a55817be01de64b2c293c2aeeb121b252fbc7。该有限回归不证明所有目录结果正确、全称SPE界或当前任意六人half。

## 旧成功复用和当前复现边界

旧6279B报告完整实读，audit_program_sha256恰等本b4f9…；input/上传程序/四原文件manifest及清单SHA都与现保存字节完全一致。因此本批准确复用已成功的大实例定义级审计，新增uploaded CLI0次，不重复无疑run。

旧报告保Python3.12.14、NumPy2.3.5、base commit8f9bcf4dc6743bbf08ac3283bfbbf33221516a15和全部209例结果；它没有单列search/canonical各代码SHA。本批将其保为当时成功tiny证据，不倒填成现各依赖代码都重新跑过的认证。

CLI支持--source-dir与--output，预先拒已存在输出；算完后才建父目录写报告并stdout。特别地math检查之后还调用Git只读rev-parse短ref8f9bcf4作metadata；新独立镜像没有那份Git历史，异地原CLI需真实该ref，不伪造ref、不动共享Git。既有成功足够，本批没有为已知metadata域再造一次后置失败；这也不是声称现在凭据或网络有问题。

来源文件的“clone DNS失败/未同步”仅保为旧上传包历史，本轮Boss串行发布是另一事实。外审/新颖性/普遍half均无新增认证，原件/旧页不改，相关依赖不额外done。
'''

formals = [
 doc('archives/customer-attraction/state/资料/真实前缀席位与随机索引交换的两份审计--资料.md',
     'customer-attraction/true-prefix-seats-and-random-index-audit-contracts',
     '真实前缀席位与随机索引交换的两份审计',
     '124客户原输入补全31节点SPE及谱比较；五客户13节点随机位置交换反例、正确uniform符号和末回复表。',
     ['311146e332d3bac3e525', '24f446797606924d0916'], seats),
 doc('archives/customer-attraction/state/资料/隐藏回复价格投影审计的真实行与有限域--资料.md',
     'customer-attraction/priced-projection-auditor-real-nodes-and-domain',
     '隐藏回复价格投影审计的真实行与有限域',
     '完整真实非负slack恒等式、三scheme/3024参数槽与16棵六人策略112794局部行；不作任意策略half认证。',
     ['b7956ea98f712cf7917f'], priced),
 doc('archives/customer-attraction/state/资料/九人六极大算术审计的参数域和端点勘误--资料.md',
     'customer-attraction/nine-plus-six-maxima-arithmetic-and-gap-label',
     '九人六极大算术审计的参数域和端点勘误',
     'NP21–25全部有限域与解析接口；私有包络/共享恒等式/log3下界、精确B9与统一下界余量分清。',
     ['06319e5bab2a4043ed15'], nine),
 doc('archives/customer-attraction/state/资料/上传完整策略与四路微型比较的独立审计合同--资料.md',
     'customer-attraction/uploaded-independent-policy-and-tiny-crosscheck-contract',
     '上传完整策略与四路微型比较的独立审计合同',
     '18133B审计及完整真实依赖/哈希链；四人1885历史的逐人θ反例和209根四路/1793前缀两路比较，准确旧成功复用。',
     ['9d31cb84f11929de63c3'], uploaded),
]
dump(E / 'formal-manifest.json', formals)

targets = {i: row['path'] for ids, row in [
 (['311146e332d3bac3e525', '24f446797606924d0916'], formals[0]),
 (['b7956ea98f712cf7917f'], formals[1]), (['06319e5bab2a4043ed15'], formals[2]),
 (['9d31cb84f11929de63c3'], formals[3])] for i in ids}
notes = {
 '311146e332d3bac3e525': ('124行主源码、1486B全部实际输入/声明行实读；无输入策略而补全31节点策略，菜单和真实全树比较/新旧席位谱全数学理解。', '一次新原CLI，完整报告与旧5758B每字段相同；限定单实例，保write_text可覆写与zip行比较边界，新输出仅新external路径。'),
 'b7956ea98f712cf7917f': ('149行主源码、2908B直接依赖全文、包四精确既读代码、三scheme和全部16真实目录/tie seed实读；字面min/排序与真实slack身份理解。', '一次新原CLI精确核3024槽、2664真实源/112794行，与旧6159B全文相同；每game一SPE、仅余尾至少2、不是任意策略/乘子或half。'),
 '24f446797606924d0916': ('94行主源码全部内嵌单位客户/13动作/六排列/势及uniform目标实读；末位可选已覆盖主题、位置与主题身份分清。', '旧616B sourceSHA精确e443且全stdlib无依赖，成功复用新run0；两个旧正式页措辞只给beforeSHA建议，不覆shared页/不复done其source。'),
 '06319e5bab2a4043ed15': ('52行主源码及全部字面n/t/s参数实读；private平方、delta因式、log正项/trapezoid及B9精确和的数学接口理解。', '一次新原CLI与旧519B全字段同；124744/496/499有限检查非全称扫描，n9玩家/s6极大分开；发现旧页把uniform gap混作exact B9 gap，给最小建议而不覆旧页。'),
 '9d31cb84f11929de63c3': ('348行主码、300行上传代码/329行search全部实际读；四规范依赖同SHA既读复用；完整证书字段/4095weights与1885policy结构、4文件hash依赖和旧6279B所有字段实读。', '同b4f9主源/完整四文件SHA成功run准确复用0新CLI；保真实定义级全树大例与tiny旧209根四路/1793前缀两路域、canonical/search旧SHA未单列及后置git refmetadata边界；不伪称新全stack运行。'),
}
receipts = []
for row in sources:
    i = row['id']
    receipts.append({'id': i, 'full_file_reviewed': True, 'related_material_checked': True,
        'unique_content_accounted_for': True, 'read_note': notes[i][0] + f" 原{row['size']}B与inventory SHA相符，两refs同字节。",
        'comparison_note': notes[i][1], 'decision_note': '全部独有程序/数学/输入语义归入自足资料；限有限、条件、历史与当前证据，不额外done依赖或改原件，不导阶段三图，不关一般六人half。',
        'disposition': 'integrated', 'targets': [targets[i]]})
dump(W / 'semantic-receipts.json', receipts)
dump(E / 'reading-scope.json', {'primary_files': 5, 'primary_bytes': 37791,
 'primary_actual_full_lines': [124, 149, 94, 52, 348], 'primary_line_sum': 767,
 'related_inventory_sources': 17, 'related_bytes': 328665,
 'code_dependency_reading': 'priced2908/whole uploaded12157/whole search16033 full actual reads; four canonical exact prior full reads reused by hash',
 'JSON_input_reading': 'all fields/metadata/case/policy meaning and numeric vector structure; exact old same-code big audit binds full certificate; not artificial human per-digit reading claim',
 'formal_context_full_actual_or_exact_prior_read': 10,
 'new_original_CLI_invocations': 3, 'new_report_scopes': ['prefix one real input', 'priced finite sorting plus16 m6 policies', 'nine arithmetic finite domain'],
 'old_success_reused_without_new_CLI': ['random exact code SHA/no project imports', 'uploaded exact audit/4 original file SHA chain; old tiny scope retained'],
 'existing_page_correction_suggestions': 4, 'shared_existing_pages_changed': 0,
 'additional_related_sources_done': 0, 'general_six_player_half_closed': False, 'phase_three_imports': 0})
(E / 'README.md').write_text('''# 前缀席位、隐藏回复、九人算术与上传审计五主源

5主源37791B/767行全文实际读完，17真实依赖328665B和10相关正式页实读/精确既读复用。三新原CLI均一次成功、完整JSON逐字段等旧；随机和上传各有同SHA成功链，准确复用不重复。四自足资料/五semantic receipts，有限/固定输入/旧tiny/current依赖与一般六人目标分开。

四项旧页问题只给beforeSHA+精确replacement建议，未改shared页/旧原件或额外done相关源：B9与uniform余量混标；mask0输入合同；随机末位误称全未覆盖；AB/BA按位置与按主题的份额混称。原件、代码、运行和修正建议都独立保存。
''')
(W / 'relation-review.md').write_text('''# 数学关系审查

124客户谱改进是一个完整三人SPE数值例；随机排列例只否定交换步骤且uniform接口slack仍正。隐藏回复行是有来源IC/共同末位价格/容量的局部必要式，16游戏不是任意策略证书。n≥9且s≤6的强化覆盖由解析包络/真实路由归纳承担，有限算术不是全称证明；上传θ反例又不等于真正静态混合安全值失败。

旧报告/旧缺入口/旧同步历史保持原时态；本批只建立阶段二正文和建议，不建图边、不重done旧来源，也不关闭任意六人half。
''')
(W / 'delivery.md').write_text('''# 精确交付

五主源/四自足资料/五收据/原件及全部真实依赖证据，copy-files.json按路径/bytes/SHA白名单交付。三次新原CLI与两份同SHA旧成功复用分开；四条旧页修正仅建议并带beforeSHA，原页未覆盖。
''')

checks = []
def check(label, ok):
    assert ok, label
    checks.append({'check': label, 'passed': True})
for row in sources + deps:
    raw = (ROOT / row['saved_path']).read_bytes()
    check('exact inventory bytes ' + row['id'], len(raw) == row['size'] and hashlib.sha256(raw).hexdigest() == row['sha256'])
claim = json.loads((E / 'actual-claim-receipt.json').read_text())
check('actual pushed Boss4 synced primary five', claim['status'] == 'pushed' and claim['actor'] == 'Boss4' and claim['local_sync']['status'] == 'synced' and set(x['id'] for x in sources) <= set(claim['ids']))
ready = json.loads((E / 'input-structure-and-run-readiness.json').read_text())
check('actual dependency/schema readiness', ready['status'].startswith('passed') and ready['all_related_JSON_fields_traversed'])
runs = json.loads((E / 'runs/new-run-summary.json').read_text())
check('exactly three new original runs', len(runs) == 3 and len({r['source_id'] for r in runs}) == 3)
for r in runs:
    check('new original successful report ' + r['name'], r['exit_code'] == 0 and r['stdout_bytes'] > 0 and r['runtime']['optimize'] == 0 and r['source_CLI_invocations_this_batch'] == 1)
comp = json.loads((E / 'new-old-comparison.json').read_text())
check('all three complete reports equal old', comp['all_passed'] and comp['prefix_complete_JSON_equal'] and comp['priced_complete_JSON_equal'] and comp['nine_arithmetic_complete_JSON_equal'])
old_random = json.loads((ROOT / byid['bd8eb256f44a2cc7e18c']['saved_path']).read_text())
check('random same SHA success reused', old_random['source_sha256'] == byid['24f446797606924d0916']['sha256'] and old_random['all_checks_passed'])
old_uploaded = json.loads((ROOT / byid['f1acdd55c80eb7a7df09']['saved_path']).read_text())
check('uploaded same audit code and input success reused', old_uploaded['audit_program_sha256'] == byid['9d31cb84f11929de63c3']['sha256'] and old_uploaded['input_certificate_sha256'] == byid['e19d793c64bcdc37ccd0']['sha256'])
check('priced finite exact domain', price_result['sorting_cases'] == 3024 and price_result['true_nodes_checked'] == 2664 and price_result['projected_inequalities_checked'] == 112794 and len(price_result['games']) == 16)
prefix_result = json.loads((E / 'runs/prefix-seats-report.json').read_text())
check('prefix source had no strategy, new full policy true scope', len(prefix_result['actions']) == 31 and prefix_result['comparisons_including_own'] == 155 and prefix_result['strict_gap'] == '13/6')
nine_result = json.loads((E / 'runs/nine-plus-arithmetic-report.json').read_text())
check('nine full finite arithmetic scope', nine_result['private_pointwise_checks'] == 124744 and nine_result['shared_identity_cases'] == 496 and nine_result['delta_difference_cases'] == 499)
check('exact gap separate from uniform gap', Fraction(nine_result['exact_B9']) - Fraction(1, 2) == Fraction(2322041, 912652650) and Fraction(nine_result['shared_uniform_n9_lower']) - Fraction(1, 2) == Fraction(nine_result['half_gap']))
corrections = json.loads((E / 'suggested-existing-page-corrections.json').read_text())
check('four suggested only corrections', len(corrections['proposals']) == 4 and all(not r['applied_to_shared_tree'] for r in corrections['proposals']))
for proposal in corrections['proposals']:
    saved = E / 'context' / proposal['path']
    check('exact before correction snapshot ' + proposal['path'], hashlib.sha256(saved.read_bytes()).hexdigest() == proposal['before_sha256'])
for row in formals:
    text = (ROOT / row['path']).read_text()
    check('flat MATEK ' + row['path'], all(re.search(r'^' + key + r':', text, re.M) for key in ['id', 'kind', 'type_tag', 'title', 'status', 'summary', 'source_refs']))
    check('formal C0 ' + row['path'], not any(ord(c) < 32 and c not in '\t\r\n' for c in text))
    check('formal trailing whitespace ' + row['path'], all(line == line.rstrip(' \t') for line in text.splitlines()))
check('exact five complete receipts', len(receipts) == 5 and {r['id'] for r in receipts} == {r['id'] for r in sources})
for r in receipts:
    check('complete receipt ' + r['id'], all(r[k] for k in ['full_file_reviewed', 'related_material_checked', 'unique_content_accounted_for', 'read_note', 'comparison_note', 'decision_note']) and all((ROOT / t).is_file() for t in r['targets']))
report = {'passed': True, 'checks': len(checks), 'details': checks,
          'scope': 'byte/domain/runtime/reuse/semantic receipt/formal format; not universal mathematical or production certification',
          'formal_forbidden_C0': 0, 'formal_trailing_whitespace': 0}
dump(E / 'self-check.json', report)
dump(W / 'self-check.json', report)
print(json.dumps({'formal_files': len(formals), 'formal_bytes': sum(r['bytes'] for r in formals),
                  'primary_files': 5, 'primary_bytes': 37791, 'semantic_receipts': 5,
                  'checks': len(checks), 'passed': True}, ensure_ascii=False))
