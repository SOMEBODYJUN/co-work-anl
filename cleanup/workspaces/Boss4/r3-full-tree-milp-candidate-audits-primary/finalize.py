from pathlib import Path
import hashlib,json,subprocess,os

S=Path(__file__).resolve().parents[4];R=Path('/workspace/scratch/37f0f9248cfc/boss4-research')
E=S/'archives/customer-attraction/tools/evidence/full-tree-milp-candidate-audits-primary'
W=S/'cleanup/workspaces/Boss4/r3-full-tree-milp-candidate-audits-primary'
A='archives/customer-attraction/state/等价/实际玩家归一的全树效用向量表示--等价.md'
B='archives/customer-attraction/state/计算/自由终局逐人归一模型的候选与对偶复核--计算.md'
C='archives/customer-attraction/state/反例/逐人末位二倍保底的七客户反例--反例.md'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,v):
    p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
primary=json.loads((E/'primary-manifest.json').read_text())['sources']
deps=json.loads((E/'dependency-manifest.json').read_text())['sources']
runtime=json.loads((E/'runtime-manifest.json').read_text())['sources']
dump(E/'source-manifest.json',{'primary_count':5,'primary_bytes':150796,'runtime_input_count':8,'runtime_input_bytes':107270,
 'comparison_count':6,'comparison_bytes':53141,'runtime_code_dependency_count':5,'runtime_code_dependency_bytes':46042,
 'unique_raw_files':24,'unique_raw_bytes':357249,'only_claimed_intersection_is_primary':True,
 'sources':primary+deps+runtime})

related={
 'archives/customer-attraction/state/等价/完整有序历史终局选择的整数投影--等价.md':'全文比较总质量归一、固定q/roota、M1/终局selector，与本u_j1/自由路径/全玩家向量M=m不同，不移用其run/审查身份。',
 'archives/customer-attraction/state/计算/完整终局选择的有限回归与恢复边界--计算.md':'重新单文件全文读6508B/680LP/20MIP记录及恢复/距离边界；不把此同名代码已执行当作本6376B已运行。',
 'archives/customer-attraction/state/计算/完整树保存运行与恢复版本边界--计算.md':'重新单文件全文读五点266有序节点1120非自身、旧恢复cut/版本行数，未共用固定策略图或数值bounds。',
 'archives/customer-attraction/state/定理/固定完整策略的客户重数锥--定理.md':'此前全文同SHA；固定Γ/精确原始对偶/标签接口/全策略量词，用新归一行n替W。',
 'archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md':'此前全文同SHA；严格SET目录与同覆盖标签扩展区分；七客户四覆盖互异直接属于原模型。',
 'archives/customer-attraction/state/反例/笛卡尔银行目录的逐人分数门槛反族--反例.md':'本批全文重读实际全部收益(根1+1/(m−1),中间2+1/(m−1),末位2)，不是误猜末位m；以OPT3m−2核旧2m−1逐人floor从m4已否，未否GAP/C2。',
 'archives/customer-attraction/state/计算/逐人净覆盖缺口的完整终局见证攻击--计算.md':'本批全文读GAP准确mu_i>=OPT−W、W1/M1见证及一次无incumbent代表运行；它不依计数净化，与本u_j1/Mm目标一致但数据/模型不同。',
 'archives/customer-attraction/state/反例/末位收益不可按人数均摊的全历史不交族--反例.md':'此前同SHA全文对象比较(m−1)u_m<=W，与C2的2W>=(m+1)u_m不同，不能按末位/聚合名称合并。',
 'archives/customer-attraction/state/定理/五人半覆盖--定理.md':'此前完整同SHA证明；五人别证和六人主问题原量词保留，本批不升finite/auxiliary为half。'
}
dump(E/'related-material.json',{'global_search_terms':['full_tree_milp','audit_milp_candidates','exact_candidate_audit','terminal_clone_counterexample','GAP','逐人净覆盖缺口','末位克隆','2W and (m+1)u_m'],
 'objects':[{'path':p,'size':(R/p).stat().st_size,'sha256':sha(R/p),'semantic_comparison':note,'primary_in_this_batch':False} for p,note in related.items()],
 'old_same_SHA_generic_method_read_as_comparison_only':'tests/audits/cone_attack_joint_milp.py7637B; not run/no extra done',
 'same_SHA_6376B_R216_baseline':'exact byte identity recognized via inventory; no independent implementation or new done inferred'})

