"""Explicit degree-two weighted-menu UM backend (structured audit implementation).

Input: nonempty ``groups`` and explicit ``resources``; each group has nonempty
indexed ``states``, each state has ``incidences`` [{resource, p}].  IDs are unique
strings; p is an exact int or rational string, never a float.  This implements
only the domain in UM-DEGREE-TWO-BOUNDED-MENU-JOINT-ROUNDING-v2.

The core uses no optimum oracle, enumeration, LP, recursive DFS, or external
solver.  The only imported mathematical ingredient is VW2010v1 Theorem 12,
implemented here by forced-largest preprocessing and iterative BFS coloring.
"""
from collections import deque
from dataclasses import dataclass
from fractions import Fraction
from math import lcm
import argparse
import json
import re
import sys

# Explicit rational encodings may exceed CPython's decimal digit default.
# The algorithm works in encoding length and never expands a numeric count.
if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)


def rat(x):
    if isinstance(x, bool) or not isinstance(x, (int, str, Fraction)):
        raise ValueError('processing times must be exact integers/rational strings')
    if isinstance(x, str) and re.fullmatch(r'-?[0-9]+(?:/[0-9]+)?', x) is None:
        raise ValueError('use explicit N or N/D, without decimal/exponent shorthand')
    try:
        return Fraction(x)
    except ZeroDivisionError as exc:
        raise ValueError('zero rational denominator') from exc


def named(x, what):
    if not isinstance(x, str):
        raise ValueError(what + ' ID must be a string')
    return x


@dataclass(frozen=True)
class State:
    name: str
    incidences: tuple


@dataclass(frozen=True)
class Group:
    name: str
    states: tuple


@dataclass(frozen=True)
class Instance:
    resources: tuple
    groups: tuple


def parse(payload):
    resources = tuple(named(x, 'resource') for x in payload['resources'])
    if len(set(resources)) != len(resources):
        raise ValueError('duplicate explicit resource')
    allowed = set(resources)
    groups = []
    group_names = set()
    support = {r: set() for r in resources}
    for gi, raw_g in enumerate(payload['groups']):
        gn = named(raw_g['id'], 'group')
        if gn in group_names:
            raise ValueError('duplicate group ID')
        group_names.add(gn)
        states = []
        state_names = set()
        for raw_s in raw_g['states']:
            sn = named(raw_s['id'], 'state')
            if sn in state_names:
                raise ValueError('duplicate state ID inside group')
            state_names.add(sn)
            inc = []
            seen = set()
            for raw_i in raw_s['incidences']:
                r = named(raw_i['resource'], 'resource')
                if r not in allowed or r in seen:
                    raise ValueError('unlisted resource or duplicate incidence inside state')
                seen.add(r)
                p = rat(raw_i['p'])
                if p < 0:
                    raise ValueError('negative private processing time')
                inc.append((r, p))
                support[r].add(gi)
            if sum((p for _, p in inc), Fraction(0)) > 1:
                raise ValueError('state private sum exceeds one')
            states.append(State(sn, tuple(inc)))
        if not states:
            raise ValueError('empty menu')
        groups.append(Group(gn, tuple(states)))
    if not groups:
        raise ValueError('empty group set is outside this Exact domain')
    if any(len(s) > 2 for s in support.values()):
        raise ValueError('a resource occurs in more than two distinct groups')
    return Instance(resources, tuple(groups))


