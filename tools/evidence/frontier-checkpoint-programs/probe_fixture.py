"""Additional finite probes; executed only from a newly created disposable root."""
from pathlib import Path
import importlib.util,json,subprocess,sys

root=Path.cwd()
spec=importlib.util.spec_from_file_location('checkpoint_tests',root/'research/weighted_congestion_frontier/tests/test_checkpoint.py')
t=importlib.util.module_from_spec(spec);spec.loader.exec_module(t)
out=[]
def fixture(name,action):
    f=t.CheckpointTests('runTest')
    try:
        f.setUp();result=action(f);out.append({'case':name,'result':result})
    finally:f.doCleanups()
def merge(f):
    f.peer('peer.md','published local peer\n');f.note.write_text('our snapshot\n');x=f.save()
    assert x['status']=='pushed' and x['commit']!=x['pushed_head']
    assert all(a['asset']['commit']==x['pushed_head'] for a in x['assets'])
    return {k:x[k] for k in ['status','commit','pushed_head','checked_head','remote_tip']}
def branch(f,create):
    name='archive-fixture'
    t.run(f.repo,'checkout','-b',name);t.run(f.repo,'config','wcg.branch',name)
    if not create:t.run(f.repo,'push','origin',name)
    f.note.write_text('branch fixture\n');before=t.run(f.repo,'rev-parse','HEAD')
    try:
        x=f.save(create_branch=create)
        assert x['status']=='pushed' and x['branch']==name and all(a['asset']['branch']==name for a in x['assets'])
        return {'status':'pushed','branch':x['branch'],'descriptor_branches':sorted({a['asset']['branch'] for a in x['assets']})}
    except t.c.Stop as exc:
        assert 'main' in str(exc) and t.run(f.repo,'rev-parse','HEAD')==before
        return {'status':'rejected-before-commit','reason':str(exc)}
fixture('snapshot commit versus merged published head',merge)
fixture('existing bound non-main branch',lambda f:branch(f,False))
fixture('first bound branch publication with explicit create flag',lambda f:branch(f,True))
wrapper=root/'research/weighted_congestion_frontier/tools/work.py'
helped=subprocess.run([sys.executable,str(wrapper),'--help'],cwd=root,capture_output=True,text=True,timeout=15)
assert helped.returncode==0 and 'checkpoint' in helped.stdout
out.append({'case':'wrapper real same-ref root help','result':{'returncode':0,'contains_checkpoint':True}})
spec=importlib.util.spec_from_file_location('legacy_work_wrapper',wrapper);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
assert callable(m.main) and m.DEFAULT_SAVE=='customer-attraction'
out.append({'case':'wrapper import real same-ref root without main execution','result':{'callable_main':True,'DEFAULT_SAVE':m.DEFAULT_SAVE,'DEFAULT_BRANCH':getattr(m,'DEFAULT_BRANCH',None)}})
missing=root/'missing/research/weighted_congestion_frontier/tools/work.py';missing.parent.mkdir(parents=True);missing.write_bytes(wrapper.read_bytes())
p=subprocess.run([sys.executable,str(missing),'--help'],cwd=root,capture_output=True,text=True,timeout=15)
assert p.returncode!=0 and 'complete repository-root work.py' in p.stderr
out.append({'case':'wrapper missing root fails explicitly','result':{'returncode':p.returncode,'message':p.stderr.strip()}})
print(json.dumps(out,ensure_ascii=False))
