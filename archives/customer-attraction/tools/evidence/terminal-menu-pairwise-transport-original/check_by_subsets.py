"""Independent finite check: literal subset assignment, no original import/sort.

Read every frozen report field and all input atoms.  Enumerate every assignment
of a binary target menu within the source's shared T groups for each atom/pair.
This verifies extrema of the stated relaxation, not a complete SPE or a global
simultaneous customer/menu coupling.
"""
from fractions import Fraction as F
from itertools import combinations, product
from pathlib import Path
import hashlib
import json
import time

HERE = Path(__file__).resolve().parent
INPUT = HERE / "original/next_credible/enhanced_2396_exact_obstruction.json"
FROZEN = HERE / "original/round3_indexed/transport_bounds.json"

def read_input_atoms():
    data = json.loads(INPUT.read_text())
    atoms = data["atom_masses"]
    assert len(atoms) == data["positive_atoms"] == 38
    assert len(data["point"]) == data["atoms"] == 65
    assert [F(x) for x in data["point"] if F(x) > 0] == [F(x["mass"]) for x in atoms]
    assert len({json.dumps({k:a[k] for k in ("bits", "AB_hist", "AE_hist", "second_hist", "menus_lh")}, sort_keys=True) for a in atoms}) == 38
    for a in atoms:
        assert len(a["bits"]) == 10 and set(a["bits"]) <= {"0", "1"}
        assert F(a["mass"]) > 0
        ds = []
        for key, width in [("AB_hist", 3), ("AE_hist", 3), ("second_hist", 4)]:
            hist = a[key]
            assert len(hist) == 2**width and sum(hist) == 5
            assert all(isinstance(n, int) and n >= 0 for n in hist)
            ds.append(sum(n * bits[0] for n,bits in zip(hist, product((0,1), repeat=width))))
        assert ds[0] == ds[1] == ds[2]
        for ell,h in a["menus_lh"]:
            assert all(isinstance(v,int) for v in (ell,h))
            assert 0 <= h <= ds[0] and 0 <= ell-h <= 5-ds[0]
    return data, atoms

def expand_and_construct(a):
    bits = {c: int(a["bits"][i]) for i,c in enumerate("ABCDEUVWXY")}
    paths = {}
    for name,key,width,bg in [("AB","AB_hist",3,bits["A"]+bits["B"]),
            ("AE","AE_hist",3,bits["A"]+bits["E"]), ("S","second_hist",4,bits["A"])]:
        rows = [w for n,w in zip(a[key],product((0,1),repeat=width)) for _ in range(n)]
        paths[name] = (bg, rows)
    ts = [w[0] for w in paths["AB"][1]]
    d = sum(ts)
    for f, letters in enumerate(["ABC", "AEU", "ABE"]):
        ell,h = a["menus_lh"][f]
        rows = ([(0,1)]*(ell-h)+[(0,0)]*(5-d-ell+h)+[(1,1)]*h+[(1,0)]*(d-h))
        paths["L"+str(f)] = (sum(bits[c] for c in letters), rows)
    sources = {}
    targets = {"T": (0,d)}
    for name,(bg,rows) in paths.items():
        sources[name] = {"t":[w[0] for w in rows],
            "weights":[F(1,bg+sum(w[:-1])+1) for w in rows],
            "U":sum((F(w[-1],bg+sum(w[:-1])+1) for w in rows),F())}
        for j in range(1,len(rows[0])):
            targets[name+str(j)] = tuple(sum(w[j] for w in rows if w[0]==t) for t in (0,1))
    assert len(sources)==6 and len(targets)==11
    return sources, targets, d

