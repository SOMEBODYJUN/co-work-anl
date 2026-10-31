from pathlib import Path
import json,hashlib,difflib
R=Path('/workspace/scratch/37f0f9248cfc');REPO=R/'boss4-research';S=R/'boss4-next-cache/r3-profit-credit-and-saturated-query-source-bindings';E=Path('tools/evidence/profit-credit-and-saturated-query-source-bindings');F=E/'format-recovery'
def sha(b):return hashlib.sha256(b).hexdigest()
def put(p,t):
 q=S/p;q.parent.mkdir(parents=True,exist_ok=True);q.write_text(t,encoding='utf-8')
def cp(p,q):
 q=S/q;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(p.read_bytes())
def js(p,d):put(p,json.dumps(d,ensure_ascii=False,indent=2)+'\n')
# Restore all formulas from actual complete originals, not a mechanical C0 substitution.
n1='archives/customer-attraction/state/资料/动态信用背景探针来源与开放边界--资料.md'
n2='archives/customer-attraction/state/引理/任意背景的末位利润精确余项分解--引理.md'
old1=(REPO/n1).read_bytes();old2=(REPO/n2).read_bytes()
assert sha(old1)=='5ef555ece8d90fc039c345799e580f02bb71770d0dc5fe92c44c79f9fff51540'
assert sha(old2)=='884e4f472fce503fa122b39eb37fa3f01ca3ca2a9bec13de4172c949ee0f9151'
def fm(b):return b.decode().split('---',2)[1]
body1=r'''# 来源身份和核心处置

本页对应 dynamic_credit/background_probe 的三份来源：README（1,250 B）、末位利润余项正文（6,149 B）和 exact JSON（639 B）。三份原字节均完整复制到同一 evidence 目录，逐源 SHA 与读取范围保存在各自 receipt；跨源比较记录在 `comparisons/comparison-notes.md`。

README 把本批定位为 2026-10-23 个人探索资产，并明确一般 Q-CAG-HALF 仍为 `OPEN`。它将 `terminal_profit_remainder.md` 描述为任意固定非负整数背景、任意实际终局、只用末位最佳回应的精确非负余项分解；将 `audit_terminal_profit_remainder.py` 和 exact JSON 定位为独立 Fraction 核验及输出。脚本源码不在本批三个来源中，不能把 README 的指向当作本轮已读取或重新运行脚本。

本资料处置为 `integrated` 来源地图。其独有价值是把末位余项正文、有限 JSON 和未完成信用义务放在同一身份下；它不构成定理本身，也不改变任何 Q-CAG-HALF、direct-cover 或 dynamic-query-credit 对象的状态。

# 已证、候选与停止边界

README 明确区分四种内容：

- 已证：以实际末位收益 \(v\) 为基准的背景余项版本；
- 已有特例：恰两人时，由现行两人税定理推出 \(F_2(b)-P\le\min(u_1,u_2)\)；
- 未证候选：\(F_r(b)-P\le r\min_i u_i\) 及更强的 \(F_r(b)-P\le(r-1)\min_i u_i\)；
- 未完成义务：末位收益过高时，要从早期真实离轨菜单支付余项，不能只靠末位证书。

因此不能把“真实最小收益在末位时强版本成立”扩展成完整 SPE 中末位总是最小，也不能把一个 69 客户样例的余量写成任意人数的半覆盖结果。README 还要求继续使用早期真实离轨菜单和一个已知非 SPE 模板的缺口，说明终端余项只是后续路线的入口。

# 与现有对象的关系

现有[末位收益与前缀税的根诊断](../引理/末位收益税诊断--引理.md)给出空背景下只用末位 BR 的 \(\operatorname{OPT}_m\le m v+\tau\)，并强调末位高于平均只是根税反例的必要过滤，不是充分反例。本批把这一末位证书推广到任意固定非负背景，但保留相同的“不能替代早期激励”边界。

现有[固定背景下恰两名剩余玩家的税界](../引理/固定背景两人税界--引理.md)使用同一完整策略的真实末位回复和三个 SPE 比较，得到任意背景两人更强税界；本批 README 明确 \(r=2\) 只作为该结果的推论，不把它扩为一般 \(r\) 的归纳。

现有 `dynamic-query-credit-primary` 把每个实际节点的静态信用 \(L_i\) 和自适应罚项 \(Q_i\) 分开，且 HALF?/SHARP? 仍未证；direct-cover README 则把弱匹配、弱平均和旧强平均分成不同支付接口。本批只处理固定背景的终端 \(L+K+J\) 余项，不计算跨节点 \(Q_i\)，不把互斥真实分支合成一个共同钱包。

# 当前接续

下一步必须从完整策略的早期真实偏离菜单构造非循环支付，或更换信用目标；单纯把终端 \(v\) 替换为 \(\min_i u_i\)、重复静态 LP 或增加随机样本都不能闭合一般 Q-CAG-HALF。三源不迁移到 unrelated-machines，也不产生外部新颖性、完整 SPE、一般福利上界或六人结论。
'''
body2=r'''# 1. 对象、量词与来源范围

固定有限非空共同目录、单位客户和 \(r\ge1\) 名剩余单位玩家。客户 \(x\) 的固定背景负载 \(b_x\in\mathbb Z_{\ge0}\) 可以来自合法前缀；代数推导本身甚至不需要验证其可实现性。实际主题依次为 \(A_1,\ldots,A_r\)，令
\[
e_x=\sum_{i<r}\mathbf1_{\{x\in A_i\}},\qquad
l_x=\mathbf1_{\{x\in A_r\}},\qquad
P=\sum_x\frac{e_x+l_x}{b_x+e_x+l_x},\qquad
v=\sum_{x\in A_r}\frac1{b_x+e_x+1}.
\]
只假设末位 \(A_r\) 是实际前缀后的最佳回应；前 \(r-1\) 人的最优性不用于下述分解。对任意比较主题 \(T_1,\ldots,T_r\)，记 \(d_x=\sum_j\mathbf1_{\{x\in T_j\}}\)，其固定背景剩余收益为
\[
R_b(T)=\sum_x\frac{d_x}{b_x+d_x},\qquad F_r(b)=\max_T R_b(T).
\]
所有零分子项取零；空主题、重复主题、零客户和 \(r=1\) 都在该约定下保留。此为原空背景末位证书的全背景推广与精确余项重写，不声明新颖性或一般 half 已证。

# 2. 精确 \(L+K+J\) 分解

定义
\[
L(T)=\sum_{j=1}^r\left[v-\sum_{x\in T_j}\frac1{b_x+e_x+1}\right],
\]
\[
K=\sum_x\left[\frac{e_x}{b_x+e_x+l_x}-\frac{e_x}{b_x+e_x+1}\right],\qquad
J(T)=\sum_x\left[\frac{d_x+e_x}{b_x+e_x+1}-\frac{d_x}{b_x+d_x}\right].
\]
这里也沿用零分子取零。末位最佳回应使 \(L\) 中每个括号非负，因此 \(L(T)\ge0\)。逐客户有
\[
K_x=\begin{cases}
0,&l_x=1\text{ 或 }e_x=0,\\[2pt]
\displaystyle\frac{e_x}{(b_x+e_x)(b_x+e_x+1)},&l_x=0,\ e_x>0,
\end{cases}
\]
所以 \(K\ge0\)。对 \(J\)，若 \(b_x+d_x>0\)，通分得到
\[
J_x=\frac{b_xe_x+d_x(d_x-1)}{(b_x+e_x+1)(b_x+d_x)}\ge0,
\]
因为 \(d_x\) 是非负整数；若 \(b_x=d_x=0\)，则按零分子约定得到 \(J_x=e_x/(e_x+1)\ge0\)，不能代入含零分母的上一式。因此
\[
\boxed{P+(r-1)v-R_b(T)=L(T)+K+J(T).}\tag{1}
\]
证明只需展开 \(L\)，用 \(\sum_j\mathbf1_{\{x\in T_j\}}=d_x\) 消去比较主题和，再由 \(K\) 把 \(\sum_x e_x/(b_x+e_x+1)\) 换成实际早期总收益，末位实际收益由 \(v\) 给出。没有把不同比较分支当成同一实际历史。

空背景 \(b=0\) 时，\(J\) 具体记录比较组合的重复覆盖和实际早期覆盖落在比较组合之外：
\[
J_x=\frac{d_x-1}{e_x+1}\quad(d_x\ge1),\qquad
J_x=\frac{e_x}{e_x+1}\quad(d_x=0).\tag{2}
\]

# 3. 末位界和条件性最小收益替换

取达到 \(F_r(b)\) 的比较组合 \(T^*\)，由 (1) 的非负性得到
\[
\boxed{F_r(b)-P\le(r-1)v.}\tag{3}
\]
如果额外知道实际末位是全体实际收益中的最小者，即 \(v=\min_i u_i\)，则
\[
F_r(b)-P\le(r-1)\min_i u_i\le\frac{r-1}{r}P,
\]
从而 \(F_r(b)\le(2-1/r)P\)。完整 SPE 本身并不保证末位收益普遍最小；因此不能删除该条件，也不能将 (3) 改写成一般 \((r-1)\min_i u_i\) 界。

现有恰两人背景税引理还给出合法特例：由 \(F_2(b)-P\le g_b(A_1,A_1)\)，以及
\[
u_1\ge\sum_{x\in A_1}\frac1{b_x+2}\ge g_b(A_1,A_1),\qquad
u_2\ge U_b(A_1,A_1)=\sum_{x\in A_1}\frac1{b_x+2}\ge g_b(A_1,A_1),
\]
有
\[
F_2(b)-P\le\min(u_1,u_2).\tag{4}
\]
第一条是当前与另一位最多分摊的保底；第二条是实际末位可改 \(A_1\) 的真实最佳回应。这里是现有两人税界的推论，不是由本分解建立的一般人数归纳。

# 4. 真实末位过高时的未解决信用义务

令 \(R^*=L(T^*)+K+J(T^*)\)。将 (1) 改写后，一般背景 half 恰需的余项条件为
\[
R^*\ge(r-1)v-P.\tag{HALF}
\]
这一式在冻结原稿的“真实末位过高时还缺什么”式 (5) 明写；旧派生页曾遗漏该方向，此处随逐式可读性恢复一并准确补回。若要把 \(v\) 换为全体最小收益，分别需
\[
R^*\ge(r-1)v-r\min_i u_i,\tag{5}
\]
或更强版本
\[
R^*\ge(r-1)(v-\min_i u_i).\tag{6}
\]
(HALF)/(5)/(6) 是不同的候选或充分支付条件，不是本页已证结果。它们要求早期真实偏离菜单提供非循环信用，不能由重新排列 (1) 自动得到。现有 dynamic-query-credit 分解中的自适应罚项 \(Q_i\) 和 direct-cover 的弱匹配/弱平均接口正说明了这项困难：多条强制分支互斥，尾部余项不能直接相加成同一钱包。

# 5. 69 客户标量分解和非 SPE 压力测试

来源以四人六主题既有完整 SPE 为标量例：实际路径 \((0,0,0,5)\)，收益 \((10,10,10,18)\)，\(P=48\)，\(F_4(0)=69\)。取比较组合 \((0,1,2,3)\)，覆盖全部 69 名客户且 \(d_x=1\)，则
\[
v=18,\qquad L=\frac{51}{2},\qquad K=\frac{15}{2},\qquad J=0,\qquad R^*=33,
\]
并满足 \(P+3v-F_4(0)=48+54-69=33\)。原稿还说明：主题0的30名早期客户不被末位5覆盖，故 \(K=30/4=15/2\)；比较四主题在末位前缀的收益为 \(15/2,13,13,13\)，故 \(L=72-93/2=51/2\)。强候选 (6) 在该例需 \(3(18-10)=24\)，余项33足够，仅是这个实例的标量核算。JSON 只保存此标量重算，`full_SPE_reaudit=false`；完整 SPE 合法性沿用既有独立审查，不能写成此 JSON 已重审。

来源还给出一个非 SPE 模板。为避免与上文余项 \(K\) 同名，这里将原稿的大主题大小记为 \(\kappa=\operatorname{lcm}(1,\ldots,r)\)：有 \(r\) 个不交大主题；前 \(r-1\) 位按位置选互不交私有主题，第 \(j\) 位私有客户数 \(\kappa/(r-j+1)\)，末位选大主题。其早期真实偏离严格获利，因此不是完整 SPE。对比较组合取全部大主题，有
\[
P=\kappa H_r,\qquad F_r(0)=r\kappa,\qquad v=\kappa,\qquad
L=0,\qquad K=J=\frac{\kappa(H_r-1)}2,\qquad R^*=\kappa(H_r-1).
\]
大 \(r\) 时它违反 (HALF)，说明仅有末位最优性和粗分母保底不能支付早期真实激励。它不是新的完整 SPE 反例，也不反驳 half。

# 6. 状态与关系

该引理是一般背景的精确末位余项/条件界。它不证明 Q-CAG-HALF，不提供一般人数动态信用桥，不产生新的完整 SPE 族，也不迁移到 unrelated-machines。后续若闭合 (HALF)/(5)/(6)，仍须另证所有早期真实偏离、历史平局和跨分支支付；若找不到支付，则这些接口保持未证状态。
'''
proposals={n1:'---'+fm(old1)+'---\n\n'+body1,n2:'---'+fm(old2)+'---\n\n'+body2};rows=[]
for n,after in proposals.items():
 old=(REPO/n).read_bytes();t=old.decode();b=after.encode();assert not any(ord(c)<32 and c!='\n' for c in after);assert all(l==l.rstrip() for l in after.splitlines());before=F/'before'/n;proposed=F/'proposed'/n;cp(REPO/n,before);put(proposed,after)
 defects=[{'character_offset':i,'utf8_byte_offset':len(t[:i].encode()),'code':ord(c),'context_repr':repr(t[max(0,i-15):i+25])} for i,c in enumerate(t) if ord(c)<32 and c!='\n']
 diff=''.join(difflib.unified_diff(t.splitlines(True),after.splitlines(True),fromfile='a/'+n,tofile='b/'+n,n=0));pd=F/(Path(n).stem+'.patch.json');js(pd,{'format':'unified diff stored as JSON string; controls in removed frozen text escaped, decode exact string before use','before_sha256':sha(old),'after_sha256':sha(b),'target':n,'unified_diff':diff})
 rows.append({'target':n,'before_path':str(before),'before_bytes':len(old),'before_sha256':sha(old),'nonLF_C0':defects,'proposed_path':str(proposed),'proposed_bytes':len(b),'proposed_sha256':sha(b),'patch_json':str(pd),'applied_to_shared':False,'proposed_formal_nonLF_C0':0,'proposed_formal_trailing_whitespace':0,'scope':'complete body restored formula-by-formula from actual6149B note/1250README/639JSON, existing frontmatter byte-identical; all lostbackslashes restored, not mechanical control substitution'})