audit=json.loads((E/'replay-audit/execution.json').read_text())
milp=json.loads((E/'replay-milp/execution.json').read_text())
ind=json.loads((E/'independent-exact-review.json').read_text())
dump(W/'runtime-summary.json',{'new_original_entry_runs':2,'original_discovery_main_runs':1,'original_audit_main_runs':1,
 'new_MILP_calls':2,'new_fixed_cone_LP_calls':14,'new_canonical_verify_calls':14,'new_ExactSPESolver_calls':0,
 'observed_raw_line_events':28,'distinct_dual_records':14,'events_are_not_solver_call_count':True,
 'original_observer_execution_wall_seconds':audit['wall_seconds'],'original_discovery_wall_seconds':milp['wall_seconds'],
 'audit_output_bytes':134039,'audit_output_sha256':audit['output_sha256'],'audit_report_byte_identical':True,
 'discovery_output_bytes':milp['output_bytes'],'discovery_output_sha256':milp['output_sha256'],
 'independent_script_runs':1,'independent_timed':False,'independent_optimizer_calls':0,
 'gap_points':14,'gap_histories':796,'gap_including_self_comparisons':3919,'gap_nonself_comparisons':3123,
 'terminal_comparison_points':2,'terminal_histories':42,'terminal_including_self_comparisons':168,'terminal_nonself_comparisons':126,
 'combined_histories':838,'combined_including_self_comparisons':4087,'combined_nonself_comparisons':3249,
 'new_terminal_dual_replay':False,'new_old_terminal_independent_main_runs':0,
 'old_m4_long_discovery_repeated':False,'other_full_tree_680LP_regression_repeated':False,
 'source_order_note':'Primary code and full14 exact report fully read before run; raw8 files SHA verified before run, remaining raw numerical metadata completed full lossless reading after run. Do not retroactively claim pre-run full raw read.'})
dump(W/'read-order-note.json',{'primary_all_full_read':True,'all_runtime_and_comparison_material_finally_full_read':True,
 'before_original_runs':['all5 primary including complete14 exact instances/full action maps','actual original code/used dependency branches','8runtime files frozen identity and exact filenames'],
 'completed_after_original_runs':['full raw numerical proposal metadata/types/solver counters in8 frozen JSON, compact lossless view retained'],
 'scope_limit':'Do not substitute SHA verification for that earlier semantic read. No second original run was invented to change this order.',
 'observer_correction':'Original append line produced28pairwise equal observations; raw metadata and executed observer retained,14distinct actual LP outcomes derived. No extra optimization/repeated original run.'})

