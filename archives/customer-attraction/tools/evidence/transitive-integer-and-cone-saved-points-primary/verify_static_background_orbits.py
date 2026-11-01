"""One current static rational reconstruction. No original program import/DP/LP.

The mathematical completeness argument is the eleven pairs of partitions of
four rivals across two blocks of four labels, plus transitive uniform query.
All recorded SPE minimum-welfare, G rows, and strategy claims remain unaudited.
"""
from pathlib import Path
from itertools import permutations, combinations
from fractions import Fraction
from math import comb
import json,hashlib
ROOT=Path(__file__).resolve().parent
PREFIX=ROOT/'source-root/research/workspaces/customer-attraction/R-ab183d14fb74403091d09db766b05f73/security'
FILES={'integer':('transitive_n5_g4.json','b64a2462d52736d3dec034531eaf234f92d2e3e9166dfaba1b91e7067b95660a'),'cone':('transitive_cones_n5_g4.json','a3fda4cfadbe78708569135274a9e754d833af2e50f2839c52df8fc6ed889c6b')}
data={};sources=[]
for role,(name,sha) in FILES.items():
    b=(PREFIX/name).read_bytes()
    assert hashlib.sha256(b).hexdigest()==sha
    data[role]=json.loads(b);sources.append({'role':role,'file':name,'sha256':sha,'size':len(b)})
classes=[tuple(c) for c in data['integer']['classes']]
assert classes==[tuple(c) for c in data['cone']['classes']]
assert classes==[(a,b) for a in range(5) for b in range(a,5) if (a,b) not in [(0,0),(4,4)]]
representatives=[
 (0,0,0,0,4,0,0,0),(0,0,0,0,3,1,0,0),(0,0,0,0,2,2,0,0),
 (0,0,0,0,2,1,1,0),(0,0,0,0,1,1,1,1),
 (1,0,0,0,3,0,0,0),(1,0,0,0,2,1,0,0),(1,0,0,0,1,1,1,0),
 (2,0,0,0,2,0,0,0),(2,0,0,0,1,1,0,0),(1,1,0,0,1,1,0,0)]
