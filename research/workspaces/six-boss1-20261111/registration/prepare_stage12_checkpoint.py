"""Update the recoverable Stage12 entry and actual agent ledger."""
from pathlib import Path
from hashlib import sha256
import json
import subprocess

HERE = Path(__file__).resolve().parent
WS = HERE.parent
REPO = WS.parents[2]
PREFIX = 'research/workspaces/six-boss1-20261111/'
OID = 'customer-attraction/shared-maximal-potential-early-safe-prefix-family'
BODY = 'archives/customer-attraction/state/引理/共同最大潜力主题的早期安全预算投影--引理.md'

def bind(p):
    return {'path': p, 'sha256': sha256((REPO / p).read_bytes()).hexdigest()}

def run_saved(args, stem):
    r = subprocess.run(['python', 'work.py'] + args, cwd=REPO, capture_output=True, text=True)
    (HERE / (stem + '.stdout.json')).write_text(r.stdout)
    (HERE / (stem + '.stderr.txt')).write_text(r.stderr)
    print(json.dumps({'step': stem, 'exit_code': r.returncode, 'stdout': r.stdout[-900:], 'stderr': r.stderr[-900:]}, ensure_ascii=False), flush=True)
    assert r.returncode == 0

def main():
    reg = json.loads((REPO / 'research/registry.json').read_text())
    obj = next(o for o in reg['objects'] if o['object_id'] == OID)
    assert obj['body'] == bind(BODY)
    ep = 'map/edges/six-boss1-20261111/complete-history-to-common-X-early-SAFE.json'
    edge = {
        'status': 'accepted', 'premises_mode': 'all', 'relation_mode': 'unconditional',
        'reviewed_by': 'Boss1/Main six-boss1-20261111',
        'edge_id': 'ca-six-boss1-complete-history-pays-common-X-early-SAFE',
        'kind': 'implies', 'source_ids': ['CAG-MODEL'], 'target_ids': [OID],
        'conditions': '恰六人，i=1,2,3，原前缀及其真实续局定义b、P、u；同一个X最大化全目录f_P，所有查询和后继均为合法标签。',
        'roles': {'CAG-MODEL': '支付原源真实IC、各合法后继标签在原源的SAFE、真实末位查询；有限共同目录支付固定X最大性。', OID: '用同一全局权与全类型四角解析余项推出三条普遍必要不等式。'},
        'explanation': '目标减去α源IC、各中间sSAFE、r末SAFE、各中间aMAX及1真末查询，恰等于逐客户E。x=0取q=1,k=r−2、x=1取q=k=0只降E；四角非负由s/r+a/(r−1)=1/2、凸G的端点及d≤5证明。SAFE必须重取该标签偏离后的真实σ后继，不冻结X枝。',
        'scope': '支付C6=206/5、C5=121/4、C4=61/3的全类型有效性，及同一根实际路径共用X。',
        'contribution': {'result': '同一末两位最大潜力标签向前三位源的更强必要式。', 'remaining': '不支付六人half、完整SPE反例、有限LP最优或这些常数的真实SPE锐性。'},
        'evidence': [bind('archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md'), bind(BODY), bind(PREFIX + 'early3_maxx_cone/audit_main_family.md'), bind(PREFIX + 'early3_maxx_cone/audit_main_family.json')],
        'review_note': 'Main亲自推导全四角证明，独立席从原份额核1440型与2880付款。X、P、原源u及各真实后继身份逐项核对；不由旧AP减非负SAFE冒证新式。'
    }
    assert not (REPO / ep).exists()
    (REPO / ep).write_text(json.dumps(edge, ensure_ascii=False, indent=2) + '\n')
    run_saved(['research', 'edge-bind', ep, '--write'], 'stage12-prefix-edge-bind')
    run_saved(['research', 'edge-check', ep], 'stage12-prefix-edge-check')

    intro = '''## Stage12当前入口：第十精确最优面已排，23676共同交叠系统待唯一发现

原六人2W≥OPT6仍OPEN。最后确认pushed是ef43da7b2a1bdf1bdaa06e302586dc4a3748a13a，收据checkpoints/stage11-results.json；本节及本轮文件须以随后checkpoint的pushed收据为远端恢复上限。保持同Boss1、同RUN、同分支和子档继续。

完整共同X的22297×21021有限必要系统已精确闭合：W10=41418833157785254128446533347783719656800199407573523353330084664882709/83821400169176597880954822390709624066211318077718478066891770484527716≈.4941319647988424。463个正对偶行权匹配，全部22297原始行、21021对偶列、归一/互补及11164规范辅助独立PASS。primal SHA5b1b649af5fc9d359e31dd03945d12708e599e0eeac75983ed188e60178b3bfe，dual SHA4a6b6ca154ce645bcdabceb50bcb83982fead5875f257bf0a4c56f9576d7405f，路径maxb_augmented_lp/full_lift/recovery/。Main完整实读独立检查器和证书报告，不重跑数值。

新12个正行权及新列残差精确合成为γMC6，γ=789080258691877867746986463043339529104615894873787767345518839040651/83821400169176597880954822390709624066211318077718478066891770484527716。故原20910加单MC6的20911系统也精确同值，452正行权，证据compact_projection/；只证最优值相等，不证投影域相等。原17MAX行在本点全严格松且dual0，只是此证书支撑情况。

旧W9整个最优面由MC6的精确signed identity排除，独立保号ray给.4931316100867487严格下界，现已被W10提高；old_optimum_face/保留全部证明，不把其当匹配最优。唯一22297云发现run43091082992、job130768110298、artifact13889091562来自ef43da7，原ZIP/数组、六输入和执行源码均已取回按SHA核验。没有未取回的旧云产物。

第十整个最优面也已排除。旧任意锚AP的actual3→A6行AP39在每个W10最优点恒等于−2387360308883849167939463658247160398139890481107232380975950684899327/167642800338353195761909644781419248132422636155436956133783540969055432≈−.014240756561364065。仅正dual支撑的初试失败，其5列形式方向不是可行最优面方向。补用全局相反行和3384步非负面传播，取得9787强制零列、6376强制等式；223行权和5682零列权的signed identity逐21021列精确验证。完整路径early_ap_optimum_face/facial_zero_closure/；Main已实读报告和独立重放器。不把整面排除等同于已给新的定量最优。

Main全类型解析推导把actual1/2/3常数43、65/2、23分别改进为206/5、121/4、61/3。付款为原源真实IC、原源分别改后继标签的SAFE、同一f_P最大X及真实末节点查询；不冻结别枝。四角解析证明与1440型/2880份额付款独立PASS，正式父档引理“共同最大潜力主题的早期安全预算投影”v1已登记。工作原文main_prefix_safety_maxx_family.md/.py/.json；51行SHA1a1876a01a505e74b1497fc1ac1ad62400b93bf648f53bf9966fc630f13b770c。新行=旧AP−ΔSAFE只是系数接口，普遍性由独立预算证明承担。

H3常数10正式父档引理v1及计算对象v10已登记、有关承重边重新绑定。H3的17行在5b1b全正；指定七权锥最佳仍10。第三位八权锥最佳61/3；另加正确前缀(h2,X,Y)的三份真实倒二PAIR后仍61/3，新增对偶reduced costs为(6,1/3,139/6)，全部最优η=0；early3_pair_cone/保全288型与11权精确恒等式，0优化。这些只关闭明定证书锥，不声称真实SPE锐性。

210组X/RZ或X/B4共同八格的1260投影行已冻结，SHA711e0d2b1499784f26fce26d8cc7a7a985c618df52a125f91af61a168bfc70ba；5b1b固定canonical y有5条O6负，均不排自由重选。新系统中420个y已升真实core，禁止canonical_min。六facet在各组局部充要，未宣称210组自动有全局共同客户律。root_x_joint_contract.md/还给一个同X根η合同。

唯一下一数值输入在common_x_joint_lp/final/：23676×21021、3313758非零；保旧22297，加H3 17、原AP51、own1260、新SAFE/MAX51。保16hist、6个历史零hist及4992共享624隐藏列；10277core包括420真实y，仅10744旧辅助可规范重算。精确矩阵SHA1b4a4e544e5b9eeea1fa64b3849a9d4cc532b997a5ad972ce33df81c224551e7。全新行与六自足输入经独立审查，receiver五类异常均正确拒收或失去eligible。当前没有新最优值或原始点。正式本地请求C-six-boss1-common-x-joint-23676-01，一次DS1800秒/job40分钟；随本次推送触发，0自动重试。

实际在续：/root/common_x_joint_lp准备已冻结，等Main取回原数组后由原席接精确原始/对偶及210组β=L八格核验；/root/common_x_joint_audit已完成并释放。/root/early12_safe_maxx_cones已完成第一、第二源完整非对称权锥，报告两个常数已最优，Main正在实读证书。/root/root_x_shared_queries及其子审/root/root_x_shared_queries/independent_audit正把已证明的共同根η合同落实为新42真实查询接口；/root/opt6_shared_x_exchange正在核同一X的OPT6槽交换约束。各自独占新目录，不改已冻结23676输入。Main同时推进全部源同一X合账，继续真正未付的共同身份义务。

'''
    mainpath = WS / 'main.md'
    old = mainpath.read_text()
    start = old.index('## Stage12当前入口')
    end = old.index('## Stage11结果与当前入口', start)
    mainpath.write_text(old[:start] + intro + old[end:])
    readme = '''# Boss1：恰六人半覆盖

RUN：six-boss1-20261111；Boss1；分支rebuild/research-v2；存档customer-attraction；子档six-providers。

## 恢复入口

实际clone：/workspace/scratch/b0fef5ec503f/co-work-anl-boss1。实际工作区research/workspaces/six-boss1-20261111/。先打开main.md顶部“Stage12当前入口”、spec.json及实际任务稿、程序和输入输出，再执行research resume six-boss1-20261111核证据包、未答反馈和任务状态。环境丢失时按同Boss、分支、存档和子档start --resume。原题OPEN，保存之后继续Main循环。

## 当前已核结论

完整共同X的22297×21021必要系统精确最优W10约.4941319647988424，精确分数、463正对偶与全行列证书在maxb_augmented_lp/full_lift/recovery/；primal SHA5b1b649af5fc9d359e31dd03945d12708e599e0eeac75983ed188e60178b3bfe。新增对偶投影给20911单MC6系统同值，compact_projection/有452正对偶和独立匹配证书。只是固定16hist必要LP，低于half不是SPE反例或全域下界。

W9整个最优面被MC6排除。W10整个最优面又被旧AP的actual3→A6行排除：精确恒等负值约−.014240756561364065。后者证据在early_ap_optimum_face/facial_zero_closure/，需保全3384步强制零面传播与21021列signed identity；初试正dual支撑不足的失败也保留。没有据此认领下一LP的新定量最优。

正式解析入口包括父档“共同最大潜力主题的末两位容量投影”“共同最大潜力主题的三尾前接不等式”和新增“共同最大潜力主题的早期安全预算投影”。Main的新全类型证明给前三源常数206/5、121/4、61/3，独立1440型原份额核验PASS。H3七权锥最佳10、第三源加三份真PAIR的十一权锥最佳仍61/3，各自限定证书锥，不外推真实SPE锐性。

210组共同X/own的1260六facet已核；420交叠今后必须是独立真实core，不能取各自min。旧5b1b的5条O6负只否定给定y。根438和RZE177旧cb45完成、旧b0ca的164目录排除均保各自点/域，不迁移。

## 当前实际义务

common_x_joint_lp/final/已经冻结23676×21021、3313758非零；matrix SHA1b4a4e544e5b9eeea1fa64b3849a9d4cc532b997a5ad972ce33df81c224551e7。10277core含420真实y，10744旧辅助保规范合同。最终六输入、全51增量与恢复路径独立PASS；同目录actions_request.json及freeze_manifest.json是准确输入，Main正式本地请求为C-six-boss1-common-x-joint-23676-01，推送触发一次DS1800秒/job40分钟。

取回这份请求的原始ZIP/数组，核request、source commit、六输入、实际源码、输出清单和返回scales，再交原/root/common_x_joint_lp做精确原始/对偶及210组八格验证；不可把数值状态当结论。/root/common_x_joint_audit已完成。/root/early12_safe_maxx_cones给前两源锥的精确最优，待Main实读；/root/root_x_shared_queries及其independent_audit落实同一X根η的真实查询接口；/root/opt6_shared_x_exchange核最大覆盖槽交换。各新任务只能写独占目录，不改已冻结final输入。

## 远端状态

最后确认pushed为ef43da7b2a1bdf1bdaa06e302586dc4a3748a13a，收据checkpoints/stage11-results.json，公屏seq81。上述Stage12结果、新正文和23676请求在本次checkpoint确认前仅本地。旧云run43091082992/artifact13889091562已完整取回并核验，当前没有已派未取的旧云产物；新请求以随后真实run回执为准。checkpoint成功后继续原题。
'''
    (REPO / 'archives/customer-attraction/subarchives/six-providers/workspaces/Boss1/README.md').write_text(readme)
    assignments = {
        'common_x_joint_audit': '独立核23625/23676真实420core恢复路径、旧10744辅助、六自足输入及51新增系数；发现五类接收绑定缺口并独立复验修复。实际席/root/common_x_joint_audit。已完成冻结，0优化。',
        'early3_pair_cone': '在原第三位八权锥追加正确真实前缀(h2,X,Y)的TP(Q,X)、TP(Q,Q)、TP(X,X)；全288型11权，先延旧对偶，0优化闭合C*=61/3、三η必零。实际席/root/early3_pair_cone，已完成冻结。',
        'early12_safe_maxx_cones': '核第一、第二源完整非对称SAFE/MAX权锥；仅每r一份≤60秒tiny LP，完整有理原始/对偶与独立真实份额核查，禁止固定LP点拟合。实际席/root/early12_safe_maxx_cones，现已冻结，待Main实读。',
        'root_x_shared_queries': '把已证同一X根η合同落实为42条真实源查询及可行的小规模PAIR接口；0优化，不读已排cb45点，不改23676。实际席/root/root_x_shared_queries，子审/root/root_x_shared_queries/independent_audit；独占root_x_shared_queries/。',
        'opt6_shared_x_exchange': 'Main推导OPT6的k槽交换计数，代理独立核并落地V=X加actual子集、以及六标签覆盖上界；先去除已有同向行，零新列/零优化，不改23676。实际席/root/opt6_shared_x_exchange。'
    }
    for name, body in assignments.items():
        p = WS / 'assignments' / (name + '.md')
        assert not p.exists()
        p.write_text('# Boss1 / RUN six-boss1-20261111\n\n' + body + '\n')
    jobs = [
        ('early3_maxx_cone', 'closed', 'early3_maxx_cone.md', '已完成61/3八权最优、17行及Main三源1440型独立审计；新义务另分配。'),
        ('common_x_joint_audit', 'closed', 'common_x_joint_audit.md', '最终23676六输入与恢复合同PASS；新数值返回后按实际风险另核。'),
        ('early3_pair_cone', 'closed', 'early3_pair_cone.md', '指定十一权锥已解析闭合，三PAIR不能降61/3；换新真实预算。'),
        ('early12_safe_maxx_cones', 'working', 'early12_safe_maxx_cones.md', '完整两锥证书已冻结，Main实读后关闭。'),
        ('root_x_shared_queries', 'working', 'assignments/root_x_shared_queries.md', '完成同一η的42新根查询，精确源历史/系数/独立审计。'),
        ('root_x_shared_queries_independent_audit', 'working', 'assignments/root_x_shared_queries.md', '独立审查同一η接口、源历史与字面系数，不调用优化器。'),
        ('opt6_shared_x_exchange', 'working', 'assignments/opt6_shared_x_exchange.md', '核最大覆盖交换与现有行，冻结真正新的零新列包或精确冗余。'),
        ('common_x_joint_lp', 'working', 'common_x_joint_lp.md', 'final23676已冻结；Main唯一Actions返回后原席精确恢复，全core及210八格。'),
        ('Main', 'working', 'main.md', '确认Stage12结果与23676请求pushed，接回唯一云数组；继续同X真实源/根联合义务。')
    ]
    for name, state, note, next_text in jobs:
        aid = '/root' if name == 'Main' else '/root/' + name
        if name == 'root_x_shared_queries_independent_audit':
            aid = '/root/root_x_shared_queries/independent_audit'
        run_saved(['research', 'save', 'six-boss1-20261111', '--solver', name, '--profile', 'full', '--note', PREFIX + note, '--next', next_text, '--state', state, '--agent-id', aid], 'stage12-final-save-' + name)

if __name__ == '__main__':
    main()
