"""Shared notes claims use ordinary Git push as compare-and-swap.

Task changes are committed on an isolated index and worktree. A rejected push
re-reads the latest board before retrying. Drafts in the caller's clone are
never part of a task transaction. No leases expire silently.
"""
from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import uuid


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')


def safe(repo, name, beneath=None):
    path = Path(name)
    path = path if path.is_absolute() else repo / path
    path = path.resolve()
    if not path.is_relative_to((beneath or repo).resolve()):
        raise ValueError('Path must stay in the assigned workspace')
    return path


def fetch(repo, env, rt):
    rt.git(repo, 'fetch', '--quiet', '--no-tags', 'origin',
           '+refs/heads/' + rt.BRANCH + ':refs/remotes/origin/' + rt.BRANCH, env=env)
    return rt.git(repo, 'rev-parse', 'origin/' + rt.BRANCH).stdout.decode().strip()


def tree_json(repo, tip, path, rt):
    return json.loads(rt.git(repo, 'show', tip + ':' + path).stdout)


def board(repo, tip, rt):
    listing = rt.git(repo, 'ls-tree', '-r', '--name-only', tip, '--', 'tasks').stdout.decode().splitlines()
    tasks = [tree_json(repo, tip, name, rt) for name in listing if name.endswith('.json')]
    if not tasks:
        raise ValueError('No registered notes; initialize the input catalog first')
    return sorted(tasks, key=lambda t: t['order'])


def current_batch(tasks):
    return next((t['batch'] for t in tasks if t['status'] in {'pending', 'claimed'}), None)


def summary(tasks):
    batch = current_batch(tasks)
    return {'counts': dict(Counter(t['status'] for t in tasks)), 'current_batch': batch,
            'max_active_notes': 3, 'tasks': tasks,
            'claimable': [t['note_id'] for t in tasks if t['batch'] == batch and t['status'] == 'pending'],
            'completion_certified': False}


def owned(task, actor, run):
    if task.get('owner') != actor or task.get('run') != run:
        raise ValueError('Task is owned by another Boss/RUN; preserve its work and request an explicit handoff')


CONTENT_UNCERTAINTY_MARKERS = (
    'content_resolved', 'unresolved', 'glyph', 'recovery', 'ambiguous',
    '字形', '疑字', '模糊', '恢复', '未决', '判字', '人工', '看不清',
)


def reject_content_block(reason):
    """Keep visual uncertainty in the claimed work loop.

    A missing/corrupt input or an unavailable tool can be a real block. A
    recoverable reading uncertainty must be handled by another visual pass,
    not handed to the user as a manual task.
    """
    lowered = reason.casefold()
    return any(marker.casefold() in lowered for marker in CONTENT_UNCERTAINTY_MARKERS)


def prepare_autonomous_recovery(manifest, ledger, report):
    """Render the next recovery pass before returning the audit refusal.

    This is intentionally best-effort.  A malformed audit input must still
    remain a normal submission error, while a valid content gate should leave
    the model with an immediately usable crop queue instead of a handoff to a
    person.
    """
    try:
        from tools.autonomous_recovery import build
        project = manifest.parent
        return build(project, report, project / 'autonomous-recovery', dpi=800, ledger_path=ledger)
    except (OSError, RuntimeError, ValueError, KeyError, json.JSONDecodeError):
        return None


def remote_hash(repo, tip, path, rt):
    return hashlib.sha256(rt.git(repo, 'show', tip + ':' + path).stdout).hexdigest()


def assert_published(repo, tip, files, rt):
    for name, expected in files.items():
        if remote_hash(repo, tip, name, rt) != expected:
            raise ValueError('Published file differs from the checked evidence: ' + name)


def checked_source(repo, task):
    for source in task['source_pdfs']:
        if digest(safe(repo, source['path'])) != source['sha256']:
            raise ValueError('Original source changed: ' + source['path'])


