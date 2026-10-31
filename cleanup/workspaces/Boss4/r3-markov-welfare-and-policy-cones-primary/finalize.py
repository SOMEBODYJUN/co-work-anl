from pathlib import Path
from fractions import Fraction
import hashlib,json,os,subprocess

S=Path(__file__).resolve().parents[4]
R=Path('/workspace/scratch/37f0f9248cfc/boss4-research')
E=S/'archives/customer-attraction/tools/evidence/markov-welfare-policy-cones-primary'
W=S/'cleanup/workspaces/Boss4/r3-markov-welfare-and-policy-cones-primary'
A='archives/customer-attraction/state/计算/最差覆盖计数化的三人有限筛查--计算.md'
B='archives/customer-attraction/state/计算/计数策略客户锥搜索与保存输入的精确分版--计算.md'
BASE='archives/customer-attraction/state/计算/七主题固定输入基线与终局搜索版本--计算.md'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,x):
    p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
sources=json.loads((E/'primary-manifest.json').read_text())['sources']
dump(E/'source-manifest.json',{'primary_count':5,'primary_bytes':sum(x['size'] for x in sources),
 'runtime_external_repo_code_files':0,'runtime_external_input_files':0,
 'runtime_external_packages':{'python':'3.12.14','numpy':'2.3.5','scipy':'1.17.0'},
 'new_original_entry_ids':[sources[0]['id'],sources[1]['id']],
 'runtime_input_note':'Only original source-built generators/seeds/defaults. Frozen policies are separate explicit inputs for the new independent exact verifier.',
 'sources':sources})
review=json.loads((E/'independent-policy-review.json').read_text())
old=json.loads((S/sources[2]['saved_path']).read_text());new=json.loads((E/'replay-cone/new_policy_cone.json').read_text())
differences=[{'field':k,'frozen':old[k],'new':new[k]} for k in old if old[k]!=new[k]]
assert [x['field'] for x in differences]==['seconds']
dump(E/'original-output-comparison.json',{'frozen_file_id':sources[2]['id'],'frozen_sha256':sources[2]['sha256'],
 'new_file':'replay-cone/new_policy_cone.json','new_sha256':sha(E/'replay-cone/new_policy_cone.json'),
 'byte_identical':False,'json_differences':differences,'all_policy_and_weight_values_equal':True,
 'frozen_original_run_restarts_steps_not_recorded':True,'m6_m8_original_search_new_runs':0})

related={
 'archives/customer-attraction/state/反例/完整历史与计数统一策略的严格分离--反例.md':'Same-SHA full prior read/recheck: original5-theme24831-client example disproves general worst-welfare and root-set purification; not remade or rerun.',
 'archives/customer-attraction/state/计算/计数统一续局的有限枚举与辅助终局分离--计算.md':'Own previous batch complete comparison:3exact probes; auxiliary6-theme025 only root-set separation and both minimum sums6. New welfare screen specifically tests weaker min comparison.',
 'archives/customer-attraction/state/问题/完整历史计数策略净化--问题.md':'Already refuted general candidate; historical16000/499 records not overwritten by new20000 sample.',
 'archives/customer-attraction/state/定理/固定完整策略的客户重数锥--定理.md':'Full re-read: complete actual IC, normalized compact section, exact primal/dual and label-domain scope; specific count-policy quotient is valid without universal purification.',
 'archives/customer-attraction/state/算法/可信续局菜单与完整策略重构--算法.md':'Full re-read max-min exact set recursion and disjoint ordered child proof; full menus distinct from simultaneous count continuation.',
 'archives/customer-attraction/state/计算/首人弱覆盖门槛的固定策略探针与计数游走--计算.md':'Full re-read: different m5k7 mask27/8client table,root u1-normalization and explicit2801history old audit; current mask28/9client W-normalization not same instance/run.',
 'archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md':'Same-SHA full read retained: strict SET directory distinct from software noninjective labels; all3 saved policy inputs have duplicate coverages, not merged.',
 'archives/customer-attraction/state/定理/五人半覆盖--定理.md':'Same-SHA full prior read: separate universal5theorem; current finite points no6upper bound.',
 BASE:'Full previous mature body read: seven mutually disjoint topics/11clientsW5OPT9 different from current duplicate-label input. Actually published657bd0c anddone3afc9; current checkout loss is later merge regression, not original failure to publish.'
}
records=[]
for p,note in related.items():
    local=R/p;origin='current checkout'
    if not local.exists():
        assert p==BASE
        local=S.parent/'r3-true-spe-outcome-evidence-primary'/p;origin='previous mature external stage, bytes independently matched original published commit657bd0c'
    records.append({'path':p,'size':local.stat().st_size,'sha256':sha(local),'read_location':origin,
                    'exists_in_current_checkout':(R/p).exists(),'semantic_comparison':note,'primary_in_this_batch':False})
