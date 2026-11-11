"""Exact symbolic 30-pair aggregation audit; no LP or parameter search."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
from collections import Counter,defaultdict
import json,hashlib
from separate_master import blocks_from_columns,div

HERE=Path(__file__).resolve().parent


def main():
    strict=json.loads((HERE/'exact_332_lift_cross_strictness_5775_v1.json').read_text())
    raw=Path(strict['source_path']).read_bytes();assert hashlib.sha256(raw).hexdigest()==strict['source_sha256']
    data=json.loads(raw);blocks=blocks_from_columns(data['columns'])
    identity=json.loads((HERE/'cross_query_disagreement_identity_5775_v1.json').read_text())
    G={tuple(r['state']):F(r['old_min_integer_scale']) for r in identity['min_table']}
    old_total=F(0);new_credit=F(0);count_lower=F(0);T_only_lower=F(0);reports=[]
    g=(0,5,10,12,10,5,0)
    for block in blocks:
        words=block['words'];n=Counter(words);a=block['a'];p,ell=sum(a[:3]),sum(a[:5]);mass=F(block['column']['weight'])
        nT=sum(w[0] for w in words);nB=sum(w[1] for w in words);nTB=sum(w[0]*w[1] for w in words)
        Ntc=Counter((w[0],w[2]) for w in words);Mb=Counter(w[1] for w in words)
        m={(al,ga,be):Ntc[al,ga]*Mb[be]-n[al,be,ga] for al,ga,be in product((0,1),repeat=3)}
        literal=Counter((words[i][0],words[i][2],words[j][1]) for i in range(6) for j in range(6) if i!=j)
        assert dict(m)=={key:literal[key] for key in m} and sum(m.values())==30
        rtypes=defaultdict(F)
        for _,column in block['joint']:
            family,diag,wl,wr=column['group']
            if (family,diag)==(0,0) and column['state'][0]:rtypes[tuple(wl),tuple(wr)]+=F(column['weight'])
        H=defaultdict(F);direct_credit=F(0)
        for i in range(6):
            for j in range(6):
                if i==j:continue
                wl,wr=words[i],words[j];rmass=rtypes[wl,wr];assert 0<=rmass<=mass
                H[wl[0],wl[2],wr[1]]+=rmass
                disagreement=abs(wl[0]-wr[1])
                direct_credit+=F(24,30)*disagreement*((mass-rmass)/((p+1)*(p+2))+rmass/((p+2)*(p+3)))
        assert all(0<=H[key]<=mass*m[key] for key in m)
        D=5*(nT+nB)-2*nT*nB+2*nTB
        assert D==sum(m[key]*abs(key[0]-key[2]) for key in m)
        DR=sum(H[key]*abs(key[0]-key[2]) for key in m)
        closed_credit=F(4,5)*((p+3)*mass*D-2*DR)/((p+1)*(p+2)*(p+3))
        lower=F(4,5)*mass*D/((p+2)*(p+3));tonly=F(4,5)*mass*g[nT]/((p+2)*(p+3))
        assert closed_credit==direct_credit and closed_credit>=lower>=tonly>=0
        folded_old=sum((mass*m[key]*G[p,ell,0,*key]+H[key]*(G[p,ell,1,*key]-G[p,ell,0,*key]))/30 for key in m)
        old_total+=folded_old;new_credit+=closed_credit;count_lower+=lower;T_only_lower+=tonly
        reports.append({'hist_column':block['ci'],'p':p,'ell':ell,'N_T':nT,'N_B':nB,'N_TB':nTB,'D':D,'D_R_mass':str(DR),'mass':str(mass),'eight_pair_type_counts':[{'t_i':key[0],'c_i':key[1],'b_j':key[2],'count':m[key],'R_mass':str(H[key])} for key in m],'old_min_total_integer_scale':str(folded_old),'exact_disagreement_credit_integer_scale':str(closed_credit),'R_free_lower_integer_scale':str(lower),'T_count_only_lower_integer_scale':str(tonly)})
    assert new_credit/413==F(identity['normalized_disagreement_premium'])
    actual=list(map(F,strict['actual_utilities']));K=F(strict['K']);budget=413*actual[3]+164*actual[5]+14*K
    assert (budget-old_total-new_credit)/413==F(strict['cross_cut']['exact_slack'])
    assert (budget-old_total)/413==F(identity['old_replacement_normalized_slack'])
    # Exact combinatorial minimum over B counts and feasible same-index overlap.
    minima=[]
    for nt in range(7):
        candidates=[(5*(nt+nb)-2*nt*nb+2*ov,nb,ov) for nb in range(7) for ov in range(max(0,nt+nb-6),min(nt,nb)+1)]
        value,nb,ov=min(candidates)
        assert value==g[nt]==min(5*nt,5*(6-nt),30-2*nt*(6-nt))
        minima.append({'N_T':nt,'minimum_D':value,'attaining_N_B':nb,'attaining_N_TB':ov})
    out={'status':'PASS','scope':'Symbolic aggregation of the 12-integer-weight first-branch disagreement credit across all30 ordered off-diagonal pairs. No new optimization or current-master separation is asserted.','source_path':strict['source_path'],'source_sha256':strict['source_sha256'],'histogram_count':len(blocks),'integer_budget':str(budget),'integer_old_min_total':str(old_total),'integer_exact_disagreement_credit':str(new_credit),'integer_R_free_lower':str(count_lower),'integer_T_count_only_lower':str(T_only_lower),'normalized_exact_disagreement_credit':str(new_credit/413),'normalized_exact_disagreement_credit_float':float(new_credit/413),'normalized_R_free_lower':str(count_lower/413),'normalized_R_free_lower_float':float(count_lower/413),'normalized_T_count_only_lower':str(T_only_lower/413),'normalized_T_count_only_lower_float':float(T_only_lower/413),'normalized_new_slack':str((budget-old_total-new_credit)/413),'normalized_R_free_weakened_slack':str((budget-old_total-count_lower)/413),'normalized_R_free_weakened_slack_float':float((budget-old_total-count_lower)/413),'optimal_count_lower_table':minima,'blocks':reports}
    target=HERE/'aggregate_30_disagreement_v1.json';target.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:out[k] for k in ('status','histogram_count','normalized_exact_disagreement_credit_float','normalized_R_free_lower_float','normalized_T_count_only_lower_float','normalized_R_free_weakened_slack_float')},ensure_ascii=False))


if __name__=='__main__':main()
