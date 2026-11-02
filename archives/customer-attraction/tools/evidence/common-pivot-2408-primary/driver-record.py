from pathlib import Path
from fractions import Fraction as F
from functools import lru_cache
from itertools import product, combinations
import subprocess, sys, json, shutil, hashlib, time, platform

REPO=Path('/workspace/scratch/b197e2376a82/co-work-anl-boss7')
SRC=Path('/workspace/scratch/b197e2376a82/boss7-resume/sources')
EV=REPO/'archives/customer-attraction/tools/evidence'
claims=json.loads((SRC.parent/'claimed.json').read_text())
inventory={x['id']:x for x in map(json.loads,(REPO/'cleanup/inventory.jsonl').open())}
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def put(src,dst):
    dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dst)
    return {'path':str(dst.relative_to(REPO)),'sha256':digest(dst),'bytes':dst.stat().st_size}
def primary(base,ids):
    records=[]
    for sid in ids:
        x=inventory[sid];src=SRC/(sid+'--'+Path(x['path']).name)
        assert digest(src)==x['sha256']
        r=put(src,base/'original'/Path(x['path']).name);r['source']=x;records.append(r)
    (base/'source-manifest.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n')
    return records
def execute(base,argv,cwd):
    t=time.perf_counter();p=subprocess.run(argv,cwd=cwd,capture_output=True)
    (base/'stdout.txt').write_bytes(p.stdout);(base/'stderr.txt').write_bytes(p.stderr)
    record={'argv':argv,'cwd':str(cwd.relative_to(REPO)),'python':platform.python_version(),
            'exit_code':p.returncode,'elapsed_seconds':time.perf_counter()-t,
            'stdout_sha256':digest(base/'stdout.txt'),'stderr_sha256':digest(base/'stderr.txt')}
    (base/'execution.json').write_text(json.dumps(record,indent=2)+'\n')
    assert p.returncode==0,p.stderr.decode()
    return p

base=EV/'prefix-coverage-probe-primary';base.mkdir(exist_ok=True)
primary(base,['641419c9b3c06f082c59','dabbe5516e3c88e1bb89'])
runtime=base/'runtime';pkg=EV/'exact-spe/customer_attraction'
for name in ['__init__.py','model.py','exact.py','certificate.py']:
    put(pkg/name,runtime/'customer_attraction'/name)
script=runtime/'research/workspaces/customer-attraction/R-64201cd12083425899e2d643ec9bc087/round3_tree/prefix_coverage_probe.py'
put(base/'original/prefix_coverage_probe.py',script)
output=base/'replayed.json'
assert not output.exists(),'do not rerun this event'
execute(base,[sys.executable,'-B',str(script),'--output',str(output)],runtime)
old=json.loads((base/'original/prefix_coverage_probe.json').read_text());new=json.loads(output.read_text())
old['config']['output']=str(output);assert old==new

# A second implementation at the saved point only, with integer shares scaled by 60.
weights=new['best']['weights'];prefix=tuple(new['best']['prefix']);p=5;m=6
def cov(c,excluded=(0,)*5):
    return sum(w for b,w in enumerate(weights,1) if any(c[a] for a in range(p) if b>>a&1)
               and not any(excluded[a] for a in range(p) if b>>a&1))
def payoff(c,a):
    return sum(w*60//sum(c[j] for j in range(p) if b>>j&1)
               for b,w in enumerate(weights,1) if w and b>>a&1)
@lru_cache(None)
def tails(c):
    if sum(c)==m:return frozenset([c])
    children=[tails(tuple(v+(j==a) for j,v in enumerate(c))) for a in range(p)]
    threshold=max(min(payoff(t,a) for t in child) for a,child in enumerate(children))
    return frozenset(t for a,child in enumerate(children) for t in child if payoff(t,a)>=threshold)
outcomes=sorted(tails(prefix));old_cov=cov(prefix)
residual=max(cov(tuple(int(a in C) for a in range(p)),prefix) for C in combinations(range(p),4))
check={'scope':'independent integer-scaled outcome-set recursion at the one saved prefix only',
       'scale':60,'total_customers':sum(weights),'prefix':prefix,'outcomes':outcomes,
       'old_coverage':old_cov,'residual_optimum':residual,
       'outcome_ledger':[{'terminal':t,'new_coverage':cov(t,prefix),'slack':2*cov(t,prefix)+old_cov-residual} for t in outcomes],
       'count_states':tails.cache_info().currsize,'replay_fields_equal_except_output_path':True}
