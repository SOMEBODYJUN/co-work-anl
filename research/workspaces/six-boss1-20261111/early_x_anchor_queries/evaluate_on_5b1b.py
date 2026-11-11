#!/usr/bin/env python3
"""Evaluate the already-frozen 51 AP rows at the newly authorized exact point.

This post-freeze diagnostic does not change the prior packet or its manifest,
does not open the old cb45 point, and does not import or call an optimizer.
"""
from collections import Counter
from datetime import datetime, timezone
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
import gzip
import json

HERE = Path(__file__).resolve().parent
WORK = HERE.parent
REPO = WORK.parents[2]
POINT = WORK/'maxb_augmented_lp/full_lift/recovery/augmented_lp_exact.json'
POINT_SHA = '5b1b649af5fc9d359e31dd03945d12708e599e0eeac75983ed188e60178b3bfe'
FROZEN_SHA = 'd9108516ee468be141ea223b61a167220f85bff933151b650b322e4bea65870f'
ROW_SHA = '0ad0b697193d7a8da2cc62275bbf9265912b0485d778d5edd93fc334bd8bb3eb'


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def frozen(value):
    return tuple(map(frozen,value)) if isinstance(value,list) else value


def save(name,value):
    path=HERE/name
    assert not path.exists(),('refuse_overwrite',str(path))
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')


def sign(value):
    return 'positive' if value>0 else 'negative' if value<0 else 'zero'


