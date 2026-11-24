from pathlib import Path
import json, hashlib, re

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
IDENTITY = '/root/ra07_rebuild'

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def overlap(a, b):
    return max(a[0],b[0]) < min(a[2],b[2]) and max(a[1],b[1]) < min(a[3],b[3])

def build():
    manifest=json.loads((PROJECT/'manifest.json').read_text())
    pages=[json.loads(p.read_text()) for p in sorted((HERE/'pages').glob('p*.json'))]
    study_plan=json.loads((HERE/'study-order.json').read_text()) if (HERE/'study-order.json').exists() else None
    policy=HERE/'editorial-policy.md'
    policy.write_text('RA07 作者首遍。原稿内容保留原式、重复和未完路线；蓝色 info 块是编者补充/补证/纠错；红字仅标原稿明确待填。正文 unit 标记与手工像素框逐一对应。无旧稿。作者和实际会话均为 /root/ra07_rebuild。此文件只说明编辑规则，不证明视觉与数学正确。\n',encoding='utf-8')
    sources=[]; targets=[]; pchecks=[]; rchecks=[]; recoveries=[]; issues=[]
    toc='\n'.join(f'{i+1}. [{p["title"]}](#{p["anchor"]})' for i,p in enumerate(study_plan or pages))
    front={
      'T': '# 实分析 7：原序保真转写\n\n原件：实分析7.pdf，共 13 物理页。按原稿页序保留公式、旁注、问题、重复及原错误。中性编号标识尚不能唯一恢复的字迹；数学补充不冒充原文。当前为作者首遍提议稿。',
      'N': '# 实分析 7：测度与 Lebesgue 外测度\n\n## 阅读约定\n\n普通正文保留原稿内容与原有路线。蓝色 `info` 块按“补充”“补证”“纠错”说明新增内容；红色只标原稿明确未答位置。中性疑字编号见独立疑点表。\n\n## 目录\n\n'+toc
    }
    blocks={'T':[('T-INTRO',front['T'],[], 'editorial','说明原序转写的编辑约定。','resolved')], 'N':[('N-INTRO',front['N'],[], 'editorial','编排阅读说明和完整目录，不冒充原稿标题。','resolved')]}
    for p in pages:
        n=p['page']; pid=f'p{n:04d}'; mp=manifest['pages'][n-1]
        if not p.get('blank'):
            blocks['T'].append((f'T-P{n:03d}-HEAD',f'## 物理第 {n} 页\n',[],'editorial',f'为物理第 {n} 页新增页序定位标题。','resolved'))
            blocks['N'].append((f'N-P{n:03d}-HEAD',f'<a id="{p["anchor"]}"></a>\n\n## {p["title"]}\n',[],'editorial','为复习编排新增知识单元标题。','resolved'))
        for i,u in enumerate(p['units'],1):
            sid=f'RA07-P{n:03d}-U{i:03d}'; tid=f'T-P{n:03d}-{i:03d}'; nid=f'N-P{n:03d}-{i:03d}'
            regs=[r['id'] for r in mp['regions'] if overlap(u['bbox'],r['bbox_px'])]
            ev=['image:'+pid]+['image:'+r for r in regs]+u.get('extra_evidence',[])
            status=u.get('status','resolved')
            sources.append({'id':sid,'page_id':pid,'region_ids':regs,'bbox_px':u['bbox'],'label':u['label'],'status':status,'transcription_target_ids':[tid],'study_target_ids':[nid],'evidence_ids':ev})
            blocks['T'].append((tid,u['transcript'],[sid],'source',f'物理第{n}页“{u["label"]}”原序转写；识读状态见来源清单。',status))
            blocks['N'].append((nid,u.get('study',u['transcript']),[sid],'source',f'保留原稿“{u["label"]}”，按复习依赖重新定位；新增数学内容另列蓝色单元。',status))
            for j,s in enumerate(u.get('supplements',[]),1):
                xid=f'N-P{n:03d}-{i:03d}-S{j}'
                blocks['N'].append((xid,s,[sid],'supplement',s.splitlines()[0].replace('> [!info] ','')+'；为编者新增内容，不冒充原稿字迹；来源若未决则保守继承其未决状态。',status))
                sources[-1]['study_target_ids'].append(xid)
        page_sources=[s for s in sources if s['page_id']==pid]
        common={'pass':1,'reviewer_id':IDENTITY,'session_id':IDENTITY,'assessment':'blank' if p.get('blank') else 'content'}
        pchecks.append({'id':'first-'+pid,'page_id':pid,**common,'source_unit_ids':[s['id'] for s in page_sources],'cross_region_unit_ids':[s['id'] for s in page_sources if len(s['region_ids'])>1],'evidence_ids':['image:'+pid],'observation':p['observation'],'layout_observation':p['layout']})
        for r,obs in zip(mp['regions'],p['regions']):
            sids=[s['id'] for s in page_sources if r['id'] in s['region_ids']]
            rchecks.append({'id':'first-'+r['id'],'region_id':r['id'],**common,'assessment':'content' if sids else 'blank','source_unit_ids':sids,'evidence_ids':['image:'+r['id']],'observation':obs})
        issues.extend(p.get('issues',[])); recoveries.extend(p.get('recoveries',[]))
    if study_plan:
        original=blocks['N']
        ordered=[original[0]]
        used={'N-INTRO'}
        for group in study_plan:
            ordered.append((group['id'],f'<a id="{group["anchor"]}"></a>\n\n## {group["title"]}',[],'editorial','按定义、先备工具、证明与应用的依赖关系编排复习章节。','resolved'))
            for base in group['items']:
                matches=[b for b in original if b[0]==base or b[0].startswith(base+'-S')]
                if not matches: raise ValueError('Missing study unit '+base)
                for block in matches:
                    if block[0] in used: raise ValueError('Duplicated study unit '+block[0])
                    used.add(block[0]);ordered.append(block)
        omitted=[b[0] for b in original if b[0] not in used and not b[0].endswith('-HEAD')]
        if omitted: raise ValueError('Study order omitted '+repr(omitted))
        blocks['N']=ordered
    if (HERE/'recoveries.json').exists():
        recoveries.extend(json.loads((HERE/'recoveries.json').read_text()))
    artifacts=[]
    lookup={s['id']:s for s in sources}
    for typ,name,kind in [('T','source-transcript.md','transcription'),('N','study-notes.md','study')]:
        lines=[]
        for block_index,(uid,body,sids,origin,explanation,status) in enumerate(blocks[typ]):
            start=len(lines)+1
            lines.extend([f'<!-- unit: {uid} -->']+[line.rstrip() for line in body.strip().splitlines()]+([''] if block_index+1<len(blocks[typ]) else []))
            end=len(lines)
            ev=['artifact:editorial-policy'] if not sids else sorted(set(e for sid in sids for e in lookup[sid]['evidence_ids']))
            targets.append({'id':uid,'artifact_id':kind,'start_line':start,'end_line':end,'text_sha256':hashlib.sha256('\n'.join(lines[start-1:end]).encode()).hexdigest(),'source_ids':sids,'status':status,'origin':origin,'old_ids':[],'evidence_ids':ev,'explanation':explanation})
        path=HERE/name
        temporary=path.with_suffix(path.suffix+'.tmp')
        temporary.write_text('\n'.join(lines).rstrip()+'\n',encoding='utf-8')
        temporary.replace(path)
        artifacts.append({'id':kind,'path':str(path.relative_to(PROJECT)),'sha256':sha(path),'kind':kind,'format':'text'})
    artifacts.append({'id':'editorial-policy','path':str(policy.relative_to(PROJECT)),'sha256':sha(policy),'kind':'evidence','format':'text'})
    cropfile=HERE/'crops.json'
    if cropfile.exists():
        for c in json.loads(cropfile.read_text()):
            artifacts.append({'id':c['id'],'path':c['path'],'sha256':sha(PROJECT/c['path']),'kind':'evidence','format':'image','source_crop':{'page_id':c['page_id'],'bbox_px':c['bbox_px']}})
    extra_evidence=HERE/'extra-evidence.json'
    if extra_evidence.exists():
        for a in json.loads(extra_evidence.read_text()):
            artifacts.append({**a,'sha256':sha(PROJECT/a['path'])})
    ledger={'schema_version':'1.0','manifest_sha256':sha(PROJECT/'manifest.json'),'authors':[IDENTITY,'/root'],'artifacts':artifacts,'source_units':sources,'target_units':targets,'old_units':[],'region_checks':rchecks,'recoveries':recoveries,'issues':issues,'final_rounds':[],'page_checks':pchecks}
    (PROJECT/'ledger.json').write_text(json.dumps(ledger,ensure_ascii=False,indent=2)+'\n')
    (HERE/'source-units.json').write_text(json.dumps(sources,ensure_ascii=False,indent=2)+'\n')
    (HERE/'mapping.json').write_text(json.dumps({'source_to_targets':[{k:s[k] for k in ['id','transcription_target_ids','study_target_ids']} for s in sources],'target_units':targets},ensure_ascii=False,indent=2)+'\n')
    (HERE/'observations-first.json').write_text(json.dumps({'reviewer_id':IDENTITY,'session_id':IDENTITY,'tool':'functions.exec -> tools.view_image','page_checks':pchecks,'region_checks':rchecks},ensure_ascii=False,indent=2)+'\n')
    print(f'Saved {len(pages)} pages, {len(sources)} source units, {len(targets)} target units.')

if __name__=='__main__': build()
