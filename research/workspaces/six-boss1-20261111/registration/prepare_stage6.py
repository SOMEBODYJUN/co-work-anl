"""Prepare Main-reviewed stage-six bodies and a full additive registry candidate.

This script does not commit, push or replace the live registry.  work.py
research register performs the subsequent checked registration.
"""
from pathlib import Path
from hashlib import sha256
import json

HERE=Path(__file__).resolve().parent
WS=HERE.parent
REPO=WS.parents[2]
REG=REPO/'research/registry.json'
COMP_ID='customer-attraction/six-providers/cross-branch-necessary-system-20261111'
BG_ID='customer-attraction/one-prefix-five-profit-exclusive-charge'
PRICE_ID='customer-attraction/previous-theme-uniform-positive-price'
COMP='archives/customer-attraction/subarchives/six-providers/state/计算/同源增广与跨枝运输的必要系统推进--计算.md'
BG='archives/customer-attraction/state/引理/一位背景五人利润的独占客户收费--引理.md'
PRICE='archives/customer-attraction/state/引理/上一主题查询的统一正客户价格--引理.md'
BASE='research/workspaces/six-boss1-20261111/'


def digest(path):return sha256((REPO/path).read_bytes()).hexdigest()
def ev(path):return {'path':path,'sha256':digest(path)}
def header(oid,title,status):
    return f'---\nid: {oid}\nkind: lemma\ntype_tag: 引理\ntitle: {title}\nstatus: {status}\ntruth_status: proved\n---\n\n'
def write(path,text):
    p=REPO/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text.rstrip()+'\n')


