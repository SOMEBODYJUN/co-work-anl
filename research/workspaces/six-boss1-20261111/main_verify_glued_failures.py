"""Literal atom audit of all nine failed interfaces of Main's product law.

Independently enumerates the compact gluing kernel; no import of the first
calculation.  Marginal identities and original per-customer payoffs are exact.
"""
from collections import defaultdict
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
from pathlib import Path
import json

W = Path(__file__).resolve().parent


def canon(seq):
    d={}
    return tuple(d.setdefault(i,len(d)) for i in seq)


def main():
    a=json.loads((W/'main_glued_terminal_interfaces.json').read_bytes())
    n=json.loads((W/'common_network_19662/common_atoms.json').read_bytes())
    r=json.loads((W/'root_pair_joint_19662/joint_completion_exact.json').read_bytes())
    blocks={b['hist_column']:b for b in n['blocks']}
    nodes=[e for e in product(range(2),range(6),range(6)) if e[0] or e[1]!=e[2]]
    failed=[x for x in a['rows'] if F(x['slack'])<0]
    assert len(failed)==9
    own_net,own_root=defaultdict(F),defaultdict(F)
    slacks=[F() for _ in failed]
    total=F();atoms=0;literal_evaluations=0
    for k in a['conditional_kernel']:
        hi,ri=k['hist'],k['root_atom'];H=F(k['hist_mass'])
        root=r['atoms'][ri];block=blocks[hi]
        assert F(k['root_mass'])==F(root['mass'])
        old=tuple(w for w,m in enumerate(block['hist']) for _ in range(m))
        assert sorted(root['old_words'])==list(old)
        actual=tuple(map(int,block['actual_bits']))
        P=sum(actual[:4]);base=sum(actual[:3])+actual[5]
        for ai,net in enumerate(block['atoms']):
            for aligned in k['aligned_root_vectors']:
                mass=F(net['mass'])*F(root['mass'])*aligned['multiplicity']/(H*k['number_of_alignments'])
                assert mass>0
                nw=aligned['new_words'];assert len(nw)==6
                own_net[hi,ai]+=mass;own_root[ri]+=mass;total+=mass;atoms+=1
                for j,row in enumerate(failed):
                    q=row['query'];value=F()
                    if q[0]=='F-to-Y':
                        h1,h2,_=net['B4_state']
                        bit=q[1]
                        value=F(6*h2-sum((w>>(4-bit))&1 for w in nw),6*(base+h1+1))
                        literal_evaluations+=6
                    else:
                        assert q[0]=='Z-to-Y'
                        f,typ=q[1];typ=tuple(typ);bit=q[2]
                        counts=defaultdict(int);size=0
                        for i in range(6):
                            y=(nw[i]>>(4-bit))&1
                            for ei,(ff,b,c) in enumerate(nodes):
                                if ff==f and canon((i,b,c))==typ:
                                    rr,zz=divmod(net['states'][ei],2)
                                    counts[P+rr+1]+=zz-y;size+=1
                        assert size>0
                        value=sum((F(v,den*size) for den,v in counts.items()),F())
                        literal_evaluations+=size
                    slacks[j]+=mass*value
    assert total==1
    for hi,b in blocks.items():
        for ai,x in enumerate(b['atoms']):assert own_net[hi,ai]==F(x['mass'])
    for ri,x in enumerate(r['atoms']):assert own_root[ri]==F(x['mass'])
    for row,s in zip(failed,slacks):assert s==F(row['slack'])<0
    out=dict(status='EXACT-LITERAL-GLUING-AND-NINE-FAILURES-PASS',
        script_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
        source_sha256=sha256((W/'main_glued_terminal_interfaces.json').read_bytes()).hexdigest(),
        canonical_atoms=atoms,total_mass=str(total),network_atom_margins=len(own_net),
        root_atom_margins=len(own_root),literal_original_payoff_evaluations=literal_evaluations,
        failed_queries=[dict(query=row['query'],slack=str(s),slack_float=float(s)) for row,s in zip(failed,slacks)],
        scope='Rejects exactly the explicit conditional-product gluing; does not reject every coupling or the fixed old point.')
    target=W/'main_glued_terminal_failures_audit.json';assert not target.exists()
    target.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='failed_queries'},ensure_ascii=False))


if __name__=='__main__':main()
