"""Materialize a selected rational common completion as deterministic gzip JSONL."""
from fractions import Fraction as F
from hashlib import sha256
from itertools import permutations,product
from math import lcm
from pathlib import Path
import argparse,gzip,json

def sha(p):return sha256(p.read_bytes()).hexdigest()

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--witness',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True);ap.add_argument('--manifest',type=Path,required=True)
    args=ap.parse_args();w=json.loads(args.witness.read_bytes())
    assert sha(Path(w['input_path']))==w['input_sha256']
    ns=list(map(tuple,w['literal_node_order']));ni={e:k for k,e in enumerate(ns)}
    perms=list(map(tuple,w['symmetrization']['permutations']))
    assert len(perms)==720 and set(perms)==set(permutations(range(6)))
    inverse=[]
    for p in perms:
        inv=[None]*66
        for source,(f,i,j) in enumerate(ns):inv[ni[f,p[i],p[j]]]=source
        inverse.append(inv)
    count=0;total=F();scale=1
    with args.output.open('wb') as raw:
      with gzip.GzipFile(filename='',fileobj=raw,mode='wb',mtime=0) as gz:
        def put(x):gz.write((json.dumps(x,sort_keys=True,separators=(',',':'))+'\n').encode())
        put({'type':'header','witness_sha256':sha(args.witness),'input_sha256':w['input_sha256'],
             'literal_node_order':ns,'state_encoding':['00','01','10','11']})
        for phase in ('A','B'):
            weight=F(w[f'phase_{phase}_weight'])
            if not weight:continue
            assert weight>0
            for h in w['phases'][phase]:
                ws=[z for z,n in zip(product(range(2),repeat=3),h['hist']) for _ in range(n)]
                pwords=[]
                for p in perms:
                    pws=[None]*6
                    for i in range(6):pws[p[i]]=''.join(map(str,ws[i]))
                    pwords.append(pws)
                for ai,atom in enumerate(h['atoms']):
                    mass=weight*F(atom['mass'])/720;assert mass>0
                    scale=lcm(scale,mass.denominator);total+=720*mass
                    for pi,inv in enumerate(inverse):
                        put({'type':'atom','phase':phase,'hist_column':h['hist_column'],'base_atom':ai,
                             'permutation':pi,'mass':str(mass),'actual_bits':h['actual_bits'],
                             'old_words':pwords[pi],'states':''.join(str(atom['states'][k]) for k in inv)})
                        count+=1
    assert count==w['expanded_positive_atoms']
    out={'scope':w['scope'],'input_sha256':w['input_sha256'],'witness_sha256':sha(args.witness),
         'source_sha256':sha(Path(__file__)),'atoms_path':str(args.output),'atoms_sha256':sha(args.output),
         'expanded_positive_atoms':count,'total_rational_mass':str(total),
         'unit_customer_scale':str(scale),'unit_scale_digits':len(str(scale))}
    args.manifest.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='unit_customer_scale'},ensure_ascii=False))

if __name__=='__main__':main()
