#!/usr/bin/env python3
"""Check a full offline teaching export against its recorded source files."""
import hashlib
import json
from pathlib import Path
import re
import sys
from collections import Counter
from lxml import html


def main():
    export = Path(sys.argv[1]).resolve()
    repo = Path(__file__).resolve().parents[1]
    report = json.loads(Path(str(export) + '.audit.json').read_text())
    content = export.read_text()
    tree = html.fromstring(content)
    errors = []
    sources = report['sources']
    for source in sources:
        data = (repo / source['path']).read_bytes()
        if len(data) != source['bytes'] or hashlib.sha256(data).hexdigest() != source['sha256']:
            errors.append('Source changed since export: ' + source['path'])
    expected = {m['path'] for m in json.loads((repo / 'learning/manifest.json').read_text())['modules']}
    actual = {s['path'] for s in sources}
    if actual != expected:
        errors.append(f'Source coverage differs from manifest: missing={expected-actual}, extra={actual-expected}')
    counts = Counter(tree.xpath('//*[@id]/@id'))
    errors += ['Duplicate ID: ' + i for i, count in counts.items() if count > 1]
    for href in tree.xpath('//a/@href'):
        if href.startswith('#') and href[1:] not in counts:
            errors.append('Missing anchor: ' + href)
    annotations = tree.xpath('//annotation[@encoding="application/x-tex"]')
    if len(annotations) != report['equations']:
        errors.append(f'Math coverage: {len(annotations)} rendered, {report["equations"]} recorded')
    if report['mathErrors'] or tree.xpath('//*[contains(concat(" ",normalize-space(@class)," ")," katex-error ")]'):
        errors.append('Math render errors remain')
    if report['sectionFallbacks']:
        errors.append('Heading links fell back to chapter entry')
    for node in tree.xpath('//script[@src] | //link[@href] | //img[@src]'):
        resource = node.get('src') or node.get('href')
        if not resource.startswith('data:'):
            errors.append('External display resource: ' + resource)
    for resource in re.findall(r'url\(([^)]+)\)', content):
        if not resource.strip('"\' ').startswith('data:'):
            errors.append('External CSS resource: ' + resource)
    # A display-math delimiter left in ordinary prose means the reader sees raw TeX.
    for node in tree.xpath('//script | //style | //pre | //code | //*[contains(concat(" ",normalize-space(@class)," ")," katex ")]'):
        if node.getparent() is not None:
            node.drop_tree()
    visible = tree.text_content()
    if '$$' in visible or re.search(r'\\\[|\\\]', visible):
        errors.append('Unrendered display math remains in ordinary text')
    if errors:
        print('\n'.join(errors))
        raise SystemExit(1)
    print(json.dumps({'sources':len(sources), 'equations':len(annotations), 'uniqueAnchors':len(counts),
                      'mathErrors':0, 'sectionFallbacks':0, 'externalDisplayResources':0}, ensure_ascii=False))


if __name__ == '__main__':
    main()
