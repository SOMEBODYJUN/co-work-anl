#!/usr/bin/env python3
"""Prepare, without optimizing, the complete finite 39-class ZZ upper mechanism.

Each new z is an auxiliary upper-bound variable, not a claimed true joint mass.
All old 5799 rows and 4849 descriptors are preserved, with zero new coefficients.
"""
from collections import Counter,defaultdict
from fractions import Fraction as F
from pathlib import Path
import datetime,gzip,hashlib,io,json,sys,time
HERE=Path(__file__).resolve().parent
REPO=HERE.parents[3]
STEM='complete_zz_5799_v1'
BASE=HERE/'dynamic_5799_matrix.json.gz'
POINT=HERE/'dynamic_5799_exact.json'
BASE_SHA='0b4bd0a81097b022a638fdc44324c731768255579a5bf07618e12c35c9342bec'
POINT_SHA='63edbafd53493a20ec64ced5f09a694ead3f894bfb6419cde425de0b3a1710c1'

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def canonical(value):
    return hashlib.sha256(json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def pattern(values):
    names={}
    return tuple(names.setdefault(value,len(names)) for value in values)
def sparse(row):return [[j,str(v)] for j,v in sorted(row.items()) if v]
def save(suffix,value):
    p=HERE/(STEM+'_'+suffix+'.json');assert not p.exists()
    p.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n');return p
def append_row(rows,name,values,kind,**metadata):
    entries=sparse(values);assert entries
    rows.append({'index':len(rows),'name':name,'sparse_sha256':canonical(entries),
                 'nonzero':entries,'new_row_kind':kind,**metadata})

def main():
    started=time.time();started_utc=datetime.datetime.now(datetime.timezone.utc).isoformat()
    assert sha(BASE)==BASE_SHA and sha(POINT)==POINT_SHA
    output=HERE/(STEM+'_matrix.json.gz');assert not output.exists()
    with gzip.open(BASE,'rt',encoding='utf-8') as f:base=json.load(f)
    point=json.loads(POINT.read_text())
    assert base['row_count']==5799 and base['column_count']==4849
    assert [{k:v for k,v in c.items() if k!='weight'} for c in point['columns']]==base['columns']
    x=[F(c['weight']) for c in point['columns']]
    old_columns=len(x);old_rows=len(base['rows'])
    blocks={};current=None
    for j,column in enumerate(base['columns']):
        if column['kind']=='hist':
            current=j;blocks[j]={'descriptor':column,'groups':defaultdict(dict)}
        elif column['kind']=='joint-reply':
            group=column['group'];key=(group[0],group[1],tuple(group[2]),tuple(group[3]))
            blocks[current]['groups'][key][tuple(column['state'])]=j
    assert len(blocks)==16 and sum(len(b['groups']) for b in blocks.values())==194
    edges=[(family,i,j) for family in (0,1) for i in range(6) for j in range(6) if family or i!=j]
    assert len(edges)==66
    all_classes=defaultdict(list)
    for e,(f,i,j) in enumerate(edges):
        for other,(ff,k,l) in enumerate(edges):
            label=(f,ff,pattern((i,j,k,l)))
            if e!=other:all_classes[label].append((e,other))
            else:all_classes[label]
    assert len(all_classes)==42
    omitted=[label for label,pairs in sorted(all_classes.items()) if not pairs]
    assert omitted==[(0,0,(0,1,0,1)),(1,1,(0,0,0,0)),(1,1,(0,1,0,1))]
    labels=[label for label,pairs in sorted(all_classes.items()) if pairs]
    assert len(labels)==39
    class_number={label:i for i,label in enumerate(labels)}
    columns=list(base['columns']);rows=list(base['rows'])
    budgets={label:defaultdict(F) for label in labels}
    block_maps=[];auxiliaries=[];degree_checks=0
    for h,block in blocks.items():
        descriptor=block['descriptor'];words=[]
        for word,count in enumerate(descriptor['hist']):words += [tuple(map(int,f'{word:03b}'))]*count
        assert len(words)==6
        group_at=[(f,int(i==j),words[i],words[j]) for f,i,j in edges]
        groups=sorted(block['groups']);gid={g:i for i,g in enumerate(groups)}
        edge_sets=defaultdict(list)
        for e,g in enumerate(group_at):edge_sets[g].append(e)
        assert set(groups)==set(edge_sets)
        counts={};used_pairs=set()
        for label in labels:
            pair_sets=defaultdict(list)
            for e,f in all_classes[label]:pair_sets[group_at[e],group_at[f]].append((e,f))
            current_counts={}
            for (g,k),pairs in pair_sets.items():
                source_degrees=Counter(e for e,f in pairs);query_degrees=Counter(f for e,f in pairs)
                assert len({source_degrees[e] for e in edge_sets[g]})==1
                assert len({query_degrees[f] for f in edge_sets[k]})==1
                degree_checks+=2
                current_counts[g,k]=len(pairs);used_pairs.add((g,k))
            assert sum(current_counts.values())==len(all_classes[label])
            counts[label]=current_counts
        z_index={};group_records=[]
        for g in groups:
            states=block['groups'][g];assert set(states)=={(0,1),(1,0),(1,1)}
            group_records.append({'group_id':gid[g],'group':[g[0],g[1],list(g[2]),list(g[3])],
                'joint_columns':{'01':states[0,1],'10':states[1,0],'11':states[1,1]},
                'literal_edge_indices':edge_sets[g]})
        for g,k in sorted(used_pairs):
            j=len(columns);z_index[g,k]=j
            source=block['groups'][g];query=block['groups'][k]
            q_columns=[source[1,0],source[1,1]];v_columns=[query[0,1],query[1,1]]
            column={'kind':'zz-frechet-upper-auxiliary','hist_column':h,
                'source_group':[g[0],g[1],list(g[2]),list(g[3])],
                'query_group':[k[0],k[1],list(k[2]),list(k[3])],
                'meaning':'auxiliary z <= min(q_source,v_query), not a true cross intersection'}
            columns.append(column)
            upper_q=defaultdict(F,{j:F(-1)});upper_v=defaultdict(F,{j:F(-1)})
            for c in q_columns:upper_q[c]+=1
            for c in v_columns:upper_v[c]+=1
            row_q=len(rows);append_row(rows,f'zz-complete:upper-q:h{h}:g{gid[g]}:k{gid[k]}',upper_q,'upper-q',auxiliary_column=j)
            row_v=len(rows);append_row(rows,f'zz-complete:upper-v:h{h}:g{gid[g]}:k{gid[k]}',upper_v,'upper-v',auxiliary_column=j)
            q=sum(x[c] for c in q_columns);v=sum(x[c] for c in v_columns)
            auxiliaries.append({'column_index':j,'hist_column':h,'source_group_id':gid[g],
                'query_group_id':gid[k],'source_R_columns':q_columns,'query_Z_columns':v_columns,
                'upper_q_row':row_q,'upper_v_row':row_v,'canonical_value_at_base':str(min(q,v))})
        P=sum(map(int,descriptor['actual_bits'][:4]));D=(P+1)*(P+2)
        class_counts=[]
        for label in labels:
            entries=[];N=len(all_classes[label]);out=budgets[label]
            for (g,k),count in sorted(counts[label].items()):
                source=block['groups'][g];query=block['groups'][k]
                weight=F(count,N)
                for state in ((0,1),(1,1)):
                    out[source[state]]+=weight/F(P+1)
                    out[query[state]]-=weight/F(P+1)
                out[source[1,1]]-=weight/F(D)
                out[z_index[g,k]]+=weight/F(D)
                entries.append([gid[g],gid[k],count])
            class_counts.append({'class_index':class_number[label],'pair_counts':entries})
        block_maps.append({'hist_column':h,'actual_bits':descriptor['actual_bits'],
            'P':P,'words':[list(w) for w in words],'groups':group_records,
            'used_auxiliaries':[[z_index[g,k],gid[g],gid[k]] for g,k in sorted(used_pairs)],
            'class_pair_counts':class_counts})
    budget_start=len(rows);classes=[]
    for label in labels:
        index=len(rows);f,ff,equality=label;N=len(all_classes[label])
        append_row(rows,f"zz-complete:budget:{f}:{ff}:{''.join(map(str,equality))}",budgets[label],
                   'normalized-ZZ-budget',literal_pairs=N,class_index=class_number[label],
                   literal_class=[f,ff,list(equality)])
        classes.append({'class_index':class_number[label],'class':[f,ff,list(equality)],
            'literal_pairs':N,'normalization_scale':str(F(1,N)),'row_index':index})
    n_aux=len(auxiliaries);assert len(columns)==4849+n_aux
    assert len(rows)==5799+2*n_aux+39
    assert rows[:5799]==base['rows'] and columns[:4849]==base['columns']
    objective=base['objective']+['0']*n_aux;normalization=base['normalization']+['0']*n_aux
    extended=dict(base)
    extended.update({'scope':'Fixed sixteen histograms: unchanged certified 5799 master, plus an exact auxiliary representation of every non-self class of the finite ZZ Frechet upper-bound mechanism. Auxiliary z are not true intersections. Prepared only; optimization requires separate approval.',
        'base_row_count':5799,'base_column_count':4849,'added_row_count':2*n_aux+39,
        'added_column_count':n_aux,'row_count':len(rows),'column_count':len(columns),
        'rows':rows,'columns':columns,'objective':objective,'normalization':normalization,
        'nonnegative_columns':'all','fixed_ZZ_class_count':39})
    # Deterministic gzip header: identical coefficients and metadata replay to
    # identical archived bytes, independent of invocation time.
    raw=json.dumps(extended,ensure_ascii=False,separators=(',',':')).encode()
    with output.open('wb') as f:
        with gzip.GzipFile(fileobj=f,mode='wb',filename='',mtime=0) as zipped:zipped.write(raw)
    maps=save('mapping',{'base_matrix':str(BASE.relative_to(REPO)),'base_matrix_sha256':BASE_SHA,
        'base_point_sha256':POINT_SHA,'literal_edges':[list(e) for e in edges],
        'omitted_pure_self_classes':[[f,ff,list(p)] for f,ff,p in omitted],
        'classes':classes,'hist_blocks':block_maps,'auxiliaries':auxiliaries,
        'source_column_prefix':4849,'source_row_prefix':5799,
        'upper_row_range':[5799,budget_start],'budget_row_range':[budget_start,len(rows)]})
    fill=x+[F(a['canonical_value_at_base']) for a in auxiliaries]
    assert len(fill)==len(columns) and min(fill)>=0
    assert sum(F(c)*v for c,v in zip(normalization,fill))==1
    assert sum(F(c)*v for c,v in zip(objective,fill))==F(point['W'])
    upper_slacks=[sum(F(v)*fill[j] for j,v in row['nonzero']) for row in rows[5799:budget_start]]
    assert min(upper_slacks)>=0
    budget_values=[sum(F(v)*fill[j] for j,v in rows[c['row_index']]['nonzero']) for c in classes]
    # Verify exact equality with independently prepared literal-class min rows
    # at this point. This is a construction check, not the Main independent audit.
    reference=HERE/'neighbor_5799_audit_v1.json';audit=json.loads(reference.read_text())
    assert audit['point_sha256']==POINT_SHA
    comparison={tuple([c['class'][0],c['class'][1],tuple(c['class'][2])]):c for c in audit['zz_classes']}
    for label,value in zip(labels,budget_values):
        item=comparison[label]
        assert value==F(item['exact_slack'])/item['literal_pairs']
    fill_path=save('canonical_fill',{'scope':'The 5799 point with every auxiliary at its maximal allowed value; a diagnostic fill, NOT an extension-feasible point.',
        'source_point_sha256':POINT_SHA,'auxiliary_values':[[a['column_index'],a['canonical_value_at_base']] for a in auxiliaries],
        'minimum_upper_slack':str(min(upper_slacks)),
        'negative_budget_count':sum(v<0 for v in budget_values),
        'budget_values':[{'row_index':c['row_index'],'class':c['class'],'slack':str(v)} for c,v in zip(classes,budget_values)],
        'reference_min_audit_sha256':sha(reference)})
    # Structural direction of elimination: old rows do not read z, each z
    # enters only its two -z upper rows and positive budget coefficients.
    positive_budget_uses=Counter()
    for row in rows[budget_start:]:
        for j,v in row['nonzero']:
            if j>=4849:assert F(v)>0;positive_budget_uses[j]+=1
    assert set(positive_budget_uses)==set(range(4849,len(columns)))
    identity=save('identity',{'status':'PREPARED_EXACT_NOT_OPTIMIZED','base_matrix_sha256':BASE_SHA,
        'base_point_sha256':POINT_SHA,'base_rows':5799,'base_columns':4849,
        'rows':len(rows),'columns':len(columns),'added_upper_rows':2*n_aux,
        'added_budget_rows':39,'added_auxiliary_columns':n_aux,
        'nonzeros':sum(len(r['nonzero']) for r in rows),
        'matrix_sha256':sha(output),'mapping_sha256':sha(maps),'canonical_fill_sha256':sha(fill_path),
        'old_column_descriptor_sha256':canonical(columns[:4849]),
        'all_column_descriptor_sha256':canonical(columns),
        'row_vector_list_sha256':canonical([r['sparse_sha256'] for r in rows]),
        'literal_equal_degree_checks':degree_checks,'negative_budgets_at_canonical_base_fill':sum(v<0 for v in budget_values),
        'elimination':'For any nonnegative old variables, q,v are nonnegative; z=min(q,v) satisfies both upper rows and maximizes all 39 budgets coordinatewise. Hence an auxiliary completion exists iff all 39 substituted min upper bounds are nonnegative. No true-joint interpretation.',
        'command':[sys.executable,'-B',str(Path(__file__).resolve())],'script_sha256':sha(Path(__file__)),
        'started_utc':started_utc,'elapsed_seconds':time.time()-started,
        'optimizer_calls':0,'floating_point_math':0})
    print(json.dumps(json.loads(identity.read_text()),ensure_ascii=False),flush=True)

if __name__=='__main__':main()
