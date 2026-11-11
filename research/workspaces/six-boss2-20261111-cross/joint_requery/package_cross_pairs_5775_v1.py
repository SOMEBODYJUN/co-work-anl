"""Freeze exact 616 cuts, fair comparison, and the visible disagreement identity."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import hashlib,json
import cross_query_pairs_v1 as new
import portfolio_master as old
from separate_master import blocks_from_columns

HERE=Path(__file__).resolve().parent


def write(name,data):
    path=HERE/name;path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    return {'path':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}


def main():
    discovered=json.loads((HERE/'cross_pairs_5775_v1_separation.json').read_text())
    previous=json.loads((HERE/'portfolio_5775_separation.json').read_text())
    assert len(discovered['scans'])==len(previous['scans'])==24
    assert discovered['source_sha256']==previous['source_sha256']=='81983304076358d591cbdac2e6bf7a4b697fc2854aad40918e8cf8cf2d99dd02'
    raw=Path(discovered['source_path']).read_bytes();assert hashlib.sha256(raw).hexdigest()==discovered['source_sha256']
    columns=json.loads(raw)['columns'];blocks=blocks_from_columns(columns)
    package={k:discovered[k] for k in ('scope','source_path','source_sha256','columns','query_menu','feature_count','feature_names','extra_pair_configurations','actual_utilities','K')}
    seen=set();package['cuts']=[]
    for cut in discovered['cuts']:
        if cut['row_sha256'] in seen:continue
        seen.add(cut['row_sha256']);assert F(cut['exact_slack'])<0
        row=[F(0)]*len(columns)
        for ci,value in cut['sparse_row']:row[ci]=F(value)
        assert max(i for i,value in enumerate(row) if value)<1905
        assert sum(F(c['weight'])*value for c,value in zip(columns,row))==F(cut['exact_slack'])
        assert hashlib.sha256(json.dumps(list(map(str,row)),separators=(',',':')).encode()).hexdigest()==cut['row_sha256']
        package['cuts'].append(cut)
    package['cut_count']=len(package['cuts']);assert package['cut_count']==8
    pfile=write('cross_pairs_selected_5775_v1.json',package)
    oldpackage={k:previous[k] for k in ('scope','query_menu','source_path','source_sha256','columns','actual_utilities','K','feature_count','feature_names','cuts')}
    oldpackage['cut_count']=len(oldpackage['cuts']);oldfile=write('portfolio_selected_5775_v1.json',oldpackage)
    oldscans={(x['i'],x['member'],tuple(x['orb'])):x for x in previous['scans']}
    cuts={(x['i'],x['member'],tuple(x['orb'])):x for x in package['cuts']}
    fair=[]
    for scan in discovered['scans']:
        key=(scan['i'],scan['member'],tuple(scan['orb']));s=oldscans[key]
        assert s['success'] and scan['success']
        fair.append({'i':key[0],'member':key[1],'orb':key[2],'old_332_gap_float':s['gap_float'],'new_616_gap_float':scan['gap_float'],'discovered_min_r_improvement_float':scan['gap_float']-s['gap_float'],'new_exact_negative_slack':cuts.get(key,{}).get('exact_slack')})
    fairfile=write('cross_query_comparison_5775_v1.json',{'scope':'Same actual source/orbit/menu and source budget; 24 old332/new616 LP pairs. Numerical optimization is for comparison only; exact negative cuts and one exact old lift are separately saved.','source_sha256':package['source_sha256'],'comparisons':fair,'new_cut_pack':pfile,'old_cut_pack':oldfile})
    strict=json.loads((HERE/'exact_332_lift_cross_strictness_5775_v1.json').read_text())
    theta={name:F(value) for name,value in strict['cross_cut']['normalized_weights'].items()}
    oldtheta=dict(theta);weight=oldtheta.pop('oldpair1:6,10:product')
    assert weight==F(48,413)
    for qi in (6,10):oldtheta[f'pair1:q{qi},q{qi}']=weight/2
    row,au,aK,psi=new.make_row(columns,blocks,0,(0,0),3,theta)
    oldrow,oldau,oldaK,oldpsi=old.make_row(columns,blocks,0,(0,0),3,oldtheta)
    assert (au,aK)==(oldau,oldaK)==(F(164,413),F(14,413))
    table=[]
    for p in range(4):
        for ell in range(p,p+3):
            a=tuple(int(j<p) for j in range(3))+tuple(int(j<ell-p) for j in range(2))+(0,)
            for t,ti,ci,bj in product((0,1),repeat=4):
                words=((ti,0,ci),(0,bj,0))+((0,0,0),)*4
                qs,mu=new.queries_and_moments(a,words,0,1,t,0)
                newmin=psi(p,ell,t,qs,mu);oldmin=oldpsi(p,ell,t,qs)
                premium=F(24*abs(ti-bj),413*(p+t+1)*(p+t+2))
                assert newmin==oldmin+premium
                table.append({'state':[p,ell,t,ti,ci,bj],'new_min_integer_scale':str(413*newmin),'old_min_integer_scale':str(413*oldmin),'disagreement_increment_integer_scale':str(413*premium)})
    assert len(table)==192
    fullvis=new.visible_distribution(blocks,0,(0,0),3)
    premium=sum(w*F(24,413)*abs(qs[6]-qs[10])/((p+t+1)*(p+t+2)) for p,ell,t,qs,mu,w in fullvis)
    newslack=sum(F(c['weight'])*value for c,value in zip(columns,row));oldslack=sum(F(c['weight'])*value for c,value in zip(columns,oldrow))
    assert oldslack-newslack==premium and oldslack>=0 and newslack<0
    identity={'scope':'Exact hidden-independent disagreement increment for the 12-weight k=3 first-branch cross-query cut, and all 192 actual fourth-source visible parameter types.','source_sha256':package['source_sha256'],'integer_budget':{'source':413,'u6':164,'K':14},'integer_cross_weights':strict['cross_cut']['integer_weights'],'old_332_replacement_weights':{n:str(w*413) for n,w in oldtheta.items()},'new_normalized_slack':str(newslack),'old_replacement_normalized_slack':str(oldslack),'normalized_disagreement_premium':str(premium),'new_normalized_slack_float':float(newslack),'old_replacement_normalized_slack_float':float(oldslack),'normalized_disagreement_premium_float':float(premium),'min_table':table}
    identityfile=write('cross_query_disagreement_identity_5775_v1.json',identity)
    print(json.dumps({'cut_pack':pfile,'old_pack':oldfile,'comparison':fairfile,'identity':identityfile,'new_slack':float(newslack),'old_replacement_slack':float(oldslack),'disagreement_premium':float(premium)},ensure_ascii=False,indent=2))


if __name__=='__main__':main()
