from static_comparison_probe import *

def probe(m,p,r):
    ins=Instance(tuple(map(str,range(p))),tuple(CustomerType(frozenset(a for a in range(p) if mask>>a&1),v) for mask,v in enumerate(r,1) if v),m)
    sol=ExactSPESolver(ins);opt=ins.optimal_welfare()
    for q in sol.outcomes():
        w=ins.welfare(q);pay=ins.topic_payoffs(q);umin=min(pay[a] for a in range(p) if q[a])
        if m*umin<opt-w:
            return {'m':m,'p':p,'types':r,'q':q,'min_pay':str(umin),'opt':opt,'w':w,'factor':str(F(opt-w)/umin),'certificate':sol.certificate(q).to_dict()}
    return None
if __name__=='__main__':
    rng=Random(8712266)
    for m,p,rounds in [(3,4,20000),(4,5,10000),(5,7,1000)]:
        for i in range(rounds):
            r=[rng.choice([0,0,0,1,2,3,5,8]) for _ in range(2**p-1)]
            x=probe(m,p,r)
            if x:
                Path(__file__).with_name('gap_floor_counterexample.json').write_text(json.dumps(x,indent=2));print(json.dumps({k:v for k,v in x.items() if k!='certificate'}));sys.exit()
        print('completed',m,p,rounds,flush=True)
