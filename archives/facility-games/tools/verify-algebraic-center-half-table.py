"""Compare the algebraic-center half table to independent closed-support enumeration."""
from bisect import bisect_left, bisect_right
from fractions import Fraction as F
from itertools import product
from random import Random

CENTER = None

def sign(x):
    return (x > 0) - (x < 0)

class Root:
    def __init__(self, coefficients, lo, hi):
        self.coefficients = coefficients
        self.lo, self.hi = F(lo), F(hi)
        self.low_sign = sign(self.evaluate(self.lo))
        assert self.low_sign and self.low_sign == -sign(self.evaluate(self.hi))

    def evaluate(self, rational):
        value = 0
        for coefficient in self.coefficients:
            value = value * rational + coefficient
        return value

    def against(self, rational):
        """Return the sign of center minus a rational."""
        if rational <= self.lo:
            return 1
        if rational >= self.hi:
            return -1
        at = sign(self.evaluate(rational))
        return at * self.low_sign

    def clip(self, lo, hi):
        if self.against(lo) <= 0:
            return lo
        if self.against(hi) >= 0:
            return hi
        return CENTER

    def compare_distance(self, a, b):
        ra = 0 if a is CENTER else self.against(a)
        rb = 0 if b is CENTER else self.against(b)
        if ra == 0 or rb == 0:
            return sign(abs(ra) - abs(rb))
        if ra == rb:
            return ra * sign(b - a)
        midpoint = (a + b) / 2
        return ra * self.against(midpoint)

def states(weights):
    groups = {}
    for word in product((-1, 0, 1), repeat=len(weights)):
        mixed = word.count(0)
        signed = sum((w * action for w, action in zip(weights, word)), F(0))
        groups.setdefault(mixed, {}).setdefault(signed, word)
    return groups

def half_candidates(a, b, weights, center):
    total = a + b + sum(weights)
    for h in range(len(weights) + 1):
        cut = h // 2
        left = states(weights[:cut])
        right = states(weights[cut:h])
        lower = weights[h] if h < len(weights) else F(0)
        upper = weights[h - 1] if h else total
        for direction in (-1, 1):
            lo, hi = (-upper, -lower) if direction < 0 else (lower, upper)
            offset = a - b - direction * sum(weights[h:])
            for ml, ls in left.items():
                for mr, rs in right.items():
                    factor = 1 - ml - mr
                    ordered = sorted(rs)
                    for zl, wl in ls.items():
                        if factor == 0:
                            zr = -offset - zl
                            candidates = [(center.clip(lo, hi), zr)] if zr in rs else []
                        else:
                            v1, v2 = factor * lo - offset - zl, factor * hi - offset - zl
                            first = bisect_left(ordered, min(v1, v2))
                            end = bisect_right(ordered, max(v1, v2))
                            low, high = first, end
                            while low < high:
                                mid = (low + high) // 2
                                gap = (offset + zl + ordered[mid]) / factor
                                if factor * center.against(gap) > 0:
                                    low = mid + 1
                                else:
                                    high = mid
                            candidates = [((offset + zl + ordered[k]) / factor, ordered[k])
                                          for k in (low - 1, low) if first <= k < end]
                        for gap, zr in candidates:
                            yield gap, wl + rs[zr] + (-direction,) * (len(weights) - h)

def brute_candidates(a, b, weights, center):
    total = a + b + sum(weights)
    for word in product((-1, 0, 1), repeat=len(weights)):
        lo, hi, signed, mixed = -total, total, a - b, 0
        for w, action in zip(weights, word):
            if action != 1:
                lo = max(lo, -w)
            if action != -1:
                hi = min(hi, w)
            signed += action * w
            mixed += action == 0
        if lo > hi:
            continue
        if mixed == 1:
            if signed == 0:
                yield center.clip(lo, hi), word
        else:
            gap = signed / (1 - mixed)
            if lo <= gap <= hi:
                yield gap, word

def best(rows, center):
    chosen = next(rows)
    for row in rows:
        if center.compare_distance(row[0], chosen[0]) < 0:
            chosen = row
    return chosen

def verify_output(a, b, weights, center, gap, word):
    def affine_sign(x, y):
        return sign(x) if not y else sign(y) * center.against(-x / y)

    gap_c, gap_d = (F(0), F(1)) if gap is CENTER else (gap, F(0))
    load_c, load_d = a - b, F(0)
    for w, action in zip(weights, word):
        pc, pd = (F(1 + action, 2), F(0)) if action else (F(1, 2) + gap_c / (2*w), gap_d / (2*w))
        assert affine_sign(pc, pd) >= 0 and affine_sign(1 - pc, -pd) >= 0
        diff = affine_sign(gap_c + w * (1 - 2 * pc), gap_d - 2 * w * pd)
        assert action * diff <= 0 if action else diff == 0
        load_c += w * (2 * pc - 1)
        load_d += 2 * w * pd
    assert affine_sign(load_c - gap_c, load_d - gap_d) == 0

rng = Random(72511)
roots = (Root((2, 0, -1), 0, 1), Root((2, 0, -1), -1, 0),
         Root((3, -1), 0, 1), Root((1, 0, 0, -2), 1, 2))
counts = {"instances": 0, "affine_outputs": 0, "rational_outputs": 0}
for center in roots:
    cases = [(F(0), F(0), []), (F(0), F(0), [F(1)]), (F(0), F(0), [F(3)])]
    for _ in range(35):
        weights = sorted((F(rng.randint(1, 9), rng.randint(1, 4)) for _ in range(rng.randrange(7))), reverse=True)
        cases.append((F(rng.randrange(6), 2), F(rng.randrange(6), 3), weights))
    for a, b, weights in cases:
        half_gap, half_word = best(half_candidates(a, b, weights, center), center)
        brute_gap, _ = best(brute_candidates(a, b, weights, center), center)
        assert center.compare_distance(half_gap, brute_gap) == 0
        verify_output(a, b, weights, center, half_gap, half_word)
        counts["instances"] += 1
        counts["affine_outputs" if half_gap is CENTER else "rational_outputs"] += 1
print(counts)