dump(E/'related-material.json',{'scope':'Full repository exact original filename/actor references and count-Markov/min-welfare/cone/first-floor/normalized-root comparisons',
 'objects':records,'prior_publication_evidence':'published-predecessor-proof.json',
 'progress_warning':'Root reports later merge regression of published bodies/claims/done. Missing local progress is not evidence of availability; root must consult restored real ledger.'})

runtime=[]
for name in ['welfare','cone']:
    x=json.loads((E/f'replay-{name}/execution.json').read_text());assert x['returncode']==0 and not x['timed_out']
    runtime.append({'name':name,'execution':str((E/f'replay-{name}/execution.json').relative_to(S)),
      **{k:x[k] for k in ['wall_seconds','original_entry_runs_this_batch','stdout_bytes','stderr_bytes','source_sha256']}})
stdout=[json.loads(x) for x in (E/'replay-cone/stdout.txt').read_text().splitlines()]
assert len(stdout)==3 and stdout[-1]['done'] and not any('status' in x for x in stdout)
scan=json.loads((E/'replay-welfare/stdout.txt').read_text())
dump(W/'runtime-summary.json',{'new_original_entry_runs':2,'original_runs':runtime,
 'welfare_scan':scan,'welfare_total_attempts':scan['checked']+scan['skipped'],
 'welfare_original_counterexample_output_created':False,'welfare_no_optimizer':True,
 'cone_completed_LP_calls_from_full_control_flow':300,'cone_full_call_trace_saved':False,
 'cone_output_bytes':(E/'replay-cone/new_policy_cone.json').stat().st_size,'cone_output_sha256':sha(E/'replay-cone/new_policy_cone.json'),
 'm6_m8_discovery_main_new_runs':0,'new_independent_standard_library_runs':1,'independent_timing_recorded':False,
 'independent_solver_calls':0,'explicit_ordered_history_enumeration':False,
 'counts_per_frozen_policy':[{k:x[k] for k in ['m','k','count_policy_entries','complete_ordered_decision_histories_covered',
                 'ordered_comparisons_including_self_covered','ordered_comparisons_excluding_self_covered']} for x in review['frozen_policies']],
 'three_weight_readings':'literal decimal rational; exact parsed binary float; explicit new small-denominator reconstruction limit1e6',
 'm5_binary_interpretation_exact_IC_failure':'-1/90071992547409920 at root chosen4 alternative0',
 'm5_literal_and_small_reconstruction_SPE':True,'m6_all_three_SPE_but_different_integer_inputs':True,
 'm8_all_three_identical_SPE':True})

