import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parents[3]
folder = Path(__file__).resolve().parent
task_id = folder.name
task = json.loads((root / 'research/operations/map-v2/tasks' / (task_id + '.json')).read_text())['definition']

def ref(path):
    path = Path(path)
    return {'path': path.relative_to(root).as_posix(), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}

edge_id = 'ca-r22-common-core-pays-endogenous-credit-one-sharpness'
edge_path = folder / 'common-core-sharpness.json'
edge = {
    'edge_id': edge_id, 'kind': 'implies', 'status': 'accepted',
    'source_ids': ['R22-POSITIVE-DEPTH-SECURITY-NO-v1'],
    'target_ids': ['B10-ENDOGENOUS-WATERFILL-SHARP-v1'],
    'premises_mode': 'all', 'relation_mode': 'unconditional',
    'conditions': '固定R22的53单位四人七标签完整σ0和真正v4；每个整数c≥0给所有标签添加相同c个共同单位客户。仅在辅助水位计算中降低actual第二位X0质量，原完整单位SPE不改。严格有理夹界量化c>0；c=0时Γ=0。',
    'roles': {
        'R22-POSITIVE-DEPTH-SECURITY-NO-v1': '提供同一完整σ0、精确静态鞍点t0、actual唯一低尾和23客户负载谱的真实单位基底。',
        'B10-ENDOGENOUS-WATERFILL-SHARP-v1': '通过共同核心平移和真水位方程得到指定族的全部系数一锐性、显式门槛和收敛常数。'
    },
    'explanation': '给任意四人叶添加共同核心后每人恰增c/4，全部有序历史IC和平局不变，静态K矩阵每项也增c/4，同一p/Q仍匹配，故tc=t0+c/4。实际X0的12个负载2和11个负载3客户在辅助质量ρ下密度为12/(1+ρ)+11/(2+ρ)+c/(3+ρ)，其与tc之差在0处正、1处−D，严格递减，故唯一真水位ρc∈(0,1)。令δ=1−ρc，根返还Γ=cδ/[4(4−δ)]，并由密度差逐项得D=δ[6/(2−δ)+11/(3(3−δ))]+Γ。于是δ≤16D/(c+4D)，δ→0，Γ/D→1。对c>0，Γ/D=c/(c+H(δ))，H=24(4−δ)/(2−δ)+(44/3)(4−δ)/(3−δ)严格递增于608/9和94之间，给全部严格夹界、c(1−Γ/D)→608/9及c>94K/(1−K)的显式门槛。K<0以c=0处理。本条完整解析推导无需对有限二分数据外推。根−tc恒27075/2924>0；Wc−4tc及half余量均正，不能移作低根聚合失败或六人half反例。详证见本包mathematical-review.md。',
    'whole_result': 'R22指定同一53单位四人完整σ0经任意整数共同核心c≥0平移后仍为完整SPE，真正v4(c)=28481/2924+c/4，actual唯一低尾缺口D=647/8772不变，根严格高于阈值。唯一ρc∈(0,1)满足12/(1+ρc)+11/(2+ρc)+c/(3+ρc)=v4(c)，Γ=c/(3+ρc)−c/4，D=B(1−ρc)+Γ且Γ/D→1。每个c>0有c/(c+94)<Γ/D<c/(c+608/9)，c(1−Γ/D)→608/9；每个0≤K<1取整数c>94K/(1−K)使Γ>KD，K<0取c=0。因此内生真实阈值共同信用系数1不能统一减小。',
    'scope': '只量化这个指定完整四人单位客户族及真实静态v4，不量化所有四人SPE、root<tc子域或六人模型；ρ仅为辅助分数叶。',
    'evidence': [ref(folder / 'mathematical-review.md'), ref(root / 'archives/customer-attraction/state/定理/内生安全水位的信用系数一锐性--定理.md'), ref(root / 'archives/customer-attraction/state/构造/五十三单位四人完整策略与内生水位基准--构造.md'), ref(root / 'archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md')],
    'reviewed_by': 'Boss4',
    'review_note': '实读精确两端与承重证明，逐项核共同核心对所有IC/静态矩阵的同移、唯一真水位、返还分解、H单调和极限；保c=0边界及root高阈值限制。成熟大数组和历史执行按同SHA合同复用，未重跑旧IC、LP或二分。'
}
edge_path.write_text(json.dumps(edge, ensure_ascii=False, indent=2) + '\n')
receipt = {
    'coverage': {
        oid: {
            'state': 'linked', 'object_pin': task['input_pins'][oid], 'edge_ids': [edge_id],
            'comparison_scope': '实读本包R22 v3、B10 v2和CAG-MODEL v1，比较同一σ0的单位输入、完整历史/静态证书合同与全部共同核心解析变换。三张400动作表按既有同SHA证明及真实身份比较复用，未再次逐数组核IC；新推导与实际阅读边界见本包数学审读。无任务follow-up对；deferred未冒算实读。',
            'reason': ('同一完整SPE及真正静态鞍点提供真实单位基底；共同核心变换保所有有序历史IC，完整推导出目标整条锐性结论。正深度逐人floor失败不否聚合/half。' if oid.startswith('R22') else '精确恒等式与H单调支付指定族全部参数、严格夹界和收敛常数；原根始终高于阈值，不能将此锐性扩大为root<t子域的预算障碍或six-half反例。')
        } for oid in task['object_ids']
    },
    'assets': [], 'closed_overlaps': [], 'follow_up_tasks': []
}
(root / 'map/receipts' / (task_id + '.json')).write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + '\n')
print(edge_path.relative_to(root))
