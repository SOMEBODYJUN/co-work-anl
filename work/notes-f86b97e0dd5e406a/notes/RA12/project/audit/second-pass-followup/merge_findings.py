"""Apply the actual trio's complete a71365ac/54e496a6 second-pass findings.

All prior reports remain immutable. This authors corrections and proposals only;
it does not create review observations, acceptances, or a final review chain.
"""
from pathlib import Path
import copy
import hashlib
import json
import shutil
import sys

P = Path(__file__).resolve().parents[2]
ROOT = P.parents[4]
sys.path.insert(0, str(ROOT / 'tools'))
from build_note_ledger import build
from catalog_note_evidence import catalog

def read(path):
    return json.loads(path.read_text(encoding='utf-8'))

def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

before = {name: sha(P / name) for name in ['source-transcript.md', 'study-notes.md', 'source-target-map.json']}
assert before == {
    'source-transcript.md': 'a71365aceea5c44e9c343143116ed3434a4d8f91d07bfd5080bb3f9b73d4ee9b',
    'study-notes.md': '54e496a6a0b3913d5870818915c4d824c4e1d5ef2dbec528cb038ecabb096f35',
    'source-target-map.json': 'f53dd5aaacc67ea1abbdbb2b3b9983207af11cb4e45506a6cf2fc5f22779e1ca',
}
plan, ledger, manifest = (read(P / name) for name in ['content-plan.json', 'ledger.json', 'manifest.json'])
assert len(plan['recoveries']) == 34 and len(plan['issues']) == 34
assert not ledger['final_rounds'] and not (P / 'audit/final-freeze.json').exists()
reports = []
text_files, crop_indexes = [], []
for role in ['visual', 'math', 'adversarial']:
    folder = Path(f'proposals/ra12_{role}/granular-update')
    report = read(P / folder / 'second-pass-report.json')
    assert report['reviewer_id'] == report['session_id'] == '/root/ra12_' + role
    assert report['document_hashes_start'] == before == report['document_hashes_end']
    assert report['findings']
    for key, field in [('source_unit_ids', 'source_units'), ('target_unit_ids', 'target_units'), ('recovery_ids', 'recoveries'), ('issue_ids', 'issues')]:
        assert set(report['reviewed_scope'][key]) == {x['id'] for x in ledger[field]}
    reports.append({'reviewer_id': report['reviewer_id'], 'path': str(folder / 'second-pass-report.json'), 'sha256': sha(P / folder / 'second-pass-report.json'), 'findings': report['findings']})
    text_files += [str(x.relative_to(P)) for x in sorted((P / folder).glob('*')) if x.suffix in ['.json', '.md']]
    crop_indexes.append(str(folder / 'crop-index.json'))
assert (P / 'proposals/ra12_math/granular-update/role-clarification.md').is_file()

archive = P / 'history/second-pass-a71365ac-54e496a6'
archive.mkdir(parents=True, exist_ok=False)
for name in ['content-plan.json', 'authored-content.json', 'ledger.json', 'source-transcript.md', 'study-notes.md', 'source-target-map.json']:
    shutil.copy2(P / name, archive / name)
shutil.copy2(P / 'audit/granular-followup/body-and-source-overrides.json', archive / 'body-and-source-overrides.json')
write(archive / 'actual-review-reports.json', {'document_hashes': before, 'reports': reports, 'accepted_as_pass_2': False})

evidence = catalog(P, {'text_files': text_files + ['audit/granular-followup/boss-name-check.md'], 'crop_indexes': crop_indexes})
existing = {x['path']: x['id'] for x in plan['evidence_artifacts']}
for item in evidence['evidence_artifacts']:
    assert item['path'] not in existing
    record = dict(item)
    record.pop('sha256', None)
    plan['evidence_artifacts'].append(record)
    existing[item['path']] = item['id']

def eid(path):
    return 'artifact:' + existing[path]

def sid(page, unit):
    return f'RA12-P{page:03d}-U{unit:02d}'

def native(page, unit):
    return eid(f'audit/granular-reread-7f2b9670fcd1/RA12-P{page:03d}-U{unit:02d}-800.png')

def block(kind, n):
    return plan['transcription_blocks' if kind == 'T' else 'study_blocks'][n - 1]

def append(kind, n, text):
    b = block(kind, n)
    assert b['origin'] == 'supplement'
    b['text'] += '\n>\n> ' + text.replace('\n', '\n> ')

def replace(kind, n, old, new):
    b = block(kind, n)
    assert old in b['text'], (kind, n, old)
    b['text'] = b['text'].replace(old, new)

