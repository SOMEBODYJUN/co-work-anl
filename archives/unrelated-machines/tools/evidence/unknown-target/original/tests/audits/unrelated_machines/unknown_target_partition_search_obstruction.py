from itertools import product

def has_balanced_partition(w):
    B=sum(w)//2
    return any(sum(w[i] for i,b in enumerate(bits) if b)==B for bits in product((0,1), repeat=len(w)))

def feasible_two_machine(w):
    B=sum(w)//2
    return has_balanced_partition(w)

for w,expected in [([1,1],True),([1,2,3],True),([1,1,1,3],True),([2,2,2,2,2],False)]:
    assert feasible_two_machine(w)==expected
print('ok')