def bodies():
    bg=(WS/'background_five_bridge.md').read_text()
    bg=bg.replace('RUN：six-boss1-20261111；Boss1 子任务 background_five_bridge。本稿只使用当前仓库已定位正文及冻结证书，未改 registry、RUN、其他代理文件或 Git。原六人全称 half 问题仍 **OPEN**。',
        '本页给任意合法一位背景下五人子 SPE 的精确收费定理。Main已实读源行、物理分母平移、全部系数域枚举方法与独立字面核验。六人全称 half 仍 **OPEN**。\n\n本页证据的仓库根目录是 `'+BASE+'background_five_bridge/`；后文未写全前缀的程序及 JSON 均在此处。其完整原研究稿为 `'+BASE+'background_five_bridge.md`。')
    write(BG,header(BG_ID,'一位背景五人利润的独占客户收费','普遍收费命题已证；六比较的剩余根账仍开放')+bg)
    pr=(WS/'main_previous_theme_price.md').read_text()
    pr=pr.replace('ν>0 时每个客户 w_x 严格正；ν=0 时 w_x=0。',
        'ν>0 时每个客户 w_x 严格正；ν=0 时 w_x=0。余两人 k=2 时没有中间位，两个端点相等，故 w_x=(1−θ)ν/(p_x+t+1) 恒等成立；此时其它自由参数影响共同价格上限。')
    pr=pr.replace('## 5. 下一义务','## 5. 独立复核与下一义务\n\n本页的 S² 最大化、完整预算、静态查询量词和 min 差界另经 `/root/anchored_requery` 实读复核，见 `'+BASE+'anchored_requery/previous_theme_price_review.md`。该复核不代替上面的普遍证明，也没有另加数值分离主张。\n\n### 下一义务')
    write(PRICE,header(PRICE_ID,'上一主题查询的统一正客户价格','任意尾长正价合同已证；后续跨源付款未完成')+pr)
    p=REPO/COMP;text=p.read_text()
    text=text.replace('status: 五个固定支持必要LP有精确原始对偶证书；完整ZZ自由min闭合仍低于half',
        'status: 六个固定支持必要LP有精确原始对偶证书；132个旧末位节点共同层可行；原题开放')
    text=text.replace('## 五个有限系统的精确证书','## 六个有限系统的精确证书')
    row='| 完整ZZ min及6新早期行：19556行、15593列 | 精确原始与零扩展旧对偶匹配 | 0.4911650507957935 |'
    if '| 再加22具名同源行：19578行' not in text:
        text=text.replace(row,row+'\n| 再加22具名同源行：19578行、15593列 | 精确原始与127个正对偶行权匹配 | 0.4913710398913766 |')
    text=text.replace('前三轮新最优值严格增加，后两轮保持第三轮最优值，均小于 $1/2$。',
        '前三轮新最优值严格增加，中间两轮保持第三轮最优值，第六轮再次提高；所有值均小于 $1/2$。')
    text=text.replace('下一条不同的原始义务是全部旧真实末节点 $Z_e\\to Z_f$ 的互查。',
        '该阶段的下一义务是全部旧真实末节点的互查；此后已完成下文所列全部 R/Z 共同层。')
    marker='## 22条具名同源行与第六个精确系统'
    if marker not in text:
        text += r'''

## 22条具名同源行与第六个精确系统

19556点仍违反22条新的具名源预算行：11条零折扣自由portfolio、10条二状态四分之一折扣、1条四状态四分之一折扣。新行使用同一真实源的末回复映射，全部查询权客户无关；强制主题来自共同目录中的已保存真实H/M标签。四状态保上一主题，初态上一标签可以任意合法选择，不要求它在末回复映射下指向当前标签。一般机制沿用Boss2已核折扣闭包，未重复认领。

22条完整原4849向量互异且与旧行不同，全部零质量列也独立重构，辅助列系数零。冻结包为 `shared_source_deepening/selected_all_named_19556.json`，SHA `3b373504be8593d6737433ea8341aac5eba67a153243392d173631e05f02e130`。此前4906个固定向量在19556点全非负；这个事实只对那些固定向量，不封闭它们的全参数族。

接入后得到19578×15593必要系统，精确最优值为

\[
v_4=\frac{32965083449070092662501584108519329553807075826256965818189}
{67087965656985842091686366650394832101978655548218343240984}
\approx0.4913710398913766.
\]

新点330个正原列、1549个正max辅助、651个正min辅助。原支持秩325，五个自由有理值均保存；对偶128变量秩128，127行乘子正。Main独立核全部19578行及15593列的Fraction恒等式、非负性和原始/对偶匹配，见 `main_19578_audit.json`。

127个正对偶行权中，仅四条新增行承重：零基行19569、19571、19574、19576，即actual第三源的B2:H2、B2:H3、B3:H1、B3:H2二状态θ=1/4行。其余123个正行权来自旧系统；11条零折扣和四状态新行在此份证书中的权均零。这说明旧系统加这四条新行已支付当前精确最优值；不声称每行单独不可或缺或整个零折扣锥无效。

Main另给源第二位的一条普遍显式四状态表，预算82u2+3K，见 `main_four_state_closed_form.py/json`；它在旧19556点严格负、在新点已正。将上一主题位取差还得到统一正价格，普遍命题另见父档《上一主题查询的统一正客户价格》，不以本有限LP赋予其证明。

矩阵、点、对偶和独立核验在 `discounted_augmented_lp/`。点SHA `a4e48a91f0e2c7b65725178d042b515c6bedf11562afdeeea2ae69b815e8f505`；矩阵SHA `a95bd72e0fdc2b0b93af79b1a0e8b324b6bd1fc8f62abe8a3ce642be4bcc3936`；对偶SHA `117389015b031455767c48421702078fa4e9162dbe2cf847267fa699360c83c6`。

## 全部132个旧末位节点的同一客户完成

设旧R节点的真实客户前缀分母为

\[
d_e=p_3+t_i+(w_j)_{1+f}+1,
\qquad e=(f,i,j),\quad P=\sum_{k\le4}a_k.
\]

同一客户的四类原始末位查询成本直接为

\[
\frac{r_e-r_f}{d_e},\quad\frac{r_e-z_f}{d_e},\quad
\frac{z_e-r_f}{P+1+r_e},\quad\frac{z_e-z_f}{P+1+r_e}.
\]

前两式只用已有边缘；Z→R才需要RR交叠。独立重建的126条轨道上包络与原矩阵逐列相等，排除了把旧R前缀误读为含R_e本身的分母。1306个overlap列仍只是正上包络接口。

在19556点，原全R阈值相与family1改Z阈值相各取1/2，得到77040正有理客户原子；新19578点单独全R阈值即足够：

\[
R_e=[0,q_e),\qquad Z_e=[0,t_e)\cup[q_e,q_e+v_e-t_e)
\]

在每个hist的同一[0,H)上实现全部66对own四态和全部RR=min。同步对六旧词和字面节点施加全部720个置换，58个基础原子展开为41760个正有理原子。不同字面标签未被合并，分母所用真实旧词随节点一起置换。

两点上四类查询各4356条，共17424条，逐字面直接收益式全部非负：R→R有4260正、96零；R→Z与Z→R各4356正；Z→Z有4290正、66自查零。新点最小正ZZ余量约0.00002785689484903378。有限单位客户可通过141位共同分母整体清分母实现这一共同覆盖层。

输入、完整共同原子、源程序、逐字面精确余量及126条接口全系数审计在 `old_r_joint/`。新见证SHA `6e4932cd3ed8b216fcb5ccaf2379ef7f8257455577da5aaa08ea514397270ad0`，原子SHA `4460a00cb798266bc645c9d7694eefcc49c87c0dbd3b42de8610f6087ae35398`。验证器不导入构造器，按真实R/Z前缀直接计算全部查询。

因此，在这些指定点上，仅由own四态和这四类R/Z互查组成的共同运输域已可行。任何这些相同IC的全局非负权或合法联合运输势都不能切这些点。该结论未加入跨family共同状态、全部其它目录查询或完整策略；后者仍是下一实际义务。原六人全称half继续开放。
'''
    write(COMP,text)