def transition(tasks, args, actor, event_id, handoff=None, completion=None):
    """Pure state transition; the caller publishes it atomically or discards it."""
    action, run = args.action, args.run
    existing = [t for t in tasks if t['status'] == 'claimed' and t.get('owner') == actor and t.get('run') == run]
    selected = []
    if action == 'claim':
        batch = current_batch(tasks)
        available = [t for t in tasks if t['batch'] == batch and t['status'] == 'pending']
        if args.note:
            target = next((t for t in tasks if t['note_id'] == args.note), None)
            if target is None: raise ValueError('Unknown note ID')
            if target in existing: return [], [target]
            if target not in available: raise ValueError('Note is owned, blocked, complete, or outside the current batch')
            selected = [target]
        else:
            selected = available[:max(0, args.limit - len(existing))]
        slots = 3 - sum(t['status'] == 'claimed' for t in tasks)
        selected = selected[:max(0, slots)]
        for task in selected:
            task.update(status='claimed', owner=actor, run=run,
                        workspace=f'work/{run}/notes/{task["note_id"]}')
        result = existing + selected
    else:
        task = next((t for t in tasks if t['note_id'] == args.note), None)
        if task is None: raise ValueError('Unknown note ID')
        owned(task, actor, run)
        if action == 'resume':
            if task['status'] == 'claimed': return [], [task]
            if task['status'] != 'blocked': raise ValueError('Only a blocked task can be resumed')
            batch = current_batch(tasks)
            active = [t for t in tasks if t['status'] == 'claimed']
            if len(active) >= 3 or (batch is not None and batch != task['batch'] and (active or task['batch'] > batch)):
                raise ValueError('Finish the current batch before resuming an earlier blocked note')
            task['status'] = 'claimed'
        else:
            if task['status'] != 'claimed': raise ValueError('Task must be claimed first')
            if action in {'release', 'block'}:
                if not args.reason.strip(): raise ValueError('Provide a concrete reason')
                if action == 'block' and reject_content_block(args.reason):
                    raise ValueError(
                        'Do not block a note for visual or mathematical uncertainty. '
                        'Keep the task claimed and run autonomous recovery: render a targeted '
                        'high-resolution crop, inspect the original image, compare candidates, '
                        'verify the mathematics in both directions, update the ledger and drafts, '
                        'then rerun the audit. Block only for missing/corrupt input or unavailable tools.'
                    )
                task.update(status='pending' if action == 'release' else 'blocked',
                            handoff=handoff, reason=args.reason)
                if action == 'release': task.update(owner=None, run=None)
            elif action == 'submit':
                task.update(status='done', completion=completion)
        selected = result = [task]
    for task in selected:
        task.setdefault('history', []).append({'event_id': event_id, 'action': action,
            'actor': actor, 'run': run, 'at': datetime.now(timezone.utc).isoformat(),
            'workspace': task.get('workspace'),
            **({'reason': args.reason, 'handoff': handoff} if handoff else {})})
    return selected, result


