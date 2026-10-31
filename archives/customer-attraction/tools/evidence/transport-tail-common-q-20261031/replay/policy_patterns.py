"""Complete ordered-history policy candidates. No equilibrium is asserted.

Use with a full-Gamma cone LP; the prescribed policy is independent of weights.
The file does not import or change the repository.
"""
from __future__ import annotations

import argparse
import hashlib
from itertools import product
import json
from pathlib import Path


class GroupPolicy:
    def __init__(self, name: str, groups: tuple[tuple[int, ...], ...], n: int):
        self.name, self.groups, self.n = name, groups, n
        self.m = sum(map(len, groups))
        assert sorted(a for G in groups for a in G) == list(range(self.m))
        self.owner = {a: g for g, G in enumerate(groups) for a in G}

    def pick(self, g, h, shift=0, menu=None):
        """Always defined, including repeated/exhausted arbitrary histories."""
        G = self.groups[g] if menu is None else tuple(menu)
        order = G[shift % len(G):] + G[:shift % len(G)]
        return min(order, key=lambda a: (h.count(a), order.index(a)))

    def next(self, g):
        return (g + 1) % len(self.groups)

    def missing(self, h):
        represented = {self.owner[a] for a in h}
        start = self.next(self.owner[h[-1]]) if h else 0
        order = tuple((start + k) % len(self.groups) for k in range(len(self.groups)))
        return next((g for g in order if g not in represented), start)

    def nominal(self):
        if self.name == 'returning_minority':
            return (0, 3, 1, 4, 5)
        if self.name == 'delayed_reversal':
            return (0, 3, 4, 1, 2)
        return (0, 2, 4, 5, 6)

    def action(self, h):
        h = tuple(h)
        d = len(h)
        assert 0 <= d < self.n and all(a in self.owner for a in h)
        if d == 0:
            return 0
        if self.name in ('cascade', 'ordered_cascade'):
            anchor = self.n - 3
            if d <= anchor:
                return self.pick(self.missing(h), h)
            g = self.owner[h[anchor]]
            shift = self.owner[h[0]] + 2 * self.owner[h[1]] if self.name == 'ordered_cascade' else 0
            return self.pick(g, h, shift)
        if self.name == 'returning_minority':
            g = self.next(self.owner[h[0]]) if d == 1 else self.owner[h[0]] if d == 2 else self.owner[h[1]]
            return self.pick(g, h)
        if self.name == 'delayed_reversal':
            g = self.next(self.owner[h[0]]) if d in (1, 2) else self.owner[h[0]]
            return self.pick(g, h)
        if self.name in ('first_deviator_chase', 'latest_deviator_chase', 'deviator_successor'):
            z = self.nominal()
            if self.name == 'latest_deviator_chase':
                # Recompute the finite automaton, recording a genuine deviation
                # from the action prescribed before that observed move.
                latest = None
                for j, a in enumerate(h):
                    expected = z[j] if latest is None else self.pick(self.owner[h[latest]], h[:j], shift=latest)
                    if a != expected:
                        latest = j
                mismatches = [] if latest is None else [latest]
            else:
                mismatches = [j for j, a in enumerate(h) if a != z[j]]
            if not mismatches:
                return z[d]
            j = mismatches[-1] if self.name == 'latest_deviator_chase' else mismatches[0]
            g = self.owner[h[j]]
            if self.name == 'deviator_successor':
                g = self.next(g)
            return self.pick(g, h, shift=j)
        if self.name == 'ordered_pair_menu':
            if d <= 2:
                return self.pick(self.missing(h), h)
            g = self.owner[h[2]]
            G = self.groups[g]
            shift = (self.owner[h[0]] + 2 * self.owner[h[1]]) % len(G)
            pair = (G[shift], G[(shift + 1) % len(G)]) if len(G) > 1 else G
            return self.pick(g, h, menu=pair)
        raise ValueError(self.name)

    def actions(self):
        return {h: self.action(h) for d in range(self.n) for h in product(range(self.m), repeat=d)}

    def finish(self, h=()):
        h = tuple(h)
        while len(h) < self.n:
            h += (self.action(h),)
        return h


def candidates():
    tri = ((0, 1), (2, 3), (4, 5, 6))
    two = ((0, 1, 2), (3, 4, 5, 6))
    yield GroupPolicy('cascade', tri, 5)
    yield GroupPolicy('returning_minority', two, 5)
    yield GroupPolicy('delayed_reversal', two, 5)
    yield GroupPolicy('first_deviator_chase', tri, 5)
    yield GroupPolicy('latest_deviator_chase', tri, 5)
    yield GroupPolicy('deviator_successor', tri, 5)
    yield GroupPolicy('ordered_pair_menu', tri, 5)
    yield GroupPolicy('ordered_cascade', ((0, 1), (2, 3), (4, 5, 6, 7)), 5)
    yield GroupPolicy('cascade', ((0,), (1, 2), (3, 4), (5, 6, 7)), 6)


def summary(policy):
    actions = policy.actions()
    raw = [{'history': list(h), 'action': a} for h, a in actions.items()]
    root = policy.finish()
    roots = [policy.finish((a,))[1:] for a in range(policy.m)]
    bycounts = {}
    witnesses = []
    for h, a in actions.items():
        counts = tuple(h.count(b) for b in range(policy.m))
        if counts in bycounts and bycounts[counts][1] != a and len(witnesses) < 3:
            witnesses.append([list(bycounts[counts][0]), list(h), bycounts[counts][1], a])
        bycounts.setdefault(counts, (h, a))
    return {'name': policy.name, 'n': policy.n, 'm': policy.m, 'groups': policy.groups,
            'root': root, 'root_group_counts': [sum(policy.owner[a] == g for a in root) for g in range(len(policy.groups))],
            'ordered_decision_histories': len(actions), 'all_action_comparisons': policy.m * len(actions),
            'unique_root_competitor_counts': len({tuple(B.count(a) for a in range(policy.m)) for B in roots}),
            'same_counts_different_action_witnesses': witnesses,
            'policy_sha256': hashlib.sha256(json.dumps(raw, separators=(',', ':')).encode()).hexdigest()}


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--output', type=Path)
    p.add_argument('--export-actions', action='store_true')
    args = p.parse_args()
    policies = list(candidates())
    out = {'status': 'FORMAL_POLICIES_ONLY_NOT_SPE_CERTIFICATES', 'candidates': [summary(x) for x in policies]}
    if args.export_actions:
        for row, policy in zip(out['candidates'], policies):
            row['actions'] = [{'history': list(h), 'action': a} for h, a in policy.actions().items()]
    serialized = json.dumps(out, indent=2) + '\n'
    if args.output:
        args.output.write_text(serialized)
    else:
        print(serialized)
