from catalogue_pruning_probe import *

def run_ordered():
    rng=Random(20261024)
    tested=0
    for m,t,attempts in [(2,3,300),(3,3,1000),(3,4,1000),(4,4,500)]:
        for z in range(attempts):
            customers=tuple(CustomerType(frozenset(a for a in range(t) if mask>>a&1),r)
                            for mask in range(1,1<<t) if (r:=rng.randrange(10)))
            inst=Instance(tuple(chr(65+a) for a in range(t)),customers,m)
            solver=ExactSPESolver(inst)
            cache={}
            for path in solver.ordered_outcomes():
                support=tuple(sorted(set(path)))
                if len(support)==t: continue
                if support not in cache:
                    small=restrict(inst,support)
                    paths=set(ExactSPESolver(small).ordered_outcomes())
                    cache[support]=(small,paths)
                small,paths=cache[support]
                target=tuple(support.index(a) for a in path)
                tested+=1
                if target not in paths:
                    cert=solver.certificate(on_path=path)
                    verify_certificate(inst,cert).assert_valid()
                    result={'tested':tested,'m':m,'t':t,'sample':z,'instance':inst.to_dict(),'path':path,
                            'support':support,'restricted':small.to_dict(),'restricted_paths':sorted(paths),
                            'certificate':cert.to_dict()}
                    (OUT/'ordered_pruning_failure.json').write_text(json.dumps(result,indent=2))
                    print(json.dumps({k:v for k,v in result.items() if k!='certificate'},indent=2))
                    return
    print('No failure among',tested,'sampled ordered outcomes')

if __name__=='__main__': run_ordered()
