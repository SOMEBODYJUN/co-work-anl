"""Whitelisted original scalar definitions only; no original imports/CLI/init/pricing.

This is a source-function extraction binding, not an independent coefficient
implementation, historical CLI replay, LP, BI, or universal pricing certificate.
load() reads only the ten listed local definition copies plus primary AP/tuple.
"""
import ast
import hashlib
import json
from collections import defaultdict
from fractions import Fraction as F
from itertools import product, combinations_with_replacement
from math import comb
from pathlib import Path
from types import SimpleNamespace

PRIMARY = {'mp': 'original/95ae42780dac898a9c0d/menu_ap_pricing.py',
           'mt': 'original/1f4560c9319c2a285e47/max_menu_tuple_pricing.py'}

def load(evidence_root=None):
    root = Path(evidence_root or Path(__file__).resolve().parent)
    contract=[]
    def source(rel):
        p=root/rel; raw=p.read_bytes()
        return ast.parse(raw, filename=str(p)), str(p), raw
    def ns(name, **extra):
        return dict(__name__=name, F=F, product=product,
                    combinations_with_replacement=combinations_with_replacement,
                    defaultdict=defaultdict, comb=comb, **extra)
    def extract(rel, env, functions=(), assignments=(), class_bases=None):
        tree,filename,raw=source(rel); selected=[]
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef,ast.AsyncFunctionDef)) and node.name in functions:
                selected.append(node)
            elif isinstance(node, ast.Assign) and any(isinstance(t,ast.Name) and t.id in assignments for t in node.targets):
                selected.append(node)
            elif isinstance(node, ast.ClassDef) and class_bases is not None and node.name in class_bases:
                methods=[m for m in node.body if isinstance(m,ast.FunctionDef) and m.name=='atom_rows']
                assert len(methods)==1
                selected.append(ast.ClassDef(name=node.name,bases=class_bases[node.name],keywords=[],body=methods,decorator_list=[]))
        foundfunctions={n.name for n in selected if isinstance(n,ast.FunctionDef)}
        assert foundfunctions==set(functions), (rel,foundfunctions,functions)
        module=ast.fix_missing_locations(ast.Module(body=selected,type_ignores=[]))
        contract.append({'path':rel,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),
                         'selected_top_level':[getattr(n,'name',','.join(t.id for t in n.targets if isinstance(t,ast.Name))) if isinstance(n,ast.Assign) else n.name for n in selected],
                         'selected_ast_sha256':hashlib.sha256(ast.dump(module,include_attributes=False).encode()).hexdigest(),
                         'selected_ast':ast.dump(module,include_attributes=False)})
        exec(compile(module,filename,'exec'),env)
        return env
    ex=extract('related/five_indexed.py', ns('selected_indexed'),
        functions=('q','old_rows','third_rows','second_rows','evaluate'),
        assignments=('labels','paths','start','families','types','quads'))
    term=extract('related/offdiagonal_closure.py',ns('selected_terminal'),functions=('rows',))
    pair=extract('related/partition_pair_closure.py',ns('selected_pair'),
        functions=('partition','query_cost','compact_costs','rows'),assignments=('PARTITIONS',))
    full=extract('related/full_pricing.py',ns('selected_full',EX=ex,terminal_rows=term['rows'],pair_rows=pair['rows']),
        class_bases={'Universe':[]})
    cross=extract('related/cross_pair_pricing.py',ns('selected_cross',Universe=full['Universe'],
        compact_costs=pair['compact_costs'],PARTITIONS=pair['PARTITIONS']),assignments=('COUNTS','FIELDS'),
        class_bases={'CrossUniverse':[ast.Name(id='Universe',ctx=ast.Load())]})
    mp=extract(PRIMARY['mp'],ns('selected_mp',CrossUniverse=cross['CrossUniverse'],
        LABELS='ABCDEUVWXY', PATHS={'actual':'ABCDE','second':'AEUVW','third':'ABEXY'},
        START={'actual':0,'second':2,'third':3},q=ex['q']),
        functions=('aa','source','ap_value','fixed_rows','menu_specs'),
        assignments=('NODES','MENUS','FIELDS','TYPES'),
        class_bases={'Universe':[ast.Name(id='CrossUniverse',ctx=ast.Load())]})
    lm=extract('related/lift_maximum_branch.py',ns('selected_lm'),functions=('q','rows'),
        assignments=('LABELS','PATHS','START','STATES','TY3','TY4','TY5'))
    mj=extract('related/max_menu_joint_pricing.py',ns('selected_mj',mp=SimpleNamespace(**mp),lm=SimpleNamespace(**lm)),
        functions=('rho4','mapping','new_rows'),assignments=('STATES','RHOMIN'),
        class_bases={'Universe':[ast.Attribute(value=ast.Name(id='mp',ctx=ast.Load()),attr='Universe',ctx=ast.Load())]})
    mt=extract(PRIMARY['mt'],ns('selected_mt',mp=SimpleNamespace(**mp),mj=SimpleNamespace(**mj),lm=SimpleNamespace(**lm)),
        functions=('specs','tuple_rows'),assignments=('SPECS','SPEC'),
        class_bases={'Universe':[ast.Attribute(value=ast.Name(id='mj',ctx=ast.Load()),attr='Universe',ctx=ast.Load())]})
    verify=extract('related/exact_primal.py',ns('selected_verify'),functions=('verify_atom',))
    def evaluator(mode='menu'):
        cls={'menu':mp['Universe'],'joint':mj['Universe'],'tuple':mt['Universe']}[mode]
        u=cls.__new__(cls);u.overlap=1;u.ty={k:list(product((0,1),repeat=k)) for k in (3,4)}
        u.cross=[]
        for src in ('AB','AE'):
            for dst in ('AB','AE','Sbranch'):
                if src==dst:continue
                for a,b in combinations_with_replacement(range(4 if dst=='Sbranch' else 3),2):
                    for orb in pair['PARTITIONS']:
                        u.cross.append((f'crosspair:{src}:{dst}:{a}{b}:{orb}',src,dst,a,b,orb))
        u.specs=mp['menu_specs']()
        return u
    return SimpleNamespace(evaluator=evaluator,verify_atom=verify['verify_atom'],ex=ex,term=term,pair=pair,
                           mp=mp,lm=lm,mj=mj,mt=mt,contract=contract)
