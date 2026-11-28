"""Persistent research ledger for the CN crisis workbench.

Every command returns JSON-compatible data. register_cli(subparsers) registers
handlers expecting args.workspace. Files given to stage/review/release are
relative to that workspace. JSON imports may be outside it; referenced raw_file
and proposed write paths must remain inside it. Initial graph-put creates nodes
and ALL-premise edges; later edits go through proposal/apply with revision CAS.
The ledger preserves model judgments; it does not manufacture causal truth.
"""
from __future__ import annotations

import copy
import hashlib
import json
import os
from pathlib import Path
import re
import tempfile
from datetime import datetime, timezone
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

FIRST_STAGES = tuple('s01_scope s02_inventory s03_acquisition s04_vintages s05_methods s06_viewpoints s07_property s08_fiscal s09_households s10_banks s11_external s12_history s13_graph s14_models s15_adversarial s16_verdict s17_writing s18_calculator s19_audit s20_release'.split())
REPORT_STAGES = tuple('s18_editorial' if x == 's18_calculator' else x for x in FIRST_STAGES)
REPORT_DEPS = {
    's01_scope': (), 's02_inventory': ('s01_scope',), 's03_acquisition': ('s02_inventory',),
    's04_vintages': ('s03_acquisition',), 's05_methods': ('s01_scope',),
    's06_viewpoints': ('s03_acquisition',),
    **{x: ('s04_vintages', 's06_viewpoints') for x in
       ('s07_property', 's08_fiscal', 's09_households', 's10_banks', 's11_external')},
    's12_history': ('s06_viewpoints',),
    's13_graph': ('s07_property', 's08_fiscal', 's09_households', 's10_banks', 's11_external', 's12_history'),
    's14_models': ('s05_methods', 's13_graph'), 's15_adversarial': ('s13_graph', 's14_models'),
    's16_verdict': ('s15_adversarial',), 's17_writing': ('s16_verdict',),
    's18_editorial': ('s17_writing',), 's19_audit': ('s18_editorial',), 's20_release': ('s19_audit',),
}
UPDATE_STAGES = tuple('i01_restore i02_delta i03_research i04_proposal i05_review i06_merge i07_replay i08_release'.split())
FACT_KINDS = {'fact', 'observation', 'dataset'}
SOURCE_KINDS = FACT_KINDS | {'opinion', 'method'}
NODE_KINDS = {'fact', 'judgment', 'opinion', 'action', 'method'}
IDENTIFIER = re.compile(r'^[A-Za-z0-9][A-Za-z0-9_.:-]{0,127}$')


class EngineError(ValueError):
    pass


def now():
    return datetime.now(timezone.utc).isoformat(timespec='seconds')


def digest(value):
    b = value if isinstance(value, bytes) else json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()
    return hashlib.sha256(b).hexdigest()


def canonical_url(url):
    parts = urlsplit(str(url).strip())
    if parts.scheme not in ('https', 'http'):
        return str(url).strip()
    query = [(k, v) for k, v in parse_qsl(parts.query, keep_blank_values=True)
             if not k.lower().startswith('utm_') and k.lower() not in ('fbclid', 'gclid', 'spm')]
    path = parts.path.rstrip('/') or '/'
    return urlunsplit((parts.scheme.lower(), parts.netloc.lower(), path, urlencode(sorted(query)), ''))


def read_json(path):
    try:
        return json.loads(Path(path).read_text(encoding='utf-8-sig'))
    except (OSError, ValueError) as exc:
        raise EngineError(f'Cannot read JSON {path}: {exc}') from exc


def checked_id(value):
    if not isinstance(value, str) or not IDENTIFIER.fullmatch(value):
        raise EngineError(f'Invalid ID: {value!r}')
    return value


def nonempty(value, name):
    if not isinstance(value, str) or not value.strip():
        raise EngineError(f'{name} must be nonempty text')
    return value.strip()


def iso_time(value):
    try:
        d = datetime.fromisoformat(str(value).replace('Z', '+00:00'))
        if d.tzinfo is None:
            d = d.replace(tzinfo=timezone.utc)
        return d
    except ValueError as exc:
        raise EngineError(f'Invalid ISO timestamp {value!r}') from exc