def link(kind, n, ids):
    b = block(kind, n)
    b['evidence_ids'] = sorted(set(b.get('evidence_ids', []) + ids))

littlewood = '标题英文统一排 Littlewood。原 i 与 e 之间只分辨两条较高纵笔及相应短横，未另见独立第三条 l 竖，近 Littewood；也可解释为第二 t 与 l 压缩共笔。此处只披露可见笔数与连并候选，不断言作者写错了哪一字母；三原则的内容确定所指姓名，不能证明每个标准字母均已分别写出。'
egorov = '本页页首姓名原形近 Egrov：g 后直接接 r，下一圆环在 r 与 v 之间，g/r 间未分出独立 o。仍保留极紧连写的候选，按一致收敛工具的指称采用通行 Egorov；这一处不同于第 3 页已经登记的 Englov／Engrov 近形。'
topology_names = '两位姓名采用通行的 Tietze、Urysohn。前者首个 e 位置呈 c 样开口，与同词末 e 的闭眼不同，第五位 z／7 样笔上另有点；近 Tictze 只是低至中置信的分字候选，也可作普通 e、z 草写，不强判拼写错误。后者在 s 后见回环接高升笔、独立 e 样小环及末 n，近 Urysden／Urysoden／Urysolen；也保留 o/h 特殊连笔的解释，具体字母分配不唯一。闭集连续延拓与不交闭集的端点分离分别确定两定理的指称，不能据此把规范拼法说成逐笔唯一。'
append('T', 4, littlewood)
append('S', 5, littlewood)
append('T', 29, egorov)
append('S', 29, '第 4 页页首原名近 Egrov，g 与 r 间没有单独 o，保留压缩连写候选；本节按工具指称统一称 Egorov。第 3 页的 Englov／Engrov 近形已另记，不能替代这一位置的说明。')
append('T', 34, topology_names)
append('S', 37, topology_names)
replace('T', 33, '则存在连续函数', '则 $\\exists$ 连续函数')
append('T', 34, r'第 (3) 条“则”与“连续函数”之间原有独立的 $\exists$ 符号，保真按原位保留；中文“存在”是可用的数学译写，不是该位的两个原字。')
append('S', 37, r'第 (3) 条的量词在纸面是独立 $\exists$，保真稿保留符号；本节的连续分离表述按其存在量化理解。')
replace('S', 23, r'和 $\sum_i m(E\setminus F_{i,\delta})$。', r'和 $\sum m(E\setminus F_{i,\delta})$。')
append('S', 23, r'原求和号下方没有另写索引，上面的原式引述保留裸 $\sum$。正确公式中的下标 $i$ 来自前面有限值层的编号，属于规范写法；它不能反证原纸上已经有这个下标。')

labels = {
    sid(1, 1): 'Littlewood三原则标题（英文按通行名）。原i/e间两条高竖，近Littewood，第二t/l共笔为备选，未能独立分出第三竖；不强断拼错。3与定律在原位，末字择优律。',
    sid(4, 1): '〔校读：用〕Egrov（近形，规范名Egorov），∃Gδ⊂E。g/r间无独立o，紧连写为备选；用/同依据同手内轴下探择优用。',
    sid(5, 7): '括注姓名规范Tietze；首e位置为开口c样弧，末e有闭眼，第五位z/7样笔上有点。近Tictze与普通草写均留作解释，不断言唯一拼错。',
    sid(5, 10): '原两式f|A=0、f|B=1，中间有形近B的独写连接符；且为依据合取语境的限定校读，非无疑直读。',
    sid(5, 11): '括注姓名规范Urysohn；s后回环接高升笔、e样小环及n，近Urysden/Urysoden/Urysolen，o/h特殊连笔亦可，逐字分配有限置信。',
    sid(5, 19): r'$\varphi_k\xrightarrow{\mathrm{a.e.}}f$。这是本页原墨；下一物理页的证明标题单独定位在P006-U01，不在此框内伪引其箭形。',
}
for source in plan['sources']:
    if source['id'] in labels:
        source['label'] = labels[source['id']]

