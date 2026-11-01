"""Minimize a genuine loss of SPE terminal realizability after omitted deletion.

This is a diagnostic for one proposed general reduction, never a half counterexample.
Run from the repository root with PYTHONPATH=. python <this file>.
"""
import json
import sys
from pathlib import Path
from customer_attraction.model import Instance, CustomerType
from customer_attraction.exact import ExactSPESolver

HERE = Path(__file__).resolve().parent
raw = json.loads((HERE / (sys.argv[1] if len(sys.argv) > 1 else 'discovery.json')).read_text())
target = tuple(raw['target'])
base = Instance.from_dict(raw['instance'])

def obstruction(instance, counts):
    if counts not in ExactSPESolver(instance).outcomes():
        return False
    kept = tuple(x for x in instance.customers if any(counts[a] for a in x.topics))
    if kept == instance.customers:
        return False
    return counts not in ExactSPESolver(Instance(instance.topics, kept, instance.players)).outcomes()

rows = list(base.customers)
assert obstruction(base, target)
changes = 0
while True:
    changed = False
    for i in range(len(rows)):
        old = rows[i]
        for weight in range(old.multiplicity):
            replacement = [CustomerType(old.topics, weight)] if weight else []
            trial = rows[:i] + replacement + rows[i+1:]
            inst = Instance(base.topics, tuple(trial), base.players)
            if obstruction(inst, target):
                rows = trial
                changes += 1
                print('reduce', sorted(old.topics), old.multiplicity, 'to', weight, flush=True)
                changed = True
                break
        if changed:
            break
    if not changed:
        break
inst = Instance(base.topics, tuple(rows), base.players)
result = {'instance': inst.to_dict(), 'target': list(target), 'reductions': changes}
(HERE / (sys.argv[2] if len(sys.argv) > 2 else 'minimal.json')).write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result), flush=True)
