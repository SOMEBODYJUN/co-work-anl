#!/usr/bin/env python3
"""Index explicitly named, already-existing note evidence without reading it.

This utility creates only artifact metadata. It makes no visual, mathematical,
candidate-selection or completion decisions. Original-PDF crop authenticity is
checked independently by the note auditor.
"""
from pathlib import Path
import argparse
import hashlib
import json
import re


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def catalog(project, inputs):
    project = project.resolve()
    records, paths, identifiers = [], {}, set()

    def contained(relative):
        path = (project / relative).resolve()
        if not path.is_relative_to(project) or not path.is_file():
            raise ValueError('evidence must already exist inside the current project: ' + relative)
        return path

    def register(relative, image=None, expected_hash=None, preferred_id=None):
        path = contained(relative)
        relative = path.relative_to(project).as_posix()
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if expected_hash and digest != expected_hash:
            raise ValueError('crop-index hash differs from actual file: ' + relative)
        if relative in paths:
            prior = next(item for item in records if item['id'] == paths[relative])
            if image is not None and prior.get('source_crop') != image:
                raise ValueError('conflicting declarations for one crop: ' + relative)
            return paths[relative]
        slug = re.sub('[^a-zA-Z0-9_-]+', '-', str(Path(relative).with_suffix(''))).strip('-')
        identifier = preferred_id or ('ev-' + slug[-88:] + '-' + hashlib.sha256(relative.encode()).hexdigest()[:8])
        if identifier in identifiers:
            raise ValueError('duplicate evidence identifier: ' + identifier)
        record = {'id': identifier, 'path': relative, 'sha256': digest,
                  'kind': 'evidence', 'format': 'image' if image else 'text'}
        if image:
            record['source_crop'] = image
        else:
            if not path.read_text(encoding='utf-8').strip():
                raise ValueError('empty textual evidence: ' + relative)
        records.append(record)
        identifiers.add(identifier)
        paths[relative] = identifier
        return identifier

    for item in inputs['text_files']:
        if isinstance(item, str):
            register(item)
        else:
            register(item['path'], preferred_id=item['id'])
    for relative in inputs.get('crop_indexes', []):
        register(relative)
        entries = read(contained(relative))
        if isinstance(entries, dict):
            entries = entries['crops']
        for item in entries:
            crop = {key: item[key] for key in ['page_id', 'bbox_px', 'dpi']}
            if not isinstance(crop['dpi'], int) or not 72 <= crop['dpi'] <= 1200:
                raise ValueError('a crop must declare its actual original-PDF rendering dpi')
            if len(crop['bbox_px']) != 4:
                raise ValueError('a crop needs the four manifest-resolution bbox coordinates')
            register(item['path'], crop, item['sha256'])
    return {'evidence_artifacts': records,
            'path_to_evidence_id': {key: 'artifact:' + value for key, value in paths.items()},
            'content_decisions_generated': False}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('project', type=Path)
    parser.add_argument('--inputs', required=True, help='Project-relative JSON with text_files and crop_indexes')
    parser.add_argument('--out', default='audit/evidence-catalog.json')
    args = parser.parse_args()
    root = args.project.resolve()
    source, destination = (root / args.inputs).resolve(), (root / args.out).resolve()
    if not source.is_relative_to(root) or not destination.is_relative_to(root):
        raise ValueError('input and output must remain inside the current project')
    result = catalog(root, read(source))
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'artifacts': len(result['evidence_artifacts']),
                      'images': sum(x['format'] == 'image' for x in result['evidence_artifacts']),
                      'content_decisions_generated': False}, ensure_ascii=False))
