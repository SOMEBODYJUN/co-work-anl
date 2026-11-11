"""Three-way merge disjoint mathematical registrations; reject true collisions."""
from pathlib import Path
import hashlib
import json
import subprocess

B=Path(__file__).resolve().parent
R=B.parents[2]
def git(*args):
    return subprocess.check_output(['git',*args],cwd=R,text=True).strip()
ours=git('rev-parse','HEAD')
theirs=git('rev-parse','refs/remotes/origin/rebuild/research-v2')
base=git('merge-base',ours,theirs)
assert ours=='38aeb0a7dfcea7524fecbdb360ac2af8a6300b34'
assert theirs=='08d120b3337d3f3fcd608432bb288edcc81f8d33'
def read(rev):
    return json.loads(git('show',rev+':research/registry.json'))
A,O,T=map(read,(base,ours,theirs))
out={}
report={'base':base,'ours':ours,'theirs':theirs,'rule':'Keyed three-way merge; differing simultaneous edits are rejected, not overwritten.','collections':{}}
for key,idkey in (('objects','object_id'),('materials','path')):
    a,o,t=({v[idkey]:v for v in d[key]} for d in (A,O,T))
    assert all(len(z)==len(d[key]) for z,d in zip((a,o,t),(A,O,T)))
    order=list(o)+[i for i in t if i not in o]
    values=[]
    oc=tc=0
    for i in order:
        av,ov,tv=a.get(i),o.get(i),t.get(i)
        if ov==tv:v=ov
        elif ov==av:v=tv;tc+=1
        elif tv==av:v=ov;oc+=1
        else:raise AssertionError(('Actual overlapping edit',key,i))
        if v is not None:values.append(v)
    out[key]=values
    report['collections'][key]={'base_count':len(a),'ours_count':len(o),'theirs_count':len(t),'merged_count':len(values),'ours_distinct_changes':oc,'theirs_distinct_changes':tc,'true_collisions':0}
for key in A:
    if key in out:continue
    if key=='edge_files':
        assert set(A[key])<=set(O[key]) and set(A[key])<=set(T[key])
        out[key]=list(dict.fromkeys(O[key]+T[key]))
    else:
        av,ov,tv=A[key],O[key],T[key]
        if ov==tv:out[key]=ov
        elif ov==av:out[key]=tv
        elif tv==av:out[key]=ov
        else:raise AssertionError(('Unresolved metadata',key))
out={k:out[k] for k in O}
prepared=B/'registry-round6-merged.json'
assert not prepared.exists()
prepared.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
report['merged_registry_sha256']=hashlib.sha256(prepared.read_bytes()).hexdigest()
report['status']='PREPARED_WITH_NO_SEMANTIC_COLLISIONS'
(B/'registry-round6-merge-receipt.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False,indent=2))
