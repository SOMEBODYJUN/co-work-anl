"""Inspect exact script/data bytes and active resource declarations. This is never a browser verdict."""
import argparse
import hashlib
from html.parser import HTMLParser
import json
import re
from pathlib import Path
HERE = Path(__file__).resolve().parent
AUTHOR = HERE.parent / 'household_engine'
p = argparse.ArgumentParser()
p.add_argument('--html', default=AUTHOR / 'calculator.html', type=Path)
p.add_argument('--scenarios', type=Path, default=AUTHOR / 'scenarios.json')
args = p.parse_args()

class Document(HTMLParser):

    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.scripts = []
        self.ext = []
        self.csp = None
        self.script = None
        self.styles = []
        self.style = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'script':
            self.script = {'id': a.get('id'), 'type': a.get('type'), 'text': ''}
            self.scripts.append(self.script)
        if tag == 'style':
            self.style = True
        if tag == 'meta' and a.get('http-equiv', '').lower() == 'content-security-policy':
            self.csp = a.get('content')
        for k in ['src', 'href', 'action', 'poster', 'srcset']:
            if k in a and re.search('(?:https?:)?//', a[k]):
                self.ext.append([tag, k, a[k]])

    def handle_data(self, data):
        if self.script:
            self.script['text'] += data
        if self.style:
            self.styles.append(data)

    def handle_endtag(self, tag):
        if tag == 'script':
            self.script = None
        if tag == 'style':
            self.style = False
sha = lambda x: hashlib.sha256(x).hexdigest()
html = args.html.read_bytes()
doc = Document()
doc.feed(html.decode())
scripts = [s for s in doc.scripts if s['type'] != 'application/json']
blobs = {s['id']: json.loads(s['text']) for s in doc.scripts if s['type'] == 'application/json'}
source_data = json.loads(args.scenarios.read_text())
target = source_data.get('scenarios') if isinstance(source_data, dict) else source_data
items = {'embedded_engine_byte_identical_to_node_tested_source': scripts[0]['text'].encode() == (AUTHOR / 'engine.js').read_bytes(), 'embedded_ui_byte_identical_to_reviewed_source': scripts[1]['text'].encode() == (AUTHOR / 'ui.js').read_bytes(), 'embedded_scenario_records_match_expected_source': blobs['scenario-data'] == target, 'embedded_demo_matches_explicit_synthetic_file': blobs['example-data'] == json.loads((AUTHOR / 'synthetic_household.json').read_text()) and blobs['example-data']['dataKind'] == 'synthetic_example', 'attribute_level_external_inclusions': doc.ext, 'stylesheet_external_imports': re.findall('@import|url\\(\\s*[\\\'"]?(?:https?:)?//', ''.join(doc.styles), re.I), 'execution_source_network_api_calls': re.findall('\\b(?:fetch|XMLHttpRequest|WebSocket|EventSource|sendBeacon|importScripts)\\s*\\(', ''.join((s['text'] for s in scripts))), 'inline_CSP_forbids_connect': "connect-src 'none'" in (doc.csp or '')}
res = {'scope': 'static packaging and byte equality only; no browser, network event, layout, screenshot or download observed', 'html': str(args.html), 'sha256': sha(html), 'scriptCount': len(scripts), 'embeddedEngineSha256': sha(scripts[0]['text'].encode()), 'embeddedUiSha256': sha(scripts[1]['text'].encode()), 'checked': items}
(HERE / 'packaging_report.json').write_text(json.dumps(res, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(res, ensure_ascii=False))
raise SystemExit(0 if all((x is True or x == [] for x in items.values())) else 1)
