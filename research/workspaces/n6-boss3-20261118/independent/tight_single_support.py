"""Build a sharp six-person single-on-path-coverage example and full strategy.
Action0 covers six core blocks of six unit clients each. Actionj covers core
blockj and five distinct private unit clients. The strategy is action0 at every
ordered history, including all off-path histories.
"""
import itertools,json
from pathlib import Path
base=Path(__file__).resolve().parent
A=7
weights=[0]*(1<<A)
for j in range(1,7):
    weights[1|(1<<j)]=6
    weights[1<<j]=5
obj={'players':6,'actions':A,'weights':weights,'root_terminal_counts':[6,0,0,0,0,0,0],'construction':'action0 covers six disjoint core blocks of six unit clients each; actionj covers coreblockj plus five private unit clients; constant action0 at every history'}
(base/'tight-single-support.json').write_text(json.dumps(obj,indent=2)+'\n')
with (base/'tight-single-support-strategy.csv').open('w') as f:
    f.write('history,action\n')
    for d in range(6):
        for h in itertools.product(range(A),repeat=d):
            f.write((''.join(map(str,h)) or '_')+',0\n')
print(json.dumps({'instance':'tight-single-support.json','strategy':'tight-single-support-strategy.csv','decision_nodes':sum(A**d for d in range(6)),'constant_action':0}))
