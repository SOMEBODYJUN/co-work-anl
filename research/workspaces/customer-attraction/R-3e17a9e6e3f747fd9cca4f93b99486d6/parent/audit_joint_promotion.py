"""Parent audit: reconstruct new first-follower rows independently of author.

Old 1143 raw families use their frozen old implementation and are explicitly
not claimed to be independently rederived here. New 88 rows, conditional DE
masses and objective are calculated directly. No discovery program is imported.
"""
from pathlib import Path
from itertools import product,combinations_with_replacement
from fractions import Fraction as F
import hashlib,json,sys

HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'work.py').exists())
POINT=HERE.parent/'astra/promotion_joint_atoms_exact.json'
OLD=ROOT/'research/workspaces/customer-attraction/R-a8ee6fdb155c47da95540775b4a6a2db/closure'
WORDS=tuple(product((0,1),repeat=3))

def share(a,d):return F(a,d) if a else F()
def potential(p,x,y):return F(x+y,p+1)-F(x*y,(p+1)*(p+2))
def pairbudget(p,d,e):return share(d+e,p+d+e)+F(d,(p+1)*(p+2))

QUERIES=('T','B','C')+tuple('a'+str(i) for i in range(6))
PAIR_QUERIES=tuple(combinations_with_replacement(QUERIES,2))
NAMES=['source','oldpair-newpair']+['oldC:'+v for v in ('D','E')]
NAMES+=['newE:'+v for v in ('T','B','C','D','E','opt','oldB','oldC')+tuple('a'+str(i) for i in range(6))]
NAMES+=['pair:'+str(v) for v in PAIR_QUERIES]+['pair:opt','pair:Topt','pair:Bopt','pair:Copt']
NAMES+=['price:'+v+':'+str(i) for v in ('D','E') for i in range(6)]
NAMES+=['capacity:D','capacity:E']
ACTUAL_PAIRS=(('D','E'),('B','D'),('B','E'),('C','D'),('C','E'),('T','D'),('T','E'))
NAMES+=['actualpair:'+str(v) for v in ACTUAL_PAIRS]

def rows(a,h,w,de):
    p=sum(a[:3]);t,b,c=w;d,e=de;s=sum(a);bg=p+b
    nT=sum(n*word[0] for n,word in zip(h,WORDS));nB=sum(n*word[1] for n,word in zip(h,WORDS));nC=sum(n*word[2] for n,word in zip(h,WORDS))
    mem={'T':F(t),'B':F(b),'C':F(c),'D':F(d),'E':F(e),'opt':F(nT,6),'oldB':F(nB,6),'oldC':F(nC,6)}
    mem.update({'a'+str(i):F(a[i]) for i in range(6)})
    newbudget=pairbudget(bg,d,e)
    out=[share(a[3],s)-share(b,p+b+d+e),pairbudget(p+t,b,c)-potential(p+t,d,e)]
    out.extend(share(c,p+t+b+c)-F(mem[x],p+t+b+1) for x in ('D','E'))
    out.extend(share(e,p+b+d+e)-F(mem[x],p+b+d+1) for x in ('T','B','C','D','E','opt','oldB','oldC')+tuple('a'+str(i) for i in range(6)))
    out.extend(newbudget-potential(bg,mem[x],mem[y]) for x,y in PAIR_QUERIES)
    out.append(newbudget-F(nT,3*(bg+1))+F(nT*(nT-1),30*(bg+1)*(bg+2)))
    out.extend(newbudget-potential(bg,mem[x],F(nT,6)) for x in ('T','B','C'))
    out.extend(share(a[i],s)-F(mem[x],sum(a[:i])+6-i) for x in ('D','E') for i in range(6))
    out.extend((-F(d),-F(e)))
    out.extend(pairbudget(sum(a[:4]),a[4],a[5])-potential(sum(a[:4]),mem[x],mem[y]) for x,y in ACTUAL_PAIRS)
    assert len(out)==len(NAMES)==88
    return out


def main():
    point=json.loads(POINT.read_text());nh=len(point['histograms']);masses=[F()]*nh;W=O=F()
    for atom in point['RZ_atoms']:
        i=atom['hist_index'];v=F(atom['weight']);assert v>0;masses[i]+=v
    states={};groups=[]
    for i,h in enumerate(point['histograms']):
        for wi,n in enumerate(h['hist']):
            if n:groups.append((i,wi));states[i,wi]={de:F() for de in product((0,1),repeat=2)}
    for row in point['promotion_states']:
        key=(row['hist_index'],row['word_index']);de=tuple(row['DE']);v=F(row['weight'])
        assert key in states and de!=(0,0) and v>0
        states[key][de]+=v
    state_slacks=[]
    for (i,wi),vals in states.items():
        vals[0,0]=masses[i]-sum(vals.values());assert min(vals.values())>=0
        assert sum(vals.values())==masses[i];state_slacks.append(vals[0,0])
    K=F(point['K']);new=[6*K if name.startswith('capacity:') else F() for name in NAMES]
    for i,h in enumerate(point['histograms']):
        a=tuple(map(int,h['actual_bits']));assert sum(h['hist'])==6
        W+=masses[i]*int(any(a));O+=masses[i]*int(h['d']>0)
        for wi,n in enumerate(h['hist']):
            if not n:continue
            for de,v in states[i,wi].items():
                if v:
                    vals=rows(a,h['hist'],WORDS[wi],de)
                    new=[x+n*v*y for x,y in zip(new,vals)]
    assert min(new)>=0,(NAMES[new.index(min(new))],min(new))
    assert W==F(point['W']) and O==1 and 2*W<1
    # The old verifier is explicitly a reused dependency, not this audit's new
    # independent mathematical content.
    sys.path.insert(0,str(OLD));import joint_atoms as old
    oldnames,oldK,locs=old.model()
    assert [loc['hist'] for loc in locs]==point['histograms']
    oldslack=[K*v for v in oldK]
    for atom in point['RZ_atoms']:
        v=F(atom['weight']);vals=old.atom(locs[atom['hist_index']],atom['R'],atom['Z'],True)
        oldslack=[x+v*y for x,y in zip(oldslack,vals)]
    assert len(oldslack)==1143 and min(oldslack)>=0
    report={'status':'EXACT_FEASIBLE_SPECIFIED_NECESSARY_SYSTEM_NOT_SPE','target_status':'OPEN',
            'point_sha256':hashlib.sha256(POINT.read_bytes()).hexdigest(),
            'RZ_atoms':len(point['RZ_atoms']),'positive_nonzero_DE_states':len(point['promotion_states']),
            'old_raw_rows_reused':len(oldslack),'new_raw_rows_independently_rebuilt':len(new),
            'conditional_mass_bounds':len(groups),'total_rows':len(oldslack)+len(new)+len(groups),
            'minimum_old_slack':str(min(oldslack)),'minimum_new_slack':str(min(new)),
            'minimum_unassigned_00_mass':str(min(state_slacks)),
            'O':str(O),'W':str(W),'strict_half_gap':str(1-2*W),'K':str(K),
            'new_row_slacks':{name:str(v) for name,v in zip(NAMES,new)},
            'joint_realizability':'For each positive histogram mass n, couple its RZ law and all DE group laws by conditional product. All marginals and listed rows preserved. This is a common customer-membership distribution, not an SPE strategy.'}
    (HERE/'audit_joint_promotion.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='new_row_slacks'},indent=2))

if __name__=='__main__':main()