def new_object(oid,title,path,model,statement,quantifiers,assumptions,scope,objections,files,keywords):
    evidence=[ev(p) for p in files]
    return {'object_id':oid,'version':1,'title':title,'kind':'lemma','truth_status':'proved',
        'model':model,'statement':statement,'quantifiers':quantifiers,'assumptions':assumptions,
        'scope':scope,'objections':objections,'body':ev(path),'evidence':evidence,
        'sources':['frontmatter-id:'+oid,'material:'+path]+['material:'+p for p in files],
        'keywords':keywords}


def main():
    bodies();reg=json.loads(REG.read_bytes());byid={o['object_id']:o for o in reg['objects']}
    obj=byid[COMP_ID];assert obj['version']==3
    obj['version']=4;obj['title']='六个有限必要系统的精确最优与132旧末位节点的共同完成'
    obj['body']=ev(COMP)
    obj['statement']+=' 追加22具名同源行得19578×15593，精确最优v4约0.4913710398913766；127正对偶中四条新增theta=1/4行承重。19556和19578点分别有77040/41760原子同一客户完成，17424条R/R、R/Z、Z/R、Z/Z真前缀查询全非负，新点全部RR=min。'
    obj['scope']+=' 最新指定点的132旧末位节点互查层已有共同精确可行测度；需转向跨family身份或新的真实早源约束。'
    obj['assumptions'][1]='全部继承列逐描述符保留；辅助列只编码所列正部及虚拟最小值上界，目标与归一化系数零'
    extra=[BASE+p for p in (
        'discounted_augmented_lp/augmented_lp_exact.json','discounted_augmented_lp/exact_matrix.json.gz',
        'discounted_augmented_lp/exact_dual_certificate.json','discounted_augmented_lp/certificate_verification.json',
        'discounted_augmented_lp/new_cut_exact_slacks.json','discounted_augmented_lp/final_manifest.json',
        'main_19578_audit.json','shared_source_deepening/selected_all_named_19556.json',
        'main_four_state_closed_form.py','main_four_state_closed_form.json',
        'old_r_joint.md','old_r_joint/common_completion_19578.json','old_r_joint/common_atoms_19578.jsonl.gz',
        'old_r_joint/full_network_verification_19578.json','old_r_joint/full_network_verification_19556.json',
        'old_r_joint/interface_audit_19578.json','old_r_joint/verify_network.py','old_r_joint/final_manifest.json')]
    obj['evidence'] += [ev(p) for p in extra if p not in {e['path'] for e in obj['evidence']}]
    obj['sources']=list(dict.fromkeys(obj['sources']+['material:'+p for p in extra]))
    bgfiles=[BASE+'background_five_bridge/'+p for p in ('shift_local.py','shift_certificate.py','verify_literal_and_bridge.py',
        'shifted_local_tables.json','fixed53_b0_profit.json','fixed53_b1_profit.json','fixed53_b1_coverage.json',
        'literal_bridge_audit.json','exact_32_type_table.md','artifact_manifest.json')]
    bgfiles += ['archives/customer-attraction/tools/half5-exact/certificate.json','archives/customer-attraction/tools/half5-exact/verify_certificate.py']
    bg=new_object(BG_ID,'一位背景五人利润的独占客户收费',BG,
        '有限单位客户、有限非空共同标签目录、完整有序历史纯SPE；固定任意合法长度一历史(Z)，随后恰五名单位提供者；保空覆盖、重复与同覆盖异标签、任意平局和零客户。',
        '记五尾覆盖并集U、真实总利润V=sum c/(b+c)，b=1_Z；任意五合法比较标签重数d给R_Z=sum d/(b+d)。有R_Z<=2V+epsilon|Z\\U|，epsilon=62212762317811658581/1250000000000000000000<1/20，因此R_Z<=2V+r_Z/20。证书保原53外乘子，合法背景平移和局部重算后全6144条件态仅32负态，均在b=1,c=0；共享K剩余正。另给六槽删除精确损失和未付根账。',
        '对任意客户数、目录、完整策略、合法Z历史及任意五元比较标签（允许重复）；不要求前置者根最优。',
        ['所有隐藏后继来自同一完整策略的对应真实历史','所有物理收益与保证分母加入同一b；利润目标不能沿用覆盖目标税','保原53外乘子与共同K，局部下包络在完整二元域重算并向安全方向取整'],
        '普遍一背景五尾利润收费定理；精确六比较删槽账及两个付款模板的有效边界。全系数枚举覆盖任意非负整数客户求和。',
        '未证明任意一背景零收费BG5，未把R_Z视作OPT6或V视作新覆盖。十一客户完整SPE只否定删槽损失由2u1单独支付，不否定six-half。19556固定点仍通过本收费及192类加强。',
        bgfiles,['background-five','exclusive-prefix-clients','exact-coefficient-certificate','six-slot-deletion'])
    pricefiles=[BASE+p for p in ('main_previous_theme_price.md','main_four_state_closed_form.py','main_four_state_closed_form.json',
        'anchored_requery/previous_theme_price_review.md')]
    price=new_object(PRICE_ID,'上一主题查询的统一正客户价格',PRICE,
        '有限单位客户、任意有限非空共同标签目录、任意完整有序历史纯SPE；合法源h尚余k>=2，源收益r和同一actual末价u_m、共同K；任意平局、空与重复标签、零客户保留。',
        '四状态(a,t)->(t,c)同源Bellman成本含上一主题查询nu*a/(p+t+s+1)。固定当前初题T及静态查询后，任意合法初始上一题F均满足sum w_x 1_F<=B-sum b_x，其中b_x=Psi(0,1_T)，w_x=Psi(1,1_T)-Psi(0,1_T)。有(1-theta)nu/(p+1_T+k-1)<=w_x<=(1-theta)nu/(p+1_T+1)，nu>0时逐客户严格正；无需源权等于总查询权。k2时上下界相等。',
        '对任意0<=theta<1和全部全局非负参数；静态T,Q及参数先固定，然后对所有目录标签F同时成立。初对不要求C_h(F)=T。',
        ['同一源与同一完整策略产生C_h；上一主题是合法末位查询','固定静态查询不随被定价F改变','所有源/actual末价/容量及常数项完整付款，跨源收入不免费合并'],
        '一般四状态正价接口及显式82u2+3K分数表，可给其它真实后继统一定价；普遍证明由S²辅助最大值与同候选min差界承担。',
        '未证明该完整价格锥严格超出平衡当前主题价格，未声称已分离新点或证明六人half；每次跨源使用均须支付完整价格上限。',
        pricefiles,['previous-theme-query','four-state-Bellman','positive-client-price','cross-source-budget'])
    for new in (bg,price):
        assert new['object_id'] not in byid
        reg['objects'].append(new)
    mats={m['path']:m for m in reg['materials']}
    for ob in (obj,bg,price):
        for item,isbody in [(ob['body'],True)]+[(e,False) for e in ob['evidence']]:
            path=item['path'];h=item['sha256']
            if path in mats:
                old=mats[path]
                if old['sha256']!=h:
                    assert path==COMP,('unexpected changed material',path)
                    old['sha256']=h
                continue
            rec={'path':path,'sha256':h,'disposition':'objects' if isbody else 'attachment',
                 'object_ids':[ob['object_id']],
                 'reason':'Boss1 Main实读源行与证明、核全域方向及精确证据后回流；数学量词与有限边界以承重正文为准。'}
            reg['materials'].append(rec);mats[path]=rec
    target=HERE/'stage6-registry-candidate.json';target.write_text(json.dumps(reg,ensure_ascii=False,indent=2)+'\n')
    summary={'base_registry_sha256':sha256(REG.read_bytes()).hexdigest(),'candidate_sha256':sha256(target.read_bytes()).hexdigest(),
             'objects':[{'object_id':o['object_id'],'version':o['version'],'body':o['body']} for o in (obj,bg,price)],
             'total_objects':len(reg['objects']),'total_materials':len(reg['materials'])}
    (HERE/'stage6-registration-summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
    for ob in (obj,bg,price):
        (HERE/({'computation':'stage6-computation','lemma': 'stage6-background' if ob['object_id']==BG_ID else 'stage6-price'}[ob['kind']]+'.json')).write_text(json.dumps(ob,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(summary,ensure_ascii=False))


if __name__=='__main__':main()
