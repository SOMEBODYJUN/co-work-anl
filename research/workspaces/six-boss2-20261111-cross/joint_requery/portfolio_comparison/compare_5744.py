"""Fair same-point comparison: 17 separate full single-Q cones vs joint 332."""
from pathlib import Path
from fractions import Fraction as F
from collections import defaultdict
import sys,json,hashlib,time

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent))
import portfolio_master as portfolio
from explore_projection import solve,ALL_NAMES
from separate_master import blocks_from_columns


def single_visible(joint_visible,query_index):
    ans=defaultdict(F)
    for p,ell,t,qvec,mass in joint_visible:ans[p,ell,t,qvec[query_index]]+=mass
    return [(*key,w) for key,w in sorted(ans.items()) if w]


def main():
    start=time.monotonic();package=json.loads((HERE.parent/'portfolio_selected_5744.json').read_text())
    source=Path(package['source_path']);raw=source.read_bytes();assert hashlib.sha256(raw).hexdigest()==package['source_sha256']
    blocks=blocks_from_columns(json.loads(raw)['columns']);actual=list(map(F,package['actual_utilities']));K=F(package['K']);u=actual[5]
    original=json.loads((HERE.parent/'portfolio_5744_separation.json').read_text())
    joint_scans={(s['i'],s['member'],tuple(s['orb'])):s for s in original['scans']}
    out={'scope':'Same 5744 point, same 17 query menu and budgets; 136 complete single-Q 76-row LP comparisons. Floats are diagnostic until separately recovered.','source_path':str(source),'source_sha256':package['source_sha256'],'query_menu':package['query_menu'],'structures':[]}
    for cut in package['cuts']:
        i,member,orb=cut['i'],cut['member'],tuple(cut['orb']);k=6-i;r=actual[i]
        joint_visible=portfolio.visible_distribution(blocks,member,orb,i)
        record={'i':i,'k':k,'member':member,'orb':orb,'r_actual':str(r),'joint_required_r_float':joint_scans[i,member,orb]['minimum_r_float'],'joint_cut_slack_exact':cut['exact_slack'],'single_queries':[]}
        for qi in range(17):
            visible=single_visible(joint_visible,qi);res,_,_=solve(visible,u,K,ALL_NAMES,k)
            row={'query':qi,'label':package['query_menu'][qi],'success':bool(res.success),'visible_states':len(visible),'message':res.message}
            if res.success:row.update({'required_r_float':res.fun,'gap_to_actual_float':res.fun-float(r)})
            record['single_queries'].append(row)
        best=max((z for z in record['single_queries'] if z['success']),key=lambda z:z['required_r_float'])
        record['best_single_query']=best['query'];record['best_single_required_r_float']=best['required_r_float'];record['best_single_gap_to_actual_float']=best['gap_to_actual_float'];record['joint_gain_over_best_single_float']=record['joint_required_r_float']-best['required_r_float'];record['all_single_feasible_at_actual_float']=len([z for z in record['single_queries'] if z['success']])==17 and best['gap_to_actual_float']<=1e-9
        out['structures'].append(record);out['elapsed_seconds']=time.monotonic()-start;(HERE/'comparison_5744.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
        print(json.dumps({key:record[key] for key in ('i','member','orb','best_single_query','best_single_gap_to_actual_float','joint_gain_over_best_single_float','all_single_feasible_at_actual_float')}),flush=True)
    print('done',out['elapsed_seconds'])


if __name__=='__main__':main()
