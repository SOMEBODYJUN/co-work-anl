#!/usr/bin/env python3
"""Write compact human tables and exact old-zero-anchor witnesses."""
from pathlib import Path
from fractions import Fraction as F
import json

P=Path(__file__).resolve().parent


def write(name,text):
    (P/name).write_text(text.rstrip()+"\n",encoding="utf-8")


def main():
    assert not (P/"freeze_manifest.json").exists(),"Frozen package: replay in a separate copy."
    slices=json.loads((P/"exact_envelopes.json").read_text())["slices"]
    lines=["# 完整公共断点及真实条件事件","",
           "所有断点都保闭端点弱态；同一 mode、δ 的三个 s 有相同断点。完整尾表在 exact_envelopes.json。","",
           "| mode | δ | s | 全部 h 断点 |","|---|---:|---:|---|"]
    params=["# 全部预算参数","",
            "β3(h)=B−h；S(h)=S0−h；真实末帽和末 BR 权均为1。","",
            "| slice | a | τ4 | τ5 | B | β4 | β5 | S0 |","|---|---:|---:|---:|---:|---:|---:|---:|"]
    witnesses=[]
    for sl in slices:
        w=sl["weights_at_zero"]
        lines.append(f"| {sl['mode']} | {sl['delta']} | {sl['s']} | {'，'.join(sl['common_breaks'])} |")
        params.append(f"| {sl['id']} | {w['source_ic']} | {w['tau'][1]} | {w['tau'][2]} | {w['beta3_original']} | {w['beta'][1]} | {w['beta'][2]} | {w['S']} |")
        c=next(c for c in sl["conditions"] if c["p"]==0 and c["t"]==0 and c["n"]==1)
        tail=next(r for r in c["tails"] if r["tail"]=="1000")
        h=F(w["beta3_original"])/2
        anchor=F(w["q0"])*(1+F(w["tau"][1])/3+F(w["tau"][2])/2)
        actual=F(tail["intercept"])+F(tail["slope"])*h
        assert actual-anchor==-h
        witnesses.append(dict(slice_id=sl["id"],delta=sl["delta"],s=sl["s"],h=str(h),
                              p=0,t=0,q=w["q0"],tail="1000",old_zero_anchor=str(anchor),
                              actual_COST=str(actual),actual_minus_old_anchor=str(-h),
                              interpretation="A local COST violation of the old anchor, not an SPE counterexample."))
    lines += ["", "## 全部内部事件", "",
              "- 纯族唯一内断点 H6：p=1、t=0、o=1 的最小尾由0000变为1000，断点两尾都保留。",
              "- ordered 第一内断点 H2：p=1、t=0、d=2 的最小尾由0000变为1000；它不改变最终G，仍保留端点行。",
              "- ordered 第二内断点 H1：p=1、t=0、d=1 的最小尾由0000变为1000；它改变p=1的G仿射式。",
              "- h=0：p=t=0、q=q0 的0000、0001、0010、0100与1000平局，前四态仅在该点达到。",
              "- h=B：两个p的t=q=0条件新增1000弱最优；该尾在这些条件只于此端点达到。",
              "- 全部t=1物理条件的弱最优尾均含r3=1，随h共同平移−h；其各自弱态名单完整保存在机器附件。",
              "- 全部六重数的两两仿射交点为空，没有额外重数细分点。"]
    write("breakpoint_table.md","\n".join(lines))
    write("parameter_table.md","\n".join(params))
    write("old_zero_anchor_failures.json",json.dumps(witnesses,ensure_ascii=False,indent=2))
    print("Wrote compact breakpoint/parameter tables and 12 exact old-anchor failures.")


if __name__=="__main__":
    main()
