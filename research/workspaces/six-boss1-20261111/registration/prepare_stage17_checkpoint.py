"""Save the actual closed results and active next obligations without touching frozen inputs."""
from pathlib import Path
import json
import subprocess
import shutil

P=Path(__file__).resolve().parent
WS=P.parent
REPO=P.parents[3]
RUN='six-boss1-20261111'
assert not (P/'stage17-save-receipts.json').exists()
assert json.loads((WS/'main_all_source_joint_check.json').read_text())['status']=='PASS'
assert json.loads((WS/'actual_source2_fixed_C_lift/freeze_manifest.json').read_text())['optimizer_calls']==0
assert json.loads((REPO.parent/'map-stage17-integration-checkpoint.stdout.json').read_text())['pushed_head']=='3d2b34b8e72754f31e13e9e2c15c8f89fe090e32'
shutil.copyfile(REPO.parent/'map-stage17-integration-checkpoint.stdout.json',WS/'checkpoints/stage17-map-integration.json')
note=WS/'stage17-current.md'
s=note.read_text()
s=s.replace('写本说明时 assemble 正在运行，尚未把新索引声明为已推送；三个旧 Boss1 3A 任务保持原状。',
'''本次十四条关系已通过正规 assemble 接回 canonical，包含此前漏索引的十三条，实际边文件总数为 2127。随后 Main 写了准确的局部整合审读，保留旧 pending 与同期未审变化；三派生文件及本批审读已确认推到 `3d2b34b8e72754f31e13e9e2c15c8f89fe090e32`。全仓 final check 仍报告 18 个未纳入当前冻结基线的新正式路径，本批不声称全仓终验完成；三个旧 Boss1 3A 任务保持原状。研究 clone 随后仅 fast-forward 这些已确认推送且与数学工作区不相交的 tracked 路径，没有再 stash/reset/清理新工作。''')
s=s.replace('`visible_maximum_joint_v3/` 正按原合同准备 1050 原行：', '`visible_maximum_joint_v3/` 已按原合同冻结 1050 原行：')
s=s.replace('它尚无求解授权。Main 新派的 `all_source_joint_reweighted_safe/` 推广全部内部 SAFE 和源 IC 权；第一源的参数域较宽，其余源分别保原有完整边界。该包正在推导/生成，尚未冻结审定的部分不作为已核输入。若完整新族及时完成，将在已冻结 1050 上续加，直接做一次更完整的 LP，1050 本身保留未求解状态。',
'''它明确保留 `NO_SOLVE_INTERMEDIATE_INPUT`，输入 SHA `c5ddba49b71303083b07b96f90888d56f11b291d7c307f0c3e8280b7385d280e`，manifest `f7cf345480b2d0c328a12a3485b0ad9d66c260f611b6c6e5253a16b361c857f9`。

`all_source_joint_reweighted_safe/` 已完成全部内部 SAFE 与源 IC 权的普遍推广，四源参数域分别有 39、16、8、4 个顶点，31 个真面；原源权为 `a=25+Theta-s`，一般 T 的大小项完全保留。第一源额外范围为 `s<=15+5theta_j`，最大 s 为 `1070/63`、最小 a 为 `605/63`，均唯一在四个 theta=`25/63`。Main 独立重新求交所有顶点、核全部 8064 余项、444 minimum 与 536×513=274968 系数，及 source2,C 的 8208 列模质量等式身份，全部 PASS。完整 family SHA `c8a40df9458e2add557ef14b8282880a1d14b05d55238ecf0715f63968907c18`，proof `1a72e75cbcfa36d215c5030d1b86426746d068c1afc806894272b5c9aca60f70`，manifest `3f08170af4b678688317bdebfd8468a8c62e8a801923b3e86f7612a8873825eb`。

下一输入 `visible_maximum_joint_v4/` 正准备在完整 1050 上追加这 536 行，总 1586 raw、513 非负列及两等式。新增数值除数全为 25，K 原列保持 c_i，所有旧行、重复和零型保留。`visible_maximum_joint_v4_solve/` 只准备下一求解骨架，必须等 Main 精确输入释放，当前没有优化授权。''')
s=s.replace('`actual_source2_fixed_C_lift/` 正准备无点绑定的固定 C 真实分支模板。', '`actual_source2_fixed_C_lift/` 已冻结无点绑定的固定 C 真实分支模板。')
s=s.replace('当前不绑定已排除的 1002/1003 点，不消耗 phase-I。',
'''当前不绑定已排除的 1002/1003 点，不消耗 phase-I。Main 全文实读完整推导并独立核当前 21 条 checksum；有效新冻结 manifest 为 `10012e13e443042a6be1150277207c67bfd222c7e0967e9b3818fd4a49c54f61`。首次两份收尾清单因 Main 同步与写入竞态缺失，已保存原 SHA 和事件，仅重新生成元数据；不声称原清单逐字恢复，没有数学输入或求解重跑。1050 首次 checker 的同一竞态失败亦保留，输入未变，仅重放确定性 checker。详见 `stage17_sync_recovery/`。''')
s=s.replace('已闭合 NS5 独审及 16 端点族；继续全 actual 源、多内部 SAFE 和源权重配的参数域与完整纯标签行，0 优化。',
'''已闭合 NS5、16 端点及一般源 536 行。下一义务 `all_source_ordered_joint_menu/`：外层强制 Q_k，内层对同菜单 l!=k 的五查询平均，保准确重数 d 后再取全尾 minimum，检查是否能改进已失败的独立 outermean；0 优化。''')
s=s.replace('已闭合跨源第五 SAFE 族；准备 1050 原行输入与排除证据，0 优化。新输入逐项获 Main 复核前不释放求解。',
'''已闭合跨源第五 SAFE 及 1050 未求解中间输入；准备完整 1586 输入，0 优化。新输入逐项获 Main 复核前不释放求解。''')
s=s.replace('已闭合 1003 唯一 LP、全原对偶与整面排除；准备 734 固定 C 无点模板，0 新优化。',
'''已闭合 1003 唯一 LP、全原对偶与整面排除及 734 固定 C 无点模板；只准备 1586 求解骨架，等待 Main 输入 SHA 与一次明确释放，0 新优化。''')
s=s.replace('完成当前正规 mapper 集成；随后审核更强完整输入并释放唯一求解。', '当前正规 mapper 集成已 pushed；随后审核更强完整输入并释放唯一求解。')
note.write_text(s)
main_path=WS/'main.md'
old=main_path.read_text()
headline='# Boss1：六人共同目录跨真实分支研究\n\n'
assert old.startswith(headline) and '# Stage17：' not in old
main_path.write_text(headline+s+'\n## 此前阶段的历史入口\n\n'+old[len(headline):])
readme=REPO/'archives/customer-attraction/subarchives/six-providers/workspaces/Boss1/README.md'
readme.write_text('# Boss1：恰六人半覆盖\n\n'+s)
(WS/'assignments/stage17.md').write_text(s)
tasks=[
('main_source2_maximum_nested_safe_audit','main_source2_maximum_nested_safe_audit.md','closed','/root/early_shared_x_source_audit','128态、4096菜单、513列及8192付款独审已闭合。'),
('visible_maximum_joint_v2','visible_maximum_joint_v2.md','closed','/root/visible_maximum_joint_solve','1003输入已被指定求解恰消费一次；不得重跑。'),
('visible_maximum_joint_v2_solve','visible_maximum_joint_v2_solve.md','closed','/root/visible_maximum_joint_solve','全1003/513/2准确原对偶及全最优面排除已闭合，Main完整重放。'),
('source2_joint_internal_safe','source2_joint_internal_safe.md','closed','/root/early_shared_x_source_audit','完整四参数域和16端点已冻，Main亲核全部系数。'),
('all_source_nested_safe_family','all_source_nested_safe_family.md','closed','/root/visible_maximum_joint','36候选准确；4outer弱、C2模等式重复明确。'),
('all_source_joint_reweighted_safe','all_source_joint_reweighted_safe.md','closed','/root/early_shared_x_source_audit','67顶点536行完整冻结，Main另核8064态/274968系数。'),
('actual_source2_fixed_C_lift','actual_source2_fixed_C_lift.md','closed','/root/visible_maximum_joint_solve','734隐藏加17显式路由已冻；固定C删除外q矩，UNBOUND，0优化。'),
('visible_maximum_joint_v3','visible_maximum_joint_v3.md','closed','/root/visible_maximum_joint','1050已冻但NO_SOLVE；直接准备更强1586，禁止消费此中间输入。'),
('visible_maximum_joint_v4','assignments/stage17.md','working','/root/visible_maximum_joint','准备1586raw/513cols/2eq完整输入，0优化。'),
('visible_maximum_joint_v4_solve','assignments/stage17.md','working','/root/visible_maximum_joint_solve','仅建精确恢复/完整面骨架，等Main input SHA和一次明确释放。'),
('all_source_ordered_joint_menu','assignments/stage17.md','working','/root/early_shared_x_source_audit','用同一六菜单的30异索引结构保重数d，再全尾投影；0优化。'),
('main','main.md','working','/root','确认本轮pushed，审1586 input后释放唯一LP；并亲推有序内外菜单共同付款，接回主正文。')]
results=[]
for solver,nn,state,agent,nxt in tasks:
    argv=['python','work.py','research','save',RUN,'--solver',solver,'--profile','full',
          '--note',f'research/workspaces/{RUN}/{nn}','--state',state,'--agent-id',agent,'--next',nxt]
    result=subprocess.run(argv,cwd=REPO,capture_output=True,text=True)
    (P/f'stage17-save-{solver}.stdout.json').write_text(result.stdout)
    (P/f'stage17-save-{solver}.stderr.txt').write_text(result.stderr)
    assert result.returncode==0,(solver,result.stderr)
    results.append({'solver':solver,'state':state,'agent':agent,'receipt':json.loads(result.stdout)})
    print(solver+':'+state,flush=True)
(P/'stage17-save-receipts.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
