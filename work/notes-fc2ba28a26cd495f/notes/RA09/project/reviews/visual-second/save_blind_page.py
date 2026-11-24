import json, hashlib, sys
from pathlib import Path
from datetime import datetime, timezone

P = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
M = json.loads((P / 'manifest.json').read_text())
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def stamp(): return datetime.now(timezone.utc).isoformat()
def intersects(a,b): return a[0]<b[2] and b[0]<a[2] and a[1]<b[3] and b[1]<a[3]

payload=json.load(sys.stdin)
page=next(p for p in M['pages'] if p['id']==payload['page_id'])
jpath=OUT/'blind-observations.json'
mpath=OUT/'independent-inventory.md'
if jpath.exists():
    d=json.loads(jpath.read_text())
else:
    d={'note_id':'RA09','run_id':'notes-fc2ba28a26cd495f','role':'VISUAL_SECOND','stage':'1_blind_source_reading','status':'in_progress','reviewer_id':'/root/ra09_visual_second','session_id':'/root/ra09_visual_second','identity_note':'规范任务路径为实际提供的任务标识；底层会话 UUID 未向本读者暴露。此前未参与 RA09。','started_at':stamp(),'source_sha256_start':sha(P/'source.pdf'),'manifest_sha256_start':sha(P/'manifest.json'),'source_sha256_end':None,'manifest_sha256_end':None,'permitted_context':['AGENTS.md','prompts/worker-prompt.md','prompts/coordinator-prompt.md','.agents/skills/math-notes-evidence-audit/SKILL.md','.agents/skills/math-notes-evidence-audit/references/protocol.md','.agents/skills/math-notes-evidence-audit/references/tools.md','.agents/skills/math-notes-evidence-audit/scripts/schema/ledger.schema.json','work/notes-fc2ba28a26cd495f/tools/input-contract.md','manifest.json','source.pdf','input/pdf/实分析9(1).pdf','reviews/source-crop-index.json: id/path/page_id/bbox_px only','pages/ and regions/ images','25 indexed source crops'],'excluded_context_read':[],'actual_image_opens':[],'independent_units':[],'page_checks':[],'region_checks':[],'crop_checks':[],'checkpoints':[]}
    mpath.write_text('# RA09 第二遍：独立原图清单（阶段 1）\n\n- 实际任务标识：`/root/ra09_visual_second`；角色 `VISUAL_SECOND`。\n- 此前未参与本笔记；阶段 1 仅接触任务合同、原 PDF、manifest、页区图及裁图索引的四个允许字段。未读取正文、ledger、作者报告、研究证据、疑点表或其他审阅者结果。\n- 底层会话 UUID 未暴露；使用实际给定规范任务路径标识本读者。\n- 起始源 PDF SHA256：`'+d['source_sha256_start']+'`。\n- 起始 manifest SHA256：`'+d['manifest_sha256_start']+'`。\n- 下列读数来自实际 `tools.view_image` 后以 `image(...)` 显示的图像，无 OCR。bbox 是 2480 × 3509 整页原图像素范围；区域相交关系只作几何登记。\n- 直接可辨、字形候选与数学判断分开记录；普通空白不视为待填。\n\n',encoding='utf-8')
assert not any(x['page_id']==page['id'] for x in d['page_checks']), 'Do not overwrite a saved page'
unit_ids=[]
for i,u in enumerate(payload['units'],1):
    u['id']=page['id']+'-blind-u'+str(i).zfill(3)
    u['page_id']=page['id']
    u['region_ids']=[r['id'] for r in page['regions'] if intersects(u['bbox_px'],r['bbox_px'])]
    u['evidence_ids']=['image:'+page['id']]+['image:'+r for r in u['region_ids']]
    unit_ids.append(u['id'])
    d['independent_units'].append(u)
opened=[{'id':page['id'],'path':page['image']['path'],'kind':'full_page','bbox_px':page['image']['bbox_px']}]+[{'id':r['id'],'path':r['image']['path'],'kind':'region','bbox_px':r['bbox_px']} for r in page['regions']]
for crop in payload.get('crops',[]):
    opened.append({'id':crop['id'],'path':crop['path'],'kind':'source_crop','bbox_px':crop['bbox_px']})
    d['crop_checks'].append(dict(crop,page_id=page['id']))
for x in opened:
    x.update(page_id=page['id'],sha256=sha(P/x['path']),sequence=len(d['actual_image_opens'])+1,tool='tools.view_image; emitted with image(...)')
    d['actual_image_opens'].append(x)
pc={'id':'visual-second-blind-'+page['id'],'page_id':page['id'],'pass':2,'reviewer_id':d['reviewer_id'],'session_id':d['session_id'],'assessment':payload['assessment'],'source_unit_ids':unit_ids,'evidence_ids':['image:'+page['id']]+['image:'+r['id'] for r in page['regions']],'observation':payload['observation'],'cross_region_unit_ids':[u['id'] for u in payload['units'] if len(u['region_ids'])>1],'layout_observation':payload['layout']}
d['page_checks'].append(pc)
assert len(payload['regions'])==6
for r,obs in zip(page['regions'],payload['regions']):
    assert obs['region_id']==r['id']
    d['region_checks'].append({'id':'visual-second-blind-'+r['id'],'region_id':r['id'],'pass':2,'reviewer_id':d['reviewer_id'],'session_id':d['session_id'],'assessment':obs['assessment'],'source_unit_ids':[u['id'] for u in payload['units'] if r['id'] in u['region_ids']],'evidence_ids':['image:'+page['id'],'image:'+r['id']],'observation':obs['observation']})
d['checkpoints'].append({'page_id':page['id'],'saved_at':stamp(),'source_sha256':sha(P/'source.pdf'),'manifest_sha256':sha(P/'manifest.json'),'pages_completed':len(d['page_checks']),'regions_completed':len(d['region_checks']),'crops_completed':len(d['crop_checks'])})
jpath.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
lines=['## '+page['id']+'（物理第 '+str(page['number'])+' 页）','',payload['layout'],'',payload['observation'],'','### 独立内容单元','']
for u in payload['units']:
    lines.extend(['- **'+u['id']+'** · bbox `'+str(u['bbox_px'])+'` · '+u['kind']+' · **'+u['reading_status']+'**\n  '+u['text']+(('\n  字形／限制：'+u['note']) if u.get('note') else '')])
lines.extend(['','### 六区实查',''])
for o in payload['regions']: lines.extend(['- **'+o['region_id']+'**（'+o['assessment']+'）：'+o['observation']])
if payload.get('crops'):
    lines.extend(['','### 本页补充裁图',''])
    for c in payload['crops']:lines.append('- `'+c['id']+'` · `'+c['path']+'` · bbox `'+str(c['bbox_px'])+'`：'+c['observation'])
lines.extend(['','### 实际打开的图像',''])
for o in opened:lines.append('- `'+o['path']+'` · SHA256 `'+o['sha256']+'`。')
lines.extend(['','本页保存时源 PDF SHA256：`'+d['checkpoints'][-1]['source_sha256']+'`；进度 '+str(len(d['page_checks']))+'/12 页，'+str(len(d['region_checks']))+'/72 区，'+str(len(d['crop_checks']))+'/25 裁图。',''])
with mpath.open('a',encoding='utf-8') as f:f.write('\n'.join(lines)+'\n')
print(json.dumps({'saved_page':page['id'],'pages':len(d['page_checks']),'regions':len(d['region_checks']),'crops':len(d['crop_checks']),'units':len(d['independent_units']),'inventory_sha256':sha(mpath),'observations_sha256':sha(jpath)},ensure_ascii=False))
