"""Recover an exact D lift from the single floating discovery; no new solve."""
from collections import defaultdict
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
POINT = HERE.parent/'union_augmented_lp/augmented_lp_exact.json'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dump(name,obj):
    (HERE/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')


def main():
    lift = json.loads((HERE/'symbolic_lift.json').read_bytes())
    num = json.loads((HERE/'phase_I_discovery.json').read_bytes())
    point = json.loads(POINT.read_bytes())
    assert num['phase_I']==0 and num['success']
    assert sha(POINT)==lift['point_sha256']
    assert sha(HERE/'symbolic_lift.json')==num['symbolic_lift_sha256']
    old = lift['fixed_old_columns']
    weights = [F(c['weight']) for c in point['columns']]
    xindices = [i for i,c in enumerate(lift['new_columns']) if c['kind']=='D-membership-marginal']
    xtuple = {(c['hist_column'],tuple(c['word'])):i for i,c in enumerate(lift['new_columns'])
              if c['kind']=='D-membership-marginal'}
    own = defaultdict(dict)
    b4 = defaultdict(list)
    for j,c in enumerate(point['columns'][:4849]):
        if c['kind']=='hist':
            h=j
        elif c['kind']=='joint-reply':
            f,s,u,v = c['group'];g=(f,s,tuple(u),tuple(v))
            own[h].setdefault(g,{})[tuple(c['state'])]=j
        elif c['kind']=='actual-B-family-state' and c['source']==4:
            b4[c['hist_column']].append(j)
    caps = {}
    for i,c in enumerate(lift['new_columns']):
        if c['kind']=='D-membership-marginal':
            continue
        h=c['hist_column']
        if c['kind']=='virtual-R-D-min-upper':
            f,s,u,v=c['group'];g=(f,s,tuple(u),tuple(v))
            cap=sum(weights[j] for state,j in own[h][g].items() if state[0])
        elif c['kind']=='virtual-H1-D-min-upper':
            cap=sum(weights[j] for j in b4[h] if point['columns'][j]['hidden'][0])
        else:
            raise AssertionError(c)
        caps[i]=(xtuple[h,tuple(c['word'])],cap)

    # Canonical min values can only increase Z/F query slacks relative to the
    # discovery's arbitrary envelopes.  Select a piece for exact recovery only.
    pieces={i:('x' if num['x'][x] <= float(cap) else 'cap') for i,(x,cap) in caps.items()}
    canonical_num=list(num['x'][:-1])
    for i,(x,cap) in caps.items():
        canonical_num[i]=min(canonical_num[x],float(cap))
    equations=[]
    for i in xindices:
        if abs(num['x'][i])<1e-11:
            equations.append(({'zero_x':i},{i:F(1)},F()))
    for r,desc in enumerate(lift['rows']):
        constant=F();coef=defaultdict(F)
        for j,sv in desc['row']:
            v=F(sv)
            if j<old:
                constant+=v*weights[j]
            elif j-old in xindices:
                coef[j-old]+=v
            else:
                y=j-old;x,cap=caps[y]
                if pieces[y]=='x':coef[x]+=v
                else:constant+=v*cap
        coef={j:v for j,v in coef.items() if v}
        approx=float(constant)+sum(float(v)*num['x'][j] for j,v in coef.items())
        if coef and abs(approx)<1e-10:
            equations.append(({'row':r,'name':desc['name']},coef,-constant))
        elif not coef:
            assert constant>=0, (desc['name'],constant)

    # Small exact sparse row reduction, with all rejected inconsistencies fatal.
    basis={};equation_log=[]
    for name,coef,rhs in equations:
        rr=dict(coef);bb=rhs
        while rr:
            p=min(rr)
            if p not in basis:
                v=rr[p]
                rr={j:a/v for j,a in rr.items()};bb/=v
                basis[p]=(rr,bb)
                equation_log.append({'origin':name,'independent':True})
                break
            er,eb=basis[p];v=rr[p]
            for j,a in er.items():
                rr[j]=rr.get(j,F())-v*a
                if not rr[j]:del rr[j]
            bb-=v*eb
        else:
            assert bb==0, ('inconsistent active equations',name,str(bb))
            equation_log.append({'origin':name,'independent':False})
    free=[j for j in xindices if j not in basis]
    values={j:F(num['x'][j]).limit_denominator(10**12) for j in free}
    for p in sorted(basis,reverse=True):
        er,eb=basis[p]
        values[p]=eb-sum(a*values[j] for j,a in er.items() if j!=p)
    result=[None]*len(lift['new_columns'])
    for i in xindices:result[i]=values[i]
    for i,(x,cap) in caps.items():result[i]=min(values[x],cap)
    assert all(v is not None and v>=0 for v in result)
    allv=weights+result
    slacks=[sum(F(v)*allv[j] for j,v in row['row']) for row in lift['rows']]
    bad=[{'row':r,'name':lift['rows'][r]['name'],'slack':str(s)} for r,s in enumerate(slacks) if s<0]
    report={'scope':'Exact recovery of one necessary marginal/min lift; no common-measure/SPE claim.',
            'point_sha256':sha(POINT),'symbolic_lift_sha256':sha(HERE/'symbolic_lift.json'),
            'discovery_sha256':sha(HERE/'phase_I_discovery.json'),'script_sha256':sha(Path(__file__)),
            'x_variables':len(xindices),'active_equations':len(equations),'rank':len(basis),
            'free_variables':[{'column':j+old,'local_index':j,'value':str(values[j])} for j in free],
            'equations':equation_log,'phase_I':'0',
            'new_values':[str(v) for v in result],
            'rows':[{'index':r,'name':row['name'],'slack':str(s),'approx':float(s)}
                    for r,(row,s) in enumerate(zip(lift['rows'],slacks))],
            'minimum_slack':str(min(slacks)),'negative_rows':bad,
            'positive_new_columns':sum(v>0 for v in result),
            'global_zero_rows':[row['name'] for row,s in zip(lift['rows'],slacks) if not s and
                                'min-at-most' not in row['name'][0] and row['name'][0]!='D-at-most-hist'],
            'max_x_change_from_numeric':max(abs(float(values[j])-num['x'][j]) for j in xindices),
            'auxiliaries_are_exact_canonical_minima':True}
    dump('exact_lift.json',report)
    assert not bad,bad
    print(json.dumps({k:report[k] for k in ('scope','x_variables','active_equations','rank','free_variables',
                      'minimum_slack','positive_new_columns','global_zero_rows','max_x_change_from_numeric')},ensure_ascii=False))


if __name__=='__main__':
    main()
