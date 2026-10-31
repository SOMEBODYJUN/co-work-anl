from pathlib import Path
import json

S=Path(__file__).resolve().parents[4]
E=S/'archives/customer-attraction/tools/evidence/full-tree-milp-candidate-audits-primary'
primary=json.loads((E/'primary-manifest.json').read_text())['sources']
deps=json.loads((E/'dependency-manifest.json').read_text())['sources']
code=json.loads((E/'runtime-manifest.json').read_text())['sources']
selected=[x for x in primary if x['path'].endswith(('/full_tree_milp.py','/audit_milp_candidates.py'))]
selected+=code+[x for x in deps if x['role']=='runtime-input-not-primary']
tree=E/'replay-tree'
assert not tree.exists()
for x in selected:
    dest=tree/x['path'];dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_bytes((S/x['saved_path']).read_bytes())
(E/'runtime-tree-manifest.json').write_text(json.dumps({'runtime_root':str(tree),'code_files':7,'code_bytes':57220,
 'input_files':8,'input_bytes':107270,'sources':selected,'comparison_sources_not_used_by_original_entries':True},ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'code_files':7,'input_files':8}))
