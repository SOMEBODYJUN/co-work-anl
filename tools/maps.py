"""Build explained multi-source hypergraphs using vendored upstream records."""
from __future__ import annotations
import argparse, hashlib, json, os, re, tempfile
from pathlib import Path
from vendor.mathagent.model import NodeRecord, HyperEdgeRecord, GraphSnapshot
from vendor.matek.frontmatter import parse_flat_frontmatter

LOGICAL_KINDS={'implies','refutes','specializes','transfers','derived_from','equivalent_to'}
CONTEXT_KINDS={'motivates','cites','sourced_from','implements','checks','corrects','supersedes'}


def scopes(root):
    """Current problem scopes only; comparison snapshots are not graph scopes."""
    from curation import _safe_path
    _safe_path(root,'archives');_safe_path(root,'map')
    pattern = re.compile(r'^archives/[^/]+(?:/subarchives/[^/]+)*$')
    found=[]
    for p in (root/'archives').rglob('map'):
        if p.is_dir() and pattern.fullmatch(p.parent.relative_to(root).as_posix()):
            _safe_path(root,p.relative_to(root).as_posix());found.append(p.parent)
    return [root]+sorted(found)


def edge_paths(root):
    from curation import _safe_path
    found=set()
    for scope in scopes(root):
        edge_dir=scope/'map/edges'
        _safe_path(root,edge_dir.relative_to(root).as_posix())
        for p in edge_dir.glob('*.md'):
            _safe_path(root,p.relative_to(root).as_posix());found.add(p)
    return sorted(found)


def _bindings(values, label):
    if not isinstance(values,list):
        raise ValueError(label+' must be a list of identity:SHA-256 bindings')
    result={}
    for value in values:
        if not isinstance(value,str) or ':' not in value:
            raise ValueError(label+' requires identity:SHA-256')
        name,sha=value.rsplit(':',1)
        if not name or not re.fullmatch(r'[0-9a-f]{64}',sha) or name in result:
            raise ValueError('invalid or duplicate '+label+' binding')
        result[name]=sha
    return result


