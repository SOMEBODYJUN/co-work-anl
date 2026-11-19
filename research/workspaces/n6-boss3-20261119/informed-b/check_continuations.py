"""Using the one explicit integer menu, enumerate true last/fifth/fourth continuations."""
import csv
from fractions import Fraction as F
from functools import lru_cache
import hashlib
from itertools import product
import json
from audit_candidate import HERE, PREV, LABELS, PATTERN

A=range(len(LABELS))
SCALE=60
OPT=0
MENU=json.loads((HERE/"integer-menu.json").read_text())
OPT=MENU["OPT6"]
ATOMS=[(tuple(LABELS.index(k) for k in r["labels"]),r["end_exclusive"]-r["first"]) for r in MENU["client_intervals"]]
COV=[0]*len(LABELS)
for r in MENU["client_intervals"]:
    mask=((1<<(r["end_exclusive"]-r["first"]))-1)<<r["first"]
    for k in r["labels"]:
        COV[LABELS.index(k)] |= mask


@lru_cache(None)
def terminal(z):
    payoff,welfare=[0]*len(LABELS),0
    for members,n in ATOMS:
        load=sum(z[a] for a in members)
        if load:
            welfare+=n
            for a in members:
                payoff[a] += (SCALE//load)*n
    # Independently compute each rational share from literal unit-client bitsets.
    level=[(1<<MENU["clients"])-1]+[0]*6
    for a,n in enumerate(z):
        for _ in range(n):
            for k in range(6,0,-1):
                level[k]=(level[k]&~COV[a]) | (level[k-1]&COV[a])
            level[0] &= ~COV[a]
    assert welfare==MENU["clients"]-level[0].bit_count()
    for a,mask in enumerate(COV):
        assert payoff[a] == sum((SCALE//d)*(mask&level[d]).bit_count() for d in range(1,7))
    assert sum(n*p for n,p in zip(z,payoff))==SCALE*welfare
    return tuple(payoff),welfare


def counts(h):
    return tuple(h.count(a) for a in A)


def fmt(v):
    return str(F(v,SCALE))


def names(h):
    return [LABELS[a] for a in h]


def branches():
    reports=[]
    with (HERE/"terminal-comparisons.csv").open("w",newline="") as file:
        out=csv.writer(file,lineterminator="\n")
        out.writerow(["j","fourth","fifth","sixth","u3","u4","u5","u6","W","last_BR","fifth_SPE","fourth_SPE"])
        for j,row in enumerate(PATTERN):
            e0,a0,y0=(a+6 for a in row)
            p=(4,5,j)
            fixed=p+(e0,a0,y0)
            base,basew=terminal(counts(fixed))
            pairs,tables,last_br,fourth_low,fifth_report={},{},{},{},{}
            for e in A:
                low={}
                for a in A:
                    table={y:terminal(counts(p+(e,a,y))) for y in A}
                    best=max(v[y] for y,(v,w) in table.items())
                    br={y:v[a] for y,(v,w) in table.items() if v[y]==best}
                    tables[e,a],last_br[e,a]=table,br
                    low[a]=min(br.values())
                    if e==e0:
                        fifth_report[LABELS[a]]={"BR6_u5":{LABELS[y]:fmt(v) for y,v in br.items()},
                            "best_u6":fmt(best),"min_u5":fmt(low[a]),"gain_over_candidate":fmt(low[a]-base[a0])}
                threshold=max(low.values())
                pairs[e] = [(a,y) for a in A for y,v in last_br[e,a].items() if v>=threshold]
                fourth_low[e]=min(tables[e,a][y][0][e] for a,y in pairs[e])
            triples=[]
            for e,a,y in product(A,repeat=3):
                v,w=tables[e,a][y]
                last=y in last_br[e,a]
                fifth=(a,y) in pairs[e]
                fourth=fifth and v[e]>=max(fourth_low.values())
                if fourth:
                    triples.append((e,a,y))
                out.writerow([LABELS[j],LABELS[e],LABELS[a],LABELS[y],fmt(v[j]),fmt(v[e]),fmt(v[a]),fmt(v[y]),
                              w,int(last),int(fifth),int(fourth)])
            reports.append({"j":LABELS[j],"fixed_leaf":names(fixed),"payoffs":[fmt(base[a]) for a in fixed],
                "W":basew,"W_over_OPT6":str(F(basew,OPT)),"specified_last_BR":y0 in last_br[e0,a0],
                "specified_last_two_SPE":(a0,y0) in pairs[e0],
                "same_fifth_action_any_BR":any(a==a0 for a,y in pairs[e0]),
                "fifth_queries":fifth_report,"fifth_floor":str(max(F(x["min_u5"]) for x in fifth_report.values())),
                "fourth_lows":{LABELS[e]:fmt(low) for e,low in fourth_low.items()},
                "fourth_floor":fmt(max(fourth_low.values())),
                "same_fourth_action_any_true_tail":any(e==e0 for e,a,y in triples),
                "specified_triple_SPE":(e0,a0,y0) in triples,
                "true_ordered_triples":[{"actions":names(t),"u3":fmt(terminal(counts(p+t))[0][j]),
                    "W":terminal(counts(p+t))[1]} for t in triples]})
    return reports


def prefix_and_root(reports):
    """Reuse the exact, set-valued history recurrence from the prior run."""
    import importlib.util
    source=PREV.parent/"informed-b"/"exact_tail.py"
    assert hashlib.sha256(source.read_bytes()).hexdigest()=="1b51b11d1dd5aadd0c523dbad4504690e8fd25b8fda2d6b868f42ab214efe200"
    spec=importlib.util.spec_from_file_location("prior_exact_tail",source)
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    class Solver(mod.Solver):
        def __init__(self):
            self.A=len(LABELS)
            self.branches={}
            self.state_evaluations=0

        terminal=staticmethod(terminal)

    sol=Solver()
    for j,b in enumerate(reports):
        expected={counts((4,5,j)+tuple(LABELS.index(a) for a in t["actions"])) for t in b["true_ordered_triples"]}
        assert expected==sol.E(counts((4,5,j)))
        assert sol.branches[counts((4,5,j))][0]==SCALE*F(b["fourth_floor"])

    def sample_path(q, z, first=None):
        if sum(q)==6:
            return ()
        threshold,_=sol.branches[q]
        for a in (A if first is None else (first,)):
            child=sol.child(q,a)
            if z in sol.E(child) and terminal(z)[0][a]>=threshold:
                return (a,)+sample_path(child,z)
        raise AssertionError((q,z))

    result={}
    for key,p in (("two_anchor_prefix",(4,5)),("root",())):
        q=counts(p)
        feasible=sol.E(q)
        v,a,z=sol.current_worst(q)
        path=p+sample_path(q,z,first=a)
        assert counts(path)==z
        result[key]={"num_reachable_terminal_count_vectors":len(feasible),
            "all_terminal_multisets":[{"actions":names([i for i,n in enumerate(y) for _ in range(n)]),
                "W":terminal(y)[1]} for y in sorted(feasible)],
            "min_W":min(terminal(y)[1] for y in feasible),
            "max_W":max(terminal(y)[1] for y in feasible),
            "min_current_payoff":fmt(v),"witness_leaf":names(path),
            "witness_payoffs":[fmt(terminal(z)[0][i]) for i in path],
            "witness_W":terminal(z)[1],"witness_W_over_OPT6":str(F(terminal(z)[1],OPT))}
    result["evaluated_count_states"]=sol.state_evaluations
    result["evaluated_terminal_multisets"]=terminal.cache_info().currsize
    return result


if __name__=="__main__":
    r=branches()
    summary={"menu_sha256":hashlib.sha256((HERE/"integer-menu.json").read_bytes()).hexdigest(),
             "OPT6":OPT,"payoff_scale":SCALE,"four_fixed_branches":r}
    summary.update(prefix_and_root(r))
    (HERE/"continuation-audit.json").write_text(json.dumps(summary,indent=2)+"\n")
    print([{k:x[k] for k in ("j","payoffs","W","W_over_OPT6","specified_last_BR","specified_last_two_SPE",
            "same_fourth_action_any_true_tail","fourth_floor")} for x in r])
    for k in ("two_anchor_prefix","root"):
        print(k,{a:b for a,b in summary[k].items() if a!="all_terminal_multisets"})