notes=[
 ([A],'4266B正式claim后全码双冻结读：numpy六倍整数份额/所有pairs triples映射、末位全部ties与乘积cap、full两层maxmin、计数全末映射/二层独立、同min提前break、默认参数/稀疏随机生成/仅阳性写file/总done全读。',
  '与BR集合比较和旧5主题合法最差22428<22429精确比较；min相同不推集合相同，policy_count非实际遍历数。默认小整数域安全，np.prod及1e15哨兵不许诺任意大参数。',
  'integrated自足三人有限筛查对象。原默认main1次wall8.901155004s/exit0，20000=19856checked+144skip、无反例file；不把skip/阴性变一般结论，源无冻结stdout不冒复现旧统计。'),
 ([B],'6616B正式claim后全文双冻结读：全部comps/types/coeff/支持/children；bi两容差和poor随机、W1完整countIC LP、重启lognormal/两种支持选择/噪声、best1e-7和weights1e-9截断、完整输出/default30x10全读。',
  '固定完整策略锥正确但搜索只受限count策略；与旧first-floor u1归一化不同。bi容差/浮点LP不自动精确SPE，saved point未必达OPT；全客户锥、固定目标及全策略界不同。',
  'integrated新资源。原默认m5唯一main1次wall23.947556420s/exit0、无失败完成300LP；新38047B仅seconds异不字节同。保存点全部独立Fraction核三版本；m5binary真违IC明确，m6/m8未重跑大搜索。'),
 ([B],'38047B正式claim后全JSON：m5k7 ratio1.8/root/support/5非零weights/restart0step5秒数及330条policy按原组合顺序全action串无损读核SHA，非抽样/非只读header。',
  '原mask28核心9客户与旧mask27核心8客户不是同输入，7标签中3核心重复仍保全部历史。330count≠2801ordered。十进制.2=1/5、IEEE float略大、小分母重构必须独立；当前原main仅seconds异。',
  'integrated。A/C原表精确SPE/9客户W5OPT9；B根违差−1/90071992547409920，绝不称原float精确点已认证。计数2310项精确IC覆盖19607ordered比较但未枚举全部ordered。'),
 ([B],'161444B正式claim后全JSON：m6k8/root/support/5个.16666666666666666与核心134:1、ratio/restart1step0秒数；1287条原policy全部规范顺序无损action读，核两冻结SHA。',
  '1287计数覆盖37449ordered/299592含自身；重复核心1/2/7不合并。原有限十进制、IEEE二进制与1/6显式重构各自Fraction核，不把原浮点列表直接写11单位客户。',
  'integrated，三版本均SPE但实际原始整数人数分别91666666666666665、66052794534767273、重构11；比例/全部实际路径/IC/OPT全自足。未新跑m6大搜索/未认证固定锥全局最优或六人half。'),
 ([B],'804839B正式claim后全JSON：m8k8/ratio1.5/root/support8/5非零weights/restart1step1/136.812秒；6435条policy全部按原深度和组合顺序action无损全文读，核2冻结SHA。',
  '6435条目涵盖2396745ordered，19173960含自身/16777215非自身，不冒真遍历两千万。核心201含0/3/6/7，全表频数和重复覆盖精确核；.125三种解释同1/8。',
  'integrated，独立count51480项含自身精确IC，12客户W8OPT12/ratio3/2，半覆盖余额4；原表保4核心标签不merge。原历史seconds不是本轮run，本轮m8发现0次，无锐性/通用最优/half反例。')
]
receipts=[]
for x,(targets,read,compare,decision) in zip(sources,notes):
    receipts.append({'id':x['id'],'full_file_reviewed':True,'related_material_checked':True,'unique_content_accounted_for':True,
                     'read_note':read,'comparison_note':compare,'decision_note':decision,'disposition':'integrated','targets':targets})
dump(W/'semantic-receipts.json',receipts)
dump(W/'relations-review.json',{'status':'reviewed; no phase-three graph fabricated','objects':[A,B],
 'relations':[
 {'between':[A,'archives/customer-attraction/state/反例/完整历史与计数统一策略的严格分离--反例.md'],'type':'finite negative vs known strict refutation','reason':'m3k4 sample negatives do not restore general worst-welfare purification refuted at k5'},
 {'between':[B,'archives/customer-attraction/state/定理/固定完整策略的客户重数锥--定理.md'],'type':'exact special representation and numeric implementation','reason':'given count policy induces full policy; quotient IC exact, approximate BI/LP only discoveries'},
 {'between':[B,'archives/customer-attraction/state/计算/首人弱覆盖门槛的固定策略探针与计数游走--计算.md'],'type':'different normalized goal and actual input','reason':'W1/ratio9/5 mask28 current vsu1=1/ratio8 mask27 old'},
 {'between':[B,BASE],'type':'different legal directory scope','reason':'saved repeated-cover labels vs seven mutually disjoint actual themes; same9/5 numeric ratio not same certificate'},
 {'between':[B,'archives/customer-attraction/state/定理/五人半覆盖--定理.md'],'type':'finite point vs universal theorem','reason':'literal/small exact points positive half margin; neither float negative IC nor six11/6 supports half counterexample/upper bound'}],
 'new_math_distinctions':['literal decimal vs exact parsed binary vs new rational reconstruction','count IC checks vs lifted ordered comparisons','root-set vs minimum-welfare purification','selected support vs actual OPT']})

