"""Continue after a wrong v4 summary path; preserve all previous save receipts."""
from pathlib import Path
import json
import subprocess

HERE=Path(__file__).resolve().parent
WS=HERE.parent
REPO=HERE.parents[3]
RUN='six-boss1-20261111'


def main():
    output=HERE/'stage15-save-receipts.json';assert not output.exists()
    receipts=[]
    for solver in ['v3_optimum_joint_face','maximal_root_tail_wallet_v2','maximal_root_tail_wallet_v2_audit','actual_source2_opt_requery','actual_source2_opt_requery_audit']:
        p=HERE/f'stage15-save-{solver}.stdout.json'
        receipts.append({'solver':solver,'state':'closed','receipt':json.loads(p.read_text()),'preserved_original_save':True})
    note='\n### Stage15保存前追加状态\n\nsource31_family_audit已完整冻结，正文SHA e21c6abfe0882fb57d216c9259e49b4ff08e809e708258d9800cb4d5985bc4b1，冻结清单4337943a2ad2cc6f4d42590d404392e793de417120cd93efc26cc7e1738ce35d。该义务闭合。新独立代理/root/background_projection_audit（fresh fork_turns=none）只审已冻BG投影的继承合同、12288表项和257列；写background_projection_audit/，0优化器，不改旧包。v5唯一LP授权不变。\n'
    for p in [WS/'main.md',WS/'assignments/stage15.md']:
        old=p.read_text();assert '### Stage15保存前追加状态' not in old
        if p.name=='main.md':
            pos=old.index('## Stage14历史入口：');old=old[:pos]+note+'\n'+old[pos:]
        else:old+=note
        p.write_text(old)
    tasks=[
      ('universal_union_wallet_v4','universal_union_wallet_v4/summary.md','closed','/root/universal_union_wallet_lp','225精确原对偶及后验诊断已冻；Main全行列复核完成。'),
      ('source31_family_audit','source31_family_audit.md','closed','/root/early_shared_x_source_audit','456态/60min/82240列独立通过并冻结，停止本义务。'),
      ('v4_source2_identity','assignments/stage15.md','working','/root/universal_true_x_tail','0优化器完成225整面和真实A5分支身份，精确候选已核，正在证明冻结。'),
      ('universal_union_wallet_v5','assignments/stage15.md','working','/root/universal_union_wallet_lp','已释放唯一546raw/257col LP，先前检正缩放后精确恢复，不静默重试。'),
      ('background_projection_audit','assignments/stage15.md','working','/root/background_projection_audit','fresh独立审BG已有合同与全257投影，0优化器，完成即冻。'),
      ('main','main.md','working','/root','Stage15确认pushed后立即正式正文/登记与缺失图集成；接v5精确点继续true-source2。')]
    for solver,note,state,aid,nxt in tasks:
        cmd=['python','work.py','research','save',RUN,'--solver',solver,'--profile','full','--note',f'research/workspaces/{RUN}/{note}',
             '--state',state,'--agent-id',aid,'--next',nxt]
        result=subprocess.run(cmd,cwd=REPO,capture_output=True,text=True)
        (HERE/f'stage15-save-{solver}-continued.stdout.json').write_text(result.stdout)
        (HERE/f'stage15-save-{solver}-continued.stderr.txt').write_text(result.stderr)
        if result.returncode:raise RuntimeError((solver,result.stderr))
        receipts.append({'solver':solver,'state':state,'actual_agent_id':aid,'receipt':json.loads(result.stdout)})
        print(solver+':'+state,flush=True)
    output.write_text(json.dumps(receipts,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':main()
