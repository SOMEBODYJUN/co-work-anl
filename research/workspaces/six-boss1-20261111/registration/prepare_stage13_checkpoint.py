"""Main serial restoration notes and real task states; no mathematical source edits."""
from pathlib import Path
import json
import subprocess

HERE=Path(__file__).resolve().parent
WS=HERE.parent
REPO=WS.parents[2]
RUN='six-boss1-20261111'
PREFIX='research/workspaces/'+RUN+'/'

def main():
    marker=HERE/'stage13-second-save-receipts.json'
    assert not marker.exists()
    additions='''### 全256型合账已经精确闭合；下一问改为真实分支共同实现

universal_union_wallet_lp/只做一次257列小LP，随后精确恢复：alpha=243427385229576983115/571565195660569935844≈.4258960956295508。它既是217原始行指定必要系统的精确最优值，也给原六人全域有效下界W≥alpha OPT6；没有固定16hist假设，含全部256型和最优并外客户。13个正整数预算与256列非负余项支付恒等式，K列严格抵消；17客户型余项零、239正。13原子加K的精确点不是完整SPE。Main逐217行/257列重放PASS，独立来源审核逐55769系数PASS；见main_universal_union_wallet_check.json与universal_union_wallet_audit/。不认领最佳已知下界改进，独有结果是指定预算系统的精确不足及清楚的缺失接口。

early_shared_x_menu_pair_closure/已冻结：394原始PAIR扣84旧副本及4逐点正项，306新行131721非零；其中42又由旧末BR和非负余项支付，可选264行116034非零同锥版本。9条31/25/19平均前缀投影已从旧436层付款，完整5040域与独立literal核验PASS；C菜单的非零Π保留，不能拿T/B的零罚替代。freeze888e5c76e84e8ccfb9cb0d6b0b20ea5898c7c139766d4c4af988c10d1298aca4。所有结论都没有宣称整锥不可再约简或全SPE充分。

新实际义务：(1) /root/universal_union_wallet_lp转入universal_max_label_completion/，用13个新会员变量补真正达到K的合法C，核54个actual和根钱包；已发现一个明确解析候选，待完整独立冻结。(2) /root/universal_true_x_tail独占universal_true_x_tail/，补四条真正强制X的780个尾部会员、52质量式及608原始行；只一次小phaseI，必须接精确完成或Farkas。(3) /root/early_shared_x_source_audit完成普遍审计后接root_near_equality_audit/，独立核Main新等号障碍：ROOT_NEAR=0是否迫强制最大C分支中间四覆盖均C，并由该分支第五源SAFE迫K≥23OPT6/63。此新命题尚待审完，不能提前登记为证明。Main同时亲推其定量版本。

截至21:06 UTC的check6，唯一云run43096304349仍queued、jobs=[]、artifacts=[]。未取到新数组，未重复派发，未本地绕过Actions-only输入。被冻结的23676与新全256型小系统是不同问题，不能混用点或目标值。

'''
    p=WS/'main.md'; s=p.read_text(); anchor='## Stage12历史入口：'
    at=s.index(anchor); s=s[:at]+additions+s[at:]
    s=s.replace('新early_shared_x_menu_pair_closure/仍在原builder及literal席续作','新early_shared_x_menu_pair_closure/现已完成并冻结，原builder及literal席已闭合')
    p.write_text(s)
    readme=REPO/'archives/customer-attraction/subarchives/six-providers/workspaces/Boss1/README.md'
    readme.write_text('''# Boss1：恰六人半覆盖

RUN：six-boss1-20261111；Boss1；分支rebuild/research-v2；存档customer-attraction；子档six-providers。

## 恢复入口与确认的远端上限

实际clone：/workspace/scratch/b0fef5ec503f/co-work-anl-boss1。工作区research/workspaces/six-boss1-20261111/。先读main.md顶部Stage13、spec.json及实际稿件/输入/输出，再research resume six-boss1-20261111核原证据、未答反馈和事件。环境丢失按同Boss、分支、存档、子档start --resume。原题仍OPEN，checkpoint后继续Main循环。

写此入口时最后确认pushed是b96dbcdfe0dec963bbaf91f3a9a2f0ed597467ad，收据checkpoints/stage12.json，公屏seq82。Stage13须以随后实际checkpoint的pushed回执确认；其前只属本地。

## 当前数学与边界

W10=.4941319647988424的22297×21021固定16hist必要系统有完整匹配有理原对偶；W9/W10整个最优面分别被MC6/AP39精确排除。证据maxb_augmented_lp/full_lift/recovery/及early_ap_optimum_face/facial_zero_closure/。低于half的固定域点不是SPE反例，也不是全域下界。

Main同一actual前四最大f_P标签X的覆盖并前缀界：对任意六合法标签覆盖并O，C_i u_i−(C_i−1)Σ_X1/(b_i+7−i)≥(1/6)Σ_O[x/(b_i+7−i)+(1−x)/(b_i+1)]，C=(31,25,19,10)。六真查询平均d/6可逐客户减弱到o/6，O不成为新合法行动。一般平均版本另有显式Π。正式覆盖并父档引理已本地登记并bind/check；先前C*族完整2r权唯一性也升级v2。大X粗half条件被旧W≥(889K+6OPT6)/900支配，不能认领扩大已证区域。

universal_union_wallet_lp/得到全256型217原始行的精确最优alpha=243427385229576983115/571565195660569935844≈.4258960956295508；13正钱包与全256型非负余项亦给普遍W≥alpha OPT6。不认领最佳界改善。Main精确重放及universal_union_wallet_audit/独立全部55769系数审核PASS。13原子必要系统点不是SPE，接下来的实际义务是把遗漏的真实合法标签和共享后继补齐或严格排除。

root_x_shared_queries/冻结同一η的42/236真查询；x_conditioned_zz/冻结5580零新列条件上界，必须在明确下一点固定core重算2790min及39预算；opt6_shared_x_exchange/的70候选全部旧行锥冗余。early_shared_x_joint/的1920μ、128质量式、436约束及36投影已冻结；early_shared_x_menu_pair_closure/的306新PAIR（可进一步删42BR冗余为264）和9平均投影也已冻。它们都不是全目录全历史充分条件。

## 正在接续的具体任务

- /root/universal_union_wallet_lp：新目录universal_max_label_completion/，13变量真实最大大小标签C的明确候选与54行精确完成核验。
- /root/universal_true_x_tail：同名目录，四源真实强制X的780变量、52质量式、608预算，唯一小phaseI及精确证书。
- /root/early_shared_x_source_audit：普遍审计已冻；新root_near_equality_audit/核Main的ROOT_NEAR等号结构及K≥23OPT6/63障碍，未审定前不当结论。
- Main亲自合账、检查承重步骤、推ROOT_NEAR定量版本；串行RUN/registry/Git。

## 唯一云端计算

C-six-boss1-common-x-joint-23676-01；run43096304349；source b96dbcdfe0dec963bbaf91f3a9a2f0ed597467ad；创建20:28:55 UTC。21:06 UTC的check6仍queued，jobs/artifacts均空。没有新数值点、没有重复派发。

common_x_joint_lp/final/输入冻23676×21021，3313758非零；10277core含420真实y，10744aux。取回真实ZIP/数组后先核request/source/六输入/执行源码/scales，再交原/root/common_x_joint_lp做freeW有理原对偶及210组八格核验。严禁把420真实y作独立min重置。恢复上限只到实际确认pushed内容。
''')
    assignments='''# Stage13第二轮实际义务

同Boss1/RUN。Main /root统一RUN、登记及Git；全部旧冻结材料只读。

已闭合：universal_union_wallet_lp与universal_union_wallet_audit；early_shared_x_menu_pair_closure及literal。各自原始发现、源码、输入/输出、精确分数及freeze在同名包。

新实际followup /root/universal_union_wallet_lp → universal_max_label_completion/与.md：固定明确SHA的13原子点，真实C取到K，actual SAFE/MAX/MX/RC、ROOT_RIG、六槽OPT cap，至多一次小LP，优先检查已写明确候选。

新实际spawn /root/universal_true_x_tail（fork_turns=none）→ 同名目录/md：同固定点四条真强制X分支，780μ、52质量式、608真预算，至多一次phaseI，精确完成或Farkas；若提出普遍切必须补全所有256型消元。

新实际followup /root/early_shared_x_source_audit → root_near_equality_audit/与.md：Main提出的ROOT_NEAR=0强制中间四覆盖C和K≥23O/63的独立来源证明；未审完不登记。
'''
    (WS/'assignments/stage13-second-round.md').write_text(assignments)
    tasks=[
      ('universal_union_wallet_lp','universal_union_wallet_lp.md','closed','/root/universal_union_wallet_lp','原217行精确不足闭合；新真实最大标签义务在独立任务名接续。'),
      ('universal_union_wallet_audit','universal_union_wallet_audit.md','closed','/root/early_shared_x_source_audit','全来源及55769系数核完，13预算普遍恒等式成立；不重复旧审计。'),
      ('early_shared_x_menu_pair_closure','early_shared_x_menu_pair_closure.md','closed','/root/early_shared_x_joint','394候选、306新行、42直接BR冗余、9平均投影均已独立核完。'),
      ('early_shared_x_menu_pair_literal_audit','early_shared_x_menu_pair_closure.md','closed','/root/early_shared_x_joint/literal_audit','字面209920系数和937600配对核完，旧29冻结文件不变。'),
      ('universal_max_label_completion','assignments/stage13-second-round.md','working','/root/universal_union_wallet_lp','检查真实C补全54行并冻结；只固定明确13原子点，不当SPE。'),
      ('universal_true_x_tail','assignments/stage13-second-round.md','working','/root/universal_true_x_tail','唯一780变量phaseI后接精确完成或Farkas，保52质量和真实枝内共同身份。'),
      ('root_near_equality_audit','assignments/stage13-second-round.md','working','/root/early_shared_x_source_audit','独立核ROOT_NEAR等号结构与K>=23O/63，再回Main亲核。'),
      ('main','main.md','working','/root','先确认Stage13 pushed；继续真实分支与根等号定量付款，云run尚queued。'),
    ]
    receipts=[]
    for solver,note,state,aid,nxt in tasks:
        cmd=['python','work.py','research','save',RUN,'--solver',solver,'--profile','full','--note',PREFIX+note,'--next',nxt,'--state',state,'--agent-id',aid]
        r=subprocess.run(cmd,cwd=REPO,text=True,capture_output=True)
        (HERE/('stage13-second-save-'+solver+'.stdout.json')).write_text(r.stdout)
        (HERE/('stage13-second-save-'+solver+'.stderr.txt')).write_text(r.stderr)
        if r.returncode: raise RuntimeError((solver,r.returncode,r.stderr))
        receipts.append({'solver':solver,'state':state,'actual_agent_id':aid,'receipt':json.loads(r.stdout)})
    marker.write_text(json.dumps(receipts,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'saved':len(receipts),'states':[r['solver']+':'+r['state'] for r in receipts]},ensure_ascii=False))

if __name__=='__main__': main()
