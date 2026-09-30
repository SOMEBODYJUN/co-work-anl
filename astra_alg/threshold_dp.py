"""Exact two-facility mixed-NE load spectrum by threshold dynamic programming.

Common weights are positive integers; private weights may be rational.
This research implementation retains all DP parent layers for witnesses.
"""

from dataclasses import dataclass
from fractions import Fraction as F
from itertools import product


@dataclass(frozen=True)
class Piece:
    lo: F
    hi: F
    cutoff: int
    sign: int
    state: tuple


class Spectrum:
    def __init__(self, weights, exclusive_a=0, exclusive_b=0):
        if any(not isinstance(w, int) or w <= 0 for w in weights):
            raise ValueError('Common weights must be positive integers')
        self.weights = list(weights)
        self.order = sorted(range(len(weights)), key=lambda i: weights[i], reverse=True)
        self.sorted_weights = [weights[i] for i in self.order]
        self.a, self.b = F(exclusive_a), F(exclusive_b)
        self.delta = self.a - self.b
        self.total = self.a + self.b + sum(weights)
        self.parents = [{(0, 0): None}]
        self.pieces = []
        light = sum(weights)
        n = len(weights)
        for j in range(n + 1):
            states = self.parents[j]
            low_abs = F(self.sorted_weights[j]) if j < n else F(0)
            high_abs = F(self.sorted_weights[j - 1]) if j else None
            for (k, z) in states:
                for sign in (-1, 1):
                    numerator = self.delta - sign * light + z
                    if k == 1:
                        if numerator or high_abs is None:
                            continue
                        lo, hi = ((-high_abs, -low_abs) if sign < 0
                                  else (low_abs, high_abs))
                    else:
                        gap = numerator / (1 - k)
                        magnitude = sign * gap
                        if magnitude < low_abs or (high_abs is not None and magnitude > high_abs):
                            continue
                        lo = hi = gap
                    self.pieces.append(Piece(lo, hi, j, sign, (k, z)))
            if j < n:
                w = self.sorted_weights[j]
                nxt = {}
                for k, z in states:
                    for action, state in (('A', (k, z + w)),
                                          ('B', (k, z - w)),
                                          ('M', (k + 1, z))):
                        nxt.setdefault(state, ((k, z), action))
                self.parents.append(nxt)
                light -= w

    def witness(self, piece, gap=None):
        gap = piece.lo if gap is None else F(gap)
        if not piece.lo <= gap <= piece.hi:
            raise ValueError('Gap not in spectral piece')
        states = ['A' if piece.sign < 0 else 'B'] * len(self.weights)
        state = piece.state
        for j in range(piece.cutoff, 0, -1):
            state, action = self.parents[j][state]
            states[j - 1] = action
        probs = [None] * len(self.weights)
        for j, action in enumerate(states):
            w = self.sorted_weights[j]
            p = F(1) if action == 'A' else F(0) if action == 'B' else (1 + gap / w) / 2
            probs[self.order[j]] = p
        assert verify(self.weights, self.a, self.b, probs)
        return probs

    def minimum(self):
        piece = min(self.pieces, key=lambda p: p.lo)
        return (self.total + piece.lo) / 2, self.witness(piece)

    def quotas(self, min_a, min_b):
        lo, hi = 2 * F(min_a) - self.total, self.total - 2 * F(min_b)
        for piece in self.pieces:
            gap = max(lo, piece.lo)
            if gap <= min(hi, piece.hi):
                return self.witness(piece, gap)
        return None

    def merged_gaps(self):
        return merge_intervals((p.lo, p.hi) for p in self.pieces)


def verify(weights, a, b, probabilities):
    a, b = F(a), F(b)
    la = a + sum(w * p for w, p in zip(weights, probabilities))
    lb = b + sum(w * (1 - p) for w, p in zip(weights, probabilities))
    for w, p in zip(weights, probabilities):
        if not 0 <= p <= 1:
            return False
        # Costs conditional on own facility choice exclude one's own expected mass.
        cost_a = la + w * (1 - p)
        cost_b = lb + w * p
        if p > 0 and cost_a > cost_b:
            return False
        if p < 1 and cost_b > cost_a:
            return False
    return True


def merge_intervals(intervals):
    result = []
    for lo, hi in sorted(set(intervals)):
        if result and lo <= result[-1][1]:
            result[-1] = (result[-1][0], max(hi, result[-1][1]))
        else:
            result.append((lo, hi))
    return result


def brute_gaps(weights, a=0, b=0):
    """Independent support enumerator used only as a small-instance oracle."""
    ans = []
    delta = F(a) - F(b)
    for actions in product(('A', 'B', 'M'), repeat=len(weights)):
        k = actions.count('M')
        numerator = delta + sum(w * (1 if action == 'A' else -1 if action == 'B' else 0)
                                for w, action in zip(weights, actions))
        lower = max([-F(w) for w, action in zip(weights, actions) if action != 'A'], default=None)
        upper = min([F(w) for w, action in zip(weights, actions) if action != 'B'], default=None)
        if k == 1:
            if numerator == 0 and lower <= upper:
                ans.append((lower, upper))
        else:
            gap = numerator / (1 - k)
            if (lower is None or gap >= lower) and (upper is None or gap <= upper):
                ans.append((gap, gap))
    return merge_intervals(ans)


if __name__ == '__main__':
    from random import Random
    rng = Random(918274)
    count = 0
    for n in range(9):
        for trial in range(70 if n < 7 else 20):
            weights = [rng.randint(1, 8) for _ in range(n)]
            a, b = F(rng.randint(0, 35), rng.randint(1, 7)), F(rng.randint(0, 35), rng.randint(1, 7))
            spectrum = Spectrum(weights, a, b)
            oracle = brute_gaps(weights, a, b)
            assert spectrum.merged_gaps() == oracle, (weights, a, b, spectrum.merged_gaps(), oracle)
            spectrum.minimum()
            for piece in spectrum.pieces:
                spectrum.witness(piece, (piece.lo + piece.hi) / 2)
            count += 1
    print(f'PASS: {count} instances, full gap spectra equal 3^n oracle, every midpoint witness Nash-checked.')
