#!/usr/bin/env python3
"""共同宏退出与完整接收池的实际调度构造。

Uses only the existing exact covering FPTAS and Hungarian primitive.
No generic unrelated-machine approximation is asserted.  The explicit
pool profile and private-home structure are part of the input contract.
"""
from fractions import Fraction as F
from importlib.util import spec_from_file_location, module_from_spec
from pathlib import Path

PRIMITIVE = Path(__file__).resolve().with_name('shared_sink_joint_assignment.py')
spec = spec_from_file_location('shared_sink_primitives', PRIMITIVE)
base = module_from_spec(spec)
spec.loader.exec_module(base)

def solve_shared_sink_with_exits(H, macros, tinies, T, eta):
    """Macro row has H home entries and one sink entry; None means forbidden.

    Every finite home entry must be > T/2.  Sink entries need only be
    nonnegative.  Tinies are (unique_home, home_time, sink_time).
    On success returns the complete actual assignment and exact loads.
    The pool wrapper normalizes its work budget to this sink target T.
    """
    if type(H) is not int or H < 0:
        raise ValueError('bad home count')
    T, eta = base._fraction(T), base._fraction(eta)
    budget = T
    if not 0 < eta <= 1:
        raise ValueError('bad accuracy')
    normalized = []
    for row in macros:
        if len(row) != H + 1:
            raise ValueError('bad macro row')
        row = [None if p is None else base._fraction(p) for p in row]
        if all(p is None for p in row):
            raise ValueError('macro has no available machine')
        if any(p is not None and p <= T/2 for p in row[:H]):
            raise ValueError('macro home times must exceed T/2')
        normalized.append(row)
    macros = normalized
    jobs = []
    for h, a, c in tinies:
        if type(h) is not int or not 0 <= h < H:
            raise ValueError('bad unique home')
        a = None if a is None else base._fraction(a)
        c = None if c is None else base._fraction(c)
        if a is None and c is None:
            raise ValueError('private job has no available machine')
        jobs.append((h, a, c))
    b = len(macros)
    # Preserve a genuine zero optimum even if the caller supplied positive T.
    # Every available macro-home time is positive, so a zero schedule must
    # put every macro at its zero-cost sink endpoint.
    if all(row[H] == 0 for row in macros):
        zero = [H] * b
        for h, a, c in jobs:
            if a == 0:
                zero.append(h)
            elif c == 0:
                zero.append(H)
            else:
                break
        else:
            return {'status': 'SCHEDULE', 'assignment': zero, 'loads': [F()] * (H+1),
                    'macro_exits': list(range(b))}
    fixed_home = [F()] * H
    fixed_sink = F()
    optional = [[] for _ in range(H)]
    default = []
    for label, (h, a, c) in enumerate(jobs):
        if c is None:
            fixed_home[h] += a
            default.append(h)
        elif a is None:
            fixed_sink += c
            default.append(H)
        else:
            optional[h].append((a, c, label))
            default.append(h)
    if fixed_sink > budget:
        return {'status': 'REJECT_TARGET'}

    def mode(h, macro_time):
        if macro_time is None or fixed_home[h] + macro_time > T:
            return None
        demand = fixed_home[h] + macro_time + sum((a for a, _, _ in optional[h]), F()) - T
        return base.covering_fptas(optional[h], demand, eta)

    real_modes = [[mode(h, row[h]) for h in range(H)] for row in macros]
    empty_modes = [mode(h, F()) for h in range(H)]
    # H+b by H+b.  Exit positions have no individual capacity: their real
    # costs all contribute to the one shared sink objective and budget.
    costs = [[None if witness is None else witness[0] for witness in real_modes[j]]
             + [macros[j][H]] * b for j in range(b)]
    costs += [[None if witness is None else witness[0] for witness in empty_modes]
              + [F()] * b for _ in range(H)]
    matching = base.minimum_assignment(costs)
    if matching is None:
        return {'status': 'REJECT_TARGET'}
    assignment = [None] * b + default[:]
    exits = []
    for j, destination in enumerate(matching):
        if j < b:
            if destination >= H:
                assignment[j] = H
                exits.append(j)
                continue
            assignment[j] = destination
            witness = real_modes[j][destination]
        elif destination < H:
            witness = empty_modes[destination]
        else:
            continue
        for label in witness[1]:
            assignment[b + label] = H
    loads = single_sink_loads(H, macros, jobs, assignment)
    assert all(load <= T for load in loads[:H])
    if loads[H] > (1 + eta)*budget:
        return {'status': 'REJECT_TARGET'}
    return {'status': 'SCHEDULE', 'assignment': assignment, 'loads': loads, 'macro_exits': exits}