notes=[
 ([A,B,C],'3353B正式claim后全文双冻结核：任意实际j归一/主题m界/全效用向量及两portfolio轨道、3目标、14候选有限地位、七客户C1/真正C2公式/内部独审、旧逐人floor与GAP状态及停止延长样本建议全读。',
  '比较总质量12814Bselector和7637B旧固定路径联合码；新表证实银行末位实际2，不猜聚合公式。七客户严格4覆盖点全原稿/两terminal报告/独审原代码JSON全文对比；主原SET与其他重复标签点区分。',
  'integrated三自足对象。保原作者发现/历史独审，不领novelty；当前2m−1floor已被后银行族否，GAP与half/C2各自保量词。比较源全保但不额外done。'),
 ([B],'4802B正式claim后完整原码双SHA：显式inputs/out拒覆盖、norm实际root路径主题、固定图LP3目标分支/Γ符号、Fraction10^7与临时welfare顶点恢复、integer缩放、双完整IC验收、βμ余项判据、完整报告及stdout去大字段全部读。',
  '14保存点与8真实输入/5代码闭包全核；原报告省μ不假称独立可重放证书。新只读观察原main不改参数/值，补所有14对偶；standalone独立重构Γ/行hash/每坐标/原始归一值，非联合全MIP界。',
  '原__main__经runpy真实执行唯一1次3.729519172s/14LP/exit0，134039B全字节同；新增μ14，raw行事件28两两同且纠正LP字段，原raw和执行时observer保留，不重跑。源status/恢复失败分支不冒都执行。'),
 ([B],'134039B正式claim后全报告8组14记录逐项：各portfolio/norm/β/primitive实例/完整796有序actions/utility WOPT/GAP/flags全部规范顺序无损读，非摘要；双冻结SHA2c97695a…核。',
  '原审计一次同字节，std新核796h/3919incl3123nonself、所有OPT/真实paths/GAP、14Γ对偶全部坐标。4i0整数化后u1/4与归一LP点w4尺度不同保真；重复覆盖不merge，beta只选定目标不套全部J。',
  'integrated完整14表/历史8input数值边界/全部14μ支持。unit点和β都精确，原数值MIPbound不精确；terminal2对偶未纳这14不升级，保主half独立身份。'),
 ([A,B],'6376B正式claim后全源：输入检验m,p,j、完整含叶histories/全玩家utility/所有动作变量、root0、一热/主题m界/叶共享/2m差分行/当前无条件比较/u_j1、gap/individual/terminal目标、两对称支持、MIP字段和>.5提取/输出完整读。',
  '原方法7637B全文读不run，本是归一/自由终局变体；与R2166376同SHA不称独立方法。已有R-ab12814M1不同不能借其680LP。原review2226完整重构双向/Mm和GAP>m非half，算法变量/行与8input一致。',
  'integrated自足向量投影证明及计算。原defaultm3p4gap30s单次4.782849652s、2MIP/status0，raw2和2.0000000000000004；完整新动作/types与旧3p4相同，未将浮点upper当exact，也不重旧m4长run。'),
 ([A,B],'2226B正式claim后全文双冻结读：日期/审读对象非run认证、全玩家向量选中递推与全部真实IC、任意实际j正收益归一主题m界、root0/含不含0轨道、GAP阈值自我纠正及精确恢复义务。',
  '独立逐式核Mm不是2m，rootchosenj无需最小；保存域m1p1边界、raw14和fixedΓ对偶实际相符。其W>=m也不能让gap>m蕴含half的最终纠正保留，不重复原稿问句为错误结论。',
  'integrated自足双向证明，原历史“独立审读”不冒本轮新盲审/外审；比较来源与新原run各身份完整，不把正确编码和某次认证升级一般福利。')
]
receipts=[]
for src,(targets,read,compare,decision) in zip(primary,notes):
    receipts.append({'id':src['id'],'full_file_reviewed':True,'related_material_checked':True,'unique_content_accounted_for':True,
       'read_note':read,'comparison_note':compare,'decision_note':decision,'disposition':'integrated','targets':targets})
dump(W/'semantic-receipts.json',receipts)
dump(W/'relations-review.json',{'status':'semantically reviewed, not phase-three graph publication','new_objects':[A,B,C],
 'relations':[
 {'between':[A,B],'type':'exact formulation and finite implementation evidence','reason':'selected-edge vector induction defines all SPE; numeric MIP separate exact fixed-cone primal/dual'},
 {'between':[A,C],'type':'different linear objective and genuine auxiliary refutation','reason':'terminal objective with normu1 yieldsC1point7/3, not half'},
 {'between':[B,C],'type':'distinct audit scopes','reason':'14new gap duals exclude terminal optimum,standalone unit verifier checks2terminal points and root26; no transferred dual'},
 {'between':[A,'archives/customer-attraction/state/等价/完整有序历史终局选择的整数投影--等价.md'],'type':'different representations and normalizations','reason':'free pathu_j1/Mm vs fixedqtotalmass1/M1; no borrowed execution/novelty'},
 {'between':[A,'archives/customer-attraction/state/计算/逐人净覆盖缺口的完整终局见证攻击--计算.md'],'type':'same GAP contract, different interface','reason':'individual actual profit normalized versusWnormalized target outcome DAG; no incumbent from latter not global result'},
 {'between':[C,'archives/customer-attraction/state/反例/末位收益不可按人数均摊的全历史不交族--反例.md'],'type':'nonidentical target','reason':'C1andC2 not same as(m−1)um<=W; exact coefficients retained'}],
 'not_inferred':['half counterexample','all-strategy rational MIP upper bound','global fixed-cone bound across untestedJ','new discovery novelty','new independent blind review','runtime inputs automatically primary done']})