def audit_submission(repo, args, task, rt):
    root = safe(repo, task['workspace'])
    manifest = safe(repo, args.manifest, root)
    ledger = safe(repo, args.ledger, root)
    report = safe(repo, args.report, root)
    source = json.loads(manifest.read_text())['source_pdf']
    if (source['sha256'], source['page_count']) != (task['source_pdfs'][0]['sha256'], task['pages']):
        raise ValueError('Audit manifest must cover the registered original and all its physical pages')
    record = json.loads(ledger.read_text())
    old_hashes = sorted(a['sha256'] for a in record['artifacts'] if a['kind'] == 'old')
    if old_hashes != sorted(a['sha256'] for a in task['previous_markdowns']):
        raise ValueError('Old-note audit scope differs from the registered input scope')
    script = repo / '.agents/skills/math-notes-evidence-audit/scripts/audit.py'
    result = subprocess.run([sys.executable, str(script), 'check', '--manifest', str(manifest),
        '--ledger', str(ledger), '--report', str(report)], cwd=repo, capture_output=True, timeout=600)
    if result.returncode:
        detail = rt.SECRET.sub(b'[REDACTED]', result.stderr + result.stdout).decode(errors='replace')[-1600:]
        if result.returncode == 2:
            recovery_plan = prepare_autonomous_recovery(manifest, ledger, report)
            plan_note = (' Recovery queue generated at ' + recovery_plan.relative_to(repo).as_posix() + '.'
                         if recovery_plan else
                         ' The recovery queue could not be generated; inspect the audit report and keep the task claimed.')
            raise ValueError(
                'AUTONOMOUS_RECOVERY_REQUIRED: the structural audit ran, but visual or '
                'mathematical records remain unresolved. Do not call notes block and do not '
                'ask the user. Read every unresolved record, render a targeted high-resolution '
                'crop, compare at least two candidates against the original image and the '
                'forward/backward mathematics, update both drafts and the ledger, then rerun '
                'notes submit.' + plan_note + ' ' + detail
            )
        raise ValueError('STRUCTURE_INCOMPLETE: finish the recorded page/region, mapping, or hash work before submitting. ' + detail)
    audit = json.loads(report.read_text())
    if not audit['audit_pass']:
        raise ValueError('STRUCTURE_INCOMPLETE: the audit does not satisfy the structural submission gate')
    if not audit['content_resolved']:
        recovery_plan = prepare_autonomous_recovery(manifest, ledger, report)
        plan_note = (' Recovery queue generated at ' + recovery_plan.relative_to(repo).as_posix() + '.'
                     if recovery_plan else
                     ' The recovery queue could not be generated; inspect the audit report and keep the task claimed.')
        raise ValueError(
            'AUTONOMOUS_RECOVERY_REQUIRED: content_resolved is false. Keep the task claimed, '
            'perform the high-resolution visual recovery loop, and submit again. This is not a '
            'human handoff and must never be converted into notes block.' + plan_note
        )
    files = {p.relative_to(repo).as_posix(): digest(p) for p in [manifest, ledger, report]}
    for kind, filename in [('transcription', 'source-transcript.md'), ('study', 'study-notes.md')]:
        artifacts = [a for a in record['artifacts'] if a['kind'] == kind]
        if len(artifacts) != 1: raise ValueError('Publish exactly one main document of each kind')
        output = repo / 'output' / task['note_id'] / filename
        if digest(output) != artifacts[0]['sha256']:
            raise ValueError('Published document differs from the audited document: ' + filename)
        files[output.relative_to(repo).as_posix()] = digest(output)
    saved = subprocess.run([sys.executable, str(repo / 'work.py'), 'checkpoint', task['workspace'],
        f'output/{task["note_id"]}', '-m', 'Save audited notes ' + task['note_id']],
        cwd=repo, capture_output=True, timeout=600)
    if saved.returncode or json.loads(saved.stdout)['status'] != 'pushed':
        raise ValueError('Save evidence before submitting: ' + rt.SECRET.sub(b'[REDACTED]', saved.stderr).decode(errors='replace')[-1200:])
    workspace_tree = rt.git(repo, 'rev-parse', 'HEAD:' + task['workspace']).stdout.decode().strip()
    return {'files': files, 'snapshot_sha256': audit['snapshot_sha256'],
            'workspace': task['workspace'], 'workspace_tree': workspace_tree,
            'status': audit['status'], 'visual_reading_proven': False,
            'mathematical_correctness_proven': False, 'zero_omission_proven': False,
            'scope': 'Current registered PDFs and supplied old notes only'}


