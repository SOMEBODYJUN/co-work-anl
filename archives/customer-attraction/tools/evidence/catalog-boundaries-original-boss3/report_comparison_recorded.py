from pathlib import Path
import hashlib,json
b=Path('/workspace/scratch/9559bf893d22');s=b/'boss3_boundary_padding_stage';r=b/'co-work-anl-boss3'
a=s/'archives/customer-attraction/tools/evidence/catalog-boundaries-original-boss3';p=s/'archives/customer-attraction/tools/evidence/safe-padding-three-reports-boss3'
def load(e,id,name):return json.loads((e/'original'/id/name).read_text())
def dump(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
maximal=load(a,'2860808d33ef55be8a45','maximal_catalog_boundary.json');compression=load(a,'e388bd6d29dc8e4a13ce','strict_compression_boundary.json')
maxrows=[]
for c in maximal['checks']:
 k=c['k'];assert c['players']==k+1
 for kind,q in [('maximal',2*k+1),('full',3*k+1)]:
  row=c[kind];assert row['opt']==3*k+2
  info=dict(k=k,kind=kind,topics=q,players=k+1,minimum=row['minimum_SPE_welfare'],outcome_counts=row['outcome_count'],designated_path=row['designated_path'])
  if 'decision_histories' in row:
   assert row['decision_histories']==sum(q**d for d in range(k+1))
   assert row['full_ordered_history_certificate_verified'] is True
   info['verified_certificate_histories']=row['decision_histories']
  maxrows.append(info)
comprows=[]
for c in compression['checks']:
 L=c['L'];assert c['proper_retained_subcatalogs_checked']==2**(L-1)-1
 assert c['minimum_last_reply_strict_gap']=='1' and c['minimum_forced_root_deviation_gain']=='1'
 comprows.append(dict(L=L,topics=c['topics'],customers=c['customer_count'],proper_subcatalogs=c['proper_retained_subcatalogs_checked'],W_OPT=c['welfare_equals_unique_optimum']))
dump(a/'report-structure-comparison.json',dict(scope='Saved report structural and integer-identity comparison, not another game/BI/IC execution',maximal_inputs=maxrows,verified_certificates=sum('verified_certificate_histories' in x for x in maxrows),verified_certificate_history_total=sum(x.get('verified_certificate_histories',0) for x in maxrows),compression_inputs=comprows,total_proper_subcatalogs=sum(x['proper_subcatalogs'] for x in comprows),full_catalog_minimum_equals_2k_plus2_only_finite_k1_to4=True,uniform_full_catalog_minimum_claimed=False))
old=load(p,'3d2b262066accaaa836e','safe_padding_audit_replay.json');strict=load(p,'1654c40a76a3d458e3d0','safe_padding_strict_catalog_replay.json');author=load(p,'f647d3bd371793998372','audit_safe_catalog_padding.json')
assert {k:strict[k] for k in author}==author
assert len(old['cases'])==len(strict['cases'])==36
common=['players','sample','old_max_size','minimum_gap','OPT','convolution'];changes=[]
for before,after in zip(old['cases'],strict['cases']):
 assert all(before[k]==after[k] for k in common)
 assert before['old_topics']==after['requested_old_topics']
 m=after['players'];q_old=before['old_topics']+m;q_new=after['old_topics']+(m if after['old_max_size'] else 0)
 assert before['comparisons']==sum(q_old**d for d in range(1,m+1))
 assert after['comparisons']==sum(q_new**d for d in range(1,m+1))
 if before['comparisons']!=after['comparisons']:
  changes.append(dict(players=m,requested_old_topics=before['old_topics'],sample=after['sample'],old_topics_before=before['old_topics'],old_topics_after=after['old_topics'],K=after['old_max_size'],comparisons_before=before['comparisons'],comparisons_after=after['comparisons'],difference=before['comparisons']-after['comparisons'],ext_topics_before=q_old,ext_topics_after=q_new))
assert sum(c['comparisons'] for c in old['cases'])==old['comparisons']==17106
assert sum(c['comparisons'] for c in strict['cases'])==strict['comparisons']==15849
assert sum(x['difference'] for x in changes)==1257 and len(changes)==3
code=p/'original/4aee24ec865e93986c02/audit_safe_catalog_padding.py'
statement=r/'archives/customer-attraction/tools/evidence/coupled-cartesian-and-safe-padding-primary/original/research/workspaces/customer-attraction/R-5d61c5324e744dc0a66133207fcbd010/security/safe_catalog_padding.md'
assert hashlib.sha256(code.read_bytes()).hexdigest()==strict['audit_source_sha256']
assert hashlib.sha256(statement.read_bytes()).hexdigest()==strict['statement_source_sha256']
dump(p/'three-report-comparison.json',dict(scope='Full 36-record field comparison and all-history comparison-count identities; no second policy generator or SPE run',current_author_report_equals_strict_replay_projection=True,current_author_report_root_fields=list(author),strict_replay_extra_root_fields=[k for k in strict if k not in author],legacy_report_root_fields=list(old),all_36_common_numeric_fields_equal=common,legacy_vs_strict_comparison_changes=changes,total_comparison_difference=1257,comparison_count_includes_self=True,minimum_gap_zero_is_forced_by_self_comparisons=True,current_source_SHA_matches_strict_metadata=True,current_statement_SHA_matches_strict_metadata=True,legacy_program_SHA_bound=False,legacy_original_entry_rerun=False,statement_repository_path=str(statement.relative_to(r))))
print({'maximal_cases':len(maxrows),'certificates':6,'certificate_histories':1608,'compression_lengths':len(comprows),'proper_subcatalogs':sum(x['proper_subcatalogs'] for x in comprows),'padding_changed_cases':changes})