ids=['874c0db324473e83674c','8542015b808290c371cf','ebda4e0db4f534b555d5','e1dbcd18938f638babaa','2cfcb16f997f78dba665']
inv={x['id']:x for x in map(json.loads,(R/'cleanup/inventory.jsonl').read_text().splitlines()) if x['id'] in ids}
nexts=[]
for i in ids:
    q=subprocess.run(['git','show',f'HEAD:cleanup/progress/{i}.json'],cwd=R,env={**os.environ,'GIT_NO_LAZY_FETCH':'1'},capture_output=True)
    nexts.append({**{k:inv[i][k] for k in ['id','path','size','sha256']},
       'local_HEAD_progress_observation':json.loads(q.stdout) if q.returncode==0 else None,
       'local_progress_exists':(R/'cleanup/progress'/f'{i}.json').exists(),
       'availability_not_established_from_missing_progress':True,
       'requires_root_restored_actual_ledger_check':True,'primary_content_not_read_before_claim':True,
       'proposed_stage':'r3-full-tree-milp-candidate-audits-primary'})
dump(W/'next-candidates.json',{'metadata_candidates_only':True,'root_reported_progress_regression':True,
 'do_not_infer_available_from_local_absence':True,'only_actual_future_root_claim_authorizes_primary':True,
 'candidates':nexts})
dump(W/'self-review.json',{'status':'mathematics-complete; current checkout restoration dependency explicitly recorded',
 'mathematics':[
 'All5 primary full sources double frozen verified;8052 policy records read losslessly and every actual state/action used by exact reviewer.',
 'Specific count policy defines complete history policy; induction on remaining length proves exact quotient IC; lifted counts not falsely called explicitly enumerated.',
 'Source welfare6-scaled integers exact within current bounded default; product cap skips144 and early equality break preserved, no complete-set claim.',
 'Source coneW1 different oldflooru1=1; proposal tolerance and truncation can lose exactIC, source success not proof.',
 'Literal/binary/reconstructed inputs separate: m5B false exactIC−1/90071992547409920; m5A/C pass; allm6 pass but different integer instances; m8 allsame.',
 'Core-only analytic all-history certificate proves every positive claimed version and actual OPT; original repeated labels kept, not strict SET merged.',
 'No exact dual/global fixed-cone optimality or universal half claimed. Five known independently,six remains original open target.',
 'All original and new m5 reports preserved; onlyseconds JSONdifference, not byte identity; originalm6/m8 discovery0newruns.'
 ],'provenance':[
 'Actual claim989fa664…pushed/Boss4/synced and all5 owners verified before primary; subsequent root-reported merge regression does not rewrite this historical receipt.',
 'New original welfare andcone each1run successful, real generator inputs and package versions recorded; no helper/code input dependencies omitted.',
 'New independent std reviewer1run,untimed/0optimizer,12 input interpretations includes explicit expected negative; no solver trace invented.',
 'BL predecessor originally actuallypublished657bd0c anddone3afc9, current absence is later merge tree deletion;gitshow bytes matched external mature stage.',
 'Next local missing progress is not availability under known rollback; candidates require root true ledger recovery/claim.',
 'All writes external; no shared Git/claim/done/sync/checkpoint/auth change,no spawn.'
 ],'remaining_limits':['No original full CLI/run budgets recorded for3 frozen policy discoveries; not backfilled.',
 'Original LP intermediate first point/full300trace and discarded small weights not preserved; only actual saved inputs certified.',
 'Prior published baseline link may be temporarily absent in current checkout pending root restoration; original publication evidence retained.']})

