#!/usr/bin/env python3
"""Independent literal successor/policy audit and exact full-vector freeze.

This file does not import the discounted discovery implementation.  It
rebuilds every original coefficient, enumerates literal intermediate bits,
solves four two-state stationary policies, checks every Bellman inequality,
and audits all 64 actual signatures plus every used fixed-query membership.
"""
from __future__ import annotations
import argparse
from collections import defaultdict
from fractions import Fraction as F
from functools import lru_cache
import gzip
import hashlib
from itertools import product
import json
from pathlib import Path
import sys

sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
RUN=HERE.parent


def ratio(a,b):return F(a,b) if a else F()


def canonical(row):
    return json.dumps([[int(i),str(F(v))] for i,v in sorted(row) if F(v)],separators=(',',':')).encode()


def read_member(column,actual,name):
    if name.startswith('A') and name[1:].isdigit():return F(actual[int(name[1:])-1])
    if name=='M':return F(column['M'])
    if name=='Y-average':return F(column['ell'],6)
    assert name.startswith('H')
    return F(column['hidden'][int(name[1:])])


class Audit:
    def __init__(self,record):
        assert record['state_count']==2 and record['previous_theme'] is None
        self.record=record
        self.source=record['actual_source_zero_based']
        self.k=6-self.source
        self.theta=F(record['theta'])
        self.par={n:F(v) for n,v in record['parameters'].items()}
        assert all(v>=0 for v in self.par.values())
        assert sum(self.par.values(),F())==1
        self.fixed=tuple(q for q in record['queries'] if self.par.get('mu_'+q,F()))
        self.inequalities=0
        self.literal_edges=0
        self.cache={}

    def cost(self,p,ell,t,c,middle,qs):
        P=self.par;s=sum(middle);z=p+t+s+c;den=p+t+s+1
        mu=P.get('mu_current',F())+sum((P.get('mu_'+q,F()) for q in self.fixed),F())
        query=sum((P['mu_'+name]*q for name,q in zip(self.fixed,qs)),F())+P.get('mu_current',F())*t
        return (ratio(P.get('source',F())*t-mu*c,z)
                +s*(P.get('beta_middle',F())+P.get('alpha_middle',F())/F(ell+1))
                +c*(P.get('beta_last',F())+P.get('alpha_last',F())/F(ell+1))
                +query/den)

    def value(self,p,ell,t0,qs):
        key=(p,ell,tuple(qs))
        if key not in self.cache:
            edges={}
            literal={}
            for t,c in product((0,1),repeat=2):
                values=[self.cost(p,ell,t,c,middle,qs)
                        for middle in product((0,1),repeat=self.k-2)]
                literal[t,c]=values;edges[t,c]=min(values)
                self.literal_edges+=len(values)
            th=self.theta;oo=1-th
            # Policy orders are c(0),c(1), independent of discovery formula.
            v00=(edges[0,0]/oo,edges[1,0]+th*edges[0,0]/oo)
            v01=(edges[0,0]/oo,edges[1,1]/oo)
            v10=((edges[0,1]+th*edges[1,0])/(1-th*th),
                 (edges[1,0]+th*edges[0,1])/(1-th*th))
            v11=(edges[0,1]+th*edges[1,1]/oo,edges[1,1]/oo)
            policies=(v00,v01,v10,v11)
            v=(min(x[0] for x in policies),min(x[1] for x in policies))
            assert v in policies
            for t,c in product((0,1),repeat=2):
                for cost in literal[t,c]:
                    assert cost+th*v[c]-v[t]>=0
                    self.inequalities+=1
            for t in (0,1):assert v[t]==min(edges[t,c]+th*v[c] for c in (0,1))
            self.cache[key]=tuple(oo*x for x in v)
        return self.cache[key][t0]

    def full_domain(self):
        named=[q for q in self.fixed if not q.startswith('A') and q!='Y-average']
        ylevels=range(7) if 'Y-average' in self.fixed else (0,)
        visible=0
        for actual in product((0,1),repeat=6):
            for named_bits in product((0,1),repeat=len(named)):
                nm=dict(zip(named,named_bits))
                for dy in ylevels:
                    qs=tuple(F(actual[int(q[1:])-1]) if q.startswith('A') else
                             (F(dy,6) if q=='Y-average' else F(nm[q])) for q in self.fixed)
                    for t0 in (0,1):
                        self.value(sum(actual[:self.source]),sum(actual[:5]),t0,qs)
                        visible+=1
        return {'all_actual_signatures':64,'active_fixed_query_names':self.fixed,
                'independent_named_query_bits':len(named),'Y_query_levels':list(ylevels),
                'visible_initial_cases':visible,'distinct_edge_problems':len(self.cache),
                'literal_middle_bits':self.k-2,'terminal_bits':1,
                'literal_edge_values_checked':self.literal_edges,
                'bellman_inequalities_checked':self.inequalities,
                'all_four_stationary_policies_solved_exactly':True,
                'all_bellman_inequalities_nonnegative':True,
                'each_state_has_a_tight_action':True,
                'scope':'An enlarged Boolean query domain: every actual signature and every used named fixed-query membership; no realizability restriction is needed for this lower envelope.'}

    def row(self,columns):
        P=self.par;k=self.k;source=self.source
        hist={i:c for i,c in enumerate(columns) if c['kind']=='hist'}
        row={}
        cap=(k-2)*P.get('beta_middle',F())+P.get('beta_last',F())
        if cap:row[0]=cap
        count=zero_count=0
        for i,c in enumerate(columns[:4849]):
            family=('M1' if c['kind']=='maximum-root-family-state' else
                    ('B'+str(c['source']) if c['kind']=='actual-B-family-state' else None))
            if family!=self.record['family']:continue
            actual=tuple(map(int,hist[c['hist_column']]['actual_bits']))
            t0=int(read_member(c,actual,self.record['forced']))
            qs=tuple(read_member(c,actual,q) for q in self.fixed)
            psi=self.value(sum(actual[:source]),sum(actual[:5]),t0,qs)
            wallet=P.get('source',F())*ratio(actual[source],sum(actual))
            wallet+=((k-2)*P.get('alpha_middle',F())+P.get('alpha_last',F()))*ratio(actual[5],sum(actual))
            if wallet!=psi:row[i]=wallet-psi
            count+=1;zero_count+=(F(c['weight'])==0)
        return row,count,zero_count


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--discovery',type=Path,required=True)
    ap.add_argument('--output',type=Path,default=HERE/'selected_discounted_cuts_19556.json')
    args=ap.parse_args();raw=args.discovery.read_bytes();found=json.loads(raw)
    point_path=Path(found['input']);matrix_path=Path(found['matrix'])
    point_raw=point_path.read_bytes();matrix_raw=matrix_path.read_bytes()
    assert hashlib.sha256(point_raw).hexdigest()==found['input_sha256']
    assert hashlib.sha256(matrix_raw).hexdigest()==found['matrix_sha256']
    point=json.loads(point_raw);columns=point['columns'];matrix=json.loads(gzip.decompress(matrix_raw))
    desc=lambda c:{k:v for k,v in c.items() if k!='weight'}
    assert list(map(desc,columns))==matrix['columns']
    base=defaultdict(list)
    for i,row in enumerate(matrix['rows']):base[canonical(row)].append({'index':i,'name':matrix['row_names'][i]})
    selected=[];duplicates=[];seen={}
    for n,record in enumerate(found['results']):
        if F(record.get('exact_slack','0'))>=0:continue
        audit=Audit(record);row,ncols,nzero=audit.row(columns);encoded=canonical(row.items())
        assert encoded==canonical(record['coefficients'])
        value=sum((v*F(columns[i]['weight']) for i,v in row.items()),F())
        assert value==F(record['exact_slack']) and value<0
        if encoded in seen:
            duplicates.append({'discovery_index':n,'same_as':seen[encoded]});continue
        name=f'named-discount:{record["family"]}:{record["actual_source_zero_based"]}:{record["forced"]}:{record["theta"]}'
        seen[encoded]=name
        assert not base.get(encoded)
        domain=audit.full_domain()
        rec={k:v for k,v in record.items() if k not in ('elapsed_seconds','coefficients','vector_sha256')}
        rec.update(name=name,discovery_index=n,coefficients=json.loads(encoded),
                   vector_sha256=hashlib.sha256(encoded).hexdigest(),
                   slack=str(value),slack_float=float(value),
                   full_domain_audit=domain,independently_constructed_family_columns=ncols,
                   independently_constructed_zero_mass_columns=nzero,
                   independent_full_vector_equal=True,baseline_matches=[])
        selected.append(rec)
        print(json.dumps({'name':name,'slack_float':float(value),'independent_full_vector_equal':True,
                          'full_domain_audit':domain},ensure_ascii=False),flush=True)
    out={'scope':'Independent exact full-domain and full-vector audit of selected named-discount negative rows; no SPE or half claim',
         'source':str(point_path),'source_sha256':found['input_sha256'],'input_W':point['W'],
         'matrix':str(matrix_path),'matrix_sha256':found['matrix_sha256'],'baseline_rows':len(matrix['rows']),
         'columns':len(columns),'original_columns':4849,'input_records':len(found['results']),
         'distinct_rows':len(selected),'selected_rows':selected,'duplicates':duplicates,
         'discovery':str(args.discovery.resolve()),'discovery_sha256':hashlib.sha256(raw).hexdigest(),
         'auditor_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    args.output.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'output':str(args.output),'sha256':hashlib.sha256(args.output.read_bytes()).hexdigest(),
                      'distinct_negative_rows':len(selected)}),flush=True)


if __name__=='__main__':main()