def dispatch(repo, args, rt):
    actor = rt.config(repo, 'wcg.actor')
    if not actor: raise ValueError('Run start before accessing the shared queue')
    if args.action != 'queue':
        if not rt.IDENT.fullmatch(args.run): raise ValueError('Use a simple RUN ID')
        state_path = repo / 'work' / args.run / 'checkpoint.json'
        state = json.loads(state_path.read_text())
        if state['owner'] != actor: raise ValueError('RUN belongs to another Boss')
        if args.note and not rt.IDENT.fullmatch(args.note): raise ValueError('Use a simple note ID')
        for text in [getattr(args, 'reason', ''), args.run, args.note or '']:
            if rt.SECRET.search(text.encode()): raise ValueError('Do not put credentials in task metadata')
    event_id = uuid.uuid4().hex
    with rt.environment(repo) as env:
        tip = fetch(repo, env, rt)
        tasks = board(repo, tip, rt)
        if args.action == 'queue': return dict(summary(tasks), remote_tip=tip)
        for task in tasks:
            if task['status'] == 'pending' or task['note_id'] == args.note:
                checked_source(repo, task)
        handoff = completion = None
        if args.action in {'release', 'block'}:
            target = next((t for t in tasks if t['note_id'] == args.note), None)
            if target is None: raise ValueError('Unknown note ID')
            owned(target, actor, args.run)
            path = safe(repo, args.handoff, repo / 'work' / args.run)
            if not path.read_text().strip(): raise ValueError('Handoff must contain the actual stopping point and next action')
            handoff = {'path': path.relative_to(repo).as_posix(), 'sha256': digest(path)}
            assert_published(repo, tip, {handoff['path']: handoff['sha256']}, rt)
        if args.action == 'submit':
            target = next((t for t in tasks if t['note_id'] == args.note), None)
            if target is None: raise ValueError('Unknown note ID')
            owned(target, actor, args.run)
            if target['status'] != 'claimed': raise ValueError('Claim the task before submitting')
            completion = audit_submission(repo, args, target, rt)
        # Never check out or stage inside the user's working tree.
        with tempfile.TemporaryDirectory(prefix='.notes-transaction-', dir=repo.parent) as temp:
            tx = Path(temp) / 'tx'
            rt.git(repo, 'clone', '--quiet', '--shared', '--no-checkout', str(repo), str(tx), env=env)
            remote = rt.git(repo, 'remote', 'get-url', 'origin').stdout.decode().strip()
            rt.git(tx, 'remote', 'set-url', 'origin', remote)
            for attempt in range(8):
                base = fetch(tx, env, rt)
                run_file = 'runs/' + args.run + '.json'
                registered = rt.git(tx, 'show', base + ':' + run_file, check=False)
                if registered.returncode == 0 and json.loads(registered.stdout)['owner'] != actor:
                    raise ValueError('RUN is registered to another Boss; use a unique RUN from notes init auto')
                tasks = board(tx, base, rt)
                if handoff: assert_published(tx, base, {handoff['path']: handoff['sha256']}, rt)
                if completion:
                    assert_published(tx, base, completion['files'], rt)
                    actual_tree = rt.git(tx, 'rev-parse', base + ':' + completion['workspace']).stdout.decode().strip()
                    if actual_tree != completion['workspace_tree']:
                        raise ValueError('Published evidence workspace changed after audit; inspect and audit the current files')
                changed, selected = transition(tasks, args, actor, event_id, handoff, completion)
                if not changed:
                    commit = base
                    break
                rt.git(tx, 'checkout', '--quiet', '--detach', base)
                for task in changed: write(tx / 'tasks' / (task['note_id'] + '.json'), task)
                write(tx / run_file, {'run': args.run, 'owner': actor})
                rt.git(tx, 'add', '--', 'tasks', run_file)
                rt.git(tx, '-c', 'user.name=Notes Queue', '-c', 'user.email=notes@users.noreply.github.com',
                       'commit', '--quiet', '-m', f'notes {args.action}: ' + ', '.join(t['note_id'] for t in changed))
                commit = rt.git(tx, 'rev-parse', 'HEAD').stdout.decode().strip()
                pushed = rt.git(tx, 'push', '--quiet', 'origin', 'HEAD:refs/heads/' + rt.BRANCH, env=env, check=False)
                observed = fetch(tx, env, rt)
                confirmed = board(tx, observed, rt)
                confirmed_ids = {t['note_id'] for t in confirmed if any(h['event_id'] == event_id for h in t.get('history', []))}
                if confirmed_ids == {t['note_id'] for t in changed}: break
                if pushed.returncode == 0: raise ValueError('Remote task receipt is missing; inspect notes queue before retrying')
                if observed == base:
                    raise ValueError('Task push failed; no remote claim was made. ' + rt.SECRET.sub(b'[REDACTED]', pushed.stderr).decode(errors='replace')[-1000:])
            else: raise ValueError('Queue is busy; retry the same command. No unconfirmed claim may be worked on.')
        synced = rt.sync(repo, env)
    workspace_paths = []
    for task in selected:
        if task['status'] == 'claimed' and task.get('owner') == actor and task.get('run') == args.run:
            path = safe(repo, task['workspace'])
            path.mkdir(parents=True, exist_ok=True)
            assignment = path / 'assignment.json'
            if not assignment.exists(): write(assignment, task)
            workspace_paths.append(task['workspace'])
    local_tasks = board(repo, synced['remote_tip'], rt)
    state['active_notes'] = [t['note_id'] for t in local_tasks if t['status'] == 'claimed' and t.get('owner') == actor and t.get('run') == args.run]
    state['completed_notes'] = [t['note_id'] for t in local_tasks if t['status'] == 'done' and t.get('owner') == actor and t.get('run') == args.run]
    state['blocked_notes'] = [t['note_id'] for t in local_tasks if t['status'] == 'blocked' and t.get('owner') == actor and t.get('run') == args.run]
    state['status'] = 'working' if state['active_notes'] else 'idle'
    state['next_action'] = 'Read the assigned originals and record the exact page/region stopping point; a push is a save, not completion.'
    write(state_path, state)
    return {'status': args.action + '-confirmed' if selected else 'waiting', 'actor': actor,
            'run': args.run, 'commit': commit, 'tasks': selected, 'workspaces': workspace_paths,
            'queue': summary(local_tasks), 'remote_saved': True,
            'next_action': 'Save the RUN checkpoint and assignment files before stopping'}