expected_sizes=[8,24,12,24,2,32,96,32,16,48,36]
orbits=[];table=[]
for i,h in enumerate(representatives):
    a=set(permutations(h[:4]));b=set(permutations(h[4:]));orb={x+y for x in a for y in b}|{y+x for x in a for y in b}
    assert len(orb)==expected_sizes[i] and all(len(q)==8 and sum(q)==4 for q in orb)
    orbits.append(orb);row=[0]*13
    for mask in range(1,256):
        cl=tuple(sorted(((mask&15).bit_count(),(mask>>4).bit_count())))
        if cl not in classes:continue
        d=1+sum(h[j] for j in range(8) if mask>>j&1)
        assert 60%d==0
        row[classes.index(cl)]+=mask.bit_count()*(60//d)
    table.append(row)
assert sum(map(len,orbits))==len(set.union(*orbits))==comb(11,7)==330
orbit_sizes=[(2 if a<b else 1)*comb(4,a)*comb(4,b) for a,b in classes]
records=[('best',data['integer']['best'])]+[(f'bank[{i}]',r) for i,r in enumerate(data['integer']['bank'])]+[(f'results[{i}].initial',r['initial']) for i,r in enumerate(data['cone']['results'])]
checks=[];mismatches=[]
for name,r in records:
    x=r['orbit_weights'];assert len(x)==13 and all(type(v) is int and v>=0 for v in x)
    expanded=[]
    for mask in range(1,256):
        cl=tuple(sorted(((mask&15).bit_count(),(mask>>4).bit_count())))
        expanded.append(x[classes.index(cl)] if cl in classes else 0)
    values=[sum(c*v for c,v in zip(row,x)) for row in table]
    vnum=min(values);mins=[i for i,v in enumerate(values) if v==vnum]
    bgs=set.union(*(orbits[i] for i in mins));saved=[tuple(h) for h in r['minimizing_backgrounds']]
    N=sum(expanded);positive=[mask for mask,v in enumerate(expanded,1) if v]
    listed=r['worst_counts'];full_coverage=all(len(q)==8 and sum(q)==5 and all(v in (0,1) for v in q) for q in listed) and all(mask.bit_count()>=4 for mask in positive)
    flags={'n5_k8':r['n']==5 and r['k']==8,'expanded_all_255_weights_match':expanded==r['weights'],
      'uniform_query_exact':all(Fraction(str(q))==Fraction(1,8) for q in r['query']) and len(r['query'])==8,
      'static_value_numerator_match':vnum==r['value_numerator'],'static_value_denominator_match':r['value_denominator']==480,
      'all_minimizing_background_vectors_match':set(saved)==bgs and len(saved)==len(bgs),
      'minimizing_background_order_matches_lex_count_order':saved==sorted(bgs,reverse=True),
      'reported_W_equals_customer_total':r['min_welfare']==N,'listed_terminal_full_coverage_by_interest_size':full_coverage,
      'gap_numerator_arithmetic_match':r['gap_numerator']==N*480-5*vnum}
    if not all(flags.values()):mismatches.append({'record':name,'failed':[k for k,v in flags.items() if not v]})
    checks.append({'record':name,'orbit_weights':x,'customers':N,'nonzero_types':len(positive),
       'minimum_static_numerator':vnum,'static_denominator':480,'exact_static_value':str(Fraction(vnum,480)),
       'all_11_static_numerators':values,'minimizing_background_orbit_indices':mins,
       'minimizing_background_count':len(bgs),'listed_terminal_count':len(listed),
       'listed_full_coverage_gap_over_static_value':str(Fraction(N*480-5*vnum,480)),
       'reported_relative_gap_as_exact_ratio':str(Fraction(N*480-5*vnum,5*vnum)) if vnum else None,
       'checks':flags,'original_full_SPE_minimum_welfare_independently_certified':False})
cone_rows=[]
for i,r in enumerate(data['cone']['results']):
    x=[Fraction(str(v)) for v in r['orbit_weights']]
    scores=[sum((Fraction(c)*v for c,v in zip(row,x)),Fraction())/480 for row in table]
    v=min(scores);N=sum((s*y for s,y in zip(orbit_sizes,x)),Fraction())
    flags={'same_single_dense_type_orbit':x==[Fraction(1,8) if j==12 else Fraction() for j in range(13)],
       'exact_static_value_matches_decimal':v==Fraction(str(r['value'])),
       'exact_listed_root_coverage_one':N==1 and sum(r['root'])==5 and all(t in (0,1) for t in r['root']),
       'exact_gap_matches_decimal':1-5*v==Fraction(str(r['gap']))}
    if not all(flags.values()):mismatches.append({'record':f'results[{i}]','failed':[k for k,z in flags.items() if not z]})
    cone_rows.append({'record':f'results[{i}]','rational_orbit_weights':[str(z) for z in x],
      'customer_mass':str(N),'exact_static_value':str(v),'exact_listed_root_gap':str(1-5*v),
      'minimizing_background_orbit_indices':[j for j,z in enumerate(scores) if z==v],
      'minimizing_background_count':sum(len(orbits[j]) for j,z in enumerate(scores) if z==v),
      'checks':flags,'G_or_policy_independently_certified':False})
result={'status':'PASS_STATIC_VALUES_AND_RECORDED_VECTOR_ARITHMETIC_ONLY' if not mismatches else 'STATIC_RECONSTRUCTION_MISMATCH',
 'current_reconstruction_not_historical_execution':True,'original_program_imports':0,'original_DP_SPE_IC_LP_random_entries':0,
 'sources':sources,'classes':classes,'orbit_size_per_customer_type_class':orbit_sizes,
 'static_background_total':330,'group_background_orbits':11,'coefficient_common_denominator':480,
 'background_orbit_table':[{'index':i,'representative':h,'orbit_size':len(orbits[i]),'coefficient_numerators':table[i]} for i,h in enumerate(representatives)],
 'integer_record_count_including_duplicate_best':len(records),'distinct_integer_inputs':len({tuple(r['weights']) for _,r in records}),
 'maximum_total_customers':max(sum(r['weights']) for _,r in records),'machine_scaled_query_sum_bound':480*max(sum(r['weights']) for _,r in records),
 'records':checks,'normalized_cone_output_static_checks':cone_rows,'mismatches':mismatches,
 'certification_exclusions':['original full-SPE minimum welfare','completeness of original outcome sets','fixed G inequalities','original policy','LP optimality or infeasibility','actual original argv/source version/runtime']}
output=ROOT/'current-static-value-certificate.json';output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'status':result['status'],'background_orbits':11,'background_counts':330,'integer_records':len(records),'distinct_integer_inputs':result['distinct_integer_inputs'],'cone_output_records':len(cone_rows),'mismatch_count':len(mismatches)},ensure_ascii=False))
