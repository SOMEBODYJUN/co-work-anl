import json, importlib.util
spec=importlib.util.spec_from_file_location('prd','padded_residual_dag.py')
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
d=json.load(open('padded_residual_m6_dag.json')); inst=m.instance(6); s=m.ExactSPESolver(inst); s.outcomes(); nodes=d['nodes']; checked=0
for idx,node in enumerate(nodes):
    k=tuple(node['counts']); c=tuple(node['target'])
    if sum(k)==6:
        assert k==c
        continue
    a=node['action']; child=k[:a]+(k[a]+1,)+k[a+1:]
    assert c in s.outcomes(child)
    assert inst.topic_payoff(a,c)>=s.threshold(k)
    for b,ci in enumerate(node['children']):
        child2=k[:b]+(k[b]+1,)+k[b+1:]
        dnode=nodes[ci]
        assert tuple(dnode['counts'])==child2
        assert tuple(dnode['target']) in s.outcomes(child2)
    checked+=1
print({'nodes':len(nodes),'nonterminal_checked':checked,'status':'PASS'})
