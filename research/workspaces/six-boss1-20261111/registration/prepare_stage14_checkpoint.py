"""Write actual continuation state and save completed/active obligations serially."""
from pathlib import Path
import json
import subprocess

HERE = Path(__file__).resolve().parent
WS, REPO = HERE.parent, HERE.parent.parents[2]
RUN = 'six-boss1-20261111'
PREFIX = 'research/workspaces/' + RUN + '/'


def main():
    receipt = HERE / 'stage14-save-receipts.json'
    assert not receipt.exists()
    entry = '''## Stage14当前入口：真实根尾、全类型精确界与最优菜单重查

原六人2W≥OPT6仍OPEN；Main继续推导，不以checkpoint结束研究。Boss1、RUN six-boss1-20261111、分支rebuild/research-v2和customer-attraction/six-providers不变。写本入口时最后确认pushed为d9c1b9937fb66b811e85968c4ba52a40cc759c10（checkpoints/stage13.json），公屏seq83；本轮须以实际Stage14 pushed收据确认为可恢复上限。

### 本轮已核数学

全256型217行系统的精确界约.4258960956295508已被真实根第五源NEW加强；其整个最优面K固定，NEW恒负，Main全257列signed identity给无新LP严格界约.42608659882235334。静态最大C会员可精确补全54新预算，但不支付真实根后继；universal_max_label_completion/与root_near_equality_audit/均已冻。

Main亲推NEW=10980u1−1658K−87O≥0及SIZE=67140u1−9878K−627O≥0：分别保真实第五源SAFE与同一第五标签大小一致性，128型ρ/η解析非负。新TAIL=112944305160u1−11595684007K−2178783435O≥0由真实最大C分支的第三/四/六SAFE、完整36PAIR及五尾K帽共同支付。Main和独立audit核全部128型及u/K/O三参数，不能把两个有效式直接相减。正式父档根收益加强v1已登记，原题未闭合。

universal_true_x_tail/将同一真实第四源强制X的Y,T跨真PAIR与actual RC联合付款，六整数权(4096,800,71,384,512,900)给全256型QX；Main另核1024态。正式父档两尾跨实际钱包投影v1已登记。219行精确最优22634634904624698063/52739368771603064323≈.4291791015294076，新增NEW与QX均正权。Main进一步证明整个219面K恒定、SIZE恒为−2694628988940630887460/52739368771603064323；main_universal_wallet_v2_face/同名三文件记录全列身份及无LP严格界约.4294380660455146。

221行v3保原219，只加SIZE和TAIL。精确最优alpha3=999866079286562265469481/2318932167377271341801106≈.4311752164865684，11正原子+K，10正预算，全部256型余项非负。Main重放全部221行/257列及新根公式PASS，输入d5808676b4a59bc9a63deece83e291887ead8847a7177c3afac4221523f30f55，证书1d9a898e3ca429b6af3611f01ada831ad50cf7f0708f14d7c518478573f0a9e3。它既是明定必要系统精确最优，也是普遍有效界；不声称SPE实现、half或最佳已知界。整个最优面由正权迫K=|A6|、TAIL=QX=0；只代表点的SAFE6(X)=0不能直接传播整面。

maximal_root_opt_requery/新160ν/10质量式/141原始行已精确Farkas：根C分支第三源依次查询六个真实Q，保其同一后三尾和合法重数矩区间[o/6,o]。九正钱包给126000v3+65719v4+4962v6−Σm(h)w_h≥0，全128型与2048状态认证，旧根71点严格违反。Main识别并独立核量词推广：这九权没有C最大性、K或根u，故任意两行动历史后的真实四人续局及任意六合法查询并均有效。直接映到actual的全256列时与X无关，在221代表点精确值−1458110288660943054148007972513/1471748948895441544929768608≈−990.7330，已排该点。来源、完整公式和逐点值见main_opt_requery_any_history.md及main_opt_requery_cut_check.py/.json；整面排除另等专门线代任务，不能仅从点负值推出。

### 当前实际代理和下一承重义务

/root/universal_union_wallet_lp 已冻v3，现独占v3_optimum_joint_face/：0优化，精确最优面参数及全列身份、K/u1/RC(X,O)与SAFE6(X)范围，并将actual重查cut接回整面；若成立给保号严格对偶。真实C=A6根分支13个零余项型的等号结构也须保同一客户账本。

/root/universal_true_x_tail 已冻requery，现获显式释放在maximal_root_tail_wallet_v2/保原71行、只加此一全128重查cut，K固定为v3的1125421575458286230366665/6570307807568935468436467、O=1，唯一129列小LP；必须恢复两个自由质量乘子及全域u/K/O线，不能直接搬固定K数值。

/root/early_shared_x_source_audit 已冻结maximal_root_opt_requery_audit/；其独立输入22560系数、全域2048状态及2178列齐次身份PASS，并确认任意两前缀推广。现转独立maximal_root_tail_wallet_v2_audit/，核新根72来源、输入及自由K/O的普遍线；不改旧冻结包。

Main已把两条父档引理、计算对象v11及五条计算承重边接回，旧四边只继续支付原AP/H3/容量/MC6步骤，相关承重正文逐字未变；新联合边才支付221行全类型十钱包证书。结构build只核结构，不当数学判决。Stage13 build日志因上轮checkpoint时间竞合未完整推入，本轮保存已完成版本；数学输入未受影响。

### 原云端义务仍未返回

C-six-boss1-common-x-joint-23676-01；run43096304349；source b96dbcdfe0dec963bbaf91f3a9a2f0ed597467ad。check8仍queued、jobs=[]、artifacts=[]，无新数组/数值点，无重发或本地绕过。原冻结23676×21021包含420真实交叠core；收到实际ZIP后先核请求/source/六输入/执行源码/scales，再交原席freeW精确恢复。固定16hist的W10≈.4941319648不能与本全256型界互换。

'''
    mainpath = WS / 'main.md'
    old = mainpath.read_text()
    assert '## Stage14当前入口：' not in old
    old = old.replace('## Stage13当前入口：', '## Stage13历史入口：', 1)
    heading, tail = old.split('\n', 1)
    mainpath.write_text(heading + '\n\n' + entry + tail.lstrip())
    assignment = '''# Stage14实际派工与恢复

Boss1；RUN six-boss1-20261111；Main串行登记、RUN和Git。所有旧冻结包只读。

已闭合：真实最大C静态54行完成；真X四源Farkas与256型cut；根NEW/SIZE等号审计；universal v2/v3；root71与独立audit；root最优查询重查构建包。实际agent ID在下面RUN记录中，不新造研究者身份。

当前 /root/universal_union_wallet_lp → v3_optimum_joint_face/与.md：0优化器，完整v3面及actual新cut的signed恒等式，真实C=A6根13型的准确等号信息。

当前 /root/universal_true_x_tail → maximal_root_tail_wallet_v2/与.md：旧71行+已全域认证重查cut共72行/129列，K取v3准确值；Main显式释放一次小LP，正行尺度与自由K/O乘子必须保。

当前 /root/early_shared_x_source_audit → maximal_root_tail_wallet_v2_audit/与.md：上一requery全域cut、独立Farkas及任意两前缀推广已PASS并冻结；现独立核根72输入、原对偶与两个自由质量乘子，不运行builder或优化器。

Main当前义务：完成Stage14 serial checkpoint并确认pushed，继续把重查切面接回新的根线与下一全256系统；原云run43096304349仍queued，不重复或绕过。
'''
    (WS / 'assignments/stage14.md').write_text(assignment)
    readme = REPO / 'archives/customer-attraction/subarchives/six-providers/workspaces/Boss1/README.md'
    readme.write_text('''# Boss1：恰六人半覆盖

RUN：six-boss1-20261111；Boss1；分支rebuild/research-v2；存档customer-attraction；子档six-providers。

## 恢复与推送上限

实际clone：/workspace/scratch/b0fef5ec503f/co-work-anl-boss1；工作目录research/workspaces/six-boss1-20261111/。先读main.md顶部Stage14、spec.json及实际稿件/源码/输入/输出，再research resume six-boss1-20261111核证据包、未答反馈和下一步。原环境丢失时同Boss、分支、存档、子档start --resume。

写本入口时最后确认pushed为d9c1b9937fb66b811e85968c4ba52a40cc759c10，收据checkpoints/stage13.json，公屏seq83。本轮随后Stage14 checkpoint必须实际返回pushed才成为新的恢复上限。原六人2W≥OPT6仍OPEN，推送后Main继续研究。

## 已成立的最新数学

原固定16hist的十个必要系统已精确推进到W10≈.4941319647988424；其整个最优面被AP39排除，下一23676系统仍等Actions。这个值不是全客户型福利下界，也不是SPE反例。

独立全256客户型+K路线的217/219/221行精确值依次约.42589609563、.42917910153、.43117521649；完整非负对偶同时给原模型普遍界。当前221精确值为999866079286562265469481/2318932167377271341801106。Main全行列重放PASS；输入d5808676…、证书1d9a898e…，完整路径universal_union_wallet_v3/。不声称最佳已知界或half。

真实最大C根分支保第五SAFE、同一尾大小和第三/四/六SAFE+全36PAIR，分别给NEW、SIZE、TAIL三根线；普遍正式正文“最大主题真实尾部的根收益加强”已登记。真source4强制X的同一Y/T联合actual RC给六权QX，另一正式父档引理已登记。旧217与219整个最优面分别被NEW与SIZE排除，Main signed全257列身份保在main_universal_wallet_face与main_universal_wallet_v2_face各三文件。

最新最优菜单重查给126000v3+65719v4+4962v6−Σm(h)w_h≥0：分别查询六合法Q，保真实后三尾与会员区间[o/6,o]。其全128型/2048状态已精确核定；九权不用C最大/K/rootu，故可用于任意两行动历史后的真实四人续局。直接映到actual后，221代表点余量精确−1458110288660943054148007972513/1471748948895441544929768608，已被排除。Main来源推广与全部系数在main_opt_requery_any_history.md、main_opt_requery_cut_check.py/.json。

## 当前实际任务

- /root/universal_union_wallet_lp：v3_optimum_joint_face/，0优化器，完整最优面与新actual cut身份，根C=A6等号结构。
- /root/universal_true_x_tail：maximal_root_tail_wallet_v2/，71旧行+1重查cut，唯一129列LP，恢复更强普遍根线。
- /root/early_shared_x_source_audit：maximal_root_opt_requery_audit/已冻结；现独立maximal_root_tail_wallet_v2_audit/核根72输入、证书及自由K/O线。
- Main亲自核承重预算和全列证书、正式回流、串行checkpoint，继续下一全256合账。

## 唯一云任务

C-six-boss1-common-x-joint-23676-01，run43096304349，source b96dbcdfe0dec963bbaf91f3a9a2f0ed597467ad，创建20:28:55 UTC。最新check8仍queued，jobs/artifacts为空，没有新数值点，无重发。

冻结common_x_joint_lp/final/为23676×21021；10277core含420真实y，10744aux。实际产物回来后先核request/source/六输入/执行源码/scales，再由原/root/common_x_joint_lp恢复freeW精确原始/对偶及210组共同八格。不能把420真实y重新作独立min。恢复上限只到最后实际确认pushed的内容。
''')
    tasks = [
        ('universal_max_label_completion', 'universal_max_label_completion.md', 'closed', '/root/universal_union_wallet_lp', '静态C的54预算精确完成已冻；真实根分支另有排除，不继续同点优化。'),
        ('universal_true_x_tail', 'universal_true_x_tail.md', 'closed', '/root/universal_true_x_tail', '四真实源阶段I精确Farkas及全部256型QX已冻，父档参数族已回流。'),
        ('root_near_equality_audit', 'root_near_equality_audit.md', 'closed', '/root/early_shared_x_source_audit', 'NEW来源、整217面身份与严格对偶均已独立通过。'),
        ('universal_union_wallet_v2', 'universal_union_wallet_v2.md', 'closed', '/root/universal_union_wallet_lp', '219行精确原对偶冻结，Main进一步已排整个最优面；不改旧包。'),
        ('maximal_root_tail_wallet', 'maximal_root_tail_wallet.md', 'closed', '/root/universal_true_x_tail', '71行根系统及自由K/O的TAIL线精确通过，后续在独立v2包。'),
        ('maximal_root_tail_audit', 'maximal_root_tail_audit.md', 'closed', '/root/early_shared_x_source_audit', '9159系数与131列普遍恒等式独立核完。'),
        ('universal_union_wallet_v3', 'universal_union_wallet_v3.md', 'closed', '/root/universal_union_wallet_lp', '221行精确原对偶已冻；新actual重查已排代表点，整面另研究。'),
        ('maximal_root_opt_requery', 'maximal_root_opt_requery.md', 'closed', '/root/universal_true_x_tail', '160变量精确不可补全与全部128型cut已冻；九权可用于任意两前缀。'),
        ('maximal_root_opt_requery_audit', 'maximal_root_opt_requery_audit.md', 'closed', '/root/early_shared_x_source_audit', '独立全系数/Farkas/2178列与任意两前缀来源已PASS并冻结；转独立根72审计。'),
        ('maximal_root_tail_wallet_v2_audit', 'assignments/stage14.md', 'working', '/root/early_shared_x_source_audit', '独立根72来源、输入与完整原对偶，特别核自由K/O的131列普遍恒等式；不运行优化器。'),
        ('v3_optimum_joint_face', 'assignments/stage14.md', 'working', '/root/universal_union_wallet_lp', '0优化，完整v3面与actual重查cut全列signed身份和严格对偶。'),
        ('maximal_root_tail_wallet_v2', 'assignments/stage14.md', 'working', '/root/universal_true_x_tail', '已显式释放一次根72行/129列LP；固定v3 K，只加重查cut，须自由K/O普遍线。'),
        ('main', 'main.md', 'working', '/root', 'Stage14确认pushed后继续真实最优查询、根72和全256合账；原Actions仍queued，原题OPEN。'),
    ]
    receipts = []
    for solver, note, state, aid, nxt in tasks:
        args = ['python', 'work.py', 'research', 'save', RUN, '--solver', solver, '--profile', 'full', '--note', PREFIX + note,
                '--next', nxt, '--state', state, '--agent-id', aid]
        r = subprocess.run(args, cwd=REPO, text=True, capture_output=True)
        (HERE / ('stage14-save-' + solver + '.stdout.json')).write_text(r.stdout)
        (HERE / ('stage14-save-' + solver + '.stderr.txt')).write_text(r.stderr)
        if r.returncode:
            raise RuntimeError((solver, r.returncode, r.stderr))
        receipts.append({'solver': solver, 'state': state, 'actual_agent_id': aid, 'receipt': json.loads(r.stdout)})
        print(solver + ':' + state, flush=True)
    receipt.write_text(json.dumps(receipts, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'saved': len(receipts)}, ensure_ascii=False))


if __name__ == '__main__':
    main()
