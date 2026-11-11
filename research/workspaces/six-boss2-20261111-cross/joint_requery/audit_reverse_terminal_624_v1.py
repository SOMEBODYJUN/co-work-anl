"""Literal-history and zero-new-weight audits for the eight reverse queries."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import json,hashlib,time
import reverse_terminal_624_v1 as new
from separate_master import blocks_from_columns,div

HERE=Path(__file__).resolve().parent


def main():
    start=time.monotonic();checks=0
    # Original R history has A1,A2,A3,Ti,Yj; original Z history has
    # A1,A2,A3,A4,R. These histories are built as ordered bit lists here.
    for p3,a4,ti,bj,cj,r,z in product(range(4),(0,1),(0,1),(0,1),(0,1),(0,1),(0,1)):
        actual=tuple(int(j<p3) for j in range(3))+(a4,0,0)
        words=((ti,0,0),(0,bj,cj))+((0,0,0),)*4
        qs,mu=new.base.queries_and_moments(actual,words,0,1,r,z)
        for family in (0,1):
            prices=new.reverse_prices(qs,(family,0));historyR=list(actual[:3])+[ti,(bj,cj)[family]];historyZ=list(actual[:4])+[r]
            for bits in product((0,1),repeat=4):
                for node,history,response in ((0,historyR,r),(1,historyZ,z)):
                    for bit in bits:
                        literal=F(bit,sum(history)+1)-div(response,sum(history)+response)
                        assert literal==prices[2*node]*bit-prices[2*node+1]
                        checks+=1
    assert new.budget(3)[-8:]==((0,0,0),)*8
    source=HERE.parent/'master_cuts/dynamic_5786_exact.json';raw=source.read_bytes();data=json.loads(raw);columns=data['columns'];blocks=blocks_from_columns(columns)
    embeddings=[]
    for filename in ('cross_pairs_selected_5775_v1.json','cross_pairs_selected_5783_three_compact_v1.json'):
        packraw=(HERE/filename).read_bytes();package=json.loads(packraw)
        for index,cut in enumerate(package['cuts']):
            theta={name:F(value) for name,value in cut['weights'].items()}
            row,au,aK,psi=new.make_row(columns,blocks,cut['member'],tuple(cut['orb']),cut['i'],theta)
            expected=[F(0)]*len(columns)
            for ci,value in cut['sparse_row']:expected[ci]=F(value)
            assert row==expected and au==F(cut['u6_coefficient']) and aK==F(cut['K_coefficient'])
            embeddings.append({'source_package':filename,'package_sha256':hashlib.sha256(packraw).hexdigest(),'cut_index':index,'i':cut['i'],'member':cut['member'],'orb':cut['orb'],'row_sha256':cut['row_sha256'],'coordinates':len(row)})
    # Exercise genuinely nonzero R and Z reverse-query weights together in one
    # hidden minimum and all four visible R/Z states.
    first=json.loads((HERE/'cross_pairs_selected_5783_three_compact_v1.json').read_text())['cuts'][0]
    theta={name:F(value) for name,value in first['weights'].items()};theta.update({'priorR:b':F(1,5),'priorR:c':F(2,7),'priorZ:j':F(3,11),'priorZ:v':F(5,13)})
    row,au,aK,psi=new.make_row(columns,blocks,0,(0,0),3,theta)
    visible=new.base.visible_distribution(blocks,0,(0,0),3);vectorchecks=0
    indices=[(new.NAMES.index(name),weight) for name,weight in theta.items()]
    for p,ell,t,qs,mu,mass in visible:
        candidates=[]
        for hi in range(16):
            vector=new.feature_vector(p,ell,t,qs,mu,hi,3,(0,0))
            candidates.append(sum(weight*vector[ni] for ni,weight in indices))
        literal=min(candidates)
        assert literal==psi(p,ell,t,qs,mu);vectorchecks+=16
    actual=[sum(F(b['column']['weight'])*div(b['a'][i],sum(b['a'])) for b in blocks) for i in range(6)];K=F(columns[0]['weight'])
    direct=actual[3]+au*actual[5]+aK*K-sum(mass*psi(p,ell,t,qs,mu) for p,ell,t,qs,mu,mass in visible)
    assert direct==sum(F(c['weight'])*value for c,value in zip(columns,row))
    out={'status':'PASS','scope':'Exact implementation audit only, not separation or strictness.','source_sha256':hashlib.sha256(raw).hexdigest(),'literal_ordered_history_query_checks':checks,'zero_new_weight_embeddings':embeddings,'nonzero_reverse_shared_min_hidden_checks':vectorchecks,'nonzero_reverse_direct_equals_full_column_dot':True,'nonzero_reverse_test_exact_slack':str(direct),'feature_count':624,'extra_feature_count':8,'all_extra_budgets_zero':True,'elapsed_seconds':time.monotonic()-start}
    target=HERE/'reverse_terminal_624_v1_audit.json';target.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ('zero_new_weight_embeddings','nonzero_reverse_test_exact_slack')},ensure_ascii=False))


if __name__=='__main__':main()
