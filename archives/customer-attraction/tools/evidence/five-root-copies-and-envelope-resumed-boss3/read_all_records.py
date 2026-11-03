"""Consume all thirty frozen files and every atom/field, without importing solvers.

Checks the necessary schema and menu identities actually encoded by these files.
This is a complete data reading/binding report, not a full row-feasibility audit.
"""
from collections import Counter
from fractions import Fraction as F
from itertools import product
import ast, hashlib, json, math
from pathlib import Path

HERE=Path(__file__).resolve().parent
REPO=HERE.parents[4]
MAN=json.loads((HERE/'source-manifest.json').read_text())
PARENT=REPO/'archives/customer-attraction/tools/evidence/maxroot-gamma-shared-menu-primary/source-root'
SPECS={'B':4,'C':4,'D':4,'E':4,'D2':3,'D3':2}

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False)
def walk(x,c):
    c[type(x).__name__]+=1
    if isinstance(x,dict):
        for k,v in x.items():walk(k,c);walk(v,c)
    elif isinstance(x,list):
        for v in x:walk(v,c)
    elif isinstance(x,float):assert math.isfinite(x)

def atom_scan(atoms):
    schemas=Counter();copy_schemas=Counter();histcoords=Counter();dcounts=Counter();bits=Counter()
    issues=Counter();examples={};keys=set();allfield=Counter();root_count=0;menu_corners=Counter()
    def issue(k,index):issues[k]+=1;examples.setdefault(k,index)
    for idx,a in enumerate(atoms):
        schemas[','.join(sorted(a))]+=1
        for k in a:allfield[k]+=1
        bits[a['bits']]+=1
        if len(a['bits'])!=10 or set(a['bits'])-{'0','1'}:issue('bits-not-ten-binary',idx)
        ds=[]
        for k,arity in [('AB_hist',3),('AE_hist',3),('second_hist',4),('root_hist',5)]:
            if k not in a:continue
            h=a[k];histcoords[k]+=len(h)
            if len(h)!=1<<arity or any(type(v)is not int or v<0 for v in h) or sum(h)!=5:issue('bad-'+k,idx)
            ds.append(sum(h[1<<(arity-1):]))
        if len(set(ds))!=1:issue('unequal-first-membership-d',idx)
        d=ds[0];dcounts[d]+=1
        if 'root_hist'in a:root_count+=1
        for ell,h in a['menus_lh']:
            if not(all(type(v)is int for v in (ell,h)) and 0<=h<=d and 0<=ell-h<=5-d):issue('bad-LH-menu',idx)
            menu_corners[str((ell,h) in {(0,0),(d,d),(5-d,0),(5,d)})]+=1
        if len(a['menus_lh'])!=3:issue('wrong-menu-count',idx)
        if 'copies'in a:
            cp=a['copies'];copy_schemas[','.join(sorted(cp))]+=1
            for s,z in cp.items():
                if s not in SPECS or len(z)!=SPECS[s] or any(v not in (0,1) for v in z):issue('bad-copy-tail',idx)
        k=canonical(a)
        if k in keys:issue('byte-semantic-duplicate-atom',idx)
        keys.add(k)
    return {'atoms':len(atoms),'schemas':dict(schemas),'all_field_occurrences':dict(allfield),
        'copy_schemas':dict(copy_schemas),'histogram_coordinates_consumed':dict(histcoords),
        'membership_d_frequencies':dict(dcounts),'distinct_visible_bits':len(bits),
        'root_hist_present':root_count,'menu_corner_flags':dict(menu_corners),
        'issues':dict(issues),'issue_first_indices':examples,'distinct_complete_atoms':len(keys)}

def binding(d):
    result=[]
    for rel,expected in d.get('sources',{}).items():
        candidates=[HERE/'original'/rel,PARENT/rel]
        found=next((p for p in candidates if p.is_file()),None)
        actual=sha(found) if found else None
        result.append({'path':rel,'recorded_sha256':expected,'available_sha256':actual,
            'status':'match' if actual==expected else 'different-version' if found else 'not-in-preserved-closure',
            'available_file':str(found.relative_to(REPO)) if found else None})
    return result

