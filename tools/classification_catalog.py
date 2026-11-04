"""Combine already-read, exact-version material records into a numbered catalogue.

This is an export operation. It never classifies text, edits source material,
executes a recommended route, registers a Boss, or claims a mathematical task.
"""
from __future__ import annotations

import argparse
import collections
import csv
import hashlib
import json
import os
from pathlib import Path

import curation
import triage


LABELS = {
    'math-exposition': '数学正文', 'numeric-witness': '数值见证待理解',
    'math-fragment': '数学片段缺入口', 'algorithm-result': '独立算法成果',
    'evidence-only': '计算或证据材料', 'non-math': '非数学材料',
    'mixed/needs-context': '混合或待上下文',
}
ROUTE_LABELS = {
    'retain': '沿用', 'distill': '第二步理解与蒸馏',
    'restore': '第二步定向恢复', 'extract': '第二步提取数学',
    'attach': '建议第二步评估附件用途', 'delete': '建议第二步评估清退',
    'clarify': '第二步澄清上下文',
}


def cell(value):
    return str(value).replace('\n', ' ').replace('|', '\\|')


def build(root, source_runs, output, corrections=None):
    root = root.resolve()
    if not output.startswith('curation/catalogs/'):
        raise ValueError('Catalogue output belongs in curation/catalogs/')
    home = curation._safe_path(root, output)
    if home.exists():
        raise ValueError('Catalogue already exists; preserve its numbering and snapshot')
    if not source_runs or len(set(source_runs)) != len(source_runs):
        raise ValueError('Distinct source runs are required in chronological order')
    snapshot = curation.scan(root)
    snapshot.pop('status')
    snapshot['commit'] = curation._git(root, 'rev-parse', 'HEAD').decode().strip()
    curation._check_snapshot(root, snapshot)
    lookup, history, order = {}, collections.defaultdict(list), []
    for run in source_runs:
        source_home, source_snapshot = triage.load(root, run)
        for original in sorted(source_snapshot['files'], key=lambda row: row['path']):
            path = original['path']
            if path not in history:
                order.append(path)
            record_path = source_home/'records'/f"{original['material_id']}.json"
            record = json.loads(record_path.read_text())
            triage.validate_record(record)
            if record['path'] != path or record['sha256'] != original['sha256']:
                raise ValueError('Source record does not match its frozen material: ' + path)
            record_name = record_path.relative_to(root).as_posix()
            lookup[(path, record['sha256'])] = (record, record_name)
            history[path].append({'run': run, 'record': record_name,
                                  'sha256': record['sha256'], 'category': record['category']})
    overrides = {}
    if corrections:
        records = json.loads(curation._safe_path(root, corrections).read_text())
        if not isinstance(records, list):
            raise ValueError('Corrections must contain a list of manually read records')
        for record in records:
            triage.validate_record(record)
            if record['path'] in overrides:
                raise ValueError('Duplicate manual correction: ' + record['path'])
            overrides[record['path']] = record
    originals = {row['path']: row for row in snapshot['files']}
    if set(originals) != set(order):
        raise ValueError('Current formal paths and previously read paths differ; read the increment first')
    if overrides.keys() - originals.keys():
        raise ValueError('Correction is outside the material catalogue')
    rows = []
    for serial, path in enumerate(order, 1):
        original = originals[path]
        prior = lookup.get((path, original['sha256']))
        if prior is None:
            raise ValueError('No exact-version reading record: ' + path)
        record, source = prior
        if path in overrides:
            record, source = overrides[path], corrections
            if record['sha256'] != original['sha256']:
                raise ValueError('Manual correction binds an outdated version: ' + path)
        rows.append(dict(record, display_id=f'P25-{serial:05d}',
                         material_id=hashlib.sha256(path.encode()).hexdigest()[:20],
                         category_label=LABELS[record['category']],
                         route_label=ROUTE_LABELS[record['route']],
                         classification_source=source, source_versions=history[path]))
    counts = collections.Counter(row['category'] for row in rows)
    report = {'version': 1, 'operation_mode': 'classification-only',
              'snapshot_commit': snapshot['commit'], 'materials': len(rows),
              'classified': len(rows), 'unclassified': 0,
              'source_runs': source_runs, 'manual_corrections': len(overrides),
              'categories': dict(counts), 'source_changes_performed_by_export': 0,
              'numbering': 'First source snapshot sorted by path; later new paths append. Numbers identify material rows, not mathematical objects.',
              'routes': 'Recommendations only; no deletion, move, merge, rewrite, or graph admission.'}
    home.mkdir(parents=True)
    triage.write(home/'snapshot.json', snapshot)
    triage.write(home/'summary.json', report)
    triage.write(home/'materials.json', rows)
    mathematics = [row for row in rows if row['category'] not in {'non-math', 'evidence-only'}]
    candidates = [row for row in rows if row['route'] in {'distill', 'restore', 'extract', 'clarify'}]
    triage.write(home/'mathematics.json', mathematics)
    triage.write(home/'stage2-candidates.json', candidates)
    triage.write(home/'evidence-and-nonmath.json', [row for row in rows if row['category'] in {'non-math', 'evidence-only'}])
    fields = ['display_id', 'material_id', 'path', 'sha256', 'category', 'category_label',
              'math_subject_or_nonmath_reason', 'locator', 'route', 'route_label', 'classification_source']
    with (home/'materials.csv').open('w', encoding='utf-8-sig', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, lineterminator='\n')
        writer.writeheader()
        writer.writerows({key: row[key] for key in fields} for row in rows)
    archives = collections.defaultdict(list)
    categories = collections.defaultdict(list)
    for row in rows:
        archives[triage.PurePathArchive(row['path'])].append(row)
        categories[row['category']].append(row)
    for folder, groups in [('by-archive', archives), ('by-category', categories)]:
        for name, items in groups.items():
            page = home/folder/(name.replace('/', '-') + '.md')
            page.parent.mkdir(parents=True, exist_ok=True)
            lines = [f'# {LABELS.get(name, name)} 材料目录', '',
                     '只登记性质；建议去向未执行。编号是本目录材料行号，不是数学对象身份。', '',
                     '| 编号 | 原材料 | 类别 | 具体理由 | 文内定位 | 后续建议 |',
                     '| --- | --- | --- | --- | --- | --- |']
            for row in items:
                link = os.path.relpath(root/row['path'], page.parent)
                lines.append('| ' + ' | '.join([
                    row['display_id'], f"[{cell(Path(row['path']).stem)}](<{link}>)",
                    LABELS[row['category']], cell(row['math_subject_or_nonmath_reason']),
                    cell(row['locator']), ROUTE_LABELS[row['route']]]) + ' |')
            page.write_text('\n'.join(lines)+'\n')
    lines = ['# 2.5 第一步：完整编号分类目录', '',
             f"**{len(rows):,} / {len(rows):,} 份已登记，未分类 0。** 本目录只定性、编号和分流；未执行任何建议去向，不审定数学真值，不登记超边。", '',
             f"材料快照：`{snapshot['commit']}`。复用既有逐份实读记录，严格按路径与 SHA256 匹配，并合入定向补读的分类更正。", '',
             '[完整编号表 CSV](materials.csv) · [JSON](materials.json) · [数学及待抽取材料](mathematics.json) · [第二步候选](stage2-candidates.json) · [证据和非数学目录](evidence-and-nonmath.json)', '',
             '| 类别 | 份数 |', '| --- | ---: |']
    for category in LABELS:
        lines.append(f"| [{LABELS[category]}](by-category/{category.replace('/', '-')}.md) | {counts[category]} |")
    lines += ['', '按研究存档浏览：', '']
    lines.extend(f'- [{name}](by-archive/{name}.md)：{len(items)} 份。' for name, items in sorted(archives.items()))
    lines += ['', '旧运行中的清理动作仅为历史记录；本轮已恢复其原页面及链接。当前目录链接始终指向原材料。原始证据附件也保留。', '',
              '编号先按首轮 4,608 份固定顺序分配，再给 11 份新增材料追加编号；同路径的版本记录保存在 JSON 的 source_versions 中。', '',
              '[第二步唯一完整提示词](../../../prompts/02.5-2-distill.txt) · [操作手册](../../../research/CURATION_OPERATIONS.md)']
    (home/'INDEX.md').write_text('\n'.join(lines)+'\n')
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--source-runs', nargs='+', required=True)
    parser.add_argument('--out', required=True)
    parser.add_argument('--corrections')
    args = parser.parse_args()
    try:
        report = build(args.repo, args.source_runs, args.out, args.corrections)
    except (ValueError, OSError, KeyError, json.JSONDecodeError) as exc:
        raise SystemExit(str(exc))
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
