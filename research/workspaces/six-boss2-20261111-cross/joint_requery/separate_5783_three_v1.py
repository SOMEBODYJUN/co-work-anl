"""Only the three parent-requested active R structures, existing 616 cone.

This is pure reweighting of frozen legal features; no new query slots or family.
"""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib,time
import cross_query_pairs_v1 as cone
from separate_master import blocks_from_columns,div

HERE=Path(__file__).resolve().parent
STRUCTURES=((3,(0,0)),(2,(0,0)),(2,(1,0)))


def main():
    start=time.monotonic();source=HERE.parent/'master_cuts/dynamic_5783_exact.json';raw=source.read_bytes()
    sha=hashlib.sha256(raw).hexdigest();assert sha=='525139e949098e14426d483a334b7ad7acb454ff692f76ee19769dd305c227df'
    data=json.loads(raw);columns=data['columns'];blocks=blocks_from_columns(columns)
    actual=[sum(F(b['column']['weight'])*div(b['a'][i],sum(b['a'])) for b in blocks) for i in range(6)];u=actual[5];K=F(columns[0]['weight'])
    out={'scope':'Pure reweighting of the already established 616 feature cone at exactly three previously active R/source/orbit structures. No new legal-query family.','source_path':str(source),'source_sha256':sha,'columns':len(columns),'feature_count':len(cone.NAMES),'feature_names':cone.NAMES,'query_menu':cone.QUERY_MENU,'actual_utilities':list(map(str,actual)),'K':str(K),'scans':[],'cuts':[]}
    target=HERE/'cross_pairs_selected_5783_three_v1.json'
    for i,orb in STRUCTURES:
        k=6-i;visible=cone.visible_distribution(blocks,0,orb,i);res=cone.solve(visible,u,K,k,4)
        scan={'i':i,'k':k,'member':0,'orb':orb,'visible_states':len(visible),'hidden_per_state':len(cone.hidden_configs(k)),'success':bool(res.success),'message':res.message}
        if res.success:scan.update({'minimum_r_float':res.fun,'gap_float':res.fun-float(actual[i])})
        out['scans'].append(scan)
        if res.success and res.fun>float(actual[i])+1e-9:
            for den in (1000,10000,100000,1000000,10000000):
                theta=cone.weights_from_dual(res,den);assert theta is not None
                row,au,aK,psi=cone.make_row(columns,blocks,0,orb,i,theta)
                slack=sum(F(c['weight'])*value for c,value in zip(columns,row))
                if slack>=0:continue
                # Avoid discarding most of a discovered separator's margin
                # through coarse rational rounding. This changes no features.
                if -float(slack)<0.99*scan['gap_float'] and den<10000000:continue
                assert slack==actual[i]+au*u+aK*K-sum(mass*psi(p,ell,t,qs,mu) for p,ell,t,qs,mu,mass in visible)
                assert max(j for j,value in enumerate(row) if value)<1905
                cut={'i':i,'k':k,'member':0,'orb':orb,'pure_reweighting_of_existing_616':True,'weights':{name:str(w) for name,w in theta.items()},'source_weight_sum':'1','u6_coefficient':str(au),'K_coefficient':str(aK),'exact_slack':str(slack),'slack_float':float(slack),'denominator_limit':den,'sparse_row':[[j,str(value)] for j,value in enumerate(row) if value],'row_sha256':hashlib.sha256(json.dumps(list(map(str,row)),separators=(',',':')).encode()).hexdigest(),'visible':[{'state':[p,ell,t,list(map(str,qs)),list(map(str,mu))],'mass':str(mass),'minimum':str(psi(p,ell,t,qs,mu))} for p,ell,t,qs,mu,mass in visible]}
                out['cuts'].append(cut);print(json.dumps({'i':i,'orb':orb,'gap_float':scan['gap_float'],'exact_slack_float':float(slack),'weights':len(theta)}),flush=True);break
        out['elapsed_seconds']=time.monotonic()-start;target.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    out['cut_count']=len(out['cuts']);out['elapsed_seconds']=time.monotonic()-start;target.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'complete':True,'cuts':len(out['cuts']),'source_sha256':sha,'pack_sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'elapsed':out['elapsed_seconds']},ensure_ascii=False))


if __name__=='__main__':main()
