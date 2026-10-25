"""Independent standard-library reconstruction of supported row coefficients.

Does not import discovery code, SciPy, or a game/SPE solver. This is an internal
independent implementation, not external peer review or a HALF(5) proof.
"""
from fractions import Fraction as F
from itertools import product,combinations_with_replacement
from pathlib import Path
import json,hashlib
HERE=Path(__file__).resolve().parent
T=((F(0),F(960),F(1220),F(1480),F(1740),F(2000)),
   (F(0),F(1665,4),F(2745,4),F(3785,4),F(4825,4),F(5865,4)),
   (F(0),F(320),F(524),F(728),F(932),F(1136)))
def share(z,l):return F(z,l) if z else F()

def short_rows(b,d):
    u=[share(z,sum(b)) for z in b];p=sum(b[:3]);h=u[3]+u[4]+F(b[3],(p+1)*(p+2))
    out={f'size:{j}':F(b[0]-b[j]) for j in range(1,5)}
    out['size:opt']=F(5*b[0]-d)
    for i in range(1,5):
        pref=sum(b[:i]);rem=5-i
        for j in range(5):out[f'IC:{i}:{j}']=u[i]-F(b[j],pref+rem)
        out[f'opt:{i}']=5*u[i]-F(d,pref+rem)
    out['r2:O']=F(5,2)*h+F(p,p+1)-int(d>0)
    out['r2:opt']=10*h-F(d*(5-d),p+1)-F(d*(d-1),p+2)
    for i,j in combinations_with_replacement(range(5),2):
        out[f'r2:pair:{i}:{j}']=h-F(b[i]+b[j]-2*b[i]*b[j],p+1)-F(2*b[i]*b[j],p+2)
    p=sum(b[:2])
    for j in range(5):out[f'trueH:repeat:{j}']=17040*u[2]+1085*b[0]-F(13395*b[j],p+3)-T[p][d]
    out['trueH:opt']=17040*u[2]+1085*b[0]-F(2679*d,p+3)-T[p][d]
    return out

def old_and_new_envelopes():
    old=HERE.parent/'five_only'/'maxroot_envelope.json';new=HERE/'envelope.json';out=[]
    for path,key in [(old,'records'),(new,'sampled_exact_lines')]:
        data=json.loads(path.read_text());seen=set()
        for rec in data[key]:
            B,C=F(rec['B']),F(rec['C']);weights={n:F(w) for n,w in rec['multipliers'].items() if n!='root-IC'}
            if (B,C,tuple(weights.items())) in seen:continue
            seen.add((B,C,tuple(weights.items())));assert min(weights.values())>=0
            residuals=[]
            for b in product((0,1),repeat=5):
                for d in range(6):
                    residual=B*share(b[0],sum(b))-C*b[0]-int(d>0)-sum((w*short_rows(b,d)[n] for n,w in weights.items()),F())
                    assert residual>=0,(path.name,B,C,b,d,residual);residuals.append(residual)
            out.append({'source':path.name,'B':str(B),'C':str(C),'states':len(residuals),'minimum_residual':str(min(residuals)),'zero_residuals':sum(z==0 for z in residuals)})
    return out

def seven_row_projection():
    count=0;minimum=None
    for p in range(3):
        for d in range(6):
            vals=[]
            for h,q,r in product((0,1),repeat=3):
                n=p+h+q+r;vh,vq,vr=[share(z,n) for z in (h,q,r)]
                tax=vq+vr+F(q,(p+h+1)*(p+h+2))
                val=(-17040*vh+9000*F(h-q,p+3)+10080*F(h-r,p+3)
                     +600*(5*vr-F(d,p+h+q+1))-1085*h
                     +360*(5*tax-F(5*r+d-2*r*d,p+h+1)-F(2*r*d,p+h+2))
                     +2679*F(5*h,p+3))
                gap=-T[p][d]-val;assert gap>=0;count+=1
                minimum=gap if minimum is None else min(minimum,gap);vals.append(val)
            assert max(vals)==-T[p][d]
    return {'states':count,'minimum_residual':str(minimum)}

