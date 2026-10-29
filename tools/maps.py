"""Build explained multi-source hypergraphs using vendored upstream records."""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
from vendor.mathagent.model import NodeRecord, HyperEdgeRecord, GraphSnapshot
from vendor.matek.frontmatter import parse_flat_frontmatter


def read_records(root):
    nodes, edges = {}, {}
    valid_source_refs = None
    paths = list((root/'archives').rglob('state/**/*.md'))
    paths += list((root/'archives').rglob('问题--问题.md'))
    for path in sorted(set(paths)):
        if path.name == 'README.md':
            continue
        meta, body = parse_flat_frontmatter(path.read_text())
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
        nodes[nid]=NodeRecord(nid,kind,meta)
    for path in sorted(root.rglob('map/edges/*.md')):
        meta, body=parse_flat_frontmatter(path.read_text())
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
                p=(root/ref.split('#')[0]).resolve()
                if not p.is_relative_to(root) or not p.is_file():
                    raise ValueError('missing evidence: '+ref)
        if meta['status'] not in ('accepted','proposed','rejected'):
            raise ValueError('edge status must be accepted/proposed/rejected')
        meta['path']=path.relative_to(root).as_posix()
        edges[eid]=HyperEdgeRecord(eid,kind,source_ids,target_ids,meta)
    return nodes,edges


def build(root,draft=False):
    if not draft:
        from cleanup import inventory, progress, stats, validate_receipt
        rows=inventory(root)
        pending=[r for r in rows if progress(root,r['id']).get('disposition') not in {'integrated','retained','duplicate','retired'}]
        if pending:
            raise ValueError(f'{len(pending)} source versions are not semantically completed; stage 3 final build is blocked (use --draft only for a labelled scaffold)')
        if stats(root)['local_source_hold']:
            raise ValueError('Local unpublished source intake is still unresolved; final completeness cannot be reported')
        for row in rows:
            record=progress(root,row['id']);validate_receipt(root,record)
            if record.get('source_sha256')!=row['sha256'] or not record.get('owner'):
                raise ValueError('Source completion is not bound to the frozen bytes and an owner')
    nodes,edges=read_records(root)
    if not draft and any(n.attributes['status'].startswith('scaffold') for n in nodes.values()):
        raise ValueError('Question-identity scaffolds must be read and curated before a final map')
    accepted={k:v for k,v in edges.items() if v.attributes['status']=='accepted'}
    scopes=[root]+sorted(p.parent for p in (root/'archives').rglob('map'))
    for scope in scopes:
        prefix=scope.relative_to(root).as_posix()+'/' if scope!=root else ''
        local={nid for nid,n in nodes.items() if not prefix or n.attributes['path'].startswith(prefix)}
        selected={eid:e for eid,e in accepted.items() if local.intersection(e.source_ids+e.target_ids)}
        required=local|{x for e in selected.values() for x in e.source_ids+e.target_ids}
        snapshot=GraphSnapshot(1,{x:nodes[x] for x in sorted(required)},selected).to_json()
        snapshot['build_status']='draft-scaffold' if draft else 'built-with-declared-edge-reviews'
        snapshot['boundary_nodes']=sorted(required-local)
        snapshot['scope']=scope.relative_to(root).as_posix()
        out=scope/'map';out.mkdir(exist_ok=True)
        (out/'graph.json').write_text(json.dumps(snapshot,ensure_ascii=False,indent=2)+'\n')
    return {'nodes':len(nodes),'accepted_edges':len(accepted),'proposed_edges':sum(e.attributes['status']=='proposed' for e in edges.values()),'status':'draft-scaffold' if draft else 'built','projections':len(scopes)}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--repo',type=Path,default=Path(__file__).resolve().parents[1])
    sub=p.add_subparsers(dest='command',required=True);sub.add_parser('check');b=sub.add_parser('build');b.add_argument('--draft',action='store_true')
    a=p.parse_args();root=a.repo.resolve()
    if a.command=='check':
        n,e=read_records(root);result={'status':'structure-valid-not-a-mathematical-verdict','nodes':len(n),'edges':len(e)}
    else:result=build(root,a.draft)
    print(json.dumps(result,ensure_ascii=False))

if __name__=='__main__':
    try:main()
    except (ValueError,OSError,KeyError) as exc:
        raise SystemExit(str(exc))
