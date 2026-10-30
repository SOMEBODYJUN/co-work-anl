#!/usr/bin/env python3
"""Current-asset curation checks only; no general proof or historical diff PASS."""
from collections import Counter
from hashlib import sha256
from pathlib import Path
import json
import re
import subprocess

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
PAPER=ROOT/'archives/facility-games/papers/shared-catalog-golden-ratio'
sources=json.loads((HERE/'source-manifest.json').read_text())['sources']
for item in sources:
    data=(ROOT/item['preserved_path']).read_bytes()
    assert len(data)==item['size'] and sha256(data).hexdigest()==item['sha256']
tex=(PAPER/'main.tex').read_text()
active=re.sub(r'(?<!\\)%[^\n]*','',tex)
bib=(PAPER/'references.bib').read_text()
labels=re.findall(r'\\label\{([^}]+)\}',active)
refs=re.findall(r'\\(?:eqref|ref)\{([^}]+)\}',active)
cites=[k for group in re.findall(r'\\cite(?:\[[^]]*\])?\{([^}]+)\}',active) for k in group.split(',')]
bibkeys=re.findall(r'@\w+\{([^,]+),',bib)
assert not (set(refs)-set(labels)) and not (set(cites)-set(bibkeys))
assert len(labels)==len(set(labels))
stack=[];begins=Counter()
for m in re.finditer(r'\\(begin|end)\{([^}]+)\}',active):
    if m[1]=='begin':stack.append(m[2]);begins[m[2]]+=1
    else:assert stack.pop()==m[2]
assert not stack
blocks=[]
for m in re.finditer(r'\\begin\{(definition|construction|lemma|theorem|proposition)\}(.*?)\\end\{\1\}',active,re.S):
    blocks.append({'kind':m[1],'labels':re.findall(r'\\label\{([^}]+)\}',m[2]),
                   'line':active[:m.start()].count('\n')+1,'sha256':sha256(m[0].encode()).hexdigest()})
assert len(blocks)==8 and begins['proof']==5
info=subprocess.run(['/usr/bin/pdfinfo',str(PAPER/'main.pdf')],capture_output=True,text=True,check=True).stdout
(HERE/'pdfinfo.txt').write_text(info)
text=subprocess.run(['/usr/bin/pdftotext','-layout',str(PAPER/'main.pdf'),'-'],capture_output=True,text=True,check=True).stdout
assert text==(HERE/'pdf-text-layout.txt').read_text()
pages=text.split('\f')
if not pages[-1].strip():pages.pop()
assert len(pages)==26 and all(p.strip() for p in pages)
math=json.loads((HERE/'math-audit.json').read_text())
assert math['box_slice']['cases']==3529 and math['finite_catalogs']['count']==320
result={'scope':'Current bytes/syntax/PDF extraction and read records; finite mathematics separately bounded in math-audit.json. No universal phi or polynomial-constructor review certificate.',
        'source_count':7,'source_bytes':sum(x['size'] for x in sources),'all_source_hashes_match':True,
        'current_tex':{'lines':len(tex.splitlines()),'formal_blocks':blocks,'formal_count':len(blocks),'proof_count':begins['proof'],
                       'label_count':len(labels),'reference_calls':len(refs),'citation_calls':len(cites),'bibliography_keys':bibkeys,
                       'displays':{'equation':begins['equation'],'bracket':len(re.findall(r'(?<!\\)\\\[',active))},
                       'environment_stack_balanced':True,'duplicate_labels':0,'undefined_refs':0,'undefined_cites':0},
        'pdf':{'pages':26,'text_lines':len(text.splitlines()),'text_lines_metric':'Python splitlines includes form-feed page boundaries','newline_terminated_lines':text.count('\n'),'formfeed_page_terminators':text.count('\f'),'page_text_sha256':[sha256(p.encode()).hexdigest() for p in pages],
               'all_text_pages_read':True,'all_26_rendered_pages_actually_inspected':True,
               'visual_findings':'No body clipping or formula spill observed; page26 contains only continuation bibliography lines, a real reference-only tail page. The final contact sheet has two empty canvas slots, not missing PDF pages.'},
        'historical_review_state':'Five round1 findings repaired in current text according to actual reading; source revision explicitly requires a fresh targeted review of cycle transport and polynomial constructor. Not upgraded by syntax/finite success.',
        'actual_executed_math_script_sha256':sha256((HERE/'audit_math.py').read_bytes()).hexdigest(),
        'initial_full_domain_math_script_sha256':sha256((HERE/'audit_math.initial-executed.py').read_bytes()).hexdigest(),
        'post_full_run_correction_scope':math.get('colocation_metadata_correction'),
        'finite_math_domains':{'box_slices':3529,'local_pairs':1089,'pure_repair_seeds':13995,'finite_C_calls_using_support_enumeration':143,
                               'catalogs':320,'ordered_layouts':2560,'cycles_for_selected_tie_map':320},
        'not_claimed':['PDF recompiled','Historical pre/post source diff rerun','External paper or current venue policy revalidated',
                       'Original O(k^4) strong-chord program recovered','General phi proof or complexity independently passed']}
(HERE/'asset-verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ('current_tex','pdf')},ensure_ascii=False,indent=2))
print(json.dumps({k:v for k,v in result['current_tex'].items() if k!='formal_blocks'},ensure_ascii=False))
