from pathlib import Path
import json,hashlib
R=Path('/workspace/scratch/37f0f9248cfc');REPO=R/'boss4-research';C=R/'boss4-next-cache';S=C/'r3-background-pair-probe-primary';E=Path('tools/evidence/background-pair-probe-primary');W=Path('cleanup/workspaces/Boss4/r3-background-pair-probe-primary-next');P='archives/customer-attraction/state/程序/合法背景首对安全值的交替锥探针--程序.md';I='2db24df0ce02d6fd610c'
inv={x['id']:x for x in map(json.loads,(REPO/'cleanup/inventory.jsonl').read_text().splitlines())}
def sha(b):return hashlib.sha256(b).hexdigest()
def put(p,t):p=S/p;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(t,encoding='utf-8')
def js(p,d):put(p,json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def cp(p,q):q=S/q;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(Path(p).read_bytes())
mp=C/'learning-fu-related-probe-inputs/local-export-manifest.json';raw=json.loads(mp.read_text());x=next(x for x in raw['rows'] if x['id']==I);b=Path(x['local_path']).read_bytes();v=inv[I];assert len(b)==5375 and sha(b)==v['sha256'] and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==v['blob'];q=E/'original'/I/v['path'];cp(x['local_path'],q);js(E/'source-manifest.json',[{**v,'preserved_path':str(q),'lines':len(b.splitlines()),'read_status':'FU full actual code reading reused after current sameSHA check; additionally earlier published use as a module dependency preserved'}]);cp(mp,E/'prior-source-and-missing-local-supply.json')
old=REPO/'archives/customer-attraction/tools/evidence/extra-slot-programs-primary';names=['source-manifest.json','comparison/2db24df0ce02d6fd610c/show.json','comparison/2db24df0ce02d6fd610c/source','original/bf46dd86db65a5613aec/source','runs/EXECUTIONS.json'];olds=[]
for n in names:
 b=(old/n).read_bytes();q=E/'reused-module-evidence'/n;cp(old/n,q);olds.append({'path':str(q),'parent_path':str(old.relative_to(REPO)/n),'bytes':len(b),'sha256':sha(b),'read_status':'actual full metadata/caller read GB, base source sameSHA reused; old executions not repeated'})
js(E/'reused-module-evidence-manifest.json',olds)
related=[]
mp=C/'learning-ft-next-readable-contexts/local-export-manifest.json'
for x in json.loads(mp.read_text())['rows']:
 if x['id']!='cae0027749fb8ec7bd95':continue
 b=Path(x['local_path']).read_bytes();v=inv[x['id']];assert sha(b)==v['sha256'];q=E/'related'/x['id']/x['path'];cp(x['local_path'],q);related.append({**v,'preserved_path':str(q),'read_status':'FU full1976B math already read; currentSHA reused, source currently FU primary not extra GB done'})
js(E/'related-source-manifest.json',related)
contexts=[]
for n,mode in [
('archives/customer-attraction/state/审查/额外槽扫描的实际强桥目标与两份定义级核验--审查.md','full actual GB read'),
('archives/customer-attraction/state/计算/响应恒等式与分支条件的精确回归--计算.md','lines1..135 actual read, includes all historical probe table; not full source completion'),
('archives/customer-attraction/state/反例/任意合法背景的前两人额外槽安全值--反例.md','full FU math read reused, currentSHA verified'),
]:
 b=(REPO/n).read_bytes();q=E/'context'/n;cp(REPO/n,q);contexts.append({'path':n,'snapshot':str(q),'bytes':len(b),'sha256':sha(b),'read_status':mode})
js(E/'context-manifest.json',contexts)
cp(C/'learning-gb-next-readable-README/local-export-manifest.json',E/'next-readable-README-local-manifest.json');cp(C/'local_blob_export.py',E/'authorized-local-export-helper.py.txt')
body=r'''---
id: "customer-attraction/legal-background-first-pair-security-alternating-cone-probe"
kind: "program"
type_tag: "程序"
title: "合法背景首对安全值的交替锥探针"
status: "full-source-and-LP-contract-read; ideal-normalization-and-baseline-proved; numerical-main-not-replayed"
summary: "5375B原码完整保全，区分精确整数初始全策略、近似Γ锥与两类浮点LP；给首对归一化的有界性和全兴趣基线1解析说明，260/500旧叙述及另一程序调用依赖不冒成本main运行。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-31bbb6cfd6594bc8bb076db7b2950993/aggregate_security/background_pair_probe.py"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-31bbb6cfd6594bc8bb076db7b2950993/aggregate_security/background_pair_probe.py"
---

# 合法背景首对安全值的交替锥探针

## 实际原件、模型和目标

[5375B原源码](../../../../tools/evidence/background-pair-probe-primary/original/2db24df0ce02d6fd610c/research/workspaces/customer-attraction/R-31bbb6cfd6594bc8bb076db7b2950993/aggregate_security/background_pair_probe.py)SHA70bf8fe44b71958d8d808a41e470f68814c01fe0bb3755dcf7f25ac5212316d5，两冻结提交同字节。FU已逐函数全文读，GB核同SHA诚实复用，不假称重新第一读。它无本地规范CAG依赖，导标准库及NumPy、SciPy.optimize.linprog；main最后有__name__=='__main__'保护。本批只读取，不导入或执行源码，不认证旧NumPy/SciPy/HiGHS版本。

固定n≥2名剩余单位提供者、k≥1个共同主题标签、一个合法沉没前缀的主题计数向量b∈Z_+^k，ℓ=Σb。客户兴趣类型为全部非空mask J⊆[k]，t=2^k−1；重数w_J初始为非负整数，LP中放松为非负实数。M_(a,J)=1_(a∈J)，s_J=Σ_ab_a M_(a,J)为真实过去客户负载。允许重复、空覆盖主题、同覆盖标签、任意离轨历史和平局；无兴趣客户对利润/覆盖恒0而被省去，所有w0可表示零有效客户。

真正静态安全值用n−1个竞争槽且竞争者不观察查询：
\[
v_n(s;w)=\max_{p\in\Delta_k}\min_{q\in\mathbb Z_+^k,\ |q|=n-1}
\sum_Jw_J\frac{\sum_ap_aM_{aJ}}{1+s_J+\sum_aq_aM_{aJ}}.
\]
程序攻击在给定背景后、固定一份完整SPE策略的实际首两位收益u1+u2≥2v_n。不是r槽extra-one，不是零根全位置pair、一般根聚合或six-player half。合法背景能由相应目录行动实现，不保证这串背景在原根SPE实际可达。

## representation：两种分母的来源

程序枚举全部n−1主题多重集，转为标签计数q，并形成
\[
R_{q,J}=1/(1+s_J+q\cdot M_{\cdot J}),\quad
L=\operatorname{lcm}(1,\ldots,\max_Js_J+n).
\]
这里+1是独立额外查询自身。后面的实际玩家利润分母则是s_J+c_J(z)，因为z中已经包括该玩家自身，不应再加1。代码的max(分母,1)仅处理分子M=0的零项；有贡献项中当前玩家覆盖该类型，真实分母至少1，clamp不改利润。不能把两个不同分母的+1照搬成缺项/重复项错误。

main选n≤6、k≤7、ℓ≤8、初始w≤15，故s+n≤14、L≤360360；每个整数收益内积绝对值≤127·15·360360=686485800，处于int64范围。在此明确main范围内，初始整数乘法/整除保真。函数本身未作通用输入/大整数安全校验；任意扩大n,k,背景或重数时LCM、NumPy固定宽度、递归和内存都须另审，不称通用精确求解API。

## policy_cone：完整有序策略与理想真实IC锥

walk(h)对每个有序历史递归算k个孩子的规范续局；终端返回标签计数，只用于利润计算。以整数缩放利润选择当前最佳行动，真正相等时用共享rng选；actions[h]保全部有序历史，未按计数合并策略。每个h和每个非规定b生成整行真实差
\[
\Gamma_{h,b;J}=M_{\sigma(h),J}/[s_J+c_J(z_h)]
-M_{b,J}/[s_J+c_J(z_{hb})].
\]
利润比值统一约定分子0时贡献0，有贡献时真实分母至少1。两个叶均沿同一完整策略在各自改变后的历史继续。原始行先按LCM表示为整数，np.unique去重**完全相同的整数行**，再转double除L；仅约束冗余去重，不匿名化actions。全部节点数N=Σ_(d=0)^(n−1)k^d，原始非自身比较行(k−1)N；main k>1时为k^n−1。它是每次构造的静态上界/结构计数，不是原260轮实际日志。

对精确有理Γ，客户锥恰为w≥0、Γw≥0，完整一步偏离原则给固定σ仍是SPE。代码存的是double近似Γ和近似LP可行性，任意返回w不能因此冒作精确IC证书。初始整数实例生成正确也不自动认证后面改过的浮点客户质量。

沿根actions得到actual叶z，首两人合计的线性行
\[
P_J=[M_{z_1,J}+M_{z_2,J}]/[s_J+c_J(z)].
\]
它是在这一固定策略的实际终局付款，既不是冻结最优查询也不是两独立分支拼起来的钱包。代码归一P·w=1。

## 两类LP的全部变量与量词

| 函数 | 精确理想输入及优化式 | 代码实际输出 |
| --- | --- | --- |
| cone_step | 固定p、变量w≥0和自由z，最大z；Γw≥0，P·w=1，且对**每个**合法静态q有Σ_Jw_J R_(q,J)(p^TM)_J≥z | SciPy/HiGHS浮点w,z；LP失败raise ValueError，不补精确证书 |
| security | 固定w，变量p≥0、Σp=1和自由v，最大v；对每个静态q有Σ_(a,J)p_aM_(a,J)R_(q,J)w_J≥v | 浮点最优查询p和值v，不附原始/对偶精确有理证书 |

数组pay=(R*w)@M.T按q为行、a为列；两函数A_ub分别是[-Γ,0]/[-beta,1]及[-pay,1]，beta=R*(p@M)。因此安全对手覆盖全部n−1槽多重集，允许重复；每个LP都固定一份查询分布而不让竞争元组看到查询实现。固定背景、固定完整策略和全部兴趣类型才是这个锥的域，不穷尽所有σ、目录、人数或背景。

一次交替先cone_step得新w，再security为该w优化p；σ与Γ不随新w重新逆向归纳。理想精确可行条件下，两步单调不降固定p/再优化p的目标，但这不是全局联合优化证明；double容差还可能破坏精确单调/可行。代码的early-stop不能当全锥已最优。

## 归一化有界性及ratio=1的通用基线

以下是针对精确理想LP的解析说明，不是本批新求解输出。任意可行非负w，首人实际节点完整IC给对每个主题a的真实偏离收益至少L_a/(ℓ+n)，其中L_a=Σ_(J含a)w_J；因为过去至多ℓ、余下至多n个覆盖者。故L_a≤(ℓ+n)u1。所有类型非空，有Σ_Jw_J≤Σ_aL_a≤k(ℓ+n)u1≤k(ℓ+n)，最后用u1+u2=1。于是P·w=1下w域有界，安全目标亦有限；这不把浮点容差当精确界。

全兴趣类型J=[k]单独取w_J=(ℓ+n)/2、其余0，是任意形式策略的合法归一化点。每个后续终局各角色都覆盖该类型，利润都是w_J/(ℓ+n)=1/2，所有真实IC恰平局，P·w=1；任意合法静态q和查询的同一安全价也是1/2。因此对任意p，理想cone_step至少能达到z=1/2，归一ratio=2v至少1。可清分母成不同单位客户，比例不变。

所以“最优观察ratio1”并非普遍pair证明或距反例很近的证据；它至少与一个所有策略都有的退化基线相容。这仅给理想最优的下界，**不说所有锥最优都等1**，也不认证原float输出恰等有理1。零客户原实例不满足P·w=1，归一化搜索本来只讨论非零严格分离。

若最终获得精确有理w,p，且全部Γw≥0、P·w=1、所有q的安全价严格>1/2，则同一σ真有u1+u2<2v_n；清w分母为单位客户后齐次缩放，比例不变。这才是原单位模型反例的路线。独立逐坐标四舍五入会破坏紧IC面，需实际精确有理可行重构和全历史/全部静态列核验。当前代码没有这些步骤；strict浮点阈值不代替它们。

## main的实际配置、停止和输出

seed310102181；--trials默认160、--output必填、--large开关。普通(n,k)为(3,5),(3,6),(4,5),(4,6),(5,6)，large为(5,7),(6,6),(6,7)。背景长从1/2/3/5/8取，每槽独立均匀标签；初始类型按密度.15/.4/.7/1保留，正重数1…15。共享rng还消费全部逆向平局抽样，不能只凭trial号恢复一个输入。

每trial两个起点：初始w的security查询和均匀查询；每起点最多7轮，ratio<old+10⁻⁹可提前停。最多一次初始security加14组cone_step/security，即最多29次LP调用/完整trial，**不是已发生次数**。incumbent更新用ratio>max+10⁻⁸，candidate保存/立即返回用ratio>1+10⁻⁷；小于阈值的真正差也可能不触发。两个起点、早停、异常和提前candidate均改变真实计数，不能把260乘29说成实际LP量。

result初为numerical_only/trials0/max_ratio0/candidate null。incumbent另含trial/n/k/background/start/iteration、归一pair_payment1及static_security浮点值；candidate仅存浮点weights/p、n/k、背景、actual及所有字符串有序history键动作，根history键为空串。两个改善阈值不同，max_ratio/incumbent不保证与candidate同一数值点；没有整数恢复、精确SPE、真实v对偶或half证书，也不保存每trial输入、完整CLI和库版本。无candidate时每10trial和末尾覆写--output，末尾打印FINISHED。--trials未强制为正，非正走空循环不产生样本；输出父目录不自动建立。LP失败ValueError及文件I/O异常无全局捕获，可只留下早先进度，不能把文件存在或trials字段当成功完成。本轮未执行这些输出写入。

## 旧记录、已实际使用的函数与本次边界

[1976B原聚合README](../../../../tools/evidence/background-pair-probe-primary/related/cae0027749fb8ec7bd95/research/workspaces/customer-attraction/R-31bbb6cfd6594bc8bb076db7b2950993/aggregate_security/README.md)称260策略锥观察最大1。其312B原JSON和330Blarge JSON、SSR两件已在FU纯本地读取缺，GB复用缺失回执不重试，不补argv/输出/260份输入。default160不能认证作者260如何调用。后续[响应资源](../计算/响应恒等式与分支条件的精确回归--计算.md)另转述500阴性探索，仍是作者历史，不能加成760个本批样本或这份SHA已验证main运行。

另有已实际成功的不同3194B extra_slot_decorrelation_probe.py，通过importlib以名字base载入本5375B同SHA模块，仅调用representation和policy_cone。该调用者原码、旧来源绑定和[EXECUTIONS完整捕获](../../../../tools/evidence/background-pair-probe-primary/reused-module-evidence/runs/EXECUTIONS.json)本批已读，旧一次75样本入口13.116131986秒exit0有其真实身份；**base.main未执行，security/cone_step也不是该调用者使用的函数**。调用者使用零背景及自己的强聚合目标，不能把它的成功转成GB的非零背景首对主程序已跑或所有数值路径均测。详[已有完整审查](../审查/额外槽扫描的实际强桥目标与两份定义级核验--审查.md)；不重复那次成功或其它父方脚本。

任意合法背景pair的当前普遍真值已由[PB-extra解析反例](../反例/任意合法背景的前两人额外槽安全值--反例.md)排除，甚至更弱n槽竞争的门槛也败；本程序有限阴性不恢复它。该大背景尚未证为根SPE实际可达，真零根聚合、安全值全位置pair及six-player half各自保持合同，不被此程序本身证明/反驳。

GB新增原CLI/模块导入/数学程序/LP/SPE/随机扫描均0，FU成功的新多项式检查也未重跑。新增内容是源程序自足数学合同、归一化有界性/全兴趣基线及现有函数运行与main范围的准确区分，无外审、新颖性或算法时界认证。[本批证据](../../../../tools/evidence/background-pair-probe-primary/README.md)保原件/依赖/读取/缺失与关系，phase2不导旧图或认mapper。
'''
put(P,body);js(E/'formal-resource-manifest.json',[{'path':P,'bytes':(S/P).stat().st_size,'sha256':sha((S/P).read_bytes())}])
put(E/'README.md',r'''# 合法背景首对程序资源

单primary5375B完整原码已FU全文实读，本批sameSHA复用、全仓比较并给独立自足程序对象。理想精确Γ/两LP/归一化有界性与全兴趣ratio1基线的解析合同，与浮点实现、作者260/500历史、不同旧调用者的函数使用分别标明。

GB所有原CLI/模块导入/LP/SPE/数学程序执行0，不重跑旧成功或FU新增多项式。原依赖NumPy/SciPy仅源码读取，不声明环境重现。先前缺312/330/SSR回执复用，0重试网络；新helper只核下批3README齐且未数学读。成功receipt在actualclaim/owner后生成，Root先推正文依赖再done；代理0shared Git/show/领/done/checkpoint/身份公屏。
''')
cp(Path(__file__),E/'build_resources.py')
print(json.dumps({'stage':str(S),'primary_bytes':5375,'primary_lines':json.loads((S/E/'source-manifest.json').read_text())[0]['lines'],'new_formal_bytes':(S/P).stat().st_size,'new_math_runs':0},ensure_ascii=False,indent=2))
