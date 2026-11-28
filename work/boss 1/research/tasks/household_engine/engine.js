/* Monthly CNY cash and contract ledger. Browser and CommonJS share this exact source. */
(function (root, factory) {
  "use strict";
  if (typeof module === "object" && module.exports) module.exports = factory();
  else root.HouseholdEngine = factory();
})(typeof globalThis === "object" ? globalThis : this, function () {
  "use strict";
  const H = 120, EPS = 1e-7;
  const clone = value => JSON.parse(JSON.stringify(value));
  const sum = (array, fn) => array.reduce((n, item) => n + fn(item), 0);
  const clip = (n, lo, hi) => Math.max(lo, Math.min(hi, n));
  const groupNames = ["incomes", "expenses", "financial", "properties", "vehicles", "loans"];
  const modes = {
    wageFactor: ["level","倍"], businessFactor: ["level","倍"], otherIncomeFactor: ["level","倍"],
    unemploymentMonths: ["event","月"], recoveryMonths: ["level","月"], reemploymentFactor: ["level","倍"],
    inflationAnnual: ["annual","年率小数"], cashRateDelta: ["annual","年率差"],
    loanRateDelta: ["annual","年率差"], propertyShock: ["shock","比例"], propertyAnnual: ["annual","年率小数"],
    rentFactor: ["level","倍"], vacancyAdd: ["level","比例差"], financialShock: ["shock","比例"],
    securityAnnual: ["annual","年率差"], concentrationHaircut: ["shock","比例"],
    saleHaircut: ["level","比例"], saleDelay: ["level","月"]
  };
  const option = (name, allowed, value) => {
    if (!allowed.includes(value)) throw Error(name + " 取值无效");
    return value;
  };
  function num(value, name, lo=-Infinity, hi=Infinity, integer=false) {
    if (typeof value !== "number" || !Number.isFinite(value) || value < lo || value > hi || (integer && !Number.isInteger(value)))
      throw Error(name + " 需要范围内的" + (integer ? "整数" : "数字") + "（空值需填写）");
    return value;
  }
  function valueFor(value, choice, name) {
    if (!value || typeof value !== "object" || Array.isArray(value)) return value;
    const lo = num(value.low, name + ".low"), hi = num(value.high, name + ".high", lo);
    if (value.base != null) num(value.base, name + ".base", lo, hi);
    if (choice === "low") return lo;
    if (choice === "high") return hi;
    if (value.base == null) throw Error(name + " 需要填写中心值或选择区间端点");
    return value.base;
  }
  const amount = (name, value, choice, lo=0, hi=1e15) => num(valueFor(value, choice, name), name, lo, hi);
  const bool = (value,name) => {if (typeof value !== "boolean") throw Error(name+" 需要是/否"); return value;};
  const monthlyRate = r => Math.expm1(Math.log1p(r) / 12);
  const idPattern = /^[A-Za-z\u3400-\u9fff0-9][A-Za-z\u3400-\u9fff0-9_.-]{0,59}$/;
  const blank = () => ({
    schema:"household-cny.v1", dataKind:"household", rangeCase:"base", cash:null, cashAnnual:0,
    reserveMonths:0, minimumLiving:null, cutFraction:0, maxSaleWait:120, preference:"cash",
    incomes:[], expenses:[], financial:[], properties:[], vehicles:[], loans:[], citySources:[]
  });
  const templates = {
    incomes:{id:"",name:"",kind:"wage",monthly:null,from:1,to:120,every:1,annualGrowth:0,stability:"未填写",
      stressJob:false,jobStart:1,jobMonths:0,jobPayFraction:0,recoveryMonths:0,returnFraction:1},
    expenses:{id:"",name:"",kind:"necessary",monthly:null,from:1,to:120,every:1,annualGrowth:0,inflationLinked:true},
    financial:{id:"",name:"",kind:"stock",value:null,annualReturn:0,concentration:0,fee:null,settle:null,
      unlock:null,maturity:null,restriction:"unknown",purpose:""},
    properties:{id:"",name:"",city:"",type:"",use:"idle",value:null,saleValue:null,saleLag:null,lock:null,
      canSell:null,rent:null,vacancy:0,leaseLag:0,discountRent:0.10,discountLeaseLag:0,
      carry:null,saleFee:null,closingFee:null,replacementAllowed:false,replacementMonthly:null,sourceId:""},
    vehicles:{id:"",name:"",value:null,saleValue:null,annualDepreciation:0,saleLag:null,lock:null,canSell:null,
      necessary:null,replacementAllowed:false,replacementMonthly:null,carry:null,saleFee:null,closingFee:null},
    loans:{id:"",name:"",kind:"mortgage",collateral:"",principal:null,annualRate:null,rateType:"fixed",
      resetFirst:12,resetEvery:12,months:null,method:"annuity",payment:null,canPrepay:null,prepayFrom:null,
      prepayMin:null,prepayFee:null,settlementFee:null,transferWithLien:null,allowRecast:null,allowShorten:null,
      start:1,monthlyFee:0}
  };
  function validateHousehold(input) {
    if (!input || input.schema !== "household-cny.v1") throw Error("家庭输入格式应为 household-cny.v1");
    const h = clone(input), choice=option("区间端点",["low","base","high"],h.rangeCase);
    option("输入类型",["household","synthetic_example"],h.dataKind);
    option("目标",["cash","wealth","debt","regret"],h.preference);
    h.cash=amount("期初现金",h.cash,choice); h.minimumLiving=amount("最低生活",h.minimumLiving,choice);
    h.cashAnnual=amount("现金年利率",h.cashAnnual,choice,-0.99,5);
    h.reserveMonths=num(h.reserveMonths,"储备月数",0,H,true);
    h.cutFraction=amount("可削减比例",h.cutFraction,choice,0,1);
    h.maxSaleWait=num(h.maxSaleWait,"可接受成交等待",0,H,true);
    const ids=new Set();
    for(const g of groupNames) {
      if(!Array.isArray(h[g]) || h[g].length>100) throw Error(g+" 应为不超过100条的清单");
      h[g]=h[g].map(original=>{
        if(!original || typeof original!=="object") throw Error(g+" 条目无效");
        const x=Object.assign({},templates[g],original);
        if(!idPattern.test(x.id)||ids.has(x.id)) throw Error("ID 为空、重复或有非法字符："+String(x.id));
        ids.add(x.id);
        if(typeof x.name!=="string") throw Error(x.id+" 名称无效");
        const n=(k,lo=0,hi=1e15)=>x[k]=amount(x.id+"."+k,x[k],choice,lo,hi);
        const integer=(k,lo,hi)=>x[k]=num(x[k],x.id+"."+k,lo,hi,true);
        const b=k=>bool(x[k],x.id+"."+k);
        const optional=(fn,k,...bounds)=>{if(x[k]!=null)fn(k,...bounds);};
        if (g==="incomes" || g==="expenses") {
          n("monthly"); integer("from",1,H);integer("to",x.from,H);integer("every",1,H);
          n("annualGrowth",-.99,5);
          if(g==="incomes") {
            option("收入类别",["wage","bonus","business","other"],x.kind);b("stressJob");
            integer("jobStart",1,H);integer("jobMonths",0,H);integer("recoveryMonths",0,H);
            n("jobPayFraction",0,1);n("returnFraction",0,5);
          } else {
            option("支出类别",["necessary","education","medical","elder","insurance","discretionary","emergency"],x.kind);b("inflationLinked");
          }
        } else if(g==="financial") {
          option("金融类别",["deposit","instant","stock","fund","bond","gold","other"],x.kind);
          option("用途限制",["unknown","free","restricted","pledged"],x.restriction);
          n("value");n("annualReturn",-.99,5);n("concentration",0,1);optional(n,"fee",0,1);
          optional(integer,"settle",0,H);optional(integer,"unlock",1,1200);optional(integer,"maturity",0,1200);
        } else if(g==="properties"||g==="vehicles") {
          n("value");optional(n,"saleValue");n("carry");optional(n,"closingFee");optional(n,"saleFee",0,1);
          optional(integer,"saleLag",0,1200);optional(integer,"lock",1,1200);optional(b,"canSell");b("replacementAllowed");
          if(x.replacementMonthly!=null)n("replacementMonthly");
          if(g==="properties") {
            option("房产用途",["occupied","let","idle"],x.use);n("rent");n("vacancy",0,1);
            integer("leaseLag",0,1200);n("discountRent",0,1);integer("discountLeaseLag",0,1200);
          }else{n("annualDepreciation",0,.99);optional(b,"necessary");}
          if(x.replacementAllowed&&x.replacementMonthly==null)throw Error(x.id+" 请填写替代支出（可填0）");
        }else{
          option("债务类别",["mortgage","car","consumer","card","business","family","margin","guarantee","other"],x.kind);
          option("还款方式",["annuity","principal","bullet"],x.method);option("利率类型",["fixed","floating"],x.rateType);
          n("principal");n("annualRate",0,5);integer("months",1,1200);integer("resetFirst",1,1200);
          integer("resetEvery",1,1200);optional(integer,"prepayFrom",1,1200);integer("start",1,1200);
          if(x.kind!=="guarantee" && x.start!==1)throw Error(x.id+" 普通债务从期初入账；仅担保可设代偿月");
          for(const k of ["canPrepay","transferWithLien","allowRecast","allowShorten"])optional(b,k);
          for(const k of ["prepayMin","settlementFee"])optional(n,k);n("monthlyFee");
          optional(n,"prepayFee",0,1);
          if(x.payment!=null){n("payment");if(x.method!=="annuity")throw Error(x.id+" 自定固定月供仅适用等额本息");}
          if(x.payment!=null&&x.principal>0&&x.payment<=x.principal*x.annualRate/12)throw Error(x.id+" 约定月供须足以支付利息并还本");
        }
        return x;
      });
    }
    const assets=new Set([...h.properties,...h.vehicles,...h.financial].map(x=>x.id));
    h.loans.forEach(l=>{if(l.collateral&&!assets.has(l.collateral))throw Error(l.id+" 关联资产不存在："+l.collateral);});
    h.financial.forEach(a=>{if(a.restriction==="pledged"&&!h.loans.some(l=>l.collateral===a.id))throw Error(a.id+" 质押状态需关联贷款，可改为受限用途");});
    if(!Array.isArray(h.citySources))throw Error("城市资料应为清单");
    h.citySources.forEach(c=>{for(const k of ["id","city","period","source","scope"])if(typeof c[k]!=="string"||!c[k].trim())throw Error("城市资料缺字段 "+k);});
    return h;
  }
  function validateScenario(input, choice="base") {
    if(!input||!idPattern.test(input.id)||typeof input.name!=="string"||!Array.isArray(input.paths))throw Error("情景需要 ID、名称和 paths 清单");
    const s=clone(input), by={};
    for(const p of s.paths) {
      if(!Object.hasOwn(modes,p.key)||!modes[p.key].includes(p.mode)||p.mode!==modes[p.key][0])throw Error("不支持的情景参数或施加方式 "+p.key);
      if(typeof p.sourceId!=="string"||!p.sourceId.trim()||p.unit!==modes[p.key][1]||typeof p.editable!=="boolean")throw Error("情景缺少来源、单位或可编辑字段 "+p.key);
      option("假设类型",["observed","historical","research_estimate","stress_test"],p.assumption);
      num(p.start,"情景起点",1,H,true);num(p.duration,"情景时长",1,H,true);
      if(!Array.isArray(p.range)||p.range.length!==2)throw Error("情景需给区间 "+p.key);
      const [lo,hi]=p.range;num(lo,"范围下限");num(hi,"范围上限",lo);
      p.value=num(valueFor(p.value,choice,p.key),p.key,lo,hi);
      if(["unemploymentMonths","recoveryMonths","saleDelay"].includes(p.key))num(p.value,p.key,0,H,true);
      if(["wageFactor","businessFactor","otherIncomeFactor","rentFactor","reemploymentFactor"].includes(p.key))num(p.value,p.key,0,10);
      if(["saleHaircut","concentrationHaircut"].includes(p.key))num(p.value,p.key,0,1);
      if(["propertyShock","financialShock","vacancyAdd"].includes(p.key))num(p.value,p.key,-1,p.key==="vacancyAdd"?1:5);
      if(["propertyAnnual","inflationAnnual"].includes(p.key))num(p.value,p.key,-.99,5);
      if(["loanRateDelta","cashRateDelta","securityAnnual"].includes(p.key))num(p.value,p.key,-5,5);
      p.target=p.target||"*";
      if(p.target!=="*"&&!idPattern.test(p.target))throw Error("情景目标 ID 无效");
      const effectiveDuration=["event","shock"].includes(p.mode)?1:p.duration;
      if(effectiveDuration!==p.duration)throw Error("单次事件/水平冲击的 duration 必须等于1");
      const list=by[p.key]||(by[p.key]=[]);
      if(list.some(old=>old.target===p.target&&p.start<old.start+old.duration&&old.start<p.start+p.duration))throw Error("同一目标的情景参数存在重叠 "+p.key);
      list.push(p);
    }
    return {...s,by};
  }
  function parameter(s,key,m,id,def=0) {
    const group=s.by[key];if(!group)return def;
    let wildcard;
    for(const p of group)if(m>=p.start&&m<p.start+p.duration){if(id&&p.target===id)return p.value;if(p.target==="*")wildcard=p.value;}
    return wildcard==null?def:wildcard;
  }
  function amortPayment(p,r,n){return r===0?p/n:p*r/-Math.expm1(-n*Math.log1p(r));}
  function newLoan(c) {
    return {c,balance:c.start===1?c.principal:0,rate:c.annualRate/12,end:c.start+c.months-1,
      payment:c.payment==null?amortPayment(c.principal,c.annualRate/12,c.months):c.payment,
      principalStep:c.principal/c.months,everActive:c.start===1};
  }
  function loanDue(l,m,s) {
    const c=l.c;
    if(!l.everActive&&m===c.start){l.balance=c.principal;l.everActive=true;}
    if(l.balance<=EPS)return {interest:0,principal:0,fee:0};
    const age=m-c.start+1, remaining=Math.max(1,l.end-m+1);
    if(c.rateType==="floating"&&age>=c.resetFirst&&(age-c.resetFirst)%c.resetEvery===0){
      l.rate=Math.max(0,c.annualRate+parameter(s,"loanRateDelta",m,c.id))/12;
      l.payment=amortPayment(l.balance,l.rate,remaining);
    }
    const interest=l.balance*l.rate;
    let principal;
    if(remaining===1)principal=l.balance;
    else if(c.method==="bullet")principal=0;
    else if(c.method==="principal")principal=l.principalStep;
    else principal=Math.max(0,l.payment-interest);
    return {interest,principal:Math.min(l.balance,principal),fee:c.monthlyFee};
  }
  function recast(l,mode,m) {
    const n=Math.max(1,l.end-m);
    if(l.balance<=EPS){l.balance=0;return;}
    if(mode==="recast"){
      l.payment=amortPayment(l.balance,l.rate,n);l.principalStep=l.balance/n;
    } else if(mode==="shorten"){
      let years=n;
      if(l.c.method==="principal")years=Math.ceil(l.balance/l.principalStep-1e-10);
      else if(l.c.method==="annuity")years=l.rate===0?Math.ceil(l.balance/l.payment-1e-10):Math.ceil(-Math.log1p(-l.balance*l.rate/l.payment)/Math.log1p(l.rate)-1e-10);
      l.end=m+Math.max(1,Math.min(n,years));
    }
  }
  function incomeAt(i,m,s) {
    if(m<i.from||m>i.to||(m-i.from)%i.every)return 0;
    const key={wage:"wageFactor",bonus:"wageFactor",business:"businessFactor",other:"otherIncomeFactor"}[i.kind];
    let factor=Infinity;
    const jobs=i.jobMonths?[{start:i.jobStart,length:i.jobMonths,rec:i.recoveryMonths,ret:i.returnFraction}]:[];
    for(const p of s.by.unemploymentMonths||[]){
      if(p.value<=0 || !(p.target===i.id || (p.target==="*"&&i.stressJob)))continue;
      jobs.push({start:p.start,length:p.value,rec:parameter(s,"recoveryMonths",p.start,i.id,i.recoveryMonths),ret:parameter(s,"reemploymentFactor",p.start,i.id,i.returnFraction)});
    }
    for(const j of jobs){
      const elapsed=m-j.start;
      if(elapsed<0)continue;
      const since=elapsed-j.length;
      const wage=since<0?i.jobPayFraction:j.rec>0&&since<j.rec?i.jobPayFraction+(j.ret-i.jobPayFraction)*(since+1)/j.rec:j.ret;
      factor=Math.min(factor,wage);
    }
    return i.monthly*Math.pow(1+i.annualGrowth,(m-i.from)/12)*(factor===Infinity?1:factor)*parameter(s,key,m,i.id,1);
  }
  function expensesAt(h,m,cpi) {
    let living=0,recurring=0,emergency=0,disc=0;
    for(const e of h.expenses) {
      if(m<e.from||m>e.to||(m-e.from)%e.every)continue;
      const val=e.monthly*Math.pow(1+e.annualGrowth,(m-e.from)/12)*(e.inflationLinked?cpi:1);
      if(e.kind==="discretionary")disc+=val;else if(e.kind==="necessary")living+=val;else if(e.kind==="emergency")emergency+=val;else recurring+=val;
    }
    const reserveBase=Math.max(h.minimumLiving*cpi,living)+recurring;
    return {required:reserveBase+emergency,reserveBase,disc};
  }
  function securityRestriction(c){
    if(c.restriction==="restricted")return "资金用途受限";
    if(c.restriction==="unknown"||c.fee==null||c.settle==null||c.unlock==null||(c.kind==="deposit"&&c.maturity==null))
      return "交易用途、费用、到账时间、解锁条件或定存到期日尚未确认";
    return "";
  }
  function availableOnDate(c,m){
    return !securityRestriction(c)&&m>=c.unlock&&(!c.maturity||m>=c.maturity);
  }
  function activeLiens(id,loans){return loans.filter(l=>l.c.collateral===id&&l.balance>EPS);}
  function replacement(c){return c.use==="occupied"||c.necessary===true;}
  function saleRestriction(c){
    if(c.canSell!==true)return c.canSell===false?"明确限制出售":"出售许可尚未确认";
    if([c.saleValue,c.saleFee,c.closingFee,c.saleLag,c.lock].some(v=>v==null))return "保守成交价、交易费用、等待月数或解锁月尚未确认";
    if(c.use==null&&c.necessary==null)return "车辆通勤或生产必要性尚未确认";
    if(replacement(c)&&!c.replacementAllowed)return "缺少可行的住房或通勤替代";
    return "";
  }
  function prepayRestriction(c,mode){
    if(c.canPrepay!==true)return c.canPrepay===false?"合同禁止提前还款":"提前还款许可尚未确认";
    if(c.prepayFrom==null||c.prepayFee==null)return "提前还款窗口或费率尚未确认（零费率也须填写）";
    if(mode==="full")return c.settlementFee==null?"结清固定费用尚未确认（零费用也须填写）":"";
    const permission=mode==="recast"?c.allowRecast:c.allowShorten;
    if(permission!==true)return permission===false?"合同禁止该种部分预付方式":"该种部分预付方式许可尚未确认";
    if(c.prepayMin==null)return "最低部分预付金额尚未确认";
    return c.method==="bullet"?"到期还本合同没有可重摊的定期本金":"";
  }
  function checkActions(h,strategy) {
    if(!strategy||!Array.isArray(strategy.actions))throw Error("策略需要 actions");
    const ids=a=>new Set(a.map(x=>x.id)),real=ids([...h.properties,...h.vehicles]),props=ids(h.properties),fin=ids(h.financial),liab=ids(h.loans);
    const occupied=new Set(), expenseAction=new Set();
    for(const a of strategy.actions) {
      num(a.month,"动作月",1,H,true);
      if(a.kind==="list"||a.kind==="rent") {
        if(!(a.kind==="list"?real:props).has(a.asset))throw Error("处置对象不存在");
        if(a.kind==="rent")bool(a.discount,"议租折让");
        if(occupied.has(a.asset))throw Error("同一实物资产动作重复");
        occupied.add(a.asset);
      }else if(a.kind==="liquidate"){
        if(!fin.has(a.asset))throw Error("金融资产不存在");
        if(occupied.has(a.asset))throw Error("同一金融资产动作重复");
        occupied.add(a.asset);
        option("证券操作",["all","stages","reserve"],a.mode);
      }else if(a.kind==="prepay"){
        if(!liab.has(a.loan))throw Error("债务不存在");
        option("提前还款",["full","recast","shorten"],a.mode);
        if(a.mode!=="full")num(a.amount,"提前还款额",EPS,1e15);
        if(occupied.has(a.loan))throw Error("同一贷款动作重复");
        occupied.add(a.loan);
      }else if(a.kind==="cut"){
        if(expenseAction.size)throw Error("支出动作重复");expenseAction.add("cut");num(a.fraction,"削减比例",0,h.cutFraction);
      }else throw Error("未知动作 "+a.kind);
      if(a.trigger!=null)option("触发规则",["now","reserve"],a.trigger);
      if(a.buffer!=null)num(a.buffer,"触发储备月数",0,H,true);
    }
  }
  function execute(h,s,strategy,detail=false,tracePool=null) {
    const actions=strategy.actions, loans=h.loans.map(newLoan);
    const assets=[...h.properties,...h.vehicles].map(c=>({c,property:c.use!=null,owned:true,mark:c.value,saleMark:c.saleValue,
      listed:null,sold:null,leaseFrom:c.use==="let"?1:null,rentFraction:1}));
    const securities=h.financial.map(c=>({c,mark:c.value,units:c.value?1:0}));
    const assetMap=new Map(assets.map(x=>[x.c.id,x])), secMap=new Map(securities.map(x=>[x.c.id,x]));
    const loanMap=new Map(loans.map(x=>[x.c.id,x])), pending=[], rows=[], events=[], blocked=[];
    const finished=new Set(), blockers=new Set(), byLoan=Object.fromEntries(loans.map(l=>[l.c.id,[]]));
    const propertyFlows=Object.fromEntries(assets.filter(z=>z.property).map(z=>[z.c.id,{rent:0,carry:0,saleNet:0}]));
    const event=(m,asset,type,note,amount=0)=>{if(detail)events.push({month:m,asset,type,note,amount});};
    const reject=(m,id,reason,need=0)=>{
      const signature=id+"|"+reason;
      if(!blockers.has(signature)){blocked.push({month:m,id,reason,need});blockers.add(signature);event(m,id,"blocked",reason,need);}
    };
    let lastCut=0,cash=h.cash,cpi=1,receivables=0,arrears=0,failed=null,maxReserveGap=0,peak=0,drawdown=0,drawdownPct=null;
    let peakDsr=0,peakDsrInfinite=false,interestTotal=0,rentNet=0,saleNet=0,prepaid=0,securityNet=0;
    const openingDebt=sum(loans,l=>l.balance),openingNet=h.cash+sum(assets,a=>a.mark)+sum(securities,f=>f.mark*f.units)-openingDebt;
    peak=openingNet;
    let maxCashResidual=0,maxNetResidual=0;
    for(let m=1;m<=H;m++){
      const open=cash,oldDebt=sum(loans,l=>l.balance),oldFin=sum(securities,z=>z.mark*z.units)+receivables,
        oldReal=sum(assets,a=>a.owned?a.mark:0),oldArrears=arrears;
      const inc={income:0,rent:0,cashInterest:0,securityReceipts:0,saleGross:0};
      const out={essential:0,discretionary:0,carry:0,replacement:0,interest:0,principal:0,loanFees:0,
        closingInterest:0,closingPrincipal:0,saleFees:0,releaseFees:0,prepaid:0,prepayFees:0};
      let tradeloss=0,assetDisposalDifference=0,gains=0,called=0,unpaid=0,missedPrincipal=0,missedDebtService=0,unfundedEssential=0,unfundedDiscretionary=0;
      function pay(k,x){const available=Math.max(0,cash),paid=Math.min(available,Math.max(0,x));cash-=paid;out[k]+=paid;return paid;}
      function receive(k,x){inc[k]+=x;cash+=x;}
      const due=new Map();
      for(const l of loans){const already=l.everActive;due.set(l.c.id,loanDue(l,m,s));if(!already&&l.everActive)called+=l.balance;}
      cpi*=1+monthlyRate(parameter(s,"inflationAnnual",m,""));
      const budget=expensesAt(h,m,cpi), triggerMonths=a=>a.buffer==null?h.reserveMonths:a.buffer;
      const triggered=a=>a.trigger!=="reserve"||open<=budget.reserveBase*triggerMonths(a)+EPS;
      const scheduledDue=()=>sum(loans,l=>{const d=due.get(l.c.id);return d.interest+d.principal+d.fee;});
      const cashRate=Math.max(-.99,h.cashAnnual+parameter(s,"cashRateDelta",m,""));
      receive("cashInterest",open*monthlyRate(cashRate));receive("income",sum(h.incomes,i=>incomeAt(i,m,s)));
      for(let j=pending.length-1;j>=0;j--)if(pending[j].month===m){
        receive("securityReceipts",pending[j].net);receivables-=pending[j].net;securityNet+=pending[j].net;
        event(m,pending[j].id,"settle","净交易款到账",pending[j].net);pending.splice(j,1);
      }
      for(const a of assets)if(a.owned){
        let multiplier;
        if(a.property)multiplier=(1+monthlyRate(parameter(s,"propertyAnnual",m,a.c.id)))*(1+parameter(s,"propertyShock",m,a.c.id));
        else multiplier=1+monthlyRate(-a.c.annualDepreciation);
        gains+=a.mark*(multiplier-1);a.mark*=multiplier;if(a.saleMark!=null)a.saleMark*=multiplier;
      }
      for(const a of securities)if(a.units>EPS){
        const market=!["deposit","instant"].includes(a.c.kind);
        const annual=Math.max(-.99,a.c.annualReturn+(market?parameter(s,"securityAnnual",m,a.c.id):0));
        const factor=(1+monthlyRate(annual))*(market?1+parameter(s,"financialShock",m,a.c.id):1)
          *(market?1-a.c.concentration*parameter(s,"concentrationHaircut",m,a.c.id):1);
        gains+=a.mark*a.units*(factor-1);a.mark*=factor;
      }
      function trade(z,units){
        units=Math.min(z.units,Math.max(0,units));if(units<=EPS)return;
        const gross=z.mark*units,fee=gross*z.c.fee,net=gross-fee;tradeloss+=fee;z.units-=units;
        if(z.units<EPS)z.units=0;
        if(z.c.settle===0){receive("securityReceipts",net);securityNet+=net;}
        else{pending.push({month:m+z.c.settle,net,id:z.c.id});receivables+=net;}
        event(m,z.c.id,"trade","卖出/到期，到账月 "+(m+z.c.settle),net);
      }
      function closingQuote(id,netOfAssetFees){
        const linked=activeLiens(id,loans),parts=[];
        let subtotal=0,priorFunding=0;
        for(const l of linked){
          const c=l.c,d=due.get(c.id),early=m<l.end;
          const reason=early?prepayRestriction(c,"full"):(c.settlementFee==null?"结清固定费用尚未确认":"");
          if(reason||c.transferWithLien==null||(early&&m-c.start+1<c.prepayFrom))
            return {reason:reason||(c.transferWithLien==null?"解押付款方式尚未确认":"交割时尚未到合同提前还款窗口"),need:0};
          const fees=c.settlementFee+(early?l.balance*c.prepayFee:0),total=l.balance+d.interest+d.fee+fees;
          subtotal+=total;if(c.transferWithLien===false)priorFunding+=total;
          parts.push({l,d,fees});
        }
        const needed=Math.max(0,priorFunding,subtotal-netOfAssetFees);
        return {parts,subtotal,need:Math.max(0,needed-cash),reason:cash+EPS<needed?"交割前资金不足（补差或先行解押）":""};
      }
      function retireLiens(quote){
        for(const {l,d,fees} of quote.parts){
          pay("releaseFees",fees);pay("loanFees",d.fee);pay("closingInterest",d.interest);
          const paid=pay("closingPrincipal",l.balance);l.balance=Math.max(0,l.balance-paid);
          if(l.balance<EPS)l.balance=0;
          if(detail)byLoan[l.c.id].push({month:m,principal:paid,interest:d.interest,balance:l.balance,annualRate:l.rate*12,settled:true});
          due.set(l.c.id,{interest:0,principal:0,fee:0});
        }
      }
      function settlePledged(z){
        const order=z.lienOrder,gross=order.gross,fee=gross*z.c.fee,net=gross-fee;
        z.lienOrder=null;
        const quote=closingQuote(z.c.id,net);
        if(quote.reason){reject(m,z.c.id,quote.reason+"，质押交易未交割，保留持仓",quote.need);return;}
        assetDisposalDifference+=gross-z.mark*z.units;tradeloss+=fee;z.units=0;
        receive("securityReceipts",net);securityNet+=net;retireLiens(quote);
        event(m,z.c.id,"settle","质押证券交割并结清关联债务，家庭可得净款",net-quote.subtotal);
      }
      function orderFull(z){
        const liens=activeLiens(z.c.id,loans);
        if(!liens.length){trade(z,z.units);return;}
        if(liens.some(l=>l.c.transferWithLien!==true)){
          reject(m,z.c.id,"尚有质押余额且未明确允许用交易款同步解押，请先结清杠杆",0);return;
        }
        const settleMonth=m+z.c.settle;
        if(settleMonth>H){reject(m,z.c.id,"质押交割超出可评估期限，继续持有");return;}
        const denied=liens.find(l=>settleMonth<l.end&&(prepayRestriction(l.c,"full")||settleMonth-l.c.start+1<l.c.prepayFrom));
        if(denied){reject(m,z.c.id,prepayRestriction(denied.c,"full")||"质押成交时尚未到提前还款窗口");return;}
        z.lienOrder={month:settleMonth,gross:z.mark*z.units};
        event(m,z.c.id,"pledged_order","整笔质押交易，锁定报价并等待第 "+settleMonth+" 月同步解押；交割前无可用卖款",z.lienOrder.gross);
        if(settleMonth===m)settlePledged(z);
      }
      for(const z of securities){
        if(z.lienOrder?.month===m)settlePledged(z);
        if(z.units>EPS&&!z.lienOrder&&z.c.kind==="deposit"&&z.c.maturity>0&&m>=z.c.maturity&&availableOnDate(z.c,m)){
          if(!activeLiens(z.c.id,loans).length)trade(z,z.units);
        }
      }
      for(const a of actions) {
        if(m<a.month || finished.has(a))continue;
        if(a.kind==="liquidate"){
          const z=secMap.get(a.asset);
          if(z.units<=EPS||z.lienOrder){finished.add(a);continue;}
          if(!availableOnDate(z.c,m)){
            reject(m,z.c.id,securityRestriction(z.c)||"交易尚未解锁或未到期，继续持有");
            if(a.mode!=="reserve")finished.add(a);continue;
          }
          let units=z.units;
          if(a.mode==="stages"){
            const offset=m-a.month;
            if(offset%3||offset>9)continue;
            units=Math.min(.25,z.units);
          }else if(a.mode==="reserve"){
            const cashNeed=budget.required+budget.reserveBase*triggerMonths(a)+budget.disc+scheduledDue()-cash;
            if(cashNeed<=EPS)continue;
            const inTransit=sum(pending,p=>p.id===a.asset?p.net:0);
            if(cashNeed-inTransit<=EPS)continue;
            units=z.mark*(1-z.c.fee)>0?(cashNeed-inTransit)/(z.mark*(1-z.c.fee)):z.units;
          }
          if(a.mode==="all"){orderFull(z);finished.add(a);continue;}
          if(activeLiens(z.c.id,loans).length){
            reject(m,z.c.id,"分批交易缺少部分解除质押安排，保留持仓");if(a.mode==="stages")finished.add(a);continue;
          }
          trade(z,units);if(z.units<=EPS)finished.add(a);
        }else if(a.kind==="list"||a.kind==="rent"){
          const z=assetMap.get(a.asset),c=z.c;
          if(!triggered(a))continue;
          finished.add(a);
          if(a.kind==="rent"){
            if(!z.property||c.use!=="idle"){reject(m,c.id,"仅闲置房允许新增出租");continue;}
            z.rentFraction=a.discount?1-c.discountRent:1;
            z.leaseFrom=m+(a.discount?c.discountLeaseLag:c.leaseLag);
            event(m,c.id,"lease","起租月 "+z.leaseFrom+"；议租比例 "+z.rentFraction);continue;
          }
          const lag=c.saleLag+parameter(s,"saleDelay",m,c.id);
          const restriction=saleRestriction(c);
          if(restriction||m<c.lock||lag>h.maxSaleWait||m+lag>H){
            reject(m,c.id,(restriction||"锁定、成交等待期限或评估期限不允许")+"，继续持有");continue;
          }
          z.listed=m+lag;event(m,c.id,"list","预计交割月 "+z.listed);
        }
      }
      for(const z of assets)if(z.owned&&z.listed===m){
        const c=z.c,gross=z.saleMark*(1-parameter(s,"saleHaircut",m,c.id)),fee=gross*c.saleFee+c.closingFee;
        const quote=closingQuote(c.id,gross-fee);
        if(quote.reason){
          reject(m,c.id,quote.reason+"，继续持有",quote.need);z.listed=null;continue;
        }
        receive("saleGross",gross);pay("saleFees",fee);retireLiens(quote);
        const net=gross-fee-quote.subtotal;saleNet+=net;if(z.property)propertyFlows[c.id].saleNet+=net;assetDisposalDifference+=gross-z.mark;
        z.owned=false;z.sold=m;event(m,c.id,"close","交割，扣交易成本和关联债务后",net);
      }
      let ownershipCosts=0,replaceCosts=0;
      for(const z of assets) {
        const c=z.c;
        if(!z.owned){if(replacement(c))replaceCosts+=c.replacementMonthly*cpi;continue;}
        ownershipCosts+=c.carry*cpi;if(z.property)propertyFlows[c.id].carry+=c.carry*cpi;
        if(z.property&&z.leaseFrom!==null&&m>=z.leaseFrom){
          const rent=c.rent*z.rentFraction*parameter(s,"rentFactor",m,c.id,1)*(1-clip(c.vacancy+parameter(s,"vacancyAdd",m,c.id),0,1));
          receive("rent",rent);propertyFlows[c.id].rent+=rent;
        }
      }
      let cut=0;
      for(const a of actions)if(a.kind==="cut"&&m>=a.month&&triggered(a))cut=a.fraction;
      if(cut!==lastCut){event(m,"discretionary","cut",cut>0?"按规则削减本月可选开支":"现金条件恢复，回到原可选开支",budget.disc*cut);lastCut=cut;}
      const disc=budget.disc*(1-cut);
      function obligation(k,x,isPrincipal=false) {
        const paid=pay(k,x),gap=Math.max(0,x-paid);
        unpaid+=gap;
        if(isPrincipal){missedPrincipal+=gap;missedDebtService+=gap;}
        else if(k==="loanFees"||k==="interest"){arrears+=gap;missedDebtService+=gap;}
        else if(k==="discretionary")unfundedDiscretionary+=gap;
        else{unfundedEssential+=gap;if(k==="carry"||k==="replacement")arrears+=gap;}
        return paid;
      }
      obligation("essential",budget.required);obligation("carry",ownershipCosts);obligation("replacement",replaceCosts);
      let regularDue=0;
      for(const l of loans){
        const d=due.get(l.c.id);
        if(!d.interest&&!d.principal&&!d.fee)continue;
        regularDue+=d.interest+d.principal+d.fee;
        obligation("loanFees",d.fee);const interest=obligation("interest",d.interest);
        const principal=obligation("principal",d.principal,true);l.balance=Math.max(0,l.balance-principal);
        if(l.balance<EPS)l.balance=0;
        if(detail)byLoan[l.c.id].push({month:m,principal,interest,balance:l.balance,annualRate:l.rate*12,settled:false});
      }
      obligation("discretionary",disc);
      const reserve=budget.reserveBase*h.reserveMonths;
      if(unpaid<EPS)for(const a of actions)if(a.kind==="prepay"&&m===a.month){
        const l=loanMap.get(a.loan),c=l.c;
        if(l.balance<=EPS){if(!l.everActive)reject(m,c.id,"担保尚未触发，无法预付");else event(m,c.id,"superseded","债务已偿清，保留现金");continue;}
        const p=a.mode==="full"?l.balance:a.amount;
        const restriction=prepayRestriction(c,a.mode)||(p>=l.balance-EPS?prepayRestriction(c,"full"):"");
        if(restriction||m-c.start+1<c.prepayFrom||p>l.balance+EPS||(p+EPS<c.prepayMin&&p<l.balance-EPS)){
          reject(m,c.id,(restriction||"提前还款期数、起点、余额或最低金额未获合同允许")+"，按原合同还款");continue;
        }
        const fee=p*c.prepayFee+(p>=l.balance-EPS?c.settlementFee:0),available=Math.max(0,cash-reserve);
        if(p+fee>available+EPS){reject(m,c.id,"本月可用现金扣生活、到期款和储备后不足，保留现金",p+fee-available);continue;}
        pay("prepaid",p);pay("prepayFees",fee);l.balance=Math.max(0,l.balance-p);recast(l,a.mode,m);
        if(detail)byLoan[c.id].push({month:m,prepay:p,fee,balance:l.balance,end:l.end,nextPayment:c.method==="annuity"?l.payment:null});
        event(m,c.id,"prepay","来自当月清算后的可支配现金",p);
      }
      const financial=sum(securities,z=>z.mark*z.units),property=sum(assets,z=>z.owned&&z.property?z.mark:0),
        vehicle=sum(assets,z=>z.owned&&!z.property?z.mark:0),debt=sum(loans,l=>l.balance);
      const cashIn=sum(Object.values(inc),x=>x),cashOut=sum(Object.values(out),x=>x);
      const cashResidual=cash-(open+cashIn-cashOut),net=cash+financial+receivables+property+vehicle-debt-arrears;
      const previousNet=open+oldFin+oldReal-oldDebt-oldArrears;
      const noncapitalOut=out.essential+out.discretionary+out.carry+out.replacement+out.interest+out.closingInterest+out.loanFees+out.saleFees+out.releaseFees+out.prepayFees;
      const predicted=previousNet+inc.income+inc.rent+inc.cashInterest+gains+assetDisposalDifference
        -tradeloss-called-noncapitalOut-(arrears-oldArrears);
      const netResidual=net-predicted;
      maxCashResidual=Math.max(maxCashResidual,Math.abs(cashResidual));maxNetResidual=Math.max(maxNetResidual,Math.abs(netResidual));
      if(Math.abs(cashResidual)>1e-6*Math.max(1,Math.abs(open),cashIn,cashOut)||Math.abs(netResidual)>1e-6*Math.max(1,Math.abs(net),Math.abs(predicted)))throw Error("逐月会计未勾稽，月 "+m);
      const cashIncome=inc.income+inc.rent;
      const dsr=cashIncome>EPS?regularDue/cashIncome:null,dsrInfinite=cashIncome<=EPS&&regularDue>EPS;
      if(dsr!=null)peakDsr=Math.max(peakDsr,dsr);peakDsrInfinite=peakDsrInfinite||dsrInfinite;
      if(net>peak)peak=net;drawdown=Math.max(drawdown,peak-net);
      if(peak>EPS)drawdownPct=Math.max(drawdownPct||0,(peak-net)/peak);
      maxReserveGap=Math.max(maxReserveGap,Math.max(0,reserve-cash));
      const earnedInterest=out.interest+out.closingInterest;
      interestTotal+=earnedInterest;prepaid+=out.prepaid;
      const propertyCarry=sum(assets,z=>z.owned&&z.property?z.c.carry*cpi:0);
      rentNet+=inc.rent-propertyCarry;
      if(unpaid>EPS)failed={month:m,unpaid,missedPrincipal,missedDebtService,unfundedEssential,unfundedDiscretionary};
      rows.push({month:m,openingCash:open,cash,netWorth:failed?null:net,realNetWorth:failed?null:net/cpi,bookNetWorth:net,cpi,
        financial,receivables:Math.max(0,receivables),property,vehicle,debt,arrears,regularDue,dsr,dsrInfinite,reserve,
        unpaid:firstPositive(unpaid),missedDebtService:firstPositive(missedDebtService),unfundedEssential:firstPositive(unfundedEssential),unfundedDiscretionary:firstPositive(unfundedDiscretionary),cashResidual,netResidual,...inc,...out,securityTradeFees:tradeloss,valuationGain:gains});
      if(failed)break;
    }
    function minimum(n){return rows.length>=n?Math.min(...rows.slice(0,n).map(x=>x.cash)):null;}
    const end=rows[rows.length-1],points={};
    for(const m of [12,36,60,120]){const r=rows[m-1];points[m]=r?{nominal:r.netWorth,real:r.realNetWorth,cash:r.cash,debt:r.debt,due:r.regularDue,dsr:r.dsr}:null;}
    const summary={completed:!failed,feasible:!failed&&!blocked.length&&maxReserveGap<EPS,firstFailure:failed?failed.month:null,
      failureBreakdown:failed,worstGap:failed?failed.unpaid:0,supportMonths:failed?failed.month-1:H,minCash12:minimum(12),minCash36:minimum(36),minCash120:minimum(120),
      minCashObserved:Math.min(...rows.map(r=>r.cash)),firstCash:rows[0].cash,endCash:end.cash,terminalReal:failed?null:end.realNetWorth,
      terminalNominal:failed?null:end.netWorth,endDebt:end.debt,endDue:end.regularDue,endDsr:end.dsr,endDsrInfinite:end.dsrInfinite,
      peakDsr,peakDsrInfinite,interestTotal,prepaid,rentNet,saleNet,securityNet,drawdown,drawdownPct,maxReserveGap,
      maxBlockedFunding:Math.max(0,...blocked.map(b=>b.need)),blocked,points,maxCashResidual,maxNetResidual,openingNet,arrears:end.arrears};
    if(tracePool){
      // Intern the complete cent-level ledger, not its endpoints or an approximate hash.
      const key=rows.map(r=>[r.cash,r.debt,r.financial,r.property,r.vehicle,r.rent,r.receivables,r.netWorth,r.unpaid,r.prepaid,r.saleGross,r.discretionary]
        .map(v=>v==null?"null":Math.round(v*100)).join(",")).join(";");
      if(!tracePool.has(key))tracePool.set(key,tracePool.size+1);
      summary.traceNumber=tracePool.get(key);
    }
    return detail?{summary,rows,events,byLoan,propertyFlows}:{summary};
  }
  function firstPositive(n){return n>EPS?n:0;}

  const baseStrategy=()=>({id:"S000",actions:[]});
  function enumerate(h,limit=200) {
    num(limit,"策略上限",100,500,true);
    const dims=[],exclusions=[];
    const add=(id,choices)=>{if(choices.length)dims.push({id,options:[null,...choices]});};
    const why=(id,reason)=>exclusions.push({id,reason});
    const currentEssential=expensesAt(h,1,1).reserveBase;
    const liquidOpening=Math.max(0,h.cash-currentEssential*h.reserveMonths);
    let neutralBudget=null;
    function fundingAt(month){
      if(!neutralBudget)neutralBudget=execute(h,{id:"contract_budget",by:{}},baseStrategy(),true).rows;
      const r=neutralBudget[month-1];
      return r&&!r.unpaid?Math.max(0,r.cash-r.reserve):0;
    }
    for(const p of [...h.properties,...h.vehicles]) {
      const choices=[];
      if(p.use==="idle"&&p.rent>0){
        choices.push({kind:"rent",asset:p.id,month:1,discount:false});
        if(p.discountRent>0&&p.discountRent<1&&p.discountLeaseLag<p.leaseLag)choices.push({kind:"rent",asset:p.id,month:1,discount:true});
        else why(p.id,"议租仅在可缩短空置时生成");
      }
      const restriction=saleRestriction(p);
      if(restriction||p.lock>H||p.saleLag>h.maxSaleWait||p.saleLag+p.lock>H)
        why(p.id,restriction||"出售受锁定、可接受成交期限约束");
      else{
        for(const month of new Set([p.lock,6,12]))if(month>=p.lock&&month+p.saleLag<=H)choices.push({kind:"list",asset:p.id,month});
        if(currentEssential>0)choices.push({kind:"list",asset:p.id,month:p.lock,trigger:"reserve",buffer:Math.max(3,h.reserveMonths)});
      }
      add(p.id,choices);
    }
    for(const z of h.financial){
      const restriction=securityRestriction(z);
      if(restriction||z.value<=0||z.kind==="deposit"&&z.maturity>0||z.unlock>H){
        why(z.id,restriction||"资产无市值、超出期限，或定存按到期自动兑付");continue;
      }
      const choices=[{kind:"liquidate",asset:z.id,mode:"all",month:z.unlock}];
      if(z.unlock+9<=H)choices.push({kind:"liquidate",asset:z.id,mode:"stages",month:z.unlock});
      if(currentEssential>0)for(const buffer of new Set([Math.max(3,h.reserveMonths),Math.max(6,h.reserveMonths)]))
        choices.push({kind:"liquidate",asset:z.id,mode:"reserve",month:z.unlock,buffer});
      add(z.id,choices);
    }
    for(const l of h.loans){
      const fullRestriction=prepayRestriction(l,"full"),recastRestriction=prepayRestriction(l,"recast"),shortenRestriction=prepayRestriction(l,"shorten");
      for(const reason of new Set([fullRestriction,recastRestriction,shortenRestriction].filter(Boolean)))why(l.id,reason);
      if(fullRestriction&&recastRestriction&&shortenRestriction)continue;
      if(l.principal<=EPS||l.months<2){why(l.id,"余额或到期期数不支持额外提前还款");continue;}
      const month=l.start+l.prepayFrom-1;
      if(month>=l.start+l.months-1||month>H){why(l.id,"提前还款窗口在到期或评估期以后");continue;}
      const choices=fullRestriction?[]:[{kind:"prepay",loan:l.id,month,mode:"full"}];
      const partialCap=Math.min(Math.max(liquidOpening,fundingAt(month))/(1+l.prepayFee),l.principal*.5);
      for(const frac of [.5,1]){
        const amount=Math.floor(partialCap*frac*100)/100;
        if(amount<=EPS||amount<l.prepayMin||l.method==="bullet")continue;
        for(const mode of ["recast","shorten"]){
          if(mode==="recast"?recastRestriction:shortenRestriction)continue;
          choices.push({kind:"prepay",loan:l.id,month,mode,amount});
        }
      }
      add(l.id,choices);
    }
    if(h.cutFraction>0&&h.expenses.some(e=>e.kind==="discretionary"&&e.monthly>0)){
      const choices=[{kind:"cut",month:1,fraction:h.cutFraction}];
      if(currentEssential>0)for(const buffer of new Set([Math.max(3,h.reserveMonths),Math.max(6,h.reserveMonths)]))
        choices.push({kind:"cut",month:1,fraction:h.cutFraction,trigger:"reserve",buffer});
      add("discretionary",choices);
    }
    const total=dims.reduce((a,d)=>a*BigInt(d.options.length),1n),selected=[],seen=new Set();
    function insert(digits){
      const key=digits.join(",");
      if(selected.length>=limit||seen.has(key))return;
      seen.add(key);
      const actions=digits.map((v,i)=>dims[i].options[v]).filter(Boolean);
      selected.push({id:"S"+String(selected.length).padStart(3,"0"),actions});
    }
    function decode(n){return dims.map(d=>{const b=BigInt(d.options.length),k=Number(n%b);n/=b;return k;});}
    const zeros=dims.map(()=>0);insert(zeros);
    if(total<=BigInt(limit)){for(let i=1n;i<total;i++)insert(decode(i));}
    else{
      // Round-robin one-action policies first; reserve capacity for cross-family interactions.
      const singleBudget=Math.max(1,Math.floor(limit*.38));
      const length=Math.max(1,...dims.map(d=>d.options.length));
      for(let j=1;j<length&&selected.length<singleBudget;j++)for(let k=0;k<dims.length&&selected.length<singleBudget;k++)
        if(j<dims[k].options.length){const d=zeros.slice();d[k]=j;insert(d);}
      // Cover light-touch, executable pairs before sampling the much denser full product.
      for(let depth=1;depth<length&&selected.length<Math.floor(limit*.67);depth++)
        for(let offset=1;offset<dims.length&&selected.length<Math.floor(limit*.67);offset++)
          for(let i=0;i<dims.length-offset&&selected.length<Math.floor(limit*.67);i++) {
            const j=i+offset,d=zeros.slice();
            d[i]=1+(depth-1)%(dims[i].options.length-1);d[j]=1+(depth+offset-2)%(dims[j].options.length-1);insert(d);
          }
      const slots=limit-selected.length;
      for(let k=1;k<=slots;k++)insert(decode((total-1n)*BigInt(k)/BigInt(slots)));
      // Multiplicative stride visits all indices when coprime to the exact product.
      let stride=total/BigInt(limit)+1n;
      const gcd=(a,b)=>{while(b){const c=a%b;a=b;b=c;}return a;};
      while(gcd(stride,total)!==1n)stride++;
      for(let i=0n;selected.length<limit;i++)insert(decode((i*stride)%total));
    }
    return {strategies:selected,coverage:{rawCombinations:total.toString(),evaluated:selected.length,limit,
      method:total<=BigInt(limit)?"完整笛卡尔积":"先保留基准，轮转单动作、跨资产双动作，再按混合进位全空间等距覆盖",
      dimensions:dims.map(d=>({id:d.id,choices:d.options.length})),exclusions}};
  }
  function prepare(input,scenarios) {
    if(!Array.isArray(scenarios)||!scenarios.length||scenarios.length>12)throw Error("请输入1至12个情景");
    const h=validateHousehold(input),paths=scenarios.map(s=>validateScenario(s,h.rangeCase));
    if(new Set(paths.map(s=>s.id)).size!==paths.length)throw Error("情景 ID 重复");
    return {h,scenarios:paths};
  }
  function assess(input,scenarios,limit=500){
    const p=prepare(input,scenarios),set=enumerate(p.h,limit),cache=new Map(),tracePool=new Map();
    function cached(actions,s){
      const k=s.id+"|"+JSON.stringify(actions);
      if(!cache.has(k))cache.set(k,execute(p.h,s,{actions},false,tracePool).summary);
      return cache.get(k);
    }
    const evaluated=set.strategies.map(strategy=>{
      const outcomes={};
      for(const s of p.scenarios){
        const summary={...cached(strategy.actions,s)};
        const without=strategy.actions.filter(a=>a.kind!=="prepay");
        const ref=without.length===strategy.actions.length?summary:cached(without,s);
        const comparable=summary.completed&&ref.completed&&!summary.blocked.length&&!ref.blocked.length;
        summary.interestSaved=comparable?ref.interestTotal-summary.interestTotal:null;
        summary.prepayCashChangeMonth1=summary.firstCash-ref.firstCash;
        summary.prepayMinCashChange=comparable?summary.minCash120-ref.minCash120:null;
        outcomes[s.id]=summary;
      }
      const all=Object.values(outcomes),ok=all.every(x=>x.feasible);
      return {strategy,outcomes,feasible:ok,
        minCash:ok?Math.min(...all.map(x=>x.minCash120)):null,
        worstWealth:ok?Math.min(...all.map(x=>x.terminalReal)):null,
        peakDsr:ok?Math.max(...all.map(x=>x.peakDsrInfinite?Infinity:x.peakDsr)):null,
        maxDebt:ok?Math.max(...all.map(x=>x.endDebt)):null,
        support:Math.min(...all.map(x=>x.supportMonths)),gap:Math.max(...all.map(x=>x.worstGap)),
        funding:Math.max(...all.map(x=>Math.max(x.worstGap,x.maxReserveGap,x.maxBlockedFunding))),
        blockedCount:sum(all,x=>x.blocked.length),regret:null,recoveryCost:null,pareto:false};
    });
    const groups=new Map();
    for(const r of evaluated){
      const key=p.scenarios.map(s=>r.outcomes[s.id].traceNumber).join("/");
      if(!groups.has(key))groups.set(key,"T"+String(groups.size+1).padStart(3,"0"));
      r.trajectory=groups.get(key);
    }
    const common=evaluated.filter(x=>x.feasible),best={};
    set.coverage.distinctMonthlyTrajectories=groups.size;
    set.coverage.distinctFeasibleMonthlyTrajectories=new Set(common.map(r=>r.trajectory)).size;
    for(const s of p.scenarios)best[s.id]=common.length?Math.max(...common.map(x=>x.outcomes[s.id].terminalReal)):null;
    const recovery=p.scenarios.find(s=>s.role==="recovery");
    for(const r of common){
      r.regret=Math.max(...p.scenarios.map(s=>best[s.id]-r.outcomes[s.id].terminalReal));
      r.recoveryCost=recovery?best[recovery.id]-r.outcomes[recovery.id].terminalReal:null;
    }
    for(const r of common)r.pareto=!common.some(t=>t!==r&&t.minCash>=r.minCash-EPS&&t.worstWealth>=r.worstWealth-EPS&&t.peakDsr<=r.peakDsr+EPS
      &&(t.minCash>r.minCash+EPS||t.worstWealth>r.worstWealth+EPS||t.peakDsr<r.peakDsr-EPS));
    const min=(items,c)=>items.length?items.slice().sort(c)[0].strategy.id:null;
    const preferred=(k)=>Object.values(k.outcomes).reduce((v,x)=>Math.min(v,x.endCash),Infinity);
    const winners={baseline:evaluated[0].strategy.id,
      robust:min(common,(a,b)=>b.minCash-a.minCash||b.worstWealth-a.worstWealth),
      cash:min(common,(a,b)=>b.minCash-a.minCash||preferred(b)-preferred(a)),
      regret:min(common,(a,b)=>a.regret-b.regret||b.minCash-a.minCash),
      wealth:min(common,(a,b)=>b.worstWealth-a.worstWealth||b.minCash-a.minCash),
      debt:min(common,(a,b)=>(a.peakDsr-b.peakDsr)||a.maxDebt-b.maxDebt||b.minCash-a.minCash),
      leastGap:min(evaluated,(a,b)=>a.funding-b.funding||a.blockedCount-b.blockedCount||b.support-a.support||a.gap-b.gap)};
    const ordered=rank(evaluated,p.h.preference),signatures=new Set(),shortlist=[];
    for(const r of [...Object.values(winners).map(id=>evaluated.find(x=>x.strategy.id===id)).filter(Boolean),...ordered]){
      if(!r.feasible||shortlist.includes(r.strategy.id))continue;
      // Equal cent-level outcomes across every scenario do not multiply the shortlist.
      const fingerprint=r.trajectory;
      if(signatures.has(fingerprint))continue;signatures.add(fingerprint);shortlist.push(r.strategy.id);if(shortlist.length===15)break;
    }
    return {prepared:p,results:evaluated,coverage:set.coverage,best,winners,commonCount:common.length,shortlist};
  }
  function rank(items,objective="cash"){
    const order={cash:(a,b)=>b.minCash-a.minCash,wealth:(a,b)=>b.worstWealth-a.worstWealth,
      debt:(a,b)=>a.peakDsr-b.peakDsr||a.maxDebt-b.maxDebt,regret:(a,b)=>a.regret-b.regret};
    option("排序目标",Object.keys(order),objective);
    return items.slice().sort((a,b)=>Number(b.feasible)-Number(a.feasible)||
      (a.feasible?order[objective](a,b):a.funding-b.funding||a.blockedCount-b.blockedCount||b.support-a.support)||
      a.strategy.id.localeCompare(b.strategy.id));
  }
  function simulate(input,scenario,strategy=baseStrategy()){
    const p=prepare(input,[scenario]);checkActions(p.h,strategy);return execute(p.h,p.scenarios[0],strategy,true);
  }
  function path(key,value,start=1,duration=H,target="*",sourceId="manual-stress") {
    const [mode,unit]=modes[key];
    return {key,mode,value,unit,start,duration:mode==="event"||mode==="shock"?1:duration,
      range:[value,value],target,sourceId,assumption:"stress_test",editable:true};
  }
  function describe(a){
    const t=a.trigger==="reserve"?"自第"+a.month+"月起，期初现金不超过必要支出×"+a.buffer+"时":"第"+a.month+"月";
    if(a.kind==="list")return t+"挂牌 "+a.asset;
    if(a.kind==="rent")return t+(a.discount?"议价出租 ":"出租 ")+a.asset;
    if(a.kind==="liquidate")return t+" "+a.asset+({all:"全部转为现金",stages:"分四次各减持原份额25%（相隔3个月）",reserve:"按现金缺口卖出，缓冲 "+a.buffer+" 个月"}[a.mode]);
    if(a.kind==="prepay")return t+"用可用现金"+(a.mode==="full"?"结清 ":a.mode==="recast"?"预付并降月供 ":"预付并缩期限 ")+a.loan+(a.mode==="full"?"":" "+a.amount.toLocaleString("zh-CN")+"元");
    return t+"削减可选支出 "+Math.round(a.fraction*100)+"%";
  }
  function nameOf(s){
    const phase={liquidate:0,list:1,rent:1,cut:2,prepay:3};
    return s.actions.length?s.actions.slice().sort((a,b)=>a.month-b.month||phase[a.kind]-phase[b.kind]).map(describe).join("；"):"不行动（维持原合同与持有方式）";
  }

  function reverse(input,scenario,strategy=baseStrategy(),selection={}) {
    const p=prepare(input,[scenario]),h=p.h,s=p.scenarios[0];checkActions(h,strategy);
    const wage=h.incomes.find(x=>x.id===selection.incomeId)||h.incomes.filter(i=>["wage","bonus"].includes(i.kind)).sort((a,b)=>b.monthly-a.monthly)[0];
    const property=h.properties.find(x=>x.id===selection.propertyId)||h.properties.find(x=>x.use!=="occupied");
    const loan=h.loans.find(x=>x.id===selection.loanId)||h.loans[0],security=h.financial.find(x=>x.id===selection.financialId)||h.financial.find(x=>!["deposit","instant"].includes(x.kind));
    const base=execute(h,s,strategy,true);
    const typeNames={wage:"所有工资/奖金额外下降",job:"指定收入中断",delay:"所有实物成交额外延迟",price:"房产估值与可成交价额外下跌",rent:"租金额外下降",joint:"工资、房价、租金同比例额外下调"};
    const grid={};
    function measure(key,x){
      let hh=h,ss=s;
      if(key==="wage"||key==="joint")hh={...hh,incomes:h.incomes.map(i=>["wage","bonus"].includes(i.kind)?{...i,monthly:i.monthly*(1-x/100)}:i)};
      if(key==="job"&&wage&&x>0){
        const extra=path("unemploymentMonths",x,1,1,wage.id);
        ss={...s,by:{...s.by,unemploymentMonths:[...(s.by.unemploymentMonths||[]),extra]}};
      }
      if(key==="delay")hh={...hh,properties:hh.properties.map(c=>({...c,saleLag:c.saleLag==null?null:c.saleLag+x})),vehicles:hh.vehicles.map(c=>({...c,saleLag:c.saleLag==null?null:c.saleLag+x}))};
      if(key==="rent"||key==="price"||key==="joint")hh={...hh,properties:hh.properties.map(c=>({...c,
        rent:c.rent*(key!=="price"?1-x/100:1),value:c.value*(key!=="rent"?1-x/100:1),saleValue:c.saleValue==null?null:c.saleValue*(key!=="rent"?1-x/100:1)}))};
      return execute(hh,ss,strategy).summary;
    }
    const anyWage=h.incomes.some(i=>["wage","bonus"].includes(i.kind)&&i.monthly>0);
    for(const key of Object.keys(typeNames)){
      const applicable=key==="job"?!!wage:key==="wage"?anyWage:key==="delay"?strategy.actions.some(a=>a.kind==="list"):key==="joint"?anyWage||h.properties.length>0:h.properties.length>0;
      if(!applicable){grid[key]={label:typeNames[key],applicable:false};continue;}
      const limit=key==="job"||key==="delay"?120:100;
      let boundary=null,previousSafe=null,reentry=false,firstBlocked=null;
      for(let x=0;x<=limit;x++){
        const r=measure(key,x);
        if(r.blocked.length&&firstBlocked==null)firstBlocked=x;
        if(!r.completed&&boundary===null)boundary={value:x,failureMonth:r.firstFailure,gap:r.worstGap,previousSafe};
        if(r.completed){if(boundary)reentry=true;previousSafe=x;}
      }
      grid[key]={label:typeNames[key],applicable:true,target:key==="job"?wage.id:"*",unit:limit===120?"月":"%",step:1,limit,
        boundary,nonmonotone:reentry,firstBlocked};
    }
    let affordablePrepay=null,breakEven=null,liquidation=null,payoff=null;
    const effect=(without,withAction)=>{
      const a=execute(h,s,{actions:without}).summary,b=execute(h,s,{actions:[...without,withAction]}).summary;
      return {holdingSupport:a.supportMonths,actionSupport:b.supportMonths,holdingFirstFailure:a.firstFailure,actionFirstFailure:b.firstFailure,
        holdingMinCash:a.minCashObserved,actionMinCash:b.minCashObserved,changeFirstCash:b.firstCash-a.firstCash,changeMinCash:b.minCashObserved-a.minCashObserved,
        actionFeasible:b.feasible,blocked:b.blocked};
    };
    if(security&&!securityRestriction(security)){
      const actions=strategy.actions.filter(a=>a.asset!==security.id);
      liquidation={id:security.id,...effect(actions,{kind:"liquidate",asset:security.id,month:Math.min(H,security.unlock),mode:"all"})};
    }
    if(loan&&loan.prepayFrom!=null){
      const actions=strategy.actions.filter(a=>!(a.kind==="prepay"&&a.loan===loan.id));
      const keep=execute(h,s,{actions},true),month=loan.start+loan.prepayFrom-1,r=keep.rows[month-1];
      const ld=(keep.byLoan[loan.id]||[]).find(t=>t.month===month&&"principal" in t);
      // A bullet may have no installment at zero interest; track its contractual opening balance.
      const balance=ld?ld.balance:(loan.method==="bullet"&&month<loan.start+loan.months-1?loan.principal:0);
      if(month<=H)payoff={id:loan.id,...effect(actions,{kind:"prepay",loan:loan.id,month,mode:"full"})};
      if(r&&balance>EPS&&["full","recast","shorten"].some(mode=>!prepayRestriction(loan,mode))){
        const upper=Math.min(balance,Math.max(0,r.cash-r.reserve)/(1+loan.prepayFee)),mode=loan.allowRecast?"recast":loan.allowShorten?"shorten":null;
        const works=x=>{
          if(x<=EPS)return keep.summary.feasible;
          const useMode=x>=balance-EPS?"full":mode;
          if(!useMode||loan.method==="bullet"&&useMode!=="full")return false;
          return execute(h,s,{actions:[...actions,{kind:"prepay",loan:loan.id,month,amount:x,mode:useMode}]}).summary.feasible;
        };
        const candidates=[0,upper,Math.min(upper,loan.prepayMin)];
        for(let j=1;j<50;j++)candidates.push(upper*j/50);
        const tests=[...new Set(candidates)].sort((a,b)=>a-b).map(x=>({x,ok:works(x)}));
        let last=tests.filter(t=>t.ok).at(-1),next=last?tests.find(t=>t.x>last.x):null;
        if(last&&next&&next.x>last.x+.01){
          let lo=last.x,hi=next.x;
          for(let j=0;j<45&&hi-lo>.002;j++){const mid=(lo+hi)/2;if(works(mid))lo=mid;else hi=mid;}
          last={x:lo};
        }
        // A non-cent contractual payoff can be rounded to cents only for display.
        const cap=last?last.x:null;
        affordablePrepay={id:loan.id,month,mode,largestTested:cap,liquidityCeiling:upper,balance,
          coarseStep:upper/50,baselineFeasible:keep.summary.feasible};
      } else affordablePrepay={id:loan.id,month,largestTested:null,reason:prepayRestriction(loan,"full")||"窗口无可测试余额或现金已截断"};
    }else if(loan)affordablePrepay={id:loan.id,month:null,largestTested:null,reason:"提前还款窗口尚未确认，维持原合同"};
    if(property&&property.use!=="occupied"&&!saleRestriction(property)&&property.lock<=H){
      const other=strategy.actions.filter(a=>a.asset!==property.id),list={kind:"list",asset:property.id,month:property.lock};
      const sold=execute(h,s,{actions:[...other,list]},true),close=sold.events.find(e=>e.asset===property.id&&e.type==="close");
      const lease=property.use==="idle"?[...other,{kind:"rent",asset:property.id,month:1,discount:false}]:other;
      const tested=(rent,detail=false)=>execute({...h,properties:h.properties.map(c=>c.id===property.id?{...c,rent}:c)},s,{actions:lease},detail);
      const upper=Math.max(property.rent*4,property.saleValue/12,1),initial=tested(property.rent,true), flow=initial.propertyFlows[property.id];
      breakEven={id:property.id,term:H,actualMonthlyNet:(flow.rent-flow.carry)/initial.rows.length,
        saleNet:close?close.amount:null,saleMonth:close?close.month:null,currentHoldReal:initial.summary.terminalReal,sellReal:sold.summary.terminalReal,
        grossMonthlyThreshold:null,netMonthlyThreshold:null,testedRange:[0,upper],reason:""};
      if(sold.summary.feasible&&close){
        const beats=rent=>{const r=tested(rent).summary;return r.feasible&&r.terminalReal>=sold.summary.terminalReal;};
        if(beats(upper)){
          let lo=0,hi=upper;
          if(beats(lo))hi=0;
          else for(let i=0;i<55&&hi-lo>.004;i++){const mid=(hi+lo)/2;if(beats(mid))hi=mid;else lo=mid;}
          const detail=tested(hi,true),f=detail.propertyFlows[property.id];breakEven.grossMonthlyThreshold=hi;breakEven.netMonthlyThreshold=(f.rent-f.carry)/H;
        }else breakEven.reason="所列租金区间内未同时满足现金约束并达到出售路径的十年实际净资产";
      }else breakEven.reason="立即依法挂牌路径未成交，或未通过现金/合同/储备约束";
    }
    return {grid,base:base.summary,affordablePrepay,breakEven,liquidation,payoff};
  }
  return {H,templates,blank,baseStrategy,modes,path,prepare,validateHousehold,validateScenario,enumerate,
    assess,simulate,rank,reverse,describe,nameOf,amortPayment,
    inspect:(study,strategyId,scenarioId)=>{
      const r=study.results.find(r=>r.strategy.id===strategyId),s=study.prepared.scenarios.find(s=>s.id===scenarioId);
      if(!r||!s)throw Error("方案或情景不存在");return execute(study.prepared.h,s,r.strategy,true);
    }};
});