(E/'README.md').write_text('''# 三人计数化与完整计数策略客户锥证据

[三人有限最差覆盖筛查](../../../state/计算/最差覆盖计数化的三人有限筛查--计算.md)与[保存策略的精确分版](../../../state/计算/计数策略客户锥搜索与保存输入的精确分版--计算.md)为两个自足对象。primary五文件1015212B，三原policy全部8052计数记录原样保存；两冻结SHA/claim/owner见manifest与cleanup工作区。

原main各1次：welfare默认20000，19856checked+144skip，wall8.901155004s，无差异文件；cone默认m5k7/30×10=300LP，wall23.947556420s，best1.8，新38047B仅seconds异。真实依赖numpy/scipy+stdlib，无仓库helper或外部实例。m6/m8大搜索本轮0次；两个原入口和所有stdout/stderr/event分别保全。

independent_policy_review.py标准库独立一次/0solver/未计时：检查全部计数状态行动，证明提升覆盖全部ordered历史；未显式枚举千万history。independent-policy-review.json保三冻结与新m5的三种精确质量解释、原始最简整数客户、真实τ/root/OPT/IC、每层完整无损actions和频数。

m5 literal decimal或新小分母重构都SPE/9客户W5OPT9；exact binary float解释根违差−1/90071992547409920。m6三版本都SPE但人数/比例不同，只有明确1/6重构是11客户。m8三版本同12客户W8OPT12。标签重复全部保，不merge；float与数学认证分开，不升half。

published-predecessor-proof记录七主题固定基线页原已实际发布657bd0c/done3afc9、原字节与成熟外部包一致；当前checkout暂缺来自之后merge回退，非原先未发布。Root负责串行恢复。下一metadata候选也不因本地progress缺失被认定available，需Root恢复真实ledger再claim。

逐源receipt、自查/关系/运行摘要/HANDOFF位于cleanup/workspaces/Boss4/r3-markov-welfare-and-policy-cones-primary。copy-files是精确白名单，Root串行复制/发布/登记。本worker无共享Git写入/认领/勾选/认证尝试。
''')
(W/'HANDOFF.md').write_text('''# CB五源交付

实际claim989fa6648a46b4211c890cdb40fc65996d675ea3/Boss4/synced，五owner核在原件导出之前。primary1015212B，五receipt全部integrated。两个新正文：最差覆盖计数化的三人有限筛查；计数策略客户锥搜索与保存输入的精确分版。

原默认welfare1次8.901155004s，20000=19856checked+144skip、无阳性file；原defaultcone1次23.947556420s、无失败300LP、best1.8。新m5输出38047B/SHA db3c2e8941e4597a7eb19724f916cc89f09b6f5f917f89e94f44bb23d6f27578仅seconds异。m6/m8本轮发现0次。

三冻结全部8052count records完整无损读，独立std1次0solver/未计时验证所有state/action并以计数策略的确切归纳提升覆盖完整ordered树，没有冒实际枚举千万历史。三精确版本必须分开：m5 literal0.2=1/5/小分母重构SPE；将Pythonfloat0.2当精确重数根真违差−1/90071992547409920。m6 literal约9.17e16客户、binary约6.61e16客户、只有明确重构为11客户；三版本都SPE。m8相同12客户。source labels重复全部保，未商成严格SET。

特殊发表依赖：BL基线页原已实际在657bd0c110e3dd7ddfd51d9cc5e70e28fe1fa06c发布且3afc9e6293320f9c8fd52737281ee2a2da267294 done；后续merge删除导致当前checkout暂缺。gitshow原发布正文与成熟外部stage11644B/SHA d820d313…相同。请按Root既定恢复流水在CB done前还原该本地链接；不能说BL从未发布，不能额外重done旧来源。本包不覆盖旧正文。

下一五只是候选874c0db324473e83674c/8542015b808290c371cf/ebda4e0db4f534b555d5/e1dbcd18938f638babaa/2cfcb16f997f78dba665；当前已知progress回退，不依据本地缺记录称available，待Root修复后真实ledger核认领再开primary。

按copy-files精确白名单保存，数学证据和原始run均完整；只本5receipt在新正文/证据发布后登记。所有sharedGit/ledger恢复由Root串行，本worker仅external写。
''')
print(json.dumps({'metadata_written':True,'formal_bodies':[{ 'path':p,'size':(S/p).stat().st_size,'sha256':sha(S/p)} for p in [A,B]]},ensure_ascii=False))
