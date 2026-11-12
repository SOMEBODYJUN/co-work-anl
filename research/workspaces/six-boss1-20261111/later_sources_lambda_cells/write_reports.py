#!/usr/bin/env python3
"""Render complete exact geometry tables from already verified local JSON."""
from pathlib import Path
from fractions import Fraction
from collections import Counter
import json

HERE=Path(__file__).resolve().parent


def equation(form,names):
    pieces=[]
    for k,v in enumerate(form):
        if not v:continue
        text=str(abs(v)) if k==0 else ("" if abs(v)==1 else str(abs(v))+" ")+names[k-1]
        pieces.append(("− " if v<0 else "+ ")+text)
    joined=" ".join(pieces) if pieces else "0"
    if joined.startswith("+ "):joined=joined[2:]
    return joined+" ≥ 0"


def main():
    data=json.loads((HERE/"parameter_domains.json").read_text())
    check=json.loads((HERE/"literal_checker_output.json").read_text())
    assert check["status"]=="PASS"
    endpoints=["# 全部110次闭窗口顶点出现","","坐标顺序为各真实内部源的τ，最后为λ。所有窗口重复与旧参数均原样保留。","",
               "| cell | vertex id | coordinate order | exact coordinates | old parameter |","|---|---|---|---|---|"]
    geometry=["# 每个闭窗口的完整几何","","24个域、96个不可约facet、110次顶点出现。各域由全部真实状态定义；独立真边裁切已逐域PASS。","",
              "| cell | dimension | raw states | raw constraints | primitive groups | facets | vertices | lambda layers |","|---|---:|---:|---:|---:|---:|---:|---|"]
    denominator=[]
    for c in data["cells"]:
        layers=Counter(v["lambda_value"] for v in c["vertices"])
        layertext=", ".join(f"{l}:{layers[l]}" for l in sorted(layers,key=Fraction))
        geometry.append(f"| {c['id']} | {c['dimension']} | {c['raw_real_state_count']} | {c['raw_constraint_count']} | {c['primitive_halfspace_count']} | {c['facet_count']} | {c['vertex_count']} | {layertext} |")
        for v in c["vertices"]:
            endpoints.append(f"| {c['id']} | {v['id']} | ({', '.join(c['coordinate_order'])}) | ({', '.join(v['coordinates'])}) | {'yes' if v['old_16_25_parameter'] else 'no'} |")
        lo,hi=map(Fraction,c["window"]);mid=(lo+hi)/2
        for p in range(c["source"]):
            D=p+7-c["source"];cut=(D-1)**2
            interior=int(mid>cut)
            ends=[]
            for lam in (lo,hi):
                choices=[0,1] if lam==cut else [int(lam>cut)]
                ends.append(dict(lambda_value=str(lam),all_anchor_terminal_choices=choices,
                                 actual_source_denominators=[D-1+z for z in choices],all_query_denominators=[D for z in choices]))
            denominator.append(dict(cell=c["id"],source=c["source"],p=p,D=D,switch_lambda=str(cut),
                                    interior_anchor_terminal=interior,interior_source_actual_denominator=D-1+interior,
                                    terminal_query_denominator=D,each_internal_query_denominator=D,closed_endpoints=ends))
    for c in data["cells"]:
        geometry.extend(["",f"## {c['id']}","",f"严格内点：`({', '.join(c['strict_interior_point'])})`。坐标：`({', '.join(c['coordinate_order'])})`。","",
                         "| facet id | exact primitive inequality | support vertices | affine rank | raw source ids |","|---|---|---:|---:|---|"])
        for f in c["facets"]:
            geometry.append(f"| {f['id']} | {equation(f['primitive_form'],c['coordinate_order'])} | {len(f['support_vertex_ids'])} | {f['support_affine_rank']} | {', '.join(f['raw_ids'])} |")
    (HERE/"endpoint_table.md").write_text("\n".join(endpoints)+"\n")
    (HERE/"geometry.md").write_text("\n".join(geometry)+"\n")
    (HERE/"anchor_denominator_contract.json").write_text(json.dumps(denominator,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps(dict(status="PASS",complete_vertex_occurrences=sum(c["vertex_count"] for c in data["cells"]),complete_facet_occurrences=sum(c["facet_count"] for c in data["cells"]),denominator_contexts=len(denominator))))


if __name__=="__main__":main()
