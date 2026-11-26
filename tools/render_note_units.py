#!/usr/bin/env python3
"""Render native original-PDF crops for every explicitly authored source unit.

This is evidence preparation only: it does not read an image, choose a glyph,
resolve a record, or create a reviewer. The source PDF is never modified.
"""
from pathlib import Path
import argparse
import hashlib
import json
import re

import fitz


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def contained(project, relative):
    path = (project / relative).resolve()
    if not path.is_relative_to(project):
        raise ValueError('all crop inputs and outputs must remain inside the project')
    return path


def render(project, sources_path, output, dpi, padding):
    manifest_path = project / 'manifest.json'
    manifest = read(manifest_path)
    pdf_path = contained(project, manifest['source_pdf']['path'])
    pdf_sha = sha(pdf_path)
    if pdf_sha != manifest['source_pdf']['sha256']:
        raise ValueError('source PDF hash differs from the original manifest')
    source_data = read(sources_path)
    if isinstance(source_data, list):
        sources = source_data
    elif 'source_units' in source_data:
        sources = source_data['source_units']
    else:
        sources = source_data['sources']
    if not sources or len({s['id'] for s in sources}) != len(sources):
        raise ValueError('the actual source-unit inventory must be nonempty and unique')
    if output.exists():
        raise ValueError('use a new output directory to preserve prior evidence bytes')
    pages = {page['id']: page for page in manifest['pages']}
    prepared = []
    for source in sources:
        identifier = source['id']
        if not re.fullmatch(r'[A-Za-z0-9_-]+', identifier):
            raise ValueError('source-unit ID is not safe as an evidence filename')
        page = pages[source['page_id']]
        x0, y0, x1, y1 = source['bbox_px']
        if not (0 <= x0 < x1 <= page['width_px'] and
                0 <= y0 < y1 <= page['height_px']):
            raise ValueError('source-unit bounds lie outside the manifest page: ' + identifier)
        box = [max(0, x0 - padding), max(0, y0 - padding),
               min(page['width_px'], x1 + padding), min(page['height_px'], y1 + padding)]
        prepared.append((source, page, box))
    output.mkdir(parents=True)
    crops = []
    with fitz.open(pdf_path) as document:
        for source, page, box in prepared:
            path = output / (source['id'] + f'-{dpi}.png')
            clip = fitz.Rect([v * 72 / manifest['render']['dpi'] for v in box])
            document[page['number'] - 1].get_pixmap(dpi=dpi, clip=clip, alpha=False).save(path)
            crops.append({'source_unit_id': source['id'], 'page_id': source['page_id'],
                          'bbox_px': box, 'dpi': dpi,
                          'path': path.relative_to(project).as_posix(), 'sha256': sha(path)})
    if sha(pdf_path) != pdf_sha:
        raise RuntimeError('the original PDF changed while rendering evidence')
    result = {'source_pdf_sha256': pdf_sha, 'manifest_sha256': sha(manifest_path),
              'source_inventory': sources_path.relative_to(project).as_posix(),
              'source_inventory_sha256': sha(sources_path), 'baseline_padding_px': padding,
              'purpose': 'Native source-unit evidence for actual independent model reading; generation does not constitute a reading.',
              'crops': crops, 'content_decisions_generated': False}
    index = output / 'crop-index.json'
    index.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'native_original_pdf_crops': len(crops), 'dpi': dpi,
                      'index': str(index), 'source_pdf_unchanged': True,
                      'content_decisions_generated': False}, ensure_ascii=False))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('project', type=Path)
    parser.add_argument('--sources', default='ledger.json', help='Project-relative ledger, content plan, or source-unit array')
    parser.add_argument('--out', required=True, help='New project-relative evidence directory')
    parser.add_argument('--dpi', type=int, choices=[800, 1200], default=800)
    parser.add_argument('--padding', type=int, default=20, help='Margin in manifest baseline pixels')
    args = parser.parse_args()
    if not 0 <= args.padding <= 200:
        parser.error('padding must be between 0 and 200 baseline pixels')
    root = args.project.resolve()
    render(root, contained(root, args.sources), contained(root, args.out), args.dpi, args.padding)
