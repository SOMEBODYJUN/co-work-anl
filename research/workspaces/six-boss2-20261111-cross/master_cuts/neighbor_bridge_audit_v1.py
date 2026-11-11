#!/usr/bin/env python3
"""Read-only audit of Boss1 bridges on a separately bound Boss2 exact point.

Only the capacity row and the current-point ZZ rows are independently rebuilt.
Other frozen rows are evaluated for prioritization, not silently certified.
"""
from collections import Counter,defaultdict
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import argparse,datetime,gzip,hashlib,json,sys,time
HERE=Path(__file__).resolve().parent
REPO=HERE.parents[3]
NEIGHBOR=REPO/'research/workspaces/six-boss1-20261111'

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def canonical(value):return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
def full_sha(row,n):
    values=['0']*n
    for j,v in row:values[j]=str(F(v))
    return hashlib.sha256(json.dumps(values,separators=(',',':')).encode()).hexdigest()
def dot(row,x):return sum(F(v)*x[j] for j,v in row if x[j])
def sparse(row):return [[j,str(v)] for j,v in sorted(row.items()) if v]
def add(row,j,v):row[j]+=v
def pattern(seq):
    seen={}
    return tuple(seen.setdefault(a,len(seen)) for a in seq)

def read_columns(point):
    columns=point['columns'];assert len(columns)==4849
    descriptions=[{k:v for k,v in c.items() if k!='weight'} for c in columns]
    assert canonical(descriptions)=='afce2dcdff01e9393c04e317ee6bd52f5c0b378daedd92816647412243362460'
    blocks={};current=None
    for j,c in enumerate(columns):
        if c['kind']=='hist':
            current=j;blocks[j]={'column':c,'groups':defaultdict(dict)}
        elif c['kind']=='joint-reply':
            g=c['group'];key=(g[0],g[1],tuple(g[2]),tuple(g[3]))
            blocks[current]['groups'][key][tuple(c['state'])]=j
    assert len(blocks)==16 and sum(len(b['groups']) for b in blocks.values())==194
    assert all(set(g)=={(0,1),(1,0),(1,1)} for b in blocks.values() for g in b['groups'].values())
    return columns,descriptions,blocks

def capacity_bridge(columns,x):
    # Source IC at actual player two, plus four capacity rows, plus the same
    # branch's terminal query A6 with weight 1/16. All 128 literal cases.
    table=[]
    def expected(p,t,q):
        return ((F(25,64)*t+F(1,16)*q-F(1,20)*t*q) if p==0 else
                (F(109,320)*t+F(1,32)*q-F(1,48)*t*q))
    for p,t,q in product((0,1),repeat=3):
        values=[]
        for f in product((0,1),repeat=4):
            m=sum(f[:3]);g=f[3];z=p+t+m+g
            source=F(t,z) if t else F()
            terminal=F(g,z) if g else F()
            cost=source-F(1,16)*terminal+F(3*m+4*g,64)+F(q,16*(p+t+m+1))
            values.append(cost)
        phi=min(values);assert phi==expected(p,t,q)
        table.append({'p':p,'t':t,'q':q,'phi':str(phi),'minimizers':sum(v==phi for v in values)})
    row=defaultdict(F);row[0]=F(13,64)
    for j,c in enumerate(columns):
        if c['kind']=='hist':
            a=list(map(int,c['actual_bits']))
            if a[1]:row[j]+=F(1,sum(a))
        elif c['kind']=='maximum-root-family-state':
            a=list(map(int,columns[c['hist_column']]['actual_bits']))
            row[j]-=expected(a[0],c['hidden'][0],a[5])
    row=sparse(row);value=dot(row,x)
    return {'mechanism':'Independent literal source + capacity + terminal-query projection',
            'budget':'u2 + 13 K / 64','forced_topic':'maximum-root-family-state hidden[0]',
            'query':'A6','literal_cases':128,'table':table,'row_nonzero':row,
            'row_sha256':full_sha(row,len(x)),'exact_slack':str(value),'slack_display':float(value)}

def zz_bridges(blocks,x,ncols):
    edges=[(f,i,j) for f in (0,1) for i in range(6) for j in range(6) if f or i!=j]
    assert len(edges)==66
    classes=defaultdict(list)
    for e,edge in enumerate(edges):
        for f,other in enumerate(edges):
            label=(edge[0],other[0],pattern(edge[1:]+other[1:]))
            if e!=f:classes[label].append((e,f))
            else:classes[label]
    assert len(classes)==42
    rows={label:defaultdict(F) for label in classes};endpoint_counts=Counter()
    degree_checks=0
    for h,block in blocks.items():
        desc=block['column'];words=[]
        for index,count in enumerate(desc['hist']):words += [tuple(map(int,f'{index:03b}'))]*count
        assert len(words)==6
        group_at=[(f,int(i==j),words[i],words[j]) for f,i,j in edges]
        edge_sets=defaultdict(list)
        for e,g in enumerate(group_at):edge_sets[g].append(e)
        assert set(edge_sets)==set(block['groups'])
        P=sum(map(int,desc['actual_bits'][:4]));D=(P+1)*(P+2)
        groups=block['groups']
        for label,pairs in classes.items():
            grouped=defaultdict(list)
            for e,f in pairs:grouped[group_at[e],group_at[f]].append((e,f))
            for (g,k),subset in grouped.items():
                n=len(subset)
                left=Counter(e for e,f in subset);right=Counter(f for e,f in subset)
                assert len({left[e] for e in edge_sets[g]})==1
                assert len({right[f] for f in edge_sets[k]})==1
                degree_checks+=2
                source=groups[g];target=groups[k];out=rows[label]
                # n*(v_g-v_k)/(P+1) - n*t_g/D.
                for state in ((0,1),(1,1)):
                    add(out,source[state],F(n,P+1));add(out,target[state],-F(n,P+1))
                add(out,source[1,1],-F(n,D))
                q=x[source[1,0]]+x[source[1,1]]
                v=x[target[0,1]]+x[target[1,1]]
                # This is a fixed pointwise upper-bound choice after discovery;
                # each option remains a valid linear necessary row elsewhere.
                endpoint='q_source' if q<=v else 'v_target';endpoint_counts[endpoint]+=1
                chosen=[source[1,0],source[1,1]] if q<=v else [target[0,1],target[1,1]]
                for j in chosen:add(out,j,F(n,D))
    output=[]
    for label,out in sorted(rows.items()):
        row=sparse(out);value=dot(row,x)
        output.append({'class':[label[0],label[1],list(label[2])],
                       'literal_pairs':len(classes[label]),'sparse_row':row,
                       'row_sha256':full_sha(row,ncols),'exact_slack':str(value),
                       'slack_display':float(value),
                       'normalized_slack_display':float(value/len(classes[label])) if classes[label] else 0})
    return output,degree_checks,dict(endpoint_counts)