def main():
    outputs={};allatoms=0;allhistory=0;totalcoords=0
    for m in MAN:
        p=HERE/'original'/m['path'];assert p.stat().st_size==m['size'] and sha(p)==m['sha256']
        if p.suffix=='.py':ast.parse(p.read_text());continue
        if p.suffix!='.json':continue
        d=json.loads(p.read_text());types=Counter();walk(d,types)
        out={'source_id':m['id'],'sha256':m['sha256'],'bytes':m['size'],'top_fields':list(d),
            'all_recursive_value_types_consumed':dict(types),'scope':d.get('scope'),'status':d.get('status'),
            'sources_binding':binding(d)}
        if 'atoms'in d:
            out['atom_scan']=atom_scan(d['atoms']);allatoms+=len(d['atoms'])
            totalcoords+=sum(out['atom_scan']['histogram_coordinates_consumed'].values())
        if 'row_names'in d:
            names=d['row_names'];out['row_names']={'count':len(names),'unique':len(set(names)),'families':dict(Counter(x.split(':')[0] for x in names))}
        mult=d.get('dual_multipliers_float',d.get('multipliers_float',{}))
        if mult:
            out['multipliers']={'count':len(mult),'minimum':min(mult.values()),'maximum':max(mult.values()),'families':dict(Counter(k.split(':')[0] for k in mult)),
                'all_values':mult}
            if 'row_names'in d:assert set(mult)<=set(d['row_names'])
        if 'primal_float'in d:
            mass=d['primal_float'];assert len(mass)==len(d['atoms'])
            W=sum(v*int(any(map(int,a['bits'][:5]))) for v,a in zip(mass,d['atoms']))
            O=sum(v*int(any(a['AB_hist'][4:])) for v,a in zip(mass,d['atoms']))
            out['primal']={'coordinates':len(mass),'positive_above_1e9':sum(v>1e-9 for v in mass),
                'minimum':min(mass),'maximum':max(mass),'total_mass':sum(mass),'W_float':W,'O_float':O,
                'saved_beta':d.get('dual_beta_float'),'trailing_zero_coordinates':len(mass)-next((i+1 for i in range(len(mass)-1,-1,-1) if mass[i]),0),
                'negative_entries':sum(v<0 for v in mass)}
        if 'history'in d:
            hs=d['history'];allhistory+=len(hs);out['history_all_records']=hs
            out['history_summary']={'records':len(hs),'new_columns_sum':sum(h['new_columns'] for h in hs),
                'first_columns':hs[0]['columns'] if hs else None,'last_columns':hs[-1]['columns'] if hs else None,
                'last_scaled_residual':hs[-1]['minimum_scaled_residual'] if hs else None,
                'all_residuals_strictly_negative':all(h['minimum_scaled_residual']<0 for h in hs),
                'last_columns_match_saved_atoms':bool(hs) and hs[-1]['columns']==len(d['atoms'])}
        for k in ('cases','records','total_IC','total_GAP5_rows','python','target','message','dual_beta_float'):
            if k in d:out[k]=d[k]
        outputs[p.name]=out
    # Independently recompute the four saved exact constant records, no original import.
    check=next(m for m in MAN if m['path'].endswith('/weighted_root_saturation_check.json'))
    d=json.loads((HERE/'original'/check['path']).read_text());arithmetic=[]
    for r in d['records']:
        lam=list(map(F,r['lambda']));ts=(4,3,2,1);assert sum(lam)==1 and min(lam)>=0
        c=sum(t*x for t,x in zip(ts,lam));aa=[F(3,4)*ts[j]*lam[j]+sum(lam[i]/(ts[i]+1) for i in range(j+1,4)) for j in range(4)]
        a=max(aa);B=5*c+100*a;C=20*a+c/5-1
        assert aa==list(map(F,r['a_j'])) and (a,c,B,C)==tuple(F(r[k]) for k in ('a','c','B','C')) and C>0
        arithmetic.append({'lambda':r['lambda'],'B':str(B),'C':str(C),'all_saved_fraction_fields_match':True})
    result={'status':'complete-data-reading-and-binding','source_files':len(MAN),'source_bytes':sum(x['size'] for x in MAN),
        'JSON_files':len(outputs),'atoms_consumed':allatoms,'histogram_coordinates_consumed':totalcoords,
        'history_records_consumed':allhistory,'reports':outputs,'weighted_exact_constants':arithmetic,
        'LP_SPE_pricing_or_random_calls':0,'original_main_calls':0,
        'scope':'Complete field/atom reading and static-domain/source-version checks; no row-feasibility or game-realization claim.'}
    (HERE/'complete-data-reading.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='reports'},ensure_ascii=False))

if __name__=='__main__':main()