name_evidence = {
    'littlewood': [native(1, 1), eid('proposals/ra12_math/granular-update/crops/p1-littlewood-letters-1200.png')],
    'egorov': [native(4, 1), native(3, 9), native(3, 16), eid('proposals/ra12_math/granular-update/crops/p4-egorov-letters-1200.png'), eid('proposals/ra12_visual/granular-update/crops/p4-egrov-name-1200.png'), eid('proposals/ra12_adversarial/granular-update/p4-egrov-name-1200.png')],
    'tietze': [native(5, 7), eid('proposals/ra12_math/granular-update/crops/p5-tietze-letters-1200.png'), eid('proposals/ra12_visual/granular-update/crops/p5-tietze-name-1200.png'), eid('proposals/ra12_adversarial/granular-update/p5-tietze-name-1200.png')],
    'urysohn': [native(5, 11), native(5, 7), eid('proposals/ra12_math/granular-update/crops/p5-urysohn-letters-1200.png'), eid('proposals/ra12_visual/granular-update/crops/p5-urysohn-name-1200.png'), eid('proposals/ra12_adversarial/granular-update/p5-urysohn-name-1200.png')],
}
for kind, n in [('T',4),('S',5)]: link(kind,n,name_evidence['littlewood'])
for kind, n in [('T',29),('S',29)]: link(kind,n,name_evidence['egorov'])
for kind, n in [('T',34),('S',37)]: link(kind,n,name_evidence['tietze']+name_evidence['urysohn'])
comparison_ids = [eid(path) for path in [
    'proposals/ra12_adversarial/final-7f2b9670fcd1/p3-qie-comparison-1200.png',
    'proposals/ra12_visual/crops/p0003-second-qie-known-1200.png',
    'proposals/ra12_visual/crops/p0005-second-urysohn-standalone-1200.png',
    'proposals/ra12_visual/crops/p0005-second-urysohn-ab-known-1200.png',
]]
link('T',34,comparison_ids)
p7 = next(p for p in manifest['pages'] if p['id']=='p0007')
blank_ids = ['image:p0007'] + ['image:' + r['id'] for r in p7['regions']]
link('T',44,blank_ids)
link('S',52,['image:p0007'])
sum_evidence = [native(2,15), eid('proposals/ra12_visual/granular-update/crops/p2-raw-sum-index-1200.png')]
exists_evidence = [native(5,9), eid('proposals/ra12_visual/granular-update/crops/p5-urysohn-exists-1200.png')]
link('S',23,sum_evidence)
link('T',33,exists_evidence)
link('T',34,exists_evidence)
link('S',37,exists_evidence)

common = [eid(r['path']) for r in reports]
common += [eid(f'proposals/ra12_{role}/granular-update/second-pass-report.md') for role in ['visual','math','adversarial']]
common += [eid('proposals/ra12_math/granular-update/role-clarification.md')]
decisions = []
def decision(number, source_ids, problem, candidates, observation, forward, backward, direct_evidence, targets=()):
    decisions.append({'number': number, 'source_ids': source_ids, 'problem': problem, 'candidates': candidates, 'observation': observation, 'forward': forward, 'backward': backward, 'direct_evidence_ids': direct_evidence, 'target_ids': list(targets)})

decision(35, [sid(5,10),sid(5,19),sid(6,1)], '源标签中的限定读法与跨页箭形不同步，T034字形比较及P7空白陈述缺直接图证',
 ['P5U10注明B样独写、且为限定校读；P5U19只描述本框a.e.趋向，将下一页箭头留给P6U01；T034连真实P3且与P5对照图；T044连P7整页六区、S052连P7整页，不制造空白内容单元。', '保持无标记且、双杆原引语及不带原图的空白说明，认为数学等价或某处已有图证即足够；不能追溯这些目标的实际字形主张。', '给空白页造一个正文来源或把P3比较字当作P5正文内容来源；混淆真实原墨与辅助图证，拒绝。'],
 '三人本轮全量复核；P5U19本框只有a.e.箭头，不含下一页题头。P6原单杆、P5独写B样与P3且图均已实际重看。P7由三人各自重看整页和六区均白。此项source_ids只列非空白原句，P7作为独立页图区证据登记。',
 '由每个目标的明确字形比较或空白断言回到对应真实影像，按原像/规范表达分层改标签。P5两端值逻辑保持合取，P6保持(1)到(3)；空白页保留零内容单元。',
 '反查每条新增图证的实际位置与声明相合；不把逻辑等价当原笔数相同，不把字形比较误加为内容边。空白无原正文，故伪造一个空白内容源反而违反来源语义。',
 comparison_ids+blank_ids+[native(5,10),native(5,19),native(6,1)],
 ['RA12-TRANSCRIPTION-034','RA12-TRANSCRIPTION-044','RA12-STUDY-052'])
