"""Definition-level independent shared-matching audit of the727-row optimum.

No discovery transport/pricing formula imported. Enumerates every distinct
label-preserving per-client matching and literally sums both ordered offdiagonal
last-player comparisons. This checks a necessary envelope, never a full SPE.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product, permutations
import hashlib
import json

HERE=Path(__file__).resolve().parent
ACTOR=HERE.parent


def expand(atom, field, arity):
    states=[s for s,n in zip(product((0,1),repeat=arity),atom[field]) for _ in range(n)]
    assert len(states)==5
    return states


def matchings(target):
    parts=[tuple(s for s in target if s[0]==t) for t in (0,1)]
    for first in set(permutations(parts[0])):
        for second in set(permutations(parts[1])):
            yield first+second


def audit():
    source=ACTOR/'round5_pricing/exact_optimum_primal_terminal_cross.json'
    cert=json.loads(source.read_text())
    separate=[F(0),F(0)]
    joint=F(0)
    count=0
    tight_atoms=0
    for atom in cert['atoms']:
        bits=dict(zip('ABCDEUVWXY',map(int,atom['bits'])))
        src=expand(atom,'AB_hist',3)
        target=expand(atom,'second_hist',4)
        assert [s[0] for s in src]==[s[0] for s in target]
        values=[]
        for assigned in matchings(target):
            count+=1
            sums=[F(0),F(0)]
            for i,s in enumerate(src):
                den=bits['A']+bits['B']+s[0]+s[1]+1
                for j,t in enumerate(assigned):
                    if i!=j:
                        sums[0]+=F(s[2]-t[2],den)
                        sums[1]+=F(s[2]-t[3],den)
            values.append(sums)
        maxima=[max(v[k] for v in values) for k in (0,1)]
        together=max(sum(v) for v in values)
        assert together<=sum(maxima)
        tight_atoms+=together==sum(maxima)
        mass=F(atom['exact_mass'])
        for k in (0,1):
            separate[k]+=mass*maxima[k]
        joint+=mass*together
    assert min(separate)>0 and joint<0
    expected=json.loads((ACTOR/'round5_coupling/exact_joint_727_separation.json').read_text())
    assert joint==F(expected['joint_slack'])
    assert separate==list(map(F,expected['separate_component_slacks']))
    return {'scope':'Independent necessary shared-matching envelope; no generalhalf/SPE claim',
            'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
            'positive_atoms':len(cert['atoms']),'literal_distinct_matchings':count,
            'strict_atoms':len(cert['atoms'])-tight_atoms,
            'separate_slacks':list(map(str,separate)),
            'joint_slack':str(joint),'joint_slack_float':float(joint),
            'reported_slacks_equal_independent_literal_reconstruction':True}


if __name__=='__main__':
    result=audit()
    (HERE/'audit_joint_matching.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