js(F/'replacement-manifest.json',rows)
base=REPO/'archives/customer-attraction/tools/evidence/dynamic-credit-background-probe-20261031/original';refs=[]
for name in ['README.md','terminal_profit_remainder.md','terminal_profit_remainder_exact.json']:
 p=base/name;b=p.read_bytes();q=F/'correct-frozen-source'/name;cp(p,q);refs.append({'path':str(p.relative_to(REPO)),'preserved_path':str(q),'bytes':len(b),'sha256':sha(b),'read_status':'GY actual entire original source, correct note/readme allmath and639JSON allfields; no new program execution or source done'})
js(F/'actual-correct-source-manifest.json',refs)
js(F/'formula-restoration-review.json',{'existing_metadata':'frontmatter preserved byte-for-byte; frozen sources and sharedformals not edited','mathematics_review':[{'section':'resource candidates/relations','source':'1250README all bullets','restoration':'restore TeX F2-P<=min, both Fr-P candidates, OPT<=mv+tau and allinlinevariables; no truth upgrade'},{'section':'lemma1','source':'6149note objects','restoration':'allindicator sums/b>=0/P/v/R/F and zero-numerator convention restored; commonfinitecatalogue/r>=1 retained'},{'section':'lemma2','source':'6149note exactdecomposition eq1-3','restoration':'allL,K,J/Cases andintegerd positivity restored, including b=d=0 exceptional J; algebra reviewed by exact symbolic expansion not newcode'},{'section':'lemma3','source':'6149note eq4 and two-person deductions','restoration':'terminalv versusmin boundary and actualtwo BR/guarantee inequalities restored, no general credit proof'},{'section':'lemma4','source':'6149note remainingobligations eq5-7','restoration':'restore missing directhalf R*>=(r-1)v-P asHALF and retain formermincandidate tags5/6; distinctconditions do not merge'},{'section':'lemma5','source':'6149note69scalar andnonSPEtemplate,639JSONallfields','restoration':'69scalar values51/2+15/2=33 andfull_SPE_reaudit=false retained; directhalf direction cited asHALF ratherthan ambiguousmin version; rename theme-size originalK to kappa avoiding collision withremainderK'}],'new_math_runs':0,'old_success_replays':0,'shared_writes':0,'not_current_render_PASS':'TeX delimiters/C0/whitespace andsourceformula comparison checked only, no claim to currentrender or externalreview'})
put(F/'README.md',r'''# 他人两页完整格式修复提案，尚未应用

Root明确要求逐式核冻结原稿，不能机械替换C0。本目录保全部before原字节/SHA/字符和UTF8偏移，1250B README、6149B数学原稿、639B JSON均实际全文读，完整after拟稿保原frontmatter。

修复恢复所有丢失的LaTeX反斜杠及公式定界，不仅28C0/1TAB。末位余项原稿的直接half未证支付R*>=(r-1)v-P曾被旧派生页漏掉，现另标HALF准确补回；旧最小收益(5)/(6)保留，非SPE模板指向HALF且主题规模改kappa，避免与余项K同名。69客户例标量和full_SPE_reaudit=false按实际639JSON保留。没有新增数学程序或重复旧审计。

replacement-manifest.json是精确before/after SHA提案；proposed/不是共享目标。两patch.json把零context unifieddiff作为JSON字符串保存，删除行中的原C0经JSON转义；需解码unified_diff字段才能得到真实补丁，不能当普通patch直接apply。Root应全文复读before/source/proposed并仅在目标beforeSHA相同后串行应用完整after；本代理没有应用或覆写shared，也不新done这三原来源。
''')
cp(Path(__file__),F/'prepare_recovery.py')
print(json.dumps({'proposals':[{k:x[k] for k in ['target','before_sha256','proposed_sha256','proposed_bytes']} for x in rows],'correct_original_bytes':sum(x['bytes'] for x in refs),'new_math_runs':0,'shared_writes':0},ensure_ascii=False,indent=2))