decision(36, [sid(1,1)], 'Littlewood规范姓名未披露两条高竖及t/l连并的实际笔形',
 ['保留通行Littlewood；局部蓝注记录i/e间两条高竖、近Littewood及t/l共笔候选，不强判拼错字母。', '标准Littlewood每个t和l均有独立竖可清楚分开；原矢量及1200图未见第三独立竖。', '原为Littlewood而第二t与l压缩共笔；作为真实可行字形备选保留，视觉员认为正常草写可解释。'],
 '数学员独立1200和原seq4–7分出两竖与两横，后接e及wood；Boss800同见两根高竖。视觉员未强判该处异写，故只作有限置信的原形披露。',
 '标题下三条分别关于可测集合、可测函数、收敛列，确定Littlewood三原则的指称；规范名有据，所见笔数独立描述。',
 '三原则内容不能区分漏l、t/l共笔或其他紧连写；未见独立第三竖不等于能证明作者主观拼错，正文因此不作该断言。', name_evidence['littlewood'])
decision(37, [sid(4,1)], 'P4页首Egrov近形不能由P3 Englov/Engrov说明替代',
 ['本位置原形近Egrov，g后紧r、圆环在r/v间，规范名Egorov；保留极紧连写o的候选。', '原有完整独立Egorov六字母，g/r间另有单独o；高倍图及原路径未见该圆环。'],
 '三人各自新1200直渲均支持g/r间没有独立o，P3另有n样开笔，两个位置分开登记。',
 '此处选小坏集并在余集上一致收敛，后续Gδ用途确定调用Egorov；规范名与证明对象一致。',
 '定理用途能确定姓名但不能产生未见的o；用P3不同近形说明概括P4会丢失本处实际字母计数。', name_evidence['egorov'])
decision(38, [sid(5,7)], 'Tietze首e开口及第五位点迹的有限置信披露',
 ['仍用Tietze，说明首e位置c样开口、末e闭眼及z/7样上独点；近Tictze与普通草写两解均存，不断言实际拼错。', '把原形唯一判成Tictze或另一姓名；草写e开口及z的简写同样可解释，语境也指向延拓定理。', '声称所有字母均与标准印刷形逐笔相同；实际首末e形和额外点迹有区别。'],
 '数学员1200确认开口及点迹，视觉员1200认为仍可作正常草写，另有对抗员同页末e对照。Boss保留两种判断空间，描述笔形而不伪造一致的错拼结论。',
 '闭子集上的连续实函数向全正规空间延拓明确所指Tietze，命题及学习证明保持不变。',
 '普通手写e可开口，z可简化，故单凭形异不推出拼错；数学命题也不证明原字都有印刷体笔画。', name_evidence['tietze'])
decision(39, [sid(5,11)], 'Urysohn旁签末部连写和独立e样环尚未就地登记',
 ['规范Urysohn，描述s后回环接高升笔、e样小环及n；近Urysden/Urysoden/Urysolen与o/h连笔均保留，具体字母分配有限置信。', '原标准Urysohn可毫无歧义逐字直读；独立小环与高升笔的分配存在真实分歧。', '必须改用近形拼串作为另一位作者；不交闭集的连续端点分离已确定所指Urysohn。'],
 '三人各自1200看同一签名，视觉近Urysden、对抗近Urysoden、数学近Urysolen；同页Tietze末e提供闭眼对照。正文保留共同可见笔形和不同分字，不强排唯一拼串。',
 '闭A/B不交、连续f取0/1是该分离定理的内容，标准姓名正确；笔形描述不改变f的对象与方向。',
 '若把e样环并入h也可能形成特殊连写，数学不能排除；因此不把某一近形宣布成唯一原字，也不凭拼串改换定理。', name_evidence['urysohn'])
decision(40, [sid(2,15)], '学习稿原式引述把原裸求和号排成Σ_i',
 ['S023原稿引述保留裸Σ；正确公式的i明确是根据有限值层作规范绑定。', '原Σ下已经写i；800及新1200图的下方白底反对，顶小横属于Σ本体。'],
 '视觉员800整单元与1200定向实见Σ下空白；T016早已按裸Σ排印，仅S023的原稿引述需同步。',
 '和式语义遍历前文值层i，学习正确计算用Σ_i无误；原式与规范推导分别表达。',
 '求和需要一个语义索引并不能说明纸面已写下标，不能把正确数学绑定反投为原笔迹。', sum_evidence)
decision(41, [sid(5,9)], 'Urysohn条件中原独立存在量词被无说明译为两个汉字',
 ['T033在则与连续函数间保留∃；学习稿可用存在语义，蓝注说明原符号。', '原纸面已写汉字存在，或∃只是相邻字的收笔；反E样的首末横及中短横独立成形。'],
 '视觉1200及Boss800见则后的独立反E样，当前U09标签原已记录∃，现使正文与来源一致。',
 '∃量化分离函数，定义域X、目标[0,1)原笔形及两端值条件保持；学习规范目标[0,1]另有证明。',
 '中文存在与∃数学同义却不是同一原字形；该位一枚独立符号不能直接读成两个汉字。', exists_evidence)

