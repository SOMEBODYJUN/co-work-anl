#!/usr/bin/env node
// Offline full-course export. Dependencies: marked; KaTeX 0.16.11 JS/CSS/fonts.
// Usage: node learning/build_reading.mjs KATEX_DIST_DIR OUTPUT_HTML
import fs from 'node:fs';
import path from 'node:path';
import {createRequire} from 'node:module';
import {fileURLToPath,pathToFileURL} from 'node:url';
import crypto from 'node:crypto';
const require=createRequire(import.meta.url);
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const [assets,outFile]=process.argv.slice(2);
if(!assets||!outFile) throw Error('Expected KaTeX distribution directory and output path.');
const {marked}=await import(pathToFileURL(require.resolve('marked',{paths:[process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES||root,root]})));
const katex=require(path.resolve(assets,'katex.min.js'));
let css=fs.readFileSync(path.join(assets,'katex.min.css'),'utf8');
css=css.replace(/src:([^;]+);/g,(whole,s)=>{
 const m=s.match(/url\((?:["']?)(fonts\/[^)"']+\.woff2)(?:["']?)\)/);
 return m?'src:url(data:font/woff2;base64,'+fs.readFileSync(path.join(assets,m[1])).toString('base64')+') format("woff2");':whole;
});
if(/url\((?!data:)/.test(css))throw Error('An external font reference remains.');
const lessons=[
 'learning/README.md','learning/00_prerequisites.md','learning/01_model.md','learning/01a_proof_techniques.md',
 'learning/02_two_facility.md','learning/03_arbitrary_k.md','learning/04_complexity.md','learning/05_tools.md',
 'learning/06_frontier.md','learning/07_seminar.md','learning/08_reading_list.md','learning/09_workshop.md','learning/AUDIT.md'];
const appendices=[
 'research/current/model.md','research/current/multi_facility/model.md',
 'research/current/shared/theorems.md','research/current/shared/algorithm.md','research/current/shared/proof.md',
 'research/current/shared/local_chord_full.md','research/current/shared/heavy_pairs.md',
 'research/current/shared/star_anchors.md','research/current/shared/sharp_phi_lower.md',
 'research/current/shared/small_sparse_catalogs.md','research/current/shared/instance_complexity_barriers.md',
 'research/current/shared/three_site_exact_hardness.md','research/current/shared/five_site_exact_hardness.md',
 'research/current/shared/atomic_granularity.md',
 'research/current/heterogeneous/four_seed_algorithm.md','research/current/heterogeneous/full_catalog_cycle.md',
 'research/current/heterogeneous/sharp_two_lower.md','research/current/heterogeneous/restricted_rho.md',
 'research/current/heterogeneous/sparse_unbounded_rho.md','research/current/heterogeneous/core_lift_and_monotone.md',
 'research/current/multi_facility/uniform_two.md','research/current/multi_facility/reverse_review.md',
 'research/current/multi_facility/polytime_frontier.md','research/current/multi_facility/adaptive_reset_floor.md',
 'research/current/multi_facility/frozen_overload_completion.md'];
const all=[...lessons,...appendices],ids=new Map(all.map((p,i)=>[p,'source-'+i])),headings=new Map(),records=[],errors=[];
let current='',equations=0;
const renderOnlyNormalizations=[];
const esc=s=>s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
const slug=s=>s.toLowerCase().replace(/<[^>]*>/g,'').replace(/[^\p{L}\p{N}\s_-]/gu,'').trim().replace(/\s+/g,'-');
function math(tex,display){
 equations++;
 if(tex.includes('\\tag{SPE_\\alpha}')){
  renderOnlyNormalizations.push({source:current,reason:'Render the SPE alpha equation label in text mode.'});
  tex=tex.replace('\\tag{SPE_\\alpha}','\\tag{$\\mathrm{SPE}_\\alpha$}');
 }
 if(tex.includes('\\begin{split}') && tex.split('\n').some(line=>(line.match(/&/g)||[]).length>1)){
  renderOnlyNormalizations.push({source:current,reason:'Render a multi-column split as aligned; keep all equation terms.'});
  tex=tex.replace(/\\begin\{split\}/g,'\\begin{aligned}').replace(/\\end\{split\}/g,'\\end{aligned}');
 }
 try{return katex.renderToString(tex,{displayMode:display,throwOnError:true,strict:'ignore',trust:false});}
 catch(e){errors.push({source:current,tex,error:e.message});return '<code>'+esc(tex)+'</code>';}
}
marked.use({extensions:[
 {name:'displayMath',level:'block',start(s){let a=s.indexOf('$$'),b=s.indexOf('\\[');return a<0?b:b<0?a:Math.min(a,b);},
  tokenizer(s){let m=s.match(/^\$\$[ \t]*\n([\s\S]*?)\n\$\$[ \t]*(?:\n|$)/)||s.match(/^\\\[\s*([\s\S]*?)\\\][ \t]*(?:\n|$)/);if(m)return{type:'displayMath',raw:m[0],text:m[1]};},
  renderer(t){return '<div class="equation">'+math(t.text,true)+'</div>\n';}},
 {name:'inlineMath',level:'inline',start(s){let a=s.indexOf('$'),b=s.indexOf('\\(');return a<0?b:b<0?a:Math.min(a,b);},
  tokenizer(s){let m=s.match(/^\$(?!\$)([^$\n]+?)\$(?!\$)/)||s.match(/^\\\(([\s\S]*?)\\\)/);if(m)return{type:'inlineMath',raw:m[0],text:m[1]};},
  renderer(t){return math(t.text,false);}}
]});
for(const p of all){
 current=p;const raw=fs.readFileSync(path.join(root,p),'utf8');
 let html=marked.parse(raw,{gfm:true});
 const titles=raw.split('\n').filter(l=>/^#{1,6}\s/.test(l)).map(l=>l.replace(/^#{1,6}\s+/,'').trim());
 const counts=new Map(),hs=[];let hi=0;
 html=html.replace(/<h([1-6])>([\s\S]*?)<\/h\1>/g,(whole,d,t)=>{
  let base=slug(titles[hi++]||t.replace(/<[^>]*>/g,'')),n=counts.get(base)||0;counts.set(base,n+1);
  const fragment=base+(n?'-'+n:''),id=ids.get(p)+'--'+fragment;
  hs.push({fragment,id});return '<h'+d+' id="'+esc(id)+'">'+t+'</h'+d+'>';
 });
 headings.set(p,hs);
 records.push({path:p,id:ids.get(p),title:titles[0]||p,html,bytes:Buffer.byteLength(raw),sha256:crypto.createHash('sha256').update(raw).digest('hex')});
}
let sectionFallbacks=0;
for(const r of records)r.html=r.html.replace(/href="([^"]+)"/g,(whole,href)=>{
 if(/^(https?:|mailto:|data:)/i.test(href))return whole;
 const [file,frag]=href.split('#');
 const target=file?path.posix.normalize(path.posix.join(path.posix.dirname(r.path),file)):r.path;
 if(ids.has(target)){
  let dest=ids.get(target);
  if(frag){const h=headings.get(target).find(h=>h.fragment===frag);if(h)dest=h.id;else sectionFallbacks++;}
  return 'href="#'+esc(dest)+'"';
 }
 return 'href="'+esc('https://github.com/SOMEBODYJUN/co-work-anl/blob/main/'+target+(frag?'#'+frag:''))+'" target="_blank" rel="noopener"';
});
const report={date:'2026-10-06',lessons:lessons.length,appendices:appendices.length,equations,mathErrors:errors,renderOnlyNormalizations,sectionFallbacks,sources:records.map(({path,sha256,bytes})=>({path,sha256,bytes}))};
fs.mkdirSync(path.dirname(path.resolve(outFile)),{recursive:true});
fs.writeFileSync(outFile+'.audit.json',JSON.stringify(report,null,2)+'\n');
if(errors.length)throw Error(errors.length+' math errors. Inspect '+outFile+'.audit.json');
const style=`
:root{--ink:#202c37;--muted:#566777;--border:#d8e1e7;--accent:#135a70}*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:#f7f8fa;color:var(--ink);font-family:system-ui,-apple-system,"Noto Sans SC","Microsoft YaHei",sans-serif;line-height:1.85}
nav{position:fixed;left:0;top:0;bottom:0;width:280px;overflow:auto;padding:26px 20px;border-right:1px solid var(--border);background:white}nav strong{display:block;margin-bottom:18px;font-size:18px}nav a{display:block;color:var(--accent);text-decoration:none;padding:7px 4px;border-bottom:1px solid #eef2f5;font-size:13px}main{max-width:1130px;margin-left:280px;padding:36px 54px 100px}header,.chapter,.appendix{background:white;border:1px solid var(--border);border-radius:8px;margin:0 0 26px;padding:34px 40px}
h1{font-size:29px;line-height:1.45}h2{margin-top:40px;font-size:23px;border-bottom:1px solid var(--border);padding-bottom:10px}h3{font-size:19px;margin-top:28px}p{margin:14px 0}li{margin:7px 0}a{color:var(--accent)}table{display:block;overflow:auto;border-collapse:collapse;margin:22px 0;font-size:14px;line-height:1.65;width:100%}th,td{border:1px solid var(--border);padding:10px 14px;vertical-align:top}th{background:#eff5f7}
pre{overflow:auto;background:#f2f5f7;padding:20px;border-radius:6px;line-height:1.55}code{font-family:ui-monospace,monospace;font-size:.92em}blockquote{border-left:4px solid #7e9ba7;padding:4px 18px;margin:22px 0;color:#3d5261}.source-note{color:var(--muted);font-size:12px;margin-bottom:20px;overflow-wrap:anywhere}.equation{overflow-x:auto;overflow-y:hidden;margin:20px 0}.katex-display{margin:10px 0}.katex{font-size:1.06em}p .katex{white-space:nowrap}
summary{cursor:pointer;font-weight:650;color:var(--accent)}details[open]>summary{margin-bottom:24px}.appendix section{padding-top:10px}.reading-card{border-left:4px solid #18768a;background:#f0f7f8;padding:18px 22px}.buttons{display:flex;gap:12px;flex-wrap:wrap}button{border:1px solid #89a4af;background:white;color:var(--accent);padding:9px 14px;border-radius:4px;cursor:pointer}:target{scroll-margin-top:24px}
@media(max-width:1000px){nav{position:static;width:auto;max-height:340px;border-bottom:1px solid var(--border)}main{margin:0;padding:24px 18px}.chapter,header,.appendix{padding:22px}h1{font-size:26px}}
@media print{nav,.buttons{display:none}main{margin:0;padding:0;max-width:none}body{background:white;color:black;font-size:11pt}.chapter,header,.appendix{border:0;padding:0;break-before:page}table{display:table;font-size:9pt}a{color:inherit}h2,h3{break-after:avoid}.equation{overflow:visible}}
`;
const behavior=`
function reveal(){let e=document.getElementById(decodeURIComponent(location.hash.slice(1)));if(e){for(let a=e;a;a=a.parentElement)if(a.tagName==='DETAILS')a.open=true;e.scrollIntoView()}}
addEventListener('hashchange',reveal);addEventListener('load',reveal);
document.getElementById('expand').onclick=()=>document.querySelectorAll('details').forEach(d=>d.open=true);
document.getElementById('collapse').onclick=()=>document.querySelectorAll('details').forEach(d=>d.open=false);
let oldOpen=[];addEventListener('beforeprint',()=>{oldOpen=[...document.querySelectorAll('details')].filter(d=>d.open);document.querySelectorAll('details').forEach(d=>d.open=true)});addEventListener('afterprint',()=>document.querySelectorAll('details').forEach(d=>d.open=oldOpen.includes(d)));
`;
const nav=records.slice(0,lessons.length).map(r=>'<a href="#'+r.id+'">'+esc(r.title)+'</a>').join('\n');
const body=(r)=>'<div class="source-note">来源：'+esc(r.path)+'</div>'+r.html;
const chapters=records.slice(0,lessons.length).map(r=>'<section class="chapter" id="'+r.id+'">'+body(r)+'</section>').join('\n');
const appendixNav=records.slice(lessons.length).map((r,i)=>'<li><a href="#'+r.id+'">'+(i+1)+'. '+esc(r.title)+'</a></li>').join('\n');
const appendixBody=records.slice(lessons.length).map((r,i)=>'<details class="appendix" id="'+r.id+'"><summary>规范长附录 '+(i+1)+' · '+esc(r.title)+'</summary><section>'+body(r)+'</section></details>').join('\n');
const html='<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>学习和演讲：证明技术分析版</title><style>'+css+'\n'+style+'</style></head><body><nav><strong>学习与讨论目录</strong>'+nav+'<a href="#appendix-list">规范长附录</a></nav><main><header><p>人类团队 · 两周研讨会 · 完整阅读版</p><h1>先理解方法为什么出现，再把推导写成证明</h1><div class="reading-card"><p>新增 01A 技术分析课。从困难出发，解释要控制什么、为什么作此替换、每步怎样操作、哪些量保持、拿到什么以及还缺什么。随后回到原长证明逐式展开。</p><p>课程原文、例题和两周安排保留。规范长附录全文内嵌，可展开或沿链接直达；教学解释不提升研究结论的审查状态。</p><p><a href="#'+ids.get('learning/01a_proof_techniques.md')+'">进入 01A 技术分析课</a> · <a href="#'+ids.get('learning/02_two_facility.md')+'">黄金比例主线</a> · <a href="#'+ids.get('learning/03_arbitrary_k.md')+'">任意设施数主线</a></p></div><p>版本：2026-10-06。公式及字体已内嵌，可离线阅读。未内嵌的代码与专题链接指向 GitHub。</p><div class="buttons"><button id="expand">展开全部长附录</button><button id="collapse">折叠长附录</button><button onclick="window.print()">打印／保存 PDF</button></div></header>'+chapters+'<section class="chapter" id="appendix-list"><h1>规范长附录：完整推导按需展开</h1><p>以下按源文件全文转排，边界、证明义务和状态说明均保留。不能以技术课的短解释代替这些长分支。</p><ol>'+appendixNav+'</ol></section>'+appendixBody+'</main><script>'+behavior+'</script></body></html>';
fs.writeFileSync(outFile,html);
console.log(JSON.stringify({output:outFile,lessons:lessons.length,appendices:appendices.length,equations,errors:errors.length,bytes:Buffer.byteLength(html),sectionFallbacks}));