def saved_row_diagnostic(path,list_key,row_key,x):
    pack=json.loads(path.read_text());items=pack[list_key];values=[]
    for index,record in enumerate(items):
        row=record[row_key]
        assert len({j for j,v in row})==len(row) and all(0<=j<len(x) for j,v in row)
        value=dot(row,x)
        values.append({'record_index':index,'name':record.get('name'),
                       'exact_slack':str(value),'slack_display':float(value)})
    return {'path':str(path.relative_to(REPO)),'sha256':sha(path),
            'role':'Frozen row evaluation only; source generator not independently certified here.',
            'rows':len(values),'negative_count':sum(F(v['exact_slack'])<0 for v in values),
            'values':values}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('point');ap.add_argument('output_stem');args=ap.parse_args()
    p=Path(args.point).resolve();assert p.is_relative_to(HERE)
    stem=args.output_stem;assert '/' not in stem and not (HERE/(stem+'.json')).exists()
    started=time.time();point=json.loads(p.read_text());columns,descriptions,blocks=read_columns(point)
    # Read the neighbor's actual 4849 descriptors, not merely a textual claim.
    neighbor_point=NEIGHBOR/'augmented_lp/round2/augmented_lp_exact.json'
    other=json.loads(neighbor_point.read_text())['columns']
    assert descriptions==[{k:v for k,v in c.items() if k!='weight'} for c in other]
    x=[F(c['weight']) for c in columns]
    cap=capacity_bridge(columns,x)
    zz,degree_checks,endpoint_counts=zz_bridges(blocks,x,len(x))
    diagnostics=[saved_row_diagnostic(NEIGHBOR/'cross_branch_math/round3_candidate_cuts.json','selected_rows','coefficients',x),
                 saved_row_diagnostic(NEIGHBOR/'common_coupling_math/zz-cuts-two-points.json','cuts','row',x)]
    transport=NEIGHBOR/'tail_constraints/augmented5716-transport.json'
    tp=json.loads(transport.read_text());transport_values=[]
    for family in tp['families']:
        value=dot(family['certificate']['sparse_original_row'],x)
        transport_values.append({'family':family['family'],'exact_slack':str(value),'slack_display':float(value)})
    report={'status':'PASS','scope':'Compatibility and independently rebuilt capacity/ZZ bridges on a bound current point; not an SPE or a new mother-system certificate.',
            'point_path':str(p.relative_to(REPO)),'point_sha256':sha(p),'W':point['W'],
            'descriptor_sha256':canonical(descriptions),'neighbor_point_sha256':sha(neighbor_point),
            'capacity_bridge':cap,'zz_classes':zz,'zz_negative_count':sum(F(c['exact_slack'])<0 for c in zz),
            'literal_group_degree_checks':degree_checks,'zz_endpoint_counts':endpoint_counts,
            'frozen_row_diagnostics':diagnostics,
            'transport_frozen_row_diagnostic':{'path':str(transport.relative_to(REPO)),'sha256':sha(transport),'values':transport_values},
            'command':[sys.executable,'-B',str(Path(__file__).resolve()),str(p),stem],
            'script_sha256':sha(Path(__file__)),'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'elapsed_seconds':time.time()-started,
            'optimizer_calls':0,'math_float_operations':'Display conversions only; all coefficients and signs are Fraction.'}
    (HERE/(stem+'.json')).write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    cuts=[c for c in zz if F(c['exact_slack'])<0]
    (HERE/(stem+'_zz_candidates.json')).write_text(json.dumps({
        'scope':'Independently rebuilt fixed-hist ZZ Frechet upper-bound necessary rows; pending Main independent review before integration.',
        'source_path':str(p.relative_to(REPO)),'source_sha256':sha(p),'columns':len(x),'cuts':cuts,
        'generator_sha256':sha(Path(__file__))},ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'status':'PASS','point_sha256':sha(p),'capacity_slack':cap['exact_slack'],
        'capacity_slack_display':cap['slack_display'],'ZZ_negative':len(cuts),
        'ZZ_minimum_display':min(c['slack_display'] for c in zz),
        'frozen_pack_negative_counts':[d['negative_count'] for d in diagnostics],
        'frozen_transport_slacks':transport_values,'elapsed_seconds':time.time()-started},ensure_ascii=False),flush=True)

if __name__=='__main__':main()
