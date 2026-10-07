#!/usr/bin/env python3
"""Check a full offline teaching export against its recorded source files."""
import hashlib
import json
from pathlib import Path
import re
import sys
from collections import Counter
from lxml import html


def source_formulas(text):
    text = re.sub(r'```[\s\S]*?```', '', text)
    text = re.sub(r'`[^`\n]*`', '', text)
    pattern = r'\$\$\s*([\s\S]*?)\$\$|\\\[\s*([\s\S]*?)\\\]|\$(?!\$)([^$\n]+?)\$(?!\$)|\\\(([\s\S]*?)\\\)'
    return [next(g for g in match.groups() if g is not None) for match in re.finditer(pattern, text)]


def render_normalization(tex):
    tex = re.sub(r'\\mspace\{([+-]?[\d.]+)mu\}', r'\\mkern\1mu', tex)
    tex = tex.replace(r'\tag{SPE_\alpha}', r'\tag{$\mathrm{SPE}_\alpha$}')
    if r'\begin{split}' in tex and any(line.count('&') > 1 for line in tex.splitlines()):
        tex = tex.replace(r'\begin{split}', r'\begin{aligned}').replace(r'\end{split}', r'\end{aligned}')
    return tex.strip()


def main():
    export = Path(sys.argv[1]).resolve()
    repo = Path(__file__).resolve().parents[1]
    report = json.loads(Path(str(export) + '.audit.json').read_text())
    content = export.read_text()
    tree = html.fromstring(content)
    errors = []
    sources = report['sources']
    for index, source in enumerate(sources):
        data = (repo / source['path']).read_bytes()
        if len(data) != source['bytes'] or hashlib.sha256(data).hexdigest() != source['sha256']:
            errors.append('Source changed since export: ' + source['path'])
        expected_math = Counter(render_normalization(tex) for tex in source_formulas(data.decode()))
        section = tree.xpath(f'//section[@id="source-{index}"]')
        if len(section) != 1:
            errors.append('Missing source section: ' + source['path'])
            continue
        rendered_math = Counter((a.text or '').strip() for a in section[0].xpath('.//annotation[@encoding="application/x-tex"]'))
        if expected_math != rendered_math:
            errors.append('Source formulas differ from rendered formulas: ' + source['path'] +
                          f' missing={list((expected_math-rendered_math).elements())[:4]!r}' +
                          f' extra={list((rendered_math-expected_math).elements())[:4]!r}')
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
    if re.search(r'\*\*[^*\n]+\*\*', visible):
        errors.append('Unrendered strong-emphasis markers remain in ordinary text')
    if errors:
        print('\n'.join(errors))
        raise SystemExit(1)
    print(json.dumps({'sources':len(sources), 'equations':len(annotations), 'uniqueAnchors':len(counts),
                      'mathErrors':0, 'sectionFallbacks':0, 'externalDisplayResources':0}, ensure_ascii=False))


if __name__ == '__main__':
    main()