decision_file = Path('audit/second-pass-followup/recovery-decisions.json')
write(P / decision_file, {'note_id':'RA12','boss':'BossNotes-2ff3215d6446','before_document_hashes':before,'actual_reports':reports,'decisions':decisions,'latest_second_pass_pending':True,'nonfinding':'P4U17有一个的个左侧短提在视觉1200图实见；Boss重开同图确认，保留当前有一个，不把800初看遗漏该短提变成修改。'})
for relative in [decision_file,Path('audit/second-pass-followup/merge_findings.py')]:
    ident='second-followup-'+relative.stem
    plan['evidence_artifacts'].append({'id':ident,'path':str(relative),'kind':'evidence','format':'text'})
    existing[str(relative)]=ident
synthesis=eid(str(decision_file))
for d in decisions:
    evidence_ids=sorted(set(common+[synthesis]+d['direct_evidence_ids']))
    rid=f'RA12-REC-{d["number"]:02d}'
    plan['recoveries'].append({'id':rid,'source_ids':d['source_ids'],'problem':d['problem'],
        'candidates':[{'id':f'candidate-{i}','text':c,'evidence_ids':evidence_ids} for i,c in enumerate(d['candidates'],1)],
        'selected_candidate_id':'candidate-1','status':'unresolved','evidence_ids':evidence_ids,
        'forward_validation':{'status':'pass','method':'从原像与所指对象作正向恢复','inputs':d['observation'],'result':d['forward'],'evidence_ids':evidence_ids},
        'backward_validation':{'status':'pass','method':'竞争读法与规范化边界反向检验','inputs':d['candidates'][0],'result':d['backward'],'evidence_ids':evidence_ids},
        'return_to_image':{'observation':d['observation'],'evidence_ids':evidence_ids},
        'reviewer_id':'BossNotes-2ff3215d6446','session_id':'BossNotes-2ff3215d6446'})
    plan['issues'].append({'id':f'RA12-ISSUE-{d["number"]:02d}','status':'open','description':d['problem']+'；基于三份真实完整二遍的Boss合并提议，等待当前新版本独立接受。','related_ids':d['source_ids']+d['target_ids']+[rid],'evidence_ids':evidence_ids,'resolution':''})
for old, newer in [(4,[36]),(5,[40]),(8,[37]),(10,[35,38,39,41]),(21,[35]),(27,[36,37,38,39]),(32,[35])]:
    plan['recoveries'][old-1]['problem']+='；本轮补核另见'+'、'.join(f'RA12-REC-{x:02d}' for x in newer)+'。'
    plan['issues'][old-1]['related_ids']=list(dict.fromkeys(plan['issues'][old-1]['related_ids']+[f'RA12-REC-{x:02d}' for x in newer]))
assert not any(o['pass']==2 for o in plan['observations'])
for rec in plan['recoveries']:rec['status']='unresolved'
for issue in plan['issues']:issue['status'],issue['resolution']='open',''

# Refresh the declared reproducible body/source overrides, retaining stable IDs.
override=read(P/'audit/granular-followup/body-and-source-overrides.json')
for source in plan['sources']:
    override['source_updates'][source['id']]={k:source[k] for k in ['label','bbox_px']}
for name,key in [('TRANSCRIPTION','transcription_blocks'),('STUDY','study_blocks')]:
    for index,b in enumerate(plan[key],1):
        override['block_updates'][f'RA12-{name}-{index:03d}']={k:b[k] for k in ['text','source_ids','evidence_ids','explanation','origin'] if k in b}
write(P/'audit/granular-followup/body-and-source-overrides.json',override)
authored=read(P/'authored-content.json')
for key in ['sources','transcription_blocks','study_blocks']:authored[key]=copy.deepcopy(plan[key])
write(P/'authored-content.json',authored)
write(P/'content-plan.json',plan)
result=build(P)
after={name:sha(P/name) for name in before}
write(P/'audit/second-pass-followup/change-summary.json',{'before_document_hashes':before,'after_document_hashes':after,'actual_reports':reports,'recovery_count_before':34,'recovery_count_after':41,'issue_count_before':34,'issue_count_after':41,'final_rounds':0,'latest_second_pass_pending':True})
print(json.dumps({**result,'document_hashes':after,'actual_reports_retained':len(reports)},ensure_ascii=False))