def vw_threshold(endpoints, agents, T):
    """Integer one-sided oracle: success >=T/2, failure certifies OPT<T."""
    if T <= 0:
        raise ValueError('threshold oracle requires a positive integer')
    n = len(endpoints)
    active = [len(e) == 2 for e in endpoints]
    owner = {}
    private = [0] * agents
    available = [0] * agents
    lists = [[] for _ in range(agents)]
    weight = [dict(e) for e in endpoints]
    for j, e in enumerate(endpoints):
        if len(e) == 1:
            g, v = e[0]
            owner[j] = g
            private[g] += v
        else:
            for g, v in e:
                lists[g].append(j)
                available[g] += v
    for g in range(agents):
        lists[g].sort(key=lambda j: (-weight[j][g], j))
    ptr = [0] * agents
    queue = deque(range(agents))
    queued = [True] * agents
    forced = []
    while queue:
        g = queue.popleft()
        queued[g] = False
        total = available[g] + private[g]
        if total < T:
            return {'success': False, 'agent': g, 'available': total,
                    'T': T, 'forced': forced}
        while ptr[g] < len(lists[g]) and not active[lists[g][ptr[g]]]:
            ptr[g] += 1
        if ptr[g] == len(lists[g]):
            continue
        j = lists[g][ptr[g]]
        if total - weight[j][g] < T:
            # A T-solution must give this item to g.  Remove BOTH occurrences.
            active[j] = False
            owner[j] = g
            forced.append({'item': j, 'owner': g,
                           'available_without': total - weight[j][g]})
            for other, value in endpoints[j]:
                available[other] -= value
                if other == g:
                    private[other] += value
                if not queued[other]:
                    queue.append(other)
                    queued[other] = True

    # The two matchings are same-item edges and consecutive local-pair edges.
    occurrence = {}
    adj = []
    def vertex(j, g):
        idx = len(adj)
        occurrence[(j, g)] = idx
        adj.append([])
        return idx
    def edge(a, b):
        adj[a].append(b)
        adj[b].append(a)
    for j, e in enumerate(endpoints):
        if active[j]:
            edge(vertex(j, e[0][0]), vertex(j, e[1][0]))
    for g in range(agents):
        live = [j for j in lists[g] if active[j]]
        tail = sum((weight[j][g] for j in live[1:]), 0)
        if tail + private[g] < T:
            raise AssertionError('forced-largest invariant not closed')
        for k in range(0, len(live) - 1, 2):
            edge(occurrence[(live[k], g)], occurrence[(live[k + 1], g)])
    color = [-1] * len(adj)
    for root in range(len(adj)):
        if color[root] != -1:
            continue
        color[root] = 0
        queue = deque([root])
        while queue:
            u = queue.popleft()
            for v in adj[u]:
                if color[v] == -1:
                    color[v] = 1 - color[u]
                    queue.append(v)
                elif color[v] == color[u]:
                    raise AssertionError('two-matching graph has odd cycle')
    for j, e in enumerate(endpoints):
        if active[j]:
            black = [g for g, _ in e if color[occurrence[(j, g)]] == 0]
            if len(black) != 1:
                raise AssertionError('item did not get exactly one owner')
            owner[j] = black[0]
    utility = utilities(endpoints, owner, agents)
    if len(owner) != n or 2 * min(utility) < T:
        raise AssertionError('threshold allocation guarantee failed')
    return {'success': True, 'owner': owner, 'utility': utility,
            'T': T, 'forced': forced}


def utilities(endpoints, owner, agents):
    result = [0] * agents
    for j, g in owner.items():
        result[g] += dict(endpoints[j])[g]
    return result


