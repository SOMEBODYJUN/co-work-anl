#!/usr/bin/env python3
"""Render one explicitly selected crop directly from the registered source PDF.

Coordinates use the manifest's base DPI. The output and index are evidence,
not a reading or a recovery decision; the model must still open the PNG.
"""
from pathlib import Path
import argparse
import hashlib
import json
import fitz


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def render(project, page_id, bbox, dpi, output, index):
    project = project.resolve()
    manifest = json.loads((project / 'manifest.json').read_text(encoding='utf-8'))
    source = (project / manifest['source_pdf']['path']).resolve()
    destination, index_path = (project / output).resolve(), (project / index).resolve()
    for path in [source, destination, index_path]:
        if not path.is_relative_to(project):
            raise ValueError('all paths must remain inside the current project')
    if sha(source) != manifest['source_pdf']['sha256']:
        raise ValueError('registered original PDF hash differs')
    page = next(p for p in manifest['pages'] if p['id'] == page_id)
    if not (0 <= bbox[0] < bbox[2] <= page['width_px'] and
            0 <= bbox[1] < bbox[3] <= page['height_px']):
        raise ValueError('crop must lie inside the selected original page')
    if destination.suffix.lower() != '.png':
        raise ValueError('source evidence is written as a lossless PNG')
    clip = fitz.Rect(*(x * 72.0 / manifest['render']['dpi'] for x in bbox))
    with fitz.open(source) as document:
        pix = document[page['number'] - 1].get_pixmap(dpi=dpi, clip=clip,
                                                    colorspace=fitz.csRGB, alpha=False)
        data = pix.tobytes('png')
    if destination.exists() and destination.read_bytes() != data:
        raise ValueError('refusing to replace a different existing evidence image')
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(data)
    entry = {'id': destination.stem, 'page_id': page_id, 'bbox_px': bbox, 'dpi': dpi,
             'path': destination.relative_to(project).as_posix(), 'sha256': sha(destination),
             'source_pdf_sha256': manifest['source_pdf']['sha256']}
    inventory = json.loads(index_path.read_text(encoding='utf-8')) if index_path.exists() else []
    entries = inventory['crops'] if isinstance(inventory, dict) else inventory
    prior = next((x for x in entries if x['path'] == entry['path']), None)
    if prior:
        if any(prior.get(k) != entry[k] for k in ['page_id', 'bbox_px', 'dpi', 'sha256']):
            raise ValueError('existing crop-index declaration differs')
    else:
        entries.append(entry)
    index_path.parent.mkdir(parents=True, exist_ok=True)
    index_path.write_text(json.dumps(inventory, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return entry


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('project', type=Path)
    parser.add_argument('--page', required=True)
    parser.add_argument('--bbox', nargs=4, type=int, required=True)
    parser.add_argument('--dpi', type=int, choices=[800, 1200], default=800)
    parser.add_argument('--out', required=True, help='Project-relative PNG path')
    parser.add_argument('--index', required=True, help='Project-relative crop-index JSON path')
    args = parser.parse_args()
    print(json.dumps(render(args.project, args.page, args.bbox, args.dpi, args.out, args.index),
                     ensure_ascii=False, indent=2))
