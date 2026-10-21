"""Independent exact audit of the new closure rows and saved feasible point.

The new formulas are checked by explicit index sums, and the conditional
extrema by enumerating all allowed target memberships. No full SPE is claimed.
"""
from fractions import Fraction as F
from itertools import combinations, combinations_with_replacement, product
from pathlib import Path
import hashlib
import importlib.util
import json

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location('probe', HERE/'cross_family_closure.py')
P = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(P)


def expanded(atom):
    b = dict(zip('ABCDEUVWXY', map(int, atom['bits'])))
    families = {}
    for tag, field, arity, fixed in [('AB','AB_hist',3,'AB'),
                                    ('AE','AE_hist',3,'AE'),
                                    ('S','second_hist',4,'A')]:
        data = tuple(ty for ty,n in zip(product((0,1),repeat=arity),atom[field])
                     for _ in range(n))
        families[tag] = sum(b[x] for x in fixed), data
    d = sum(ty[0] for ty in families['AB'][1])
    for k,(tag,fixed) in enumerate([('Lact','ABC'),('Lsec','AEU'),('Lthird','ABE')]):
        ell,h = atom['menus_lh'][k]
        data = ((0,0),)*(5-d-ell+h) + ((0,1),)*(ell-h) + ((1,0),)*(d-h) + ((1,1),)*h
        families[tag] = sum(b[x] for x in fixed), data
    return b,families


def direct_cross(atom):
    b,families = expanded(atom)
    menus = {}
    for tag in ('AB','AE','S'):
        _,data = families[tag]
        for pos in range(len(data[0])):
            menus[f'{tag}{pos}'] = tuple(ty[pos] for ty in data)
    for tag in ('Lact','Lsec','Lthird'):
        menus[tag] = tuple(ty[1] for ty in families[tag][1])
    out = {}
    for tag in ('AB','AE','S'):
        p,data = families[tag]
        arity = len(data[0])
        for pos in range(1,arity):
            for menu,query in menus.items():
                out[f'cross:{tag}:{pos}:K:{menu}'] = sum((
                    (F(ty[pos],p+sum(ty)) if ty[pos] else F(0))
                    - F(q,p+sum(ty[:pos])+arity-pos)
                    for ty in data for q in query),F(0))
        for mx,my in combinations_with_replacement(menus,2):
            val = F(0)
            for ty in data:
                background = p+sum(ty[:-2])
                h = (F(ty[-2]+ty[-1],p+sum(ty))
                     if ty[-2]+ty[-1] else F(0))
                h += F(ty[-2],(background+1)*(background+2))
                for x,y in product(menus[mx],menus[my]):
                    val += h-(F(x+y,background+x+y) if x+y else F(0))
            out[f'cross:{tag}:r2:{mx}:{my}'] = val
    for tag,path in [('actual','ABCDE'),('second','AEUVW'),('third','ABEXY')]:
        background = sum(b[x] for x in path[:3])
        h = (F(b[path[3]]+b[path[4]],sum(b[x] for x in path))
             if b[path[3]]+b[path[4]] else F(0))
        h += F(b[path[3]],(background+1)*(background+2))
        for mx,my in combinations_with_replacement(menus,2):
            out[f'cross:{tag}:r2:{mx}:{my}'] = sum((
                h-(F(x+y,background+x+y) if x+y else F(0))
                for x,y in product(menus[mx],menus[my])),F(0))
    return out