def vw_two_approx(rational_items, agents):
    """No OPT input: exact integer scaling and one-sided-certificate search."""
    if agents < 1:
        raise ValueError('nonempty agent set required')
    denominator = 1
    for _, e in rational_items:
        if not 1 <= len(e) <= 2 or len({g for g, _ in e}) != len(e):
            raise ValueError('each retained item needs one or two distinct agents')
        for g, v in e:
            if not 0 <= g < agents or v <= 0:
                raise ValueError('retained auxiliary values must be positive')
            denominator = lcm(denominator, v.denominator)
    endpoints = [tuple((g, v.numerator * (denominator // v.denominator))
                       for g, v in e) for _, e in rational_items]
    total = [0] * agents
    for e in endpoints:
        for g, v in e:
            total[g] += v
    U = min(total)
    low, high = 0, U + 1
    fallback = {j: e[0][0] for j, e in enumerate(endpoints)}
    best = {'owner': fallback, 'utility': utilities(endpoints, fallback, agents),
            'T': 0, 'forced': []}
    # high=U+1 is rejected by the initial total-available test.
    high_failure = {'agent': total.index(U), 'available': U, 'T': high,
                    'forced': []}
    calls = []
    while high - low > 1:
        T = (low + high) // 2
        answer = vw_threshold(endpoints, agents, T)
        calls.append({'T': T, 'success': answer['success']})
        if answer['success']:
            low = T
            best = answer
        else:
            high = T
            high_failure = answer
    best.update({'scale': denominator, 'low': low, 'high': high,
                 'upper_failure': high_failure, 'calls': calls})
    return best


def normalized_auxiliary(inst):
    states = []
    bonuses = []
    item_order = [('original', r) for r in inst.resources]
    values = {key: {} for key in item_order}
    for g, group in enumerate(inst.groups):
        normalized_group = []
        for s, state in enumerate(group.states):
            mass = {('original', r): p for r, p in state.incidences}
            W = sum(mass.values(), Fraction(0))
            if W < 1:
                key = ('bonus', g, s)
                mass[key] = 1 - W
                item_order.append(key)
                values[key] = {}
                bonuses.append((g, s, key, 1 - W))
            normalized_group.append(mass)
            for key, p in mass.items():
                if p > 0:
                    values[key][g] = values[key].get(g, Fraction(0)) + p / len(group.states)
        states.append(normalized_group)
    items = [(key, tuple(sorted(values[key].items())))
             for key in item_order if values[key]]
    if any(len(e) > 2 for _, e in items):
        raise AssertionError('group-degree condition lost during normalization')
    return states, bonuses, items


def original_jobs(inst):
    """Explicit original-job eligibility table; no auxiliary job is included."""
    table = {}
    for group in inst.groups:
        table[('selector', group.name)] = {
            ('state', group.name, state.name): Fraction(1) for state in group.states}
        for state in group.states:
            for r, p in state.incidences:
                table[('incidence', group.name, state.name, r)] = {
                    ('state', group.name, state.name): p,
                    ('resource', r): Fraction(1)}
    return table


def solve(payload):
    inst = parse(payload)
    states, bonuses, items = normalized_auxiliary(inst)
    backend = vw_two_approx(items, len(inst.groups))
    allocation = {items[j][0]: g for j, g in backend['owner'].items()}
    chosen, chosen_mass = [], []
    for g, group_states in enumerate(states):
        masses = [sum((p for key, p in state.items() if allocation.get(key) == g),
                      Fraction(0)) for state in group_states]
        s = max(range(len(masses)), key=lambda i: (masses[i], -i))
        chosen.append(s)
        chosen_mass.append(masses[s])
    D = backend['scale']
    utility = [Fraction(v, D) for v in backend['utility']]
    if any(chosen_mass[g] < utility[g] for g in range(len(inst.groups))):
        raise AssertionError('group averaging inequality failed')

    table = original_jobs(inst)
    assignments = []
    for g, group in enumerate(inst.groups):
        selected = group.states[chosen[g]]
        assignments.append((('selector', group.name), ('state', group.name, selected.name)))
        for s, state in enumerate(group.states):
            for r, _ in state.incidences:
                machine = (('resource', r) if s == chosen[g] and
                           allocation.get(('original', r)) == g else
                           ('state', group.name, state.name))
                assignments.append((('incidence', group.name, state.name, r), machine))
    loads = {('resource', r): Fraction(0) for r in inst.resources}
    loads.update({('state', g.name, s.name): Fraction(0)
                  for g in inst.groups for s in g.states})
    jobs = []
    for job, machine in assignments:
        p = table[job][machine]
        start = loads[machine]
        loads[machine] += p
        jobs.append({'job': list(job), 'machine': list(machine), 'p': str(p),
                     'start': str(start), 'finish': str(loads[machine])})

    # Reconstruct the normalized schedule before deleting precisely bonus jobs.
    normalized_loads = dict(loads)
    for g, s, key, p in bonuses:
        machine = (('bonus_resource', g, s) if s == chosen[g] and
                   allocation.get(key) == g else
                   ('state', inst.groups[g].name, inst.groups[g].states[s].name))
        normalized_loads[machine] = normalized_loads.get(machine, Fraction(0)) + (
            Fraction(1) if machine[0] == 'bonus_resource' else p)
    C = max(loads.values(), default=Fraction(0))
    normalized_C = max(normalized_loads.values(), default=Fraction(0))
    if normalized_C != 2 - min(chosen_mass) or C > normalized_C:
        raise AssertionError('actual private-state job accounting failed')
    if normalized_C > 2 - min(utility):
        raise AssertionError('allocation-to-makespan bound failed')
    result = {
        'scope': 'UM-DEGREE-TWO-BOUNDED-MENU-JOINT-ROUNDING-v2',
        'implementation': 'explicit structural backend; no general-UM claim',
        'K': max(len(g.states) for g in inst.groups),
        'chosen_states': [{'group': g.name, 'state': g.states[chosen[i]].name}
                          for i, g in enumerate(inst.groups)],
        'jobs': jobs, 'makespan': str(C),
        'normalized_makespan': str(normalized_C),
        'bonus_jobs_added_then_deleted': len(bonuses),
        'chosen_normalized_mass': [str(v) for v in chosen_mass],
        'aux_utility': [str(v) for v in utility],
        'aux_allocation': [{'item_index': j, 'item': list(key),
                            'group': inst.groups[backend['owner'][j]].name}
                           for j, (key, _) in enumerate(items)],
        'backend': {'integer_scale': str(D), 'successful_T': str(backend['low']),
                    'rejected_T': str(backend['high']),
                    'oracle_calls': backend['calls'],
                    'upper_failure': backend['upper_failure'],
                    'successful_forces': backend['forced']},
    }
    verify(inst, result)
    return result


def verify(inst, result):
    """Check all original jobs, eligibility, processing times and actual times."""
    table = original_jobs(inst)
    seen = set()
    occupied = {}
    loads = {}
    completion = Fraction(0)
    for rec in result['jobs']:
        job, machine = tuple(rec['job']), tuple(rec['machine'])
        if job not in table or job in seen or machine not in table[job]:
            raise AssertionError('missing/duplicate/illegal original job assignment')
        seen.add(job)
        p = table[job][machine]
        start, finish = rat(rec['start']), rat(rec['finish'])
        if p != rat(rec['p']) or start < 0 or finish != start + p:
            raise AssertionError('incorrect actual processing interval')
        loads[machine] = loads.get(machine, Fraction(0)) + p
        completion = max(completion, finish)
        if p > 0:
            occupied.setdefault(machine, []).append((start, finish))
    if seen != set(table):
        raise AssertionError('not every original job was output')
    for intervals in occupied.values():
        intervals.sort()
        if any(a[1] > b[0] for a, b in zip(intervals, intervals[1:])):
            raise AssertionError('overlapping machine execution')
    if completion != rat(result['makespan']) or max(loads.values(), default=0) != completion:
        raise AssertionError('makespan does not match complete actual schedule')
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('input', help='explicit weighted-menu JSON')
    args = ap.parse_args()
    with open(args.input) as stream:
        answer = solve(json.load(stream))
    print(json.dumps(answer, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
