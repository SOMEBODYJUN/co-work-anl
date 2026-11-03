"""Apply explicit reader classifications after full coverage; preserve needed evidence."""
from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
from urllib.parse import unquote
import curation
import triage

LINK=re.compile(r'(!?\[[^\]\n]*\]\()([^\n)]+)(\))')
ENTRY=re.compile(r'^archives/(?:README\.md|[^/]+/(?:subarchives/[^/]+/)*README\.md)$')

def resolve(source,raw):
    href=raw.strip()
    if href.startswith('<') and '>' in href:href=href[1:href.index('>')]
    if not href or href.startswith('#') or re.match(r'[A-Za-z][A-Za-z0-9+.-]*:',href):return None
    href,_,anchor=href.partition('#');href=unquote(href)
    name=os.path.normpath(str(Path(source).parent/href)).replace(os.sep,'/')
    if name.startswith('../') or name.startswith('/'):return None
    return name,('#'+anchor if anchor else '')

def references(source,text):
    return {x[0] for m in LINK.finditer(text) if (x:=resolve(source,m[2])) is not None}

def rewrite(source,target,text,routes):
    def replace(m):
        found=resolve(source,m[2])
        if found is None:return m[0]
        name,anchor=found;destination=routes.get(name,name)
        if destination is None:
            return re.sub(r'^!?\[|\]\($','',m[1])
        if source==target and destination==name:return m[0]
        relative=os.path.relpath(destination,Path(target).parent).replace(os.sep,'/')
        return m[1]+'<'+relative+anchor+'>)'
    return LINK.sub(replace,text)

def classification_digest(home):
    return hashlib.sha256(b''.join(p.name.encode()+p.read_bytes() for p in sorted((home/'records').glob('*.json')))).hexdigest()

def plan(root,run):
    home,snapshot=triage.load(root,run);report=triage.status(root,run)
    starting_classification=classification_digest(home)
    if report['remaining'] or report['stale_record_bindings']:raise ValueError('Finish material classification before the global cleanup plan')
    originals={r['path']:r for r in snapshot['files']}
    records={json.loads(p.read_text())['path']:json.loads(p.read_text()) for p in (home/'records').glob('*.json')}
    retired={p:r for p,r in records.items() if
             (r['category']=='non-math' and r['route']=='delete') or
             (r['category']=='evidence-only' and r['route'] in {'attach','delete'})}
    sources={}
    for name,row in originals.items():
        p=curation._safe_path(root,name)
        if p.exists():
            data=p.read_bytes()
            if curation.digest(data)!=row['sha256']:raise ValueError('Source changed before cleanup: '+name)
            sources[name]=data.decode('utf-8')
        else:
            action=home/'actions'/f"{row['material_id']}.json"
            if not action.exists() or json.loads(action.read_text()).get('state')!='applied':raise ValueError('Unaccounted missing material: '+name)
    entries={}
    for p in (root/'archives').rglob('README.md'):
        name=p.relative_to(root).as_posix()
        if ENTRY.fullmatch(name):
            curation._safe_path(root,name);entries[name]=p.read_text()
    kept={**{p:t for p,t in sources.items() if p not in retired},**entries}
    refs={p:references(p,text) for p,text in {**sources,**entries}.items()}
    evidence={p for p,r in retired.items() if r['category']=='evidence-only'}
    needed={target for p in kept for target in refs.get(p,set()) if target in evidence}
    frontier=list(needed)
    while frontier:
        for target in refs.get(frontier.pop(),set())&evidence-needed:
            needed.add(target);frontier.append(target)
    routes={}
    actions=[]
    for name,record in sorted(retired.items()):
        original=originals[name]
        target=f'tools/evidence/phase25-material-attachments/{run}/{original["material_id"]}.md' if name in needed else None
        routes[name]=target
        if name not in sources:continue
        if target and curation._safe_path(root,target).exists():raise ValueError('Attachment target already exists')
        actions.append({'path':name,'source_sha256':original['sha256'],'material_id':original['material_id'],
                        'action':'attach-needed-evidence' if target else 'delete-non-mathematical' if record['category']=='non-math' else 'delete-unused-evidence-wrapper',
                        'target':target,'reason':record['math_subject_or_nonmath_reason']})
    patches=[]
    for name,text in kept.items():
        revised=rewrite(name,name,text,routes)
        if revised!=text:patches.append({'path':name,'source_sha256':curation.digest(text.encode()),'new_sha256':curation.digest(revised.encode())})
    if classification_digest(home)!=starting_classification:raise ValueError('Classification changed while planning; retry from one stable decision set')
    result={'version':1,'run_id':run,'snapshot_commit':snapshot['commit'],
            'classification_sha256':starting_classification,'actions':actions,'link_patches':patches,'routes':routes,
            'status':'planned-not-applied','rules':'Only explicitly classified non-math/evidence wrappers; substantive mathematics is retained.'}
    triage.write(home/'cleanup-plan.json',result)
    return {'status':result['status'],'actions':len(actions),'needed_evidence_attachments':len(needed),'link_patches':len(patches)}