def main():
    start=time.perf_counter()
    data, atoms=read_input_atoms()
    report=json.loads(FROZEN.read_text())
    assert set(report)=={"scope","atoms","q","pairs","failures","all"}
    assert report["scope"]=="exact necessary pairwise transportation bounds only; independent couplings for different pairs; not SPE"
    assert (report["atoms"],report["q"],report["pairs"])==(38,5,66)
    totals={}
    atom_rows=[]
    assignment_count=0
    group_subsets=0
    d_counts={}
    for ai,a in enumerate(atoms):
        sources, targets,d=expand_and_construct(a)
        d_counts[d]=d_counts.get(d,0)+1
        for sn,source in sources.items():
            for tn,counts in targets.items():
                options=[]
                for t in (0,1):
                    ids=[i for i in range(5) if source["t"][i]==t]
                    assert 0<=counts[t]<=len(ids)
                    opts=list(combinations(ids,counts[t]))
                    group_subsets+=len(opts)
                    options.append(opts)
                sums=[sum((source["weights"][i] for subset in choice for i in subset),F())
                    for choice in product(*options)]
                assignment_count+=len(sums)
                u=source["U"]; lo=min(sums); hi=max(sums)
                # Literal all 25 index comparisons.  Any target representative
                # works because j is summed independently of source index i.
                target_bits=[0]*5
                for group in (0,1):
                    ids=[i for i,t in enumerate(source["t"]) if t==group]
                    for i in ids[:counts[group]]: target_bits[i]=1
                allrhs=sum((source["weights"][i]*target_bits[j] for i in range(5) for j in range(5)),F())
                key=sn+"->"+tn
                vals={"U":u,"min_diagonal_rhs":lo,"max_diagonal_rhs":hi,"all_pairs_rhs":allrhs}
                acc=totals.setdefault(key,{k:F() for k in vals})
                for k,v in vals.items(): acc[k]+=F(a["mass"])*v
                atom_rows.append({"atom_index":ai,"pair":key,"T_count":d,
                    "target_counts_by_T":counts,"assignments_enumerated":len(sums),
                    **{k:str(v) for k,v in vals.items()}})
    read_fields=0
    failures={}
    summary=[]
    for pair,v in totals.items():
        v["diagonal_best_slack"]=v["U"]-v["min_diagonal_rhs"]
        v["offdiagonal_best_slack"]=4*v["U"]-v["all_pairs_rhs"]+v["max_diagonal_rhs"]
        expected=report["all"][pair]
        assert set(expected)==set(v)
        for field,value in expected.items():
            read_fields+=1
            assert F(value)==v[field], (pair,field)
        if min(v["diagonal_best_slack"],v["offdiagonal_best_slack"])<0:
            failures[pair]={k:str(x) for k,x in v.items()}
        summary.append({"pair":pair,"diag_sign":(v["diagonal_best_slack"]>0)-(v["diagonal_best_slack"]<0),
            "off_sign":(v["offdiagonal_best_slack"]>0)-(v["offdiagonal_best_slack"]<0),
            "fixed_diagonal":v["min_diagonal_rhs"]==v["max_diagonal_rhs"],
            "all_pairs_slack":str(5*v["U"]-v["all_pairs_rhs"])})
    assert set(totals)==set(report["all"]) and len(totals)==66
    assert failures==report["failures"] and set(failures)=={"L2->L11"}
    diagonal=F()
    diagonal_terms=[]
    for ai,a in enumerate(atoms):
        bits=dict(zip("ABCDEUVWXY",map(int,a["bits"])))
        p=sum(bits[c] for c in "ABE")
        ell1,h1=a["menus_lh"][1]; ell2,h2=a["menus_lh"][2]
        coefficient=F(ell2-ell1,p+1)-F(h2-h1,(p+1)*(p+2))
        weighted=F(a["mass"])*coefficient
        diagonal+=weighted
        diagonal_terms.append({"atom_index":ai,"p":p,"coefficient":str(coefficient),"mass":a["mass"],"weighted":str(weighted)})
    assert diagonal==totals["L2->L11"]["diagonal_best_slack"]
    full_nonnegative=sum(F(r["all_pairs_slack"])>=0 for r in summary)
    result={"scope":"all 38 frozen atoms x 66 pair relaxations; exhaustive within-T binary target subsets, not simultaneous coupling or SPE",
        "input_sha256":hashlib.sha256(INPUT.read_bytes()).hexdigest(),"frozen_report_sha256":hashlib.sha256(FROZEN.read_bytes()).hexdigest(),
        "input_top_level_fields_read":list(data),"positive_atoms":len(atoms),"candidate_point_coordinates":len(data["point"]),
        "d_distribution":d_counts,"atom_pair_extrema_checked":len(atom_rows),"group_subsets_enumerated":group_subsets,
        "complete_binary_assignments_enumerated":assignment_count,"exact_report_rational_fields_compared":read_fields,
        "failure_rows":failures,"fixed_diagonal_pairs":sum(r["fixed_diagonal"] for r in summary),
        "nonnegative_all_pairs_sums":full_nonnegative,"pair_summary":summary,
        "selected_diagonal_formula_total":str(diagonal),"selected_diagonal_terms":diagonal_terms,
        "elapsed_seconds":time.perf_counter()-start,"original_imports_or_main_calls":0,"LP_or_SPE_search_runs":0}
    (HERE/"subset-check-result.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n")
    (HERE/"subset-check-atom-pairs.json").write_text(json.dumps(atom_rows,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps({k:v for k,v in result.items() if k not in ("pair_summary","selected_diagonal_terms")},ensure_ascii=False,indent=2))

if __name__=="__main__": main()
