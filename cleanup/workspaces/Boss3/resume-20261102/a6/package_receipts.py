"""Serialize substantive per-source decisions; does not run mathematics."""
from pathlib import Path
import json

ROOT = Path('/workspace/scratch/cd4305a146e6')
REPO = ROOT / 'co-work-anl-boss3'
HERE = Path(__file__).resolve().parent
EVIDENCE = 'archives/customer-attraction/tools/evidence/tree-inputs-and-padding-resumed-boss3'
FORMS = {
    'counter': 'archives/customer-attraction/state/反例/不交双前缀保留三人尾策略的末位偏离--反例.md',
    'program': 'archives/customer-attraction/state/程序/真实完整策略的七百四十七行输入映射与核账户--程序.md',
    'review': 'archives/customer-attraction/state/审查/五人覆盖重置与证书活跃原行的独立语义复核--审查.md',
    'resource': 'archives/customer-attraction/state/资源/共享最大铰链与十单位策略的原独立回放--资源.md',
}
NOTES = {
    'audit_full_actual_branch_inputs.json': (
        '全文186492B全部顶层及3输入/4真H：完整路径/菜单、22单位atoms、55AP账户、42floor概况和4×747 exact_row_slacks同键联合列读；空case全部747值零。',
        '保3972完整策略比较与2988映射不同口径、两个H不合并、oldcap1/3不能封新孩子1/2；非只读min/PASS，非当前重跑。', 'program'),
    'audit_full_actual_branch_inputs.py': (
        '全文18127B：全ordered策略/真follow及全IC、OPT/M/三族/L菜单/atoms、被测747系数与独立semantic、三真IC税及Q-AP核、完整payload/main。',
        '自足给747组行计数/合法节点和AP2账户；明确导被测rows的有限输入语义QA，不称全实现无共享、一般half或全域oracle证明。', 'program'),
    'full_actual_branch_input_QA.md': (
        '全文2273B：3输入4H、3972/2988、真floor/三IC税/AP、祖先旧cap错误、两个last查询方向及完整输出/接受限制。',
        '与完整代码/JSON及同SHA31/781策略对照，保真实输入映射用途，不重复成熟成功扫描。', 'program'),
    'audit_generic_padding_failure.py': (
        '全文2397B：六客21策略/单位展开/原completion/63非self IC、D=2u1及32单位最后4至14/3、独立性/报告输出。',
        '保核心真SPE和五人拟定叶失败不同身份，手算自足证明，不误称五人half反例或十客真证书。', 'counter'),
    'build_generic_padding_failure.py': (
        '全文1699B：规范四import、四客户类型/3人、133全证书及canonical、D14/3/三倍单位化、全部payload、无guard写出。',
        'canonical只认证核心，五人拟定尾失败来自最后偏离；不将构证器本身当五人SPE认证。', 'counter'),
    'generic_padding_failure_exact.json': (
        '全文3099B：六客输入、terminal_counts与全部21有序动作、核心133/各利润、D/单位化、两个末收益/差及canonical21/63。',
        '全部动作和全阶段收益表进正文，保23与32不同平局；32单位不存在保持44133叶的SPE，未判其余真SPE福利。', 'counter'),
    'generic_padding_failure_independent_audit.json': (
        '全文396B所有字段：true核心、独立性、6客/21/63/min0、32单位、规定4/改14/3/改善2/3。',
        '保历史成功和精确整数实现，不倒填A5当时只读base注释的认证范围，不新增数学执行。', 'counter'),
    'coverage_reset_independent_review.md': (
        '全文5147B：提示/作者读取先验、同H真η、BNS-eta/G1五项精分、原末遗漏/外fresh/24η总恒等式、净福利/旧返还/零η边界。',
        '成熟direct已保RESET，新增承接独审精细G1=7GD/4+DQ/4+xiR+GammaR+xiE；不改B4、不重跑点态audit或认证24锐性。', 'review'),
    'half5_active_row_semantics_review.md': (
        '全文6507B：原读取顺序、强PAIR三IC/20对、共同末价、PC3金额、PC2/3源系数/索引、BG/DEEP/MAXROOT/pairO及外舍入/共享d/四角。',
        '与成熟53行/复核及当前源码定点比较，保PC2 generic第四位TAX门槛缺口而当前五记录无TAX；不把原语义审查叫第二主整数核。', 'review'),
    'audit_hinge_independent.py': (
        '全文3766B：完整输入路径、14参数1512条件maxh、57原子字段/系数/W/O/长负分数及5倍、旧5421值仅schema/min、全部输出。',
        '1512按(p,d,j,t)条件而A5的3024逐h，来源及接受t1分离明确；旧值schema不等于5421原式重构，未重跑。', 'resource'),
    'hinge_independent_review.md': (
        '全文7286B：先提示旧BNS后未读作者新稿独推、全真分支金额/边界、后作者比对、57点/5421值限制、18条k2/3/4未全重演。',
        '保独立性先验及真正第三位t1接受范围，BNS母关系非新机制，旧系统可行性和全球新颖性未由本文另认证。', 'resource'),
    'hinge_independent_audit.json': (
        '全文6943B：全部顶层/14参数/1512/57、长mass/W/O/slack与5倍、5421/min0、完整57个p/d/j/u/c记录逐项读。',
        '和完整855090B输入绑定，不拿小报告代原子质量；指定必要点分离不同于SPE/half反例。', 'resource'),
    'audit_terminal_share_padding.py': (
        '全文2777B：原781动作域/标签/单位展开、所有有序真completion、3124非self、5实际节点全25利润/叶、OPT/C2、无guard输出。',
        '复用A5同SHA完整证书不重扫，保不同独立实现和实际偏离显示，不只转述实际利润。', 'resource'),
    'terminal_share_padding_independent_audit.json': (
        '全文3711B：781/3124/min0/zero380、各利润/W/OPT/C2及五个actual_history_rows全部history/chosen/25收益/25完整终局。',
        '全25个偏离叶表承接，明确不能以在轨显示替781离轨IC；3905含self与3124口径相容，当前核0次。', 'resource'),
    'two_real_weighted_branches.py': (
        '补领全文7501B：两个context/全部747rows、有理正权projected_cut、18cross rows、先边缘后有条件64joint/1512行、归因门槛/输入/输出/时间/hash/全部import。',
        '不仅清rows调用，完整保原联合LP合同；float可行不是exact实现，单边失败不作新joint归因，严格有理max8/64负值才分离；无run报告不造结果。', 'program'),
    'exact_projected_hinge.json': (
        '补领完整855090B：全部顶层/五参数、57原子八字段及长质量逐项读；5421命名有理旧值全量数据消费、行族/零支持完整记录及原字节保全。',
        '完整点与5421存值不遗漏；891c文件SHA/e192上游/3d44作者code/A5的29e0点各别，未声称重新推导5421旧行表达式或重演作者18行。', 'resource'),
}
COMMON = ('完整比较A5铰链/十客真五人策略/根审计、成熟direct RESET与独有31节点策略、53活跃行和复核纠错；'
          '实读同SHA RESET原MD/两单例31动作JSON/十客输入，并定点读PC2/PC3门槛和源字段、PAIR索引源码。'
          '保真全树、有限行QA、辅助必要点、32单位拟定失败各身份，已有成功审计不重复。')


