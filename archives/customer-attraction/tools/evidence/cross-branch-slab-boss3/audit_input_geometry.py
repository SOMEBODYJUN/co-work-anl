"""Exact input support/count audit only; do not import the old builder or solve LP."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
from math import comb
import json,hashlib,sys


def partition(values):
    labels={};out=[]
    for x in values:
        if x not in labels:labels[x]=len(labels)
        out.append(labels[x])
    return tuple(out)


def main():
    if len(sys.argv)!=3:raise SystemExit('usage: audit_input_geometry.py FROZEN_5277_JSON NEW_OUTPUT_JSON')
    source=Path(sys.argv[1]);target=Path(sys.argv[2]);point=json.loads(source.read_text());cols=point['columns'];byhist={};hi=None;bc={}
    assert hashlib.sha256(source.read_bytes()).hexdigest()=='303291e7ec19437d226bb8d33d3e689beaf54f52103fde53a12e28f1058f806a'
    for j,c in enumerate(cols):
        assert F(c['weight'])>=0
        if c['kind']=='hist':hi=j;byhist[hi]={}
        elif c['kind']=='joint-reply':
            f,d,wi,wj=c['group'];g=(f,d,tuple(wi),tuple(wj));st=tuple(c['state']);assert st not in byhist[hi].setdefault(g,{})
            byhist[hi][g][st]=j
        elif c['kind']=='actual-B-branch-state':bc[c['hist_column'],c['Q'],c['R'],c['ell']]=j
    states=list(product(range(2),range(2),(0,6)));histograms=[];S=A=B=O=0
    for hi,gs in byhist.items():
        mass=F(cols[hi]['weight']);assert all((hi,*st) in bc for st in states)
        assert all(set(v)=={(0,1),(1,0),(1,1)} for v in gs.values())
        if not mass:continue
        rm={g:F(cols[st[1,0]]['weight'])+F(cols[st[1,1]]['weight']) for g,st in gs.items()}
        assert all(0<=r<=mass for r in rm.values());cuts=sorted({F(),mass,*rm.values()});slabs=[]
        for lo,up in zip(cuts,cuts[1:]):
            width=up-lo;assert width>0;bits={g:int(up<=r) for g,r in rm.items()}
            slabs.append({'left':str(lo),'right':str(up),'mass':str(width),'groups':len(gs),'R_bits':[[g[0],g[1],list(g[2]),list(g[3]),v] for g,v in bits.items()]})
            S+=1;A+=8;B+=8*len(gs);O+=8*comb(len(gs),2)
        for g,r in rm.items():assert sum((F(s['mass'])*int(F(s['right'])<=r) for s in slabs),F())==r
        histograms.append({'hist_column':hi,'actual_bits':cols[hi]['actual_bits'],'d':cols[hi]['d'],'hist':cols[hi]['hist'],'mass':str(mass),'group_count':len(gs),'slabs':slabs})
    bell4=len({partition(v) for v in product(range(4),repeat=4)});PN=3*4*bell4;CN=8*3;BN=2*3*12
    rows=point['verified_rows']+PN+CN+BN+B+2*S+2*O
    result={'scope':'Exact geometry and loop-count reconstruction on a frozen input only; no 41649-row builder, floating solver, Farkas or SPE check.','source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'source_W':point['W'],'base_rows_from_prior_complete_matrix_replay':point['verified_rows'],'hist_count':len(byhist),'positive_hist_count':len(histograms),'slabs':S,'sectors':A,'alpha_variables':A,'beta_variables':B,'core_variables':A+B,'overlap_variables':O,'total_variables':A+B+O,'bell4':bell4,'new_terminal_rows':PN,'cross_quote_rows':CN,'B_branch_pair_rows':BN,'beta_upper_rows':B,'slab_equality_as_signed_rows':2*S,'overlap_upper_rows':2*O,'total_rows':rows,'ablation_rows':{'no-new-cross':rows-CN-BN,'quotes-only':rows-BN,'branch-pairs-only':rows-CN},'all_R_marginals_exactly_recovered_by_threshold':True,'histograms':histograms,'original_module_imports':0,'original_build_calls':0,'linprog_calls':0,'SPE_solver_calls':0}
    assert (S,A,B,A+B,O,A+B+O,rows)==(24,192,2416,2608,16816,19424,41649)
    with target.open('x') as f:json.dump(result,f,ensure_ascii=False,indent=2);f.write('\n')
    print(json.dumps({k:v for k,v in result.items() if k!='histograms'},ensure_ascii=False,indent=2))


if __name__=='__main__':main()
