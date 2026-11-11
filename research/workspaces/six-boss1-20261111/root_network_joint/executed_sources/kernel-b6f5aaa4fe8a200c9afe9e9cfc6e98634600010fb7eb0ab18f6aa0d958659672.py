"""Stream the audited, FAILED conditional-product test law, exactly.

canonical_atoms() has 3,086 items.  labelled_atoms() has 2,221,920 items,
including permutation multiplicities.  This is a common coverage measure
with the pinned margins; it violates seven required IC rows and is not a
completion certificate.  No file is written by importing or running here.
"""
from collections import defaultdict
from fractions import Fraction as F
from itertools import product,permutations
from pathlib import Path
import hashlib,json

BASE=Path(__file__).resolve().parent.parent
INPUTS={
 'union_augmented_lp/augmented_lp_exact.json':'b0ca65cfe61e5e3ef09537cba2a986c171aeaa7106f673077f803c80ee2b68e3',
 'root_marginal_closure/marginal_completion_exact.json':'9866e82bbc40e661d15d4aee3a4472fd99137ade5a9fa7fd0872f6344ffe0966',
 'fifth_reply_common/common_atoms_with_D.json':'91599404ee03184bbb072767d7d55761b95bcc89e1d55e748aebf2ee60f19c54',
}


def read():
    out=[]
    for name,pin in INPUTS.items():
        data=(BASE/name).read_bytes();assert hashlib.sha256(data).hexdigest()==pin
        out.append(json.loads(data))
    return out


def canonical_atoms():
    point,mu,net=read();marg=defaultdict(dict)
    for r in mu['positive_states']:marg[r['hist'],r['old_word']][r['state']]=F(r['mass'])
    for block in net['blocks']:
        h=block['hist_column'];H=F(point['columns'][h]['weight'])
        old=tuple(w for w,n in enumerate(block['hist']) for _ in range(n))
        for ai,atom in enumerate(block['atoms']):
            for new in product(*(sorted(marg[h,w]) for w in old)):
                mass=F(atom['mass'])
                for w,s in zip(old,new):mass*=marg[h,w][s]/H
                yield dict(hist=h,network_atom=ai,actual=block['actual_bits'],old_words=old,new_words=new,
                           mass=mass,RZ_states=tuple(atom['states']),B4_state=tuple(atom['B4_state']),D_bits=tuple(atom['D_bits']))


def labelled_atoms():
    nodes=tuple(e for e in product(range(2),range(6),range(6)) if e[0] or e[1]!=e[2]);index={e:j for j,e in enumerate(nodes)}
    for atom in canonical_atoms():
        for pi in permutations(range(6)):
            old=[0]*6;new=[0]*6;D=[0]*6;RZ=[0]*66
            for i in range(6):
                old[pi[i]]=atom['old_words'][i];new[pi[i]]=atom['new_words'][i];D[pi[i]]=atom['D_bits'][i]
            for ei,(f,j,k) in enumerate(nodes):RZ[index[f,pi[j],pi[k]]]=atom['RZ_states'][ei]
            yield dict(hist=atom['hist'],network_atom=atom['network_atom'],permutation=pi,
                actual=atom['actual'],old_words=tuple(old),new_words=tuple(new),mass=atom['mass']/720,
                RZ_states=tuple(RZ),B4_state=atom['B4_state'],D_bits=tuple(D))


if __name__=='__main__':
    count=0;total=F()
    for atom in canonical_atoms():count+=1;total+=atom['mass']
    assert count==3086 and total==1
    print(json.dumps(dict(scope='FAILED test law, not a feasible completion',canonical_atoms=count,
                          S6_copies=count*720,total_mass=str(total))))
