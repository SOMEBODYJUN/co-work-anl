"""Exact one-prefix shifts of the ACTIVE local five-player components.

All weights are frozen source weights.  The extra load is b=0 or b=1;
all share/floor/tax denominators include it.  We minimize only over the
hidden membership bits of the same genuine histories used in the source.
No assertion here identifies arbitrary types with a realizable game.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib, json
from math import floor, ceil

OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[3]
SRC=ROOT/'archives/customer-attraction/tools/half5-exact'
COMP=SRC/'components'
M=10**6

def q(n,d): return F(n,d) if n else F(0)
def states(names):
    for bits in product((0,1),repeat=len(names)):
        yield dict(zip(names,bits))
def binary(v,names):
    r=0
    for n in names: r=2*r+v[n]
    return r
def read(n):return json.loads((COMP/n).read_text())
def weights(c): return {k:F(v) for k,v in c.get('multipliers',c.get('weights')).items()}

def local_value(family,v,key,b):
    z=key.split(':')
    if z[0]=='CAP':return F(v[z[1]])
    if family=='DEEP':
        paths=('TABCD','TAQEF','TABQG','TQHIJ')
        def sh(path,i):return q(v[path[i]],b+sum(v[s] for s in path))
        if key=='ROOT':return sh('TABCD',0)
        if key.startswith('TRUE'):
            i=int(key[-1])-1
            return sh({1:'TQHIJ',2:'TAQEF',3:'TABQG'}[i],i)-sh('TABCD',i)
        if z[0]=='IC':
            pref,own,query=z[1:];path=next(p for p in paths if p.startswith(pref+own));i=len(pref)
            assert i>={'TABCD':1,'TAQEF':3,'TABQG':4,'TQHIJ':2}[path]
            return q(v[query],b+sum(v[s] for s in pref)+5-i)-sh(path,i)
        if z[0]=='TAX':
            pref,query=z[1:];path=next(p for p in paths if p.startswith(pref))
            assert len(pref)==3 and path!='TABQG'
            p=b+sum(v[s] for s in pref);n=sum(v[s] for s in query)
            H=sh(path,3)+sh(path,4)+q(v[path[3]],(p+1)*(p+2))
            return q(n,p+n)-H
    if family=='BG2':
        paths=('TBCD','TQEF','TBQG')
        def sh(path,i):return q(v[path[i]],b+v['A']+sum(v[s] for s in path))
        if key=='FORCED':return sh('TBCD',0)
        if key=='TRUE3':return sh('TQEF',1)-sh('TBCD',1)
        if key=='TRUE4':return sh('TBQG',2)-sh('TBCD',2)
        if z[0]=='IC':
            pref,own,query=z[1:];path=next(p for p in paths if p.startswith(pref+own));i=len(pref)
            assert i>={'TBCD':1,'TQEF':2,'TBQG':3}[path]
            return q(v[query],b+v['A']+sum(v[s] for s in pref)+4-i)-sh(path,i)
    if family in ('PC2','PC3'):
        if family=='PC2':
            paths={'init':'TEFG','third':'TQHI','fourth':'TEQJ'};pre=v['A'];r=4
            first={'init':1,'third':2,'fourth':3}
        else:
            paths={'init':'TEF','query':'TQG','copy':'TFH'};pre=v['A']+v['B'];r=3
            first={'init':1,'query':2,'copy':2}
        def sh(tag,i):return q(v[paths[tag][i]],b+pre+sum(v[s] for s in paths[tag]))
        if key=='FORCED':return sh('init',0)
        if z[0]=='ACTUAL':
            i=int(z[1])-1
            return q(v[z[2]],b+sum(v[s] for s in 'ABCD'[:i])+5-i)
        if z[0]=='IC':
            tag,i,query=z[1],int(z[2]),z[3];assert i>=first[tag]
            return q(v[query],b+pre+sum(v[s] for s in paths[tag][:i])+r-i)-sh(tag,i)
        if key=='TRUE3':return sh('third',1)-sh('init',1)
        if key=='TRUE4':return sh('fourth',2)-sh('init',2)
        if key=='TRUE4-F':return sh('copy',1)-sh('init',1)
        if key=='TRUE4-Q':return sh('query',1)-sh('init',1)
    raise AssertionError((family,key))

def minima(family,c,names,visible,b):
    lam=weights(c)
    if family!='DEEP':lam={'FORCED':F(1),**lam}
    vals=[None]*(2**len(visible));arg=[None]*len(vals)
    for v in states(names):
        val=sum(w*local_value(family,v,k,b) for k,w in lam.items())
        i=binary(v,visible)
        if vals[i] is None or val<vals[i]: vals[i]=val;arg[i]=''.join(str(v[s]) for s in names)
    return vals,arg

def maxroot(c,b,mode):
    """mode=profit uses internal-prefix tax p/(b+p+1).
    mode=coverage uses full-prefix tax (b+p)/(b+p+1).
    Both pairO comparisons below are valid for binary b (see report proof).
    """
    lam=weights(c);B,C=F(c['B']),F(c['C'])
    paths={'actual':'ABCD','root':'DQRS','second':'ADXY'}
    rows=[]
    for v in states('TABCDQRSXY'):
        def sh(tag,i):return q(v[paths[tag][i]],b+v['T']+sum(v[s] for s in paths[tag]))
        def raw(key):
            z=key.split(':')
            if z[0]=='CAP':return F(v['T']-v[z[1]])
            if z[0]=='copy':
                i={'root':0,'second':1}[z[1]];return sh('actual',i)-sh(z[1],i)
            tag=z[0];path=paths[tag]
            if z[1].isdigit():
                i=int(z[1]);assert i>={'actual':0,'root':1,'second':2}[tag]
                return sh(tag,i)-q(v[z[3]],b+v['T']+sum(v[s] for s in path[:i])+4-i)
            if z[1]=='pairO':
                p=v['T']+v[path[0]]+v[path[1]];h=b+p
                H=sh(tag,2)+sh(tag,3)+q(v[path[2]],(h+1)*(h+2))
                return F(5,2)*H+q(p+(b if mode=='coverage' else 0),b+p+1)
            if z[1]=='lastO':
                p=v['T']+sum(v[s] for s in path[:3])
                return 5*sh(tag,3)+q(p+(b if mode=='coverage' else 0),b+p+1)
            raise AssertionError(key)
        vT=q(v['T'],b+sum(v[s] for s in 'TABCD'))
        rho=B*vT+C*v['T']-sum(w*raw(k) for k,w in lam.items())
        rows.append({'bits':''.join(str(v[s]) for s in 'TABCDQRSXY'),'rho':str(rho)})
    return rows

def main():
    result={'source_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in COMP.glob('*.json')},'components':[]}
    specs=[('DEEP','deep_root_query.json',[0],'TABCDEFGQHIJ','TQ'),
           ('BG2','background_player2.json',[0,3,11],'ATQBCDEFG','ATQ'),
           ('PC2','priced_player2.json',[0,1,2,3],'ABCDTQEFGHIJ','ABCDTQ'),
           ('PC3','priced_player3.json',[0,1,2],'ABCDTQEFGH','ABCDTQ')]
    for family,file,ids,names,vis in specs:
        data=read(file)
        for i in ids:
            c=data[i];v0,a0=minima(family,c,names,vis,0);v1,a1=minima(family,c,names,vis,1)
            if family=='DEEP':
                g,z=F(c['gamma']),F(c['zeta'])
                old=[F(0),F(1),-g,-g-z]
            elif family=='BG2':old=[F(0)]+[F(x) for x in c['margin_coefs']]
            else:old=[F(x) for x in c.get('gamma',c.get('gamma_ABCDTQ'))]
            assert all(x>=y for x,y in zip(v0,old))
            # p=0 is the original source lower envelope.  p=1 retains the
            # same source slack margin, hence changes only physical shares.
            shifted=[o+y-x for o,x,y in zip(old,v0,v1)]
            result['components'].append({'family':family,'source_index':i,'names':names,'visible':vis,'old_gamma':[str(x) for x in old],
                'min_b0':[str(x) for x in v0],'min_b1':[str(x) for x in v1],
                'gamma_b1':[str(x) for x in shifted],
                'gamma_b1_floor_million':[floor(M*x) for x in shifted],
                'argmin_b0':a0,'argmin_b1':a1,
                'max_gamma_drop':str(max(x-y for x,y in zip(old,shifted)))})
    c=read('maxroot_four_copy.json')[0]
    result['maxroot']={}
    for mode in ('profit','coverage'):
        r0=maxroot(c,0,mode);r1=maxroot(c,1,mode)
        assert min(F(r['rho']) for r in r0)==0
        mn=min(F(r['rho']) for r in r1)
        result['maxroot'][mode]={'b0_min':'0','b1_min':str(mn),'charge_floor_million':floor(M*mn),'b1_rows':r1,
            'min_by_TABCD':{''.join(map(str,bits)):str(min(F(r['rho']) for r in r1 if r['bits'].startswith(''.join(map(str,bits))))) for bits in product((0,1),repeat=5)}}
    # Exact finite coefficient checks for the generalized five-slot profit
    # lastO and pairO rows, all possible internal prefixes (0..4 or 0..3).
    checks=[]
    for b in (0,1):
        for p in range(5):
            for d in range(6):
                last=q(d+p,b+p+1)-q(d,b+d)
                assert last>=0
                if p<4:
                    pair=(q(d*(5-d),b+p+1)+q(d*(d-1),b+p+2))/4+q(p,b+p+1)-q(d,b+d)
                    assert pair>=0
                else:pair=None
                checks.append({'b':b,'p':p,'d':d,'last_remainder':str(last),'pair_remainder':str(pair) if pair is not None else None})
    result['profit_aggregate_rows_check']=checks
    (OUT/'shifted_local_tables.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'components':[(r['family'],r['source_index'],r['max_gamma_drop']) for r in result['components']],
        'maxroot':{k:{i:v for i,v in r.items() if i not in ('b1_rows','min_by_TABCD')} for k,r in result['maxroot'].items()}},indent=2))

if __name__=='__main__':main()