def joint_rows(b,d):
    paths=(tuple(range(5)),tuple(range(5,10)));out={};u=[]
    for path in paths:u.append([share(b[i],sum(b[j] for j in path)) for i in path])
    out['root-to-max']=u[0][0]-u[1][0]
    for i in range(10):out[f'max-size:{i}']=F(b[5]-b[i])
    out['max-size:opt']=F(5*b[5]-d)
    for tag,path in enumerate(paths):
        for pos in range(tag,5):
            p=sum(b[i] for i in path[:pos]);k=5-pos
            for j in range(10):out[f'{tag}:IC:{pos}:{j}']=u[tag][pos]-F(b[j],p+k)
            out[f'{tag}:opt:{pos}']=5*u[tag][pos]-F(d,p+k)
            out[f'{tag}:O:{pos}']=5*k*u[tag][pos]+F(p,p+k)-int(d>0)
        p=sum(b[i] for i in path[:3]);H=u[tag][3]+u[tag][4]+F(b[path[3]],(p+1)*(p+2))
        out[f'{tag}:r2:O']=F(5,2)*H+F(p,p+1)-int(d>0)
        out[f'{tag}:r2:opt']=10*H-F(d*(5-d),p+1)-F(d*(d-1),p+2)
        for j,k in combinations_with_replacement(range(10),2):
            x,y=b[j],b[k];out[f'{tag}:r2:pair:{j}:{k}']=H-F(x+y-2*x*y,p+1)-F(2*x*y,p+2)
        p=sum(b[i] for i in path[:2]);g3=F(d*(5-d)*(4-d),2*(p+1))+F(d*(d-1)*(5-d),p+2)+F(d*(d-1)*(d-2),2*(p+3))
        out[f'{tag}:r3:opt']=50*sum(u[tag][2:])-3*g3
        p=b[path[0]];g4=share(d*(d-1),p+d-1)+share((5-d)*d,p+d)
        out[f'{tag}:r4:opt']=7495*sum(u[tag][1:])-750*g4
        out[f'{tag}:r4:binary']=29985*sum(u[tag][1:])-4985*(p-u[tag][0])-3000*g4
        p=sum(b[i] for i in path[:2]);uu=u[tag][2]
        for j in range(10):out[f'TrueH:{tag}:repeat:{j}']=17040*uu+1085*b[5]-F(13395*b[j],p+3)-T[p][d]
        out[f'TrueH:{tag}:opt']=17040*uu+1085*b[5]-F(2679*d,p+3)-T[p][d]
    for i,(B,C) in enumerate(((F(80),F(71,5)),(F(70),F(423,35)),(F(1920,29),F(11393,1015)),(F(5840,91),F(2627,245)))):
        out[f'weighted_root:{i}']=B*u[0][0]-C*b[5]-int(d>0)
    assert len(out)==266
    return out

def joint_witness(path):
    src=json.loads(path.read_text());slacks=None;W=O=F()
    for atom in src['atoms']:
        b=tuple(atom['bits']);d=atom['d'];mass=F(atom['mass']);assert mass>=0
        rr=joint_rows(b,d)
        if slacks is None:slacks={n:F() for n in rr}
        for n,z in rr.items():slacks[n]+=mass*z
        W+=mass*int(any(b[:5]));O+=mass*int(d>0)
    assert min(slacks.values())>=0 and O>2*W
    assert (str(W),str(O))==(src['W'],src['O'])
    assert slacks=={n:F(z) for n,z in src['slacks'].items()}
    return {'source':path.name,'support_atoms':len(src['atoms']),'rows':len(slacks),'W':str(W),'O':str(O),'O_minus_2W':str(O-2*W),'minimum_slack':str(min(slacks.values()))}

def weighted_constants():
    weights=((F(0),F(0),F(0),F(1)),(F(0),F(0),F(1,7),F(6,7)),(F(0),F(14,203),F(27,203),F(162,203)),(F(28,637),F(42,637),F(81,637),F(486,637)))
    out=[]
    for w in weights:
        assert sum(w)==1;ts=(4,3,2,1);c=sum(t*z for t,z in zip(ts,w))
        aa=[F(3,4)*ts[j]*w[j]+sum((w[i]/(ts[i]+1) for i in range(j+1,4)),F()) for j in range(4)]
        a=max(aa);out.append({'B':str(5*c+100*a),'C':str(20*a+c/5-1)})
    return out

def run():
    paths=[HERE/'joint_obstruction.json']
    if (HERE/'joint_obstruction_integer.json').exists():paths.append(HERE/'joint_obstruction_integer.json')
    out={'status':'passed','scope':__doc__,'envelopes':old_and_new_envelopes(),'trueH':seven_row_projection(),
         'weighted_root_constants':weighted_constants(),'joint_witnesses':[joint_witness(p) for p in paths],
         'sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [HERE/'envelope.json']+paths}}
    HERE.joinpath('audit.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))

if __name__=='__main__':run()