ids=['ebf6b97ab9caf5df3989','c3b51b85f6e91bfcadc2','8a6615b046f11dafa185','fede2c8665d245128ebd','b9d08f1137f1b34cf86c']
inv={x['id']:x for x in map(json.loads,(R/'cleanup/inventory.jsonl').read_text().splitlines()) if x['id'] in ids};nexts=[]
for i in ids:
    q=subprocess.run(['git','show',f'HEAD:cleanup/progress/{i}.json'],cwd=R,env={**os.environ,'GIT_NO_LAZY_FETCH':'1'},capture_output=True)
    nexts.append({**{k:inv[i][k] for k in ['id','path','size','sha256']},'local_HEAD_progress':json.loads(q.stdout) if q.returncode==0 else None,
      'local_progress_exists':(R/'cleanup/progress'/f'{i}.json').exists(),'root_actual_ledger_check_required':True,
      'local_absence_alone_does_not_establish_available':True,'current_read_role':'necessary comparison only, not primary done',
      'reason':'Formally close original C1 packet and historical independent review; reuse newly self-contained object, run original stdreview once if needed, no recreated counterexample',
      'proposed_stage':'r3-terminal-clone-primary-and-review'})
dump(W/'next-candidates.json',{'metadata_candidates_only':True,'requires_actual_future_root_claim':True,'candidates':nexts})
dump(W/'self-review.json',{'status':'pass','mathematics':[
 'Arbitrary actual positiveuj can normalize1; real prefix deviation guarantees every topic<=m; all eventual utilities in[0,m],exact conditional M=m.',
 'All-player selected-edge vector equality induction and unconditional currentIC precisely cover whole ordered tree,not countMarkov.',
 'Root0 and2portfolio orbits use simultaneous relabeling of free model; cannot transfer2orbits to a fixed graph;GAP>m nothalf.',
 '14primal/dual certificates independently rebuilt with exact Γlex rows/n/c and all coordinates,μnonnegative,beta equality; saved labels/pointscale preserved.',
 'Raw4player floating negative artifacts not accepted asclients; old exact audit reoptimizes inside fixedgraph,does not just round originaltypes.',
 '14gap838? actual gap796 plus2terminal42=838,3919+168=4087incl,3123+126=3249nonself; no invented new terminal dual.',
 'Sevenclient C1 strict4different topics/all21nodes/63nonself/root26,profits1.5,2,3.5;C2formula2W>=(m+1)um equality andhalfWOPT7.',
 'Historical individual2m−1floorOPEN corrected via bank;actual bank terminal2 notmistakenm;GAP/C2 not inferred fromnamedfailures.',
 'Fivehalf independentlyproved,sixoriginalgoalnotsettled; no novelty/globaloptimality or externalreview invented.'
 ],'provenance':[
 'Original actual merged25receipt retained unchanged;pushed/synced9bff88d… worker5intersection complete withcurrentowner verified before stage.',
 'All5primary fullread/doublefrozen;8runtimeinput+6comparison+5codedeps correctly nonprimary,all raw finallyfullyread.',
 'Explicit read-order note retains raw numeric fields completed afteroriginalrun;SHAcheck not mislabeled earlier fullsemanticread.',
 'One original2MIP CLI andone original14LP audit via runpy+read-onlylocals;original134039B byteidentical.',
 '28trace events are14identicalpairs,not28LP;rawmetadata/executedobserver saved,derived14certs andcorrectedcounter,futureobserverguard,no originalrerun.',
 'New independentstd1run untimed0optimizer,old terminalreview0newrun,othernamedimplregression0newrun.',
 'No sharedGit/claim/done/sync/checkpoint/authmutation,no spawn;allwritesexternalstage.'
 ],'receipt_counts':{'integrated':5,'primary_total':5},
 'remaining_limits':['Original14JSON omittedμ;only newobserved14μ replayed,oldterminalμstillnotnewreplayed.',
 'No exact joint-MIP upper/infeasibility certificate or general C2/GAP/half resolution.',
 'Some exact points onlynoninjectivelabeldomain;strictSETattainment not mechanicallymerged.']})