assert outcomes==[(2,0,4,0,0)] and sum(weights)==29
assert check['outcome_ledger'][0]['slack']==27
(base/'saved-point-independent.json').write_text(json.dumps(check,indent=2)+'\n')
print('prefix replay and saved point passed',flush=True)

base=EV/'common-pivot-2408-primary';base.mkdir(exist_ok=True)
primary(base,['de58007b22280f6d56d7','ee9f74e216313dff242c','c44ba0af0e5f14894dcf'])
runtime=base/'runtime';folder=runtime/'research/workspaces/customer-attraction/R-64201cd12083425899e2d643ec9bc087/round3_indexed'
for n in ['common_pivot_rows.py','recover_common_pivot.py']:
    put(base/'original'/n,folder/n)
related=[]
for sid in ['4dec003956d30e008996','439b9828ca472e39f0a3']:
    x=inventory[sid];src=SRC/(sid+'--'+Path(x['path']).name)
    assert digest(src)==x['sha256']
    r=put(src,folder/Path(x['path']).name);r['source']=x;related.append(r)
olddeps=EV/'global-indexed-reviews-boss3/related'
for n in ['offdiagonal_probe.py','crossmenu_probe.py','menutax_probe.py','alignedtax_probe.py','tripleprofit_probe.py']:
    related.append(put(olddeps/n,folder.parent/'next_credible'/n))
canonical=EV/'added-six-boss3/related/tests/audits/customer_attraction_five_indexed.py'
related.append(put(canonical,runtime/'tests/audits/customer_attraction_five_indexed.py'))
certificate=EV/'five-player-indexed/evidence/certificates/customer_attraction/five_player_indexed_bound.json'
related.append(put(certificate,runtime/'evidence/certificates/customer_attraction/five_player_indexed_bound.json'))
(base/'related-manifest.json').write_text(json.dumps(related,ensure_ascii=False,indent=2)+'\n')
assert not (folder/'common_pivot_2408_exact_obstruction.json').exists(),'do not rerun this event'
execute(base,[sys.executable,'-B',str(folder/'recover_common_pivot.py')],folder)
actual=folder/'common_pivot_2408_exact_obstruction.json'
assert actual.read_bytes()==(base/'original/common_pivot_2408_exact_obstruction.json').read_bytes()
put(actual,base/'replayed.json')
report=json.loads(actual.read_text());atoms=report['atom_masses']
# Independent twelve-row formulas; no import of the source rows or old 2396 templates.
slacks={};metadata=[]
for a in atoms:
    b=dict(zip('ABCDEUVWXY',map(int,a['bits'])));z=F(a['mass'])
    d=sum(n*t[0] for n,t in zip(a['AB_hist'],product((0,1),repeat=3)))
    assert len(a['bits'])==10 and sum(a['AB_hist'])==sum(a['AE_hist'])==sum(a['second_hist'])==5
    for r,path in enumerate(('ABCDE','AEUVW','ABEXY')):
        p=sum(b[c] for c in path[:3]);ell,h=a['menus_lh'][r];D=(p+1)*(p+2)
        for s in range(3):
            if r==s:continue
            es,hs=a['menus_lh'][s]
            values={'diag-menu':F(ell-es,p+1)-F(h-hs,D),
                    'off-menu':F(4*(ell-es),p+1)+F(d*es-4*h-hs,D)}
            for tag,v in values.items():
                n=f'common-pivot:{r}:{tag}:{s}';slacks[n]=slacks.get(n,F())+z*v
assert {n:str(v) for n,v in slacks.items()}==report['new_row_slacks']
W=sum(F(a['mass'])*int(any(map(int,a['bits'][:5]))) for a in atoms)
O=sum(F(a['mass'])*int(any(a['AB_hist'][4:])) for a in atoms)
assert W==1 and O==F(report['O'])>2 and O-2==F(report['gap_above_two'])
check={'scope':'independent 12 added rows plus W/O/positive-mass identity only; old 2396 rows reused from original recovery event',
       'recovery_byte_equal':True,'positive_atoms':len(atoms),'W':str(W),'O':str(O),
       'gap_above_two':str(O-2),'new_row_slacks':{n:str(v) for n,v in slacks.items()},
       'positive_added_rows':sum(v>0 for v in slacks.values()),'zero_added_rows':sum(v==0 for v in slacks.values()),
       'legacy_mass_numerator_present':sum('mass_numerator' in a for a in atoms),
       'legacy_numerators_are_not_current_mass':True}
(base/'independent-added-rows.json').write_text(json.dumps(check,indent=2)+'\n')
print('common pivot exact recovery and independent twelve rows passed',flush=True)