class Store:
    def __init__(self, workspace):
        self.root = Path(workspace).resolve()
        self.state_path = self.root / 'research_state.json'
        self.lock = self.root / '.engine.lock'
        self.state = None
        self.fd = None
        self.rollbacks = []

    def path(self, name):
        p = (self.root / name).resolve()
        if not p.is_relative_to(self.root) or p == self.root:
            raise EngineError(f'Path must remain inside workspace: {name}')
        if p.name in ('research_state.json', '.engine.lock'):
            raise EngineError('Ledger files cannot be supplied as research artifacts')
        return p

    def __enter__(self):
        self.root.mkdir(parents=True, exist_ok=True)
        try:
            self.fd = os.open(self.lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
            os.write(self.fd, str(os.getpid()).encode())
        except FileExistsError as exc:
            raise EngineError('Workspace is locked by another writer; preserve the lock until that writer finishes') from exc
        try:
            if self.state_path.exists():
                self.state = read_json(self.state_path)
                if self.state.get('schema') != 1:
                    raise EngineError('Unsupported ledger schema')
            return self
        except BaseException:
            self.__exit__(None, None, None)
            raise

    def require(self):
        if self.state is None:
            raise EngineError('Run init before using this workspace')
        return self.state

    def __exit__(self, typ, value, trace):
        if typ is not None:
            for p, original in reversed(self.rollbacks):
                if original is None:
                    p.unlink(missing_ok=True)
                else:
                    self._atomic(p, original)
        if self.fd is not None:
            os.close(self.fd)
            self.fd = None
            self.lock.unlink(missing_ok=True)

    def _atomic(self, path, data):
        path.parent.mkdir(parents=True, exist_ok=True)
        fd, temp = tempfile.mkstemp(prefix='.write-', dir=path.parent)
        try:
            with os.fdopen(fd, 'wb') as stream:
                stream.write(data)
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(temp, path)
        finally:
            if os.path.exists(temp):
                os.unlink(temp)

    def write_artifact(self, name, data):
        p = self.path(name)
        self.rollbacks.append((p, p.read_bytes() if p.exists() else None))
        self._atomic(p, data)

    def save(self):
        self._atomic(self.state_path, (json.dumps(self.state, ensure_ascii=False, indent=2, sort_keys=True) + '\n').encode())
        self.rollbacks.clear()

    def stages(self):
        if self.state['mode'] != 'first':
            return UPDATE_STAGES
        return REPORT_STAGES if self.report_first() else FIRST_STAGES

    def report_first(self):
        return self.state.get('runtime', {}).get('profile') == 'report-first'

    def stage_dependencies(self, stage_id):
        if self.report_first() and self.state['mode'] == 'first':
            return REPORT_DEPS[stage_id]
        return self.stages()[:self.stages().index(stage_id)]

    def event(self, kind, details):
        self.state['history'].append({'event': kind, 'at': now(), 'cycle': self.state['cycle'], **details})

    def invalidate(self, first, update):
        phases = self.stages()
        cutoff = first if self.state['mode'] == 'first' else update
        # Report research uses bound artifacts + declared dependencies. Preserve
        # unrelated work instead of deleting every later receipt on any intake.
        if not self.report_first():
            for stage_id in phases[cutoff:]:
                self.state['stages'].pop(stage_id, None)
        self.state['review'] = None
        self.state['release'] = None

    def resolve(self, source_id):
        return self.state['aliases'].get(source_id, source_id)

    def exists(self, item):
        item = self.resolve(item)
        return item in self.state['sources'] or item in self.state['nodes']

    def files(self, names):
        result = {}
        if not names:
            raise EngineError('At least one artifact is required')
        for name in names:
            p = self.path(name)
            if not p.is_file():
                raise EngineError(f'Missing artifact: {name}')
            data = p.read_bytes()
            if not data.strip():
                raise EngineError(f'Empty research artifact: {name}')
            result[str(p.relative_to(self.root))] = digest(data)
        return dict(sorted(result.items()))

    def stale_downstream(self, changed):
        affected = set(changed)
        while True:
            before = len(affected)
            for node_id, node in self.state['nodes'].items():
                if any(self.resolve(x) in affected for x in node.get('evidence', [])):
                    affected.add(node_id)
            for edge in self.state['edges'].values():
                if any(self.resolve(x) in affected for x in edge['tails'] + edge.get('counterevidence', [])):
                    affected.add(edge['head'])
                    edge['status'] = 'needs_review'
            if len(affected) == before:
                break
        for item in affected:
            if item in self.state['nodes'] and self.state['nodes'][item]['status'] != 'withdrawn':
                self.state['nodes'][item]['status'] = 'needs_review'
        return sorted(x for x in affected if x in self.state['nodes'])

    def graph_status(self):
        supported = set(self.state['sources'])
        supported_fact = {k for k, v in self.state['sources'].items() if v['kind'] in FACT_KINDS}
        reasons = {}
        while True:
            before = len(supported)
            for key, node in self.state['nodes'].items():
                if node['status'] != 'current':
                    reasons[key] = node['status']
                    continue
                direct = [self.resolve(x) for x in node.get('evidence', [])]
                incoming = [e for e in self.state['edges'].values() if e['head'] == key and e['status'] == 'current']
                direct_ok = bool(direct) and all(x in supported for x in direct)
                edge_ok = any(all(self.resolve(t) in supported for t in edge['tails']) for edge in incoming)
                if not direct_ok and not edge_ok:
                    reasons[key] = 'No grounded complete ALL-premise route (a cycle cannot support itself)'
                    continue
                if node['kind'] == 'fact':
                    factual_direct = direct_ok and all(x in supported_fact for x in direct)
                    factual_edge = any(all(self.resolve(t) in supported_fact for t in e['tails']) for e in incoming)
                    if not factual_direct and not factual_edge:
                        reasons[key] = 'Opinion or analyst judgment cannot be promoted automatically into a factual observation'
                        continue
                    supported_fact.add(key)
                supported.add(key)
                reasons.pop(key, None)
            if len(supported) == before:
                break
        edge_status = {}
        for key, edge in self.state['edges'].items():
            missing = [x for x in edge['tails'] if self.resolve(x) not in supported]
            edge_status[key] = {'status': edge['status'], 'all_premises_met': not missing, 'missing': missing}
        return {'nodes': {k: {'status': v['status'], 'grounded': k in supported, 'reason': reasons.get(k, '')}
                          for k, v in self.state['nodes'].items()}, 'edges': edge_status,
                'unresolved_edges': sorted(k for k, v in self.state['edges'].items() if v['status'] == 'needs_review'),
                'unresolved': sorted(k for k, v in self.state['nodes'].items()
                                     if v['status'] != 'withdrawn' and k not in supported)}

    def all_stage_files(self):
        paths = set()
        for stage in self.state['stages'].values():
            paths.update(stage['files'])
        return paths

    def valid_stages(self):
        valid, changed = [], {}
        for key in self.stages():
            stage = self.state['stages'].get(key)
            if stage is None:
                changed[key] = 'missing'
                continue
            try:
                current = self.files(stage['files'])
            except EngineError as exc:
                changed[key] = str(exc)
                continue
            if current != stage['files']:
                changed[key] = 'artifact changed after stage submission'
                continue
            if any(x not in valid for x in self.stage_dependencies(key)):
                changed[key] = 'required dependency is stale'
                continue
            if self.report_first():
                expected = {x: digest(self.state['stages'][x])
                            for x in self.stage_dependencies(key)}
                if stage.get('dependency_receipts') != expected:
                    changed[key] = 'dependency was revised after this stage'
                    continue
            valid.append(key)
        return valid, changed

    def untracked_formal(self, known):
        directory = self.root / 'formal'
        if not directory.exists():
            return []
        out_of_scope = {'formal/calculator.html', 'formal/scenarios.json'} if self.report_first() else set()
        return sorted(str(p.relative_to(self.root)) for p in directory.rglob('*')
                      if p.is_file() and str(p.relative_to(self.root)) not in known
                      and str(p.relative_to(self.root)) not in out_of_scope)

    def source_blob_hashes(self):
        blobs = {}
        for source in self.state['sources'].values():
            # Historical originals are part of the evidence for later revisions.
            for version in [source, *source.get('versions', [])]:
                path = version['blob']
                actual = self.files([path])[path]
                if actual != version['body_sha256']:
                    raise EngineError(f'Raw source bytes changed: {path}')
                blobs[path] = actual
        return blobs

    def snapshot(self, extra):
        paths = sorted(self.all_stage_files() | set(extra))
        return digest({'revision': self.state['revision'], 'cycle': self.state['cycle'],
                       'sources': self.state['sources'], 'aliases': self.state['aliases'],
                       'nodes': self.state['nodes'], 'edges': self.state['edges'],
                       'proposals': self.state['proposals'], 'stages': self.state['stages'],
                       'raw_files': self.source_blob_hashes(), 'files': self.files(paths)})


def initialise(args):
    with Store(args.workspace) as db:
        if db.state is None:
            if args.mode == 'update':
                raise EngineError('Incremental research requires a restored existing ledger')
            db.state = {'schema': 1, 'mode': 'first', 'cycle': 1, 'revision': 0,
                        'sources': {}, 'aliases': {}, 'nodes': {}, 'edges': {}, 'searches': [],
                        'proposals': {}, 'stages': {}, 'history': [], 'review': None, 'release': None}
            db.event('init', {'mode': 'first'})
        elif args.mode == 'update' and (db.state['mode'] != 'update' or db.state['release'] is not None):
            if not db.state['release']:
                raise EngineError('Complete and release the current cycle before beginning an update')
            reviewed = db.state['review']
            valid, _ = db.valid_stages()
            try:
                current = (reviewed and reviewed['verdict'] == 'pass'
                           and db.snapshot(reviewed['files']) == reviewed['snapshot']
                           and not db.untracked_formal(reviewed['files'])
                           and len(valid) == len(db.stages()))
            except EngineError:
                current = False
            if not current:
                raise EngineError('Repair the current cycle before update: its release snapshot is stale')
            prior = copy.deepcopy(db.state['release'])
            db.state['mode'] = 'update'
            db.state['cycle'] += 1
            db.state['stages'] = {}
            db.state['review'] = None
            db.state['release'] = None
            db.event('begin_update', {'prior_release': prior})
        db.save()
        return {'mode': db.state['mode'], 'cycle': db.state['cycle'], 'stages': db.stages()}


def ingest(args):
    records = read_json(args.file)
    records = records if isinstance(records, list) else records.get('records', [records])
    with Store(args.workspace) as db:
        state = db.require()
        output, affected = [], set()
        for original in records:
            record = copy.deepcopy(original)
            sid = checked_id(record['id'])
            if sid in state['nodes'] or sid in state['edges']:
                raise EngineError(f'ID already used by graph: {sid}')
            if 'targets' in record and not isinstance(record['targets'], list):
                raise EngineError('targets must be a list of node IDs')
            kind = record.get('kind', 'fact')
            if kind not in SOURCE_KINDS:
                raise EngineError(f'Unknown source kind {kind}')
            for field in ('url', 'source_family', 'published_at'):
                nonempty(record.get(field), field)
            if kind in FACT_KINDS:
                nonempty(record.get('observation_period'), 'observation_period')
            text_body = record.get('text', '')
            if record.get('raw_file'):
                raw = db.path(record['raw_file']).read_bytes()
            else:
                raw = nonempty(text_body, 'text').encode()
            if not raw.strip():
                raise EngineError('Raw source content must be nonempty')
            body_hash = digest(raw)
            record.update(kind=kind, canonical_url=canonical_url(record['url']), body_sha256=body_hash)
            existing = state['sources'].get(db.resolve(sid))
            if sid in state['aliases']:
                repost = next((x for x in (existing or {}).get('reposts', []) if x['id'] == sid), {})
                if (existing and existing['body_sha256'] == body_hash and existing['kind'] == kind
                        and existing.get('observation_period') == record.get('observation_period')
                        and existing.get('vintage') == record.get('vintage')
                        and all(repost.get(k) == record.get(k) for k in ('url', 'source_family', 'published_at'))):
                    output.append({'id': sid, 'status': 'unchanged', 'canonical_id': db.resolve(sid)})
                    continue
                raise EngineError('A repost alias now contains a different version; ingest it under a new evidence ID')
            duplicate = next((key for key, value in state['sources'].items()
                              if value['body_sha256'] == body_hash
                              and value['kind'] == kind
                              and value.get('observation_period') == record.get('observation_period')
                              and value.get('original_published_at', value['published_at']) == record.get('original_published_at', record['published_at'])
                              and value.get('vintage') == record.get('vintage')
                              and (not value.get('event_id') or not record.get('event_id') or value['event_id'] == record['event_id'])), None)
            if duplicate and not existing:
                if state['nodes']:
                    if 'targets' not in record:
                        raise EngineError('New or revised evidence requires explicit targets, or targets: [] with an impact_note')
                    if not record['targets']:
                        nonempty(record.get('impact_note'), 'impact_note for evidence with no affected claim')
                state['aliases'][sid] = duplicate
                state['sources'][duplicate].setdefault('reposts', []).append({
                    'id': sid, 'url': record['url'], 'source_family': record['source_family'],
                    'published_at': record['published_at']})
                output.append({'id': sid, 'status': 'duplicate', 'canonical_id': duplicate})
                continue
            if existing and existing['body_sha256'] == body_hash and all(existing.get(k) == record.get(k) for k in original):
                output.append({'id': sid, 'status': 'unchanged'})
                continue
            if sid in state['nodes'] or sid in state['edges'] or sid in state['aliases']:
                raise EngineError(f'ID already used elsewhere: {sid}')
            if state['nodes']:
                if 'targets' not in record:
                    raise EngineError('New or revised evidence requires explicit targets, or targets: [] with an impact_note')
                if not record['targets']:
                    nonempty(record.get('impact_note'), 'impact_note for evidence with no affected claim')
            record['revision'] = (existing or {}).get('revision', 0) + 1
            record['versions'] = copy.deepcopy((existing or {}).get('versions', []))
            if existing:
                record['versions'].append({k: v for k, v in existing.items() if k != 'versions'})
                affected.add(sid)
            record.setdefault('event_id', '')
            record['received_at'] = now()
            record['blob'] = f'source_blobs/{body_hash}.bin'
            db.write_artifact(record['blob'], raw)
            state['sources'][sid] = record
            for target in record.get('targets', []):
                if target not in state['nodes']:
                    raise EngineError(f'Unknown targeted claim {target}')
                affected.add(target)
            output.append({'id': sid, 'status': 'updated' if existing else 'added'})
        stale = db.stale_downstream(affected)
        if any(x['status'] != 'unchanged' for x in output):
            state['revision'] += 1
            db.invalidate(2, 1)
            db.event('ingest', {'records': output, 'affected': stale})
        db.save()
        groups = {}
        for sid, source in state['sources'].items():
            if source.get('event_id'):
                groups.setdefault(source['event_id'], []).append(sid)
        publications = {}
        for sid, source in state['sources'].items():
            origin = canonical_url(source.get('original_source_url', source['url']))
            key = digest([origin, source.get('original_published_at', source['published_at']), source.get('vintage')])[:16]
            publications.setdefault(key, {'origin_url': origin, 'source_family': source['source_family'],
                                          'published_at': source.get('original_published_at', source['published_at']), 'evidence_ids': []})['evidence_ids'].append(sid)
        return {'records': output, 'evidence_record_count': len(state['sources']),
                'publication_count': len(publications), 'publication_groups': publications,
                'source_family_count': len({r['source_family'] for r in state['sources'].values()}),
                'event_groups': groups, 'needs_review': stale}


def search_plan(args):
    with Store(args.workspace) as db:
        db.require()
        key = (' '.join(args.query.casefold().split()), args.topic.strip(), args.period.strip())
        if args.freshness_days < 0:
            raise EngineError('freshness-days must be nonnegative')
        matches, related = [], []
        for entry in db.state['searches']:
            age = (datetime.now(timezone.utc) - iso_time(entry['executed_at'])).total_seconds() / 86400
            if 0 <= age <= args.freshness_days:
                if tuple(entry['key']) == key:
                    matches.append(entry)
                elif tuple(entry['key'][1:]) == key[1:]:
                    related.append(entry)
        return {'decision': 'reuse' if matches else 'search', 'query': args.query,
                'topic': args.topic, 'period': args.period, 'matches': matches, 'related_scope_searches': related,
                'reason': 'Existing exact scope is fresh, including recorded zero-result searches' if matches
                else 'Read the related same-topic/same-period results first; the model must decide whether a new query adds evidence' if related
                else 'No fresh search covers this query, topic, and observation window'}


def search_log(args):
    entry = read_json(args.file)
    with Store(args.workspace) as db:
        db.require()
        for field in ('query', 'topic', 'period'):
            nonempty(entry.get(field), field)
        entry.setdefault('executed_at', now())
        if iso_time(entry['executed_at']) > datetime.now(timezone.utc):
            raise EngineError('Search timestamp cannot be in the future')
        entry['key'] = [' '.join(entry['query'].casefold().split()), entry['topic'].strip(), entry['period'].strip()]
        entry.setdefault('results', [])
        for sid in entry.get('result_ids', []):
            if db.resolve(sid) not in db.state['sources']:
                raise EngineError(f'Unknown search result source {sid}')
        entry['id'] = 'Q' + str(len(db.state['searches']) + 1).zfill(5)
        db.state['searches'].append(entry)
        db.event('search_log', {'id': entry['id'], 'query': entry['query'], 'result_count': len(entry['results'])})
        db.save()
        return entry


def validate_graph(db):
    for key, node in db.state['nodes'].items():
        checked_id(key)
        if node.get('kind') not in NODE_KINDS:
            raise EngineError(f'Unknown node kind {node.get("kind")}')
        nonempty(node.get('statement'), 'node.statement')
        if node['status'] not in ('current', 'needs_review', 'withdrawn'):
            raise EngineError('Invalid node status')
        if not isinstance(node.get('evidence', []), list):
            raise EngineError('node.evidence must be a list')
        for evidence in node.get('evidence', []):
            if not db.exists(evidence):
                raise EngineError(f'Unknown evidence {evidence} for {key}')
    for key, edge in db.state['edges'].items():
        checked_id(key)
        if not isinstance(edge.get('tails'), list):
            raise EngineError('edge.tails must be a list')
        if edge.get('mode', 'ALL') != 'ALL' or not edge.get('tails'):
            raise EngineError('Hyperedge must contain nonempty ALL premises')
        if len(set(edge['tails'])) != len(edge['tails']):
            raise EngineError('Duplicate hyperedge premises')
        if edge['head'] not in db.state['nodes']:
            raise EngineError(f'Unknown hyperedge conclusion {edge["head"]}')
        for premise in edge['tails'] + edge.get('counterevidence', []):
            if not db.exists(premise):
                raise EngineError(f'Unknown hyperedge reference {premise}')
        for field in ('mechanism', 'falsifier', 'lag'):
            nonempty(edge.get(field), 'edge.' + field)
        for field in ('conditions', 'counterevidence'):
            if field not in edge or not isinstance(edge[field], list):
                raise EngineError(f'edge.{field} must be a list')
        if edge['status'] not in ('current', 'needs_review', 'withdrawn'):
            raise EngineError('Invalid edge status')


def graph_put(args):
    data = read_json(args.file)
    if isinstance(data, list):
        data = {'nodes': [x for x in data if 'tails' not in x], 'edges': [x for x in data if 'tails' in x]}
    elif 'nodes' not in data and 'edges' not in data:
        data = {'edges' if 'tails' in data else 'nodes': [data]}
    with Store(args.workspace) as db:
        db.require()
        added = []
        for bucket in ('nodes', 'edges'):
            for original in data.get(bucket, []):
                item = copy.deepcopy(original)
                key = checked_id(item['id'])
                item.setdefault('status', 'current')
                if bucket == 'nodes':
                    item.setdefault('kind', 'judgment')
                    item.setdefault('evidence', [])
                else:
                    item.setdefault('mode', 'ALL')
                existing = db.state[bucket].get(key)
                if existing:
                    if all(existing.get(k) == v for k, v in item.items()):
                        continue
                    raise EngineError('Existing graph entries must be edited through proposal/apply')
                if key in db.state['sources'] or key in db.state['aliases'] or key in db.state['nodes'] or key in db.state['edges']:
                    raise EngineError(f'ID already in use: {key}')
                item['revision'] = 1
                db.state[bucket][key] = item
                added.append(key)
        validate_graph(db)
        if added:
            db.state['revision'] += 1
            db.invalidate(12, 3)
            db.event('graph_put', {'added': added})
        db.save()
        return {'added': added, **db.graph_status()}


def graph_status(args):
    with Store(args.workspace) as db:
        db.require()
        return db.graph_status()


def proposal(args):
    p = read_json(args.file)
    with Store(args.workspace) as db:
        db.require()
        pid = checked_id(p['id'])
        if pid in db.state['proposals']:
            raise EngineError('Proposal ID already exists')
        target = p.get('target')
        bucket = 'edges' if target in db.state['edges'] else 'nodes'
        current = db.state[bucket].get(target)
        if not current:
            raise EngineError(f'Unknown proposal target {target}')
        if p.get('base_revision') != current['revision']:
            raise EngineError('Proposal base revision is stale')
        action = p.get('action')
        if action not in ('retain', 'strengthen', 'weaken', 'replace', 'withdraw'):
            raise EngineError('Action must be retain, strengthen, weaken, replace, or withdraw')
        nonempty(p.get('reason'), 'proposal.reason')
        if not p.get('new_evidence') and not p.get('new_method'):
            raise EngineError('A change needs new evidence or a concrete new method')
        for evidence in p.get('new_evidence', []):
            if not db.exists(evidence):
                raise EngineError(f'Unknown new evidence {evidence}')
        old_statement = current.get('statement', current.get('mechanism'))
        if p.get('old_statement') != old_statement:
            raise EngineError('Proposal must quote the exact current statement')
        if bucket == 'nodes' and action != 'withdraw':
            nonempty(p.get('new_statement'), 'proposal.new_statement')
        if bucket == 'edges' and action != 'withdraw':
            if not isinstance(p.get('replacement'), dict):
                raise EngineError('Edge proposal needs a replacement object')
        for file in p.get('files', []):
            actual = db.files([file['path']])[file['path']]
            if file.get('base_sha256') != actual:
                raise EngineError('Proposed artifact edit is based on stale bytes')
            if not isinstance(file.get('text'), str):
                raise EngineError('Proposed artifact text is required')
        prior = [x for x in db.state['proposals'].values() if x['target'] == target and x['status'] == 'applied']
        if bucket == 'nodes' and any(x.get('old_statement') == p.get('new_statement') for x in prior):
            if prior[-1]['id'] not in p.get('responds_to', []):
                raise EngineError('A reversal must explicitly answer the previous accepted proposal in responds_to')
        p['target_type'] = bucket
        p['status'] = 'pending'
        p['created_at'] = now()
        db.state['proposals'][pid] = p
        db.state['review'] = None
        db.state['release'] = None
        db.event('proposal', {'id': pid, 'target': target, 'action': action})
        db.save()
        return {'id': pid, 'status': 'pending', 'target': target, 'base_revision': p['base_revision']}


def proposal_snapshot(db, p):
    target = db.state[p['target_type']][p['target']]
    edits = [file['path'] for file in p.get('files', [])]
    clean = {k: v for k, v in p.items() if k != 'review'}
    return digest({'proposal': clean, 'target': target, 'evidence_revision': db.state['revision'],
                   'files': db.files(edits) if edits else {}, 'raw_files': db.source_blob_hashes()})


def proposal_review(args):
    with Store(args.workspace) as db:
        db.require()
        p = db.state['proposals'].get(args.id)
        if not p or p['status'] != 'pending':
            raise EngineError('A pending proposal is required for review')
        if args.reviewer == p.get('author', 'main'):
            raise EngineError('Proposal reviewer must be distinct from its author')
        target = db.state[p['target_type']][p['target']]
        if args.verdict == 'pass' and target['revision'] != p['base_revision']:
            raise EngineError('Proposal target changed; create a rebased proposal')
        receipt = {'verdict': args.verdict, 'reviewer': args.reviewer,
                   'note': nonempty(args.note, 'proposal-review.note'), 'at': now(),
                   'snapshot': proposal_snapshot(db, p)}
        p['review'] = receipt
        if args.verdict == 'reject':
            p['status'] = 'rejected'
        db.state['review'] = None
        db.state['release'] = None
        db.event('proposal_review', {'id': p['id'], 'verdict': args.verdict, 'reviewer': args.reviewer})
        db.save()
        return {'id': p['id'], 'status': p['status'], **receipt}


def apply(args):
    with Store(args.workspace) as db:
        db.require()
        p = db.state['proposals'].get(args.id)
        if not p or p['status'] != 'pending':
            raise EngineError('No pending proposal with that ID')
        current = db.state[p['target_type']][p['target']]
        if current['revision'] != p['base_revision']:
            raise EngineError('Target changed after proposal; rebase before applying')
        for file in p.get('files', []):
            actual = db.files([file['path']])[file['path']]
            if actual != file['base_sha256']:
                raise EngineError('Artifact changed after proposal; rebase before applying')
        reviewed = p.get('review')
        if not reviewed or reviewed['verdict'] != 'pass' or reviewed['snapshot'] != proposal_snapshot(db, p):
            raise EngineError('Proposal requires an accepted review of its current target, evidence revision, and artifact bytes')
        changed = {p['target']} if p['target_type'] == 'nodes' else {current['head']}
        stale = db.stale_downstream(changed)
        if p['action'] == 'withdraw':
            current['status'] = 'withdrawn'
        elif p['target_type'] == 'nodes':
            current['statement'] = p['new_statement']
            current['evidence'] = list(dict.fromkeys(current.get('evidence', []) + p.get('new_evidence', [])))
            current['status'] = 'current'
        else:
            protected = {'id': current['id'], 'revision': current['revision']}
            current.update(copy.deepcopy(p['replacement']))
            current.update(protected)
            current['status'] = 'current'
        current['revision'] += 1
        current['last_proposal'] = p['id']
        validate_graph(db)
        for file in p.get('files', []):
            db.write_artifact(file['path'], file['text'].encode())
        p['status'] = 'applied'
        p['applied_at'] = now()
        db.state['revision'] += 1
        db.invalidate(15, 5)
        db.event('apply', {'id': p['id'], 'target': p['target'], 'action': p['action'], 'needs_review': stale})
        db.save()
        return {'id': p['id'], 'status': 'applied', 'revision': current['revision'],
                'needs_review': [x for x in stale if x != p['target']]}


def stage(args):
    with Store(args.workspace) as db:
        db.require()
        phases = db.stages()
        if args.id not in phases:
            raise EngineError(f'Unknown stage; expected one of {", ".join(phases)}')
        valid, _ = db.valid_stages()
        index = phases.index(args.id)
        missing = [x for x in db.stage_dependencies(args.id) if x not in valid]
        if missing:
            raise EngineError(f'Complete or repair earlier stages first: {", ".join(missing)}')
        receipt = {'id': args.id, 'files': db.files(args.files), 'note': nonempty(args.note, 'stage.note'),
                   'submitted_at': now(), 'revision': db.state['revision']}
        if db.report_first():
            receipt['dependency_receipts'] = {
                x: digest(db.state['stages'][x]) for x in db.stage_dependencies(args.id)}
        db.state['stages'][args.id] = receipt
        if not db.report_first():
            for later in phases[index + 1:]:
                db.state['stages'].pop(later, None)
        db.state['review'] = None
        db.state['release'] = None
        db.event('stage', {'id': args.id, 'files': receipt['files']})
        db.save()
        return receipt


def review(args):
    with Store(args.workspace) as db:
        db.require()
        if args.verdict == 'reject':
            names = sorted(db.all_stage_files() | set(args.files))
            files = db.files(names) if names else {}
            db.state['review'] = {'verdict': 'reject', 'reviewer': args.reviewer,
                                  'author': args.author, 'files': files,
                                  'note': nonempty(args.note, 'review.note'), 'at': now(),
                                  'snapshot': db.snapshot(names) if names else None}
            db.state['release'] = None
            db.event('review', copy.deepcopy(db.state['review']))
            db.save()
            return db.state['review']
        valid, changed = db.valid_stages()
        if len(valid) != len(db.stages()):
            raise EngineError(f'Stages incomplete or stale: {changed}')
        if args.reviewer == args.author:
            raise EngineError('The final reviewer must be distinct from the author')
        graph = db.graph_status()
        if graph['unresolved'] or graph['unresolved_edges']:
            raise EngineError(f'Graph conclusions or mechanisms need adjudication: {graph["unresolved"] + graph["unresolved_edges"]}')
        if any(x['status'] == 'pending' for x in db.state['proposals'].values()):
            raise EngineError('Pending proposals require a disposition before review')
        names = sorted(db.all_stage_files() | set(args.files))
        files = db.files(names)
        unknown = db.untracked_formal(files)
        if unknown:
            raise EngineError(f'Unregistered formal artifacts: {unknown}')
        receipt = {'verdict': 'pass', 'reviewer': args.reviewer, 'author': args.author,
                   'note': nonempty(args.note, 'review.note'), 'at': now(), 'files': files,
                   'snapshot': db.snapshot(names)}
        db.state['review'] = receipt
        db.state['release'] = None
        db.event('review', {'verdict': 'pass', 'reviewer': args.reviewer, 'snapshot': receipt['snapshot']})
        db.save()
        return receipt


def release(args):
    with Store(args.workspace) as db:
        db.require()
        reviewed = db.state['review']
        if not reviewed or reviewed['verdict'] != 'pass':
            raise EngineError('An accepted current independent review is required')
        valid, changed = db.valid_stages()
        if len(valid) != len(db.stages()):
            raise EngineError(f'Stages incomplete or stale: {changed}')
        if db.snapshot(reviewed['files']) != reviewed['snapshot']:
            raise EngineError('Research or artifacts changed after the reviewed snapshot')
        files = db.files(args.files)
        if any(reviewed['files'].get(k) != v for k, v in files.items()):
            raise EngineError('All release files must be included in the reviewed snapshot')
        unknown = db.untracked_formal(reviewed['files'])
        if unknown:
            raise EngineError(f'Unregistered formal artifacts: {unknown}')
        judgment = nonempty(args.judgment, 'release.judgment')
        receipt = {'cycle': db.state['cycle'], 'mode': db.state['mode'], 'released_at': now(),
                   'files': files, 'judgment': judgment, 'review_snapshot': reviewed['snapshot']}
        db.state['release'] = receipt
        db.event('release', copy.deepcopy(receipt))
        db.save()
        return receipt


def status(args):
    with Store(args.workspace) as db:
        db.require()
        return status_result(db)


def status_result(db):
    """Inspect one locked ledger, also used by the resumable session entry."""
    valid, changed = db.valid_stages()
    result = {'mode': db.state['mode'], 'cycle': db.state['cycle'], 'revision': db.state['revision'],
              'sources': len(db.state['sources']), 'repost_aliases': len(db.state['aliases']),
              'searches': len(db.state['searches']), 'nodes': len(db.state['nodes']),
              'edges': len(db.state['edges']), 'completed_stages': valid, 'remaining_stages': changed,
              'graph': db.graph_status(), 'review': db.state['review'], 'release': db.state['release']}
    if result['release']:
        review_state = db.state['review']
        try:
            current = review_state and db.snapshot(review_state['files']) == review_state['snapshot']
            current = current and not db.untracked_formal(review_state['files']) and len(valid) == len(db.stages())
        except EngineError:
            current = False
        if not current:
            result['release'] = {**result['release'], 'current': False,
                                 'reason': 'Workspace changed after release; repair and submit a new review'}
        else:
            result['release'] = {**result['release'], 'current': True}
    return result


def register_cli(subparsers):
    def command(name, handler):
        p = subparsers.add_parser(name, help=(handler.__doc__ or name))
        p.set_defaults(func=handler)
        return p
    p = command('init', initialise)
    p.add_argument('--mode', choices=('first', 'update'), default='first')
    for name, handler in [('ingest', ingest), ('search-log', search_log), ('graph-put', graph_put), ('proposal', proposal)]:
        command(name, handler).add_argument('--file', required=True)
    p = command('search-plan', search_plan)
    p.add_argument('--query', required=True)
    p.add_argument('--topic', required=True)
    p.add_argument('--period', required=True)
    p.add_argument('--freshness-days', type=float, default=7)
    command('graph-status', graph_status)
    command('apply', apply).add_argument('--id', required=True)
    p = command('proposal-review', proposal_review)
    p.add_argument('--id', required=True)
    p.add_argument('--verdict', choices=('pass', 'reject'), required=True)
    p.add_argument('--reviewer', required=True)
    p.add_argument('--note', required=True)
    p = command('stage', stage)
    p.add_argument('--id', required=True)
    p.add_argument('--files', nargs='+', required=True)
    p.add_argument('--note', required=True)
    p = command('review', review)
    p.add_argument('--verdict', choices=('pass', 'reject'), required=True)
    p.add_argument('--files', nargs='*', default=[])
    p.add_argument('--note', required=True)
    p.add_argument('--reviewer', default='independent-reviewer')
    p.add_argument('--author', default='main')
    p = command('release', release)
    p.add_argument('--files', nargs='+', required=True)
    p.add_argument('--judgment', required=True)
    command('status', status)
