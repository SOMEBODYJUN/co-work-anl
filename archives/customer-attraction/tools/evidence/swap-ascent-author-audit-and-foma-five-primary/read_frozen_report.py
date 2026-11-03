"""Lossless frozen-JSON reading only: no payoff, SPE, solver or source imports."""
import json
from pathlib import Path


def main():
    here=Path(__file__).resolve().parent
    source=here/'original/swap_ascent_counterexample_audit.json'
    original=json.loads(source.read_text())
    reports=original['reports']
    comparison_keys=[[x['history'],x['deviation']] for x in reports[0]['comparisons_including_prescribed']]
    strategy=reports[0]['strategy']
    endpoint_keys=['outcome','old_B_profit','new_last_profit','W']
    encoded=[]
    for record in reports:
        assert record['strategy']==strategy
        assert [[x['history'],x['deviation']] for x in record['comparisons_including_prescribed']]==comparison_keys
        assert len(record)==17 and len(record['comparisons_including_prescribed'])==20
        compact={k:v for k,v in record.items() if k not in ('types','strategy','comparisons_including_prescribed','all_SPE_endpoints_after_fixed_B')}
        encoded.append({'fields':compact,'types':[[x['mask'],x['count']] for x in record['types']],
                        'endpoint_rows':[[x[k] for k in endpoint_keys] for x in record['all_SPE_endpoints_after_fixed_B']],
                        'comparison_gap_strings':[x['gap'] for x in record['comparisons_including_prescribed']]})
    ledger={'header':{k:v for k,v in original.items() if k!='reports'},'common_strategy':strategy,
            'comparison_history_action_keys':comparison_keys,'endpoint_field_order':endpoint_keys,'reports':encoded}
    restored=[]
    for entry in ledger['reports']:
        rec=dict(entry['fields'])
        rec['types']=[dict(zip(('mask','count'),x)) for x in entry['types']]
        rec['strategy']=ledger['common_strategy']
        rec['all_SPE_endpoints_after_fixed_B']=[dict(zip(ledger['endpoint_field_order'],x)) for x in entry['endpoint_rows']]
        rec['comparisons_including_prescribed']=[{'history':key[0],'deviation':key[1],'gap':gap}
                                                   for key,gap in zip(ledger['comparison_history_action_keys'],entry['comparison_gap_strings'])]
        restored.append(rec)
    decoded=dict(ledger['header']);decoded['reports']=restored
    assert decoded==original
    (here/'lossless-report-ledger.json').write_text(json.dumps(ledger,ensure_ascii=False,indent=2)+'\n')
    check={'status':'lossless semantic roundtrip passed','reports':len(reports),'fields_per_report':[len(x) for x in reports],
           'comparison_records':sum(len(x['comparisons_including_prescribed']) for x in reports),
           'fixed_B_endpoint_records':sum(len(x['all_SPE_endpoints_after_fixed_B']) for x in reports),
           'payoff_or_SPE_or_source_entry_executions':0}
    (here/'report-reading-check.json').write_text(json.dumps(check,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(check,ensure_ascii=False))

if __name__=='__main__':
    main()
