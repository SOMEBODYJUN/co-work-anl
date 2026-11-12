#!/usr/bin/env python3
"""Exact nonnegative identities for the 12 old ordered epsilon nonvertices.

Keeps every new endpoint row.  This is parameter-family containment, not an
optimization, a candidate-point test, or a general cone-redundancy decision.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import traceback

P=Path(__file__).resolve().parent


def save(name,obj):
    def ser(x):
        if isinstance(x,F): return str(x)
        if isinstance(x,dict): return {str(k):ser(v) for k,v in x.items()}
        if isinstance(x,(list,tuple)): return [ser(v) for v in x]
        return x
    (P/name).write_text(json.dumps(ser(obj),ensure_ascii=False,indent=2)+"\n",encoding="utf-8")


def level(delta,k):
    return (F(0),F(63143,2073600)+delta/300,
            F(90577,1036800)+delta/100,F(59833,414720)+delta/60)[k]


def main():
    assert not (P/"freeze_manifest.json").exists(),"Frozen: replay separately."
    binding=json.loads((P/"source_binding.json").read_text())
    info=binding["previous_families"]["cap3_186"]
    source=Path(info["path"])
    assert hashlib.sha256(source.read_bytes()).hexdigest()==info["sha256"]
    old=json.loads(source.read_text())["rows"]
    new=json.loads((P/"exact_family.json").read_text())["rows"]
    literal={tuple(F(x) for x in r["a"]):r for r in new}
    identities=[]
    nontrivial=0
    metadata_checks=0
    for pos,row in enumerate(old):
        vector=tuple(F(x) for x in row["a"])
        if vector in literal:
            support=[(F(1),literal[vector])]
        else:
            assert row["mode"]=="ordered" and F(row["delta"])==F(1,144)
            delta,h,s=F(row["delta"]),F(row["h"]),F(row["s"])
            k=next(k for k in range(4) if level(delta,k)==h)
            candidates=[r for r in new if r["mode"]=="ordered" and F(r["s"])==s]
            values=sorted({F(r["delta"]) for r in candidates})
            lo=max(d for d in values if d<delta)
            hi=min(d for d in values if d>delta)
            left=next(r for r in candidates if F(r["delta"])==lo and F(r["h"])==level(lo,k))
            right=next(r for r in candidates if F(r["delta"])==hi and F(r["h"])==level(hi,k))
            support=[((hi-delta)/(hi-lo),left),((delta-lo)/(hi-lo),right)]
            nontrivial+=1
        assert all(w>=0 for w,r in support) and sum(w for w,r in support)==1
        actual=tuple(sum(w*F(r["a"][i]) for w,r in support) for i in range(513))
        assert actual==vector
        # Along each of these parameter edges all true weights interpolate too.
        for field in ("raw_K","K","free_EC"):
            assert F(row[field])==sum(w*F(r[field]) for w,r in support)
            metadata_checks+=1
        assert F(row["real_budget"]["source_IC"])==sum(w*F(r["real_budget"]["source_IC"]) for w,r in support)
        metadata_checks+=1
        for field in ("tau","beta_original","beta_actual"):
            for j in ("3","4","5"):
                assert F(row[field][j])==sum(w*F(r[field][j]) for w,r in support)
                metadata_checks+=1
        identities.append(dict(old_position=pos,old_row_id=row["id"],old_delta=row["delta"],old_h=row["h"],
                               old_s=row["s"],mode=row["mode"],support=[dict(weight=w,new_row_id=r["id"],
                               source_vertex_id=r["source_vertex_id"],vertex_key=r["vertex_key"]) for w,r in support],
                               full_columns_checked=513,true_budget_weights_checked=True,status="PASS"))
    assert len(identities)==186 and nontrivial==12
    save("old186_containment.json",dict(status="PASS",old_row_count=186,literal_identities=174,
         two_vertex_positive_identities=12,coefficient_identities_checked=186*513,
         metadata_identities_checked=metadata_checks,all_new_585_rows_retained=True,identities=identities,
         meaning="The old 186 parameter family is contained in the new 585 endpoint family. This does not classify general-T or ordered rows against all other inequalities."))
    print(json.dumps(dict(status="PASS",literal=174,two_vertex=12,column_identities=186*513,
                          metadata_identities=metadata_checks),ensure_ascii=False,indent=2))


if __name__=="__main__":
    try: main()
    except BaseException as exc:
        file=P/"failure_log.json"
        entries=json.loads(file.read_text()) if file.exists() else []
        entries.append(dict(stage="check_old186_containment",type=type(exc).__name__,message=str(exc),traceback=traceback.format_exc()))
        save("failure_log.json",entries)
        raise
