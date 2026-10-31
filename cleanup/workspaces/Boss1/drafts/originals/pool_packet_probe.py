"""Pooled-load attack on one pre-existing complete acyclic SPE automaton."""
import sys,json
from pathlib import Path
import numpy as np
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'parent'))
from full_terminal_packet_probe import load_packet,ROOT
from pool_probe import probe

source=ROOT/'research/workspaces/customer-attraction/R-c50fecc37aa44fb4a69a2122bb70e5fe/security/refined_tax_k10_packet.json.gz'
data,G,tensor,c,seed=load_packet(source)
nodes=data['nodes'];k=len(data['instance']['topics']);n=data['instance']['players']
targets=[None]*len(nodes)
for j in sorted(range(len(nodes)),key=lambda j:-sum(nodes[j]['counts'])):
    node=nodes[j]
    targets[j]=targets[node['children'][node['action']]] if 'action' in node else np.array(node['counts'])
mem=np.array([[(mask>>a)&1 for mask in range(1,1<<k)] for a in range(k)])
H=np.zeros((k,len(c)));j=data['root'];path=[]
while 'action' in nodes[j]:
    node=nodes[j];path.append(node['action'])
    for a,child in enumerate(node['children']):H[a]+=(targets[child]@mem-mem[a])/n
    j=node['children'][node['action']]
assert len(path)==n
result=probe(G,c,mem,H,n,17120261021,starts=30)
result.update(status='finite numerical discovery only',source=str(source.relative_to(ROOT)),gamma_rows=len(G),nodes=len(nodes),n=n,k=k,on_path=path)
(HERE/'pool_packet_report.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
