"""Direct literal-index audit of every saved extremal 53-row witness.

Does not import either coefficient constructor or the frozen verifier.
The complete maximization still belongs to shift_certificate.py; this second
calculation checks its chosen maximizers and all shared K columns directly.
It also records the exact six-slot averaging identity and diagnoses the given
necessary-LP point, without treating that point as an SPE.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
from math import ceil,floor
import hashlib,json

OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[3]
SRC=ROOT/'archives/customer-attraction/tools/half5-exact';COMP=SRC/'components'
M=10**6;D=10**22
PATHS={'actual':'ABCDE','second':'AEUVW','third':'ABEXY'}
LABELS='ABCDEUVWXY'
def q(n,d):return F(n,d) if n else F(0)
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
CERT=load(SRC/'certificate.json');WEIGHTS={k:int(v) for k,v in CERT['integer_multipliers'].items()}
SHIFT=load(OUT/'shifted_local_tables.json')
TABS={(r['family'],r['source_index']):r for r in SHIFT['components']}
RAW={k:load(COMP/v) for k,v in {'BG':'background_player2.json','PC2':'priced_player2.json','PC3':'priced_player3.json','DEEP':'deep_root_query.json'}.items()}

def literal_row(name,bits,d,menus,families,b,mode):
    z=name.split(':');tag=z[0]
    def sh(path,i):return q(bits[path[i]],b+sum(bits[c] for c in path))
    def target():return q(d,b+d) if mode=='profit' else F(d>0)
    def local(kind,e,t,v):
        if kind=='BG':
            idx={0:0,2:3,4:11}[e];c=RAW['BG'][idx]
            gamma=TABS['BG2',idx]['gamma_b1_floor_million'] if b else [0]+[floor(M*F(x)) for x in c['margin_coefs']]
            kap=ceil(M*F(c['Kcoef']));val=M*sh('ABCDE',1)-gamma[4*bits['A']+2*t+v]
        else:
            family='PC2' if e<5 else 'PC3';idx=e if e<5 else e-5;c=RAW[family][idx]
            gamma=TABS[family,idx]['gamma_b1_floor_million'] if b else [floor(M*F(x)) for x in c.get('gamma',c.get('gamma_ABCDTQ'))]
            uc=[ceil(M*F(x)) for x in c.get('u_coefs',c.get('u_coefficients'))]
            if 'u_coefs' in c:uc[1]+=M
            kap=ceil(M*F(c['Kcoef']));ii=32*bits['A']+16*bits['B']+8*bits['C']+4*bits['D']+2*t+v
            val=sum(uc[i]*sh('ABCDE',i) for i in range(5))-gamma[ii]
        return val,kap
    if tag in ('BG','PC'):
        return local(tag,int(z[1]),bits[LABELS[int(z[2])]],bits[LABELS[int(z[3])]])
    if tag=='MAX':return -F(bits[LABELS[int(z[2])]]),F(1)
    if name=='MAXROOT-NEW':
        fee=SHIFT['maxroot'][mode]['charge_floor_million'] if b else 0
        return 46313177*sh('ABCDE',0)-M*target()-fee,F(-7412362)
    if tag=='DEEP':
        c=RAW['DEEP'][int(z[1])];a,k,g,zz=[ceil(M*F(c[n])) for n in ('alpha','beta','gamma','zeta')]
        t=bits[LABELS[int(z[2])]];v=bits[LABELS[int(z[3])]]
        val=a*sh('ABCDE',0)-TABS['DEEP',0]['gamma_b1_floor_million'][2*t+v] if b else a*sh('ABCDE',0)+g*t-M*v+(M+zz)*t*v
        return val,F(k)
    if tag=='F':
        i={'second':1,'third':2}[z[1]]
        return sh('ABCDE',i)-sh(PATHS[z[1]],i),F(0)
    # The actual sum-SU/SV rows are terminal queries to the Sbranch menu.
    if tag in PATHS and z[1]=='5' and z[2] in ('sum-SU','sum-SV'):
        pos={'sum-SU':1,'sum-SV':2}[z[2]]
        return 5*sh(PATHS[tag],4)-sum(q(t[pos],b+sum(bits[c] for c in PATHS[tag][:4])+1) for t in families['Sbranch']),F(0)
    if tag in PATHS:
        path=PATHS[tag]
        if z[1]=='reply':
            p=b+sum(bits[c] for c in path[:3]);den=(p+1)*(p+2);ell,h=menus[list(PATHS).index(tag)];kind=z[2]
            if kind=='S':val=5*sh(path,3)-q(d,p+1)+q(h,den)
            elif kind=='V':val=q(d*ell-5*h,den)
            elif kind=='Z':val=5*sh(path,4)-q(ell,p+bits[path[3]]+1)
            else:
                assert kind.startswith('cross-L-');other=menus[list(PATHS).index(kind[len('cross-L-'):])][0]
                val=q(5*(ell-other),p+1)+q(d*other-5*h,den)
            return val,F(0)
        i=int(z[1])-1;p=sum(bits[c] for c in path[:i]);rem=5-i
        if z[2]=='K':val=sh(path,i)-q(bits[z[3]],b+p+rem)
        elif z[2]=='O':val=5*rem*sh(path,i)+q(p+(b if mode=='coverage' else 0),b+p+rem)-target()
        else:
            assert z[2].startswith('sum-L-');ell=menus[list(PATHS).index(z[2][len('sum-L-'):])][0]
            val=5*sh(path,i)-q(ell,b+p+rem)
        return val,F(0)
    assert tag in families,name
    branch=families[tag];k=len(branch[0]);pref=b+bits['A']+(bits['B'] if tag=='AB' else bits['E'] if tag=='AE' else 0)
    def bs(t,i):return q(t[i],pref+sum(t))
    if z[1] in ('BG','PC'):
        assert z[3]=='eq';i,j=int(z[4]),int(z[5]);vals=[local(z[1],int(z[2]),t[i],t[j]) for t in branch]
        return sum(x[0] for x in vals),sum(x[1] for x in vals)
    if z[1] in ('F2','F3'):
        i=1 if k==4 else 2;path=PATHS['second' if tag=='AE' else 'actual']
        return 5*sh(path,i)-sum(bs(t,0) for t in branch),F(0)
    if z[1] in PATHS:
        path=PATHS[z[1]];i=int(z[2])-1;pos=('TUVW' if k==4 else 'TXY').index(z[3][len('sum-'):])
        return 5*sh(path,i)-sum(q(t[pos],b+sum(bits[c] for c in path[:i])+5-i) for t in branch),F(0)
    if z[1]=='pair':
        assert z[3]=='query_equal';r,s=map(int,z[2]);value=F(0)
        for i,t in enumerate(branch):
            p=pref+sum(t[:k-2]);den=(p+1)*(p+2);H=bs(t,k-2)+bs(t,k-1)+q(t[k-2],den)
            for j,v in enumerate(branch):
                if i!=j:value+=H-q(v[r]+v[s],p+1)+q(v[r]*v[s],den)
        return value,F(0)
    seat=int(z[1]);pos=seat-(6-k);value=F(0)
    if z[2]=='K':
        for t in branch:value+=bs(t,pos)-q(bits[z[3]],pref+sum(t[:pos])+k-pos)
    else:
        query=int(z[3]) if z[2]=='offdiag' else ('TUVW' if k==4 else 'TXY').index(z[2][len('sum-'):])
        for i,t in enumerate(branch):
            for j,v in enumerate(branch):
                if z[2]!='offdiag' or i!=j:value+=bs(t,pos)-q(v[query],pref+sum(t[:pos])+k-pos)
    return value,F(0)

def expand(hist,k):
    out=[]
    for t,n in zip(product((0,1),repeat=k),hist):out.extend([t]*n)
    assert len(out)==5
    return out

def audit():
    reports=[];rho_tables={}
    for b,mode in ((0,'profit'),(1,'profit'),(1,'coverage')):
        a=load(OUT/f'fixed53_b{b}_{mode}.json');count=0
        for row in a['min_by_actual_and_d']:
            w=row['witness'];bits=dict(zip(LABELS,map(int,w['bits'])));d=w['d']
            families={tag:expand(h,4 if tag=='Sbranch' else 3) for tag,h in w['histograms'].items()}
            vals={name:literal_row(name,bits,d,w['menus'],families,b,mode) for name in WEIGHTS}
            combined=sum(F(weight,D)*vals[name][0] for name,weight in WEIGHTS.items())
            kap=sum(F(weight,D)*vals[name][1] for name,weight in WEIGHTS.items())
            assert kap==-F(226487,10**21)
            c=sum(bits[x] for x in 'ABCDE');tar=2*q(c,b+c)-q(d,b+d) if mode=='profit' else 2*int(bool(b+c))-int(d>0)
            rho=tar-combined
            assert rho==F(row['min_rho']),(b,mode,row['actual'],d,rho,row['min_rho'])
            count+=1
            if mode=='profit':rho_tables[b,row['actual'],d]=rho
        reports.append({'background':b,'mode':mode,'saved_extremal_witnesses_verified':count,'literal_row_evaluations':count*53})
    eps=F(62212762317811658581,1250000000000000000000)
    # Verify the final pointwise epsilon charge on all 12,288 saved conditional
    # minima, not just the coarser 192-row display.
    min_charge=None
    for b in (0,1):
        a=load(OUT/f'fixed53_b{b}_profit.json')
        for r in a['all_6144_conditional_residuals']:
            value=F(r['rho'])+(eps if b and r['bits'][:5]=='00000' else 0)
            assert value>=0
            min_charge=value if min_charge is None else min(min_charge,value)
    assert eps<F(1,20)
    # Six-comparison averaging: each omission has five legal slots.  There
    # are d deletions with d-1 and 6-d with d memberships, including repeats.
    bridge=[]
    for b in (0,1):
        for bits_tuple in product((0,1),repeat=5):
            bits=''.join(map(str,bits_tuple));c=sum(bits_tuple)
            for d in range(7):
                avg=(F(6-d,6)*rho_tables[b,bits,d] if d<6 else 0)+(F(d,6)*rho_tables[b,bits,d-1] if d else 0)
                avgR=F(6-d,6)*q(d,b+d)+F(d,6)*q(d-1,b+d-1) if d else F(0)
                delta=F(d>0)-avgR
                explicit=F(0) if d==0 else F(7,6*(d+1)) if b else F(d==1,6)
                assert delta==explicit
                root_share=q(b,b+c)
                bridge.append({'background':b,'actual_tail':bits,'comparison_multiplicity':d,'average_min_rho':str(avg),
                    'omission_debt':str(delta),'first_player_share':str(root_share),'root_bridge_coefficient':str(avg+2*root_share-delta)})
    # Exact range of a single added actual-last query to the prefix label.
    lower=F(0);upper=None;lower_witness=None;upper_witness=None
    for (b,bits,d),rho in rho_tables.items():
        e=tuple(map(int,bits));s=q(e[-1],b+sum(e))-q(b,b+sum(e[:4])+1)
        if s<0 and rho/s>lower:lower=rho/s;lower_witness=[b,bits,d]
        if s>0 and (upper is None or rho/s<upper):upper=rho/s;upper_witness=[b,bits,d]
    assert lower>upper
    # A real complete-SPE counterexample to the isolated averaging payment
    # delta<=2u_prefix: six-client A and five disjoint singleton labels.
    # Every player chooses A at every history; 6/(k_A+remaining)>=1.
    counterexample={'customers':11,'topics':{'A':list(range(6)),**{f'B{i}':[5+i] for i in range(1,6)}},
        'complete_policy':'choose A at every legal ordered history','W':6,'OPT6':11,'prefix_payoff':'1','tail_profit':'5',
        'average_five_comparison_profit':'20/3','omission_debt':'13/3','claimed_isolated_payment':'2','violation':'7/3'}
    # Given LP point diagnostic (an exact necessary relaxation, not a game).
    pointpath=ROOT/'research/workspaces/six-boss1-20261111/zz_closure_lp/round2/augmented_lp_exact.json'
    point=load(pointpath);assert sha(pointpath)=='bf47390017e37f49f47a8f89126eb8e812982e16bd535adb555f042c178a2ca3'
    hist=[x for x in point['columns'] if x['kind']=='hist'];K=F(point['columns'][0]['weight'])
    u=[sum(F(x['weight'])*q(int(x['actual_bits'][i]),sum(map(int,x['actual_bits']))) for x in hist) for i in range(6)]
    assert sum(u)==F(point['W'])
    zmiss=sum(F(x['weight']) for x in hist if x['actual_bits']=='100000')
    avgr=F(0);avgres=F(0);debt=F(0)
    lookup={(r['background'],r['actual_tail'],r['comparison_multiplicity']):r for r in bridge}
    for x in hist:
        weight=F(x['weight']);b=int(x['actual_bits'][0]);d=x['d'];bits=x['actual_bits'][1:];r=lookup[b,bits,d]
        avgr+=weight*(F(d>0)-F(r['omission_debt']));avgres+=weight*F(r['average_min_rho']);debt+=weight*F(r['omission_debt'])
    base_slack=2*sum(u[1:])+eps*zmiss-avgr
    refined_slack=2*sum(u[1:])-avgr-avgres-F(226487,10**21)*K
    assert base_slack>0 and refined_slack>0 and zmiss==0
    diagnostic={'input_sha256':sha(pointpath),'not_an_SPE':True,'W':point['W'],'u':[str(x) for x in u],
        'first_exclusive_mass':str(zmiss),'average_five_comparison_profit':str(avgr),'average_omission_debt':str(debt),
        'average_coefficient_minimum':str(avgres),'charged_lemma_slack':str(base_slack),'refined_fixed53_slack':str(refined_slack)}
    result={'status':'ALL DIRECT WITNESS AND CHARGING CHECKS PASSED','epsilon':str(eps),'epsilon_less_than_one_twentieth':True,
        'charged_global_min':'0','reports':reports,'first_terminal_prefix_query_interval':{'lower':str(lower),'upper':str(upper),
        'lower_witness':lower_witness,'upper_witness':upper_witness,'nonempty':False},
        'eleven_customer_counterexample':counterexample,'latest_point_diagnostic':diagnostic,
        'all_448_six_slot_bridge_coefficients':bridge,'frozen_outer_weights':CERT,
        'input_sha256':{str(p.relative_to(ROOT)):sha(p) for p in (SRC/'certificate.json',OUT/'shifted_local_tables.json',OUT/'fixed53_b0_profit.json',OUT/'fixed53_b1_profit.json',OUT/'fixed53_b1_coverage.json')}}
    (OUT/'literal_bridge_audit.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('all_448_six_slot_bridge_coefficients','frozen_outer_weights','input_sha256')},indent=2))

if __name__=='__main__':audit()
