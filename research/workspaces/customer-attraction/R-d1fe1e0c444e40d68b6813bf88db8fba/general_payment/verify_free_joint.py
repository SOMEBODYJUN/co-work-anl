"""Independent literal expansion and exact saved-cut replay; no optimizer."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
import free_joint as gen

HERE=Path(__file__).resolve().parent

def sh(n,d):return F(n,d) if n else F(0)

def literal_features(p,ell,t,q,first,second):
    b,c=first[-2:];j,v=second[-2:]
    s=sum(first[:-2]);ss=sum(second[:-2])
    den1=p+t+sum(first);den2=p+c+sum(second)
    mem={'t':t,'q':q,'b':b,'c':c,'j':j,'v':v}
    answer=[]
    for name in gen.NAMES:
        kind,label=(name.split(':')+[''])[:2]
        if name=='sourceT':answer.append(sh(t,den1))
        elif name=='sourceC':answer.append(sh(c,den2))
        elif kind=='price':answer.append(F(s if label=='s' else ss if label=='ss' else mem[label],ell+1))
        elif kind=='cap':answer.append(F(s if label=='s' else ss if label=='ss' else mem[label]))
        elif kind=='last1':answer.append(F(mem[label],p+t+sum(first[:-1])+1)-sh(c,den1))
        elif kind=='last2':answer.append(F(mem[label],p+c+sum(second[:-1])+1)-sh(v,den2))
        elif kind=='safeB':answer.append(F(mem[label],p+t+sum(first[:-2])+2)-sh(b,den1))
        elif kind=='safeJ':answer.append(F(mem[label],p+c+sum(second[:-2])+2)-sh(j,den2))
        else:raise AssertionError(name)
    return tuple(answer)

def main():
    data=json.loads((HERE/'compact_cuts.json').read_text());m=6
    types=[(a,d) for a in product((0,1),repeat=m) for d in range(m+1)]
    n=gen.decode(data['input'],types)
    # Literal hidden arrays vs the generator's count-compressed state set.
    # Sets are sufficient: repeated states do not change a minimum.
    local_states=0
    for k in range(3,7):
        arrays=list(product((0,1),repeat=k-1))
        for p,ell,t,q in product(range(m-k+1),range(m),(0,1),(0,1)):
            literal={literal_features(p,ell,t,q,f,g) for f in arrays for g in arrays}
            compressed=set(gen.states(k,p,ell,t,q))
            assert literal==compressed,(k,p,ell,t,q)
            local_states+=len(literal)
    # The previously published fixed requery is exactly a member of this cone.
    original={'sourceT':F(2),'sourceC':F(3,2),'last1:q':F(1),'last2:b':F(1,2),'price:j':F(1,4),'price:v':F(5,12),'cap:v':F(1,12)}
    match=0
    for k in range(3,7):
        for p,ell,t,q in product(range(m-k+1),range(m),(0,1),(0,1)):
            got=min(sum(original.get(name,0)*coef for name,coef in zip(gen.NAMES,state)) for state in gen.states(k,p,ell,t,q))
            expected=min(sh(2*t-c,p+t+s+b+c)+sh(3*c-v,2*(p+c+ss+j+v))+F(b,2*(p+c+ss+j+1))+F(j,4*(ell+1))+F(5*v,12*(ell+1))+F(v,12)+F(q,p+t+s+b+1)
                         for b,c,j,v in product((0,1),repeat=4) for s,ss in product(range(k-2),repeat=2))
            assert got==expected;match+=1
    cuts=[]
    for index,cut in enumerate(data['cuts']):
        weights=gen.weight_map(cut);assert min(weights)>=0
        name,row=gen.make_row(types,m,gen.rawcut(cut))
        slack=sum(x*y for x,y in zip(row,n))
        assert slack==F(cut['at_input_slack']) and slack<0
        cuts.append({'index':index,'k':cut['k'],'T':cut['T'],'Q':cut['Q'],'slack':str(slack)})
    report={'scope':'exact local compiler and separation replay; not six-player half or SPE counterexample','parameters':len(gen.NAMES),'count_compressed_feature_states':local_states,'fixed_requery_matches':match,'full_six_external_types_per_row':len(types),'exact_negative_cuts':cuts,'all_checks_passed':True}
    (HERE/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='exact_negative_cuts'},indent=2))

if __name__=='__main__':main()
