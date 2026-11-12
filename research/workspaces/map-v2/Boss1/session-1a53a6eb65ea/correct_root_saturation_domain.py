"""Apply the narrowly reviewed actual-path domain correction, once.

Run from the Boss1 clone after queue synchronization. The old mathematical
bytes and v1 object must still match; all other current registry data remain.
"""
from pathlib import Path
from fractions import Fraction
import copy
import hashlib
import json
import subprocess

ROOT = Path.cwd()
OUT = ROOT/'research/workspaces/map-v2/Boss1/session-1a53a6eb65ea'
OID = 'customer-attraction/root-saturation-fixed-topics-and-five-index-summed-necessary-rows'
BODY = 'archives/customer-attraction/state/引理/根饱和必要行的固定主题与五索引求和--引理.md'
OLD = '3a69be0f24a96fa951503d7e8e1750045a8f3d793f155059c0da284c4a77f5e6'

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p, d): p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')

regpath=ROOT/'research/registry.json'
before_reg_sha=sha(regpath)
reg=json.loads(regpath.read_text())
obj=next(o for o in reg['objects'] if o['object_id']==OID)
assert obj['version']==1 and obj['body']['sha256']==OLD
assert sha(ROOT/BODY)==OLD
before_obj=copy.deepcopy(obj)
baseline_ref=copy.deepcopy(reg['baseline'])
basepath=ROOT/baseline_ref['path']
assert sha(basepath)==baseline_ref['sha256']
baseline=json.loads(basepath.read_text())
for rows in [reg['materials'],baseline['materials']]:
    hits=[x for x in rows if x['path']==BODY]
    assert len(hits)==1 and hits[0]['sha256']==OLD

source=(ROOT/BODY).read_text()
old1='对每个客户x，令bᵢ=1_{x∈Pᵢ}、k=Σᵢ₌₀⁴bᵢ、r=b₀/k（k0时为0），并令'
new1=('为写成程序中仅依赖十位与比较重数的单客户系数，本节将第一节的P₀,…,P₄具体取为同一策略σ的实际有序五行动ABCDE；P₅,…,P₉仍可任取合法标签。第一节的标量关系及其133个保留实际u为独立量的索引求和，对任意十个合法标签仍成立，不受这项编码取法限制。对每个客户x，令bᵢ=1_{x∈Pᵢ}、k=Σᵢ₌₀⁴bᵢ、r=b₀/k（k=0时为0），并令')
old2='旧557行的[完整直方图松弛](../审查/增强索引系统的全型定价与可行点分离--审查.md)保十位b、AB/AE两份8格直方图、Sbranch一份16格直方图及三旧菜单。'
new2=('接入旧557域时，另沿用该域的路径语义：ABCDE是σ的实际有序路径，AEUVW和ABEXY分别是同一σ在历史(A)指定第二位改选E、在历史(A,B)指定第三位改选E后的真实续局；故此时P₅,…,P₉也按这些路径选取。'+old2)
assert source.count(old1)==1 and source.count(old2)==1
source=source.replace(old1,new1).replace(old2,new2)
(ROOT/BODY).write_text(source)
newsha=sha(ROOT/BODY)

