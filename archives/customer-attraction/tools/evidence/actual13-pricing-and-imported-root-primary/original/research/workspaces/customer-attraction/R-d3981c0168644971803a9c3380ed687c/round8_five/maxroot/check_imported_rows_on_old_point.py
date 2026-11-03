"""Explain the old >2 relaxation point using imported theorem's active rows.

Uses the imported portable literal row evaluator for this diagnostic only;
this is not an independent second full proof verifier.
"""
from pathlib import Path
from fractions import Fraction as F
import importlib.util,json,hashlib
HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'AGENTS.md').exists())
PACKAGE=ROOT/'customer_attraction/proofs/half5_exact_v1'
SOURCE=HERE.parent/'certificate/exact_full_actual_extension_known_v1.json'
def run():
    spec=importlib.util.spec_from_file_location('imported_half5_portable',PACKAGE/'verify_certificate.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    bg,pc,deep,_=mod.source_tables();domain=mod.LiteralDomain(bg,pc,deep);_,weights,B,D,_=mod.load_certificate(PACKAGE/'certificate.json')
    point=json.loads(SOURCE.read_text());atoms=point['atoms'];index={k:{tuple(h):i for i,h in enumerate(domain.hist[k])} for k in (3,4)}
    slacks={n:F(0) for n in weights};kcols={};K=sum(F(a['exact_mass'])*int(a['max_bits'][0]) for a in atoms)
    for a in atoms:
        mass=F(a['exact_mass']);b=dict(zip(mod.LABELS,map(int,a['bits'])));d=sum(a['AB_hist'][4:]);menus=a['menus_lh']
        for n in weights:
            tag=n.split(':')[0]
            if tag not in mod.FAMILIES and ':sum-S' in n:tag='Sbranch'
            if tag in mod.FAMILIES:
                key,const,kap=domain.family_parts(tag,b,{n:1});k,p,terms=key;field={'AB':'AB_hist','AE':'AE_hist','Sbranch':'second_hist'}[tag];i=index[k][tuple(a[field])];num=const+sum(v*int(domain.features[k,p][f][i]) for f,v in terms);coef=F(int(num),120)
            else:coef,kap=domain.fixed_value(n,b,d,menus)
            slacks[n]+=mass*coef
            if n in kcols:assert kcols[n]==kap
            else:kcols[n]=kap
    for n in slacks:slacks[n]+=kcols[n]*K
    negative={n:str(v) for n,v in slacks.items() if v<0};assert negative
    W=sum(F(a['exact_mass'])*int(any(map(int,a['bits'][:5]))) for a in atoms);O=sum(F(a['exact_mass'])*int(any(a['AB_hist'][4:])) for a in atoms)
    out={'status':'old point strictly separated by imported active necessary rows','scope':__doc__,'source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'proof_certificate_sha256':hashlib.sha256((PACKAGE/'certificate.json').read_bytes()).hexdigest(),'projected_atoms':len(atoms),'W':str(W),'O':str(O),'K':str(K),'negative_rows':negative,'all_53_slacks':{n:str(v) for n,v in slacks.items()}}
    HERE.joinpath('old_point_imported_row_separation.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='all_53_slacks'},indent=2))
if __name__=='__main__':run()
