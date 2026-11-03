"""Lossless record indexing; no original solver, LP, BI, or random search."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
HERE = Path(__file__).resolve().parent
RAW = ROOT / 'cleanup/workspaces/Boss7/resume-current-20261102/raw'
IDS = ['86baaa948961a2dcdb57', '70b13b2c9d0ce481c738',
       '6249d81b166c8d2b4b87', '56bd7b24afb2d39b51b5']


def main():
    manifest = json.loads((RAW.parent / 'raw-manifest.json').read_text())
    sources = [next(r for r in manifest if r['id'] == i) for i in IDS]
    indexed = []
    for src in sources:
        raw = (RAW / src['id']).read_bytes()
        assert len(raw) == src['size']
        assert hashlib.sha256(raw).hexdigest() == src['sha256']
        name = Path(src['path']).name
        (HERE / 'original' / name).write_bytes(raw)
        data = json.loads(raw)
        groups, seen = [], {}
        for loc, record in [('best', data['best'])] + [
                (f'bank/{i}', r) for i, r in enumerate(data['bank'])]:
            key = json.dumps(record, sort_keys=True, separators=(',', ':'))
            if key not in seen:
                seen[key] = len(groups)
                groups.append({'locations': [], 'record': record})
            groups[seen[key]]['locations'].append(loc)
        all_records = [data['best'], *data['bank']]
        indexed.append({
            'id': src['id'], 'name': name,
            'root_fields_except_records': {k: v for k, v in data.items()
                                          if k not in ('best', 'bank')},
            'root_field_order': list(data), 'record_groups': groups,
            'record_count_including_best': len(all_records),
            'distinct_record_count': len(groups),
            'distinct_weight_count': len({tuple(r['weights']) for r in all_records}),
            'best_equal_bank0': data['best'] == data['bank'][0],
            'customer_totals': sorted({sum(r['weights']) for r in all_records}),
            'universal_multiplicities': sorted({r['weights'][-1] for r in all_records}),
            'record_field_sets': sorted({tuple(r) for r in all_records}),
        })
        # Reconstitute every original semantic record, including duplicates/order.
        restored = {}
        for g in groups:
            for loc in g['locations']:
                restored[loc] = g['record']
        assert restored['best'] == data['best']
        assert [restored[f'bank/{i}'] for i in range(len(data['bank']))] == data['bank']
    (HERE / 'source-manifest.json').write_text(
        json.dumps(sources, ensure_ascii=False, indent=2) + '\n')
    (HERE / 'complete-record-read-index.json').write_text(
        json.dumps(indexed, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps([{k: v for k, v in r.items() if k not in
                      ('record_groups', 'record_field_sets')} for r in indexed],
                     ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