def main():
    assert digest(HERE/'freeze_manifest.json')==FROZEN_SHA
    initial=json.loads((HERE/'freeze_manifest.json').read_text())
    for item in initial['assets']:
        assert digest(REPO/item['path'])==item['sha256'],item['path']
    assert digest(POINT)==POINT_SHA and digest(HERE/'rows_51.json')==ROW_SHA
    packet=json.loads((HERE/'rows_51.json').read_text())
    with gzip.open(HERE/'columns_21021.json.gz','rt') as file:
        columns=json.load(file)
    point=json.loads(POINT.read_text())
    descriptors=[{k:v for k,v in c.items() if k!='weight'} for c in point['columns']]
    assert descriptors==columns and len(columns)==21021
    values=[F(c['weight']) for c in point['columns']]
    assert min(values)>=0 and F(point['O'])==1
    hist={h:c for h,c in enumerate(columns) if c['kind']=='hist'}
    assert len(hist)==16
    xcols={c['hist_column']:j for j,c in enumerate(columns) if c['kind']=='common-X-mass'}
    upper={(c['hist_column'],frozen(c['query_token'])):j for j,c in enumerate(columns)
           if c['kind']=='X-query-overlap-upper'}
    assert len(xcols)==16 and len(upper)==420
    for (h,token),j in upper.items():
        marginal=sum((F(a)*values[k] for k,a in columns[j]['query_marginal']),F())
        assert values[j]==min(values[xcols[h]],marginal)
    income={i:sum((values[h]/sum(map(int,c['actual_bits'])) for h,c in hist.items()
                   if c['actual_bits'][i-1]=='1'),F()) for i in range(1,7)}
    assert sum(income.values(),F())==F(point['W'])
    rows=[]
    for index,row in enumerate(packet['rows']):
        value=sum((F(a)*values[j] for j,a in row['row']),F())
        i,r,C=row['actual_player'],row['remaining_players'],F(row['C'])
        kappa=F();quote=F();correction=F()
        for record in row['histogram_frequencies']:
            h=record['hist_column']
            b=sum(map(int,hist[h]['actual_bits'][:i-1]))
            kappa+=values[xcols[h]]/F(b+r)
            for raw,n in record['frequencies']:
                token=frozen(raw)
                probability=F(n,row['orbit_size'])
                if token[0]=='bit':
                    q=values[h]*token[1]
                    xy=values[xcols[h]]*token[1]
                else:
                    j=upper[h,token]
                    q=sum((F(a)*values[k] for k,a in columns[j]['query_marginal']),F())
                    xy=values[j]
                quote+=probability*q/F(b+1)
                correction+=probability*F(r-1,(b+1)*(b+r))*xy
        assert value==C*income[i]-(C-1)*kappa-quote+correction
        rows.append({'index':index,'name':row['name'],'actual_player':i,
                     'remaining_players':r,'C':str(C),'orbit_size':row['orbit_size'],
                     'u_i':str(income[i]),'kappa_X':str(kappa),
                     'SAFE_slack':str(income[i]-kappa),
                     'average_query_quote':str(quote),
                     'average_positive_overlap_correction':str(correction),
                     'exact_slack':str(value),'slack_float':float(value),'sign':sign(value)})
    assert len(rows)==51
    counts=Counter(row['sign'] for row in rows)
    minimum=min(F(row['exact_slack']) for row in rows)
    minima=[row for row in rows if F(row['exact_slack'])==minimum]
    per_player={}
    for i in range(1,4):
        subset=[row for row in rows if row['actual_player']==i]
        totals=Counter(row['sign'] for row in subset)
        least=min(F(row['exact_slack']) for row in subset)
        per_player[str(i)]={'rows':17,'positive':totals['positive'],'zero':totals['zero'],
                            'negative':totals['negative'],'minimum_exact_slack':str(least),
                            'minimum_slack_float':float(least),
                            'minimum_names':[row['name'] for row in subset if F(row['exact_slack'])==least]}
    result={'status':'EXACT_POST_FREEZE_EVALUATION_COMPLETE',
            'scope':'Evaluation of the frozen 51 AP rows at this one newly authorized exact primal; no optimization or new theorem.',
            'point_path':str(POINT.relative_to(REPO)),'point_sha256':POINT_SHA,
            'row_packet_sha256':ROW_SHA,'prior_frozen_manifest_sha256':FROZEN_SHA,
            'point_W':point['W'],'point_W_float':float(F(point['W'])),
            'point_reported_verified_rows':point['verified_rows'],
            'point_full_feasibility_reverified_here':False,
            'all_21021_descriptors_match_frozen_coordinate_copy':True,
            'all_coordinates_nonnegative':True,'O':'1',
            'all_six_actual_incomes_sum_exactly_to_W':True,
            'all_420_new_overlap_coordinates_equal_canonical_min':True,
            'all_51_sparse_products_equal_direct_source_formula':True,
            'row_count':51,'positive':counts['positive'],'zero':counts['zero'],'negative':counts['negative'],
            'minimum_exact_slack':str(minimum),'minimum_slack_float':float(minimum),
            'minimum_rows':minima,'per_player':per_player,'rows':rows,
            'point_excluded_by_this_51_row_package':counts['negative']>0,
            'optimum_improvement_proved':False,'six_player_half_proved':False,
            'cb45_point_opened':False,'optimizer_called':False,'inputs_mutated':False,
            'created_utc':datetime.now(timezone.utc).isoformat()}
    assert digest(POINT)==POINT_SHA and digest(HERE/'freeze_manifest.json')==FROZEN_SHA
    for item in initial['assets']:
        assert digest(REPO/item['path'])==item['sha256'],item['path']
    save('evaluation_on_5b1b.json',result)
    assets=[Path(__file__),HERE/'evaluation_on_5b1b.json']
    manifest={'status':'POST_FREEZE_EVALUATION_FROZEN_RELEASED',
              'prior_frozen_manifest_sha256':FROZEN_SHA,'point_sha256':POINT_SHA,
              'row_packet_sha256':ROW_SHA,'rows_evaluated':51,
              'positive':counts['positive'],'zero':counts['zero'],'negative':counts['negative'],
              'original_frozen_assets_unchanged':True,'optimizer_called':False,
              'assets':[{'path':str(p.relative_to(REPO)),'sha256':digest(p),'bytes':p.stat().st_size} for p in assets],
              'created_utc':datetime.now(timezone.utc).isoformat()}
    save('evaluation_freeze_manifest.json',manifest)
    print(json.dumps({key:result[key] for key in ('status','row_count','positive','zero','negative',
                      'minimum_exact_slack','minimum_slack_float','per_player',
                      'point_excluded_by_this_51_row_package')},ensure_ascii=False,indent=2))


if __name__=='__main__':
    main()
