#!/usr/bin/env python3
"""Validate the mathematical hypergraph and generate a standalone HTML viewer."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
KINDS = {"definition", "lemma", "construction", "counterexample",
         "claim", "source", "evidence", "obligation", "rejected", "artifact"}
RELATIONS = {"derives", "attacks", "checks", "implements", "limits"}
TRACKS = {"model", "local", "shared", "heterogeneous", "computation",
          "extensions", "evidence"}
REVIEW_STATES = {
    "source_proof": {"complete", "source_note", "published_lower_plus_sketch", "synthesis", "new_current_work"},
    "current_proof": {"complete", "candidate", "conditional", "depends_on_claims", "direct"},
    "internal_review": {"multiple_audits", "current_exact_audit", "candidate", "self_attack_and_exact_audit"},
    "external_review": {"not_recorded", "completed"},
    "implementation": {"implemented", "partial", "none", "not_applicable", "finite_example", "audit_only"},
}


def require(condition: bool, message: object) -> None:
    if not condition:
        raise ValueError(message)


def validate(data: dict) -> None:
    require(data["version"] == 1, "unsupported graph schema")
    nodes = {node["id"]: node for node in data["nodes"]}
    require(len(nodes) == len(data["nodes"]), "duplicate node ID")
    review = json.loads((HERE / "review_status.json").read_text(encoding="utf-8"))
    require(review["version"] == 1, "unsupported claim-review schema")
    states = {row["id"]: row for row in review["entries"]}
    require(len(states) == len(review["entries"]), "duplicate claim-review ID")
    declared = set()
    table = (HERE / "current/claims.md").read_text(encoding="utf-8").split("## 逻辑使用规则")[0]
    for line in table.splitlines():
        if not line.startswith("| "):
            continue
        cell = line.split("|", 2)[1].strip()
        if cell == "ID" or cell.startswith("---"):
            continue
        pieces = [piece.strip() for piece in cell.split(" / ")]
        for piece in pieces:
            claim_id = piece if piece in nodes else pieces[0].rsplit("-", 1)[0] + "-" + piece
            require(claim_id in nodes, ("unrecognized registered claim", cell))
            declared.add(claim_id)
    require(set(states) == declared,
            ("claim-review ledger must cover exactly the IDs in claims.md",
             sorted(declared - set(states)), sorted(set(states) - declared)))
    require(all(nodes[claim_id]["kind"] in {"claim", "lemma"} for claim_id in declared),
            "a registered claim must be a claim or claim-level lemma in the graph")
    for claim_id, state in states.items():
        require(state["graph_status"] == nodes[claim_id]["status"],
                ("claim status drift", claim_id))
        for field, allowed in REVIEW_STATES.items():
            require(state.get(field) in allowed,
                    ("invalid claim review state", claim_id, field))
    edges = {edge["id"]: edge for edge in data["hyperedges"]}
    require(len(edges) == len(data["hyperedges"]), "duplicate edge ID")
    require(set(data["legend"]) == RELATIONS, "invalid relation legend")
    for node in data["nodes"]:
        require(node["kind"] in KINDS and node["track"] in TRACKS, node["id"])
        require(node["title"] and node["detail"] and node["refs"] and node["status"], node["id"])
        for ref in node["refs"]:
            require((ROOT / ref).is_file(), (node["id"], ref))
    for edge in data["hyperedges"]:
        require(edge["kind"] in RELATIONS and edge["track"] in TRACKS, edge["id"])
        require(edge["premises"] and len(edge["premises"]) == len(set(edge["premises"])), edge["id"])
        require(all(p in nodes for p in edge["premises"]), edge["id"])
        require(edge["conclusion"] in nodes, edge["id"])
        require(edge["conclusion"] not in edge["premises"], edge["id"])
        require(edge["statement"] and edge["refs"] and edge["status"], edge["id"])
        for ref in edge["refs"]:
            require((ROOT / ref).is_file(), (edge["id"], ref))
    require({n["id"] for n in data["nodes"] if n["kind"] == "claim"} <= {
        e["conclusion"] for e in data["hyperedges"]
    }, "claim lacks an incoming hyperedge")
    used = {x for edge in data["hyperedges"] for x in
            [*edge["premises"], edge["conclusion"]]}
    require(used == set(nodes), "unconnected node")


HTML = r'''<!doctype html>
<html lang="zh">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>双设施研究：数学超图</title>
<style>
:root { color-scheme: light; --ink:#17252d; --muted:#52636b; --line:#ccd9dc; --paper:#f5f7f5; --card:#fff; --teal:#146b69; --ochre:#a36c18; --red:#aa4a45; }
* { box-sizing:border-box }
body { margin:0; font:15px/1.5 system-ui,-apple-system,Segoe UI,sans-serif; background:var(--paper); color:var(--ink) }
header { padding:26px max(20px,calc((100vw - 1480px)/2)); background:#143b41; color:#f2f8f6 }
h1 { margin:0; font-size:clamp(1.5rem,3vw,2.3rem); letter-spacing:-.025em }
header p { max-width:900px; margin:9px 0 0; color:#d5e4e2 }
header a { color:#d0e8eb }
.shell { max-width:1480px; margin:auto; padding:20px; display:grid; grid-template-columns:minmax(0,1fr) minmax(270px,340px); gap:18px; align-items:start }
.tools { grid-column:1/-1; display:flex; gap:10px; flex-wrap:wrap; align-items:center }
input,select { border:1px solid #a9bcbf; border-radius:7px; padding:10px 12px; font:inherit; background:white; color:var(--ink) }
button.clear { border:1px solid #a9bcbf; border-radius:7px; padding:10px 12px; font:inherit; background:white; color:var(--ink); cursor:pointer }
input { flex:1 1 250px }
.count { color:var(--muted); margin-left:auto }
.routes { min-width:0; display:grid; gap:11px }
.route { background:var(--card); border:1px solid var(--line); border-left:5px solid var(--teal); padding:14px 16px; border-radius:9px; box-shadow:0 1px 3px #18394210 }
.route[data-kind=attacks] { border-left-color:var(--red) }
.route[data-kind=checks],.route[data-kind=limits] { border-left-color:var(--ochre) }
.route[data-kind=implements] { border-left-color:#556cac }
.meta { display:flex; gap:9px; align-items:center; font-size:12px; text-transform:uppercase; letter-spacing:.08em; color:var(--muted); font-weight:700 }
.relation { display:grid; grid-template-columns:minmax(0,1fr) 34px minmax(150px,32%); align-items:center; gap:8px; margin:13px 0 }
.premises { display:flex; flex-wrap:wrap; gap:5px; padding:8px; border:1px solid var(--line); border-radius:7px; background:#f8faf8; min-height:45px }
.junction { text-align:center; font-size:20px; color:var(--teal); font-weight:700 }
.node { border:1px solid #a6c9c4; color:#124d52; background:#e8f4f1; border-radius:5px; padding:5px 8px; font:inherit; font-size:13px; text-align:left; cursor:pointer }
.node:hover,.node:focus-visible { outline:2px solid var(--teal) }
.node small { display:block; font-size:11px; opacity:.78 }
.target { width:100%; background:#e5f0f3; border-color:#7da6af }
.route[data-kind=attacks] .target { background:#faeae7; border-color:#d1a29d; color:#7c3430 }
.route p { margin:6px 0; }
.refs { font-size:12px; color:var(--muted); overflow-wrap:anywhere }
a { color:#145c76 }
aside { position:sticky; top:16px; background:#fff; border:1px solid var(--line); border-radius:9px; padding:18px; max-height:calc(100vh - 32px); overflow:auto }
aside h2 { margin:0 0 10px; font-size:19px }
aside p { margin:9px 0 }
aside ul { padding-left:20px }
.badge { display:inline-block; padding:2px 7px; border-radius:4px; background:#e9efee; font-size:12px }
.empty { padding:24px; border:1px dashed var(--line); border-radius:9px }
@media(max-width:850px) { .shell { display:block } .tools { margin-bottom:12px } aside { position:static; max-height:none; margin-top:16px } }
@media(max-width:570px) { .relation { grid-template-columns:1fr; gap:3px } .junction { transform:rotate(90deg) } }
</style>
</head>
<body>
<header>
<h1>数学研究超图</h1>
<p>每张关系卡是一条超边：左侧的前提须同时成立，才按中间的关系类型通向右侧结论。红色反驳的是被提出的错误命题；黄色表示有限测试或适用边界。点击节点查看精确作用和原始来源。共享主定理的完整主稿与现行 Markdown 全分支重写均经过内部审读；外部同行评审另记。</p>
<p><a href="../README.md">研究总览</a> · <a href="current/claims.md">现行命题</a> · <a href="graph.json">结构化数据</a></p>
</header>
<div class="shell">
<div class="tools">
<input id="search" type="search" placeholder="搜索数学内容、命题 ID 或来源路径…">
<select id="track" aria-label="研究分支"><option value="">全部分支</option></select>
<select id="kind" aria-label="关系类型"><option value="">全部关系</option></select>
<button id="clear" class="clear" type="button" hidden>清除选中节点</button>
<span id="count" class="count"></span>
</div>
<main id="routes" class="routes"></main>
<aside id="inspector" aria-live="polite"><h2>选择节点</h2><p>前提以合取方式连接。点击任一前提或结论，查看来源与相关关系。</p></aside>
</div>
<script id="graph-data" type="application/json">__GRAPH_DATA__</script>
<script>
const graph = JSON.parse(document.getElementById('graph-data').textContent);
const byId = new Map(graph.nodes.map(n => [n.id,n]));
const routeBox = document.getElementById('routes');
const inspector = document.getElementById('inspector');
const search = document.getElementById('search');
const track = document.getElementById('track');
const kind = document.getElementById('kind');
const clear = document.getElementById('clear');
let selected = null;
const trackNames = {model:'Model',local:'Local geometry',shared:'Shared phi',heterogeneous:'Heterogeneous',computation:'Exact computation',extensions:'Cost extensions',evidence:'Evidence'};
const add = (parent,tag,text,cls) => { const e=document.createElement(tag); if(text!==null)e.textContent=text; if(cls)e.className=cls; parent.appendChild(e); return e; };
const link = (parent,path) => { const a=add(parent,'a',path); a.href='../'+path; a.target='_blank'; a.rel='noopener'; return a; };
for(const t of Object.keys(trackNames)) { const o=add(track,'option',trackNames[t]); o.value=t; }
for(const k of Object.keys(graph.legend)) { const o=add(kind,'option',k); o.value=k; }
function nodeButton(parent,id,target) {
  const n=byId.get(id), b=add(parent,'button',null,'node'+(target?' target':''));
  b.type='button'; b.setAttribute('aria-label',n.id+' '+n.title);
  add(b,'strong',n.id); add(b,'small',n.title);
  b.addEventListener('click',()=>selectNode(id)); return b;
}
function selectNode(id) {
  selected=id; clear.hidden=false; const n=byId.get(id); inspector.replaceChildren();
  add(inspector,'h2',n.title); add(inspector,'span',n.id+' · '+n.kind+' · '+n.status+' · '+trackNames[n.track],'badge');
  add(inspector,'p',n.detail);
  add(inspector,'h3','现行说明与原始来源'); const list=add(inspector,'ul');
  for(const ref of n.refs) link(add(list,'li'),ref);
  const incoming=graph.hyperedges.filter(e=>e.conclusion===id);
  const outgoing=graph.hyperedges.filter(e=>e.premises.includes(id));
  add(inspector,'h3','Relationships');
  add(inspector,'p',incoming.length+' incoming · '+outgoing.length+' outgoing. Click a route ID to keep the branch in view.');
  const rel=add(inspector,'ul');
  for(const e of [...incoming,...outgoing]) {
    const a=add(add(rel,'li'),'a',e.id+' · '+e.kind+' · '+e.statement); a.href='#'+e.id;
  }
  render();
}
function render() {
  const q=search.value.trim().toLowerCase(), branch=track.value, relation=kind.value;
  routeBox.replaceChildren(); let count=0;
  for(const e of graph.hyperedges) {
    const terms=[e.id,e.statement,...e.refs,e.conclusion,byId.get(e.conclusion).title,...e.premises.flatMap(p=>[p,byId.get(p).title])].join(' ').toLowerCase();
    if(branch && e.track!==branch) continue;
    if(relation && e.kind!==relation) continue;
    if(q && !terms.includes(q)) continue;
    if(selected && !e.premises.includes(selected) && e.conclusion!==selected) continue;
    count++;
    const card=add(routeBox,'article',null,'route'); card.id=e.id; card.dataset.kind=e.kind;
    const meta=add(card,'div',null,'meta'); add(meta,'span',e.id); add(meta,'span',e.kind); add(meta,'span',e.status); add(meta,'span',trackNames[e.track]);
    const row=add(card,'div',null,'relation'); const inputs=add(row,'div',null,'premises');
    for(const p of e.premises) nodeButton(inputs,p,false);
    add(row,'span',e.kind==='attacks'?'⊣':'⇒','junction');
    nodeButton(row,e.conclusion,true);
    add(card,'p',e.statement);
    const sources=add(card,'div',null,'refs'); add(sources,'span','现行说明与来源: ');
    e.refs.forEach((ref,i)=>{ if(i)add(sources,'span',' · '); link(sources,ref); });
  }
  if(!count)add(routeBox,'div','No routes match. Clear a filter or select another branch.','empty');
  document.getElementById('count').textContent=count+' / '+graph.hyperedges.length+' hyperedges';
}
for(const control of [search,track,kind]) control.addEventListener('input',render);
clear.addEventListener('click',()=>{selected=null;clear.hidden=true;render();});
render();
</script>
</body>
</html>
'''


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="validate data and generated HTML")
    args = parser.parse_args()
    data = json.loads((HERE / "graph.json").read_text(encoding="utf-8"))
    validate(data)
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    rendered = HTML.replace("__GRAPH_DATA__", payload)
    output = HERE / "index.html"
    if args.check:
        require(output.is_file() and output.read_text(encoding="utf-8") == rendered,
                "run research/build_map.py")
    else:
        output.write_text(rendered, encoding="utf-8")
    print(f"Validated {len(data['nodes'])} nodes, {len(data['hyperedges'])} hyperedges and all source paths")


if __name__ == "__main__":
    main()
