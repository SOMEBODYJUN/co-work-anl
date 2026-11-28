"use strict";
const E=HouseholdEngine,$=id=>document.getElementById(id),q=(s,root=document)=>root.querySelector(s);
const html=v=>String(v??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
const deepcopy=v=>JSON.parse(JSON.stringify(v));
const originals=()=>JSON.parse($("scenario-data").textContent);
let h=E.blank(),scenarios=originals(),study=null,active="inputs",scenarioId=scenarios[0].id,strategyId="S000",compareId="S000";
let objective="cash",filter="all",unit=1,limit=500,chartKey="cash",stressResult=null;
const names={incomes:"收入来源",expenses:"支出",financial:"金融及其他资产",properties:"房产",vehicles:"车辆",loans:"贷款与其他债务"};
const labels={
  id:"唯一 ID",name:"名称",kind:"类别",monthly:"每次到账 / 支出",from:"起始月",to:"结束月",every:"间隔月数",annualGrowth:"年增长率",
  stability:"收入稳定性说明",stressJob:"采用情景整体失业事件",jobStart:"自行指定失业起点",jobMonths:"自行指定失业时长",jobPayFraction:"中断期间收入比例",
  recoveryMonths:"恢复至复工水平用时（月）",returnFraction:"复工最终收入比例",inflationLinked:"随通胀调整",value:"期初账面市值",annualReturn:"年总回报（含股息）",
  concentration:"集中持仓占比",fee:"交易成本率",settle:"卖出后到账月数",unlock:"最早解锁月",maturity:"到期兑付月（0无到期）",restriction:"资金限制",purpose:"资金用途",
  city:"所在城市",type:"房屋类型",use:"住房用途",saleValue:"保守可成交总价",saleLag:"挂牌至交割月数",lock:"最早可挂牌月",canSell:"允许出售",
  rent:"整月市场租金",vacancy:"预计空置比例",leaseLag:"正常议价起租等待（月）",discountRent:"快速出租租金折让",discountLeaseLag:"快速出租等待（月）",
  carry:"每月持有费用",saleFee:"成交成本率",closingFee:"成交固定费用",replacementAllowed:"具备可行住房 / 出行替代",replacementMonthly:"替代方案每月费用",
  sourceId:"城市资料 ID",annualDepreciation:"年折旧比例",necessary:"必要通勤 / 生产用车",collateral:"关联资产 ID（无则空）",
  principal:"剩余本金 / 代偿额",annualRate:"合同年利率",rateType:"利率类型",resetFirst:"首次重定价期数",resetEvery:"重定价间隔（月）",
  months:"剩余合同期数",method:"合同还款方式",payment:"约定等额月供（留空按公式）",canPrepay:"允许提前还款",prepayFrom:"最早提前还款期数",
  prepayMin:"最低部分预付额",prepayFee:"预付本金费用率",settlementFee:"结清固定费用",transferWithLien:"可用交易款同步解押",
  allowRecast:"允许部分预付降月供",allowShorten:"允许部分预付缩期限",start:"担保代偿月（普通债务为1）",monthlyFee:"每期合同费用",
  cash:"期初可用现金",cashAnnual:"现金年收益率",reserveMonths:"目标储备月数",minimumLiving:"最低生活支出 / 月",cutFraction:"可选支出最大削减比例",
  maxSaleWait:"最长可接受成交等待（月）",rangeCase:"家庭区间取值",preference:"单项目标"
};
const sels={
  incomeKind:{wage:"税后工资",bonus:"税后奖金",business:"经营净回款",other:"其他已存在收入"},
  expenseKind:{necessary:"必要生活",education:"教育",medical:"医疗",elder:"养老",insurance:"保险",discretionary:"可削减",emergency:"突发"},
  financialKind:{deposit:"定期存款",instant:"随时可变现余额",stock:"股票",fund:"基金",bond:"债券",gold:"黄金",other:"其他计价资产"},
  loanKind:{mortgage:"住房贷款",car:"车贷",consumer:"消费贷",card:"信用卡",business:"经营贷",family:"亲友借款",margin:"证券杠杆",guarantee:"担保代偿",other:"其他债务"},
  restriction:{unknown:"交易与用途尚未确认",free:"可用于家庭支出",restricted:"专款/受限",pledged:"质押（依合同先行或同步解押）"},use:{idle:"闲置",occupied:"自住",let:"已出租"},
  rateType:{fixed:"固定利率",floating:"按期重定价"},method:{annuity:"等额本息",principal:"等额本金",bullet:"按月付息、到期还本"},
  rangeCase:{low:"全部低端",base:"各项中心值",high:"全部高端"},preference:{cash:"最大化最坏路径最低现金",wealth:"最大化最坏十年实际净资产",debt:"最小化峰值偿债比",regret:"最小化最大后悔额"}
};
const fast={incomes:["id","name","kind","monthly","from","to"],expenses:["id","name","kind","monthly","from","to"],
  financial:["id","name","kind","value","annualReturn","settle"],properties:["id","name","city","use","value","saleValue","rent","carry"],
  vehicles:["id","name","value","saleValue","carry","necessary"],loans:["id","name","kind","collateral","principal","annualRate","months","method"]};
const money=new Set(["monthly","value","saleValue","rent","carry","closingFee","replacementMonthly","principal","payment","prepayMin","settlementFee","monthlyFee","cash","minimumLiving"]);
const percentages=new Set(["annualGrowth","jobPayFraction","returnFraction","annualReturn","concentration","fee","vacancy","discountRent","saleFee","annualDepreciation","annualRate","prepayFee","cashAnnual","cutFraction"]);
const conditionalFlags=new Set(["canPrepay","allowRecast","allowShorten","transferWithLien","canSell","necessary"]);
const words=new Set(["id","name","stability","purpose","city","type","sourceId","collateral"]);
const groupKind={incomes:"incomeKind",expenses:"expenseKind",financial:"financialKind",loans:"loanKind"};
const pLabels={wageFactor:"工资/奖金倍数",businessFactor:"经营回款倍数",otherIncomeFactor:"其他收入倍数",unemploymentMonths:"失业事件时长",recoveryMonths:"复工过渡月数",
  reemploymentFactor:"复工后收入倍数",inflationAnnual:"通胀年率",cashRateDelta:"存款年率差",loanRateDelta:"浮息合同年率差",propertyShock:"一次性房价变动",propertyAnnual:"房价年变动率",
  rentFactor:"租金倍数",vacancyAdd:"空置率变化",financialShock:"一次性金融市值变动",securityAnnual:"金融年总回报差",concentrationHaircut:"集中持仓一次性折价",saleHaircut:"成交折价",saleDelay:"额外成交等待"};
const assumptions={observed:"观测",historical:"历史参照",research_estimate:"研究估计",stress_test:"人为压力测试"};
const opts=(xs,value)=>Object.entries(xs).map(([k,v])=>'<option value="'+html(k)+'" '+(String(value)===k?'selected':'')+'>'+html(v)+'</option>').join("");
function say(msg,bad=false){$("status").textContent=msg;$("status").classList.toggle("error",bad);}
function mark(){const e=$("kind"),example=h.dataKind==="synthetic_example";e.textContent=example?"合成示例 · 编辑后仍为示例":"家庭录入 · "+(h.cash==null?"金额待填":"本机数据");e.classList.toggle("sample",example);}
function resetResults(){study=null;stressResult=null;mark();say("输入已修改，运行后更新方案。");}
function valueText(v,mul){
  if(v==null)return "";
  const scale=x=>typeof x==="number"?String(Number((x*mul).toPrecision(14))):String(x);
  if(typeof v==="object")return [scale(v.low),v.base==null?"":scale(v.base),scale(v.high)].join("~");
  return scale(v);
}
function parseNumber(text,mul){
  const x=text.trim();if(!x)return null;
  const convert=s=>s.trim()!==""&&Number.isFinite(Number(s))?Number(s)/mul:s;
  if(x.includes("~")){const v=x.split("~");if(v.length===2)return {low:convert(v[0]),high:convert(v[1])};
    if(v.length===3)return {low:convert(v[0]),...(v[1].trim()?{base:convert(v[1])}:{}),high:convert(v[2])};return x;}
  return convert(x);
}
function field(group,index,key,obj){
  const v=obj[key],choice=sels[key==="kind"?groupKind[group]:key],factor=money.has(key)?1/unit:percentages.has(key)?100:1;
  const useUnit=money.has(key)?"（"+(unit===10000?"万元":"元")+"）":percentages.has(key)?"（%）":"";
  const ids=' id="f-'+group+'-'+index+'-'+key+'" data-group="'+group+'" data-index="'+index+'" data-key="'+key+'"';
  let control;
  if(conditionalFlags.has(key))control='<select'+ids+' data-contract-flag="true">'+opts({'':'尚未确认',true:'明确允许 / 是',false:'明确禁止 / 否'},v==null?'':v)+'</select>';
  else if(choice)control='<select'+ids+'>'+opts(choice,v)+'</select>';
  else if(typeof v==="boolean")control='<input type="checkbox"'+ids+(v?' checked':'')+'>';
  else control='<input type="text" '+(words.has(key)?'':'inputmode="decimal"')+ids+' value="'+html(valueText(v,factor))+'" '+(!words.has(key)&&v==null?'placeholder="填写或留空"':'')+'>';
  return '<label class="field"><span>'+html(labels[key]||key)+useUnit+'</span>'+control+'</label>';
}
function cards(){
  return Object.keys(names).map(group=>'<details class="panel g" id="g-'+group+'"><summary>'+names[group]+' <span class="pill">'+h[group].length+' 项</span></summary><div class="in">'
    +h[group].map((obj,i)=>'<details class="item" data-row="'+group+'-'+i+'"><summary>'+html(obj.name||obj.id||"未命名")+' <span class="small">'+html(obj.id)+'</span></summary><div class="fields">'
    +fast[group].map(k=>field(group,i,k,obj)).join("")+'</div><details><summary>合同、限制与路径参数</summary><p class="small">可保留未知条件。相应处置和预付需确认许可、日期与费用，免手续费请填 0。</p><div class="fields">'
    +Object.keys(E.templates[group]).filter(k=>!fast[group].includes(k)).map(k=>field(group,i,k,obj)).join("")+'</div></details><button class="danger" data-remove="'+group+'" data-i="'+i+'">删除此项</button></details>').join("")
    +'<button data-add="'+group+'">添加'+names[group]+'</button></div></details>').join("");
}
function drawInputs(openGroup=null,openRow=null){
  $("inputs").innerHTML='<div class="cols"><div><section class="panel"><div class="summaryline"><h2 class="sectiontitle">家庭底账</h2><label class="small">金额输入 <select id="unit"><option value="1">元</option><option value="10000">万元</option></select></label></div>'
    +'<p class="small">金额可填单值，或用 ~ 分开低值、中心值、高值。只有两端时选择低端或高端。比例输入框使用百分数。</p><div class="fields">'
    +["cash","minimumLiving","reserveMonths","cashAnnual","cutFraction","maxSaleWait","rangeCase","preference"].map(k=>field("base",0,k,h)).join("")+'</div></section>'+cards()
    +'<details class="panel" id="g-scenario"><summary>情景参数 <span class="pill">'+scenarios.length+' 条路径</span></summary><div class="in"><p class="small">以下假设采用小数年率或倍数；一次冲击仅在起点生效。具体目标 ID 优先于通用目标 *。所有候选在每条路径下分别运行。</p><div id="scenarioEditor"></div></div></details>'
    +'<details class="panel" id="g-city"><summary>城市资料与适用范围</summary><div class="in"><p class="small">每项填写 id、city、period、source、scope。房产按城市单独登记，城市资料随 JSON 离线导入。</p>'
    +'<textarea id="cities" rows="5" style="width:100%">'+html(JSON.stringify(h.citySources,null,2))+'</textarea><button id="applyCities">应用城市资料</button></div></details></div>'
    +'<aside class="panel sticky"><h2 class="sectiontitle">试算设置</h2><label class="field">最多运行的不同方案<select id="limit">'+opts({"100":"100","200":"200","300":"300","400":"400","500":"500"},limit)+'</select></label>'
    +'<p class="small">小于上限的组合全部运行。超过上限时覆盖基准、单项动作、跨资产两项动作和整个组合空间的分层样本。</p><p>先检查能否付清当月必需支出与债务，再对照储备目标和十年购买力。</p>'
    +'<button class="primary" id="runAside">运行 120 个月</button><hr style="border:0;border-top:1px solid var(--line);margin:17px 0"><button id="clearInputs" class="danger">新建空白家庭</button></aside></div>';
  $("unit").value=String(unit);$("runAside").onclick=doRun;$("limit").onchange=e=>{limit=Number(e.target.value);resetResults();};
  $("unit").onchange=e=>{unit=Number(e.target.value);drawInputs();};
  $("clearInputs").onclick=()=>{h=E.blank();scenarios=originals();study=null;stressResult=null;scenarioId=scenarios[0].id;drawInputs();mark();say("空白家庭已就绪。");};
  $("applyCities").onclick=()=>{try{const v=JSON.parse($("cities").value);if(!Array.isArray(v))throw Error("城市资料应为数组");h.citySources=v;resetResults();say("城市资料已应用。");}catch(e){say(e.message,true);}};
  drawPathEditor();
  if(openGroup){$("g-"+openGroup).open=true;if(openRow!=null){const node=q('[data-row="'+openGroup+'-'+openRow+'"]');if(node)node.open=true;}}
}
function drawPathEditor(){
  const s=scenarios.find(z=>z.id===scenarioId)||scenarios[0];
  const cell=(a,k,i,readonly=false)=>'<td><input aria-label="'+html(k)+'" data-pp="'+k+'" data-pi="'+i+'" value="'+html(a)+'" '+(readonly?'disabled':'')+' style="width:'+(['sourceId','target'].includes(k)?'140':'78')+'px"></td>';
  $("scenarioEditor").innerHTML='<label class="field">编辑情景<select id="editScenario">'+opts(Object.fromEntries(scenarios.map(z=>[z.id,z.name])),s.id)+'</select></label><p>'+html(s.description||"")+'</p><div class="scroll"><table class="compact"><thead><tr>'
    +["参数","数值","范围下限","范围上限","起点月","持续月","单位","目标 ID","来源 ID","假设类型"].map(k=>'<th>'+k+'</th>').join("")+'</tr></thead><tbody>'
    +s.paths.map((p,i)=>'<tr><th>'+html(pLabels[p.key])+'</th>'+cell(valueText(p.value,1),"value",i,!p.editable)+cell(p.range[0],"low",i,!p.editable)+cell(p.range[1],"high",i,!p.editable)
    +cell(p.start,"start",i,!p.editable)+cell(p.duration,"duration",i,!p.editable)+ '<td>'+html(p.unit)+'</td>'+cell(p.target,"target",i,!p.editable)+cell(p.sourceId,"sourceId",i,!p.editable)
    +'<td>'+html(assumptions[p.assumption])+'</td></tr>').join("")+'</tbody></table></div><details><summary>直接编辑全部情景 JSON</summary><textarea id="rawPaths" rows="8" style="width:100%">'+html(JSON.stringify(scenarios,null,2))+'</textarea><button id="applyPaths">应用情景 JSON</button></details>';
  $("editScenario").onchange=e=>{scenarioId=e.target.value;drawPathEditor();};
  $("applyPaths").onclick=()=>{try{const v=JSON.parse($("rawPaths").value);if(!Array.isArray(v)||!v.length)throw Error("至少需要一个情景");v.forEach(s=>E.validateScenario(s,h.rangeCase));if(new Set(v.map(s=>s.id)).size!==v.length)throw Error("情景 ID 重复");scenarios=v;scenarioId=v[0].id;resetResults();drawPathEditor();say("情景输入已应用。");}catch(e){say(e.message,true);}};
}
$("inputs").addEventListener("change",e=>{
  const t=e.target;
  if(t.dataset.group){
    const {group,index,key}=t.dataset,obj=group==="base"?h:h[group][index];
    const factor=money.has(key)?1/unit:percentages.has(key)?100:1;
    obj[key]=t.dataset.contractFlag?(t.value===""?null:t.value==="true"):t.type==="checkbox"?t.checked:t.tagName==="SELECT"||words.has(key)?t.value:parseNumber(t.value,factor);
    if(key==="preference")objective=obj[key];resetResults();
  }else if(t.dataset.pp){
    const s=scenarios.find(s=>s.id===scenarioId),p=s.paths[Number(t.dataset.pi)],k=t.dataset.pp;
    if(k==="value"){
      const single=p.range[0]===p.value&&p.range[1]===p.value;
      p.value=parseNumber(t.value,1);if(single&&typeof p.value==="number")p.range=[p.value,p.value];
    }else if(k==="low"||k==="high")p.range[k==="low"?0:1]=parseNumber(t.value,1);
    else p[k]=["target","sourceId"].includes(k)?t.value:parseNumber(t.value,1);
    resetResults();drawPathEditor();
  }
});
$("inputs").addEventListener("click",e=>{
  const b=e.target.closest("button");if(!b)return;
  const group=b.dataset.add||b.dataset.remove;if(!group)return;
  if(b.dataset.add){
    const pref={incomes:"inc",expenses:"exp",financial:"fin",properties:"house",vehicles:"car",loans:"loan"}[group];
    const ids=new Set(Object.keys(names).flatMap(g=>h[g].map(x=>x.id)));let n=1;while(ids.has(pref+n))n++;
    h[group].push({...deepcopy(E.templates[group]),id:pref+n});resetResults();drawInputs(group,h[group].length-1);
  }else{h[group].splice(Number(b.dataset.i),1);resetResults();drawInputs(group);}
});
function download(name,content,type){
  const blob=new Blob(Array.isArray(content)?content:[content],{type}),url=URL.createObjectURL(blob),a=document.createElement("a");
  a.href=url;a.download=name;document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),30000);
}
$("exportJSON").onclick=()=>{download("household-input.json",JSON.stringify({schema:"household-offline.bundle.v1",household:h,scenarios},null,2),"application/json");say("已导出当前家庭与情景。");};
$("importFile").onchange=async e=>{
  try{const f=e.target.files[0];if(!f)return;const data=JSON.parse(await f.text()),house=data.household||data,paths=data.scenarios||scenarios;
    // Permit reopening a deliberately incomplete draft; validate all amounts at run time.
    if(!house||house.schema!=="household-cny.v1"||!["household","synthetic_example"].includes(house.dataKind)||Object.keys(names).some(k=>!Array.isArray(house[k])||house[k].some(v=>!v||typeof v!=="object"||Array.isArray(v))))throw Error("家庭 JSON 结构不符");
    if(!Array.isArray(paths)||!paths.length)throw Error("情景缺失");paths.forEach(z=>E.validateScenario(z,house.rangeCase));
    h=house;scenarios=paths;scenarioId=scenarios[0].id;objective=h.preference;resetResults();setTab("inputs");drawInputs();say("JSON 已载入，请运行当前输入。");
  }catch(err){say("导入失败 · "+err.message,true);}e.target.value="";
};
$("loadDemo").onclick=()=>{h=JSON.parse($("example-data").textContent);scenarios=originals();scenarioId=scenarios[0].id;objective=h.preference;
  resetResults();setTab("inputs");drawInputs();say("已载入合成示例，可修改后运行。");};
