"""Record semantic decisions and local provenance; no Git or source retrieval."""
from pathlib import Path
import hashlib,json,os,subprocess
S=Path(__file__).resolve().parents[4];R=S.parent.parent/'boss4-research'
E=S/'archives/customer-attraction/tools/evidence/terminal-clone-primary-and-review'
W=S/'cleanup/workspaces/Boss4/r3-terminal-clone-primary-and-review'
CF=S.parent/'r3-full-tree-milp-candidate-audits-primary'
BODY='archives/customer-attraction/state/计算/末位克隆独审入口与两份固定锥证书--计算.md'
COUNTER='archives/customer-attraction/state/反例/逐人末位二倍保底的七客户反例--反例.md'
CALC='archives/customer-attraction/state/计算/自由终局逐人归一模型的候选与对偶复核--计算.md'
EQUIV='archives/customer-attraction/state/等价/实际玩家归一的全树效用向量表示--等价.md'
def save(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def info(p):b=p.read_bytes();return {'size':len(b),'sha256':hashlib.sha256(b).hexdigest()}
defs=[
 ('ebf6b97ab9caf5df3989','duplicate',[COUNTER,BODY],
  '3090B正式认领后全文重读：精确C1五重量词、七单位客户与严格4主题、21节点完整策略、第二/根真实偏离收益、DCD三份覆盖机制、倒二界/C2等号及发现与固定锥认证区别全保。',
  '与CF同SHA必要比较源及其自足反例全文逐表核；4059B独审、25133B逐节点报告、新原独审入口均相同数学；历史Q-CAG整体OPEN改按五人别证/六人当前目标分域。',
  '反例、完整16末回复/第二层/根层证明和独有失败机制已在同一CF反例正文，无独有数学遗失；不重造反例、不领novelty。此源duplicate；本批新增terminal对偶另属计算资源。'),
 ('c3b51b85f6e91bfcadc2','integrated',[BODY],
  '8648B两组两完整记录重新全部实读：各portfolio、归一位置、β7/3与2、原始整数实例/全部21动作、counts、实际效用WOPT/GAP及flags，包含第二个2客户边界点而不只首反例。',
  'CF已认证两可行点但明确terminal μ未补；本批以原记录明确生成新派生图输入，不虚造未提供旧MIP参数，原4802B审计一次2LP产生完整records完全同，逐字典source之外无差。',
  '新增自足两固定锥证明：A48/B51完整IC行、每图四个正μ、全部15坐标余项及达到点；std新重放一次0优化器核30余项。B同覆盖标签不合并，β只限两给定图，不升级全策略/half。'),
 ('8a6615b046f11dafa185','duplicate',[COUNTER,BODY],
  '4059B认领后全文重读：2026-10-21独立定义级内部复核先验、无规范solver/LP依赖、单位客户展开、21节点/63非自身、16末回复向量、四根分支及C1/C2差和外审边界。',
  '源中先验与原4574B实际代码一致；CF反例正文已自足保全全部表和DCD解释。实际脚本读取JSON后先在数学运算中不使用actions，递归E集合，再审给定图；未误称物理文件中从未含策略。',
  '独有审查身份、C2补偿、倒二界不受反驳均在旧对象完整保留，本批补程序证据但不造新数学反例。duplicate且原件留存，不冒新盲审/外审。'),
 ('fede2c8665d245128ebd','integrated',[BODY],
  '4574B原源码完整实读：stdlib依赖、SOURCE固定相对路径、main只首记录、per-unit Fraction、先集合递归E再读取actions、完整键/范围校验、真实后继IC、64有序叶OPT、根/末位/客户全表及无尾newline JSON写出全核。',
  '与CF另一新std实现和原规范包区分：CF原main明确0次；本批原main隔离一次0.061540064s、0优化器，25265B仅source改变，所有原25133B数学字段同。E根26为终局路径数非策略数。',
  'integrated原独审可执行资源、集合递归必要充分拼接证明和真实一次运行；保21决定/84含自身/63非自身准确计数。不重跑同SHA CF14LP/2MIP或冒原程序审核第二terminal点。'),
 ('b9d08f1137f1b34cf86c','duplicate',[COUNTER,BODY],
  '25133B报告正式认领后全文重新读完：全部21×4偏离行、16末位回复/平局、四根分支、七单位客户份额、26根路径计数与完整摘要/source/method；不止摘要。',
  '原字节SHA d0f743…与CF比较原件同；新原程序一次输出逐字段只source绝对路径不同，计数和全部有理表相同，未假称byte-identical。CF既有自足反例及std逐节点证据足以保数学。',
  'duplicate原有限报告到同一反例及新程序资源。25133B是旧完整输出，不赋予其LP μ证书；本批新μ另存新身份，也不声称26条路径列表在旧JSON已全部列出。')]
receipts=[]
for i,d,targets,read,compare,decision in defs:
 receipts.append({'id':i,'full_file_reviewed':True,'related_material_checked':True,
  'unique_content_accounted_for':True,'read_note':read,'comparison_note':compare,
  'decision_note':decision,'disposition':d,'targets':targets})
save(W/'semantic-receipts.json',receipts)

comparison=[]
paths=[(CF,COUNTER,'CF成熟自足C1反例，完整客户/图/收益表和先验；本批不覆盖旧正文'),
 (CF,CALC,'CF十四GAP证书及terminal两点先前只核可行/原独审main0次；逐程序不同范围'),
 (CF,EQUIV,'实际任意j归一、M=m完整向量表示与固定图/联合模型边界'),
 (R,'archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md','严格SET/有序IC/单位客户与重复标签软件扩展'),
 (R,'archives/customer-attraction/state/反例/末位收益不可按人数均摊的全历史不交族--反例.md','不同式(m−1)um≤W从m4被否，不混C2'),
 (R,'archives/customer-attraction/state/问题/逐人覆盖缺口价格桥--问题.md','GAP/早期真实续局共同付款未闭，与C1辅助式区分'),
 (R,'archives/customer-attraction/state/定理/五人半覆盖--定理.md','五人原模型普遍half已有别证；六人目标未被当前有限点解决')]
for root,path,note in paths:
 p=root/path;row={'path':path,'actual_read_path':str(p),'full_text_read':True,'role':'comparison-not-primary','mathematical_comparison':note,**info(p)}
 if root==CF:row.update(repo_copy_exists=(R/path).exists(),repo_copy_matches_mature=(R/path).exists() and (R/path).read_bytes()==p.read_bytes(),publication_attested_here=False)
 comparison.append(row)
save(E/'comparison-manifest.json',{'whole_repo_search':'rg terminal_clone/C1/2W/末位二倍/全树效用 over current customer-attraction state and evidence; then actual full-text objects listed below read; no remote lookup',
 'source_primary_rechecked_against_CF_same_SHA':True,'comparisons':comparison,
 'CF_publication_note':'Root announced CF mature package serial saving. Repo copies presently exist/match as recorded; no independent pushed claim here. Root must confirm CF target publication before CR done.'})
save(W/'relations-review.json',{'reviewer':'Boss4/credible_cap_resume','phase':'phase2 semantic relationship review; no phase3 graph fabrication',
 'new_object':BODY,'relationships':[
  {'type':'certificate-completion','from':CALC,'to':BODY,'common_contract':'固定给定完整有序策略/实际j收益归一的非负类型锥',
   'reason':'CF十四GAP对偶不包括terminal；本页只补两张旧terminal图的μ和30坐标余项，不改变CF旧运行次数或继承其GAP最优给terminal。'},
  {'type':'resource-and-proof-support','from':BODY,'to':COUNTER,'common_contract':'三人四互异覆盖、七单位客户的同一完整21节点图A',
   'reason':'原std主入口一次复现26可实现根路径和逐历史SPE；新β7/3最优是额外固定图信息，C1反驳本身只需可行点，故不是反例必要前提。'},
  {'type':'scope-comparison','from':EQUIV,'to':BODY,'common_contract':'归一位置j及terminal目标',
   'reason':'自由全树联合图优化与固定图LP域不同；原source浮点发现7/3不能成为联合全局精确最优。'},
  {'type':'non-implication','from':COUNTER,'to':BODY,'common_contract':'C1逐人2ui≥um；C2为2W≥(m+1)um；half为2W≥OPT',
   'reason':'A上三差−1/2、0、7；只否C1。B同覆盖标签的等号达到性不能移入严格四集合域。'}],
 'no_edges_claimed':['不由有限2锥生成一般C2/half定理','不自动沿旧图或为连通造超边','不将输入、比较或运行依赖记为本5外的primary done']})

original=json.loads((E/'replay-original-review/execution.json').read_text())
duals=json.loads((E/'replay-terminal-duals/execution.json').read_text())
independent=json.loads((E/'exact-terminal-duals-review.json').read_text())
save(W/'runtime-summary.json',{'original_standard_library_main':original,'original_fixed_cone_main_on_new_derived_inputs':duals,
 'new_standalone_dual_replay':{k:v for k,v in independent.items() if k!='records'},
 'new_runs_this_batch':{'original_std_review_main':1,'original_audit_main_new_derived_inputs':1,'fixed_cone_LP':2,
  'MILP':0,'new_std_replay_entry':1,'CF_original_audit_reruns':0,'CF_MILP_reruns':0,'old_original_terminal_MIP_reruns':0},
 'counts_are_program_specific_not_distinct_game_histories':True,
 'read_order':'All five primary text/JSON, actual std main, audit code/used closure and two explicitly derived inputs read and hashes verified before current runs. Dependencies retain full same-SHA CF source read identity.',
 'no_network_clean_show_lazy_fetch_or_auth':True})

inventory=[json.loads(x) for x in (R/'cleanup/inventory.jsonl').read_text().splitlines()]
candidate_ids=['803f20f0f54fc58a267c','cf0af9e399949ffdbb1a','0625693da7f9a719c3f3','08f7bce19d1d835bfbd4','e77639427f0940cb0f13']
candidates=[]
for cid in candidate_ids:
 row=next(x for x in inventory if x['id']==cid)
 check=subprocess.run(['git','cat-file','-e',f'HEAD:cleanup/progress/{cid}.json'],cwd=R,capture_output=True,env={**os.environ,'GIT_NO_LAZY_FETCH':'1'})
 candidates.append({**row,'primary_read_or_receipt_in_this_batch':False,
   'local_working_progress_exists':(R/f'cleanup/progress/{cid}.json').exists(),
   'local_HEAD_progress_record_exists':check.returncode==0,
   'actual_availability':'candidate only; Root must check actual authoritative ledger/owner before claim, because prior merge deletions mean absence is not proof',
   'suggested_scope':('原terminal发现输入版本/status/types与精确报告逐项区分；不重复既足同SHA运行' if 'terminal_m' in row['path'] else '原完整材料与实际代码自读定合同，不预设abstract与原模型相同')})
save(W/'next-candidates.json',{'status':'metadata candidates not a claim; no network/source read performed','sources':candidates})

save(W/'self-review.json',{'status':'pass','reviewer':'Boss4/credible_cap_resume','primary_count':5,
 'mathematical_checks':[
  '逐一完整原件重读和全仓后修比较，不由摘要、flags或旧图代替原始图/数值。',
  '两完整21节点图/15类型坐标、所有偏离真实后继、j0/j1、C2准确公式已逐式核。',
  'βn−c=ΣμG+r符号、等式β无预设非负、8正μ/30余项、两达到点及原始整数化尺度均正确。',
  'A严格四覆盖、B重复覆盖不merge；Γ行去重不合并策略历史。',
  'E递归必要充分需跨不同有序孩子可独立拼接；26为根终局路径数，非策略数。',
  '原std脚本只第一terminal记录；第二点由不同规范审计和新证书重放核，不冒原脚本也审核。',
  'C1仅辅助失败、C2等号非证明、half正余额；五人别证与六人目标保真。',
  '原报告未存μ、新完整μ身份及固定图最优/联合MIP浮点值分开。'],
 'source_and_execution_checks':[
  'whole24 claim retained and onlyactual5 receipts; providedwhole27 intake retained withothergroups notdone。',
  '5原件45504B size/SHA256/blobSHA1；所有依赖仅本地同SHA复制；无clean show/network/lazy fetch。',
  '原std1次，原audit新派生2输入1次2LP；新std重放1次0solver；不回填CF原0或重跑CF14LP/2MIP。',
  '两个新输出只source变化，未冒byte-identical；原始stdout/stderr/started/execution均留存。',
  '新派生输入不冒历史MIP；原terminal发现JSON本批未取回或推测字段。'],
 'publication_boundary':'Only external staging written. Repo CF copies observed existing; actual CF publication/done remains Root serial responsibility before CR done.',
 'limitations':['只两给定图的terminal精确极值，不是全部图极值','没有外审/新颖性/最小性认证','下一候选仅metadata，须Root核实际ledger再认领']})
print(json.dumps({'receipts':len(receipts),'duplicate':sum(x['disposition']=='duplicate' for x in receipts),
 'integrated':sum(x['disposition']=='integrated' for x in receipts),'comparisons':len(comparison),'next_candidates':len(candidates)}))