def main():
    rows = json.loads((ROOT/'boss3-session/a6-sources.json').read_text())
    rows += json.loads((ROOT/'boss3-session/a6-extra-sources.json').read_text())
    receipts = []
    for x in rows:
        read, decision, target = NOTES[Path(x['path']).name]
        receipts.append({'id': x['id'], 'full_file_reviewed': True,
            'related_material_checked': True, 'unique_content_accounted_for': True,
            'read_note': read, 'comparison_note': COMMON,
            'decision_note': decision+' 原数学程序/新数学checker/LP/BI/随机本批均0，原件size/SHA核符。',
            'disposition': 'integrated', 'targets': [FORMS[target], EVIDENCE+'/README.md']})
    (HERE/'semantic-receipts.json').write_text(json.dumps(receipts, ensure_ascii=False, indent=2)+'\n')
    delivery = {'source_count': len(rows), 'source_bytes': sum(x['size'] for x in rows),
        'initial_claim_remote_tip': '7b037c53ef561b353d3a449937c51ac921ffc20e',
        'extra_claim_remote_tip': '7980380e6d118e7be81eb409e0847c3fb01dd66f',
        'formal_objects': list(FORMS.values()),
        'checkpoint_paths': list(FORMS.values())+[EVIDENCE, str(HERE.relative_to(REPO))],
        'receipt_file': str((HERE/'semantic-receipts.json').relative_to(REPO)),
        'original_clean_show_calls': 14, 'original_clean_show_successes': 14,
        'original_math_program_runs': 0, 'new_math_checker_runs': 0, 'LP_BI_random_runs': 0,
        'remaining_in_assigned_scope': 0,
        'parent_actions': 'Review four objects/16 receipts, checkpoint/pushed before done; internal agent no Git write/claim/checkpoint/done.'}
    (HERE/'delivery.json').write_text(json.dumps(delivery, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps({'primary': len(rows), 'bytes': delivery['source_bytes'], 'receipts': len(receipts)}))


if __name__ == '__main__':
    main()
