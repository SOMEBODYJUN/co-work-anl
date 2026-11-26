#!/usr/bin/env python3
"""Create internal Word-math previews of the two Markdown deliverables.

The preview tests equation, Chinese-font and table layout. It is not an Obsidian
renderer and it never changes the Markdown source or certifies mathematics.
Use the selected primary-runtime Python to run this helper.
"""
from pathlib import Path
import argparse
import hashlib
import json
import os
import subprocess
from zipfile import ZipFile, ZIP_DEFLATED
from lxml import etree

from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor
from docx.enum.style import WD_STYLE_TYPE


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('project', type=Path)
    args = parser.parse_args()
    project = args.project.resolve()
    dest = project / 'audit/layout'
    dest.mkdir(parents=True, exist_ok=True)
    reference = Document()
    for section in reference.sections:
        section.page_width = Inches(8.5)
        section.page_height = Inches(11)
        section.top_margin = section.bottom_margin = Inches(.65)
        section.left_margin = section.right_margin = Inches(.65)
    for style in reference.styles:
        if style.type in (WD_STYLE_TYPE.PARAGRAPH, WD_STYLE_TYPE.CHARACTER):
            style.font.name = 'Noto Serif CJK SC'
            style.font.color.rgb = RGBColor(0, 0, 0)
            fonts = style.element.get_or_add_rPr().find(qn('w:rFonts'))
            if fonts is None:
                fonts = OxmlElement('w:rFonts')
                style.element.get_or_add_rPr().append(fonts)
            fonts.set(qn('w:eastAsia'), 'Noto Serif CJK SC')
    reference.styles['Normal'].font.size = Pt(11)
    reference.styles['Normal'].paragraph_format.space_after = Pt(6)
    reference.styles['Normal'].paragraph_format.line_spacing = 1.12
    for name in ['Quote', 'Intense Quote']:
        reference.styles[name].font.color.rgb = RGBColor(0, 70, 180)
        reference.styles[name].font.italic = False
    for name, color in [('SourceBlank', 'C00000'), ('SourceAnnotation', '0046B4')]:
        style = reference.styles.add_style(name, WD_STYLE_TYPE.CHARACTER)
        style.font.color.rgb = RGBColor.from_string(color)
    ref_path = dest / 'preview-reference.docx'
    reference.save(ref_path)
    lua = dest / 'preview-styles.lua'
    lua.write_text('''function Span(el)
  local color = string.match(el.attributes.style or "", "color:%s*(%a+)")
  if color == "red" then el.attributes["custom-style"] = "SourceBlank" end
  if color == "blue" then el.attributes["custom-style"] = "SourceAnnotation" end
  return el
end
''', encoding='utf-8')
    records = []
    for stem in ['source-transcript', 'study-notes']:
        source = project / (stem + '.md')
        target = dest / (stem + '.docx')
        command = ['pandoc', str(source), '--from=markdown+tex_math_dollars+raw_html',
                   '--to=docx', '--reference-doc=' + str(ref_path),
                   '--lua-filter=' + str(lua), '-o', str(target)]
        done = subprocess.run(command, capture_output=True, text=True)
        records.append({'source':source.name,
                        'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
                        'preview':str(target.relative_to(project)),
                        'returncode':done.returncode,'warnings':done.stderr})
        if done.returncode:
            raise RuntimeError(done.stderr)
        # Pandoc emits ASCII backslash for LaTeX setminus in OMML. The bundled
        # LibreOffice interprets that character as an escape and corrupts the
        # following subscript. Use the identical mathematical Unicode operator
        # only in this internal preview; the Markdown remains untouched.
        with ZipFile(target) as archive:
            members = {item.filename:archive.read(item.filename) for item in archive.infolist()}
        xml = etree.fromstring(members['word/document.xml'])
        math_ns = {'m':'http://schemas.openxmlformats.org/officeDocument/2006/math'}
        repaired = 0
        for node in xml.findall('.//m:t', math_ns):
            if node.text == '\\':
                node.text = '\u2216'
                repaired += 1
        members['word/document.xml'] = etree.tostring(xml,encoding='UTF-8',xml_declaration=True)
        with ZipFile(target,'w',ZIP_DEFLATED) as archive:
            for name,data in members.items():
                archive.writestr(name,data)
        records[-1]['omml_setminus_preview_compatibility_changes'] = repaired
    (dest / 'docx-preview-build.json').write_text(json.dumps({
        'purpose':'Internal layout preview; not the final Markdown renderer',
        'records':records}, ensure_ascii=False, indent=2)+'\n',encoding='utf-8')
    print(json.dumps(records,ensure_ascii=False))


if __name__ == '__main__':
    main()
