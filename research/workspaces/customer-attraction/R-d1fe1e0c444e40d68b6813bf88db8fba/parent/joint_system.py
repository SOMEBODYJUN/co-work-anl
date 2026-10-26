from strong_pair_projection import *
BASE=Path(__file__).parents[1]
sys.path.insert(0,str(BASE/'query_closure'))
sys.path.insert(0,str(BASE/'general_payment'))
from same_menu_reply import from_weights,separate as separate_menu
from free_joint import make_row,rawcut

def build():
    types,rows,diags=system()
    for filename in ('exact_cuts.json','exact_cuts_threecopy.json'):
        for idx,c in enumerate(json.loads((BASE/'six_maxroot'/filename).read_text())):
            B,C=F(c['B']),F(c['C'])
            rows.append(('maxroot:'+filename+':'+str(idx),[B*sh(a[0],sum(a))-int(d>0) for a,d in types]+[C]))
    pair=json.loads((BASE/'parent/strong_pair_projection.json').read_text())
    for cut in pair['cuts']:
        rows.append(row(types,{k:v for k,v in cut.items() if k!='separation_slack'}))
    menus=json.loads((BASE/'query_closure/iterate_same_menu.json').read_text())
    for idx,c in enumerate(menus['cuts']):rows.append(('same-menu-initial:'+str(idx),from_weights(c['weights'])))
    joint=json.loads((BASE/'general_payment/compact_cuts.json').read_text())
    for cut in joint['cuts']:rows.append(make_row(types,6,rawcut(cut)))
    rows.append(('existing-root-saturation',[F(150)*sh(a[0],sum(a))-int(d>0) for a,d in types]+[-F(139,6)]))
    return types,rows


def verify_primal(result,types,rows):
    n=decode(result,types)
    assert min(n)>=0
    assert sum(int(d>0)*v for (a,d),v in zip(types,n[:-1]))==1
    assert sum(int(any(a))*v for (a,d),v in zip(types,n[:-1]))==F(result['W'])
    for name,coeff in rows:assert sum(x*y for x,y in zip(coeff,n))>=0,name
    return n

def solve_primal(types,rows):
    from six_stress import exact_solve
    o=[int(d>0) for a,d in types]+[0];w=[int(any(a)) for a,d in types]+[0]
    mat=np.array([[float(v) for v in rr] for _,rr in rows])
    sol=linprog(w,A_ub=-mat,b_ub=np.zeros(len(rows)),A_eq=[o],b_eq=[1],bounds=(0,None),method='highs')
    assert sol.success,sol.message
    support=[j for j,x in enumerate(sol.x) if x>1e-8]
    eqs=[[rr[j] for j in support]+[F(0)] for (name,rr),fl in zip(rows,mat) if abs(np.dot(fl,sol.x))<1e-8]
    eqs += [[F(o[j]) for j in support]+[F(1)]]
    vals=exact_solve(eqs,len(support));n=[F(0)]*len(sol.x)
    for j,v in zip(support,vals):n[j]=v
    value=sum(F(w[j])*v for j,v in enumerate(n))
    result={'m':6,'scope':'exact feasible necessary-system point; no exact optimum assertion','n_types':len(types),'n_rows':len(rows),'O':'1','W':str(value),'K':str(n[-1]),'support':[{'actual_bits':''.join(map(str,a)),'d':d,'weight':str(n[j])} for j,(a,d) in enumerate(types) if n[j]]}
    verify_primal(result,types,rows)
    return result,n

if __name__=='__main__':
    target=Path(__file__).with_suffix('.json')
    types,rows=build()
    if '--verify' in sys.argv:
        data=json.loads(target.read_text())
        for idx,c in enumerate(data['menu_cuts']):rows.append(('same-menu-joint:'+str(idx),from_weights(c['weights'])))
        for cut in data['pair_cuts']:rows.append(row(types,{k:v for k,v in cut.items() if k!='separation_slack'}))
        verify_primal(data['certificate'],types,rows);print('EXACT VERIFIED JOINT',data['certificate']['W'],len(rows))
    else:
        result,n=solve_primal(types,rows)
        menu_cuts=[];pair_cuts=[];records=[]
        if '--resume' in sys.argv:
            old=json.loads(target.read_text())
            menu_cuts=old['menu_cuts'];pair_cuts=old['pair_cuts'];records=old['records']
            for idx,c in enumerate(menu_cuts):rows.append(('same-menu-joint:'+str(idx),from_weights(c['weights'])))
            for cut in pair_cuts:rows.append(row(types,{k:v for k,v in cut.items() if k!='separation_slack'}))
            result,n=solve_primal(types,rows)
        for step in range(30):
            print('JOINT STEP',step,'W',result['W'],'rows',len(rows),flush=True)
            target.write_text(json.dumps({'scope':'necessary conditions only, not SPE nor half proof','menu_cuts':menu_cuts,'pair_cuts':pair_cuts,'records':records,'certificate':result},indent=2)+'\n')
            mc,mr=separate_menu(n,True)
            pc,pr=separate(types,n)
            records.append({'W':result['W'],'menu_slack':mc['exact_cut_slack'],'pair_cuts':len(pc)})
            if F(mc['exact_cut_slack'])<0:
                rows.append(('same-menu-joint:'+str(len(menu_cuts)),mr));menu_cuts.append(mc)
            if pc:
                for c in pc:rows.append(row(types,{k:v for k,v in c.items() if k!='separation_slack'}))
                pair_cuts.extend(pc)
            if F(mc['exact_cut_slack'])>=0 and not pc:break
            result,n=solve_primal(types,rows)
        target.write_text(json.dumps({'scope':'necessary conditions only, not SPE nor half proof','menu_cuts':menu_cuts,'pair_cuts':pair_cuts,'records':records,'certificate':result},indent=2)+'\n')
