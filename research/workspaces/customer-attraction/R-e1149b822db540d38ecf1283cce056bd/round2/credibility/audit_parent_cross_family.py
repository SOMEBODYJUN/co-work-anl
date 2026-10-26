"""Independent added-row/feature/routing audit, without re-auditing old 557 rows."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import hashlib
import importlib.util
import json
import sys
import numpy as np

HERE = Path(__file__).resolve().parent
PARENT = HERE.parent / "parent/cross_family_pricing.py"
spec = importlib.util.spec_from_file_location("parent_cross_family_review_target", PARENT)
target = importlib.util.module_from_spec(spec)
spec.loader.exec_module(target)

TAGS = ("AB", "AE", "Sbranch")
QUERY = {"AB": "XY", "AE": "XY", "Sbranch": "UVW"}
KEYS = {"AB": "AB_hist", "AE": "AE_hist", "Sbranch": "second_hist"}
SPECS = [(s,t,q) for s in TAGS for t in TAGS for q in QUERY[t]]
NAMES = ["XC:"+":".join(s) for s in SPECS]
TYPES = {3: list(product((0,1),repeat=3)), 4: list(product((0,1),repeat=4))}


def pfx(bits, tag):
    return bits[0]+(bits[1] if tag=="AB" else bits[4] if tag=="AE" else 0)


def explicit_row(atom, source, query_family, query_name):
    """Expand the two histograms into five indexed customer membership records."""
    bits = tuple(map(int, atom["bits"]))
    k = 4 if source=="Sbranch" else 3
    records = [t for n,t in zip(atom[KEYS[source]], TYPES[k]) for _ in range(n)]
    qk = 4 if query_family=="Sbranch" else 3
    qrecords = [t for n,t in zip(atom[KEYS[query_family]], TYPES[qk]) for _ in range(n)]
    qpos = QUERY[query_family].index(query_name)+1
    pref = pfx(bits, source)
    remaining = k-1
    value = F(0)
    for t in records:
        actual = F(t[1], pref+sum(t)) if t[1] else F(0)
        for z in qrecords:
            value += actual-F(z[qpos], pref+t[0]+remaining)
    return value


def oracle_scores(U, bits, routing):
    """Independent exact integer coefficient arrays, each in the legacy 120 grid."""
    output = {}
    for fam in TAGS:
        k = 4 if fam=="Sbranch" else 3
        H = np.asarray(U.hist[k], dtype=np.int64)
        ty = np.asarray(TYPES[k], dtype=np.int64)
        d = H@ty[:,0]
        ownpref = pfx(bits,fam)
        scaled_profit = H@np.asarray([600*t[1]//(ownpref+sum(t)) if t[1] else 0 for t in TYPES[k]], dtype=np.int64)
        score = np.zeros(len(H), dtype=np.int64)
        for (source, query_family, query_name), weight in routing:
            if fam==source:
                score += weight*scaled_profit
            if fam==query_family:
                qpos = QUERY[fam].index(query_name)+1
                count = H@ty[:,qpos]
                pref = pfx(bits,source)
                rem = 3 if source=="Sbranch" else 2
                table = np.asarray([int(120*(F(dd,pref+rem+1)+F(5-dd,pref+rem))) for dd in range(6)],dtype=np.int64)
                score -= weight*count*table[d]
        output[fam] = score
    return output


def dispatched(routing):
    weights = {f: [] for f in TAGS}
    for (s,t,q),v in routing:
        name = "XC:"+":".join((s,t,q))
        weights[s].append((name,v))
        if t!=s:
            weights[t].append((name,v))
    return weights


def feature_vector(U,bits,fam,weights):
    key,const,vec,E,H = U.family_score(bits,fam,weights,integer=True)
    k = 4 if fam=="Sbranch" else 3
    value = np.zeros(len(U.hist[k]),dtype=np.int64)
    assert const==0 and not np.any(E) and not np.any(H)
    for v,a in vec:
        value += int(v)*np.asarray(a,dtype=np.int64)
    return key,value


def run():
    assert target.SPECS==SPECS and target.NAMES==NAMES and len(NAMES)==21
    U = target.Universe()
    warm = target.SOURCE/"root_shared_max_copy_cg.json"
    data = json.loads(warm.read_text())
    row_cases = 0
    for atom,w in zip(data["atoms"],data["primal_float"]):
        if w<=0:
            continue
        actual = target.row_values(atom)
        for name,(s,t,q) in zip(NAMES,SPECS):
            assert actual[name]==explicit_row(atom,s,t,q),(name,atom)
            row_cases += 1
    patterns=[]
    for a,b,e in product((0,1),repeat=3):
        bits = [0]*10
        bits[0],bits[1],bits[4] = a,b,e
        patterns.append(tuple(bits))
    compared = 0
    # Every histogram in every family, every relevant fixed-prefix pattern,
    # and every one-hot new row; hence this includes all seven same-family rows.
    for bits in patterns:
        for triple in SPECS:
            routing=[(triple,1)]
            routed=dispatched(routing)
            expected=oracle_scores(U,bits,routing)
            for fam in TAGS:
                key,score=feature_vector(U,bits,fam,routed[fam])
                assert np.array_equal(score,expected[fam]),(bits,triple,fam)
                compared += len(score)
    # Nonzero mixed weights exercise simultaneous positive and negative terms,
    # and compare all reused cache keys against the complete score vector.
    routing=list(zip(SPECS,range(1,22)))
    routed=dispatched(routing)
    hashes={}
    collisions=0
    independent_min=None
    for bits in patterns:
        expected=oracle_scores(U,bits,routing)
        family_max=[]
        for fam in TAGS:
            key,score=feature_vector(U,bits,fam,routed[fam])
            assert np.array_equal(score,expected[fam])
            digest=hashlib.sha256(score.tobytes()).hexdigest()
            if key in hashes:
                assert hashes[key]==digest,(bits,fam,"unsafe cache alias")
                collisions+=1
            hashes[key]=digest
            k=4 if fam=="Sbranch" else 3
            family_max.append([int(max(score[ids])) for ids in U.ids[k]])
        for dd in range(6):
            rho=-sum(vals[dd] for vals in family_max)
            independent_min=rho if independent_min is None else min(independent_min,rho)
    lam=np.zeros(len(U.names),dtype=np.int64)
    for name,weight in zip(NAMES,range(1,22)):
        lam[U.names.index(name)]=weight
    got,_,contexts=U.price(lam,0,batch=1,integer="object")
    assert got==independent_min,(got,independent_min)
    report={
        "target":str(PARENT.relative_to(target.ROOT)),
        "target_sha256":hashlib.sha256(PARENT.read_bytes()).hexdigest(),
        "scope":"Only the 21 added CFM rows, their separable feature contributions, routing, and XC-only pricing. No re-audit of old 557 rows or certified welfare bound.",
        "row_values_expanded_25_pair_comparisons":row_cases,
        "one_hot_feature_integer_coordinates_checked":compared,
        "relevant_fixed_prefix_patterns":len(patterns),
        "same_source_target_rows":7,
        "mixed_weight_cache_contexts":len(hashes),
        "reused_cache_contexts_checked":collisions,
        "xc_only_exact_pricing_minimum":str(got),
        "xc_only_pricing_contexts":contexts,
        "status":"passed; author of original CFM row independently audited the parent's implementation, not blind theorem review",
    }
    (HERE/"audit_parent_cross_family.json").write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps(report,indent=2))


if __name__=="__main__":
    run()
