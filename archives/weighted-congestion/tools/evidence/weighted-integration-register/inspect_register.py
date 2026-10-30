#!/usr/bin/env python3
"""Inspect the historical register as data; run no audit, CLI child or Git.

The original is reused from the preceding replay-entry evidence rather than
copied again. All source observations/classifications are exported losslessly.
Inventory comparisons compare digest metadata, not 164 fetched source files.
"""
from pathlib import Path
import argparse,collections,csv,hashlib,json,re


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo',type=Path,default=Path(__file__).resolve().parents[4])
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();repo=args.repo.resolve();out=args.output
    if out.exists():parser.error('output must be a new directory')
    inventory=[json.loads(x) for x in (repo/'cleanup/inventory.jsonl').read_text().splitlines()]
    meta=next(x for x in inventory if x['id']=='fb6582949719b818251e')
    original=repo/'archives/weighted-congestion/tools/evidence/weighted-replay-entry/original'/meta['path']
    data=original.read_bytes();assert len(data)==meta['size'] and hashlib.sha256(data).hexdigest()==meta['sha256']
    duplicates=[]
    def objects(pairs):
        result={}
        for k,v in pairs:
            if k in result:duplicates.append(k)
            result[k]=v
        return result
    doc=json.loads(data,object_pairs_hook=objects);assert not duplicates
    assert set(doc)=={'schema_version','base_main','policy','branches','source_files','classification','completed_cleanup'}
    assert doc['schema_version']==1
    sources=doc['source_files'];classified=doc['classification'];assert set(sources)==set(classified)
    bypath=collections.defaultdict(list)
    for x in inventory:bypath[x['path']].append(x)
    table=[];cross=collections.Counter();mismatches=[];source_observations=[];topics=collections.defaultdict(collections.Counter)
    for old,observations in sources.items():
        assert observations
        item=classified[old]
        assert all(set(x)=={'branch','commit','sha256'} and re.fullmatch('[0-9a-f]{40}',x['commit']) and re.fullmatch('[0-9a-f]{64}',x['sha256']) for x in observations)
        if 'sources'in item:assert item['sources']==observations
        else:assert old=='tests/test_wc_asset_roles.py'
        if 'path'in item:
            assert all(k in item for k in ['disposition','role','topic','sha256','sources'])
            versions=bypath[item['path']];assert versions
            oldmatch=any(x['sha256']==item['sha256'] for x in observations)
            currentmatch=any(x['sha256']==item['sha256'] for x in versions)
            cross[str((oldmatch,currentmatch))]+=1
            row={'old_path':old,'canonical_path':item['path'],'disposition':item['disposition'],'role':item['role'],'topic':item['topic'],'declared_canonical_sha256':item['sha256'],'declaration_matches_old_observation':oldmatch,'declaration_matches_current_frozen_inventory_digest':currentmatch,'current_frozen_versions':[{'id':x['id'],'sha256':x['sha256'],'size':x['size']}for x in versions]}
            table.append(row);topics[item['topic']][item['role']]+=1
            if not currentmatch:mismatches.append(row)
        else:assert item['disposition']=='git_history_only' and item['reason']
        for obs in observations:
            source_observations.append({'old_path':old,**obs,'classification_disposition':item['disposition'],'canonical_path':item.get('path'),'role':item.get('role'),'topic':item.get('topic')})
    mapped=[x for x in classified.values()if'path'in x]
    counts=collections.Counter(x['path']for x in mapped);assert max(counts.values())==1
    reconstructed=[{'old_path':p,**x}for p,x in classified.items()if x['disposition']=='reconstructed'];assert len(reconstructed)==1
    assert reconstructed[0]['source_commit'] in {x['commit']for x in sources[reconstructed[0]['old_path']]}
    summary={'schema_version':doc['schema_version'],'base_main':doc['base_main'],'policy':doc['policy'],'source_path_count':len(sources),'source_observation_count':len(source_observations),'distinct_old_path_sha_versions':sum(len({x['sha256']for x in v})for v in sources.values()),'classification_dispositions':dict(collections.Counter(x['disposition']for x in classified.values())),'mapped_path_count':len(mapped),'unmapped_history_only_count':len(classified)-len(mapped),'canonical_path_unchanged_count':sum(p==x['path']for p,x in classified.items()if'path'in x),'canonical_path_changed_count':sum(p!=x['path']for p,x in classified.items()if'path'in x),'path_alias_collisions':[],'canonical_roles':dict(collections.Counter(x['role']for x in mapped)),'topics':{t:dict(v)for t,v in sorted(topics.items())},'source_observation_branches':dict(collections.Counter(x['branch']for x in source_observations)),'branch_dispositions':dict(collections.Counter(x['disposition']for x in doc['branches'])),'declared_canonical_sha_vs_old_observation_and_current_frozen_inventory':dict(cross),'historical_sha_drift_count':len(mismatches),'drift_suffixes':dict(collections.Counter(Path(x['canonical_path']).suffix for x in mismatches)),'current_inventory_comparison_method':'Compare recorded digest strings; no claim to have fetched or read all 164 target files.','new_math_audit_or_cli_child_executions':0,'git_commands_executed':0}
    assert summary['source_path_count']==170 and summary['source_observation_count']==239 and summary['distinct_old_path_sha_versions']==173
    assert summary['mapped_path_count']==164 and len(mismatches)==65
    out.mkdir(parents=True)
    def save(name,value):(out/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
    save('register-review.json',{'summary':summary,'all_mapped_path_metadata':table,'hash_drift_records':mismatches,'all_unmapped_history_records':[{'old_path':p,'classification':x,'source_observations':sources[p]}for p,x in classified.items()if'path'not in x],'reconstructed_record':reconstructed,'all_branches_as_historically_recorded':doc['branches'],'completed_cleanup_as_historically_recorded':doc['completed_cleanup']})
    save('source-observations.json',source_observations)
    with (out/'canonical-paths.tsv').open('w',newline='')as f:
        fields=['old_path','canonical_path','disposition','role','topic','declared_canonical_sha256','declaration_matches_old_observation','declaration_matches_current_frozen_inventory_digest']
        writer=csv.DictWriter(f,fieldnames=fields,delimiter='\t',extrasaction='ignore');writer.writeheader();writer.writerows(table)
    save('provenance.json',{'claim_commit':'a3d62358d32360bf41e0bc40eb52bd77298c1483','assigned_source_count':1,'source':meta,'original_reused_at':str(original.relative_to(repo)),'actual_original_sha256':hashlib.sha256(data).hexdigest(),'source_file_copy_added':False,'comparison_reused':'archives/weighted-congestion/tools/evidence/weighted-replay-entry/classification-review.json','math_source_reading_scope':'This source is a historical metadata register, not the 170 underlying mathematical source files. All register fields/rows are read and accounted for; underlying results use separately read formal objects.'})
    print(json.dumps(summary,ensure_ascii=False,indent=2))


if __name__=='__main__':main()
