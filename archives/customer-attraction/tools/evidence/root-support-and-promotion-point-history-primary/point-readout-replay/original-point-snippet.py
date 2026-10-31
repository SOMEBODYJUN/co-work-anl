import json
from fractions import Fraction
from collections import defaultdict

p = 'research/workspaces/customer-attraction/R-3e17a9e6e3f747fd9cca4f93b99486d6/astra/promotion_joint_atoms_exact.json'
a = json.load(open(p))
h = a['histograms']
mass = defaultdict(Fraction)
for atom in a['RZ_atoms']:
    mass[atom['hist_index']] += Fraction(atom['weight'])
assert len(h) == 16 and {row['d'] for row in h} == {1}
assert sum(mass.values()) == 1
assert [i for i in range(len(h)) if mass[i] > 0] == [2,3,4,5,6,7,9,11,12,13,14]
assert sum(w for i,w in mass.items() if h[i]['d'] == 0) == 0
