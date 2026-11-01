from pathlib import Path
import json,hashlib,difflib
R=Path('/workspace/scratch/37f0f9248cfc');REPO=R/'boss4-research';S=R/'boss4-next-cache/r3-covariance-menu-coherence-and-escape-review';E=Path('tools/evidence/covariance-menu-coherence-and-escape-review');D=E/'hypothesis-clarification-proposals'
def sha(b):return hashlib.sha256(b).hexdigest()
def put(p,t):
 q=S/p;q.parent.mkdir(parents=True,exist_ok=True);q.write_text(t,encoding='utf-8')
def js(p,x):put(p,json.dumps(x,ensure_ascii=False,indent=2)+'\n')
rows=[]
p1='archives/customer-attraction/state/障碍/双向隔离惩罚的福利上限与逃逸预算--障碍.md';p2='archives/customer-attraction/state/资源/独立利润消元与惩罚菜单证据的复用边界--资源.md'
for n,expected in [(p1,'9ba917329aa9476dd378e6846b2c0d8b7e03a82ab2462d2e41fdd750bf8612d6'),(p2,'eb03937d304717431bb84a104bbbe903451f1e53d7f2ae1ee9eb30e93e8c363d')]:
 before=(REPO/n).read_bytes();assert sha(before)==expected;ntext=before.decode()
 if n==p1:
  old='设局部核心a=|X_i|+|Y_i|>0，B_i=X_i∪Y_i∪Z，实际末端为r次同D=Z∪R；'
  new='本段是另一个具体重复尾方案，不套用前节m=k+1的比率界。固定r≥1、D=Z⊔R，局部核心X_i∪Y_i与D不交；除已指定的实际C_i、偏离A_i及下面列出的尾行动外，其余行动均不覆盖X_i∪Y_i∪R。\n\n设局部核心a=|X_i|+|Y_i|>0，B_i=X_i∪Y_i∪Z，实际末端为r次同D；'
 else:
  old='若实际尾部r次D=Z∪R，拟惩罚A_i后r次B_i=X_i∪Y_i∪Z，'
  new='本段固定r≥1、D=Z⊔R及局部核心X_i∪Y_i与D不交；除已指定的实际C_i、偏离A_i及所列尾行动外，其余行动均不覆盖X_i∪Y_i∪R。若实际尾部r次D，拟惩罚A_i后r次B_i=X_i∪Y_i∪Z，'
 assert ntext.count(old)==1;after=ntext.replace(old,new,1);assert after.split('---',2)[1]==ntext.split('---',2)[1];assert not any(ord(c)<32 and c!='\n' for c in after);assert all(l==l.rstrip() for l in after.splitlines());bp=D/'before'/n;ap=D/'proposed'/n;put(bp,ntext);put(ap,after);patch=D/(Path(n).stem+'.patch');put(patch,''.join(difflib.unified_diff(ntext.splitlines(True),after.splitlines(True),fromfile='a/'+n,tofile='b/'+n,n=0)));rows.append({'target':n,'before_path':str(bp),'before_bytes':len(before),'before_sha256':sha(before),'proposed_path':str(ap),'proposed_bytes':len(after.encode()),'proposed_sha256':sha(after.encode()),'patch_path':str(patch),'applied_to_shared':False,'change':'only explicitly state intended repeated-tail assumptions r>=1/D=disjointZ,R/core-Ddisjoint/otherunspecifiedactionsavoidcore-andR; firstpage also distinguishes this tailarchitecture from prior m=k+1 bound','source':'HP primary b93aa6e5de99b7936688 section multipleidenticalpunishmentfollowers andreviewconclusion','math_result_or_finite_report_changed':False,'metadata_unchanged':True})
js(D/'replacement-manifest.json',rows)
js(D/'scope-and-source-review.json',{'source_id':'b93aa6e5de99b7936688','source_sha256':'57d25a1d0d8183034cb2eeb9a6381db4e881d46381a7ba84a57de5f91cdf4cf5','source_first_full_read':'HF actual entire source now HP sameSHA reused','source_precise_condition':'r>=1; D=Z dotcup R; localcore disjointD; except specifiedC/A/tail actions, otheractions do notcoverlocalcore orR','why':'cancellation of commonZ leaves R/r inactual comparison and firstcoverageR inpunishment; overlapR-Z orprecoveredR invalidates these denominators','no_global_invalidation':'only clarify intendedlocal-template hypotheses, no negativejudgment onentireoldsource/done or generalhalf','Z_othercoverage':'commonZ contribution cancels within each one-shot last-player comparison; no newclaim that otherZcoverage alone invalidates inequality','prior_manifests_affected':[{'path':'tools/evidence/d22-frontier-ledger-primary/formal-resource-manifest.json','role':'historical GS deliveredformal beforeSHA, do not silently rewrite frozenstage/transport; Root may separately record actualapplicationnewSHA'},{'path':'tools/evidence/independent-profit-isolation-and-menu-proofs/formal-resource-manifest.json','role':'historical HD deliveredformal beforeSHA, same archival treatment'}],'shared_writes':0,'math_program_runs':0,'application':'Root fullread then beforeSHAcheck andserialapply, proposals evidenceonly'})
put(D/'README.md',r'''# 两处重复尾模板的最小假设澄清，尚未应用

实际全文独审b93指出：D=Z⊔R、核心与D不交，指定C_i/A_i和尾部以外其他行动不覆盖核心/R，均为具体分母比较的承重条件。此前GS/HD两正文保了 intended公式和“R未覆盖”，但没有完整显式列出，容易误用到交叠Z/R或被其他中间行动先覆盖R的变种。

本提案仅补这些条件，GS页另明确这段不是前节k+1人数界；元数据、数值、真值及其他证明不改，不否定旧done整体。before完整原字节/SHA、proposed完整正文、zero-context普通patch皆齐，不直接覆盖shared路径；Root审读后只在beforeSHA一致时串行应用。旧GS/HD源/外部交付包和manifest保持各自交付时的历史，实际应用另记afterSHA。

E的一般三比较精确余项反而不需要B_i局部支撑或B_i枝末位指定A_i；本提案只澄清后段具体重复方案，不给一般E多加这些强假设。无数学程序或旧成功复跑。
''')
put(D/'prepare_proposals.py',Path(__file__).read_text())
print(json.dumps(rows,ensure_ascii=False,indent=2))