def single_sink_loads(H, macros, tinies, assignment):
    loads = [F()] * (H+1)
    for j, row in enumerate(macros):
        p = row[assignment[j]]
        assert p is not None
        loads[assignment[j]] += p
    b = len(macros)
    for j, (h, a, c) in enumerate(tinies):
        target = assignment[b+j]
        assert target in (h, H)
        p = a if target == h else c
        assert p is not None
        loads[target] += p
    return loads


def solve_exit_pool(H, macros, private_jobs, rates, T, eta, beta,
                    rho=1, pool_times=None):
    """Return an actual schedule or a sound REJECT_TARGET for this class.

    Macro row: H home times followed by its pool work c (None forbids pool).
    Private row: (designated_home, home_time, pool_work).
    Every finite macro-home edge is >T/2; private jobs have only their home.
    rates[z]>0; every pool-enabled job is eligible on EVERY pool machine.
    Supplied pool_times has one row per job (macros first); rows are None
    exactly for pool-forbidden jobs.  Otherwise a_z*c <= p_zj <= rho*a_z*c
    and p_zj <= beta*T for every z.  If omitted p_zj=a_z*c is generated.
    Output home loads <=T and pool loads <=(rho*(1+eta)+beta)*T.
    Runtime is polynomial in input bit length and numeric 1/eta.
    """
    if type(H) is not int or H < 0:
        raise ValueError('bad home count')
    T, eta, beta, rho = map(base._fraction, (T, eta, beta, rho))
    if not 0 < eta <= 1 or rho < 1:
        raise ValueError('eta in (0,1] and rho>=1 required')
    rates = [base._fraction(a) for a in rates]
    if not rates or any(a == 0 for a in rates):
        raise ValueError('pool must be nonempty with positive rates')
    macros = [[None if v is None else base._fraction(v) for v in row]
              for row in macros]
    if any(len(row) != H+1 for row in macros):
        raise ValueError('bad macro row')
    private_jobs = [(h, None if a is None else base._fraction(a),
                     None if c is None else base._fraction(c))
                    for h, a, c in private_jobs]
    works = [row[H] for row in macros] + [c for h, a, c in private_jobs]
    if pool_times is None:
        pool_times = [None if c is None else [a*c for a in rates] for c in works]
    if len(pool_times) != len(works):
        raise ValueError('one pool profile per job required')
    actual = []
    for c, row in zip(works, pool_times):
        if c is None:
            if row is not None:
                raise ValueError('forbidden job has pool profile')
            actual.append(None)
            continue
        if row is None or len(row) != len(rates):
            raise ValueError('complete pool eligibility required')
        row = [base._fraction(p) for p in row]
        if any(not a*c <= p <= rho*a*c or p > beta*T
               for a, p in zip(rates, row)):
            raise ValueError('pool bounds violated')
        actual.append(row)
    speed_sum = sum((1/a for a in rates), F())
    virtual_macros = [row[:H]+[None if row[H] is None else row[H]/speed_sum]
                      for row in macros]
    virtual_private = [(h, a, None if c is None else c/speed_sum)
                       for h, a, c in private_jobs]
    virtual = solve_shared_sink_with_exits(H, virtual_macros, virtual_private, T, eta)
    if virtual['status'] != 'SCHEDULE':
        return virtual
    assignment = virtual['assignment'][:]
    loads = [F()] * (H+len(rates))
    pool_work = F()
    for j, destination in enumerate(assignment):
        if destination < H:
            p = macros[j][destination] if j < len(macros) else private_jobs[j-len(macros)][1]
        else:
            z = min(range(len(rates)), key=lambda q: (loads[H+q], q))
            assert loads[H+z] <= rho*(1+eta)*T
            destination = H+z
            assignment[j] = destination
            p = actual[j][z]
            pool_work += works[j]
        loads[destination] += p
    assert pool_work <= (1+eta)*T*speed_sum
    assert all(q <= T for q in loads[:H])
    assert all(q <= (rho*(1+eta)+beta)*T for q in loads[H:])
    return dict(status='SCHEDULE', assignment=assignment, loads=loads,
                pool_work=pool_work, makespan=max(loads),
                factor=rho*(1+eta)+beta)
