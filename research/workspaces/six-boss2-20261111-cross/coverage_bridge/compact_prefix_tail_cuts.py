#!/usr/bin/env python3
"""Small common-denominator recovery of saved alpha/beta discoveries."""
from fractions import Fraction as F
from pathlib import Path
import hashlib,json,sys
import prefix_tail_requery as p


def main():
    input_path,raw_path,out_path=map(Path,sys.argv[1:4])
    data,cols,hs,K,u=p.tail.read_input(input_path);raw=json.loads(raw_path.read_text());cuts=[]
    for old in raw['results']:
        if F(old.get('exact_slack','0'))>=0:continue
        source=old['source']-1;member=old['member'];orb=tuple(old['orbit']);delta=F(old['delta']);k=6-source
        states=p.tail.state_measure(hs,source,member,orb)
        orig=[F(old['alpha'].get(n,'0')) for n in p.prefix.NAMES]+[F(old['beta'].get(n,'0')) for n in p.tail.NAMES]
        for scale in (1000,10000,100000,1000000,10000000):
            ints=[max(0,round(float(v)*scale)) for v in orig]
            total=ints[p.prefix.NAMES.index('sourceT')]+ints[p.prefix.NAMES.index('sourceC')]+ints[p.DA]
            if not total:continue
            vals=[F(n,total) for n in ints];a,b=vals[:p.DA],vals[p.DA:]
            rb,ub,kb=p.combined_budgets(k,a,b);sums=[F(0)]*3
            for st,mass in states.items():
                parts=p.combined_value(*st,k,a,b,delta,components=True)
                for j,v in enumerate(parts):sums[j]+=mass*v
            slack=rb*u[source]+ub*u[5]+kb*K-sums[0]
            if slack<0:break
        else:raise RuntimeError('No compact negative recovery: '+str((source,member,orb,delta)))
        row,ns=p.exact_row(cols,hs,source,member,orb,a,b,delta)
        assert sum((v*F(c['weight']) for v,c in zip(row,cols)),F(0))==slack
        record={'source':source+1,'k':k,'member':member,'orbit':list(orb),'delta':str(delta),
                'grid':scale,'common_source_denominator':total,'source_weight_sum':'1',
                'alpha':{n:str(v) for n,v in zip(p.prefix.NAMES,a) if v},
                'beta':{n:str(v) for n,v in zip(p.tail.NAMES,b) if v},
                'budget':list(map(str,(rb,ub,kb))),'exact_slack':str(slack),'exact_slack_float':float(slack),
                'separate_projection_slack':str(rb*u[source]+ub*u[5]+kb*K-sums[1]-sums[2]),
                'joint_projection_gain':str(sums[0]-sums[1]-sums[2]),
                'full_column_count':len(cols),'full_projected_states':ns,
                'row_nonzero':[[j,str(v)] for j,v in enumerate(row) if v],
                'row_sha256':hashlib.sha256(json.dumps(list(map(str,row)),separators=(',',':')).encode()).hexdigest()}
        cuts.append(record);print('COMPACT',source+1,member,orb,str(delta),'grid',scale,'slack',float(slack),flush=True)
    report={'scope':'compact exact prefix/tail common-endpoint cuts, full vectors; not SPE',
            'input':str(input_path),'input_sha256':hashlib.sha256(input_path.read_bytes()).hexdigest(),
            'discovery_report':str(raw_path),'discovery_report_sha256':hashlib.sha256(raw_path.read_bytes()).hexdigest(),
            'alpha_names':p.prefix.NAMES,'beta_names':p.tail.NAMES,'cuts':cuts,
            'unique_vectors':len({r['row_sha256'] for r in cuts})}
    out_path.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print({'cuts':len(cuts),'unique_vectors':report['unique_vectors']},flush=True)


if __name__=='__main__':main()
