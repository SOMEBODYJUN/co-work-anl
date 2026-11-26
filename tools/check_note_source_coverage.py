#!/usr/bin/env python3
"""Locate dark source pixels outside the authored source-unit rectangles.

This geometric diagnostic cannot determine whether a word was read, whether a
rectangle is meaningful, or whether the transcription is correct. Every gap
still needs actual visual inspection; the tool never expands or creates units.
"""
from pathlib import Path
import argparse
import json
import numpy as np
from PIL import Image
from scipy import ndimage


def check(project, source_path, threshold):
    manifest = json.loads((project / 'manifest.json').read_text(encoding='utf-8'))
    data = json.loads(source_path.read_text(encoding='utf-8'))
    sources = data['source_units'] if isinstance(data, dict) and 'source_units' in data else data
    if isinstance(sources, dict):
        sources = sources['sources']
    result = []
    for page in manifest['pages']:
        with Image.open(project / page['image']['path']) as image:
            ink = np.asarray(image.convert('L')) < threshold
        covered = np.zeros(ink.shape, dtype=bool)
        for unit in sources:
            if unit['page_id'] == page['id']:
                x0, y0, x1, y1 = unit['bbox_px']
                covered[y0:y1, x0:x1] = True
        gaps = ink & ~covered
        labels, count = ndimage.label(gaps, structure=np.ones((3, 3), dtype=int))
        sizes = np.bincount(labels.ravel())
        components = []
        for number, slices in enumerate(ndimage.find_objects(labels), 1):
            if slices is None:
                continue
            y, x = slices
            components.append({'bbox_px': [x.start, y.start, x.stop, y.stop],
                               'dark_pixels': int(sizes[number])})
        result.append({'page_id': page['id'], 'dark_pixels': int(ink.sum()),
                       'uncovered_dark_pixels': int(gaps.sum()),
                       'components': components})
    return {'threshold': threshold, 'bbox_convention': 'half-open integer manifest-pixel coordinates',
            'pages': result, 'uncovered_dark_pixels': sum(x['uncovered_dark_pixels'] for x in result),
            'visual_or_mathematical_correctness_proven': False, 'records_modified': False}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('project', type=Path)
    parser.add_argument('--sources', default='ledger.json', help='Project-relative ledger or sources array')
    parser.add_argument('--threshold', type=int, default=225)
    parser.add_argument('--out', help='Optional project-relative JSON diagnostic output')
    args = parser.parse_args()
    project = args.project.resolve()
    source = (project / args.sources).resolve()
    if not source.is_relative_to(project) or not 1 <= args.threshold <= 255:
        raise ValueError('invalid current-project source or grayscale threshold')
    result = check(project, source, args.threshold)
    if args.out:
        destination = (project / args.out).resolve()
        if not destination.is_relative_to(project):
            raise ValueError('diagnostic output must remain inside the current project')
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result, ensure_ascii=False, indent=2))
