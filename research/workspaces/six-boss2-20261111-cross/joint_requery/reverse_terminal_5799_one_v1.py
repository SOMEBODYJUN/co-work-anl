"""Same one-structure 616/624 comparison, freshly bound to the 5799 point."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib,time
import reverse_terminal_624_v1 as cone
from separate_master import blocks_from_columns,div

HERE=Path(__file__).resolve().parent


def exact_cut(res,columns,blocks,visible,actual,K):
    gap=res.fun-float(actual[3])
    if gap<=1e-9:return None
    for grid in (10**5,10**6,10**7,10**8,10**9):
        theta,den=cone.rational_weights(res,grid)
        row,au,aK,psi=cone.make_row(columns,blocks,0,(0,0),3,theta)
        slack=sum(F(c['weight'])*value for c,value in zip(columns,row))
        if slack>=0 or -float(slack)<0.99*gap:continue
        assert slack==actual[3]+au*actual[5]+aK*K-sum(mass*psi(p,ell,t,qs,mu) for p,ell,t,qs,mu,mass in visible)
        return {'i':3,'k':3,'member':0,'orb':[0,0],'weights':{name:str(w) for name,w in theta.items()},'new_reverse_weights':{name:str(theta[name]) for name in cone.REVERSE_NAMES if name in theta},'source_weight_sum':'1','u6_coefficient':str(au),'K_coefficient':str(aK),'common_denominator':den,'rounding_grid':grid,'exact_slack':str(slack),'slack_float':float(slack),'sparse_row':[[ci,str(value)] for ci,value in enumerate(row) if value],'row_sha256':hashlib.sha256(json.dumps(list(map(str,row)),separators=(',',':')).encode()).hexdigest(),'visible':[{'state':[p,ell,t,list(map(str,qs)),list(map(str,mu))],'mass':str(mass),'minimum':str(psi(p,ell,t,qs,mu))} for p,ell,t,qs,mu,mass in visible]}
    raise ValueError('No rational direction preserved the discovered margin')


def main():
    start=time.monotonic();source=HERE.parent/'master_cuts/dynamic_5799_exact.json';raw=source.read_bytes();sha=hashlib.sha256(raw).hexdigest();assert sha=='63edbafd53493a20ec64ced5f09a694ead3f894bfb6419cde425de0b3a1710c1'
    data=json.loads(raw);columns=data['columns'];blocks=blocks_from_columns(columns)
    previous=json.loads((HERE/'reverse_terminal_5786_one_v1.json').read_text());oldpoint=json.loads(Path(previous['source_path']).read_text())
    assert [{k:v for k,v in c.items() if k!='weight'} for c in columns]==[{k:v for k,v in c.items() if k!='weight'} for c in oldpoint['columns']]
    actual=[sum(F(b['column']['weight'])*div(b['a'][i],sum(b['a'])) for b in blocks) for i in range(6)];K=F(columns[0]['weight']);visible=cone.base.visible_distribution(blocks,0,(0,0),3)
    old=cone.base.solve(visible,actual[5],K,3,4);new=cone.solve(visible,actual[5],K,3,(0,0))
    out={'scope':'Fresh5799 actual4/R/orb00 fair616/624 comparison. Eight original R/Z terminal queries only; no strictness claim from positive new weights alone.','source_path':str(source),'source_sha256':sha,'columns':len(columns),'i':3,'k':3,'member':0,'orb':[0,0],'feature_count':624,'feature_names':cone.NAMES,'query_menu':cone.base.QUERY_MENU,'actual_utilities':list(map(str,actual)),'K':str(K),'old616':{'success':bool(old.success),'message':old.message},'new624':{'success':bool(new.success),'message':new.message},'old616_cut':None,'cuts':[]}
    if old.success:
        out['old616'].update({'minimum_r_float':old.fun,'gap_float':old.fun-float(actual[3])});out['old616_cut']=exact_cut(old,columns,blocks,visible,actual,K)
    if new.success:
        out['new624'].update({'minimum_r_float':new.fun,'gap_float':new.fun-float(actual[3])});cut=exact_cut(new,columns,blocks,visible,actual,K)
        if cut:out['cuts'].append(cut)
    saved=previous['cuts'][0];fixed=[F(0)]*len(columns)
    for ci,value in saved['sparse_row']:fixed[ci]=F(value)
    value=sum(F(c['weight'])*w for c,w in zip(columns,fixed))
    out['previous_5786_row_on_this_point']={'row_sha256':saved['row_sha256'],'exact_slack':str(value),'slack_float':float(value)}
    out['elapsed_seconds']=time.monotonic()-start;target=HERE/'reverse_terminal_5799_one_v1.json';target.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'old616':out['old616'],'new624':out['new624'],'old_exact_negative':out['old616_cut']['slack_float'] if out['old616_cut'] else None,'new_exact_negative':out['cuts'][0]['slack_float'] if out['cuts'] else None,'new_reverse_weights':out['cuts'][0]['new_reverse_weights'] if out['cuts'] else {},'sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'elapsed':out['elapsed_seconds']},ensure_ascii=False))


if __name__=='__main__':main()
