from pathlib import Path
from fractions import Fraction as F
import json,hashlib
stage=Path(__file__).resolve().parents[4];repo=stage.parent.parent/'boss4-research';ev=Path('archives/unrelated-machines/tools/evidence/um-cycle-leaf-and-cardinality-primary');ws=Path('cleanup/workspaces/Boss4/r3-um-cycle-leaf-and-cardinality-primary')
def j(path,x):
 p=stage/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def s(path,x):
 p=stage/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(x.strip()+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
m=json.loads((stage/ev/'manifest.json').read_text());by={x['id']:x for x in m['records']};objs=json.loads((stage/ws/'object-paths.json').read_text());get=lambda name:next(x for x in m['records'] if Path(x['path']).name==name)
# Independent explicit description of hardcoded input points, no primary import/main invocation.
t=2;D=4;resources=[f'g{a}_{z}' for a in range(D) for z in range(D)]+[f'A{a}_{h}' for a in range(D) for h in range(t)];core={'M':{str(a):{f'g{a}_{z}':str(F(1,D)) for z in range(D)} for a in range(D)}};lam=[['M',str(a),str(F(1,D))] for a in range(D)]
for a in range(D):
 for z in range(D):
  c=f'H{a}_{z}';core[c]={'home':{f'g{a}_{z}':'1'},'parking':{f'A{a}_{h}':str(F(1,t)) for h in range(t)}};lam.extend([[c,'home','3/4'],[c,'parking','1/4']])
L={(c,st):F(v) for c,st,v in lam};z=[[c,st,u,str(L[c,st])] for c,states in core.items() for st,row in states.items() for u,p in row.items() if F(p)>0]
family={'tag':'family_t2','epsilon':'1','old_resources':resources,'core':core,'lambda':lam,'z':z,'materialization':'direct hardcoded mathematical input description, not primary execution'}
toy={'A':{'a0':{'u1':'1/3','u2':'1/3','u4':'1/3','u0':'0','u3':'0'},'a1':{'u1':'1/3','u2':'1/3','u4':'1/3','u0':'0'}},'B':{'b0':{'u2':'1/3','u3':'1/3','u5':'1/3','u1':'0'}}}
toylam=[['A','a0','1'],['A','a1','0'],['B','b0','1']];toyz=[['A','a0','u1','2/3'],['A','a0','u2','1/3'],['A','a0','u4','2/3'],['A','a1','u1','0'],['A','a1','u2','0'],['A','a1','u4','0'],['B','b0','u2','1/2'],['B','b0','u3','1/2'],['B','b0','u5','1/2']]
partial={'tag':'partial_z_zero_lambda_d0_d1_d2','epsilon':'2/5','old_resources':[f'u{i}' for i in range(6)],'core':toy,'lambda':toylam,'z':toyz,'materialization':'direct hardcoded mathematical input description, not primary execution'}
bc={'A':{'home':{'u':'1'},'alt':{'a1':'1/2','a2':'1/2'}},'B':{'park':{'b1':'1/2','b2':'1/2','unused':'0'},'home':{'u':'1'}}};bl=[['A','home','1'],['A','alt','0'],['B','park','1'],['B','home','0']];LL={(c,st):F(v) for c,st,v in bl};bz=[[c,st,u,str(LL[c,st])] for c,states in bc.items() for st,row in states.items() for u,p in row.items() if F(p)>0]
boundary={'tag':'beta_one_with_d2_and_zero_states','epsilon':'1','old_resources':['u','a1','a2','b1','b2','unused'],'core':bc,'lambda':bl,'z':bz,'materialization':'direct hardcoded mathematical input description, not primary execution'}
j(ev/'fixtures/three-hardcoded-leaf-input-points.json',[family,partial,boundary])
cycles=[]
old=json.loads((stage/get('optimal_hull_closed_cycle_audit.json')['evidence_path']).read_text())['independent_minimax_path']
for k,d in [(3,1),(3,2),(4,1)]:
 scale=4*k*k;a=4*k*(k-1);delta=4*(k-1);c=4;nextmachine=1;ends=[];names=[];blocks=[]
 for g in range(k+1):
  homes=list(range(nextmachine,nextmachine+(d if g<k else d+k-1)));nextmachine+=len(homes);rootjob=len(ends);ends.append([[0,delta+1 if g==0 else delta if g<k else a],[homes[0],scale]]);names.append([g,0]);es=[]
  for pos,home in enumerate(homes):
   es.append(len(ends));dest=homes[pos+1] if pos+1<len(homes) else 0;ends.append([[home,a],[dest,scale if dest else 2 if g==0 else c]]);names.append([g,pos+1])
  blocks.append([rootjob,es])
 bad=sum(1<<idx for idx,(g,q) in enumerate(names) if g==0);mask=bad;path=[mask]
 for g in range(1,k):
  gr,es=blocks[g]
  for idx in reversed(es):mask|=1<<idx;path.append(mask)
  mask|=1<<gr;path.append(mask)
 cycles.append({'k':k,'d':d,'machines':nextmachine,'time_denominator':scale,'jobs_two_finite_endpoints_in_integer_units':ends,'job_labels':names,'bad_mask':bad,'explicit_path_masks':path,'historical_result':next(x for x in old if (x['k'],x['d'])==(k,d)),'materialization':'independent direct endpoint/formula description from actual primary inputs; no run(),Dijkstra or exhaustive search called'})
j(ev/'fixtures/three-closed-cycle-original-inputs-and-paths.json',cycles)
j(ev/'fixtures/m2-three-monomial-negative-square.json',{'m':2,'n':3,'t':'3/2','zero_based_job_machine_literals':[[[0,0],[1,0]],[[0,0],[2,1]],[[1,1],[2,1]]],'coefficients':[1,-1,1],'gram':[['1/8','3/16','0'],['3/16','3/8','3/16'],['0','3/16','1/8']],'expected_square':'-1/8','identity':'direct separate arithmetic certificate from same moment definition, not original Bareiss rerun'})
formal=[
'archives/unrelated-machines/state/审查/闭环容量释放与单任务逃逸精确阈值冻结审查--审查.md',
'archives/unrelated-machines/state/审查/C2多切片的一般PSD与最小边界负平方--审查.md',
'archives/unrelated-machines/state/计算/经典槽恢复与双树动态规划的程序合同--计算.md',
'archives/unrelated-machines/state/障碍/一致条件叶边际仍无福利下界--障碍.md',
'archives/unrelated-machines/state/审查/条件叶Hallv3新MC独立重构--审查.md',
'archives/unrelated-machines/state/审查/条件叶Hall与共享汇点联合审查--审查.md',
'archives/unrelated-machines/state/审查/条件叶Hallv2路径投影与Qt家族五源读后--审查.md',
'archives/unrelated-machines/state/审查/条件叶Hall投影与一致边际四源证明读后--审查.md',
'archives/unrelated-machines/state/审查/配置剥离与联合匹配有限审计--审查.md',
'archives/unrelated-machines/state/审查/C2前缀满载与单位多切片有限审计--审查.md']
j(ev/'related-formal-material.json',[{'path':p,'sha256':sha(repo/p),'size':(repo/p).stat().st_size,'read_scope':'full bearing formal page in current or preceding same-task batches; current source-bearing sections compared; existing source dispositions not reopened','modified':False} for p in formal])
findings=[]
for rel,clause,newtext in [(formal[5],'6 个 `beta=1` 状态','6次(core-state,旧资源路径块)进入beta=1分支；本fixture只有4个不同core states'),(formal[9],'rank 4，tail nonzero index 为 11、15','正pivot阶段计数4（失败矩的总代数rank未由该分支求出），消元后tail非零位置为11、15')]:
 p=repo/rel;assert clause in p.read_text();snap=ev/'existing-formal-snapshots'/p.name;(stage/snap).parent.mkdir(parents=True,exist_ok=True);(stage/snap).write_bytes(p.read_bytes());findings.append({'old_object':rel,'old_sha256':sha(p),'snapshot':str(snap),'exact_old_clause':clause,'minimal_unapplied_suggestion':newtext,'primary_evidence':by['4a1b8fc533696fbb6811' if 'beta' in clause else '366efae229e35047de7f']['evidence_path'],'reason':'loop counter reuses the same state over resource blocks' if 'beta' in clause else 'zero-diagonal nonzero tail returns failure with rank=k pivot count, not completed elimination rank','applied':False})
j(ev/'comparison-findings.json',{'old_pages_modified':False,'findings':findings,'other_scope_relations':['Early v3 Exact-only candidate identity retained, later v2/v3 independent/author-proof read-after supplies general proof increment separately.','Raw old C2 whole5fe and final968 scope-sentence revision keep unchanged program hashes.','Conditional MC oldrootcanonical1dd is documentary historical hash only; no missing whole canonical bytes fabricated.']})
j(ev/'runtime-dependencies-and-run-binding.json',{'new_original_program_runs':0,'claim_tip':m['claim_tip'],'claim_capture':m['claim_capture'],'reason':'All five actual primary hashes match adequate completed historical runs, including independent root fresh-directory replays for both leaf writers. New verification only consumes fixed data/AST and direct arithmetic, not original mains.','bindings':[
{'id':'366efae229e35047de7f','source_sha256':by['366efae229e35047de7f']['sha256'],'old_record':get('c2_unit_multislice_gap_audit.json')['evidence_path'],'payload':'independent','historical_command':'python3 tests/audits/unrelated_machines/c2_unit_multislice_independent.py','actual_run':'c2_unit_multislice_gap_review.md actual independent fullm2/3/4 run and old aggregate exact output','historical_exit_code':None,'new_stdout':False,'imports':'standard library only','input':'fixedm2,3,4; complete matrices regenerated from stated moment formula, no external input'},
{'id':'14c27eb4d50f284464fa','source_sha256':by['14c27eb4d50f284464fa']['sha256'],'old_record':get('bundle_subdivision_audit.json')['evidence_path'],'payload':'reports.cardinality_final.json','historical_command':'python3 tests/audits/unrelated_machines/cardinality_closure.py','historical_exit_code':None,'new_stdout':False,'imports':'standard library only','input':'all hardcoded finite small-matrix,7target,boundary,VW/length2subdivision generators retained in primary; no input files'},
{'id':'5b9b83fcae1bb3c91099','source_sha256':by['5b9b83fcae1bb3c91099']['sha256'],'old_record':get('optimal_hull_closed_cycle_audit.json')['evidence_path'],'payload':'independent_minimax_path','historical_command':'python3 tests/audits/unrelated_machines/closed_cycle_escape_independent.py','historical_exit_code':None,'new_stdout':False,'imports':'standard library only, no other audit constructors','input':'(3,1),(3,2),(4,1) fulltwoendpoints; direct immutable fixture materialized separately without run()'},
{'id':'4a1b8fc533696fbb6811','source_sha256':by['4a1b8fc533696fbb6811']['sha256'],'old_record':get('conditional_leaf_consistent_marginals_independent.json')['evidence_path'],'replay_record':get('conditional_leaf_hall_root_replay_scope.json')['evidence_path'],'historical_command':'python3 /workspace/scratch/038d9dcc4cac/co-work-anl-boss11/tests/audits/unrelated_machines/conditional_leaf_consistent_marginals_independent.py','historical_cwd':'fresh empty scratch directory','written_relative_name':'sol_conditional_leaf_consistent_marginals_independent_audit.json','comparison':'byte equality with frozen MC output','historical_exit_code':None,'new_stdout':False,'imports':'standard library only; no author/v2 helper import','input':'threehardcoded core/lambda/z/resource fixtures preserved as direct descriptions'},
{'id':'b99a62dba759d15bdc1e','source_sha256':by['b99a62dba759d15bdc1e']['sha256'],'old_record':get('conditional_leaf_hall_path_projection_independent.json')['evidence_path'],'replay_record':get('conditional_leaf_hall_root_replay_scope.json')['evidence_path'],'historical_command':'python3 /workspace/scratch/038d9dcc4cac/co-work-anl-boss11/tests/audits/unrelated_machines/conditional_leaf_hall_path_projection_independent.py','historical_cwd':'fresh empty scratch directory','written_relative_name':'sol_conditional_leaf_hall_independent_audit.json','comparison':'parsed JSON equality; byte equality not required because machine set insertion order can differ','historical_exit_code':None,'new_stdout':False,'imports':'standard library only; no author/checker imports','input':'samefamilyt2andpartialpoint; no LP or exhaustive optimization'}
],'nonclaims':['No original source executions, missing oldexit/timing fabricated, or newprimary generated stdout.','Read-only data validation and direct endpoint/Gram arithmetic are separately labelled and not original run() calls.','Shared oldprimarydone sources held as comparisons only.']})
units=[('366efae229e35047de7f',objs[0],['fallingmoment/Booleanonehotmerge/allbasis matrix','denominatorLCM integer scaling/fullBareiss rowcolumnpermutations/exactdivision','negative diagonal versus zero-diagonal nonzero tail failure and rank-field meaning','fixedm2/3/4finiteoutput, nootherprimary constraint checks']),('14c27eb4d50f284464fa',objs[1],['closure legalinput assumption versus no genericvalidation','forcedload/residualdualbundles/strictthreshold allqmax tailreserve/synchronousdeletion/trace','allfinite smallassignment safety and targetmonotonicity count domains','denominatorproduct/scaledintegerbisection noactualscheduleoutput','VWheight/complete labelledparallel tasks/length2subdivision/currentknownOPT','all4boundaryfixtures and22familytargets, k4noexponentialoptimization']),('5b9b83fcae1bb3c91099',objs[2],['independent4k2scaledalltwoendpointconstruction','badmask/tinyreverseexplicitpath/allcapchecks','all2nvalues beforefullhypercube minimaxDijkstra earlygoalanyOPT1','B+c exactoutput andsettledversusallstates counts, finite10**20sentinel scope']),('4a1b8fc533696fbb6811',objs[3],['allhardcodedinputs/basiclambda/z/valuechecks/positiveneighborD0/1','beta/pi slacklast and qformula/ownlowerbound/beta1branch/zeroλ','global/conditional/MC checks with unusedresourceexcludedfromconditionalcolcounter','commonintervalfullmatchingmixtures/reproduction/supportbound','threefixturecounts beta1 state-resourcebranch6 not6uniquestates','fixedCWDwriter/fulloldJSONstdoutsummary and rootfreshreplayidentity']),('b99a62dba759d15bdc1e',objs[3],['v2fullcoefficientporttransfer includingzerojobroutes/designatedpartition','prefixgloballeaf flows andsingleownholeconditional matching noMC','thresholdtestresidualpreservation and lambda0','actualmatrix allstatejobs/selectors/finiteedges/completeassignments/loads','familyt2explicitbundles/FSLP point/full201jobcount','partialtoy4zeros/d0/1/2/completealltail18jobpeak2notoptimization','CWDwriter/oldparsedJSONequalityrootreplay actualscope'])]
j(ev/'source-semantic-units.json',[{'id':sid,'destination':dest,'units':u} for sid,dest,u in units])
notes={
'366efae229e35047de7f':('全文67行/2181B核b128SHA，逐项读falling、兼容基/矩、LCM和对称整数Bareiss、全部return失败/通过分支及固定m2/3/4 main。','与最终C2一般PSD正式页、原审查scope句5fe→968修正及真实oldindependent数组比；明确m2 rank4是早停pivot计数，未倒填m5或主程序linearconstraint检查。','独有完整原矩阵和整数消元实现/失败诊断已自足保存，给三项负平方另作直接算术资源；充分同SHA旧run复用，不重复一般PSD定理或虚称新run。'),
'14c27eb4d50f284464fa':('全文248行/9866B核ce176SHA，closure所有同步/残余/trace分支、有限全分配、scaled下界二分、4边界、VW树/细分、全部target与main输入完整读懂。','全文读bundle当前承重§3的一般安全/域单调/位复杂度及细分证明，核旧聚合cardinality_final全22family记录；与既有有限审计和经典树程序合同比较，接受不等可行/一般优化。','完整API合法前提/非通用validator、真实程序各统计口径/输入量词、原/细分θ与1界已自足保存；有限accepted_infeasible0不升级完整判定，不虚构k4枚举或新执行。'),
'5b9b83fcae1bb3c91099':('全文59行/2342B核cf257SHA，实际所有根/尾/内部端点整数缩放、badmask、显式逐环反向path、所有state值和heapminimax到任一OPT状态完整实读。','与闭环原冻结审查/一般B+c第一步证明、旧aggregate independent_minimax_path三例核对；区分全部25600状态/57结算、另一subsetDP91136范围和固定终点量词修补。','独立输入/路径/精确算法和有限哨兵范围完整保存，并静态物化3实例端点/路径供复核；旧足够真run复用，不冒称槽图/最优凸组合审计或一般路径求解。'),
'4a1b8fc533696fbb6811':('全文188行/8976B核d4b8SHA，3真实core/λ/z输入、holetransport公式、beta1/zeroλ/d0/1、全部MC/行列检查、完整matching区间混合与相对CWD写入/摘要完整理解。','全文比较新条款Exact-first原审查、作者v3greedy证明和后续proof正式页；核943177B完整MC输出及rootfreshbyte-replay，候选历史页状态不覆盖。','自足保存实际有除法q实现不同于作者greedy、每条件完整叶matching混合/共同edge边际非jointlaw、所有counter语义及beta1六分支澄清；全表独立验证不算原main新run。'),
'b99a62dba759d15bdc1e':('全文203行/10072B核a27SHA，lift全部正/零系数route、阈值b保持、globalprefix/单hole条件匹配、完整ordinarymatrix、201job族与18job toy及FSLP/所有输出完整读懂。','全文读v2Exact-first自足proof、后v3transport增量及早期candidate/finite页；核191593B完整P/assignment/flows与rootparsed-replay身份，区别weak单匹配和MC混合。','保全部原jobs/zeros/未选states、指定partition与finite非优化范围；硬编码输入另静态保全、P与所有flow实核，旧真run准确复用不以finitet2授一般定理。')}
receipts=[]
for sid,dest,u in units:
 a,b,c=notes[sid];receipts.append({'id':sid,'full_file_reviewed':True,'related_material_checked':True,'unique_content_accounted_for':True,'read_note':a,'comparison_note':b,'decision_note':c,'disposition':'integrated','targets':[dest,by[sid]['evidence_path'],str(ev/'manifest.json'),str(ev/'runtime-dependencies-and-run-binding.json'),str(ws/'数学自查.md')]})
j(ws/'semantic-receipts.json',receipts)
ids=['9b448a530454307c83ef','bc7fbb3d9e7d1df6050e','3d1c2add3e0914dc2348','203f58ab81cdd87d6563','be10ebd228c9c911c731'];inv={x['id']:x for x in map(json.loads,(repo/'cleanup/inventory.jsonl').read_text().splitlines())};nexts=[]
for sid in ids:
 hits=[]
 for p in (repo/'cleanup/checklists').glob('*.md'):hits.extend((str(p.relative_to(repo)),line) for line in p.read_text().splitlines() if sid in line)
 assert len(hits)==1 and 'unread' in hits[0][1] and '未认领' in hits[0][1],(sid,hits)
 e=inv[sid];nexts.append({k:e[k] for k in ['id','path','size','sha256']}|{'local_status':'unread/未认领','checklist':hits[0][0],'not_claimed_here':True})
j(ws/'next-candidates.json',{'status':'local snapshot only; parent must resolve live ownership and actualclaim','candidates':nexts})
s(ev/'README.md','''# 五份闭环、条件叶、C2与计数闭包原程序

original为五个inventory精确原件，comparisons/historical-runs保完整相关证明/旧输出，manifest逐源给完整hash/冻结位置；旁读不替其它source done。

本批新增原入口执行0。同SHA充分真实旧run及两leaf的rootfresh目录重放由runtime-dependencies-and-run-binding准确绑定。两个leaf原脚本会写CWD固定名，本批没有运行它们或覆盖任何旧输出。

fixtures为直接数学描述保全的3个旧leaf输入点、3个闭环原双端输入/显式path和m2负平方，不导入原程序。verify_delivery只核冻结字节、全部真实矩阵/赋值/flow/matching以及直接有理算术，不重新运行Bareiss/closure/Dijkstra/lift/audit。

comparison-findings与两旧页snapshot保beta1计数和失败rank字段的最小未应用澄清；已正确的后续证明页不覆盖。四篇正式资源分别保存原程序独有数学、实现/输入和有限范围；五receipt及自查/关系见workspace。''')
s(ws/'数学自查.md',r'''# 数学自查

5主源共765行已逐行完整读取，各size/SHA核inventory，所有实际输入/依赖为标准库/硬编码。只在next9ag实际pushed/Boss4/含指定5后正式处理，未用先前其它capture替代认领。

1. C2矩基完整为常数/一次/兼容不同job二次；Boolean合并与同job异色冲突为0。m2 union最多3不除(n)4零。整数Bareiss每次整除且同换行列；尾对角全0仍查全尾，false时rank字段不冒作完整代数rank。有限m2/3/4与主m5、一般PSD证明/其它约束核验分开。
2. Cardinality剩余R=T−forced是域单调关键；不同v束互不交，maxq不相加，candidate若原singleton需扣回自身。安全性不推出接受充分，monotonic域证明另完整保。下界二分按分母位长，不输出调度。7689/53823、115799和7232统计跨目标/fixture重复，finiteaccepted_infeasible0非一般判定；k4全树/细分从未枚举。
3. Closedcycle全双端时间按4k²单位；g0根δ+1/尾2、普通尾4、macro根a和h=d+k−1均不漏。bad仅g0环开；显式逐任务path峰B+c到S0，Dijkstra目标任一cap=1最优状态。先算全部2^n再结算8/12/37，10^20哨兵只对固定小例承担。代码不检验槽图/凸组合，其它aggregate字段不借用。
4. Leaf指定partition/D_positive邻居按group非state；显式zero jobs原端保留，zeroλ不删，d0unused/d1无叶。v2单matching不强加MC；v3有理q与beta1独立分支、λ0空mixfamily、每piece覆盖全部叶且不重port，MC只给每core相同edge平均，不给allcorelaw。
5. Counter：MC4state边界beta1=6是state-resource分支数；unused资源不计conditionalport列。family36corestates与v2全部116states不同；MC2880edge条目对应1440conditionalrows，不能混数。旧页只留最小未应用建议/snapshot。
6. 版本：旧Exact-only待证明页保历史；后续v2/v3 independent/authorproof与proofread-after已给一般数学层，程序有限证据不代它授定理。rootcanonical1dd是旧记录身份，缺失原字节不伪造。两leaf旧replay明确freshCWD，weakparsedJSONequal、MCbyteequal保真。
7. 证据：全部18冻结源/比较/run身份，943177B+191593B大表的每项flow/q/matching与P/σ/loads检查，3输入点/3闭环端点路径/负平方直接算术实核；不执行五原main或导入它们，不新增/虚构exit/timing/stdout。旧正式页不改。

一般UM算法/困难性、jointcorelaw、通用SDP/LP后端、外审与新颖性均未由本批有限源关闭。''')
s(ws/'关系与来源证据.md',r'''# 关系判断

| 参与对象 | 关系及共同前提/限制 | 证据 |
|---|---|---|
| C2独立入口 → 一般多切片PSD对象 | 实现/有限检查：只m2/3/4完整矩，不独立执行其它localizers或m5；失败rank计数澄清 | b128主源、36d聚合independent、最终C2review |
| Cardinality原实现 → bundle/细分障碍 | 实现安全/单调过滤与下界；细分简单双域无第一次删除，不能由接受推可行 | ce176主源、frozenbundle§3/5、528聚合 |
| Closedcycle入口 → B+c一般阈值 | 独立端点/有限全超立方体核验；到最优集合的minimax，不认证所有特定终点 | cf257、860独立minimax、6b83冻结review |
| v2leaf → v3MC | 后者加强同一条件leaf-edge平均，改用matching混合；不是重跑旧P优化或allcorelaw | a27/d4b两主源、rootreplay、Exact-first两稿 |
| v3数学候选 → 后续证明读后 | 历史状态增量：原candidate不倒改，q-table与greedy运输/一般projection/value在各自证明源承担 | 早期障碍页、v2五源/后续四源证明页、730作者Proof |
| 两leaf程序 → 完整ordinarymatrix | 仅v2实际201+18job全回填；MC只输出流/mixtures，不能借同域冒称其又优化schedule | e7c/409两个完整JSON原字节 |

属于阶段二入库时的关系判断，不复制旧超图、不为连通造边。旧页SHA在related-formal-material，两个最小措辞建议不应用到他人正文；其它来源仅comparison，不新增done。''')
s(ws/'delivery.md','''# 交付

五个正式认领原源全部实读并整理为四篇自足数学/程序资源。逐源semantic-receipts、原件与全部必要旧证据、数学自查和精确copy-files清单齐，由Root串行保存；此处未称已pushed正文。

新增原入口执行0，充分同SHA旧真实run复用。大表/输入/证书的只读验证与静态物化另标，未运行原Bareiss/closure/Dijkstra/audit/lift。旧页两建议不覆盖，候选/证明/有限证据/原先验状态分清。

下一五个实际本地未领候选在next-candidates.json；本代理无Git/claim/done/checkpoint/spawn操作。''')
print({'receipts':len(receipts),'leaf_inputs':3,'cycle_inputs':3,'new_original_program_runs':0})