obj['version']=2
obj['body']['sha256']=newsha
obj['statement']=('五人同实际根利润u下，任意合法T,Q有G(T,Q)=(57/2)u−(11/2)|T|−|Q|+(4/5)|T∩Q|≥0，另有33482u−2897|T|−1200O≥0、28735u−4447|T|−600O≥0（O为任意五比较并集）。任意十固定标签及五比较槽，保留u为独立标量时，给90固定有序异索引对、10 fixed-opt、10 opt-fixed、1全25对opt-opt及22容量行，共133。将P₀,…,P₄取为σ实际有序五行动后，r=b₀/(Σ₀⁴bᵢ)满足Σr=u，得到正文仅依bits,d的客户系数表；opt-opt含对角，重叠项为(4/5)d²。接入旧557域时沿用其actual=ABCDE与同σ真实续局AEUVW、ABEXY，新增行保该域的条件分解。')
obj['quantifiers']=('∀五人完整σ、∀十合法命名标签、∀五合法比较索引（可重复），133个以该σ实际u为独立量的标量求和成立；bits,d客户系数表示取P₀,…,P₄为σ实际有序五行动。旧557接入另沿用AEUVW、ABEXY的同σ真实续局语义。')
obj['assumptions']=[
    'u固定同一实际根；K已经从承重普遍根刚性/容量定理消去',
    'bits,d客户系数表中，前五命名标签为该σ实际有序五行动；此条件保证Σₓ b₀/(Σ₀⁴bᵢ)=u，分母为零时该项取零。独立133行不要求其余五标签为特定续局。',
    '接入旧557域时，AEUVW、ABEXY须为其定义的同σ真实偏离续局；这是原旧域语义。',
    '仅比较元组真最优时O=OPT_5',
]
obj['scope']='解析必要行及分解保持；区分任意标签标量层与实际路径客户投影层；浮点690/2631列报告不成为精确对偶。'
obj['objections']=('本次直接核对投影恒等式并以完整all-H策略见证任取标签不能替代实际前五；保留一般标量量词及原133行系数，明确旧557已有真实路径语义。完整成熟解析证明与原科学证据复用，未重跑历史优化。')

for rows in [reg['materials'],baseline['materials']]:
    next(x for x in rows if x['path']==BODY)['sha256']=newsha
baseline['coverage_note']=baseline.get('coverage_note','')+'；Boss1仅补根饱和客户系数的实际路径语义，保一般标量层。'
baseline['commit']=subprocess.run(['git','rev-parse','HEAD'],check=True,text=True,capture_output=True).stdout.strip()
newbase=ROOT/'research/registration/baseline-boss1-root-saturation-domain-20261112.json'
assert not newbase.exists()
write(newbase,baseline)
reg['baseline']={'path':str(newbase.relative_to(ROOT)),'sha256':sha(newbase)}

OUT.mkdir(parents=True,exist_ok=True)
review=OUT/'root-saturation-domain-review.md'
review.write_bytes(Path('/workspace/scratch/1a53a6eb65ea/root-saturation-domain-check/report.md').read_bytes())
proposal=OUT/'root-saturation-domain-proposed.json'
write(proposal,reg)
r=subprocess.run(['python','work.py','research','register','--record-file',str(proposal.relative_to(ROOT))],text=True,capture_output=True)
print(r.stdout,end='');print(r.stderr,end='')
if r.returncode: raise SystemExit(r.returncode)
proposal.unlink()

wrong=Fraction(33482,5)-2897-1200*5
true=33482-2897-1200*5
assert wrong==Fraction(-11003,5) and true==24585
audit={
    'status':'registered-local-not-pushed',
    'reviewed_by':'Boss1 plus independent fresh domain worker',
    'base_registry_sha256':before_reg_sha,
    'new_registry_sha256':sha(regpath),
    'before_object':before_obj,
    'after_object':obj,
    'old_baseline':baseline_ref,
    'new_baseline':reg['baseline'],
    'body_before_sha256':OLD,
    'body_after_sha256':newsha,
    'review':{'path':str(review.relative_to(ROOT)),'sha256':sha(review)},
    'counterexample':{'players':5,'large_topic_size':5,'disjoint_singleton_size':1,'policy':'Every legal ordered history chooses the large topic','actual_root_payoff':'1','all_ten_named_labels':'singleton','all_five_comparison_labels':'large topic','incorrect_encoded_root_payoff':'1/5','incorrect_cap_sum':str(wrong),'correct_scalar_cap_sum':true},
    'scope':'Only two projection-domain clarifications, one stable object v1→v2, current material SHA and a new precise baseline; original scalar inequalities and all 133 coefficients retained. No new object or edge, no old LP/BI rerun.',
    'affected_task':'customer-attraction-3a-3a-ee18b662255f036d was available/unowned before this correction; refresh it before claim.',
}
write(OUT/'root-saturation-domain-correction.json',audit)
print(json.dumps({'status':'ROOT_SATURATION_DOMAIN_REGISTERED','object_id':OID,'version':2,'body_sha256':newsha,'baseline':str(newbase.relative_to(ROOT))},ensure_ascii=False))
