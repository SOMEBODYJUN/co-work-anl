import json, sys, hashlib
from pathlib import Path
from datetime import datetime, timezone

O=Path(__file__).resolve().parent
P=O.parents[1]
d=json.loads((O/'revision-tasks.json').read_text())
ledger=json.loads((P/'ledger.json').read_text())
source={u['id']:u for u in ledger['source_units']}
payload=json.load(sys.stdin)
assert payload['page_id'] not in [p['page_id'] for p in d['page_comparisons']]
for row in payload['rows']:
    assert row['blind_id'] not in d['blind_units_compared']
    for s in row['source_ids']: assert s in source
    row['target_ids']=sorted({t for s in row['source_ids'] for t in source[s]['transcription_target_ids']+source[s]['study_target_ids']})
    d['blind_units_compared'].append(row['blind_id'])
payload['saved_at']=datetime.now(timezone.utc).isoformat()
d['page_comparisons'].append(payload)
d['tasks'].extend(payload.get('tasks',[]))
d['mathematical_verifications'].extend(payload.get('mathematical_verifications',[]))
for p in payload.get('reopened_images',[]):
    d['reopened_images'].append({'path':p,'page_id':payload['page_id'],'sha256':hashlib.sha256((P/p).read_bytes()).hexdigest(),'reason':payload.get('reopen_reason','针对稿件差异回图复核'),'tool':'tools.view_image; image(...)'})
(O/'revision-tasks.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
lines=['## '+payload['page_id']+' 比对','',payload['summary'],'','| 盲读单元 | 来源单元 | 比对判断 |','|---|---|---|']
for r in payload['rows']:
    desc=(r['verdict']+'：'+r['note']).replace('|','\\|').replace('\n',' ')
    lines.append('| '+r['blind_id']+' | '+', '.join(r['source_ids'])+' | '+desc+' |')
lines+=['','相关目标逐项已在 `revision-tasks.json` 中登记。','']
if payload.get('ledger_extra_units'):
    lines+=['### 清单分组差异或额外原稿对象','']
    for x in payload['ledger_extra_units']:lines.append('- '+x)
    lines.append('')
for t in payload.get('tasks',[]):
    lines+=['### '+t['id']+' · '+t['priority']+' · '+t['title'],'','- 来源：'+', '.join(t['source_ids'])+'；目标：'+', '.join(t['target_ids'])+'。','- 位置 bbox：`'+str(t['bbox_px'])+'`。','- 实际字形／内容：'+t['actual'],'- 当前问题：'+t['problem'],'- 建议正文／处理：'+t['suggestion'],'']
for v in payload.get('mathematical_verifications',[]):
    lines+=['### 数学检查 '+v['id'],'',v['result'],'']
with (O/'comparison-report.md').open('a') as f:f.write('\n'.join(lines)+'\n')
print(json.dumps({'page_saved':payload['page_id'],'blind_units_compared':len(d['blind_units_compared']),'tasks':len(d['tasks']),'math_checks':len(d['mathematical_verifications'])},ensure_ascii=False))
