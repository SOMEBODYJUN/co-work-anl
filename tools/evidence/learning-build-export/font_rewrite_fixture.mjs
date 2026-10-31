// New synthetic mechanism check only; not a run of the frozen full exporter.
import fs from 'node:fs';
import path from 'node:path';
const base=path.dirname(new URL(import.meta.url).pathname);
const payload=n=>fs.readFileSync(path.join(base,`assets/font-${String(n).padStart(2,'0')}.woff2`)).toString('base64');
const fixtures=[
 {name:'src-last-without-semicolon',css:'@font-face{font-family:KaTeX_AMS;font-style:normal;font-weight:400;src:url(fonts/a.woff2) format("woff2")}@font-face{font-family:KaTeX_Caligraphic;font-style:normal;font-weight:700;src:url(fonts/b.woff2) format("woff2")}.katex{font:normal 1.21em KaTeX_Main,serif;line-height:1.2;text-indent:0;text-rendering:auto}'},
 {name:'src-last-with-semicolon',css:'@font-face{font-family:KaTeX_AMS;font-style:normal;font-weight:400;src:url(fonts/a.woff2) format("woff2");}@font-face{font-family:KaTeX_Caligraphic;font-style:normal;font-weight:700;src:url(fonts/b.woff2) format("woff2");}.katex{font:normal 1.21em KaTeX_Main,serif;line-height:1.2}'},
 {name:'src-before-other-descriptor',css:'@font-face{font-family:KaTeX_AMS;src:url(fonts/a.woff2) format("woff2");font-style:normal;font-weight:400}@font-face{font-family:KaTeX_Caligraphic;src:url(fonts/b.woff2) format("woff2");font-style:normal;font-weight:700}.katex{font:normal 1.21em KaTeX_Main,serif;line-height:1.2}'}
];
function replacement(s){const m=s.match(/url\((?:["']?)(fonts\/[^)"']+\.woff2)(?:["']?)\)/);return m?'src:url(data:font/woff2;base64,'+payload(m[1]==='fonts/a.woff2'?0:1)+') format("woff2");':null;}
const redact=s=>s.replace(/data:font\/woff2;base64,[A-Za-z0-9+/=]+/g,m=>'EMBEDDED_WOFF2_BYTES_'+m.length);
const describe=s=>({face_count:(s.match(/@font-face/g)||[]).length,families:[...s.matchAll(/@font-face\s*\{font-family:([^;]+)/g)].map(m=>m[1]),base_font_rule:/\.katex\{font:normal 1\.21em KaTeX_Main,serif;/.test(s),stylesheet:redact(s)});
const results=fixtures.map(f=>{
 // Exact matching/replacement boundary from build_reading.mjs.
 const historical=f.css.replace(/src:([^;]+);/g,(whole,s)=>replacement(s)||whole);
 // Minimal bounded proposal. Only tested against these fixtures, not a full distribution.
 const bounded=f.css.replace(/src:([^;}]+)([;}])/g,(whole,s,end)=>{const r=replacement(s);return r?r+(end==='}'?'}':''):whole;});
 if(describe(bounded).face_count!==2||!describe(bounded).base_font_rule)throw Error('Bounded proposal fixture failed');
 return {name:f.name,input:f.css,historical:describe(historical),bounded_proposal:describe(bounded)};
});
const result={scope:'3 synthetic CSS fixtures using two exact retained WOFF2 payloads; historical regex mechanism and bounded replacement proposal; no full builder, KaTeX, PDF, browser, or math test',results,proposal_applied_to_frozen_source:false,proposal_full_distribution_validated:false};
fs.writeFileSync(path.join(base,'font-rewrite-fixture.json'),JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify({fixtures:results.length,historical_missing_semicolon_collapses_faces:results[0].historical.face_count===1,bounded_fixtures_pass:true}));