function setTab(tab){
  active=tab;document.querySelectorAll(".view").forEach(v=>{v.hidden=v.id!==tab;if(v.hidden&&v.id!=="inputs")v.replaceChildren();});
  document.querySelectorAll("[data-tab]").forEach(b=>b.setAttribute("aria-selected",String(b.dataset.tab===tab)));
  if(tab!=="inputs")renderView();
}
document.querySelectorAll("[data-tab]").forEach(b=>b.onclick=()=>setTab(b.dataset.tab));
function doRun(){
  $("run").disabled=true;if($("runAside"))$("runAside").disabled=true;say("正在逐情景运行候选…");
  setTimeout(()=>{try{
    study=E.assess(h,scenarios,limit);stressResult=null;objective=h.preference;strategyId="S000";compareId="S000";filter="all";
    if(!scenarios.some(s=>s.id===scenarioId))scenarioId=scenarios[0].id;
    setTab("results");say("已运行 "+study.results.length+" 个方案 × "+scenarios.length+" 条情景。");mark();
  }catch(err){study=null;say(err.message,true);setTab("inputs");}finally{$("run").disabled=false;if($("runAside"))$("runAside").disabled=false;}},25);
}
$("run").onclick=doRun;
const yuan=n=>n==null||!Number.isFinite(n)?"—":Math.round(n).toLocaleString("zh-CN");
const ratio=(n,inf=false)=>inf?"∞":n==null?"—":(n*100).toFixed(1)+"%";
const table=(headers,rows)=>'<div class="scroll"><table><thead><tr>'+headers.map(h=>'<th>'+html(h)+'</th>').join("")+'</tr></thead><tbody>'+rows.map(row=>'<tr>'+row.map(v=>'<td>'+html(v)+'</td>').join("")+'</tr>').join("")+'</tbody></table></div>';
const metric=(label,value)=>'<div class="metric"><span>'+html(label)+'</span><strong>'+html(value)+'</strong></div>';
const rowById=id=>study.results.find(r=>r.strategy.id===id);
const scenarioName=()=>scenarios.find(s=>s.id===scenarioId).name;
const objectiveSelect=()=>'<label class="field">比较目标<select id="objective">'+opts(sels.preference,objective)+'</select></label>';
const scenarioSelect=()=>'<label class="field">查看情景<select id="resultScenario">'+opts(Object.fromEntries(scenarios.map(z=>[z.id,z.name])),scenarioId)+'</select></label>';
const policySelect=(id,value)=>'<label class="field">'+(id==="selectedPlan"?"查看方案":"并列方案")+'<select id="'+id+'">'+opts(Object.fromEntries(study.results.map(r=>[r.strategy.id,r.strategy.id+" · "+E.nameOf(r.strategy).slice(0,28)])),value)+'</select></label>';
function renderView(){
  const v=$(active);
  if(!study){v.innerHTML='<div class="panel"><h2 class="sectiontitle">尚无当前输入的结果</h2><p>填写家庭底账，或载入合成示例，再运行 120 个月。</p><button id="toInput">返回家庭与情景</button></div>';$("toInput").onclick=()=>setTab("inputs");return;}
  if(active==="results")drawResults();else if(active==="ledger")drawLedger();else if(active==="reverse")drawReverse();
  if($("resultScenario"))$("resultScenario").onchange=e=>{scenarioId=e.target.value;stressResult=null;renderView();};
  if($("selectedPlan"))$("selectedPlan").onchange=e=>{strategyId=e.target.value;stressResult=null;renderView();};
  if($("comparePlan"))$("comparePlan").onchange=e=>{compareId=e.target.value;renderView();};
  if($("objective"))$("objective").onchange=e=>{objective=e.target.value;renderView();};
}
function verdict(t){
  if(t.firstFailure){const f=t.failureBreakdown;return '<div class="verdict fail"><b>第 '+t.firstFailure+' 月现金不足，还差 '+yuan(t.worstGap)+' 元。</b> 此前完整执行 '+t.supportMonths+' 个月。该月合同还款缺口 '+yuan(f.missedDebtService)+' 元、必要与持有开支缺口 '+yuan(f.unfundedEssential)+' 元、可选预算缺口 '+yuan(f.unfundedDiscretionary)+' 元。未付本金保留在债务余额中，十年终值空缺。</div>';}
  if(t.blocked.length)return '<div class="verdict fail"><b>计划动作未能按约执行。</b> '+html(t.blocked[0].reason)+'。显示维持原安排后实际发生的收支。</div>';
  if(t.maxReserveGap>.000001)return '<div class="verdict fail"><b>120 个月到期款已付，储备最多还差 '+yuan(t.maxReserveGap)+' 元。</b></div>';
  return '<div class="verdict"><b>本路径下完整履约 120 个月，满足已录入储备条件。</b></div>';
}

