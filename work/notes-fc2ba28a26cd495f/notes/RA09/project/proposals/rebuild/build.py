"""Assemble manually observed, authored page units; never creates observation claims."""
import json, hashlib, re
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent.parent
ACTOR = '/root/ra09_rebuild'
def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def atomic_text(path, value):
    clean='\n'.join(line.rstrip() for line in value.splitlines()).rstrip()+'\n'
    tmp=path.with_name(path.name+'.tmp')
    tmp.write_text(clean)
    tmp.replace(path)
def save(path, obj): atomic_text(path, json.dumps(obj, ensure_ascii=False, indent=2))
def intersects(a,b): return a[0]<b[2] and b[0]<a[2] and a[1]<b[3] and b[1]<a[3]

manifest = json.loads((PROJECT/'manifest.json').read_text())
pages = {p['id']:p for p in manifest['pages']}
data = [json.loads(p.read_text()) for p in sorted((HERE/'page-data').glob('p*.json'))]
sources=[]; targets=[]; page_checks=[]; region_checks=[]; recoveries=[]; issues=[]; crops=[]
docs={'T':[], 'N':[]}
for d in data:
    page=pages[d['page_id']]
    for u in d['source_units']:
        u=dict(u); u['page_id']=page['id']
        u['region_ids']=[r['id'] for r in page['regions'] if intersects(u['bbox_px'],r['bbox_px'])]
        u['evidence_ids']=['image:'+page['id']]+['image:'+x for x in u['region_ids']]+u.pop('extra_evidence_ids',[])
        u['status']=u.get('status','resolved')
        u['transcription_target_ids']=[];u['study_target_ids']=[]
        sources.append(u)
    for t in d['target_units']:
        docs[t['id'][0]].append(t)
    for crop in d.get('crops',[]): crops.append(crop)
    for rec in d.get('recoveries',[]): recoveries.append(rec)
    for issue in d.get('issues',[]): issues.append(issue)
    pids=[u['id'] for u in sources if u['page_id']==page['id']]
    page_checks.append({'id':'P1-'+page['id'],'page_id':page['id'],'pass':1,'reviewer_id':ACTOR,'session_id':ACTOR,'assessment':d.get('assessment','content'),'source_unit_ids':pids,'evidence_ids':['image:'+page['id']],'observation':d['page_observation'],'cross_region_unit_ids':[u['id'] for u in sources if u['page_id']==page['id'] and len(u['region_ids'])>1],'layout_observation':d['layout_observation']})
    for r,obs in zip(page['regions'],d['region_observations']):
        ids=[u['id'] for u in sources if r['id'] in u['region_ids']]
        region_checks.append({'id':'R1-'+r['id'],'region_id':r['id'],'pass':1,'reviewer_id':ACTOR,'session_id':ACTOR,'assessment':'content' if ids else 'blank','source_unit_ids':ids,'evidence_ids':['image:'+page['id'],'image:'+r['id']],'observation':obs})

source_by_id={u['id']:u for u in sources}
artifacts=[]
for prefix,filename,kind in [('T','source-transcript.md','transcription'),('N','study-notes.md','study')]:
    lines=[]
    for t in docs[prefix]:
        start=len(lines)+1
        block=('<!-- unit: '+t['id']+' -->\n'+t['text'].strip()+'\n').splitlines()
        lines.extend(block);end=len(lines);lines.append('')
        source_ids=t.get('source_ids',[])
        ev=list(t.get('extra_evidence_ids',[]))
        for sid in source_ids:
            u=source_by_id[sid]
            u['transcription_target_ids' if prefix=='T' else 'study_target_ids'].append(t['id'])
            ev += u['evidence_ids']
        if not ev: ev=['artifact:editorial-record']
        targets.append({'id':t['id'],'artifact_id':prefix.lower()+'-body','start_line':start,'end_line':end,'text_sha256':hashlib.sha256('\n'.join(block).encode()).hexdigest(),'source_ids':source_ids,'status':t.get('status','resolved'),'origin':t.get('origin','source'),'old_ids':[],'evidence_ids':list(dict.fromkeys(ev)),'explanation':t.get('explanation','依本轮原图观察，按来源单元整理。')})
    path=HERE/filename;atomic_text(path,'\n'.join(lines))
    artifacts.append({'id':prefix.lower()+'-body','path':str(path.relative_to(PROJECT)),'sha256':digest(path),'kind':kind,'format':'text'})

for crop in crops:
    p=PROJECT/crop['path']
    artifacts.append({'id':crop['id'],'path':crop['path'],'sha256':digest(p),'kind':'evidence','format':'image','source_crop':{'page_id':crop['page_id'],'bbox_px':crop['bbox_px']}})
editorial=HERE/'editorial-record.md'
atomic_text(editorial,'# 编辑记录\n\n作者和会话：'+ACTOR+'。\n\n本轮为 REBUILD 作者首遍。标题、目录、物理页标签和排版说明为编辑新增；蓝色信息块为数学补充、解释或纠错，不冒充原稿字迹。黑色正文来自所列原稿单元。没有旧 Markdown 可供比较。`/root` 仅贡献第 2 页 M001 的一般数学补证，不参与本作者所登记的原图首遍识读。\n\n全部图像观察必须以本轮实际 view_image 调用为准，生成程序仅计算行号、哈希和网格相交关系。首遍记录不代表第二遍或终审已完成。\n')
artifacts.append({'id':'editorial-record','path':str(editorial.relative_to(PROJECT)),'sha256':digest(editorial),'kind':'evidence','format':'text'})
for extra in json.loads((HERE/'extra-artifacts.json').read_text()) if (HERE/'extra-artifacts.json').exists() else []:
    extra=dict(extra);extra['sha256']=digest(PROJECT/extra['path']);artifacts.append(extra)
save(HERE/'source-units.json',sources)
save(HERE/'mapping.json',{'source_to_targets':[{k:u[k] for k in ['id','transcription_target_ids','study_target_ids']} for u in sources],'target_units':targets})
save(HERE/'observations.json',{'reviewer_id':ACTOR,'session_id':ACTOR,'page_checks':page_checks,'region_checks':region_checks})
save(HERE/'recoveries.json',recoveries)
save(HERE/'issues.json',issues)
ledger={'schema_version':'1.0','manifest_sha256':digest(PROJECT/'manifest.json'),'authors':[ACTOR,'/root'],'artifacts':artifacts,'source_units':sources,'target_units':targets,'old_units':[],'region_checks':region_checks,'recoveries':recoveries,'issues':issues,'final_rounds':[],'page_checks':page_checks}
save(PROJECT/'ledger.json',ledger)
print(json.dumps({'pages_saved':len(data),'source_units':len(sources),'target_units':len(targets),'open_issues':sum(i['status']=='open' for i in issues),'transcript_lines':len((HERE/'source-transcript.md').read_text().splitlines()),'study_lines':len((HERE/'study-notes.md').read_text().splitlines())},ensure_ascii=False))