def apply(root,run):
    home,snapshot=triage.load(root,run);plan_data=json.loads((home/'cleanup-plan.json').read_text())
    if plan_data['status']!='planned-not-applied' or plan_data['classification_sha256']!=classification_digest(home):
        raise ValueError('Classification changed or cleanup already applied; rebuild and review plan')
    routes=plan_data['routes'];prepared=[]
    for action in plan_data['actions']:
        source=curation._safe_path(root,action['path']);data=source.read_bytes()
        if curation.digest(data)!=action['source_sha256']:raise ValueError('Stale cleanup input: '+action['path'])
        target=action['target']
        if target and curation._safe_path(root,target).exists():raise ValueError('Do not overwrite existing attachment')
        revised=rewrite(action['path'],target,data.decode(),routes) if target else None
        prepared.append((action,source,revised))
    patches=[]
    for patch in plan_data['link_patches']:
        p=curation._safe_path(root,patch['path']);data=p.read_bytes()
        if curation.digest(data)!=patch['source_sha256']:raise ValueError('Stale referring page: '+patch['path'])
        revised=rewrite(patch['path'],patch['path'],data.decode(),routes)
        if curation.digest(revised.encode())!=patch['new_sha256']:raise ValueError('Link rewrite plan differs')
        patches.append((p,revised))
    if classification_digest(home)!=plan_data['classification_sha256']:raise ValueError('Classification changed during validation; no cleanup applied')
    # All source/target/version checks complete before touching any original.
    for action,source,revised in prepared:
        target=action['target']
        if target:
            p=curation._safe_path(root,target);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(revised)
    for p,revised in patches:p.write_text(revised)
    # Record deletion intent in Git explicitly. Some managed Git workspaces
    # hydrate a missing tracked file when `git add <path>` is called; unlink
    # alone must never be mistaken for a committed retirement.
    if prepared:
        removed=subprocess.run(['git','rm','--quiet','--',*[a['path'] for a,_,_ in prepared]],cwd=root,capture_output=True,text=True)
        if removed.returncode:raise ValueError('Git retirement not staged; preserve local changes: '+removed.stderr[:500])
    for action,source,revised in prepared:
        if source.exists():raise ValueError('Retired path still exists after git rm: '+action['path'])
        outcome=dict(action,state='applied',publication='local-only',history_commit=snapshot['commit'])
        if revised is not None:outcome['target_sha256']=curation.digest(revised.encode())
        triage.write(home/'actions'/f"{action['material_id']}.json",outcome)
    triage.write(home/'retired-paths.json',routes)
    plan_data['status']='applied-local-only';triage.write(home/'cleanup-plan.json',plan_data)
    return {'status':'applied-local-only','actions':len(prepared),'link_patches':len(patches),'mathematical_body_edits':'link routing only'}
