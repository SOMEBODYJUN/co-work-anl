"""New branch arithmetic only; never rechecks full SPE histories or invokes old solvers."""
from fractions import Fraction as F
from pathlib import Path
import argparse,hashlib,json

def evaluate(path,expected_sha):
    raw=path.read_bytes();assert hashlib.sha256(raw).hexdigest()==expected_sha
    o=json.loads(raw);n=o['instance']['players'];k=len(o['instance']['topics'])
    clients=[set(c['topics']) for c in o['instance']['customers'] for _ in range(c['multiplicity'])]
    sigma={tuple(x['history']):x['action'] for x in o['certificate']['actions']}
    def finish(h):
        h=tuple(h)
        while len(h)<n:h+=(sigma[h],)
        return h
    def payoff(z,i):return sum((F(1,sum(a in c for a in z)) for c in clients if z[i] in c),F())
    def phi(z):return sum((sum((F(1,j) for j in range(1,sum(a in c for a in z)+1)),F()) for c in clients),F())
    roots=[finish((a,)) for a in range(k)]
    K=[[sum((F(1,1+sum(a in c for a in z)) for c in clients if t in c),F()) for z in roots] for t in range(k)]
    ds=[payoff(z,0) for z in roots];pot=[phi(z) for z in roots]
    return o,clients,roots,K,ds,pot,phi

def main():
    p=argparse.ArgumentParser();p.add_argument('--cycle',type=Path,required=True);p.add_argument('--empty',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();assert not a.output.exists()
    cycle,clients,z,K,d,pot,phi=evaluate(a.cycle,'d60b843f01893bf24f11141342918760a9c3f25b44e43e1ddf8e4aefe09303d9')
    assert len(clients)==348 and [[str(x) for x in row] for row in K]==cycle['K']
    assert [str(x) for x in pot]==cycle['potential'] and [str(x) for x in d]==cycle['root_payoffs']
    assert K[5][2]==K[2][5]==F(159,2) and all(x==F(304) for x in pot)
    edges=[]
    for query,source in [(5,2),(2,5)]:
        tail=z[source][1:]
        delta=sum((F(1,(1+sum(t in c for t in tail))*(2+sum(t in c for t in tail))) for c in clients if query in c and source in c),F())
        drift=phi(z[query][1:])-phi(tail)
        regret=phi((query,)+tail)-phi(z[query])
        assert K[query][source]==d[query]+drift+regret-delta
        assert regret>0
        edges.append({'source':source,'query':query,'K':str(K[query][source]),'d_query':str(d[query]),'F_query_minus_source':str(drift),'joint_R':str(regret),'intersection_tax':str(delta)})
    empty,clients2,z2,K2,d2,pot2,phi2=evaluate(a.empty,'14f8b29548715323a8ee6eac0fabc3efb7e8ea0537fb34cd866c66ed131c855d')
    prob=[F(x) for x in empty['query_probability']];D=sum((prob[i]*d2[i] for i in range(7)),F());C=sum((prob[i]*prob[j]*K2[i][j] for i in range(7) for j in range(7)),F())
    assert D==F(29,30) and C==F(41,40) and D-C==F(-7,120)
    assert max(d2)-C==F(1037,120) and K2[2][6]==F(32,3) and K2[2][2]==F(13,2)
    report={'scope':'one new fixed-root arithmetic calculation on old certified input SHAs; zero original CLI, zero full SPE replay or game search','cycle_input_sha256':'d60b843f01893bf24f11141342918760a9c3f25b44e43e1ddf8e4aefe09303d9','empty_input_sha256':'14f8b29548715323a8ee6eac0fabc3efb7e8ea0537fb34cd866c66ed131c855d','cycle348':{'unit_clients':348,'six_forced_roots':z,'six_root_payoffs':[str(x) for x in d],'six_potentials':[str(x) for x in pot],'full_root_K':[[str(x) for x in row] for row in K],'column_caps':[str(max(row[j] for row in K)) for j in range(6)],'two_edges':edges,'full_history_certification':'reused exact input-bound prior origin-retraction success; not rerun here'},'empty34':{'unit_clients':len(clients2),'seven_forced_roots':z2,'seven_root_payoffs':[str(x) for x in d2],'query_probability':[str(x) for x in prob],'D':str(D),'C':str(C),'D_minus_C':str(D-C),'u_minus_C':str(max(d2)-C),'K_2_6':str(K2[2][6]),'K_2_2':str(K2[2][2]),'full_history_certification':'reused exact input-bound prior parent unit-audit success; not rerun here'},'old_prefix_worked_example':{'k':2,'L':2,'players':4,'unit_clients':10,'D':'8/3','C':'2','tail_price':'1','TailPrice_violation':'1/3','minimum_wording':'original worked point; not minimum over the source domain L>=1'},'smaller_same_family_specialization':{'k':2,'L':1,'players':4,'unit_clients':5,'D':str(F(4,3)),'C':'1','tail_price':'1/2','TailPrice_violation':str(2-F(4,3)-F(1,2)),'scope':'analytic specialization of existing full all-m strategy, not global minimality or a new full-SPE scan'},'empty_tailprice':{'k':13,'t':'1/3','C':str(1-F(1,3)**2/3-(1-F(1,3))**2/26),'D':'1','tail_price':'8/9','M':'38/39','violation':str(F(1,27)-F(4,117)),'threshold_proof':'3(1-t)^2-12t(1-2t)=3(1-3t)^2>=0; only this parameter family'}}
    a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'cycle_edges':edges,'root_D_minus_C':str(D-C),'smaller_prefix_case_clients':5,'empty_tailprice_gap':report['empty_tailprice']['violation'],'passed':True},ensure_ascii=False))

if __name__=='__main__':main()
