---
id: "historical-research/graph-html-contract"
kind: "resource"
type_tag: "资源"
title: "旧研究超图HTML的完整表示和交互边界"
status: "historical-resource-fully-read-with-explicit-scope-and-version-boundaries"
summary: "全部shell/CSS/JS、完整graph payload绑定与未显示字段保全；静态表示检查不认证实际渲染或数学。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/index.html"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/index.html"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/graph.json"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/graph.json"
---

# 旧研究超图HTML的完整表示和交互边界

冻结 index.html 是 standalone 静态 HTML：graph-data 内嵌整份 graph.json，客户端 JS 渲染关系卡与节点检查栏。本批已读完实际 HTML 的全部非数据区 8,972 字节，内嵌 1,521,223 字节数据区通过结构相等绑定到已逐字段读完的 1,153 节点和 1,353 超边；静态模板替换重建整个 1,530,181 字节原件全等。shell 的 __GRAPH_DATA__ 标记占14字节，所以两分区字节数不能直接相加等于原件。没有运行旧 builder，且这不构成浏览器显示或交互 PASS。

## 页面实际行为与遗漏

头部可见标题“数学研究超图”，介绍前提合取、红色反驳、黄色有限测试/边界，链接总览、旧现行命题、JSON；“完整主稿内部审读”是原页面历史说明，不能推广成全页所有节点均获同级审查。红色亦不能保证每条旧 attacks 真以假命题为端点，实际反例见总合同。

工具栏是 search、九分支 track、五种 relation、清除选中节点和计数。kind 下拉只使用 legend 的键，完整五条定义没有展示；version/title/updated 的 graph metadata 也没有展示。两条额外 hyperedge.detail 均未使用：E-UM-COMMON-SIZE-UNKNOWN-B-EXACT-v1 与 E-UM-UNKNOWN-TARGET-PARTITION-SEARCH-OBSTRUCTION-v1，其 detail 为阶段接口不升级主目标。此信息仍在完整图资源中。

render 遍历全部超边，以 e.track/e.kind 筛选；搜索词只拼 e.id/e.statement/e.refs、结论及前提 ID/title，不包含节点 detail/refs/status、超边 status、legend 定义和额外 detail。选节点后只保直接关联入/出边，非传递闭包。节点按钮展示 ID/title、aria-label；检查栏展示 kind/status/track/detail/refs，并列出相关边。清除只取消 selected 和隐藏按钮，保留搜索/track/kind 与检查栏原内容；点相关边的锚点不清其它筛选，所以不能保证该边当时可见。当前源图无游离节点，静态上所有节点至少出现在一张关系卡；这不是当前新图必须连通的要求。

卡片展示 id/kind/status/track、所有前提、结论、statement 和 refs；attacks 用⊣，其余用⇒，共同前提在左框。derives 青绿、attacks 红、checks/limits 黄褐、implements 蓝。textContent 插入所有文本，未装 KaTeX/MathJax，因此数学是原文字/TeX样式字符串，不承诺排版数学公式。来源链接一律 ../ + 旧仓根相对路径，新标签页且 noopener；本批未逐个访问全部1,420种路径。颜色、字形和布局来自此 CSS，没有外部图片、嵌入字体或外部脚本的独有语义资产。

布局主宽1480px，关系卡加270–340px sticky 检查栏；850px以下改普通流，570px以下前提/结论纵排且旋转箭头。focus-visible 给节点描边，inspector aria-live=polite。这里只从实际 CSS/DOM/JS 得出设计行为，未验证浏览器实际像素、滚动性能、读屏或事件运行；不复用另一 learning HTML 的字体缺陷认定本页也有此缺陷。

## 完整外壳

下面移除且仅移除已完整另存/阅读的 JSON payload，以 __GRAPH_DATA__ 标记替代；全部 CSS、外壳文字、JS 原样保留。完整原件和绑定报告在 tools/evidence/claims-graph-review-resources。

```html
<!doctype html>
<html lang="zh">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>共同研究：数学超图</title>
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
const trackNames = {unrelated_machines:'不相关并行机',model:'Model',local:'Local geometry',shared:'Shared phi',heterogeneous:'Heterogeneous',computation:'Exact computation',extensions:'Cost extensions',evidence:'Evidence',weighted_congestion:'加权拥塞'};
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
```
