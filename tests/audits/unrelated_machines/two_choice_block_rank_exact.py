"""Exact unrelated graph balancing parameterized by maximum block cycle rank.

Independent blind-review implementation.  All finite times are exact Fractions;
parallel jobs remain distinct labelled graph edges.  No project code is imported.
Input jobs is a list of one/two-element lists of (machine_label, time) pairs.
The API uses only active machine labels; machine_count, when supplied, validates
labels without allocating machine_count slots.  None in the matrix adapter is infinity.
"""
from __future__ import annotations
from fractions import Fraction as F
from math import lcm


def _time(x):
    if type(x) not in (int, F, str):
        raise ValueError('Use an exact int/Fraction/string; bool/float are not times')
    x = F(x)
    if x < 0:
        raise ValueError('negative processing time')
    return x


class BlockRankSolver:
    def __init__(self, jobs, machine_count=None):
        if machine_count is not None and (type(machine_count) is not int or machine_count < 1):
            raise ValueError('machine_count must be positive')
        self.jobs = []
        for opts in jobs:
            opts = tuple((v, _time(p)) for v,p in opts)
            if len(opts) not in (1,2) or len({v for v,p in opts}) != len(opts):
                raise ValueError('Each job must have one/two distinct finite machines')
            if any(type(v) is not int or v < 0 or
                   (machine_count is not None and v >= machine_count) for v,p in opts):
                raise ValueError('invalid machine label')
            self.jobs.append(opts)
        self.labels = sorted({v for opts in self.jobs for v,p in opts})
        index = {v:i for i,v in enumerate(self.labels)}
        nv = len(self.labels)
        self.base = [F(0)] * nv
        self.fixed = {}
        self.edges = []
        self.adj = [[] for _ in range(nv)]
        for j,opts in enumerate(self.jobs):
            if len(opts) == 1:
                v,p = opts[0]
                self.base[index[v]] += p
                self.fixed[j] = v
            else:
                (u,pu),(v,pv) = opts
                u,v = index[u],index[v]
                e = len(self.edges)
                self.edges.append((j,u,v,pu,pv))
                self.adj[u].append((v,e)); self.adj[v].append((u,e))
        self.blocks = self._blocks()
        # Vertex-block incidence graph is a forest even for labelled multigraphs.
        incidence = [[] for _ in range(nv+len(self.blocks))]
        self.vertices = []
        for b,B in enumerate(self.blocks):
            vs = sorted({v for e in B for v in self.edges[e][1:3]})
            self.vertices.append(vs)
            for v in vs:
                incidence[v].append(nv+b); incidence[nv+b].append(v)
        self.parent = [-2] * len(incidence)
        self.order = []
        self.roots = []
        for r in range(nv):
            if self.parent[r] != -2:
                continue
            self.roots.append(r); self.parent[r] = -1
            todo = [r]
            while todo:
                x = todo.pop(); self.order.append(x)
                for y in incidence[x]:
                    if y == self.parent[x]:
                        continue
                    if self.parent[y] != -2:
                        raise AssertionError('block-incidence graph is not a forest')
                    self.parent[y] = x; todo.append(y)
        self.incidence = incidence
        self.plans = [self._plan(b) for b in range(len(self.blocks))]
        self.b = max((len(chords) for root,order,pe,pa,chords in self.plans), default=0)

    def _blocks(self):
        # Iterative Tarjan; the parent EDGE, not parent vertex, is skipped.
        # Thus a second parallel edge is correctly treated as a back edge.
        nv = len(self.labels)
        disc = [-1] * nv; low = [0] * nv; par = [-1] * nv
        tick = 0; stack = []; blocks = []
        for r in range(nv):
            if disc[r] >= 0:
                continue
            disc[r] = low[r] = tick; tick += 1
            frames = [[r,-1,0]]
            while frames:
                u,pe,at = frames[-1]
                if at < len(self.adj[u]):
                    v,e = self.adj[u][at]; frames[-1][2] += 1
                    if e == pe:
                        continue
                    if disc[v] < 0:
                        stack.append(e); par[v] = u
                        disc[v] = low[v] = tick; tick += 1
                        frames.append([v,e,0])
                    elif disc[v] < disc[u]:
                        stack.append(e); low[u] = min(low[u],disc[v])
                else:
                    frames.pop()
                    if pe >= 0:
                        p = par[u]; low[p] = min(low[p],low[u])
                        if low[u] >= disc[p]:
                            B = []
                            while True:
                                e = stack.pop(); B.append(e)
                                if e == pe:
                                    break
                            blocks.append(B)
        if sorted(e for B in blocks for e in B) != list(range(len(self.edges))):
            raise AssertionError('block partition lost labelled edges')
        return blocks

    def _plan(self, b):
        nv = len(self.labels)
        root = self.parent[nv+b]
        uf = {v:v for v in self.vertices[b]}
        def find(v):
            while uf[v] != v:
                uf[v] = uf[uf[v]]; v = uf[v]
            return v
        tree = []; chords = []
        for e in self.blocks[b]:
            _,u,v,_,_ = self.edges[e]; a,c = find(u),find(v)
            if a == c:
                chords.append(e)
            else:
                uf[a] = c; tree.append(e)
        if len(chords) != len(self.blocks[b])-len(self.vertices[b])+1:
            raise AssertionError('wrong block cycle rank')
        adj = {v:[] for v in self.vertices[b]}
        for e in tree:
            _,u,v,_,_ = self.edges[e]
            adj[u].append((v,e)); adj[v].append((u,e))
        order = [root]; pa = {root:-1}; pe = {}
        for v in order:
            for w,e in adj[v]:
                if w != pa[v]:
                    pa[w] = v; pe[w] = e; order.append(w)
        return root,order,pe,pa,chords

    def _p(self, e, v):
        _,u,w,pu,pw = self.edges[e]
        if v == u:
            return pu
        if v == w:
            return pw
        raise AssertionError('edge endpoint mismatch')

    def feasible(self, T):
        """Return a concrete schedule with makespan <= T, or None exactly if infeasible."""
        T = _time(T)
        nv = len(self.labels)
        msg = [None] * len(self.incidence)
        chosen = [None] * len(self.blocks)
        for x in reversed(self.order):
            if x < nv:
                z = self.base[x]
                for y in self.incidence[x]:
                    if self.parent[y] == x:
                        if msg[y] is None:
                            z = None; break
                        z += msg[y]
                msg[x] = z
                if self.parent[x] == -1 and (z is None or z > T):
                    return None
            else:
                b = x-nv
                root,order,pe,pa,chords = self.plans[b]
                if any(msg[v] is None for v in order if v != root):
                    continue
                best = None; best_assignment = None
                for bits in range(1 << len(chords)):
                    load = {v:(F(0) if v == root else msg[v]) for v in order}
                    assign = {}
                    for j,e in enumerate(chords):
                        _,u,v,_,_ = self.edges[e]
                        w = v if bits & (1 << j) else u
                        assign[e] = w; load[w] += self._p(e,w)
                    failed = False
                    for v in reversed(order[1:]):
                        if load[v] > T:
                            failed = True; break
                        p,e = pa[v],pe[v]
                        if load[v] + self._p(e,v) <= T:
                            assign[e] = v
                        else:
                            assign[e] = p; load[p] += self._p(e,p)
                    if not failed and (best is None or load[root] < best):
                        best = load[root]; best_assignment = assign
                msg[x] = best; chosen[b] = best_assignment
        result = [None] * len(self.jobs)
        for j,v in self.fixed.items():
            result[j] = v
        for assignment in chosen:
            if assignment is None:
                raise AssertionError('feasible root with infeasible descendant block')
            for e,v in assignment.items():
                j = self.edges[e][0]; result[j] = self.labels[v]
        if any(v is None for v in result):
            raise AssertionError('missing job in schedule')
        # Independent reconstruction check; not used to decide feasibility.
        if self.makespan(result) > T:
            raise AssertionError('reconstructed witness exceeds threshold')
        return result

    def makespan(self, schedule):
        if len(schedule) != len(self.jobs):
            raise ValueError('wrong schedule length')
        load = {}
        for v,opts in zip(schedule,self.jobs):
            options = dict(opts)
            if type(v) is not int or v not in options:
                raise ValueError('schedule uses an unavailable machine')
            load[v] = load.get(v,F(0)) + options[v]
        return max(load.values(),default=F(0))

    def solve(self):
        """Return exact (OPT, schedule), using binary search on a rational grid."""
        if not self.jobs:
            return F(0), []
        D = 1
        for opts in self.jobs:
            for v,p in opts:
                D = lcm(D,p.denominator)
        arbitrary = [opts[0][0] for opts in self.jobs]
        U = self.makespan(arbitrary)
        bound = D*U
        if bound.denominator != 1:
            raise AssertionError('common denominator missed a processing time')
        lo,hi = 0,int(bound)
        while lo < hi:
            mid = (lo+hi)//2
            if self.feasible(F(mid,D)) is None:
                lo = mid+1
            else:
                hi = mid
        opt = F(lo,D); schedule = self.feasible(opt)
        if schedule is None or self.makespan(schedule) != opt:
            raise AssertionError('exact optimum reconstruction failed')
        return opt,schedule


def solve_matrix(matrix):
    """Explicit m-by-n matrix; None denotes infinity; return exact OPT and n machine indices."""
    rows = [list(row) for row in matrix]
    if not rows or any(len(row) != len(rows[0]) for row in rows):
        raise ValueError('matrix must have >=1 rows of equal width')
    jobs = [[(i,rows[i][j]) for i in range(len(rows)) if rows[i][j] is not None]
            for j in range(len(rows[0]))]
    return BlockRankSolver(jobs,machine_count=len(rows)).solve()