def review_digest(meta,body):
    """Bind the mathematical relation itself, independently of mechanical pins."""
    ignored={'reviewed_content_sha256','endpoint_hashes','evidence_hashes'}
    payload={'metadata':{k:v for k,v in meta.items() if k not in ignored},'body':body}
    return hashlib.sha256(json.dumps(payload,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()


def input_fingerprint(root):
    """Version the complete admitted region, candidates, relations and source gate."""
    from curation import DEFAULT_MANIFEST, _safe_path, formal_paths
    manifest=_safe_path(root,DEFAULT_MANIFEST)
    if not manifest.is_file():raise ValueError('missing phase-2.5 admission manifest')
    raw=manifest.read_bytes();data=json.loads(raw)
    files={DEFAULT_MANIFEST:_safe_path(root,DEFAULT_MANIFEST)}
    baseline=data.get('baseline','')
    files[baseline]=_safe_path(root,baseline)
    for row in data.get('objects',[]):
        name=row['path'];files[name]=_safe_path(root,name)
    for path in formal_paths(root):files[path.relative_to(root).as_posix()]=path
    for path in edge_paths(root):files[path.relative_to(root).as_posix()]=path
    for name in ('cleanup/sources.json','cleanup/inventory.jsonl','cleanup/local-unpublished.json'):
        path=_safe_path(root,name)
        if path.is_file():files[name]=path
    for path in (root/'cleanup/progress').glob('*.json'):
        name=path.relative_to(root).as_posix();files[name]=_safe_path(root,name)
    sources=root/'cleanup/sources.json'
    if sources.is_file():
        for entry in json.loads(sources.read_text()).get('increments',[]):
            files[entry['path']]=_safe_path(root,entry['path'])
    state={name:hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else 'missing'
           for name,path in sorted(files.items())}
    state[DEFAULT_MANIFEST]=hashlib.sha256(raw).hexdigest()
    return hashlib.sha256(json.dumps(state,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()


def read_records(root, *, structural=False, final=False, include_edges=True):
    from curation import formal_paths, check, DEFAULT_MANIFEST, _safe_path
    nodes, edges = {}, {}
    valid_source_refs = None
    declarations={}
    artifacts={}
    if structural:
        paths=formal_paths(root)
    else:
        manifest_path=_safe_path(root,DEFAULT_MANIFEST)
        if not manifest_path.is_file():
            raise ValueError('missing phase-2.5 admission manifest; no automatic mathematical admission')
        manifest_bytes=manifest_path.read_bytes()
        admission=check(root,final=final)
        if admission['errors']:
            first=admission['errors'][0]
            raise ValueError('phase-2.5 admission invalid: '+first['path']+': '+first['error'])
        declarations={o['object_id']:o for o in admission['admitted']}
        if manifest_path.read_bytes()!=manifest_bytes:
            raise ValueError('admission manifest changed during graph read; retry a consistent snapshot')
        artifacts={o['path']:o for o in json.loads(manifest_bytes)['objects']}
        paths=[root/o['path'] for o in admission['admitted']]
    for path in sorted(set(paths)):
        if path.name == 'README.md':
            continue
        data=path.read_bytes()
        content_sha=hashlib.sha256(data).hexdigest()
        if not structural:
            declaration=artifacts[path.relative_to(root).as_posix()]
            if content_sha!=declaration['sha256']:
                raise ValueError('admitted mathematical bytes changed during graph read: '+str(path))
        meta, body = parse_flat_frontmatter(data.decode('utf-8'))
        for key in ('id','title','kind','status','summary'):
            if not isinstance(meta.get(key),str) or not meta[key].strip():
                raise ValueError(f'{path}: missing {key}')
        if not body.strip():
            raise ValueError(f'{path}: missing mathematical body')
        tag=meta.get('type_tag')
        if not isinstance(tag,str) or not tag or not path.name.endswith('--'+tag+'.md'):
            raise ValueError(f'{path}: filename must end with --type_tag.md')
        nid=meta.pop('id')
        if nid in nodes:
            raise ValueError('duplicate mathematical ID: '+nid)
        kind=meta.pop('kind')
        meta['path']=path.relative_to(root).as_posix()
        meta['content_sha256']=content_sha
        if not structural:
            meta['knowledge_status']=('unresolved-bundle' if declarations[nid]['dependency_scope']=='bundle-pending-split'
                                      else declarations[nid]['status'])
            meta['dependency_scope']=declarations[nid]['dependency_scope']
        nodes[nid]=NodeRecord(nid,kind,meta)
    if not include_edges:
        return nodes,edges
    for path in edge_paths(root):
        meta, body=parse_flat_frontmatter(path.read_text())
        current_review_digest=review_digest(meta,body)
        for key in ('id','kind','explanation','conditions','status','reviewed_by'):
            if not isinstance(meta.get(key),str) or not meta[key].strip():
                raise ValueError(f'{path}: missing explained-edge field {key}')
        for key in ('source_ids','target_ids','evidence'):
            if not isinstance(meta.get(key),list) or not meta[key] or not all(isinstance(x,str) and x for x in meta[key]):
                raise ValueError(f'{path}: nonempty {key} required')
        if not body.strip():
            raise ValueError(f'{path}: missing explanation body')
        eid=meta.pop('id');kind=meta.pop('kind')
        if eid in edges:
            raise ValueError('duplicate edge ID: '+eid)
        source_ids=tuple(meta.pop('source_ids'));target_ids=tuple(meta.pop('target_ids'))
        if any(x not in nodes for x in source_ids+target_ids):
            raise ValueError(f'{path}: unknown mathematical endpoint')
        if meta['status'] not in ('accepted','proposed','rejected'):
            raise ValueError('edge status must be accepted/proposed/rejected')
        if meta['status']=='accepted' and kind not in LOGICAL_KINDS|CONTEXT_KINDS:
            raise ValueError(f'{path}: register the semantics of a new relation kind before accepting it')
        # A declaration of an accepted relation is scoped to these exact
        # endpoint versions, not merely to stable names.
        endpoints=set(source_ids+target_ids)
        if not structural and meta['status']=='accepted':
            if meta.get('reviewed_content_sha256')!=current_review_digest:
                raise ValueError(f'{path}: missing or stale relation-content review binding')
            pinned=_bindings(meta.get('endpoint_hashes'),'endpoint_hashes')
            if set(pinned)!=endpoints:
                raise ValueError(f'{path}: bind every endpoint and no unrelated endpoint')
            for nid in endpoints:
                if kind in LOGICAL_KINDS and declarations[nid]['dependency_scope']!='single-object':
                    raise ValueError(f'{path}: split bundle into independently stated objects before accepting a logical edge')
                if pinned[nid]!=nodes[nid].attributes['content_sha256']:
                    raise ValueError(f'{path}: stale endpoint review; re-review relation, do not infer its conclusion false')
            mode=meta.get('relation_mode','unconditional')
            if mode not in {'unconditional','conditional'}:
                raise ValueError(f'{path}: relation_mode must be unconditional or conditional')
            open_premises=[nid for nid in source_ids if nodes[nid].attributes['knowledge_status'] not in {'proved','definition','finite'}]
            if kind in LOGICAL_KINDS and open_premises and mode!='conditional':
                raise ValueError(f'{path}: unproved or refuted premises require an explicit conditional relation')
            meta['relation_mode']=mode
            meta['open_premises']=open_premises
            meta['asserts_endpoint_truth']=False
        evidence_pins=(_bindings(meta.get('evidence_hashes',[]),'evidence_hashes')
                       if not structural and meta['status']=='accepted' else {})
        local_evidence=set()
        for ref in meta['evidence']:
            if ref.startswith('source:'):
                # Exact source commit/path is resolved by work.py clean show.
                fields=ref.split(':',2)
                if len(fields)!=3 or len(fields[1])!=40 or any(c not in '0123456789abcdef' for c in fields[1]) or not fields[2]:
                    raise ValueError('source evidence must be source:<commit>:<path>#section')
                from cleanup import inventory
                if valid_source_refs is None:
                    valid_source_refs={(s['commit'],s['path']) for row in inventory(root) for s in row['sources']}
                if (fields[1],fields[2].split('#')[0]) not in valid_source_refs:
                    raise ValueError('source evidence is not in the frozen inventory: '+ref)
            else:
                name=ref.split('#')[0]
                p=_safe_path(root,name)
                if not p.is_file():
                    raise ValueError('missing evidence: '+ref)
                local_evidence.add(name)
                if not structural and meta['status']=='accepted':
                    artifact=artifacts.get(name)
                    if not artifact:
                        raise ValueError(f'{path}: local evidence is not admitted mathematics or an owned attachment: '+name)
                    if artifact.get('role')=='evidence' and not endpoints.intersection(artifact.get('owner_ids',[])):
                        raise ValueError(f'{path}: evidence has no mathematical owner among these endpoints: '+name)
                    evidence_sha=hashlib.sha256(p.read_bytes()).hexdigest()
                    if evidence_sha!=artifact['sha256'] or evidence_pins.get(name)!=evidence_sha:
                        raise ValueError(f'{path}: missing or stale evidence binding: '+name)
        if evidence_pins.keys()-local_evidence:
            raise ValueError(f'{path}: evidence hashes contain unrelated files')
        meta['path']=path.relative_to(root).as_posix()
        edges[eid]=HyperEdgeRecord(eid,kind,source_ids,target_ids,meta)
    return nodes,edges


def build(root,draft=False):
    # Drafts may cover an admitted region; neither draft nor final builds
    # infer mathematical admission from a directory listing.
    original_fingerprint=input_fingerprint(root)
    nodes,edges=read_records(root,final=not draft)
    if not draft:
        from cleanup import inventory, progress, stats, validate_receipt, curation_target_routes
        rows=inventory(root)
        pending=[r for r in rows if progress(root,r['id']).get('disposition') not in {'integrated','retained','duplicate','retired'}]
        if pending:
            raise ValueError(f'{len(pending)} source versions are not semantically completed; stage 3 final build is blocked (use --draft only for a labelled scaffold)')
        if stats(root)['local_source_hold']:
            raise ValueError('Local unpublished source intake is still unresolved; final completeness cannot be reported')
        routes=curation_target_routes(root)
        for row in rows:
            record=progress(root,row['id']);validate_receipt(root,record,curation_routes=routes)
            if record.get('source_sha256')!=row['sha256'] or not record.get('owner'):
                raise ValueError('Source completion is not bound to the frozen bytes and an owner')
    if not draft and any(n.attributes['status'].startswith('scaffold') for n in nodes.values()):
        raise ValueError('Question-identity scaffolds must be read and curated before a final map')
    accepted={k:v for k,v in edges.items() if v.attributes['status']=='accepted'}
    graph_scopes=scopes(root)
    if input_fingerprint(root)!=original_fingerprint:
        raise ValueError('graph inputs changed during build; no projection was written')
    for scope in graph_scopes:
        prefix=scope.relative_to(root).as_posix()+'/' if scope!=root else ''
        local={nid for nid,n in nodes.items() if not prefix or n.attributes['path'].startswith(prefix)}
        selected={eid:e for eid,e in accepted.items() if local.intersection(e.source_ids+e.target_ids)}
        required=local|{x for e in selected.values() for x in e.source_ids+e.target_ids}
        snapshot=GraphSnapshot(1,{x:nodes[x] for x in sorted(required)},selected).to_json()
        snapshot['build_status']='draft-curated-partial' if draft else 'built-with-declared-edge-reviews'
        snapshot['mathematical_trust']='declared-reviews-not-a-formal-or-independent-proof-verdict'
        snapshot['curation_input_fingerprint']=original_fingerprint
        snapshot['boundary_nodes']=sorted(required-local)
        snapshot['scope']=scope.relative_to(root).as_posix()
        from curation import _safe_path
        out=_safe_path(root,(scope/'map').relative_to(root).as_posix());out.mkdir(exist_ok=True)
        destination=_safe_path(root,(out/'graph.json').relative_to(root).as_posix())
        temporary=None
        try:
            with tempfile.NamedTemporaryFile('w',encoding='utf-8',dir=out,prefix='.graph-',delete=False) as stream:
                temporary=Path(stream.name)
                stream.write(json.dumps(snapshot,ensure_ascii=False,indent=2)+'\n')
            os.replace(temporary,destination)
        finally:
            if temporary and temporary.exists():temporary.unlink()
    return {'nodes':len(nodes),'accepted_edges':len(accepted),'proposed_edges':sum(e.attributes['status']=='proposed' for e in edges.values()),'status':'draft-curated-partial' if draft else 'built','projections':len(graph_scopes)}


def fingerprints(root, edge):
    """Mechanical version bindings; this operation does not review an edge."""
    nodes,_=read_records(root,include_edges=False)
    from curation import _safe_path
    path=_safe_path(root,edge)
    if path not in edge_paths(root):
        raise ValueError('select a current canonical edge file')
    meta,body=parse_flat_frontmatter(path.read_text())
    ids=set(meta.get('source_ids',[])+meta.get('target_ids',[]))
    if any(n not in nodes for n in ids):raise ValueError('unknown endpoint')
    evidence=[]
    for ref in meta.get('evidence',[]):
        if ref.startswith('source:'):continue
        p=_safe_path(root,ref.split('#')[0])
        if not p.is_file():raise ValueError('missing evidence')
        evidence.append(p.relative_to(root).as_posix()+':'+hashlib.sha256(p.read_bytes()).hexdigest())
    return {'endpoint_hashes':[n+':'+nodes[n].attributes['content_sha256'] for n in sorted(ids)],
            'evidence_hashes':sorted(set(evidence)),
            'reviewed_content_sha256':review_digest(meta,body),
            'limit':'mechanical bindings only; accepting a changed relation still requires mathematical review'}


def impact(root, object_ids):
    """A review worklist, never a cascade claiming downstream falsity."""
    records=[]
    for path in edge_paths(root):
        meta,_=parse_flat_frontmatter(path.read_text())
        if meta.get('status')=='rejected':continue
        records.append((path,meta))
    affected=set(object_ids);edges=set();changed=True
    while changed:
        changed=False
        for path,meta in records:
            endpoints=set(meta.get('source_ids',[])+meta.get('target_ids',[]))
            if not affected.intersection(endpoints):continue
            edges.add(path.relative_to(root).as_posix())
            if meta.get('kind') in LOGICAL_KINDS and affected.intersection(meta.get('source_ids',[])):
                targets=set(meta.get('target_ids',[]))-affected
                if targets:affected.update(targets);changed=True
    return {'status':'needs-review-not-refuted','changed_objects':sorted(object_ids),
            'affected_edges':sorted(edges),'downstream_review_objects':sorted(affected-set(object_ids)),
            'limit':'alternative proofs may remain valid; this is a review scope, not a truth assignment'}


def freshness(root):
    from curation import _safe_path
    path=_safe_path(root,'map/graph.json')
    if not path.is_file():return {'status':'missing-derived-graph','fresh':False}
    graph=json.loads(path.read_text())
    current=input_fingerprint(root)
    fresh=graph.get('curation_input_fingerprint')==current
    return {'status':'fresh-derived-view' if fresh else 'stale-derived-view-rebuild-required',
            'fresh':fresh,'current_input_fingerprint':current,
            'limit':'Freshness of a derived graph is not mathematical correctness.'}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--repo',type=Path,default=Path(__file__).resolve().parents[1])
    sub=p.add_subparsers(dest='command',required=True)
    c=sub.add_parser('check');c.add_argument('--structural',action='store_true',help='diagnose all current formal candidates without admitting them')
    b=sub.add_parser('build');b.add_argument('--draft',action='store_true')
    f=sub.add_parser('fingerprints');f.add_argument('edge')
    i=sub.add_parser('impact');i.add_argument('object_ids',nargs='+')
    sub.add_parser('freshness')
    a=p.parse_args();root=a.repo.resolve()
    if a.command=='check':
        n,e=read_records(root,structural=a.structural);result={'status':'structure-valid-not-a-mathematical-verdict' if a.structural else 'curated-structure-valid-not-a-mathematical-verdict','nodes':len(n),'edges':len(e)}
    elif a.command=='fingerprints':result=fingerprints(root,a.edge)
    elif a.command=='impact':result=impact(root,a.object_ids)
    elif a.command=='freshness':result=freshness(root)
    else:result=build(root,a.draft)
    print(json.dumps(result,ensure_ascii=False))

if __name__=='__main__':
    try:main()
    except (ValueError,OSError,KeyError) as exc:
        raise SystemExit(str(exc))