function drawResults(){
  const r=rowById(strategyId),t=r.outcomes[scenarioId],comp=rowById(compareId).outcomes[scenarioId],c=study.coverage;
  const selected=E.rank(study.results,objective).filter(z=>filter==="all"||filter==="feasible"&&z.feasible||filter==="pareto"&&z.pareto||filter==="failed"&&!z.feasible);
  const winNames={baseline:"不行动基准",robust:"跨情景较稳健",cash:"最坏现金最好",regret:"最大后悔最少",wealth:"十年财富潜力",debt:"债务压力最低"};
  const chosen=Object.entries(winNames).map(([k,v])=>{const id=study.winners[k];return '<tr><th>'+v+'</th><td>'+(id?pick(id):"无共同可行方案")+'</td><td>'+html(id?E.nameOf(rowById(id).strategy):"—")+'</td></tr>';}).join("");
  const risk=study.commonCount?'全部 '+study.prepared.scenarios.length+' 条路径均满足资金、合同、储备的规则有 '+study.commonCount+' 个，形成 '+c.distinctFeasibleMonthlyTrajectories+' 种不同逐月轨迹。':
    '无共同可行方案。当前最小资金需求候选 '+study.winners.leastGap+'，其最坏单月缺口、储备或执行所需补资的最大值为 '+yuan(rowById(study.winners.leastGap).funding)+' 元；合同限制另列。';
  const sr=(label,a,b,fmt=yuan)=>[label,fmt(a),fmt(b)];
  $("results").innerHTML='<section class="panel"><h2 class="sectiontitle">方案比较</h2><p>'+html(risk)+'</p><div class="selectrow">'+scenarioSelect()+policySelect("selectedPlan",strategyId)+policySelect("comparePlan",compareId)+'</div><p><b>'+html(strategyId)+'</b>　'+html(E.nameOf(r.strategy))+'</p>'+verdict(t)
    +'<div class="metricgrid">'+metric("可完整履约",t.supportMonths+" 个月")+metric("首次资金缺口",t.firstFailure?yuan(t.worstGap)+" 元":"无")+metric("12 个月最低现金",yuan(t.minCash12))+metric("十年实际净资产",yuan(t.terminalReal))+'</div>'
    +'<details><summary>所选方案与并列方案的收支、还款和财富</summary>'+table(["指标（元，另注除外）",strategyId,compareId],[
      sr("12个月最低现金",t.minCash12,comp.minCash12),sr("36个月最低现金",t.minCash36,comp.minCash36),sr("120个月最低现金",t.minCash120,comp.minCash120),
      sr("已观察最坏缺口（截断后未知）",t.worstGap,comp.worstGap),sr("最后观察月剩余债务",t.endDebt,comp.endDebt),sr("最后观察月合同本息及固定费",t.endDue,comp.endDue),
      ["最后观察月偿债比",ratio(t.endDsr,t.endDsrInfinite),ratio(comp.endDsr,comp.endDsrInfinite)],
      ["峰值偿债比",ratio(t.peakDsr,t.peakDsrInfinite),ratio(comp.peakDsr,comp.peakDsrInfinite)],
      sr("提前还本",t.prepaid,comp.prepaid),sr("同动作撤去预付后对照：省息",t.interestSaved,comp.interestSaved),
      sr("预付导致首月现金变化",t.prepayCashChangeMonth1,comp.prepayCashChangeMonth1),sr("预付导致十年最低现金变化",t.prepayMinCashChange,comp.prepayMinCashChange),
      sr("租金减全部房产持有费，累计",t.rentNet,comp.rentNet),sr("房车交割净款，累计",t.saleNet,comp.saleNet),sr("金融交易已到账净款，累计",t.securityNet,comp.securityNet),
      sr("名义净资产最大峰谷回撤",t.drawdown,comp.drawdown),["峰谷回撤 / 正峰值",ratio(t.drawdownPct),ratio(comp.drawdownPct)],
      sr("恢复情景机会成本（共同可行集，实际元）",r.recoveryCost,rowById(compareId).recoveryCost),
      ...[12,36,60,120].flatMap(m=>[sr(m+"月名义净资产",t.points[m]?.nominal,comp.points[m]?.nominal),sr(m+"月实际净资产",t.points[m]?.real,comp.points[m]?.real)])
    ])+'</details></section><section class="panel"><h2 class="sectiontitle">行动次序</h2><p class="small">现金比较采用各情景最低月末可用现金。较稳健方案并列时取最坏十年实际净资产较高者。后悔额以共同可行集内该情景最高十年实际净资产为参照，报告跨情景最大差额。偿债比为合同当月到期款 / 当月到账收入及租金。</p>'
    +'<div class="scroll"><table><thead><tr><th>行动视角</th><th>方案</th><th>动作及月份</th></tr></thead><tbody>'+chosen+'</tbody></table></div>'
    +'<p class="small">现金、实际净资产及峰值偿债比同时参与 Pareto 比较。仅下列已运行候选参与排名。</p><div><b>跨情景可行短名单</b>　'+(study.shortlist.length?study.shortlist.map(pick).join(" "):"无")+'</div></section>'
    +'<section class="panel"><div class="cardhead"><h2 class="sectiontitle">全部候选</h2><span class="chip">'+c.evaluated+' / '+html(c.rawCombinations)+' 种原始组合</span></div><p class="small">'+html(c.method)+'。全部规则合计产生 '+c.distinctMonthlyTrajectories+' 种轨迹。相同情景中逐月现金、资产、债务和交易按分取整后完全相同，计作同一轨迹。短名单最多显示 15 种。</p>'
    +'<div class="selectrow">'+objectiveSelect()+'<label class="field">筛选<select id="filter">'+opts({all:"全部",feasible:"共同可行",pareto:"Pareto 非支配",failed:"未满足约束"},filter)+'</select></label>'
    +'<button id="allCSV">导出全部策略 CSV</button><button id="fullCSV">导出所有方案月表 CSV</button></div><div class="scroll tall"><table class="compact"><thead><tr><th>方案</th><th>共同可行</th><th>Pareto</th><th>最坏最低现金</th><th>最坏十年实际财富</th><th>最大后悔额</th><th>最坏资金需求</th><th>操作</th></tr></thead><tbody>'
    +selected.map(v=>'<tr class="'+(v.strategy.id===strategyId?"selected":"")+'"><td>'+pick(v.strategy.id)+'</td><td>'+(v.feasible?"是":"否")+'</td><td>'+(v.pareto?"✓":"")+'</td><td class="num">'+yuan(v.minCash)+'</td><td class="num">'+yuan(v.worstWealth)+'</td><td class="num">'+yuan(v.regret)+'</td><td class="num">'+yuan(v.funding)+'</td><td>'+html(E.nameOf(v.strategy))+'</td></tr>').join("")+'</tbody></table></div><details><summary>覆盖与未生成的动作</summary>'
    +table(["决策对象","选择数（含持有）"],c.dimensions.map(d=>[d.id,d.choices]))+table(["对象","原因"],c.exclusions.map(x=>[x.id,x.reason]))+'</details></section>';
  $("filter").onchange=e=>{filter=e.target.value;renderView();};$("allCSV").onclick=exportStrategies;$("fullCSV").onclick=()=>exportMonths(true);
  $("results").querySelectorAll("[data-pick]").forEach(b=>b.onclick=()=>{strategyId=b.dataset.pick;stressResult=null;renderView();});
}
function pick(id){return '<button class="tag" data-pick="'+html(id)+'">'+html(id)+'</button>';}
const chartFields={cash:["Available cash","Cash (CNY)"],netWorth:["Net worth","Net worth (CNY)"],debt:["Debt balance","Debt (CNY)"],regularDue:["Debt service","Payment (CNY)"]};
function chart(current,other,key){
  const vals=[...current,...other].map(r=>r[key]).filter(v=>v!=null&&Number.isFinite(v));
  if(!vals.length)return '<p class="small">此路径缺少可绘制的存续月份。</p>';
  const W=710,H=255,x0=82,x1=679,y0=37,y1=207,min=Math.min(0,...vals),max=Math.max(1,...vals),dx=m=>x0+(m-1)*(x1-x0)/119,dy=v=>y1-(v-min)/(max-min||1)*(y1-y0);
  const line=rows=>rows.filter(a=>a[key]!=null).map((r,i)=>(i?"L":"M")+dx(r.month).toFixed(1)+" "+dy(r[key]).toFixed(1)).join(" ");
  const label=n=>Math.abs(n)>=1e6?(n/1e6).toFixed(2)+"m":Math.abs(n)>=1e3?(n/1e3).toFixed(0)+"k":n.toFixed(0);
  const ticks=[0,1,2,3,4].map(j=>{const a=min+(max-min)*j/4,yy=dy(a);return '<line x1="'+x0+'" x2="'+x1+'" y1="'+yy+'" y2="'+yy+'" stroke="#d5ddd1"/><text x="'+(x0-10)+'" y="'+(yy+4)+'" text-anchor="end">'+label(a)+'</text>';}).join("");
  return '<svg class="chart" role="img" aria-label="'+chartFields[key][0]+' by month" viewBox="0 0 '+W+' '+H+'"><title>'+chartFields[key][0]+' by month</title><text x="11" y="20">'+chartFields[key][1]+'</text>'+ticks
    +[1,24,48,72,96,120].map(m=>'<text x="'+dx(m)+'" y="226" text-anchor="middle">'+m+'</text>').join("")+'<text x="360" y="248" text-anchor="middle">Month</text>'
    +'<path d="'+line(other)+'" fill="none" stroke="#b37a39" stroke-width="2.4" stroke-dasharray="6 5"/><path d="'+line(current)+'" fill="none" stroke="#13675d" stroke-width="2.8"/>'
    +'<line x1="395" y1="15" x2="417" y2="15" stroke="#13675d" stroke-width="3"/><text x="420" y="20">Selected</text><line x1="499" y1="15" x2="521" y2="15" stroke="#b37a39" stroke-dasharray="6 3"/><text x="526" y="20">Comparison</text></svg>';
}
function drawLedger(){
  const sel=rowById(strategyId),d=E.inspect(study,strategyId,scenarioId),other=E.inspect(study,compareId,scenarioId);
  const events=d.events.map(e=>[e.month,e.asset,e.note,yuan(e.amount)]);
  const actions=sel.strategy.actions;
  $("ledger").innerHTML='<section class="panel"><h2 class="sectiontitle">逐月台账</h2><div class="selectrow">'+scenarioSelect()+policySelect("selectedPlan",strategyId)+policySelect("comparePlan",compareId)
    +'<label class="field">图表指标<select id="chartKey">'+opts({cash:"可用现金",netWorth:"名义净资产",debt:"剩余债务",regularDue:"合同月供"},chartKey)+'</select></label></div>'+verdict(d.summary)+chart(d.rows,other.rows,chartKey)+'</section>'
    +'<section class="panel"><h2 class="sectiontitle">执行与到账</h2><p>'+html(E.nameOf(sel.strategy))+'</p><p class="small">挂牌与卖出指令和收款分开记录。月末结余是提前还款的资金来源。解押补差不够时继续持有，预付条件未满足时继续按合同付款，条件挂牌在触发前维持持有。</p>'
    +(events.length?table(["月","对象","动作 / 资金去向","金额（元）"],events):'<p class="small">本路径未产生处置或提前还款事件。</p>')
    +(d.summary.blocked.length?table(["月","对象","未执行原因","执行时资金还差"],d.summary.blocked.map(b=>[b.month,b.id,b.reason,yuan(b.need)])):"")
    +'<details><summary>各笔贷款逐期本息</summary>'+Object.entries(d.byLoan).map(([id,ls])=>'<details><summary>'+html(id)+'</summary>'+table(["月","利息实付","按期或结清本金","额外提前本金","欠本余额","合同年利率"],ls.map(x=>[x.month,yuan(x.interest),yuan(x.principal),yuan(x.prepay),yuan(x.balance),ratio(x.annualRate)]))+'</details>').join("")+'</details></section>'
    +'<section class="panel"><div class="cardhead"><h2 class="sectiontitle">月末收支与资产</h2><button id="oneCSV">导出当前月表 CSV</button></div><div class="scroll tall"><table class="compact"><thead><tr>'
    +["月","期初现金","税后收入","租金","证券到账","房车成交毛款","必要支出","可选支出","持有/替代","合同月供实付","交割还本息","额外提前还本","期末现金","待到账","剩余债务","应付款","当期缺口","名义净资产","实际净资产"].map(k=>'<th>'+k+'</th>').join("")+'</tr></thead><tbody>'
    +d.rows.map(z=>'<tr>'+[z.month,z.openingCash,z.income,z.rent,z.securityReceipts,z.saleGross,z.essential,z.discretionary,z.carry+z.replacement,z.interest+z.principal+z.loanFees,z.closingInterest+z.closingPrincipal,z.prepaid,z.cash,z.receivables,z.debt,z.arrears,z.unpaid,z.netWorth,z.realNetWorth].map(v=>'<td class="num">'+yuan(v)+'</td>').join("")+'</tr>').join("")+'</tbody></table></div><p class="small">现金勾稽最大绝对误差 '+html(d.summary.maxCashResidual.toExponential(2))+' 元，净资产变动勾稽 '+html(d.summary.maxNetResidual.toExponential(2))+' 元。完整 CSV 另列利息、各项手续费、实物与金融资产。</p></section>';
  $("chartKey").onchange=e=>{chartKey=e.target.value;renderView();};$("oneCSV").onclick=()=>exportMonths(false);
}
let revChoices={};
function drawReverse(){
  const hh=study.prepared.h,sel=(key,arr)=>'<label class="field">'+({incomeId:"中断的收入",propertyId:"租售对比房产",loanId:"预付贷款",financialId:"减持资产"}[key])+'<select data-rev="'+key+'">'
    +opts(Object.fromEntries(arr.map(a=>[a.id,(a.name||a.id)+" · "+a.id])),revChoices[key]||arr[0]?.id)+'</select></label>';
  $("reverse").innerHTML='<section class="panel"><h2 class="sectiontitle">逆向压力测试</h2><div class="selectrow">'+scenarioSelect()+policySelect("selectedPlan",strategyId)+'</div><p>对当前路径追加冲击，逐档重跑同一方案，找到第一次现金不足的已测水平。失业与延迟按整月，工资、房价、租金按一个百分点。</p>'
    +'<div class="selectrow">'+sel("incomeId",hh.incomes)+sel("propertyId",hh.properties.filter(p=>p.use!=="occupied"))+sel("loanId",hh.loans)+sel("financialId",hh.financial.filter(f=>f.kind!=="deposit"))+'</div><button class="primary" id="stressRun">计算压力边界</button><div id="stressOutput"></div></section>';
  const controls=$("reverse").querySelectorAll("[data-rev]");controls.forEach(n=>{revChoices[n.dataset.rev]=n.value;n.onchange=()=>{revChoices[n.dataset.rev]=n.value;stressResult=null;drawReverse();};});
  $("stressRun").onclick=()=>{
    $("stressRun").disabled=true;say("正在逐档重跑压力路径…");
    setTimeout(()=>{try{stressResult=E.reverse(h,scenarios.find(s=>s.id===scenarioId),rowById(strategyId).strategy,revChoices);drawStressOutput();say("逆向压力测试已完成。");}catch(e){say(e.message,true);}finally{$("stressRun").disabled=false;}},25);
  };
  if(stressResult)drawStressOutput();
}
function drawStressOutput(){
  const v=stressResult,rows=Object.values(v.grid).map(t=>{
    if(!t.applicable)return[t.label,"无适用收入、资产或挂牌动作","—","—","—"];
    const b=t.boundary;
    return [t.label+(t.target==="*"?"":" · "+t.target),b?b.value+t.unit:"测试至 "+t.limit+t.unit+" 仍可付清",b?b.failureMonth:"—",b?yuan(b.gap):"—",t.firstBlocked==null?"无":t.firstBlocked+t.unit+(t.nonmonotone?"；之后曾恢复履约":"")];
  });
  let out=table(["额外冲击","首次现金失败水平","失败月","缺口（元）","首次动作受阻水平"],rows);
  const b=v.breakEven,a=v.affordablePrepay;
  if(b)out+='<h3 class="sub">净租金与出售净款 · '+html(b.id)+'</h3>'+table(["交割月","卖房当月净款","持有期实际平均净租金/月","达到出售路径财富所需账面月租","相应平均净租金/月"],[[b.saleMonth??"—",yuan(b.saleNet),yuan(b.actualMonthlyNet),yuan(b.grossMonthlyThreshold),yuan(b.netMonthlyThreshold)]])
    +'<p class="small">以 120 月实际净资产、完整履约与储备为比较条件，出租路径保留期末房屋残值。搜索月租 '+yuan(b.testedRange[0])+' 至 '+yuan(b.testedRange[1])+' 元。'+html(b.reason)+'</p>';
  if(a)out+='<h3 class="sub">可承受提前还款 · '+html(a.id)+'</h3><p>'+(a.month==null?'窗口尚未确认':'第 '+a.month+' 月')+'，最高已验证预付款 <b>'+yuan(a.largestTested)+' 元</b>。'+(a.liquidityCeiling==null?html(a.reason):'现金允许上限 '+yuan(a.liquidityCeiling)+' 元。当月上限内按 50 档试算，最后可行区间细化至分，跨区间结果以已测试点为限。')+'</p>';
  const effects=[["金融资产一次转现金",v.liquidation],["用现金提前结清贷款",v.payoff]].filter(x=>x[1]);
  if(effects.length)out+='<h3 class="sub">与保持其他动作相同的反事实比较</h3>'+table(["动作 / 对象","保留可支撑月数","执行可支撑月数","首月现金变化","已观察最低现金变化","动作状态"],effects.map(([name,e])=>[name+" · "+e.id,e.holdingSupport,e.actionSupport,yuan(e.changeFirstCash),yuan(e.changeMinCash),e.blocked.length?e.blocked[0].reason:e.actionFeasible?"满足本路径约束":"现金或储备未满足"]));
  $("stressOutput").innerHTML=out;
}
function csvCell(v){
  if(v==null)return "";
  if(typeof v==="object")v=JSON.stringify(v);
  if(typeof v==="number")return Number.isFinite(v)?String(Number(v.toPrecision(14))):"Infinity";
  let s=String(v);if(/^[=+@-]/.test(s))s="'"+s;return '"'+s.replace(/"/g,'""')+'"';
}
const csvLine=arr=>arr.map(csvCell).join(",")+"\r\n";
function exportStrategies(){
  const keys=["completed","feasible","firstFailure","failureBreakdown","worstGap","supportMonths","minCash12","minCash36","minCash120","minCashObserved","maxReserveGap","maxBlockedFunding","endDebt","endDue","endDsr","endDsrInfinite","peakDsr","peakDsrInfinite","interestTotal","prepaid","interestSaved","prepayCashChangeMonth1","prepayMinCashChange","rentNet","saleNet","securityNet","drawdown","drawdownPct","terminalNominal","terminalReal","points","blocked"];
  const parts=["\ufeff",csvLine(["inputKind","strategy","actions","description","scenario","trajectoryGroup","commonFeasible","pareto","maxRegretReal","recoveryOpportunityCostReal",...keys])];
  for(const r of study.results)for(const [s,t] of Object.entries(r.outcomes))parts.push(csvLine([h.dataKind,r.strategy.id,r.strategy.actions,E.nameOf(r.strategy),s,r.trajectory,r.feasible,r.pareto,r.regret,r.recoveryCost,...keys.map(k=>t[k])]));
  download("household-strategies.csv",parts,"text/csv;charset=utf-8");say("已导出全部策略情景结果。");
}
function exportMonths(all){
  const button=$(all?"fullCSV":"oneCSV");button.disabled=true;say("正在生成逐月账表…");
  setTimeout(()=>{try{
    const strategies=all?study.results:[rowById(strategyId)],paths=all?scenarios:[scenarios.find(z=>z.id===scenarioId)],parts=["\ufeff"];
    let keys=null;
    for(const r of strategies)for(const s of paths){
      const rows=E.inspect(study,r.strategy.id,s.id).rows;
      if(!keys){keys=Object.keys(rows[0]);parts.push(csvLine(["inputKind","strategy","scenario","state",...keys]));}
      let str="";
      for(let m=1;m<=E.H;m++){
        const z=rows[m-1];str+=csvLine([h.dataKind,r.strategy.id,s.id,!z?"truncated":z.unpaid>0?"cash_failure":"observed",...keys.map(k=>z?z[k]:k==="month"?m:null)]);
      }
      parts.push(str);
    }
    download(all?"household-all-months.csv":"household-selected-months.csv",parts,"text/csv;charset=utf-8");say("月表 CSV 已生成。");
  }catch(e){say(e.message,true);}finally{button.disabled=false;}},25);
}
drawInputs();mark();say("填写可用现金与必要支出，或载入示例。");