def direct_conditional(atom):
    _,families = expanded(atom)
    menus = {}
    for tag,(_,data) in families.items():
        for pos in range(1,len(data[0])):
            menus[f'{tag}{pos}'] = tag,pos,tuple(sum(ty[pos] for ty in data if ty[0]==t)
                                              for t in (0,1))
    out = {}
    alignment_count = 0
    for tag,(p,data) in families.items():
        arity = len(data[0])
        for pos in range(1,arity):
            actual = sum((F(ty[pos],p+sum(ty)) if ty[pos] else F(0)
                          for ty in data),F(0))
            for menu,(mtag,mpos,counts) in menus.items():
                if mtag==tag:
                    candidates = [tuple(ty[mpos] for ty in data)]
                else:
                    bins = [tuple(i for i,ty in enumerate(data) if ty[0]==t) for t in (0,1)]
                    candidates = []
                    for left,right in product(combinations(bins[0],counts[0]),
                                              combinations(bins[1],counts[1])):
                        selected = set(left+right)
                        candidates.append(tuple(int(i in selected) for i in range(5)))
                alignment_count += len(candidates)
                diagonals = []
                offdiagonals = []
                for query in candidates:
                    diagonals.append(sum((F(query[i],p+sum(ty[:pos])+arity-pos)
                                          for i,ty in enumerate(data)),F(0)))
                    offdiagonals.append(sum((F(query[j],p+sum(ty[:pos])+arity-pos)
                                             for i,ty in enumerate(data) for j in range(5) if i!=j),F(0)))
                out[f'conditional:{tag}:{pos}:diag:{menu}'] = actual-min(diagonals)
                out[f'conditional:{tag}:{pos}:offdiag:{menu}'] = 4*actual-min(offdiagonals)
    return out,alignment_count


def main():
    source = json.loads(P.SOURCE.read_text())
    atoms = source['primal']['atoms']
    saved = json.loads((HERE/'cross_family_closure.json').read_text())
    mass = list(map(F,saved['exact_reweighting']))
    assert len(atoms)==len(mass)==64 and min(mass)>=0
    columns=[]
    alignments=0
    for atom in atoms:
        direct=direct_cross(atom)
        assert direct==P.cross_rows(atom)
        conditional,num=direct_conditional(atom)
        assert conditional==P.conditional_rows(atom)
        alignments+=num
        bits=tuple(map(int,atom['bits']))
        hists=[atom[k] for k in ('AB_hist','AE_hist','second_hist')]
        rows=P.NS['evaluate'](bits,hists,atom['menus_lh'],True)
        rows.update(P.OLDMODULE.module.rows(atom,direct=True))
        rows.update(direct)
        rows.update(conditional)
        assert len(rows)==1284
        columns.append(rows)
    names=tuple(columns[0])
    slacks={n:sum((r*c[n] for r,c in zip(mass,columns)),F(0)) for n in names}
    assert min(slacks.values())>=0
    welfare=sum((r*int(any(map(int,a['bits'][:5]))) for r,a in zip(mass,atoms)),F(0))
    cover=sum((r*int(sum(n*t[0] for n,t in zip(a['AB_hist'],product((0,1),repeat=3)))>0)
               for r,a in zip(mass,atoms)),F(0))
    assert welfare==1 and cover==F(saved['exact_primal_value'])>2
    report={'scope':'exact obstruction to the stated 1284-row necessary-condition system only',
            'is_SPE_counterexample':False,'source_atoms':64,'positive_atoms':sum(r>0 for r in mass),
            'row_count':len(names),'direct_cross_rows_per_atom':len(direct),
            'conditional_rows_per_atom':len(conditional),'enumerated_conditional_alignments':alignments,
            'welfare':str(welfare),'comparison_cover':str(cover),'gap_above_two':str(cover-2),
            'minimum_slack':str(min(slacks.values())),'zero_slack_count':sum(v==0 for v in slacks.values()),
            'negative_slacks':{},
            'source_sha256':hashlib.sha256(P.SOURCE.read_bytes()).hexdigest(),
            'primal_sha256':hashlib.sha256((HERE/'cross_family_closure.json').read_bytes()).hexdigest(),
            'generator_sha256':hashlib.sha256((HERE/'cross_family_closure.py').read_bytes()).hexdigest(),
            'slacks':{n:str(v) for n,v in slacks.items()}}
    (HERE/'verified_cross_family_closure.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='slacks'},indent=2))


if __name__=='__main__':
    main()
