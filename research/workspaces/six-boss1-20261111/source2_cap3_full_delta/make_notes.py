#!/usr/bin/env python3
"""Compact row recipes and exact four-corner identities; no row matrix."""
from fractions import Fraction as F
from pathlib import Path
import json

P=Path(__file__).resolve().parent
b=F(5977,6912)
v=F(43,48)


def save(name,obj):
    def ser(x):
        if isinstance(x,F): return str(x)
        if isinstance(x,dict): return {str(k):ser(vv) for k,vv in x.items()}
        if isinstance(x,(list,tuple)): return [ser(vv) for vv in x]
        return x
    (P/name).write_text(json.dumps(ser(obj),ensure_ascii=False,indent=2)+"\n",encoding="utf-8")


def ev(a,p): return a[0]+a[1]*p[0]+a[2]*p[1]


def main():
    assert not (P/"freeze_manifest.json").exists(),"Frozen: replay separately."
    pack=json.loads((P/"exact_envelopes_2d.json").read_text())
    recipes=[]
    interpolation=[]
    local_checks=0
    for sl in pack["slices"]:
        q,s=F(sl["q0"]),F(sl["s"])
        a=[25+b+v-s,F(0),F(0)]
        tau={"3":[F(0),F(0),F(0)],"4":[b,F(-1),F(0)],"5":[v,F(1),F(0)]}
        caps={"3":[q/2+q*b/12+q*v/6,q/12,F(-1)],
              "4":[q/2+b+q*v/6,F(-1)+q/6,F(0)],
              "5":[q/2+v,F(1),F(0)]}
        S=[1+sum(c[0] for c in caps.values()),q/4,F(-1)]
        mu=[S[0]-s/5,S[1],S[2]]
        recipes.append(dict(slice_id=sl["id"],mode=sl["mode"],s=s,q0=q,
                            source_IC_affine=a,internal_SAFE_affines=tau,intermediate_CAP_affines=caps,
                            terminal_CAP=F(1),terminal_BR=F(1),S_affine=S,
                            C_only_free_EC_affine=mu if sl["mode"]=="pure" else None,
                            C_only_K=s/5 if sl["mode"]=="pure" else None,
                            outer_index_average=F(1,6) if sl["mode"]=="ordered" else None,
                            inner_query_average=q,numerical_divisor=F(25)))
        point_lookup={p["id"]:tuple(F(z) for z in p["point"]) for p in sl["vertices"]}
        for cell in sl["cells"]:
            verts=[point_lookup[i] for i in cell["vertices"]]
            left,right=min(x[0] for x in verts),max(x[0] for x in verts)
            lvals=sorted(h for d,h in verts if d==left)
            rvals=sorted(h for d,h in verts if d==right)
            corners=[(left,lvals[0]),(right,rvals[0]),(right,rvals[1]),(left,lvals[1])]
            lam,eta=F(1,3),F(2,5)
            weights=[(1-lam)*(1-eta),lam*(1-eta),lam*eta,(1-lam)*eta]
            point=tuple(sum(w*c[j] for w,c in zip(weights,corners)) for j in range(2))
            assert point[0]==left+lam*(right-left)
            assert sum(weights)==1 and min(weights)>=0
            for c in sl["conditions"]:
                states=[tuple(F(z) for z in r["affine"]) for r in c["states"]]
                true=min(ev(line,point) for line in states)
                from_corners=sum(w*min(ev(line,corner) for line in states) for w,corner in zip(weights,corners))
                assert true==from_corners
                local_checks+=1
            for budget in [a,S,mu,*tau.values(),*caps.values()]:
                assert ev(budget,point)==sum(w*ev(budget,corner) for w,corner in zip(weights,corners))
            interpolation.append(dict(slice=sl["id"],cell=cell["id"],point=point,corners=corners,
                                      weights=weights,condition_count=len(sl["conditions"]),status="PASS"))
    save("row_recipe.json",dict(schema="source2-cap3-full-delta-row-recipe-v1",matrices_materialized=False,
        affine_order=["constant","delta","h"],customer_bits=[f"a{i}" for i in range(1,7)]+["x","o","c"],
        customer_order="lexicographic, 0 before 1",customer_columns=512,K_column=512,total_columns=513,
        inequality="dot(row.a,coordinate)>=0",prefix="p=a1",actual_u2="a2/(a1+...+a6), zero actual load gives zero",
        legal_targets={**{f"A{i}":i-1 for i in range(1,7)},"X":6,"C":8},
        pure_general=dict(customer="a*actual_u2-min_16_COST(p,t,o/6;delta,h)",K="S(delta,h)",free_EC="0"),
        C_only=dict(customer="a*actual_u2-min_16_COST(p,c,o/6;delta,h)+mu(delta,h)*c",K="s/5",
                    free_EC="mu=S-s/5",equality="E_C=sum_x c_x-K=0; multiplier unrestricted in sign"),
        ordered=dict(customer="a*actual_u2-o*G(p;delta,h)",K="S(delta,h)",free_EC="0",
                     G="min_{d=1..6} f_d=f_1, after computing physical condition minima",
                     physical_conditions="t=0,d=0..5; t=1,d=1..6; q=(d-t)/5"),
        parameters=recipes,finite_generation=dict(common_cells=150,source_vertex_records=225,
            prospective_general_rows=360,prospective_C_only_rows=45,prospective_ordered_rows=180,
            prospective_total_rows=585,all_rows_unmaterialized=True,
            weights="lambda=(delta-l)/(u-l), eta=(h-L(delta))/(U(delta)-L(delta)); corner weights (1-lambda)(1-eta), lambda(1-eta), lambda*eta, (1-lambda)*eta",
            C_only_status="entire two-dimensional family paid by its 15 true bottom-edge endpoint rows plus nonnegative customer masses")))
    save("four_corner_interpolation_checks.json",dict(status="PASS",local_condition_identities=local_checks,cells=interpolation))
    summary=json.loads((P/"derivation_summary.json").read_text())
    lines=["# 二维公共边界与顶点目录","",
           "所有边界来自完整16态弱最优域。h方向边界见proof式(9)；下表δ竖线与其交点构成完整公共复形。","",
           "| 来源 | cell | 边 | 顶点 | 全部δ切分点 |","|---|---:|---:|---:|---|"]
    for sl in summary["per_slice"]:
        lines.append(f"| {sl['id']} | {sl['cells']} | {sl['edges']} | {sl['vertices']} | {'，'.join(sl['vertical_cuts'])} |")
    lines += ["", "## 只在角点出现的九份弱态", "",
              "每个ordered来源在(δ,h)=(5977/6912,0)都有以下三份0100弱最优记录：p0/t0/d2，p1/t0/d3，p1/t0/d4。它们不在任何二维开cell达到，已单独保留。", "",
              "其余44个一维状态域和167个二维状态域的全部闭约束、顶点以及各face的全部弱态均见exact_envelopes_2d.json与独立重建文件。"]
    (P/"boundary_catalog.md").write_text("\n".join(lines).rstrip()+"\n",encoding="utf-8")
    print(f"Wrote matrix-free row recipes; checked {local_checks} four-corner local identities.")


if __name__=="__main__": main()
