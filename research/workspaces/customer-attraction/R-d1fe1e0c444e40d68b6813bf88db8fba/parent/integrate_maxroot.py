from strong_pair_projection import *
if __name__=='__main__':
    types,rows,diags=system()
    cuts=json.loads((Path(__file__).parents[1]/'six_maxroot/exact_cuts.json').read_text())
    for c in cuts:
        B,C=F(c['B']),F(c['C'])
        rows.append(('maxroot:'+c['C'],[B*sh(a[0],sum(a))-int(d>0) for a,d in types]+[C]))
    path=Path(__file__).with_suffix('.json')
    if '--verify' in sys.argv:
        result=json.loads(path.read_text());verify(result,types,rows)
    else:
        result,n=solve_exact_system(6,types,rows)
        path.write_text(json.dumps(result,indent=2)+'\n')
    print('EXACT MAXROOT+587',result['W'],len(rows),'rows',float(F(result['W'])),flush=True)
