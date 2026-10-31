// New, limited syntax audit. Does not run the historical exporter or KaTeX.
import fs from 'node:fs';
import path from 'node:path';
import {createRequire} from 'node:module';
import {pathToFileURL} from 'node:url';
const require=createRequire(import.meta.url);
const {marked}=await import(pathToFileURL(require.resolve('marked',{paths:[process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES]})));
const base=path.dirname(new URL(import.meta.url).pathname);
const audit=JSON.parse(fs.readFileSync(path.join(base,'original/learning/export/学习和演讲-学习定稿.html.audit.json'),'utf8'));
const esc=s=>s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
function math(tex,display){
 tex=tex.replace(/\\mspace\{([+-]?[\d.]+)mu\}/g,'\\mkern$1mu');
 tex=tex.replace('\\tag{SPE_\\alpha}','\\tag{$\\mathrm{SPE}_\\alpha$}');
 if(tex.includes('\\begin{split}')&&tex.split('\n').some(l=>(l.match(/&/g)||[]).length>1))tex=tex.replace(/\\begin\{split\}/g,'\\begin{aligned}').replace(/\\end\{split\}/g,'\\end{aligned}');
 return '<span class="math-token" data-display="'+display+'" data-tex="'+esc(tex.trim())+'"></span>';
}
marked.use({extensions:[
 {name:'displayMath',level:'block',start(s){let a=s.indexOf('$$'),b=s.indexOf('\\[');return a<0?b:b<0?a:Math.min(a,b);},tokenizer(s){let m=s.match(/^\$\$\s*([\s\S]*?)\$\$[ \t]*(?:\n|$)/)||s.match(/^\\\[\s*([\s\S]*?)\\\][ \t]*(?:\n|$)/);if(m)return{type:'displayMath',raw:m[0],text:m[1]};},renderer(t){return '<div class="equation">'+math(t.text,true)+'</div>\n';}},
 {name:'inlineMath',level:'inline',start(s){let a=s.indexOf('$'),b=s.indexOf('\\(');return a<0?b:b<0?a:Math.min(a,b);},tokenizer(s){let m=s.match(/^\$(?!\$)([^$\n]+?)\$(?!\$)/)||s.match(/^\\\(([\s\S]*?)\\\)/);if(m)return{type:'inlineMath',raw:m[0],text:m[1]};},renderer(t){return math(t.text,false);}}
]});
const result=audit.sources.map(s=>({path:s.path,html:marked.parse(fs.readFileSync(path.join(base,'related',s.path),'utf8'),{gfm:true})}));
fs.writeFileSync(path.join(base,'syntax-render.json'),JSON.stringify(result));
process.stdout.write(JSON.stringify({source_count:result.length,scope:'marked syntax plus normalized TeX tokens; no KaTeX or PDF rendering'})+'\n');
