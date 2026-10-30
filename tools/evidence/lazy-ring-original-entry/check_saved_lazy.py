"""Direct saved-output check using only standard-library rational arithmetic."""
from pathlib import Path
from fractions import Fraction as Q
import json,sys
ROOT=Path.cwd();out=ROOT/'execution';data=json.loads((ROOT/'replay/examples/shared/tiny.json').read_text());res=json.loads((out/'lazy-tiny-cli.stdout.txt').read_text())
weights=list(map(Q,data['weights']));sites=list(map(set,data['locations']));N=len(sites)
def require(ok,msg):
    if not ok:raise ValueError(msg)
def check(s,t,rec):
    common=sorted(sites[s]&sites[t]);require(common==rec['common'],'common');p=list(map(Q,rec['prob_first']));require(len(p)==len(common),'prob length')
    require(all(0<=z<=1 for z in p),'range')
    a=sum((weights[i] for i in sites[s]-sites[t]),Q(0));b=sum((weights[i] for i in sites[t]-sites[s]),Q(0))
    x=a+sum((weights[i]*z for i,z in zip(common,p)),Q(0));y=b+sum((weights[i]*(1-z) for i,z in zip(common,p)),Q(0))
    require([x,y]==list(map(Q,rec['loads'])),'loads')
    for i,z in zip(common,p):
        cost1=weights[i]+a+sum((weights[j]*v for j,v in zip(common,p) if j!=i),Q(0))
        cost2=weights[i]+b+sum((weights[j]*(1-v) for j,v in zip(common,p) if j!=i),Q(0))
        require(z==0 or cost1<=cost2,'first conditional cost');require(z==1 or cost2<=cost1,'second conditional cost')
    return x,y
s,t=res['layout'];on=check(s,t,res['on_path']);profiles={(s,t):res['on_path']};observed=set();alpha=Q(res['alpha'])
for rec in res['deviation_certificate']:
    who,dest,opp=rec['deviator'],rec['destination'],rec['opponent'];require(type(who)is int and who in(0,1),'deviator')
    current=(s,t)[who];require(opp==(t,s)[who] and dest!=current and 0<=dest<N,'legal deviation');key=who,dest,opp;require(key not in observed,'duplicate');observed.add(key)
    x,y=check(dest,opp,rec);require(x<=alpha*on[who],'factor')
    if who==0:profiles[dest,opp]=rec
    else:profiles[opp,dest]={'common':rec['common'],'prob_first':[1-Q(z) for z in rec['prob_first']],'loads':[y,x]}
expected={(0,d,t) for d in range(N) if d!=s}|{(1,d,s) for d in range(N) if d!=t};require(observed==expected,'complete actual deviations')
def greedy(s,t):
    common=sorted(sites[s]&sites[t]);a=sum((weights[i] for i in sites[s]-sites[t]),Q(0));b=sum((weights[i] for i in sites[t]-sites[s]),Q(0));p={}
    for i in sorted(common,key=lambda i:(-weights[i],i)):
        if a<=b:p[i]=Q(1);a+=weights[i]
        else:p[i]=Q(0);b+=weights[i]
    return {'common':common,'prob_first':[p[i] for i in common],'loads':[a,b]}
defaults=0
for i in range(N):
    for j in range(N):
        rec=profiles.get((i,j))
        if rec is None:rec=greedy(i,j);defaults+=1
        check(i,j,rec)
frozen=json.loads(Path(sys.argv[1]).read_text());current=dict(res);elapsed_current=current.pop('elapsed_seconds');elapsed_frozen=frozen.pop('elapsed_seconds');require(current==frozen,'frozen comparison excluding elapsed_seconds')
report={'on_path_profiles':1,'actual_deviation_profiles':len(observed),'default_profiles_constructed_by_new_checker':defaults,'complete_ordered_layouts_checked':N*N,
'global_first_orientation':'second-facility deviations reflected explicitly','frozen_comparison':'all fields except elapsed_seconds identical','current_elapsed_seconds':elapsed_current,'frozen_elapsed_seconds':elapsed_frozen,
'output_does_not_include_default_rule_or_evaluator':True,'checker_imports_producer':False}
(out/'saved-output-check.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