(E/'README.md').write_text('''# 自由终局逐人归一完整树证据

[数学向量表示](../../../state/等价/实际玩家归一的全树效用向量表示--等价.md)、[候选与对偶资源](../../../state/计算/自由终局逐人归一模型的候选与对偶复核--计算.md)、[七客户C1反例](../../../state/反例/逐人末位二倍保底的七客户反例--反例.md)为三个自足正文。正式5primary150796B，非primary8runtimeJSON107270B/6comparison53141B/5code46042B全部原样保存、双冻结核，共24raw357249B。

原合批25capture原字节保留，worker交集实际5且owner正确；没有伪造五项receipt。数学/阶段二receipt只此5，不额外done输入或比较。

新原full_tree main1次4.782849652s/2MILP0LP；新原audit main经runpy1次3.729519172s/14LP0MILP，输出134039B全字节同2c97695a…；原代码未改。audit只读观察新增14完整μ/β/归一点/余项/Γhash。不改变参数、值或多解优化器。28raw lineevents两两同，原metadata与执行时observer保留，去重14并纠正事件数误算LP数；原main没有重跑。

independent_exact_review.py新std1次/未计时/0optimizer、不导原/规范包，重构14Γ及所有对偶坐标、单位客户所有ordered IC；14gap796节点3919incl3123nonself，再核2terminal42节点168incl126nonself，共838/4087/3249。七客户首点另核26根有序可达路径。原旧独审程序0新次；terminal旧β7/3、2不冒新μ重放。

full-report-compact-read与raw-inputs-compact-read保全每字段以及所有原actions的无损规范序列；原14精确报告已在run前全读，8raw文件当时先核SHA，剩余数值元数据在run后补全阅读，如实记read-order-note，不倒填。

三目标gap/individual/terminal与half分开；浮点upper不称数学界，固定图选定支持β不泛化全策略。重复标签点保完整历史；七客户四覆盖互异直接原SET域。五人half别证/六人目标不由此解决。

cleanup/workspaces/Boss4/r3-full-tree-milp-candidate-audits-primary含5semantic receipts、自查、关系、运行计数、next候选及HANDOFF。copy-files是精确白名单，由Root串行复制/发布/登记。本worker无sharedGit、认领勾选或认证更改。
''')
(W/'HANDOFF.md').write_text('''# CF五源成熟交付

原25claim回执完整原字节保留，pushed/synced9bff88d715e258bf152edf97073591b1652307e2/Boss4；期望5与actual25交集全5、missing0、当时5HEADowner/SHA核实。只5receipt全部integrated，不投影伪造原回执、不额外done依赖。

三新自足正文：实际玩家归一的全树效用向量表示；自由终局逐人归一模型的候选与对偶复核；逐人末位二倍保底的七客户反例。保任意j归一及M=m双向证明、2根支持轨道、GAP/individual/terminal目标、原独审先验/方法复用、14点完整数据和后状态，原作者七客户发现不新领novelty。

原defaultMILP1次4.782849652s、2MILP/status0/0LP；原audit通过runpy__main__1次3.729519172s、8input14LP0MILP，134039B全字节同2c97695a…。14μ新只读观察保存并新独立Γ/坐标重放。trace28events两两同≠28LP；raw与执行旧observer保留，derived14与correctedexecution明确，绝未重跑原main。原码/helper/输入不改。

std新1次untimed0solver：14gap796h/3919incl3123nonself，2terminal42h/168incl126nonself，总838h/4087incl/3249nonself；首七客户strict4coverC1差−1/2、C2等号、WOPT7/root26。terminal旧固定β不冒这14新μ认证。所有比较源均未primarydone。

真实read-order边界已保存：run前原码+完整14精确报告全读、8raw核SHA；8raw剩余浮点metadata运行后无损全文补读，不把hash核冒成当时semantic fullread，也不虚构一次新run来改顺序。最终所有必要原件全文/独有内容完整。

按copy-files精确白名单复制，先新正文/证据发布后仅5receipt done。next5为C1原稿/terminalJSON/独审md/py/JSON，需Root实际ledger核claim再正式处理；当前只是完整比较，不重造已成反例。无sharedGit/claim/done/sync/checkpoint/auth写，Root串行发布。
''')
print(json.dumps({'metadata_written':True,'formal_bodies':[{'path':p,'bytes':(S/p).stat().st_size,'sha256':sha(S/p)} for p in [A,B,C]]},ensure_ascii=False))
