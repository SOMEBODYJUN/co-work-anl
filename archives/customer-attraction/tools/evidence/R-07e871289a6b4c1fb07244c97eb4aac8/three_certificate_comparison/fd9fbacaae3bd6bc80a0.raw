"""Independent exact off-diagonal audit; does not import another phi routine."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
from hashlib import sha256
import json

HERE=Path(__file__).resolve().parent
SOURCE=Path(__file__).resolve().parents[5]/'research/workspaces/customer-attraction/R-07e871289a6b4c1fb07244c97eb4aac8/general_from_half5/six_copy_free_results.json'

def fraction(n,d):
    return F(n,d) if n else F(0)

def independently_minimized_phi(p,ell,t,q):
    values=[]
    for b,c,j,v in product(range(2),repeat=4):
        # Expand every numerator separately to avoid a hidden 0/0 convention.
        val=(2*fraction(t,p+t+b+c)-fraction(c,p+t+b+c)
             +F(3,2)*fraction(c,p+c+j+v)-F(1,2)*fraction(v,p+c+j+v)
             +F(b,2*(p+c+j+1))+F(j,4*(ell+1))
             +F(5*v,12*(ell+1))+F(v,12)+F(q,p+t+b+1))
        values.append(val)
    return -min(values)

def main():
    raw=SOURCE.read_bytes()
    point=json.loads(raw)['final']
    assert point['m']==6 and point['n_rows']==387
    U4=F(0);U6=F(0);W=F(0);O=F(0);credit=F(0);details=[]
    for row in point['support']:
        a=tuple(map(int,row['actual_bits']));n=F(row['weight']);d=row['d']
        assert d==1
        p=sum(a[:3]);ell=sum(a[:5]);load=sum(a)
        assert p<=ell<=p+2
        source=n*fraction(a[3],load)
        last=n*fraction(a[5],load)
        # For d=1 among six optimum indices, the thirty ordered pairs i!=j
        # have twenty (0,0), five (1,0), five (0,1), zero (1,1).
        ph={f'{t}{q}':independently_minimized_phi(p,ell,t,q)
            for t,q in product((0,1),repeat=2)}
        average=(20*ph['00']+5*ph['10']+5*ph['01'])/30
        # Independently enumerate an arbitrary representative t-vector with d=1.
        rep=(1,0,0,0,0,0)
        literal=sum(independently_minimized_phi(p,ell,rep[i],rep[j])
                    for i in range(6) for j in range(6) if i!=j)/30
        assert average==literal
        U4+=source;U6+=last;credit+=n*average
        W+=n*bool(load);O+=n
        details.append({'actual_bits':row['actual_bits'],'mass':str(n),'p':p,'ell':ell,
                        'phi_tq':{k:str(v) for k,v in ph.items()},
                        'offdiag_mean_phi':str(average),'mass_times_offdiag_phi':str(n*average)})
    assert W==F(point['W']) and O==1
    K=F(point['K'])
    budget=F(7,2)*U4+F(2,3)*U6+K/12
    value=budget+credit
    assert U4==F(21185642969,347093460368)
    assert U6==F(46719837927,347093460368)
    assert value==F(-4111629751,260320095276)
    result={'status':'independently verified exact negative row',
            'scope':'a new necessary local inequality excludes a prior relaxation point, not a game/SPE counterexample',
            'source_path':str(SOURCE),'source_sha256':sha256(raw).hexdigest(),
            'old_rows_recorded_in_point':point['n_rows'],
            'new_source_provider':4,'source_prefix':'actual providers 1,2,3',
            'anchor_prefix':'actual providers 1,2,3,4,5',
            'u4':str(U4),'u6':str(U6),'K':str(K),'W':str(W),'O':str(O),
            'positive_budget':str(budget),'offdiag_phi_credit':str(credit),
            'offdiag_average_slack':str(value),'ordered_pair_sum_slack':str(30*value),
            'atom_details':details}
    (HERE/'nested_requery_oldpoint.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='atom_details'},indent=2))

if __name__=='__main__':
    main()
