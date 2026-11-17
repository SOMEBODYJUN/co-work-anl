from fractions import Fraction
from itertools import product


WEIGHTS = {
    0: [((),3,1),((0,),0,1),((0,),1,1),((1,),0,1),((0,2),0,1),((1,3),0,2)],
    1: [((),3,2),((0,),1,2),((0,3),1,2),((0,5),1,2)],
    2: [((),4,2),((0,),1,2),((0,3),2,4),((4,0),2,2)],
    3: [((),3,2),((0,),1,2),((0,2),3,2),((0,3),3,2)],
    4: [((),4,2),((0,),1,2),((0,2),4,2)],
    5: [((),5,2),((0,),1,2),((0,2),5,2),((0,3),5,2)],
}
Q = ((0,1),(0,2),(0,3))


def action(history):
    if not history:
        return 0
    if len(history) == 1:
        return 3 if history[0] < 3 else 0
    group = range(3) if history[1] < 3 else range(3, 6)
    return next(a for a in group if a not in history)


def finish(history):
    while len(history) < 3:
        history += (action(history),)
    return history


def hit(mask, a):
    return (mask >> a) & 1


def load(mask, terminal):
    return sum(hit(mask, a) for a in terminal)


def share(mask, a, terminal, background):
    return Fraction(1, background + load(mask, terminal)) if hit(mask, a) else Fraction(0)


def main():
    actual = finish(())
    counts = [0, 0, 0]
    for a, mask in product(range(6), range(1,64)):
        # coeff[d] is the coefficient of 1/(background+d) before multiplying through.
        coeff = [Fraction(0) for _ in range(4)]
        real_load = load(mask, actual)
        coeff[real_load] += Fraction(real_load, 3)
        if hit(mask, a):
            for competing in Q:
                coeff[load(mask, competing + (a,))] -= Fraction(1, 3)
        for h, alternative, weight_times_six in WEIGHTS[a]:
            prescribed = action(h)
            assert prescribed != alternative
            mult = Fraction(weight_times_six, 6)
            if hit(mask, prescribed):
                coeff[load(mask, finish(h))] -= mult
            if hit(mask, alternative):
                coeff[load(mask, finish(h + (alternative,)))] += mult
        assert coeff[0] == 0
        c1, c2, c3 = coeff[1:]
        polynomial = (6*c1+3*c2+2*c3, 5*c1+4*c2+3*c3, c1+c2+c3)
        assert min(polynomial) >= 0, (a, mask, polynomial)
        for i, v in enumerate(polynomial):
            counts[i] += v > 0
        for background in (Fraction(0), Fraction(1,3), Fraction(1), Fraction(12)):
            actual_value = Fraction(real_load, 3*(background+real_load)) if real_load else 0
            query_value = sum(share(mask,a,b+(a,),background) for b in Q)/3
            ic = sum(Fraction(w,6) * (share(mask,action(h),finish(h),background)
                     - share(mask,d,finish(h+(d,)),background)) for h,d,w in WEIGHTS[a])
            denominator = (background+1)*(background+2)*(background+3)
            assert (actual_value-query_value-ic)*denominator == sum(v*background**i for i,v in enumerate(polynomial))
    print('378 polynomial triples; positive coefficients by degree:', *counts)


if __name__ == '__main__':
    main()
