"""Boss merge of three actual failed final reviews; no review is generated."""
from pathlib import Path
import hashlib
import json

P = Path(__file__).resolve().parents[2]
def load(path):
    return json.loads(path.read_text(encoding='utf-8'))
def write(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

plan = load(P/'history/final-review-f733447a84a1/content-plan.json')
authored = load(P/'authored-content.json')
for key in ['sources', 'transcription_blocks', 'study_blocks']:
    plan[key] = authored[key]
plan['observations'] = [x for x in plan['observations'] if x['pass'] == 1]
artifacts = plan['evidence_artifacts']
by_path = {x['path']: x['id'] for x in artifacts}
by_id = {x['id'] for x in artifacts}

def register(relative, identifier=None, crop=None):
    relative = str(relative)
    if relative in by_path:
        return 'artifact:' + by_path[relative]
    path = P/relative
    if not path.is_file():
        raise ValueError('actual evidence is missing: ' + relative)
    identifier = identifier or 'terminal-' + hashlib.sha256(relative.encode()).hexdigest()[:16]
    if identifier in by_id:
        raise ValueError('duplicate artifact ID')
    record = {'id': identifier, 'path': relative, 'kind': 'evidence',
              'format': 'image' if crop else 'text'}
    if crop:
        if hashlib.sha256(path.read_bytes()).hexdigest() != crop['sha256']:
            raise ValueError('actual crop bytes differ from independently recorded hash')
        record['source_crop'] = {key: crop[key] for key in ['page_id', 'bbox_px', 'dpi']}
    artifacts.append(record)
    by_path[relative] = identifier
    by_id.add(identifier)
    return 'artifact:' + identifier

reports, all_crops = [], []
for role, index_name, narrative in [
    ('visual', 'principle3-crops.json', 'findings.md'),
    ('math', 'terminal-crop-index.json', 'full-review-notes.md'),
    ('adversarial', 'targeted-crop-index.json', 'final-findings.md')]:
    folder = Path('proposals')/('ra12_'+role)/'final-f733447a84a1'
    report = load(P/folder/'final-report.json')
    if report['reviewer_id'] != '/root/ra12_'+role or not report['findings']:
        raise ValueError('the actual failed final report is not the expected independent record')
    if report['snapshot_sha256'] != 'f733447a84a1c488a3814b28d1c180ffabb8fd72dbd531426b8e5c16b7465148':
        raise ValueError('reviewed snapshot differs')
    for name in ['final-report.json', 'source-first-reread.md', narrative, index_name]:
        evidence = register(folder/name, 'failed-final-'+role+'-'+Path(name).stem)
        if name in ['final-report.json', narrative]:
            reports.append(evidence)
    data = load(P/folder/index_name)
    for crop in data if isinstance(data,list) else data['crops']:
        crop = dict(crop)
        crop['evidence_id'] = register(crop['path'], crop=crop)
        all_crops.append(crop)
for crop in load(P/'audit/final-followup/crop-index.json'):
    crop = dict(crop)
    crop['evidence_id'] = register(crop['path'], crop=crop)
    all_crops.append(crop)
for name in ['crop-index.json', 'boss-observations.json', 'source-coverage-before.json']:
    register('audit/final-followup/'+name, 'boss-terminal-'+Path(name).stem)

decisions = [
    {'number': 15, 'source_ids': ['RA12-P001-U07'],
     'problem': '第三条的与几之间独立笔簇被省略，须决定并标注有依据的读法',
     'candidates': [
         '原有独立字形，依同手字形择优校读为是；低至中等置信，字形存在比字值更确定，正文标明择优校读。',
         '读列以补全函数列语义；语义较顺，但缺少独立右刂，不能由Egorov命题倒推原字必为列。',
         '读也或视为改笔/几的前置连笔；同手也的宽外折和上提不合，原笔簇及后续几乎各有完整起收。'],
     'observation': '三人均实看800及1200图。原矢量seq127–128为的，seq129自有上回折、中轴和下扫，seq130起几，131–133为乎；P1/P2/P5是字提供对照。',
     'forward': '先按字形将独立笔簇保留下来，再以P3/P4的可测函数列和Egorov解释口语提纲；有限测度下几乎处处收敛到有限极限确有几乎一致收敛。',
     'backward': '是、列、也的不同口语补法并不改变Egorov的数学释义，因此数学不能证明字值唯一；欠刂与同手也不同则反向降低这两个字形候选。无需补出原稿没写全的函数列。',
     'pages': ['p0001', 'p0002', 'p0005']},
    {'number': 16, 'source_ids': ['RA12-P001-U05', 'RA12-P001-U06'],
     'problem': '例题并下限等号后只有点迹，原正文把规范化的1说成直接可读',
     'candidates': [
         '原迹仅点状，按有限列惯例从1枚举；正文可规范写i=1，但必须注明该1来自上下文恢复。',
         '小点本身就是可直接辨清的完整数字1；与同手P2和P6细长竖1不符。',
         '从0或其他固定整数重编号；数学可行但需整列一致重标，不是该点的视觉证据。'],
     'observation': '1200dpi与原seq216给出约3.6×4.8px水滴框[1050.72,1962.33,1054.32,1967.09]；等号后无分立长竖。三人对比实际P2/P6下标1。',
     'forward': '把n个开区间统一编号I_1到I_n，则有限并与对称差估计均定义明确；规范后的首编号与学习稿证明一致。',
     'backward': '有限并在统一重编号下不变，所以证明正确不能证实原笔就是1。直接当完整1与原像不符，从0开始而仍只给I_1到I_n会引入未定义I_0。',
     'pages': ['p0001', 'p0002', 'p0006']},
    {'number': 17, 'source_ids': ['RA12-P001-U07'],
     'problem': '第三条每与个之间的微短提未记录，须区分平行句式恢复与清楚可读的一横',
     'candidates': [
         '按同页前两条平行句式，把独立短提校读为一的极简写法；弱至中等置信并在原位标校读。',
         '普通提笔或点迹，不独立计字；其幅度很短使该候选仍有视觉解释力。'],
     'observation': '原seq108范围[347.142,1209.033,353.917,1214.079]，独立左厚右上收细；前两条同位一宽约29、30px，第三处约6.8px。三人原图对照均支持一为优势候选但不唯一。',
     'forward': '每一个与前两条同序的量词模式吻合，所解释的是每一收敛可测函数列；选择一时保留微短笔及恢复性质，未假装看见完整长横。',
     'backward': '每个与每一个的数学量词等价，Egorov本身不能区别这两个写法；因此仅由同位笔势和平行句式作有界置信校读，不把推导当直接图像证明。',
     'pages': ['p0001']},
    {'number': 18, 'source_ids': ['RA12-P001-U05', 'RA12-P001-U06'],
     'problem': '例题原式两左一右及题面收笔被标准排印掩盖，需要分别保留原迹与规范数学层次',
     'candidates': [
         '原式物理上两枚左括、仅一枚右括；保真保留计数，不强判右括配哪层，学习稿令m作用于整个对称差并规范闭合。条件末另有独立右弧，间末弧择优解释为字框收笔而非新增数学分组。',
         '原式已有两枚重叠右括；原路径与800/1200图均只有一枚独立右弧，不支持此说。',
         '并号前长弧只是并号的一部分，故仅一左一右；并号自身完整且长弧独立，反对此读法。',
         '题面所有右括样弧都形成新的数学条件或配对分组；缺相应左括，且间字的同手门框有相同弧，不能强赋新条件。'],
     'observation': '三人独立核对原seq200外左、231内左、230唯一右弧、232小于号。有限条件的m(E)自有右括而∞后另有右弧；间末弧与同页间字的门钩同构，独立括样笔仍为备选。',
     'forward': '对称差两操作数是E与整个有限并U，测度的输入为集合EΔU。因此规范式m(EΔU)<ε类型正确，补足或省去内层冗余括均不改命题。',
     'backward': '若让m只作用E，再取m(E)ΔU，会把数与集合进行集合运算，类型不成立。反向追踪原路径只得一个右弧，故不能把规范配对伪称原稿已经写全。',
     'pages': ['p0001']},
    {'number': 19, 'source_ids': ['RA12-P004-U11'],
     'problem': '并集估计前引导词原选要估，三人终审同手字形支持要求',
     'candidates': [
         '要〔校读：求〕；中等至较高置信，依据右上独点、中轴过横及下钩与P1要求同构。',
         '要估；需要分立亻和古的口形，当前没有相应两部布局。',
         '要证；P3下证的左讠与右正分立，与目标中央长轴不同。'],
     'observation': '三人实际800/1200定向看P4[330,2095,550,2318]，并与P1要求及P3下证比较。原字右上斜点、横穿中轴、下部回环共同支持求。',
     'forward': '要求引出帽F交集后的补集损失估计，顺接差集分解与三项误差预算；蓝色学习证明依次可加性及δ/3预算成立。',
     'backward': '要估或要证也能描述同一证明任务，语义不能决字；几何缺亻/讠降低这两候选。任一引导词都不能使原次可加处的严格号普遍成立，原错式仍保留并独立订正。',
     'pages': ['p0001', 'p0003', 'p0004']},
    {'number': 20, 'source_ids': ['RA12-P003-U20', 'RA12-P005-U18'],
     'problem': '两个来源矩形略漏原待填横线左尖与s.t.末点，正文已有内容但映射范围需恢复',
     'candidates': [
         'P003-U20左界取1891，P005-U18右界取1760，其余坐标保留；包含原向量边界和被漏像素，分区对应不变。',
         '保持旧框1895和1741；会使横线左尖8个及s.t.末点12个阈值像素仍在所有来源矩形之外。'],
     'observation': '三人原图确认P3路径487左端x1893.747，P5路径500横向1753.415至1756.691。Boss独立全页阈值225检查复现8+12个框外像素，均属已转写原单元。',
     'forward': '新左界1891小于1893.747，新右界1760大于1756.691，原纵向框已包含对应笔迹，故新矩形完整包住两笔。按相同源/区相交规则重新生成双向映射。',
     'backward': '对旧框作像素集合差得到8和12个确切漏点，证明旧映射并非全包。扩大仅数像素，不跨新的分区边界；反查邻行和邻来源未被纳入新的内容主张。',
     'pages': ['p0003', 'p0005']}
]
decision_path = P/'audit/final-followup/recovery-decisions.json'
write(decision_path, {'note_id': 'RA12', 'boss': plan['review_policy']['boss_id'],
                     'superseded_snapshot': 'f733447a84a1c488a3814b28d1c180ffabb8fd72dbd531426b8e5c16b7465148',
                     'three_actual_reports': reports, 'latest_nonauthor_acceptance_pending': True,
                     'decisions': decisions})
synthesis_id = register(decision_path.relative_to(P), 'boss-terminal-recovery-decisions')
for d in decisions:
    rid = f'RA12-REC-{d["number"]:02d}'
    evidence = sorted(set(reports+[synthesis_id]+[
        x['evidence_id'] for x in all_crops if x['page_id'] in d['pages']]))
    record = {'id': rid, 'source_ids': d['source_ids'], 'problem': d['problem'],
              'candidates': [{'id': f'candidate-{i}', 'text': text, 'evidence_ids': evidence}
                             for i,text in enumerate(d['candidates'],1)],
              'selected_candidate_id': 'candidate-1', 'status': 'unresolved',
              'evidence_ids': evidence,
              'forward_validation': {'status':'pass','method':'由原像结构及前文对象进行正向验证',
                  'inputs':d['observation'],'result':d['forward'],'evidence_ids':evidence},
              'backward_validation': {'status':'pass','method':'以竞争候选、类型或几何反查进行逆向检验',
                  'inputs':d['candidates'][0],'result':d['backward'],'evidence_ids':evidence},
              'return_to_image': {'observation':d['observation'],'evidence_ids':evidence},
              'reviewer_id':'/root/ra12_adversarial','session_id':'/root/ra12_adversarial'}
    plan['recoveries'].append(record)
    plan['issues'].append({'id':f'RA12-ISSUE-{d["number"]:02d}','status':'open',
        'description':d['problem']+'；Boss合并三份独立记录后的提议，待最新稿非作者第二遍接受。',
        'related_ids':d['source_ids']+[rid],'evidence_ids':evidence,'resolution':''})
for number, extra in [(4,[15,16,17,18]),(8,[19])]:
    rec = next(x for x in plan['recoveries'] if x['id']==f'RA12-REC-{number:02d}')
    rec['problem'] += '；本轮完整终审的新细项另见'+','.join(f'RA12-REC-{x:02d}' for x in extra)+'。'
    rec['evidence_ids'] = sorted(set(rec['evidence_ids']+reports+[synthesis_id]))
    issue = next(x for x in plan['issues'] if x['id']==f'RA12-ISSUE-{number:02d}')
    issue['related_ids'] += [f'RA12-REC-{x:02d}' for x in extra]
for rec in plan['recoveries']:
    rec['status'] = 'unresolved'
for issue in plan['issues']:
    issue['status'] = 'open'
    issue['resolution'] = ''
for source in plan['sources']:
    if any(source['id'] in r['source_ids'] for r in plan['recoveries']):
        source['status'] = 'unresolved'
pending = {x['id'] for x in plan['sources'] if x['status']=='unresolved'}
for key in ['transcription_blocks','study_blocks']:
    for block in plan[key]:
        if pending.intersection(block['source_ids']):
            block['status'] = 'unresolved'
write(P/'content-plan.json',plan)
frozen = P/'audit/final-freeze.json'
if frozen.exists():
    frozen.unlink()
print(json.dumps({'recoveries':len(plan['recoveries']),'issues':len(plan['issues']),
                  'new_decisions':len(decisions),'registered_evidence':len(artifacts),
                  'latest_second_pass_pending':True},ensure_ascii=False))
