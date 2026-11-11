"""Independent exact verification of three restricted-construction failures.

Only JSON inputs are consumed. Threshold atoms and the decisive old ZZ row
are rebuilt directly. This does not assert a cut on the unrestricted own-
marginal domain.
"""
from collections import defaultdict
from fractions import Fraction as F
from hashlib import sha256
from itertools import permutations,product
from pathlib import Path
import argparse,json

NODES=tuple((f,i,j)for f,i,j in product(range(2),range(6),range(6))if f or i!=j)
NI={e:i for i,e in enumerate(NODES)}
PRE=[(p.index(0),p.index(1),p.index(2))for p in permutations(range(6))]

def sha(p):return sha256(p.read_bytes()).hexdigest()

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--point',type=Path,required=True)
    ap.add_argument('--A-witness',dest='A_witness',type=Path,required=True)
    ap.add_argument('--directory',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args();base=args.directory
    p=json.loads(args.point.read_bytes());oldA=json.loads(args.A_witness.read_bytes())
    assert oldA['input_sha256']==sha(args.point)
    col=p['columns'][:4849];mass=[F(c['weight'])for c in col];hist={i:c for i,c in enumerate(col)if c['kind']=='hist'}
    own=defaultdict(dict);family=defaultdict(dict);current=None
    for j,c in enumerate(col):
        if c['kind']=='hist':current=j
        elif c['kind']=='joint-reply':
            f,d,wi,wj=c['group'];key=f,d,tuple(wi),tuple(wj)
            own[current].setdefault(key,{})[tuple(c['state'])]=mass[j]
        elif c['kind']=='actual-B-family-state'and c['source']==4:family[c['hist_column']][j]=c
    for h in hist:
        assert sum((mass[j]for j in family[h]),F())==mass[h]
        for rho in own[h].values():rho[0,0]=mass[h]-sum(rho.values(),F());assert min(rho.values())>=0
    atoms={};oldzz={};density={};own_checks=0
    for phase in ('RR','RZ','ZR','ZZ'):
        atoms[phase]={};oldzz[phase]={};density[phase]={}
        for h,meta in hist.items():
            ws=tuple(w for w,n in zip(product((0,1),repeat=3),meta['hist'])for _ in range(n))
            ends={F(),mass[h]};ranges=[]
            for f,i,j in NODES:
                rho=own[h][f,int(i==j),ws[i],ws[j]];q=rho[1,0]+rho[1,1];v=rho[0,1]+rho[1,1];t=rho[1,1]
                if phase[f]=='R':rr=[(F(),q)];zz=[(F(),t),(q,q+v-t)]
                else:rr=[(F(),t),(v,v+q-t)];zz=[(F(),v)]
                ranges.append((rr,zz))
                for a,b in rr+zz:assert 0<=a<=b<=mass[h];ends.update((a,b))
            grid=sorted(ends);aa=[];own_seen=[defaultdict(F)for _ in NODES];zzvalue=F();dens={}
            P=sum(map(int,meta['actual_bits'][:4]))
            for index,(a,b)in enumerate(zip(grid,grid[1:])):
                mid=(a+b)/2;states=[]
                for rr,zz in ranges:
                    r=int(any(lo<=mid<hi for lo,hi in rr));z=int(any(lo<=mid<hi for lo,hi in zz));states.append(2*r+z)
                atom={'mass':b-a,'states':states};aa.append(atom)
                for k,v in enumerate(states):own_seen[k][v//2,v%2]+=b-a
                count=[0,0];zcount=0
                for i,j,k in PRE:
                    se=states[NI[0,i,j]];sf=states[NI[1,i,k]];r=se//2;ze=se%2;zf=sf%2
                    count[r]+=ze-zf;zcount+=ze
                dens[index]=F(zcount,720)
                zzvalue+=(b-a)*(F(count[0],720*(P+1))+F(count[1],720*(P+2)))
            assert sum((x['mass']for x in aa),F())==mass[h]
            for k,(f,i,j)in enumerate(NODES):
                rho=own[h][f,int(i==j),ws[i],ws[j]]
                assert {s:own_seen[k][s]for s in product((0,1),repeat=2)}==rho
                own_checks+=4
            atoms[phase][h]=aa;oldzz[phase][h]=zzvalue;density[phase][h]=dens
    for b in oldA['phases']['A']:
        h=b['hist_column'];assert [(F(x['mass']),x['states'])for x in b['atoms']]==[(x['mass'],x['states'])for x in atoms['RR'][h]]
    budget=F();denoms={}
    for h,states in family.items():
        a=tuple(map(int,hist[h]['actual_bits']))
        for j,c in states.items():
            seq=a[:3]+(a[5],)+tuple(c['hidden']);d=sum(seq[:-1])+1;denoms[j]=d
            budget+=mass[j]*F(seq[-1],d)
    certA=json.loads((base/'fixed_A_obstruction.json').read_bytes())
    certAC=json.loads((base/'phase_AC_obstruction.json').read_bytes())
    cert4=json.loads((base/'hist_four_phase_obstruction.json').read_bytes())
    for cert in (certA,certAC,cert4):assert cert['input_sha256']==sha(args.point)
    assert F(certA['budget'])==F(certAC['budget'])==F(cert4['budget'])==budget
    checks={};D=F();cost=F();cells=0
    for block in certA['blocks']:
        h=block['hist_column'];alpha={x['atom']:F(x['value'])for x in block['atom_potentials']};beta={x['column']:F(x['value'])for x in block['state_potentials']}
        assert set(alpha)==set(range(len(atoms['RR'][h])))and set(beta)==set(family[h])
        rm={i:F()for i in alpha};cm={j:F()for j in beta}
        for i,a in enumerate(atoms['RR'][h]):
            for j in beta:assert alpha[i]+beta[j]<=density['RR'][h][i]/denoms[j];cells+=1
        for e in block['positive_flow']:
            i,j,m=e['atom'],e['family_state_column'],F(e['mass']);assert m>0
            rm[i]+=m;cm[j]+=m;cost+=m*density['RR'][h][i]/denoms[j]
        assert rm=={i:a['mass']for i,a in enumerate(atoms['RR'][h])}and cm=={j:mass[j]for j in beta}
        D+=sum((a['mass']*alpha[i]for i,a in enumerate(atoms['RR'][h])),F())+sum((mass[j]*v for j,v in beta.items()),F())
    assert D==cost==F(certA['exact_minimum_cost'])and budget-D==F(certA['exact_best_slack'])<0
    checks['fixed_A']={'dual_cells':cells,'exact_gap':str(budget-D)}
    lower,upper=map(F,certAC['lambda_interval']);assert lower==0
    zA=sum(oldzz['RR'].values(),F());zC=sum(oldzz['ZZ'].values(),F());assert zC<0<zA and upper==zA/(zA-zC)
    D0=F();D1=F();cells=0;endpoint_cost=F()
    for block in certAC['blocks']:
        h=block['hist_column'];alpha={(x['phase'],x['atom']):F(x['value'])for x in block['atom_potentials']};beta={x['column']:F(x['value'])for x in block['state_potentials']}
        aa={};rm={}
        for ph,actual in (('A','RR'),('C','ZZ')):
            aa[ph]=F()
            for i,a in enumerate(atoms[actual][h]):
                rm[ph,i]=F();aa[ph]+=a['mass']*alpha[ph,i]
                for j in family[h]:assert alpha[ph,i]+beta[j]<=density[actual][h][i]/denoms[j];cells+=1
        bsum=sum((mass[j]*v for j,v in beta.items()),F());D0+=aa['A']+bsum;D1+=aa['C']-aa['A'];cm={j:F()for j in family[h]}
        for e in block['positive_flow_at_upper']:
            ph,i,j,m=e['phase'],e['atom'],e['family_state_column'],F(e['mass']);actual='RR'if ph=='A'else'ZZ'
            assert m>0;rm[ph,i]+=m;cm[j]+=m;endpoint_cost+=m*density[actual][h][i]/denoms[j]
        assert rm=={(ph,i):a['mass']*(1-upper if ph=='A'else upper)for ph,actual in (('A','RR'),('C','ZZ'))for i,a in enumerate(atoms[actual][h])}
        assert cm=={j:mass[j]for j in family[h]}
    assert D1<=0 and endpoint_cost==D0+upper*D1
    assert D0==F(certAC['dual_constant'])and D1==F(certAC['dual_lambda_coefficient'])
    assert budget-endpoint_cost==F(certAC['exact_best_slack_over_interval'])<0
    assert F(certAC['old_IC_multiplier'])==D1/(zC-zA)>=0
    checks['global_AC']={'dual_cells':cells,'exact_gap':str(budget-endpoint_cost),'lambda_upper':str(upper)}
    assert cert4['new_IC_weights']==[{'query':['new-to-Z',[0,0]],'weight':'1'}]
    assert len(cert4['old_IC_weights'])==1
    weighted=cert4['old_IC_weights'][0];assert weighted['kind']=='Z-Z'and weighted['class']==[0,1,[0,1,0,2]]
    nu=F(weighted['weight']);assert nu>=0
    D=F();cells=0;phase_checks=0
    for block in cert4['blocks']:
        h=block['hist_column'];beta={x['column']:F(x['value'])for x in block['family_potentials']};gamma=F(block['phase_potential'])
        assert set(beta)==set(family[h])
        for ph in atoms:
            alpha={x['atom']:F(x['value'])for x in block['atom_potentials'][ph]}
            assert set(alpha)==set(range(len(atoms[ph][h])))
            for i,a in enumerate(atoms[ph][h]):
                for j in family[h]:assert alpha[i]+beta[j]<=density[ph][h][i]/denoms[j];cells+=1
            bound=sum((a['mass']*alpha[i]for i,a in enumerate(atoms[ph][h])),F())-nu*oldzz[ph][h]
            assert gamma<=bound and bound==F(block['phase_potential_upper_bounds'][ph]);phase_checks+=1
        D+=gamma+sum((mass[j]*v for j,v in beta.items()),F())
    assert D==F(cert4['exact_dual_lower_cost'])and budget-D==F(cert4['exact_IC_combination_upper_bound'])<0
    checks['hist_four_phases']={'dual_cells':cells,'phase_inequalities':phase_checks,'exact_gap':str(budget-D)}
    result={'scope':'independent proof of three restricted common-construction failures only; no original-domain cut',
            'point_sha256':sha(args.point),'A_witness_sha256':sha(args.A_witness),'verifier_sha256':sha(Path(__file__)),
            'own_four_state_equalities':own_checks,'all_three_certificates_verified':True,'certificates':checks,
            'certificate_hashes':{name:sha(base/name)for name in('fixed_A_obstruction.json','phase_AC_obstruction.json','hist_four_phase_obstruction.json')}}
    args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print({'all_three_certificates_verified':True,'own_four_state_equalities':own_checks,
           'checks':{k:{kk:vv for kk,vv in v.items()if kk!='exact_gap'and kk!='lambda_upper'}for k,v in checks.items()}})

if __name__=='__main__':main()
